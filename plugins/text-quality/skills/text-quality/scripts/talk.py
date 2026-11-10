#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Шаги скила text-quality для одного текста — так же, как их запускает <пакет>/lab/lab.py.

    python3 talk.py new --lang ru|en [--name slug]   создать папку прогона, напечатать путь
    python3 talk.py check-brief RUN                  brief.md → questions.json: до 5 вопросов автору
    python3 talk.py write RUN                        brief.md → text.md
    python3 talk.py check RUN --context "…"          text.md → facts.json и review.json, параллельно
    python3 talk.py check RUN --facts-only           только сверка с заданием (после правки)
    python3 talk.py revise RUN                       одна правка: ревью 1–2 + выдуманное и пропущенное
                                                     из сверки → text.md (прежний — text.vN.md)

RUN — папка прогона; brief.md в ней пишет агент, язык записан в lang.txt.
Писатель, проверка задания, сверка и правка запускаются изолированно: из пустой
папки, `--safe-mode`, без инструментов, только их промпт. Ревьюер — из
<пакет>/review/ с Read и text_scan.py.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import NoReturn

SKILL = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def runs_dir():
    """Папка прогонов: TEXT_QUALITY_RUNS_DIR (или прежняя SPEC_RUNS_DIR), иначе .text-quality-runs/ в корне
    git-репозитория текущей папки, иначе в ней самой."""
    runs = os.environ.get('TEXT_QUALITY_RUNS_DIR') or os.environ.get('SPEC_RUNS_DIR')
    if runs:
        return os.path.abspath(runs)
    try:
        top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True,
                             check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        top = ''
    return os.path.join(top or os.getcwd(), '.text-quality-runs')


RUNS = runs_dir()

# Сообщения — как в lab/lab.py каждого пакета (ru/, en/): на них шли замеры.
LANGS = {
    'ru': {
        'dir': os.environ.get('TEXT_QUALITY_RU_DIR') or os.environ.get('SPEC_RU_DIR') or os.path.join(SKILL, 'ru'),
        'writer_user': 'Задание:\n{task}\n\nВерни только готовый текст в markdown, без пояснений и комментариев.',
        'brief_user': 'Задание:\n{task}',
        'facts_user': 'ЗАДАНИЕ:\n{task}\n\nТЕКСТ:\n{text}',
        'revise_user': 'Задание:\n{task}\n\nТвой текст:\n{text}\n\nРедактор проверил текст и нашёл проблемы:\n{findings}\n\n',
        'review_user': 'Проверь текст из файла {path}.\nКонтекст: {context}.\nВерни отчёт только в JSON.',
        'review_addendum': """

# Режим запуска

Ты работаешь в автоматическом прогоне.
- Каталог ошибок приведён ниже целиком — не читай файл error-patterns.md повторно.
- Текст для проверки лежит в файле, путь дан в сообщении. Прочитай его и запусти `python3 text_scan.py <файл>` из папки review/.
- Верни отчёт только в формате JSON по схеме из раздела «Формат отчёта (JSON, по запросу)», без markdown и без пояснений вокруг.
""",
        'catalog_heading': '\n\n# Каталог ошибок (error-patterns.md)\n\n',
        'finding': '%d. %s · %s (серьёзность %s)\n   Где: %s\n   Что не так: %s',
        'location': '%s — «%s»',
        'invented': ('Факта нет в задании', ' Убери утверждение; не заменяй его другим фактом.'),
        'missing': ('Нет факта из задания', 'весь текст',
                    'В тексте нет факта из задания: %s. %s Добавь его туда, где он нужен читателю.'),
    },
    'en': {
        'dir': os.environ.get('TEXT_QUALITY_EN_DIR') or os.environ.get('SPEC_EN_DIR') or os.path.join(SKILL, 'en'),
        'writer_user': 'Brief:\n{task}\n\nReturn only the finished text in markdown, with no explanations or comments.',
        'brief_user': 'Brief:\n{task}',
        'facts_user': 'BRIEF:\n{task}\n\nTEXT:\n{text}',
        'revise_user': 'Brief:\n{task}\n\nYour text:\n{text}\n\nAn editor reviewed the text and found problems:\n{findings}\n\n',
        'review_user': 'Review the text in the file {path}.\nContext: {context}.\nReturn the report as JSON only.',
        'review_addendum': """

# Run mode

You are working in an automated run.
- The full error catalogue is given below — do not read error-patterns.md again.
- The text to review is in a file; its path is in the message. Read it and run `python3 text_scan.py <file>` from the review/ folder.
- Return the report only as JSON, in the schema from the section "Report format (JSON, on request)", with no markdown and no explanations around it.
""",
        'catalog_heading': '\n\n# Error catalogue (error-patterns.md)\n\n',
        'finding': '%d. %s · %s (severity %s)\n   Where: %s\n   What is wrong: %s',
        'location': '%s — "%s"',
        'invented': ('Fact not in the brief', ' Remove the claim; do not replace it with another fact.'),
        'missing': ('Fact from the brief is missing', 'whole text',
                    'The text lacks a fact from the brief: %s. %s Add it where the reader needs it.'),
    },
}

