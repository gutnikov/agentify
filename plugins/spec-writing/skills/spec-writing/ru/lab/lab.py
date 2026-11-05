#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Стенд для промптов плейбука: пишущий агент → ревьюер → сверка с заданием → сводка.

    python3 lab.py write  --run r1 [--prompt ../writing-a-text.md] [--split dev] [--model sonnet] [--effort medium]
    python3 lab.py revise --run r1-rev --source r1      # одна правка писателем по находкам ревью
    python3 lab.py review --run r1                      # ревьюер из ../review/
    python3 lab.py check  --run r1                      # сверка с заданием: выдуманные и пропущенные факты
    python3 lab.py score  --run r1 [--vs baseline]

Писатель изолирован: --safe-mode, без инструментов, запуск из пустой папки sandbox/, системный промпт — только
промпт писателя. Подробности — в README.md.
"""
import argparse
import collections
import concurrent.futures
import json
import os
import re
import subprocess
import sys

LAB = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK = os.path.dirname(LAB)
REVIEW = os.path.join(PLAYBOOK, 'review')
WRITER_PROMPT = os.path.join(PLAYBOOK, 'writing-a-text.md')
FACTS_PROMPT = os.path.join(PLAYBOOK, 'checking-facts.md')
REVISE_PROMPT = os.path.join(PLAYBOOK, 'revising-a-text.md')
REVIEWER_PROMPT = os.path.join(REVIEW, 'reviewer-prompt.md')
CATALOG = os.path.join(REVIEW, 'error-patterns.md')
SCANNER = os.path.join(REVIEW, 'text_scan.py')
SANDBOX = os.path.join(LAB, 'sandbox')
BRIEFS = os.path.join(LAB, 'briefs.jsonl')
RUNS = os.path.join(LAB, 'runs')

WRITER_USER = 'Задание:\n{task}\n\nВерни только готовый текст в markdown, без пояснений и комментариев.'

REVISE_USER = 'Задание:\n{task}\n\nТвой текст:\n{text}\n\nРедактор проверил текст и нашёл проблемы:\n{findings}\n\n'

# Сессии Claude Code получают email пользователя, и писатель иногда подписывает текст названием компании из него.
# В рабочей среде писателя этого нет, поэтому сверка такие названия не считает.
CHECK_LAB_NOTE = ('\n\nНазвание компании или приложения (например, Vivid) не отмечай: автор знает его из своего окружения.')

REVIEW_ADDENDUM = """

# Режим тестирования

