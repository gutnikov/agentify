#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brief check before writing (../checking-a-brief.md): how many of the gaps that review and revision later found
it catches in advance.

    python3 brief_check.py ask      # questions to the author for each brief -> runs/brief-check/<id>.q.json
    python3 brief_check.py judge    # did the questions cover the gaps: M-IDEAL findings from GAP_RUNS and unresolved from revision
    python3 brief_check.py report
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab  # noqa: E402

OUT = os.path.join(lab.RUNS, 'brief-check')
BRIEF_PROMPT = os.path.join(lab.PLAYBOOK, 'checking-a-brief.md')
# Runs named as in rutalk's lab (see README.md, "Runs in runs/"); runs that do not exist yet are skipped.
GAP_RUNS = ['final', 'h-final', 'test-final', 'test-h-final', 'o-final', 'ox-final', 'ox-rev1']
REVISED_RUN = 'ox-rev1'

QSCHEMA = {'type': 'object', 'required': ['questions'],
           'properties': {'questions': {'type': 'array', 'items': {'type': 'string'}}}}

JUDGE_SYSTEM = """You are given a brief for a text, the questions that were put to its author before writing, and the gaps that were found later in the finished texts.
For each gap, decide whether it was covered in advance: is there a question whose answer would have closed this gap? A question close in meaning counts; a question about something else does not.
Answer only with JSON in the schema, one item per gap, in the same order."""

JUDGE_USER = 'BRIEF:\n{task}\n\nQUESTIONS TO THE AUTHOR:\n{questions}\n\nGAPS:\n{gaps}'

JSCHEMA = {'type': 'object', 'required': ['verdicts'],
           'properties': {'verdicts': {'type': 'array', 'items': {
               'type': 'object', 'required': ['covered', 'by'],
               'properties': {'covered': {'type': 'boolean'}, 'by': {'type': 'string'}}}}}}


def gaps(bid):
    out = []
    for run in GAP_RUNS:
        p = os.path.join(lab.RUNS, run, 'reviews', bid + '.json')
        if os.path.exists(p):
            for f in json.load(open(p, encoding='utf-8')).get('findings') or []:
                if f.get('code') == 'M-IDEAL':
                    out.append({'source': 'review %s' % run, 'gap': f.get('problem', '')})
    m = os.path.join(lab.RUNS, REVISED_RUN, 'meta', bid + '.json')
    if os.path.exists(m):
        for u in json.load(open(m, encoding='utf-8')).get('unresolved') or []:
            out.append({'source': 'revision', 'gap': u['missing_fact']})
    return out


def ask():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(lab.SANDBOX, exist_ok=True)
    system = lab.read(BRIEF_PROMPT)

    def one(b):
        cmd = ['claude', '-p', lab.BRIEF_USER.format(task=b['task']), '--safe-mode', '--tools', '', '--model', 'opus',
               '--effort', 'medium', '--system-prompt', system, '--output-format', 'json',
               '--no-session-persistence', '--json-schema', json.dumps(QSCHEMA, ensure_ascii=False)]
        outer, _, _ = lab.run_claude(cmd, lab.SANDBOX, 600)
        rep = (outer or {}).get('structured_output')
        if not rep:
            return '%s ERROR' % b['id']
        rep['cost_usd'] = outer.get('total_cost_usd')
        json.dump(rep, open(os.path.join(OUT, b['id'] + '.q.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return '%s questions %d' % (b['id'], len(rep['questions']))

    lab.pmap(one, lab.load_briefs(), 12)


def judge():
    os.makedirs(lab.SANDBOX, exist_ok=True)

    def one(b):
        g = gaps(b['id'])
        qs = json.load(open(os.path.join(OUT, b['id'] + '.q.json'), encoding='utf-8'))['questions']
        if not g:
            json.dump({'gaps': [], 'verdicts': []}, open(os.path.join(OUT, b['id'] + '.j.json'), 'w', encoding='utf-8'))
            return '%s no gaps' % b['id']
        user = JUDGE_USER.format(
            task=b['task'],
            questions='\n'.join('%d. %s' % (i, q) for i, q in enumerate(qs, 1)) or '(no questions)',
            gaps='\n'.join('%d. %s' % (i, x['gap']) for i, x in enumerate(g, 1)))
        cmd = ['claude', '-p', user, '--safe-mode', '--tools', '', '--model', 'sonnet', '--effort', 'high',
               '--system-prompt', JUDGE_SYSTEM, '--output-format', 'json', '--no-session-persistence',
               '--json-schema', json.dumps(JSCHEMA, ensure_ascii=False)]
        outer, _, _ = lab.run_claude(cmd, lab.SANDBOX, 600)
        rep = (outer or {}).get('structured_output')
        if not rep or len(rep['verdicts']) != len(g):
            return '%s JUDGE ERROR' % b['id']
        json.dump({'gaps': g, 'verdicts': rep['verdicts']}, open(os.path.join(OUT, b['id'] + '.j.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        return '%s covered %d of %d' % (b['id'], sum(v['covered'] for v in rep['verdicts']), len(g))

    lab.pmap(one, lab.load_briefs(), 12)


def report():
    tot = cov = nq = 0
    by_src = {}
    cost = 0
    briefs = lab.load_briefs()
    for b in briefs:
        q = json.load(open(os.path.join(OUT, b['id'] + '.q.json'), encoding='utf-8'))
        nq += len(q['questions'])
        cost += q.get('cost_usd') or 0
        j = json.load(open(os.path.join(OUT, b['id'] + '.j.json'), encoding='utf-8'))
        for g, v in zip(j['gaps'], j['verdicts']):
            s = by_src.setdefault('revision' if g['source'] == 'revision' else 'review', [0, 0])
            s[0] += 1
            s[1] += v['covered']
            tot += 1
            cov += v['covered']
    print('briefs %d, questions %d (%.1f per brief), cost $%.2f' % (len(briefs), nq, nq / float(len(briefs)), cost))
    if not tot:
        print('no gaps from review and revision yet: run GAP_RUNS first (see README.md)')
        return
    print('gaps from review and revision: %d, covered by questions in advance: %d (%.0f%%)' % (tot, cov, 100.0 * cov / tot))
    for k, (t, c) in by_src.items():
        print('  %s: %d of %d (%.0f%%)' % (k, c, t, 100.0 * c / t))


if __name__ == '__main__':
    {'ask': ask, 'judge': judge, 'report': report}[sys.argv[1]]()