QUESTIONS_SCHEMA = {'type': 'object', 'required': ['questions'],
                    'properties': {'questions': {'type': 'array', 'items': {'type': 'string'}}}}
CHECK_SCHEMA = {
    'type': 'object', 'required': ['invented', 'missing'],
    'properties': {
        'invented': {'type': 'array', 'items': {'type': 'object', 'required': ['quote', 'why'],
                                                'properties': {'quote': {'type': 'string'}, 'why': {'type': 'string'}}}},
        'missing': {'type': 'array', 'items': {'type': 'object', 'required': ['fact', 'why'],
                                               'properties': {'fact': {'type': 'string'}, 'why': {'type': 'string'}}}},
    },
}
REVISE_SCHEMA = {
    'type': 'object', 'required': ['text', 'unresolved'],
    'properties': {
        'text': {'type': 'string'},
        'unresolved': {'type': 'array', 'items': {'type': 'object', 'required': ['code', 'missing_fact'],
                                                  'properties': {'code': {'type': 'string'},
                                                                 'missing_fact': {'type': 'string'}}}},
    },
}
REPORT_SCHEMA = {
    'type': 'object', 'required': ['findings'],
    'properties': {
        'text': {'type': 'object'},
        'summary': {'type': 'object'},
        'findings': {'type': 'array', 'items': {
            'type': 'object', 'required': ['code', 'severity', 'locations', 'problem'],
            'properties': {
                'rank': {'type': 'integer'}, 'code': {'type': 'string'}, 'title': {'type': 'string'},
                'severity': {'type': 'integer'},
                'locations': {'type': 'array', 'items': {'type': 'object', 'properties': {
                    'ref': {'type': 'string'}, 'quote': {'type': 'string'}}}},
                'problem': {'type': 'string'}, 'chapter': {'type': 'string'},
            }}},
        'doubtful': {'type': 'array'},
    },
}


class Pack:
    """Файлы языкового пакета (ru/ или en/) и его сообщения."""

    def __init__(self, lang):
        self.lang = lang
        self.cfg = LANGS[lang]
        d = self.cfg['dir']
        self.review = os.path.join(d, 'review')
        self.writer = os.path.join(d, 'writing-a-text.md')
        self.brief = os.path.join(d, 'checking-a-brief.md')
        self.facts = os.path.join(d, 'checking-facts.md')
        self.revise = os.path.join(d, 'revising-a-text.md')
        self.reviewer = os.path.join(self.review, 'reviewer-prompt.md')
        self.catalog = os.path.join(self.review, 'error-patterns.md')
        missing = [p for p in (self.writer, self.brief, self.facts, self.revise, self.reviewer, self.catalog)
                   if not os.path.exists(p)]
        if missing:
            sys.exit('пакет %s неполный, нет: %s' % (lang, ', '.join(missing)))

    def __getitem__(self, key):
        return self.cfg[key]


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read().strip()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text if text.endswith('\n') else text + '\n')