Ты работаешь в автоматическом прогоне на тест-сете.
- Каталог ошибок приведён ниже целиком — не читай файл error-patterns.md повторно.
- Текст для проверки лежит в файле, путь дан в сообщении. Прочитай его и запусти `python3 text_scan.py <файл>` из папки review/.
- Верни отчёт только в формате JSON по схеме из раздела «Формат отчёта (JSON, по запросу)», без markdown и без пояснений вокруг.
"""

REPORT_SCHEMA = {
    'type': 'object',
    'required': ['findings'],
    'properties': {
        'text': {'type': 'object'},
        'summary': {'type': 'object'},
        'findings': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['code', 'severity', 'locations', 'problem'],
                'properties': {
                    'rank': {'type': 'integer'},
                    'code': {'type': 'string'},
                    'title': {'type': 'string'},
                    'severity': {'type': 'integer'},
                    'locations': {
                        'type': 'array',
                        'items': {'type': 'object', 'properties': {'ref': {'type': 'string'},
                                                                   'quote': {'type': 'string'}}},
                    },
                    'problem': {'type': 'string'},
                    'chapter': {'type': 'string'},
                },
            },
        },
        'doubtful': {'type': 'array'},
    },
}

CHECK_SCHEMA = {
    'type': 'object',
    'required': ['invented', 'missing'],
    'properties': {
        'invented': {'type': 'array', 'items': {'type': 'object', 'required': ['quote', 'why'],
                                                'properties': {'quote': {'type': 'string'}, 'why': {'type': 'string'}}}},
        'missing': {'type': 'array', 'items': {'type': 'object', 'required': ['fact', 'why'],
                                               'properties': {'fact': {'type': 'string'}, 'why': {'type': 'string'}}}},
    },
}

REVISE_SCHEMA = {
    'type': 'object',
    'required': ['text', 'unresolved'],
    'properties': {
        'text': {'type': 'string'},
        'unresolved': {'type': 'array', 'items': {'type': 'object', 'required': ['code', 'missing_fact'],
                                                  'properties': {'code': {'type': 'string'},
                                                                 'missing_fact': {'type': 'string'}}}},
    },
}

SEVERITY = {'критично': 1, 'серьёзно': 2, 'серьезно': 2, 'заметно': 3, 'шлифовка': 4}
SEV_W = {1: 4, 2: 3, 3: 2, 4: 1}


def read(path):
    return open(path, encoding='utf-8').read().strip()


def load_briefs(split=None, ids=None):
    out = [json.loads(l) for l in open(BRIEFS, encoding='utf-8') if l.strip()]
    if split:
        out = [b for b in out if b['split'] == split]
    if ids:
        want = set(ids.split(','))
        out = [b for b in out if b['id'] in want]
    return out


def run_claude(cmd, cwd, timeout):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, '', 'timeout'
    try:
        return json.loads(proc.stdout), proc.stdout, proc.stderr[-2000:]
    except ValueError:
        return None, proc.stdout, proc.stderr[-2000:]


def extract_json(text):
    text = text.strip()
    m = re.search(r'```(?:json)?\s*(.*?)```', text, re.S)
    if m:
        text = m.group(1).strip()
    start = min([i for i in (text.find('{'), text.find('[')) if i >= 0] or [0])
    return json.loads(text[start:])


def inconsistent(report):
    """Сводка не сходится со списком находок: модель сбилась при генерации JSON."""
    summary = report.get('summary') or {}
    n = len(report.get('findings') or [])
    if isinstance(summary.get('total'), int) and summary['total'] != n:
        return True
    try:
        by_sev = sum(int(v) for v in (summary.get('by_severity') or {}).values())
    except (TypeError, ValueError):
        return False
    return bool(summary.get('by_severity')) and by_sev != n


def strip_fences(text):
    t = text.strip()
    m = re.match(r'^```(?:markdown|md)?\s*\n(.*)\n```$', t, re.S)
    return (m.group(1) if m else t).strip()


def pmap(fn, items, jobs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        for n, res in enumerate(pool.map(fn, items), 1):
            print('[%d/%d] %s' % (n, len(items), res), flush=True)


# ---------------------------------------------------------------- write

def cmd_write(a):
    run = os.path.join(RUNS, a.run)
    os.makedirs(os.path.join(run, 'texts'), exist_ok=True)
    os.makedirs(os.path.join(run, 'meta'), exist_ok=True)
    os.makedirs(SANDBOX, exist_ok=True)
    prompt = read(a.prompt)
    with open(os.path.join(run, 'writer-prompt.md'), 'w', encoding='utf-8') as f:
        f.write(prompt + '\n')
    briefs = load_briefs(a.split, a.ids)
    todo = [b for b in briefs if a.force or not os.path.exists(os.path.join(run, 'texts', b['id'] + '.md'))]

    def one(b):
        cmd = ['claude', '-p', WRITER_USER.format(task=b['task']), '--safe-mode', '--tools', '',
               '--model', a.model, '--effort', a.effort, '--system-prompt', prompt,
               '--output-format', 'json', '--no-session-persistence']
        outer, raw, err = run_claude(cmd, SANDBOX, a.timeout)
        if not outer or outer.get('is_error'):
            return '%s ОШИБКА %s %s' % (b['id'], err[-300:], raw[-300:])
        text = strip_fences(outer.get('result', ''))
        with open(os.path.join(run, 'texts', b['id'] + '.md'), 'w', encoding='utf-8') as f:
            f.write(text + '\n')
        meta = {'cost_usd': outer.get('total_cost_usd'), 'duration_ms': outer.get('duration_ms'),
                'model': a.model, 'effort': a.effort, 'chars': len(text)}
        json.dump(meta, open(os.path.join(run, 'meta', b['id'] + '.json'), 'w'), ensure_ascii=False)
        return '%s ok %d зн. $%.3f' % (b['id'], len(text), meta['cost_usd'] or 0)

    print('писатель: %s/%s, заданий: %d' % (a.model, a.effort, len(todo)))
    pmap(one, todo, a.jobs)


# ---------------------------------------------------------------- revise

def format_findings(report):
    out = []
    for n, f in enumerate(report.get('findings') or [], 1):
        where = '; '.join('%s — «%s»' % (l.get('ref', ''), l.get('quote', '')) for l in f.get('locations') or [])
        out.append('%d. %s · %s (серьёзность %s)\n   Где: %s\n   Что не так: %s' % (
            n, f.get('code', ''), f.get('title', ''), f.get('severity', ''), where, f.get('problem', '')))
    return '\n'.join(out)


def cmd_revise(a):
    src = os.path.join(RUNS, a.source)
    run = os.path.join(RUNS, a.run)
    for d in ('texts', 'meta'):
        os.makedirs(os.path.join(run, d), exist_ok=True)
    os.makedirs(SANDBOX, exist_ok=True)
    prompt = read(a.prompt)
    instruction = read(REVISE_PROMPT)
    briefs = [b for b in load_briefs(a.split, a.ids) if os.path.exists(os.path.join(src, 'reviews', b['id'] + '.json'))]
    todo = [b for b in briefs if a.force or not os.path.exists(os.path.join(run, 'texts', b['id'] + '.md'))]

    def one(b):
        text = read(os.path.join(src, 'texts', b['id'] + '.md'))
        report = json.load(open(os.path.join(src, 'reviews', b['id'] + '.json'), encoding='utf-8'))
        meta = {'source': a.source, 'revised': False, 'findings_in': len(report.get('findings') or [])}
        if report.get('findings'):
            user = REVISE_USER.format(task=b['task'], text=text, findings=format_findings(report)) + instruction
            cmd = ['claude', '-p', user, '--safe-mode', '--tools', '', '--model', a.model, '--effort', a.effort,
                   '--system-prompt', prompt, '--output-format', 'json', '--no-session-persistence',
                   '--json-schema', json.dumps(REVISE_SCHEMA, ensure_ascii=False)]
            outer, raw, err = run_claude(cmd, SANDBOX, a.timeout)
            rep = (outer or {}).get('structured_output')
            if not rep:
                return '%s ОШИБКА %s' % (b['id'], (err or raw)[-300:])
            text = strip_fences(rep['text'])
            meta.update(revised=True, unresolved=rep['unresolved'], cost_usd=outer.get('total_cost_usd'),
                        duration_ms=outer.get('duration_ms'))
        meta['chars'] = len(text)
        with open(os.path.join(run, 'texts', b['id'] + '.md'), 'w', encoding='utf-8') as f:
            f.write(text + '\n')
        json.dump(meta, open(os.path.join(run, 'meta', b['id'] + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        return '%s %s' % (b['id'], ('правка, не закрыть без фактов: %d' % len(meta['unresolved']))
                          if meta['revised'] else 'без находок, не трогаю')

    pmap(one, todo, a.jobs)


# ---------------------------------------------------------------- review

def reviewer_system():
    return (read(REVIEWER_PROMPT) + REVIEW_ADDENDUM +
            '\n\n# Каталог ошибок (error-patterns.md)\n\n' + read(CATALOG))


def cmd_review(a):
    run = os.path.join(RUNS, a.run)
    os.makedirs(os.path.join(run, 'reviews'), exist_ok=True)
    system = reviewer_system()
    briefs = [b for b in load_briefs(a.split, a.ids) if os.path.exists(os.path.join(run, 'texts', b['id'] + '.md'))]
    todo = [b for b in briefs if a.force or not os.path.exists(os.path.join(run, 'reviews', b['id'] + '.json'))]

    def call(b):
        path = os.path.join(run, 'texts', b['id'] + '.md')
        user = 'Проверь текст из файла %s.\nКонтекст: %s.\nВерни отчёт только в JSON.' % (path, b['context'])
        cmd = ['claude', '-p', user, '--output-format', 'json', '--append-system-prompt', system,
               '--allowedTools', 'Read', 'Bash(python3 text_scan.py:*)',
               '--json-schema', json.dumps(REPORT_SCHEMA, ensure_ascii=False),
               '--add-dir', run, '--no-session-persistence']
        if a.model:
            cmd += ['--model', a.model]
        outer, raw, err = run_claude(cmd, REVIEW, a.timeout)
        report = None
        if outer:
            report = outer.get('structured_output')
            if report is None:
                try:
                    report = extract_json(outer.get('result', ''))
                except (ValueError, TypeError):
                    report = None
        return report, (outer or {}).get('total_cost_usd') or 0

    def one(b):
        report, cost = call(b)
        if report is None or inconsistent(report):
            report, cost2 = call(b)
            cost += cost2
        if report is None:
            return '%s НЕТ ОТЧЁТА' % b['id']
        report['_cost_usd'] = cost
        json.dump(report, open(os.path.join(run, 'reviews', b['id'] + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        return '%s ok находок %d $%.2f' % (b['id'], len(report.get('findings') or []), cost)

    print('ревьюер: %s, текстов: %d' % (a.model or 'по умолчанию', len(todo)))
    if todo and not a.no_warmup:
        print('прогрев кэша:', one(todo[0]), flush=True)
        todo = todo[1:]
    pmap(one, todo, a.jobs)


# ---------------------------------------------------------------- check

def cmd_check(a):
    run = os.path.join(RUNS, a.run)
    os.makedirs(os.path.join(run, 'checks'), exist_ok=True)
    os.makedirs(SANDBOX, exist_ok=True)
    system = read(FACTS_PROMPT) + CHECK_LAB_NOTE
    briefs = [b for b in load_briefs(a.split, a.ids) if os.path.exists(os.path.join(run, 'texts', b['id'] + '.md'))]
    todo = [b for b in briefs if a.force or not os.path.exists(os.path.join(run, 'checks', b['id'] + '.json'))]

    def one(b):
        text = read(os.path.join(run, 'texts', b['id'] + '.md'))
        user = 'ЗАДАНИЕ:\n%s\n\nТЕКСТ:\n%s' % (b['task'], text)
        cmd = ['claude', '-p', user, '--safe-mode', '--tools', '', '--model', a.model, '--effort', 'high',
               '--system-prompt', system, '--output-format', 'json', '--no-session-persistence',
               '--json-schema', json.dumps(CHECK_SCHEMA, ensure_ascii=False)]
        outer, raw, err = run_claude(cmd, SANDBOX, a.timeout)
        rep = (outer or {}).get('structured_output')
        if rep is None:
            return '%s ОШИБКА %s' % (b['id'], (err or raw)[-300:])
        json.dump(rep, open(os.path.join(run, 'checks', b['id'] + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        return '%s выдумано %d, пропущено %d' % (b['id'], len(rep['invented']), len(rep['missing']))

    pmap(one, todo, a.jobs)


# ---------------------------------------------------------------- score

def scan_counts(path):
    proc = subprocess.run([sys.executable, '-I', SCANNER, path, '--json'],
                          cwd=REVIEW, capture_output=True, text=True, timeout=120)
    data = json.loads(proc.stdout)
    return collections.Counter(f['code'] for f in data['findings'] if not f['code'].startswith('SIGNAL'))


def load_run(name, split=None, ids=None):
    run = os.path.join(RUNS, name)
    rows = []
    for b in load_briefs(split, ids):
        rp = os.path.join(run, 'reviews', b['id'] + '.json')
        tp = os.path.join(run, 'texts', b['id'] + '.md')
        if not os.path.exists(rp):
            continue
        rep = json.load(open(rp, encoding='utf-8'))
        fs = rep.get('findings') or []
        sev = collections.Counter()
        codes = collections.Counter()
        locs = 0
        for f in fs:
            s = f.get('severity')
            if isinstance(s, str):
                s = SEVERITY.get(s.strip().lower())
            sev[s] += 1
            codes[f.get('code', '?')] += 1
            locs += max(1, len(f.get('locations') or []))
        chk = os.path.join(run, 'checks', b['id'] + '.json')
        chk = json.load(open(chk, encoding='utf-8')) if os.path.exists(chk) else None
        text = open(tp, encoding='utf-8').read()
        rows.append(dict(id=b['id'], n=len(fs), locs=locs, sev=sev, codes=codes,
                         weighted=sum(SEV_W.get(k, 0) * v for k, v in sev.items()),
                         invented=len(chk['invented']) if chk else None,
                         missing=len(chk['missing']) if chk else None,
                         chars=len(text), scan=scan_counts(tp)))
    return rows


def summarize(rows):
    n = float(len(rows)) or 1
    codes = collections.Counter()
    texts_with = collections.Counter()
    sev = collections.Counter()
    for r in rows:
        codes.update(r['codes'])
        texts_with.update(set(r['codes']))
        sev.update(r['sev'])
    chk = [r for r in rows if r['invented'] is not None]
    return dict(
        texts=len(rows),
        findings_per_text=sum(r['n'] for r in rows) / n,
        locations_per_text=sum(r['locs'] for r in rows) / n,
        weighted_per_text=sum(r['weighted'] for r in rows) / n,
        sev={k: sev[k] / n for k in (1, 2, 3, 4)},
        clean_texts=sum(1 for r in rows if r['n'] == 0),
        invented_per_text=(sum(r['invented'] for r in chk) / float(len(chk))) if chk else None,
        missing_per_text=(sum(r['missing'] for r in chk) / float(len(chk))) if chk else None,
        chars=sum(r['chars'] for r in rows) / n,
        scan_per_text=sum(sum(r['scan'].values()) for r in rows) / n,
        codes=codes, texts_with=texts_with,
    )


def cmd_score(a):
    rows = load_run(a.run, a.split, a.ids)
    other = obyid = None
    if a.vs:
        ids = {r['id'] for r in rows}
        orows = [r for r in load_run(a.vs, a.split, a.ids) if r['id'] in ids]
        rows = [r for r in rows if r['id'] in {o['id'] for o in orows}]
        other = summarize(orows)
        obyid = {r['id']: r for r in orows}
    s = summarize(rows)

    def fmt(v):
        return '—' if v is None else ('%.2f' % v if isinstance(v, float) else str(v))

    def col(key):
        return (' %s |' % fmt(other[key])) if other else ''

    lines = ['# %s%s' % (a.run, (' против %s' % a.vs) if a.vs else ''), '',
             '| Метрика | %s |%s' % (a.run, (' %s |' % a.vs) if other else ''),
             '|---|---|%s' % ('---|' if other else '')]
    for key, label in [('texts', 'Текстов'), ('findings_per_text', 'Находок на текст'),
                       ('locations_per_text', 'Мест на текст'), ('weighted_per_text', 'Взвешенно (1→4, 2→3, 3→2, 4→1)'),
                       ('clean_texts', 'Текстов без находок'), ('invented_per_text', 'Выдумано фактов на текст'),
                       ('missing_per_text', 'Пропущено важных фактов на текст'), ('chars', 'Знаков в тексте'),
                       ('scan_per_text', 'Кандидатов text_scan на текст')]:
        lines.append('| %s | %s |%s' % (label, fmt(s[key]), col(key)))
    for k, lab in ((1, 'критично'), (2, 'серьёзно'), (3, 'заметно'), (4, 'шлифовка')):
        lines.append('| …%s на текст | %.2f |%s' % (lab, s['sev'][k], (' %.2f |' % other['sev'][k]) if other else ''))
    lines += ['', '## Коды (находок всего · текстов с кодом)', '',
              '| Код | %s |%s' % (a.run, (' %s |' % a.vs) if other else ''), '|---|---|%s' % ('---|' if other else '')]
    allc = set(s['codes']) | (set(other['codes']) if other else set())
    for c in sorted(allc, key=lambda c: -(s['codes'][c] + (other['codes'][c] if other else 0))):
        lines.append('| %s | %d · %d |%s' % (c, s['codes'][c], s['texts_with'][c],
                                             (' %d · %d |' % (other['codes'][c], other['texts_with'][c])) if other else ''))
    lines += ['', '## По текстам', '',
              '| id | находок | взв. | выдумано | пропущено | знаков | коды |%s' % (' было находок |' if other else ''),
              '|---|---|---|---|---|---|---|%s' % ('---|' if other else '')]
    for r in rows:
        lines.append('| %s | %d | %d | %s | %s | %d | %s |%s' % (
            r['id'], r['n'], r['weighted'], fmt(r['invented']), fmt(r['missing']), r['chars'],
            ', '.join('%s%s' % (c, '×%d' % v if v > 1 else '') for c, v in r['codes'].most_common()),
            (' %d |' % obyid[r['id']]['n']) if other else ''))
    out = '\n'.join(lines) + '\n'
    print(out)
    with open(os.path.join(RUNS, a.run, 'score%s.md' % (('-vs-' + a.vs) if a.vs else '')), 'w', encoding='utf-8') as f:
        f.write(out)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ('write', 'revise', 'review', 'check', 'score'):
        q = sub.add_parser(name)
        q.add_argument('--run', required=True)
        q.add_argument('--split', choices=('dev', 'test'))
        q.add_argument('--ids')
        q.add_argument('--jobs', type=int, default=6)
        q.add_argument('--timeout', type=int, default=1200)
        q.add_argument('--force', action='store_true')
        if name in ('write', 'revise'):
            q.add_argument('--prompt', default=WRITER_PROMPT, help='промпт писателя (по умолчанию ../writing-a-text.md)')
            q.add_argument('--model', default='sonnet')
            q.add_argument('--effort', default='medium')
        if name == 'revise':
            q.add_argument('--source', required=True, help='прогон, тексты и ревью которого правим')
        if name == 'review':
            q.add_argument('--model', default='opus')
            q.add_argument('--no-warmup', action='store_true')
        if name == 'check':
            q.add_argument('--model', default='sonnet')
        if name == 'score':
            q.add_argument('--vs')
    a = p.parse_args()
    {'write': cmd_write, 'revise': cmd_revise, 'review': cmd_review, 'check': cmd_check, 'score': cmd_score}[a.cmd](a)


if __name__ == '__main__':
    main()