def dump(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def need(path, hint) -> None:
    if not os.path.exists(path):
        sys.exit('нет %s — %s' % (path, hint))


def strip_fences(text):
    t = text.strip()
    m = re.match(r'^```(?:markdown|md)?\s*\n(.*)\n```$', t, re.S)
    return (m.group(1) if m else t).strip()


def log_cost(run, step, outer):
    entry = {'step': step, 'at': datetime.datetime.now().isoformat(timespec='seconds'),
             'cost_usd': (outer or {}).get('total_cost_usd'), 'duration_ms': (outer or {}).get('duration_ms')}
    with open(os.path.join(run, 'costs.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry['cost_usd'] or 0


def claude(args, cwd, timeout, schema=None):
    """Один вызов `claude -p`; возвращает (structured_output или result, outer)."""
    cmd = ['claude', '-p'] + args + ['--output-format', 'json', '--no-session-persistence']
    if schema:
        cmd += ['--json-schema', json.dumps(schema, ensure_ascii=False)]
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return None, {'error': 'timeout %ss' % timeout}
    try:
        outer = json.loads(proc.stdout)
    except ValueError:
        return None, {'error': (proc.stderr or proc.stdout)[-1500:]}
    if outer.get('is_error'):
        return None, outer
    return (outer.get('structured_output') if schema else outer.get('result')), outer


def isolated(prompt, user, model, effort, timeout, schema=None):
    """Писатель, проверка задания, сверка, правка: пустая папка, safe mode, без инструментов."""
    sandbox = tempfile.mkdtemp(prefix='talk-')
    try:
        return claude([user, '--safe-mode', '--tools', '', '--model', model, '--effort', effort,
                       '--system-prompt', prompt], sandbox, timeout, schema)
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def fail(step, outer) -> NoReturn:
    sys.exit('%s: ошибка — %s' % (step, (outer or {}).get('error') or (outer or {}).get('result') or outer))


# ---------------------------------------------------------------- команды

def cmd_new(a):
    os.makedirs(RUNS, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    prefix = '%s-%s-%s-' % (stamp, a.lang, a.name) if a.name else '%s-%s-' % (stamp, a.lang)
    run = tempfile.mkdtemp(prefix=prefix, dir=RUNS)
    write(os.path.join(run, 'lang.txt'), a.lang)
    print(run)


def cmd_check_brief(a, pk):
    brief = os.path.join(a.run, 'brief.md')
    need(brief, 'сначала напишите задание')
    out, outer = isolated(read(pk.brief), pk['brief_user'].format(task=read(brief)), a.model, a.effort,
                          a.timeout, QUESTIONS_SCHEMA)
    if out is None:
        fail('check-brief', outer)
    dump(os.path.join(a.run, 'questions.json'), out)
    cost = log_cost(a.run, 'check-brief', outer)
    qs = out.get('questions') or []
    print('Вопросов автору: %d ($%.3f)' % (len(qs), cost))
    for n, q in enumerate(qs, 1):
        print('%d. %s' % (n, q))


def cmd_write(a, pk):
    brief = os.path.join(a.run, 'brief.md')
    need(brief, 'сначала напишите задание')
    text, outer = isolated(read(pk.writer), pk['writer_user'].format(task=read(brief)),
                           a.model, a.effort, a.timeout)
    if not text:
        fail('write', outer)
    write(os.path.join(a.run, 'text.md'), strip_fences(text))
    cost = log_cost(a.run, 'write', outer)
    print('text.md: %d зн. ($%.3f) — %s' % (len(text), cost, os.path.join(a.run, 'text.md')))


def run_facts(a, pk):
    return isolated(read(pk.facts),
                    pk['facts_user'].format(task=read(os.path.join(a.run, 'brief.md')),
                                            text=read(os.path.join(a.run, 'text.md'))),
                    a.facts_model, 'high', a.timeout, CHECK_SCHEMA)


def review_consistent(report):
    """Сводка сходится со списком находок; иначе модель сбилась при генерации JSON (как в lab.py)."""
    summary = report.get('summary') or {}
    n = len(report.get('findings') or [])
    if isinstance(summary.get('total'), int) and summary['total'] != n:
        return False
    try:
        by_sev = sum(int(v) for v in (summary.get('by_severity') or {}).values())
    except (TypeError, ValueError):
        return True
    return not summary.get('by_severity') or by_sev == n


def run_review(a, pk, context):
    system = read(pk.reviewer) + pk['review_addendum'] + pk['catalog_heading'] + read(pk.catalog)
    user = pk['review_user'].format(path=os.path.join(a.run, 'text.md'), context=context)
    args = [user, '--append-system-prompt', system, '--allowedTools', 'Read', 'Bash(python3 text_scan.py:*)',
            '--add-dir', a.run, '--model', a.review_model]
    out, outer = claude(args, pk.review, a.timeout, REPORT_SCHEMA)
    if out is None or not review_consistent(out):
        out, outer = claude(args, pk.review, a.timeout, REPORT_SCHEMA)
    return out, outer


def cmd_check(a, pk):
    need(os.path.join(a.run, 'text.md'), 'сначала write')
    ctx_path = os.path.join(a.run, 'context.txt')
    if a.context:
        write(ctx_path, a.context)
    if not a.facts_only and not os.path.exists(ctx_path):
        sys.exit('нужен --context "<жанр>; читатель — <кто>; задача — <что он должен понять или решить>"')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        facts = pool.submit(run_facts, a, pk)
        review = None if a.facts_only else pool.submit(run_review, a, pk, read(ctx_path))
        facts_out, facts_outer = facts.result()
        review_out, review_outer = review.result() if review else (None, None)

    if facts_out is None:
        fail('check-facts', facts_outer)
    dump(os.path.join(a.run, 'facts.json'), facts_out)
    cost = log_cost(a.run, 'check-facts', facts_outer)
    print('## Сверка с заданием ($%.3f)' % cost)
    print('Выдумано: %d' % len(facts_out['invented']))
    for f in facts_out['invented']:
        print('- «%s» — %s' % (f['quote'], f['why']))
    print('Пропущено: %d' % len(facts_out['missing']))
    for f in facts_out['missing']:
        print('- %s — %s' % (f['fact'], f['why']))

    if a.facts_only:
        return
    if review_out is None:
        fail('review', review_outer)
    dump(os.path.join(a.run, 'review.json'), review_out)
    cost = log_cost(a.run, 'review', review_outer)
    findings = sorted(review_out.get('findings') or [], key=lambda f: f.get('severity') or 9)
    print('\n## Ревью ($%.3f)' % cost)
    print('Находок: %d' % len(findings))
    for f in findings:
        where = '; '.join('%s «%s»' % (l.get('ref', ''), l.get('quote', '')) for l in f.get('locations') or [])
        print('- [%s] %s %s — %s\n  %s' % (f.get('severity'), f.get('code'), f.get('title', ''), where,
                                          f.get('problem', '')))


def format_findings(pk, findings):
    out = []
    for n, f in enumerate(findings, 1):
        where = '; '.join(pk['location'] % (l.get('ref', ''), l.get('quote', '')) for l in f.get('locations') or [])
        out.append(pk['finding'] % (n, f.get('code', ''), f.get('title', ''), f.get('severity', ''), where,
                                    f.get('problem', '')))
    return '\n'.join(out)


def cmd_revise(a, pk):
    review_path = os.path.join(a.run, 'review.json')
    need(review_path, 'сначала check')
    findings = [f for f in json.load(open(review_path, encoding='utf-8')).get('findings') or []
                if (f.get('severity') or 9) <= a.max_severity]
    # Находки сверки — тоже в правку (в lab/lab.py пакета ru/ этого нет, добавлено здесь): выдумку убрать, пропущенное вернуть.
    facts_path = os.path.join(a.run, 'facts.json')
    if a.with_facts and os.path.exists(facts_path):
        facts = json.load(open(facts_path, encoding='utf-8'))
        inv_title, inv_tail = pk['invented']
        miss_title, miss_ref, miss_problem = pk['missing']
        for inv in facts.get('invented') or []:
            findings.append({'code': 'FACT-INVENTED', 'title': inv_title, 'severity': 1,
                             'locations': [{'ref': '', 'quote': inv['quote']}],
                             'problem': inv['why'] + inv_tail})
        for miss in facts.get('missing') or []:
            findings.append({'code': 'FACT-MISSING', 'title': miss_title, 'severity': 1,
                             'locations': [{'ref': miss_ref, 'quote': ''}],
                             'problem': miss_problem % (miss['fact'], miss['why'])})
    if not findings:
        print('Править нечего: нет находок серьёзности 1–%d и расхождений с заданием.' % a.max_severity)
        return
    text_path = os.path.join(a.run, 'text.md')
    user = pk['revise_user'].format(task=read(os.path.join(a.run, 'brief.md')), text=read(text_path),
                                    findings=format_findings(pk, findings)) + read(pk.revise)
    out, outer = isolated(read(pk.writer), user, a.model, a.effort, a.timeout, REVISE_SCHEMA)
    if out is None:
        fail('revise', outer)
    n = 1
    while os.path.exists(os.path.join(a.run, 'text.v%d.md' % n)):
        n += 1
    shutil.copy(text_path, os.path.join(a.run, 'text.v%d.md' % n))
    write(text_path, strip_fences(out['text']))
    dump(os.path.join(a.run, 'revision.json'), {'findings': findings, 'unresolved': out['unresolved']})
    cost = log_cost(a.run, 'revise', outer)
    print('Правка по %d находкам ($%.3f); прежний текст — text.v%d.md' % (len(findings), cost, n))
    print('Не закрыть без новых фактов: %d' % len(out['unresolved']))
    for u in out['unresolved']:
        print('- %s: %s' % (u['code'], u['missing_fact']))


def main():
    if not shutil.which('claude'):
        sys.exit('нужен Claude Code CLI (`claude`) в PATH')
    ap = argparse.ArgumentParser(description='Шаги скила text-quality для одного текста')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('new')
    p.add_argument('--lang', required=True, choices=sorted(LANGS), help='язык текста: ru → пакет ru/, en → пакет en/')
    p.add_argument('--name', default='')
    p.set_defaults(fn=cmd_new)

    def run_parser(name, fn, model='opus', effort='medium', timeout=300):
        p = sub.add_parser(name)
        p.add_argument('run')
        p.add_argument('--model', default=model)
        p.add_argument('--effort', default=effort)
        p.add_argument('--timeout', type=int, default=timeout)
        p.set_defaults(fn=fn)
        return p

    run_parser('check-brief', cmd_check_brief)
    run_parser('write', cmd_write)
    p = run_parser('check', cmd_check, timeout=900)
    p.add_argument('--context', help='«<жанр>; читатель — <кто>; задача — <что он должен понять или решить>»')
    p.add_argument('--facts-only', action='store_true')
    p.add_argument('--facts-model', default='sonnet')
    p.add_argument('--review-model', default='opus')
    p = run_parser('revise', cmd_revise)
    p.add_argument('--max-severity', type=int, default=2)
    p.add_argument('--no-facts', dest='with_facts', action='store_false',
                   help='не брать в правку выдуманное и пропущенное из facts.json')

    a = ap.parse_args()
    if a.cmd == 'new':
        return a.fn(a)
    a.run = os.path.abspath(a.run)
    if not os.path.isdir(a.run):
        sys.exit('нет папки прогона %s — создайте её: talk.py new --lang ru|en' % a.run)
    lang_path = os.path.join(a.run, 'lang.txt')
    lang = read(lang_path) if os.path.exists(lang_path) else 'ru'   # прогоны до появления en/ — русские
    if lang not in LANGS:
        sys.exit('неизвестный язык в %s: %s' % (lang_path, lang))
    a.fn(a, Pack(lang))


if __name__ == '__main__':
    main()
