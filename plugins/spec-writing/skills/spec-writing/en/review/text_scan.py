#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical pre-pass for the text reviewer (entalk).

Finds candidates for the errors in error-patterns.md that a dictionary, a regular
expression or a count can find. These are not verdicts: the reviewer checks every
hit against its meaning and against the "Not an error if" section of the catalogue.
The script does not look for errors of meaning, structure or logic; that is the
reviewer's job.

Usage:
    python3 text_scan.py text.md               # report for a human and an agent
    python3 text_scan.py text.md --json        # the same as JSON
    python3 text_scan.py text.md --all         # no limit on lines per code
    cat text.txt | python3 text_scan.py -

Locations: ¶N is block N (paragraph, heading, list item, quote, table, image;
blocks are separated by a blank line), ¶N.M is sentence M in block N.

"(weak)" marks a marker that is often neutral. A weak dictionary marker is shown
only when the same sentence has another marker of the same code. Heuristic checks
that cannot be sure on their own (P-REFERENT, a bare "there is", a four-word noun
string, a triad of abstract words, a sentence crowded with -tion words) are always
shown and always marked weak.

Where the word lists come from (files under sources/, see sources/README.md):
- GOV.UK A to Z style guide, "Words to avoid", and "Use clear language" (Open
  Government Licence v3.0): W-CORP, W-LLM ("robust"), W-BUREAU ("in order to"),
  W-ZAUM ("utilise"); 25-word sentences, 5-sentence paragraphs, -ion/-ment words.
- PLAIN, Federal Plain Language Guidelines (public domain): "Use simple words and
  phrases" (W-BUREAU, W-ZAUM), "Avoid hidden verbs" (W-NOMINAL), "Avoid noun strings"
  (W-NOUNSTACK), "Avoid jargon" (Kimble's legal words, business filler: W-BUREAU,
  W-CORP, W-CLICHE), "Be concise" (prepositions, excess modifiers, doublets:
  W-BUREAU, W-INTENS), "Write short paragraphs" (150/250 words: S-WALL), "Use
  positive language" (W-BUREAU).
- Strunk, The Elements of Style (public domain): rule 13 expressions (W-BUREAU,
  P-EXPLETIVE); chapter V: "very", "so", "certainly" (W-INTENS), "literally"
  (T-TERMS), "one of the most" (W-CLICHE), "thanking you in advance" (W-POLITE),
  "respective", "case", "nature", "character", "along these lines" (W-BUREAU,
  W-VAGUE).
- Everything else (hedges, intensifiers, praise words, clichés, corporate
  buzzwords, euphemisms, machine-text tells, clickbait, irregular participles) was
  written for entalk from general knowledge of English usage. No list was copied
  from proselint (BSD-3-Clause) or write-good (MIT); where the ideas overlap
  (weasel words, cliché checks, passive voice) the lists and the code are our own.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict

# ---------------------------------------------------------------- codes

# Only codes from the entalk plan (plus the SIGNAL-LONG hint). Finder.add refuses
# any other code, so the scanner can never emit a code the catalogue does not have.
TITLES = OrderedDict([
    ('T-BS', 'Generalization or promise without facts'),
    ('T-NUMBERS', 'Misleading numbers'),
    ('T-HIDE', 'Bad news hidden'),
    ('T-TITLE', 'Title claims more than the facts'),
    ('T-TERMS', 'Clever word in the wrong sense'),
    ('T-PERSONAL', 'Judging the person, not the action'),
    ('M-FACTS', 'Facts that do not serve the reader'),
    ('M-HOLLOW', 'Hollow text: words without information'),
    ('M-NOEXAMPLE', 'Idea without an example'),
    ('S-TITLE', 'Title does not say what the text is about'),
    ('S-CLICKBAIT', 'Clickbait title'),
    ('S-INTRO', 'Empty introduction'),
    ('S-OUTRO', 'Useless conclusion'),
    ('S-SUBHEADS', 'Subheadings do not help the reader find their way'),
    ('S-WALL', 'Wall of text'),
    ('S-LIST', 'List in the wrong place'),
    ('S-BURIED', 'Important information buried'),
    ('SIGNAL-LONG', 'Signal, not a code: long sentence — check P-OVERLOAD, P-SPLIT, P-NESTED, '
                    'P-INLINELIST, P-CLUMSY'),
    ('P-INLINELIST', 'List crammed into a sentence'),
    ('P-INACTION', 'No action: abstract subject, state verb'),
    ('P-PARCEL', 'Sentence fragments'),
    ('P-GLUED', 'Run-on sentence or comma splice'),
    ('P-NESTED', 'Clause inside a clause'),
    ('P-EXPLETIVE', 'Empty opener: "there is", "it is … that"'),
    ('P-REFERENT', 'Pronoun without a clear referent'),
    ('W-INTRO', 'Hedges and filler'),
    ('W-PROP', 'Prop instead of an argument'),
    ('W-POLITE', 'Fake politeness'),
    ('W-EVAL', 'Evaluation instead of a fact'),
    ('W-INTENS', 'Intensifier'),
    ('W-CLICHE', 'Cliché or filler phrase'),
    ('W-CORP', 'Corporate buzzword'),
    ('W-BUREAU', 'Officialese'),
    ('W-ZAUM', 'Jargon and long words'),
    ('W-NOMINAL', 'Hidden verb (nominalization)'),
    ('W-PASSIVE', 'Passive voice'),
    ('W-VAGUE', 'Vagueness'),
    ('W-NOUNSTACK', 'Noun string'),
    ('W-LLM', 'Machine-text tells'),
    ('V-DECOR', 'Decoration instead of illustration'),
    ('V-RIGHTS', "Someone else's image without rights"),
    ('V-NOSCHEME', 'Complex process in words only'),
])

# ---------------------------------------------------------------- dictionaries
# Marker syntax:
#   'as we all know'  phrase; a space = any whitespace; case and curly quotes do not matter;
#                     a hyphen matches a hyphen, a space or nothing ("cutting-edge" = "cutting edge")
#   'leverag*'        * = any continuation of the word
#   '!clearly'        only when set off: at the start of a sentence or between commas/dashes/brackets
#   'r:…'             regular expression over the normalized text (lower case, straight quotes, — for dashes)
# strong is always reported; weak only when the sentence has 2+ markers of that code.
# Dictionary codes claim their span in priority order (WORD_CODES): one place, one code.

B = r'(?<![a-z0-9])'      # word start for r: markers
E = r'(?![a-z0-9])'       # word end for r: markers

DICT = OrderedDict()
NUMBER = (r'(?:[$£€]\s?)?\d[\d,]*(?:\.\d+)?\+?(?:\s?(?:%|percent|per cent|k|m|bn|million|billion|thousand|'
          r'hundred|trillion)' + E + r')?')

DICT['T-HIDE'] = dict(strong=[
    # softened failure and criticism
    'below expectations', 'below our expectations', 'lower than expected', 'lower than anticipated',
    'slower than expected', 'slower than anticipated', 'softer than expected', 'weaker than expected',
    'more challenging than expected', 'did not meet expectations', "didn't meet expectations",
    'did not meet our expectations', 'fell short of expectations', 'fell short', 'falls short',
    'did not go as planned', "didn't go as planned", 'not go as planned', 'not ideal', 'less than ideal',
    'less than optimal', 'suboptimal', 'room for improvement', 'area for improvement',
    'areas for improvement', 'areas of improvement', 'development area*', 'opportunity for growth',
    'opportunities for growth', 'learning opportunity', 'learning experience', 'teachable moment',
    'a bit of a challenge', 'mixed results', 'headwinds', 'hiccup*', 'minor setback*', 'temporary setback*',
    'temporary difficulties', 'certain difficulties', 'some difficulties', 'minor issues', 'minor problems',
    'unforeseen circumstances', 'circumstances beyond our control', 'reasons beyond our control',
    'for operational reasons', 'operational reasons', 'technical difficulties', 'higher than usual',
    'higher than normal', 'elevated error rates', 'elevated errors', 'degraded performance',
    'some users may', 'some customers may', 'a small number of users', 'a small number of customers',
    'a subset of users', 'a subset of customers', 'abundance of caution',
    r'r:' + B + r'(?:slightly|marginally|somewhat|modestly)\s+(?:decreas|declin|lower|fell|fall|drop|reduc|down|shrank|shrunk|contract|miss|weak|soft)[a-z]*',
    r'r:' + B + r'(?:slight|modest|marginal|small)\s+(?:decrease|decline|dip|drop|reduction|downturn|loss)',
    r'r:' + B + r'despite\s+(?:the\s+|these\s+|some\s+|recent\s+|current\s+|ongoing\s+|market\s+)?(?:challenges|headwinds|difficulties|setbacks|losses|decline|downturn|turbulence|uncertainty)' + E,
    # agentless bad news
    'a decision was made', 'a decision has been made', 'the decision was made', 'the decision has been made',
    'it was decided', 'it has been decided', 'mistakes were made', 'errors were made', 'mistakes have been made',
    'difficult decision', 'tough decision', 'hard decision', 'difficult choice',
    # euphemisms for lay-offs, price rises, shutdowns
    'downsiz*', 'rightsiz*', 'right-siz*', 'workforce reduction*', 'reduction in force', 'reductions in force',
    'headcount reduction*', 'workforce optimi*', 'efficiency measures', 'cost optimi*', 'parted ways',
    'part ways', 'parting ways', 'no longer with the company', 'no longer with us', 'separated from the company',
    'released from employment', 'involuntary separation', 'career transition*', 'negative growth',
    'price adjustment*', 'pricing adjustment*', 'price correction*', 'pricing update*',
    r'r:' + B + r'(?:updat|adjust|revis|realign)[a-z]*\s+(?:our|the|its|their)\s+(?:pricing|prices|fees|rates|tariffs)' + E,
    'sunsetting', 'sunsetted', 'to sunset', 'temporarily suspend*', 'temporarily paused', 'temporarily pause*',
    'collateral damage', 'enhanced interrogation', 'misspoke', 'misstatement*', 'economical with the truth',
    'alternative facts', 'creative accounting',
    # reassurance without facts
    'everything is under control', 'the situation is under control', 'no cause for concern',
    'no reason for concern', 'no reason to worry', 'nothing to worry about', 'no need to worry',
    'no need for concern', 'no need to panic',
], weak=[
    'challenges', 'challenging', 'setback*', 'incident*', 'difficulties', 'restructur*', 'reorgani*',
    'realign*', 'discontinu*', 'temporarily', 'let go', 'transition*', 'glitch*', 'shortfall*', 'softening',
    'softened', 'under control', 'on track', 'remain committed', 'remain confident', 'we are aware',
    'investigating', 'passed away', 'pre-owned', 'neutrali*',
])

DICT['T-BS'] = dict(strong=[
    r'r:' + B + r'(?:studies|research|surveys?|data|science|evidence|statistics)\s+(?:shows?|has shown|have shown|suggests?|proves?|has proven|have proven|has proved|confirms?|indicates?|demonstrates?|tells us|says)' + E,
    r'r:' + B + r'(?:experts|scientists|researchers|analysts|specialists|doctors|economists|psychologists)\s+(?:say|agree|believe|warn|claim|suggest|recommend|have found|have shown|have proven|predict|think|are sure|now know)' + E,
    r'r:' + B + r'(?:many|most|some)\s+(?:people|experts|users|customers|companies|businesses|organi[sz]ations|professionals|developers|leaders|parents|scientists)\s+(?:say|believe|think|agree|feel|know|prefer|choose|now|already|are now|have already)' + E,
    r'r:(?<!as )' + B + r'(?:everyone|everybody|we all)\s+knows?' + E,
    r'r:' + B + r'(?:according to|in the opinion of)\s+(?:experts|studies|research|scientists|analysts|specialists|many)' + E,
    'it is widely believed', 'it is believed that', 'it is thought that', 'it is said that', 'it is often said',
    'it is generally accepted', 'widely regarded as', 'widely considered', 'is considered to be',
    'many believe', 'many say', 'some people say', 'people say', 'everyone agrees', 'no one can deny',
    'nobody can deny', 'no one would argue', 'few would argue', 'nobody would argue', 'no one doubts',
    'hardly anyone', 'any sensible person', 'any reasonable person', 'any rational person',
    'countless studies', 'numerous studies', 'many studies', 'a wealth of research', 'a growing body of',
    'clinically proven', 'scientifically proven', 'proven to', 'guaranteed to', 'the key to success',
    'the secret to', 'the only way to', 'experience shows', 'practice shows', 'history shows',
    'history has shown', 'it has been shown', 'it has been proven', 'more and more', 'increasingly popular',
    'a growing number of', 'ever-growing', 'ever-increasing', 'gaining popularity', 'gaining traction',
    'losing popularity', 'on the rise', 'in recent years', 'in recent times', 'all over the world',
    'trusted by thousands', 'trusted by millions', 'loved by thousands', 'loved by millions',
    'join thousands', 'join millions',
    r'r:' + B + r'trusted by\s+(?:over\s+|more than\s+)?(?:\d[\d,]*\+?|thousands|millions|hundreds|countless)',
    'there is no doubt that', 'there is no question that', 'undeniabl*', 'the fact is',
], weak=[
    'everyone', 'everybody', 'nobody', 'no one', 'all users', 'every user', 'every business', 'every company',
    'always', 'never', 'many', 'proven', 'lately',
])

DICT['T-PERSONAL'] = dict(strong=[
    r"r:" + B + r"(?:he|she|they|you|he's|she's|they're|you're)\s+(?:is\s+|are\s+|was\s+|were\s+)?(?:just\s+|simply\s+|so\s+|such\s+|completely\s+|totally\s+|really\s+)?(?:an?\s+)?(?:idiots?|stupid|dumb|lazy|incompetent|useless|clueless|morons?|fools?|losers?|hopeless|worthless|pathetic|careless|sloppy|ignorant|arrogant|dishonest|liars?|amateurs?)" + E,
    r"r:" + B + r"(?:he|she|they|you)\s+(?:has|have)\s+no\s+(?:talent|brains?|clue|taste|shame|common sense|skills?)" + E,
    r"r:" + B + r"(?:is|are|was|were)\s+(?:an?\s+)?(?:terrible|lousy|bad|poor|awful|horrible|incompetent|useless|hopeless)\s+(?:person|people|manager|managers|employee|employees|developer|developers|engineer|engineers|writer|writers|leader|leaders|colleague|colleagues|teacher|student|parent|worker|workers)" + E,
    r"r:" + B + r"you(?:'re| are)\s+(?:always|never)" + E,
    'not a team player', 'bad attitude', 'attitude problem',
], weak=[])

DICT['T-TERMS'] = dict(strong=[
    'literally', 'exponential*', 'decimat*', 'quantum leap', 'begs the question', 'beg the question',
    'epicent*', 'gaslight*', 'narcissis*', 'psychopath*', 'sociopath*', 'schizophreni*', 'ocd', 'nonplussed',
    'enormity', 'fortuitous*', 'irregardless', 'paradigm shift',
], weak=['bipolar', 'paranoi*', 'depressed', 'trauma*', 'toxic', 'ironic*', 'irony', 'disinterested', 'peruse',
         'penultimate', 'dna'])

DICT['W-PROP'] = dict(strong=[
    'as we all know', 'as everyone knows', 'as everybody knows', 'as you know', 'as you probably know',
    'as you may know', 'as is well known', 'it is well known', 'it is common knowledge', 'it is no secret',
    "it's no secret", 'no secret that', 'needless to say', 'it goes without saying', 'in my opinion',
    'in my view', 'in my humble opinion', 'imho', 'in our opinion', 'in our view', 'from my point of view',
    'from my perspective', '!personally', 'i think', 'i believe', 'i feel', 'we believe', 'we think',
    'we feel that', 'i would argue', 'i would say', "i'd say", 'to be honest', 'to be frank', 'frankly',
    'honestly', 'truth be told', 'to tell the truth', 'if you ask me', 'i must say', 'i have to say',
    'let me be clear', 'let me be honest', 'make no mistake', 'trust me', 'believe me', 'mark my words',
    'as you can see', 'it is obvious that', "it's obvious that",
], weak=[])

DICT['W-LLM'] = dict(strong=[
    'delve*', 'delving', 'tapestry', 'testament to', 'a testament', 'in the realm of', 'the realm of',
    'embark* on', 'unleash*', r'r:' + B + r'unlock(?:s|ed|ing)?\s+(?:the\s+|your\s+|its\s+|their\s+|our\s+|new\s+|a\s+world\s+of\s+)?(?:full\s+)?(?:potential|power|possibilities|value|insights|opportunities|growth|creativity|secrets)' + E,
    'harness* the power', 'the power of', 'elevat* your', 'elevat* the', 'underscores the', 'underscore the', 'underscored', 'underscoring',
    'showcas*', 'bolster*',
    'resonat*', 'revolutioni*', 'reimagin*', 'transformative', 'supercharg*', 'seamless*', 'robust',
    'meticulous*', 'commendable', 'intricate*', 'intricacies', 'multifaceted', 'myriad', 'plethora',
    'beacon of', 'symphony of', 'labyrinth*', 'treasure trove', 'vibrant', 'bustling', 'nestled', 'boasts',
    'pivotal', 'paramount', 'ever-evolving', 'ever-changing', 'constantly evolving', 'rapidly evolving',
    'fast-paced world', 'fast-paced environment', 'digital age', 'digital era', 'in an era of',
    'in an increasingly', 'evolving landscape', 'digital landscape', 'dynamic landscape', 'complex landscape',
    'the landscape of', 'competitive landscape',
    r"r:" + B + r"in today's\s+(?:[a-z-]+\s+){0,3}(?:world|age|era|landscape|environment|society|market|marketplace|economy|climate|business)" + E,
    r'r:' + B + r'navigat(?:e|es|ed|ing)\s+(?:the\s+|this\s+|these\s+|its\s+|their\s+|your\s+|our\s+)?(?:[a-z-]+\s+)?(?:landscape|complexit[a-z]*|challenges|world|waters|maze|terrain|intricacies|realm|journey|uncertaint[a-z]*|nuances)' + E,
    r'r:' + B + r'plays?\s+an?\s+(?:crucial|pivotal|vital|key|significant|central|critical|essential|important|major|instrumental)\s+role' + E,
    r'r:' + B + r'(?:stands|serves)\s+as\s+(?:a\s+)?(?:testament|reminder|beacon|cornerstone|catalyst|bridge)' + E,
    r"r:" + B + r"whether you(?:'re| are)\s+an?\s+(?:[a-z-]+\s+){1,3}or\s+(?:an?\s+)?[a-z-]+",
    r"r:" + B + r"it(?:'s|\s+is)\s+(?:very\s+|particularly\s+|especially\s+|also\s+|equally\s+)?(?:important|worth|crucial|essential|vital|key)\s+(?:to\s+)?(?:note|noting|remember|mention|mentioning|emphasi[sz]e|highlight|recogni[sz]e|understand|consider)" + E,
    "it's crucial to", 'it is crucial to', "let's dive", "let's delve", 'dive into', 'diving into', 'deep dive', "let's explore",
    "let's take a closer look", 'key takeaways', 'valuable insights', 'embark on a journey', 'on a journey',
    'your journey', 'the journey of', 'at its core', 'a rich history', 'rich cultural heritage',
], weak=[
    r'r:' + B + r'not\s+(?:just|only|merely|simply)\s+(?:about\s+)?[^.!?;]{1,60}?,?\s+but\s+(?:also\s+)?',
    'landscape', 'navigat*', 'journey', 'nuanced', 'realm', 'ecosystem', 'insights', 'an array of',
    'harness*', 'elevat*', 'foster*', 'enhanc*', 'empower*', 'crucial', 'comprehensive', 'embrac*', 'thrive*',
    'hinges on',
])

DICT['W-CORP'] = dict(strong=[
    # GOV.UK "Words to avoid" (the ones that are rarely literal)
    'leverag*', 'empower*', 'disincentivi*', 'incentivi*', 'liais*', 'overarching', 'streamlin*',
    'going forward', 'moving forward', 'one-stop shop', 'ring-fenc*', 'slim* down', 'drive out', 'foster*',
    'facilitat*', 'impacted', 'impacting', 'impactful',
    r'r:' + B + r'driv(?:e|es|ing|en)\s+(?:growth|innovation|change|value|results|engagement|adoption|efficienc[a-z]*|revenue|impact|success|performance|transformation|outcomes|alignment|excellence)' + E,
    r'r:' + B + r'land(?:s|ed|ing)?\s+(?:the|a|an|this|our|new|big)\s+(?:deal|project|contract|client|feature|change|launch|initiative)' + E,
    # business jargon (PLAIN "Avoid jargon") and common buzzwords
    'synerg*', 'best practice*', 'value added', 'value-added', 'added value', 'thinking outside the box',
    'think outside the box', 'outside the box', 'touch base', 'circle back', 'loop in', 'looped in',
    'low-hanging fruit', 'move the needle', 'moving the needle', 'boil the ocean', 'take it offline',
    'take this offline', 'win-win', 'game-changer', 'game-changing', 'next-generation', 'cutting-edge',
    'bleeding-edge', 'state-of-the-art', 'world-class', 'best-in-class', 'industry-leading',
    'market-leading', 'market leader*', 'leading provider', 'a leading', 'one of the leading',
    'thought leader*', 'mission-critical', 'turnkey', 'disrupt*', 'holistic*', 'customer-centric',
    'client-centric', 'customer-focused', 'customer-obsessed', 'results-driven', 'results-oriented',
    'value-driven', 'purpose-driven', 'mission-driven', 'proactive*', 'actionable', 'learnings',
    'key learnings', 'deliverable*', 'ideate', 'ideation', 'operationali*', 'productiz*', 'upskill*',
    'reskill*', 'core competenc*', 'north star', 'single source of truth', 'pain point*', 'level up',
    'double down', 'double-click on', 'peel back the onion', 'passionate about', 'we are passionate',
    'our mission is', 'our vision is', 'committed to excellence', 'commitment to excellence',
    'dedicated team', 'team of professionals', 'team of experts', 'highly qualified', 'highly skilled',
    'trusted partner', 'reliable partner', 'tailored to your needs', 'tailor-made', 'exceed* expectations',
    'exceed* your expectations', 'our top priority', 'your satisfaction is', 'enabler*', 'enablement',
    'integrating quality solutions', 'touchpoint*', 'mindshare', 'thought leadership', 'bandwidth to',
    r'r:' + B + r'(?:integrated|innovative|business|end-to-end|turnkey|tailored|bespoke|total|comprehensive|holistic|smart|digital|enterprise|cloud|quality|cutting-edge|world-class|scalable|custom)\s+solutions?' + E,
], weak=[
    'agenda', 'advance', 'collaborat*', 'combat*', 'commit*', 'pledge*', 'counter', 'deliver*', 'deploy*',
    'dialogue', 'focus*', 'impact', 'impacts', 'key', 'progress', 'promot*', 'strengthen*', 'tackl*',
    'transform*', 'hub', 'portal', 'paradigm*', 'value proposition', 'bandwidth', 'end-to-end', 'scalab*',
    'innovation', 'solution*', 'alignment', 'align*', 'stakeholder*', 'action item*', 'kpi*', 'roi',
    'competitive advantage', 'excellence', 'we value', 'we care about', 'years of experience',
    'decades of experience', 'bespoke', 'go-to-market', 'at scale', 'enhanc*', 'optimi*', 'ecosystem',
    'journey', 'empowerment', 'data-driven', 'unique value',
])

DICT['W-CLICHE'] = dict(strong=[
    'at the end of the day', 'in this day and age', 'nowadays', 'in the modern world', 'in our modern world',
    'in modern society', 'today more than ever', 'now more than ever', 'more than ever before',
    'like never before', 'since the dawn of time', 'since time immemorial', 'from time immemorial',
    'throughout history', 'last but not least', 'first and foremost', 'each and every', 'one and only',
    'tried and true', 'tried and tested', 'when all is said and done', 'all things considered',
    'it is what it is', 'the bottom line is', 'the elephant in the room', 'perfect storm', 'tip of the iceberg',
    'double-edged sword', 'a fine line', 'fine line between', "the lion's share", 'in the nick of time',
    'crystal clear', 'like the plague', 'at the drop of a hat', 'back to square one',
    'back to the drawing board', 'better late than never', 'calm before the storm', 'hit the nail on the head',
    'level playing field', 'needle in a haystack', 'only time will tell', 'time will tell',
    'push the envelope', 'pushing the envelope', 'raise the bar', 'raising the bar', 'to the next level',
    'next level', 'the sky is the limit', "the sky's the limit", 'go the extra mile', 'going the extra mile',
    'hit the ground running', 'jump on the bandwagon', 'on the same page', 'par for the course',
    'reinvent the wheel', 'reinventing the wheel', 'a whole new level', 'a whole new world', 'leaps and bounds',
    'icing on the cake', 'in a nutshell', 'stay ahead of the curve', 'ahead of the curve', 'ahead of the game', 'stay ahead',
    'in the heart of', 'at the heart of', 'cornerstone', 'pave the way', 'paves the way', 'paving the way',
    'paved the way', 'shed light on', 'sheds light on', 'shed some light', 'stand the test of time',
    'stood the test of time', 'stands the test of time', 'a far cry from', 'all walks of life',
    'in the blink of an eye', 'the rest is history', 'take a step back', 'step in the right direction',
    'food for thought', 'million-dollar question', 'silver bullet', 'magic bullet', 'holy grail',
    'the new normal', 'unprecedented times', 'uncertain times', 'these trying times', 'these challenging times',
    'come full circle', 'the writing is on the wall', 'by and large', 'few and far between',
    'first things first', 'for all intents and purposes', 'in no uncertain terms', 'in the final analysis',
    'in the grand scheme of things', 'it stands to reason', 'nothing could be further from the truth',
    'over the moon', 'part and parcel', 'slowly but surely', 'the fact of the matter', 'think twice',
    'time and time again', 'time and again', 'long story short', 'to make a long story short',
    'under the radar', 'up in the air', 'when it comes down to it', 'with bated breath', 'without further ado',
    'words cannot express', 'worth its weight in gold', 'easier said than done', 'not rocket science',
    'no-brainer', 'step up to the plate', 'take the plunge', 'breath of fresh air', 'best of both worlds',
    'bells and whistles', 'nuts and bolts', 'at your fingertips', 'with just a few clicks',
    'in just a few clicks', 'with a few clicks', 'peace of mind', 'look no further', 'say goodbye to',
    'say hello to', 'one of the most', 'the world of', 'along these lines', 'along the same lines',
    "here's the thing", 'here is the thing', 'the fact of the matter is',
], weak=[
    'these days', 'from time to time', 'big picture', 'bottom line', 'out of the box', 'lessons learned',
    'in the long run', 'more often than not', 'when it comes to', 'quick fix', r'r:' + B + r'must-have' + E,
    'one-size-fits-all', 'like clockwork', 'stark contrast', 'perfect balance', 'perfect blend',
])

DICT['W-BUREAU'] = dict(strong=[
    # PLAIN "Use simple words and phrases" (phrases) and "Be concise"
    'addressees', 'addressees are requested', 'adjacent to', 'afford an opportunity', 'as a means of',
    'as prescribed by', 'at the present time', 'at this point in time', 'be advised', 'by means of',
    'close proximity', 'due to the fact that', 'during the period', 'effect modifications', 'for a period of',
    'has a requirement for', 'have a requirement for', 'in accordance with', 'in an effort to', 'inasmuch as',
    'in a timely manner', 'incumbent upon', 'incumbent on', 'in lieu of', 'in order that', 'in order to',
    'in regard to', 'in regards to', 'with regard to', 'with regards to', 'inter alia',
    'interpose no objection', 'in the amount of', 'in the event of', 'in the event that',
    'in the near future', 'in the process of', 'in view of', 'in view of the above', 'is applicable to',
    'are applicable to', 'is authorized to', 'is authorised to', 'is in consonance with', 'it is requested',
    'it is essential', 'not later than', 'no later than', 'notwithstanding', 'on a regular basis',
    r'r:' + B + r'on an?\s+(?:daily|weekly|monthly|quarterly|yearly|annual|regular|ongoing|continuous|continual|case-by-case|case by case|as-needed|as needed|routine|periodic|temporary|permanent|voluntary|full-time|part-time|timely|consistent)\s+basis' + E,
    'pertaining to', 'prior to', 'provided that', 'provides guidance for', 'pursuant to', 'set forth',
    'successfully complete*', 'the undersigned', 'time period', 'under the provisions of',
    'until such time as', 'with reference to', 'with the exception of', 'a sufficient number of',
    'is able to', 'are able to', 'is responsible for', 'are responsible for', 'be responsible for',
    'an amount of', 'on the ground that', 'and/or', 'shall', 'no fewer than', 'no less than', 'not less than',
    'in excess of', 'is in receipt of', 'are in receipt of',
    # Kimble's legal words (PLAIN "Avoid jargon") and other legalese
    'above-mentioned', 'abovementioned', 'aforementioned', 'aforesaid', 'foregoing', 'henceforth',
    'hereafter', 'hereinafter', 'hereby', 'herein', 'heretofore', 'herewith', 'hereunder', 'hereto',
    'thereafter', 'thereof', 'therein', 'thereto', 'therewith', 'thereunder', 'whatsoever', 'whereat',
    'wherein', 'whereof', 'whereby', 'whereas', 'forthwith', 'duly', 'the said', 'commencement', 'cessation',
    # doublets (PLAIN "Be concise")
    'due and payable', 'cease and desist', 'knowledge and information', 'begin and commence',
    'null and void', 'any and all', 'full and complete', 'true and correct', 'over and above',
    'final and conclusive', 'fit and proper',
    # Strunk rule 13 and chapter V
    'the question as to whether', 'as to whether', 'there is no doubt but that', 'the fact that',
    'owing to the fact', 'in spite of the fact', 'despite the fact that', 'call your attention to the fact',
    r'r:' + B + r'(?:used\s+)?for\s+[a-z]+\s+purposes' + E, r'r:' + B + r'in an?\s+[a-z]+\s+(?:manner|fashion)' + E,
    r'r:' + B + r'of\s+an?\s+(?:[a-z]+\s+)?(?:nature|character)' + E, 'respective', 'oftentimes', 'ofttimes',
    # letters and notices
    'please be advised', 'please be informed', 'kindly be informed', 'we wish to inform you',
    'this is to inform you', 'this is to certify', 'we regret to inform you', 'please find attached',
    'please find enclosed', 'enclosed please find', 'attached please find', 'as per', 'per your request',
    'in respect of', 'by virtue of', 'for the purpose of', 'for purposes of', 'with a view to',
    'in the course of', 'the process of', 'at an early date', 'it should be noted', 'it must be noted', 'it is to be noted',
    'it is hereby', 'we apologi* for any inconvenience', 'apologies for any inconvenience',
    'sorry for any inconvenience', 'for any inconvenience caused', 'regret any inconvenience',
    'strictly prohibited', 'strictly forbidden', 'is prohibited', 'are prohibited', 'reserves the right',
    'the management reserves',
], weak=[
    'in relation to', 'relative to', 'similar to', 'the month of', 'with respect to', 'in connection with',
    'in conjunction with', 'in the absence of', 'on the grounds that', 'respectively', 'along the lines of',
    'in addition', 'regarding', 'concerning', 'accordingly', 'consequently', 'subsequently', 'thereby',
    'herewith', 'whilst', 'amongst', 'upon', 'such', 'said',
])

DICT['W-INTRO'] = dict(strong=[
    'basically', 'essentially', 'actually',
    r'r:(?<!the )(?<!a )(?<!this )(?<!that )(?<!what )(?<!any )(?<!some )(?<!same )(?<!one )(?<!every )(?<!which )'
    r'(?<!each )(?<!no )(?<!what )(?<!these )(?<!those )' + B + r'(?:sort|kind)\s+of' + E, 'perhaps', 'maybe', 'arguably', 'seemingly',
    'apparently', 'presumably', 'supposedly', 'in fact', 'as a matter of fact', 'of course', 'obviously',
    'undoubtedly', 'without a doubt', 'no doubt', 'doubtless', 'admittedly', 'interestingly',
    'interestingly enough', 'it is interesting to note', 'it is worth mentioning', 'it bears mentioning',
    'more importantly', 'most importantly', 'you know', 'i mean', 'in other words', 'that is to say',
    'to put it simply', 'simply put', 'put simply', 'to put it another way',
    'to some extent', 'to a certain extent', 'to a large extent', 'to some degree', 'to a certain degree',
    'more or less', 'so to speak', 'as it were', 'if you will', 'in essence', 'by the way', 'incidentally',
    '!in a way', '!in a sense',
    'first of all', 'firstly', 'secondly', 'thirdly', 'lastly', 'what is more', "what's more",
    'generally speaking', 'broadly speaking', 'strictly speaking', 'on the one hand', 'on the other hand',
    'in any case', 'in any event', 'at any rate', 'that said', 'having said that', 'with that said',
    'that being said', 'with that being said', 'it seems that', 'it appears that', 'it would seem',
    'one might say', 'one could argue', 'it could be argued', 'it can be said', 'it may be said',
    'it must be said', "for what it's worth", 'of sorts',
    '!clearly', '!naturally', '!indeed', '!importantly', '!significantly', '!notably', '!remarkably',
    '!surprisingly', '!unsurprisingly', '!ironically', '!luckily', '!fortunately', '!unfortunately',
    '!sadly', '!hopefully', '!thankfully', '!anyway', '!anyhow', '!well', '!so', '!now', '!look', '!listen',
    '!ok', '!okay', '!right', '!besides', '!in general', '!in principle', '!technically', '!practically',
    '!ultimately', '!finally', '!moreover', '!furthermore', '!additionally', '!also', '!as such',
    '!all in all', '!overall', '!in short', '!in brief',
], weak=['just', 'simply', 'probably', 'possibly', 'generally', 'virtually'])

DICT['W-INTENS'] = dict(strong=[
    'very', 'really', 'extremely', 'incredibly', 'absolutely', 'totally', 'utterly', 'truly', 'hugely',
    'massively', 'tremendously', 'enormously', 'immensely', 'exceedingly', 'insanely', 'ridiculously',
    'super', 'quite', 'certainly', 'definitely', 'the very', 'maximally', 'guaranteed', 'for just',
    'for only', 'only at', 'only from', 'just for you', 'absolutely free', 'completely free', 'totally free',
    '100% free', 'by far', 'most definitely',
    r'r:' + B + r'so\s+(?:very\s+)?(?:good|great|easy|simple|fast|quick|important|useful|helpful|bad|hard|difficult|much|many|nice|cool|amazing|awesome|powerful|beautiful|happy|excited|grateful|proud|glad|sad|tired|crucial|vital|critical|valuable|popular|common|complex|complicated|warm|delightful|exciting|interesting|incredible|wonderful|special|unique|different|clear|obvious)' + E,
    r'r:' + B + r'way\s+(?:more|less|better|worse|too|faster|slower|bigger|smaller|easier|harder|cheaper)' + E,
], weak=[
    'the most', 'highly', 'deeply', 'completely', 'fully', 'entirely', 'perfectly', 'particularly',
    'especially', 'significantly', 'greatly', 'vastly', 'dramatically', 'drastically', 'considerably',
    'substantially', 'exceptionally', 'remarkably', 'terribly', 'awfully', 'pretty', 'rather', 'fairly',
    'genuinely', 'sheer', 'pure', 'at all', 'ultra*', 'mega',
])

DICT['W-EVAL'] = dict(strong=[
    'amazing', 'awesome', 'incredible', 'unbelievable', 'fantastic', 'fabulous', 'wonderful', 'marvel*',
    'magnificent', 'superb', 'extraordinary', 'remarkable', 'phenomenal', 'spectacular', 'stunning',
    'breathtaking', 'gorgeous', 'brilliant', 'excellent', 'perfect', 'flawless', 'impeccable', 'unparalleled',
    'unrivalled', 'unrivaled', 'unmatched', 'unbeatable', 'unprecedented', 'revolutionary', 'groundbreaking',
    'ground-breaking', 'innovative', 'premium', 'superior', 'top-notch', 'high-quality', 'top-quality',
    'second to none', 'ultimate', 'legendary', 'iconic', 'epic', 'tremendous', 'immense', 'colossal',
    'stellar', 'terrific', 'sensational', 'astonishing', 'astounding', 'mind-blowing', 'jaw-dropping',
    'life-changing', 'invaluable', 'priceless', 'indispensable', 'stylish', 'luxurious', 'exquisite',
    'delicious', 'lovely', 'charming', 'delightful', 'sublime', 'easy-to-use', 'user-friendly', 'intuitive',
    'hassle-free', 'effortless*', 'stress-free', 'worry-free', 'reputable', 'renowned', 'world-renowned',
    'world-famous', 'acclaimed', 'award-winning', 'prestigious', 'esteemed', 'impressive', 'premier',
    'exclusive', 'next-level', 'finest', 'greatest', 'coolest', 'smartest', 'catastrophic',
    'disastrous', 'horrible', 'terrible', 'awful', 'dreadful', 'appalling', 'outrageous', 'scandalous',
    'devastating',
    r'r:' + B + r'(?:best|greatest|biggest|largest|fastest|finest|cheapest|smartest|most\s+[a-z]+)\s+(?:ever|in the world|on the market|in town|in the industry|in its class|available)' + E,
    r'r:' + B + r'(?:our|the very)\s+best' + E,
    r'r:' + B + r'the\s+best\s+(?:product|service|solution|choice|quality|price|deal|team|company|provider|tool|app|platform|experience|results?|value|in|for you)' + E,
], weak=[
    'best', 'unique', 'essential', 'crucial', 'vital', 'critical', 'important', 'significant', 'major', 'great',
    'huge', 'massive', 'enormous', 'gigantic', 'effective', 'efficient', 'powerful', 'reliable', 'convenient',
    'comfortable', 'beautiful', 'elegant', 'luxury', 'distinguished', 'respected', 'trusted', 'successful',
    'dynamic', 'modern', 'advanced', 'sophisticated', 'professional', 'comprehensive', 'extensive', 'optimal',
    'ideal', 'leading', 'outstanding', 'exceptional', 'first-class', 'dramatic', 'tragic', 'unacceptable',
    'excellence', 'quality', 'smart', 'easy', 'simple', 'fast', 'perfectly',
])

DICT['W-ZAUM'] = dict(strong=[
    # PLAIN "Use simple words" (the dirty dozen and other clear cases); GOV.UK "utilise"
    'utiliz*', 'utilis*', 'commenc*', 'ascertain*', 'endeavo*', 'disseminat*', 'promulgat*', 'expedit*',
    'necessitat*', 'effectuat*', 'remuneration', 'accrue*', 'advantageous', 'methodolog*', 'enumerat*',
    'evidenced', 'optimum', 'practicable', 'preclud*', 'apprise*', 'deem*', 'assist', 'assists', 'assisted',
    'assisting', 'accorded',
    # long Latinate and academic words
    'paradigmatic', 'praxis', 'epistemolog*', 'juxtapos*', 'exacerbat*', 'ameliorat*', 'obfuscat*',
    'elucidat*', 'cognizant', 'cognisant', 'commensurate', 'efficacious', 'exigenc*', 'propensity',
    'proclivit*', 'quintessential*', 'nomenclature', 'conceptuali*', 'contextuali*', 'problematiz*',
    'problematis*', 'actualiz*', 'actualis*', 'concretiz*', 'modalit*', 'granularit*', 'disintermediat*',
    'infrastructural', 'aforethought', 'heretofore',
], weak=[
    'accompan*', 'accomplish*', 'accurate', 'additional', 'advise', 'allocat*', 'anticipat*', 'apparent',
    'appreciable', 'assistance', 'attain*', 'attempt*', 'capabilit*', 'component*', 'compris*',
    'consolidat*', 'demonstrat*', 'designat*', 'determin*', 'disclos*', 'discontinu*', 'eliminat*',
    'encounter*', 'equitable', 'establish*', 'evident', 'exhibit*', 'expend*', 'expertise', 'expiration',
    'feasib*', 'finaliz*', 'finalis*', 'forfeit*', 'furnish*', 'identical', 'implement*', 'inception',
    'indicat*', 'initiat*', 'magnitude', 'modif*', 'numerous', 'obligat*', 'parameters', 'participat*',
    'portion', 'possess*', 'procur*', 'proficien*', 'purchas*', 'relocat*', 'remainder', 'render*',
    'reside*', 'retain*', 'solicit*', 'subsequent*', 'substantial*', 'sufficient*', 'terminat*',
    'transmit*', 'validat*', 'viable', 'warrant*', 'witnessed', 'ensure', 'optimiz*', 'optimis*',
    'prioritiz*', 'prioritis*', 'monetiz*', 'monetis*', 'functionalit*', 'interoperab*', 'instantiat*',
    'heuristic*', 'ontolog*', 'heterogene*', 'homogene*', 'dichotom*', 'salient', 'ubiquit*', 'efficacy',
    'trajector*', 'cadence', 'sociali*', 'verticals', 'facilitat*', 'stakeholder*',
])

DICT['W-VAGUE-NUM'] = dict(strong=[
    r'r:' + B + r'(?:about|approximately|approx\.?|around|roughly|nearly|almost|some|circa|ca\.|upwards of|well over|well under|just over|just under|close to|as many as|as much as|in excess of)\s+' + NUMBER,
    r'r:' + B + r'(?:over|more than)\s+(?:[$£€]\s?)?(?:\d{1,3}(?:,\d{3})+|\d{4,}|\d+(?:\.\d+)?\s?(?:%|percent|per cent|k|m|bn|million|billion|thousand|trillion))\+?' + E,
    r'r:' + B + r'(?:about|approximately|around|roughly|nearly|almost|over|more than|upwards of|well over|close to|some)\s+(?:a\s+)?(?:hundred|thousand|million|billion|dozen|half|third|quarter|fifth|tenth|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)s?' + E,
    r'r:' + B + r'(?:about|approximately|around|roughly|nearly|almost|close to|some)\s+(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen)' + E,
    'the majority of', 'a majority of', 'the vast majority', 'a significant number of',
    'a significant portion', 'a large number of', 'a small number of', 'a great many', 'a good many',
    'dozens of', 'hundreds of', 'thousands of', 'millions of', 'billions of', 'countless',
    r'r:' + B + r'top[- ]?\d+' + E, 'top ten', 'top five', 'top three', 'one of the top', 'among the top',
    'one of the largest', 'one of the biggest', 'among the leaders', 'among the first', 'leading position*',
    'a leader in',
    r'r:' + B + r'(?:from|starting at|starting from|as low as|prices? from)\s+[$£€]\s?\d',
], weak=[
    r'r:' + B + r'(?:over|more than|less than|fewer than|up to|as few as|as little as)\s+' + NUMBER,
])

DICT['W-VAGUE'] = dict(strong=[
    'various', 'a variety of', 'a wide variety of', 'a wide range of', 'a broad range of', 'a number of',
    'tons of', 'a ton of', 'and much more', 'stuff', 'somehow', 'somewhat', 'relatively', 'in some cases',
    'in many cases', 'in certain cases', 'in some instances', 'in many instances', 'at some point',
    'in due course', 'at a later date', 'at a later stage', 'necessary measures', 'appropriate measures',
    'appropriate action', 'necessary steps', 'all necessary', 'and the like', 'in terms of', 'a certain',
    r'r:' + B + r'(?:certain|some|various|several|a number of|a few|numerous|multiple|different)\s+(?:issues|problems|challenges|difficulties|concerns|factors|aspects|areas|steps|measures|changes|improvements|benefits|advantages|situations|things|reasons|stakeholders|parties|considerations|limitations|elements|circumstances|conditions|matters|questions|cases|ways|options)' + E,
], weak=[
    'certain', 'several', 'multiple', 'numerous', 'a range of', 'a lot of', 'lots of', 'plenty of',
    'a bunch of', 'and so on', 'and so forth', 'etc', 'and more', 'things', 'thing', 'something',
    'somewhere', 'sometime', 'someone', 'comparatively', 'in most cases', 'in the coming weeks',
    'in the coming months', 'soon', 'shortly', 'as soon as possible', 'asap', 'appropriate', 'relevant',
    'aspect*', 'factor*', 'issues', 'case', 'nature', 'character',
])

# W-NOMINAL: a light verb + a nominalization (PLAIN "Avoid hidden verbs"), "the -tion of" (same),
# fixed phrases. NOM_EXCLUDE removes nouns that are not hidden verbs.
LIGHT_VERBS = (r'(?:make|makes|made|making|take|takes|took|taken|taking|give|gives|gave|given|giving|have|has|had|'
               r'having|reach|reaches|reached|reaching|achieve|achieves|achieved|achieving|effect|effected|effecting|'
               r'carry out|carries out|carried out|carrying out|conduct|conducts|conducted|conducting|perform|'
               r'performs|performed|performing|undertake|undertakes|undertook|undertaken|undertaking|provide|'
               r'provides|provided|providing|gain|gains|gained|gaining|do|does|did|done|doing|come to|came to|'
               r'arrive at|arrived at|arrives at|bring about|brought about|put forward|hold|holds|held|holding|'
               r'offer|offered)')
NOM_DET = (r'(?:(?:a|an|the|its|their|our|your|his|her|my|this|that|these|those|some|any|no|further|final|full|'
           r'thorough|careful|detailed|preliminary|formal|written|new|proper|regular|initial|quick|brief|complete|'
           r'comprehensive|independent|joint|an initial)\s+){0,2}')
NOM_WORD = (r'(?:[a-z]{3,}(?:tion|sion|ment|ance|ence|ysis|ancy|ency)s?|proposal|approval|refusal|removal|renewal|'
            r'arrival|disposal|withdrawal|dismissal|denial|referral|reversal|retrieval|closure|disclosure|'
            r'departure|failure|exposure|enclosure|review|study|survey|inspection|audit|estimate|attempt|choice|'
            r'request|purchase|inquiry|enquiry|response|reply|mention|reference|search|check|test|guess|'
            r'analysis|impact|effort)')
NOM_EXCLUDE = {
    'difference', 'experience', 'attention', 'question', 'questions', 'information', 'balance', 'chance',
    'distance', 'evidence', 'sentence', 'conference', 'audience', 'science', 'presence', 'confidence',
    'patience', 'insurance', 'finance', 'instance', 'substance', 'ambulance', 'license', 'licence',
    'nation', 'station', 'position', 'section', 'portion', 'motion', 'lotion', 'potion', 'fiction',
    'vacation', 'education', 'location', 'population', 'situation', 'condition', 'tradition', 'nutrition',
    'generation', 'organization', 'organisation', 'institution', 'foundation', 'competition', 'medication',
    'destination', 'version', 'mission', 'session', 'pension', 'mansion', 'tension', 'vision', 'division',
    'commission', 'occasion', 'profession', 'moment', 'element', 'document', 'documents', 'department',
    'government', 'environment', 'apartment', 'equipment', 'instrument', 'segment', 'fragment', 'garment',
    'appointment', 'treatment', 'compliment', 'supplement', 'ornament', 'sentiment', 'monument',
    'parliament', 'pigment', 'implement', 'performance', 'importance', 'relevance', 'significance',
    'reference', 'references', 'use', 'effort', 'test', 'check', 'search', 'documentation', 'permission',
    'action', 'actions', 'caution', 'precaution', 'precautions', 'opportunity', 'option', 'options',
    'function', 'functions', 'creation', 'collection', 'connection', 'connections', 'consideration',
    'translation', 'application', 'applications', 'presentation', 'certification', 'registration',
    'qualification', 'qualifications', 'notification', 'notifications', 'migration', 'integration',
    'configuration', 'description', 'descriptions', 'definition', 'definitions', 'solution', 'solutions',
    'payment', 'payments', 'statement', 'statements', 'guidance', 'reply', 'response', 'impact', 'study',
    'survey', 'review', 'audit', 'attempt', 'choice', 'request', 'purchase', 'mention', 'estimate', 'guess',
    'repercussion', 'ambition', 'direction', 'passion', 'expression', 'impression', 'dimension', 'extension', 'mission', 'permission',
}
NOM_STRONG_EXCLUDE = NOM_EXCLUDE - {
    'action', 'consideration', 'application', 'presentation', 'payment', 'statement', 'description',
    'guidance', 'reply', 'response', 'impact', 'study', 'survey', 'review', 'audit', 'attempt', 'choice',
    'request', 'purchase', 'mention', 'estimate', 'guess', 'use', 'reference', 'permission', 'effort',
}
NOM_LIGHT = re.compile(B + r'(' + LIGHT_VERBS + r')\s+(?!(?:sure|it|them|him|her|us|me|you|up|out|off|over|back|'
                       r'down|place|part|care|sense|time|way|not|never|also|just)' + E + r')' + NOM_DET +
                       r'(?:[a-z-]+\s+)?(' + NOM_WORD + r')' + E +
                       r'(?:\s+(?:of|for|to|on|with|about|in|into|regarding|that)' + E + r')?'
                       r'(?!\s+(?:clear|clearer|easy|easier|simple|simpler|long|longer|short|shorter|better|worse|'
                       r'possible|impossible|available|visible|obvious|difficult|harder|more|less|ready|work|happen|'
                       r'sense|shorter|faster|slower|smaller|bigger)' + E + r')')
NOM_THE_OF = re.compile(B + r"(?:the|its|their|our|your|his|her|[a-z]+'s|includes?|including|involves?|requires?|"
                        r"for|by|upon|after|before|following|through|during)\s+(?:[a-z]+\s+)?"
                        r'([a-z]{3,}(?:tion|sion|ment|ance|ence|ing)|proposal|approval|'
                        r'refusal|removal|renewal|arrival|disposal|withdrawal|dismissal|denial|referral|'
                        r'reversal|retrieval|use|provision)\s+of' + E)
THE_OF_EXCLUDE = NOM_EXCLUDE | {
    'beginning', 'meaning', 'building', 'morning', 'evening', 'ceiling', 'ending', 'wording', 'being',
    'nothing', 'something', 'everything', 'anything', 'setting', 'heading', 'feeling', 'painting',
    'drawing', 'reading', 'writing', 'wedding', 'meeting', 'training', 'king', 'spring', 'string', 'ring',
    'wing', 'thing', 'during', 'opening', 'following', 'offering', 'listing', 'lighting', 'housing',
    'clothing', 'bring', 'evening', 'sibling', 'ministry', 'evidence', 'existence', 'absence', 'convenience',
    'province', 'province', 'sequence', 'consequence', 'consequences', 'experience', 'importance', 'nuance',
    'alliance', 'appliance', 'glance', 'distance', 'romance', 'ordinance', 'ordnance', 'variance',
    'questionnaire', 'regulation', 'regulations', 'legislation', 'constitution', 'convention', 'portion',
    'proportion', 'percentage', 'remainder', 'majority', 'minority', 'department', 'secretary', 'office',
}
DICT['W-NOMINAL'] = dict(strong=[
    'make use of', 'makes use of', 'made use of', 'make reference to', 'make mention of',
    'take into consideration', 'taken into consideration', 'give consideration to', 'given consideration to',
    'gain an understanding', 'gain understanding', 'have knowledge of', 'has knowledge of',
    'acknowledge receipt', 'take action to', 'make a decision', 'made a decision', 'reach a decision',
    'make an application', 'make the payment', 'make a payment', 'undertake the calculation',
    'provide assistance', 'provide guidance', 'is in compliance with', 'are in compliance with',
    'in compliance with', 'achieve compliance', 'the use of',
], weak=[])

STATE_VERBS = dict(strong=[
    r'r:^["\'(\[\s—]*(?:the\s+)?(?:[a-z-]+\s+)?[a-z]{3,}(?:tion|sion|ment|ness|ity|ance|ence|ancy|ency)\s+(?:of\s+(?:the\s+|a\s+|an\s+|our\s+|its\s+|their\s+|this\s+)?(?:[a-z-]+\s+){1,4})?(?:will\s+|can\s+|could\s+|would\s+|may\s+|should\s+)?(?:ensure|ensures|allow|allows|enable|enables|lead to|leads to|contribute to|contributes to|improve|improves|reduce|reduces|increase|increases|provide|provides|facilitate|facilitates|result in|results in|help|helps|promote|promotes|drive|drives|support|supports|guarantee|guarantees|impact|impacts|affect|affects|boost|boosts)' + E,
    'constitutes', 'constitute', 'represents', 'is comprised of', 'are comprised of', 'is characterized by',
    'is characterised by', 'are characterized by', 'are characterised by', 'is indicative of',
    'is reflective of', 'is suggestive of', 'is dependent on', 'is dependent upon', 'are dependent on',
    'is in possession of', 'is in need of', 'are in need of', 'is in agreement', 'are in agreement',
    'there is a need for', 'there is a requirement', 'has the ability to', 'have the ability to',
    'has the capacity to', 'has the potential to', 'have the potential to', 'is capable of',
    'are capable of', 'allows for', 'provides for', 'entails', 'lies in', 'consists in', 'is rooted in',
    'has an impact on', 'have an impact on', 'had an impact on', 'has an effect on', 'have an effect on',
    'contribute to', 'contributes to', 'is tasked with', 'there exists', 'there exist', 'possesses',
    r'r:' + B + r'one\s+of\s+(?:the\s+)?(?:main\s+|key\s+|primary\s+|most important\s+|biggest\s+|major\s+)?(?:tasks|goals|aims|objectives|problems|reasons|features|advantages|benefits|priorities|challenges)\s+(?:of\s+[a-z ]+\s+)?(?:is|was|will be)' + E,
    r'r:' + B + r'(?:our|the|its|their)\s+(?:main|key|primary|biggest|major|core)\s+(?:advantage|strength|benefit|priority|goal|aim|objective|task|feature)\s+(?:is|was|lies)' + E,
], weak=[
    'consists of', 'serves as', 'takes place', 'occurs', 'results in', 'resulted in', 'leads to',
    'enables', 'ensures', 'involves', 'implies', 'is subject to', 'is associated with', 'stems from',
    'is reflected in', 'remains', 'exists',
])

POLITE = [
    'please', 'kindly', 'thank you in advance', 'thanks in advance', 'thanking you in advance',
    'we would be grateful', 'i would be grateful', 'would be most grateful', 'we would appreciate',
    'i would appreciate', 'it would be appreciated', 'your cooperation is appreciated',
    'your patience is appreciated', 'we appreciate your patience', 'we appreciate your understanding',
    'thank you for your understanding', 'thank you for your patience', 'thank you for your cooperation',
    'we apologi* for any inconvenience', 'sorry for any inconvenience', 'apologies for any inconvenience',
    'we regret any inconvenience', 'sorry to bother you', 'sorry for the trouble', "if you don't mind",
    "if it's not too much trouble", 'if it is not too much trouble', 'at your earliest convenience',
    'at your convenience', 'do not hesitate', "don't hesitate", 'feel free to', 'we kindly ask',
    'kindly note', 'with all due respect', 'humbly', 'we would like to thank', 'we are pleased to',
    "we're pleased to", 'we are delighted to', "we're delighted to", 'we are happy to', "we're happy to",
    'we are excited to', "we're excited to", 'we are thrilled to', "we're thrilled to",
    'it is our pleasure', "it's our pleasure", 'it is with great pleasure', 'valued customer*',
    'dear valued', 'we value your', 'your call is important', 'hope this email finds you well',
    'hope this finds you well', 'hope you are well', "hope you're well", "hope you're doing well",
    'hope you are doing well', 'i trust this', 'trust you are well',
]

# ---------------------------------------------------------------- grammar patterns

# W-PASSIVE: a form of "be" + up to two adverbs + a past participle.
BE_FORMS = (r"(?:am|is|are|was|were|be|been|being|(?:it|he|she|that|this|what|who|which)'s|(?:they|we|you)'re)")
PASSIVE = re.compile(r"(?<![a-z0-9'])" + BE_FORMS +
                     r"(?:\s+(?:not|never|also|already|often|always|still|just|then|now|only|even|thus|being|"
                     r"all|both|each|usually|[a-z]{3,}ly)){0,2}\s+([a-z]+)(?![a-z0-9-])")
IRREGULAR = set('''
arisen awoken beaten begun bent bid bitten bled blown broken brought built burnt burned bought caught chosen cost
cut dealt done drawn dreamt driven drunk eaten fed felt fought found fled flung forbidden forgotten forgiven frozen
given ground grown hung heard hidden hit held hurt kept knelt known laid led lent let lit lost made meant met paid
put quit read ridden rung run said seen sought sold sent set sewn shaken shed shone shot shown shrunk shut sung sunk
slain slept slid slung slit sown spoken sped spent spilt spun split spread sprung stood stolen stuck stung struck
strung sworn swept swollen swung taken taught torn told thought thrown thrust trodden understood undertaken upheld
woken worn woven wed wept won wound withdrawn withheld written overcome overseen overtaken overthrown misled
misunderstood rewritten rebuilt redone foreseen forecast broadcast outdone beset bound bred clung dug used owed tied
dyed eyed axed iced
'''.split())
NOT_PARTICIPLE = set('''
need seed feed deed heed weed reed speed steed greed breed bleed creed tweed indeed proceed succeed exceed hundred
sacred naked wicked rugged ragged kindred wretched jagged crooked beloved embed aged shred bed red
'''.split())
PASSIVE_EXCLUDE = set('''
located situated interested concerned involved related based supposed married divorced tired bored excited worried
pleased satisfied dissatisfied surprised scared frightened disappointed amazed confused embarrassed exhausted
delighted determined dedicated committed devoted qualified experienced skilled talented advanced complicated
sophisticated detailed crowded gone closed limited entitled inclined equipped composed prepared accustomed
acquainted relaxed stressed motivated mistaken upset aged armed obliged convinced acquired renowned thrilled
honored honoured humbled impressed shocked stunned touched overwhelmed annoyed frustrated irritated puzzled
intrigued fascinated blessed privileged engaged focused obsessed alarmed ashamed tired
'''.split())

# P-EXPLETIVE: "there is/are … that/who" and "it is … that/to" frames; Strunk's "he is a man who".
THERE_BE = re.compile(B + r"there(?:'s|'re|\s+(?:is|are|was|were|will be|would be|has been|have been|had been|may be|"
                      r"might be|could be|can be|should be|must be|seems to be|seem to be|appears to be|"
                      r"appear to be|remains|remain|exists|exist))" + E)
IT_ADJ = re.compile(B + r"it(?:'s|\s+(?:is|was|will be|would be|has been|had been|may be|might be|can be|could be|"
                    r"should be|must be|seems|seemed|appears|appeared|becomes|became|remains|remained))\s+"
                    r"(?:(?:not|very|so|quite|really|extremely|particularly|especially|more|most|less|too|also|"
                    r"therefore|thus|[a-z]+ly)\s+){0,2}([a-z-]+)\s+(?:for\s+(?:[a-z]+\s+){1,2})?"
                    r"(?:that|to|whether|if|how|why|who)" + E)
IT_ADJ_EXCLUDE = set('''a an the this that these those my your our their his her its time up going able used designed
meant supposed built made intended set about due trying what where how all one something nothing here there now
then not also only just still being'''.split())
IT_NOUN = re.compile(B + r"it(?:'s|\s+is|\s+was|\s+would be|\s+will be)\s+(?:a|an|the)\s+(?:[a-z-]+\s+)?(?:idea|pity|"
                     r"shame|mistake|fact|case|practice|matter|question|wonder|surprise|habit|myth|truth|privilege|"
                     r"pleasure|honou?r|relief|challenge|necessity|requirement|must|good idea|bad idea)\s+"
                     r"(?:that|to|whether)" + E)
STRUNK_WHO = re.compile(B + r"(?:he|she|it|this|that|they)\s+(?:is|was|are|were)\s+an?\s+(?:[a-z]+\s+)?(?:man|woman|"
                        r"person|subject|country|thing|one|kind|type|sort)\s+(?:who|which)" + E)

# P-REFERENT: a sentence that opens with a bare this/that/these/those/it/which + verb.
REF_START = re.compile(r"^[\"'(\[\s—]*(this|that|these|those|it|which)(?![a-z0-9'])('s|'ll|'d|'ve|'re)?"
                       r"(?:\s+([a-z][a-z'-]*))?(?:\s*([a-z]+|[,.;:!?]))?")
AUX = set('is was are were has had have will would can could may might should must does did do shall '
          "isn't wasn't aren't weren't hasn't hadn't haven't won't wouldn't can't cannot couldn't doesn't didn't "
          "don't shouldn't".split())
PLURAL_VERBS = set('''include mean help allow show make give let require need lead cause create provide enable
explain suggest imply reflect apply depend seem appear become work take add come go remain represent contain
ensure affect make matter'''.split())
FUNC_AFTER = set('''the a an to in us me them him her it that this these those from by on for our your their my
its some many more less no not all both each every up out down off over into onto with at as you we they
people everyone anyone users'''.split())
NOUN_S = set('''news series species lens gas bus chaos canvas atlas alias bias basis thesis crisis analysis
process class status focus campus bonus virus census corpus radius address business access success progress
loss boss glass mass pass press dress stress guess cross miss plus minus summons physics mathematics economics
politics ethics logistics statistics analytics means ways days years times months weeks'''.split())

# P-GLUED: two sentences joined by a comma.
GLUE_PRON = re.compile(r",\s+(i|we|you|they|he|she|it|there|this|these|those)(?:('s|'re|'ll|'ve|'d|'m)|"
                       r"\s+(?:(?:also|still|just|then|now|never|always|often|usually|really|only|already|even|"
                       r"all|both)\s+)?([a-z][a-z'-]*))" + E)
GLUE_POSS = re.compile(r",\s+(?:our|my|your|their|his|her|its)\s+[a-z-]+(?:\s+[a-z-]+)?\s+(?:is|are|was|were|has|"
                       r"have|had|will|can|could|should|must|include|includes|[a-z]{2,}ed)" + E)
GLUE_ADV = re.compile(r",\s+(?:however|therefore|thus|hence|otherwise|consequently|nevertheless|nonetheless|"
                      r"moreover|furthermore|instead|meanwhile|accordingly|as a result|in fact|indeed)\s*,?\s+"
                      r"(?:i|we|you|they|he|she|it|this|that|there|the|our|my|your|their)" + E)
GLUE_START = set('i we you they he she it this that these those there the a an our my your their his her its '
                 'some many most all each every no'.split())
NON_SUBJECT_OPENERS = set('''if when whenever while although though even because since as after before once unless
until whether whereas where wherever so now given provided in on at for by with without to from during under over
through despite like unlike according having being using based following regarding besides apart instead yes no
well also however first second third finally then next still oh ok okay sure of thanks whatever whoever whichever
perhaps unfortunately fortunately today here only just please note remember and but or nor yet hence thus
therefore moreover furthermore again indeed otherwise meanwhile instead'''.split())
GLUE_FINITE = re.compile(B + r"(?:is|are|was|were|am|has|have|had|will|would|can|could|may|might|shall|should|must|"
                         r"do|does|did|isn't|aren't|wasn't|weren't|don't|doesn't|didn't|can't|won't|cannot)" + E +
                         r"|" + B + r"(?:i|we|you|they|he|she|it)\s+(?:[a-z]+ly\s+)?[a-z]{2,}" + E)
GLUE_INTRO_END = re.compile(B + r"(?:for example|for instance|in fact|of course|however|therefore|as a result|"
                            r"in addition|in short|that is|e\.g|i\.e|then|now|so|again|also|still|instead|yes|no|"
                            r"well|first|second|finally|today|here)\s*$")
SUBORD_ANY = re.compile(B + r'(?:if|when|whenever|while|although|though|because|since|unless|until|whereas|whether|'
                        r'after|before|once|as soon as|so that|even though|even if|which|who|whom|whose|where)' + E)
BASE_VERBS = set('''use make take get need want have offer provide build work help recommend suggest know think see
can love create sell support serve deliver cover run ship design develop believe focus specialize specialise
include accept charge send check review process handle plan hope expect keep try write call give go come do pay
buy find stay leave move start stop open close bring hold'''.split())
SPEECH = set('said says asked replied added noted explained wrote think thinks believe believes hope guess suppose '
             'mean know see'.split())
SUBORD = re.compile(B + r'(?:which|who|whom|whose|whether|if|when|whenever|while|because|since|although|though|'
                    r'unless|until|whereas|where|so that|even though|even if|as long as|provided that|once)' + E +
                    r'|' + B + r'that\s+(?:the|a|an|i|we|you|they|he|she|it|this|these|those|there|our|your|their|'
                    r'his|her|its|my|no|all|some|any|each|every)' + E)
INLINE_LIST_MARK = re.compile(B + r'(?:as well as|and/or|etc|and so on|and so forth|and others|and other|or other|'
                              r'including|such as|among others|inter alia|and more)' + E)
SERIAL_LIST = re.compile(B + r'[^,;:.!?()]{1,30},\s*(?:[^,;:.!?()]{1,25},\s*){2,}(?:and|or)(?=\s+[a-z])')
FRAGMENT_START = re.compile(r'^["\'(\[\s—]*(?:such as|including|especially|particularly|not to mention|let alone|'
                            r'along with|together with|as well as|like when|for instance when)' + E)
SUBCLAUSE_START = re.compile(r'^["\'(\[\s—]*(?:because|although|though|even though|whereas|while|if|when|unless|'
                             r'since)' + E)

# M-HOLLOW, S-INTRO, S-OUTRO, S-CLICKBAIT
INTRO_OPENERS = [
    "in today's", 'in this day and age', 'nowadays', 'in recent years', 'in the modern world',
    'in our modern world', 'it is no secret', "it's no secret", 'it is widely known', 'everyone knows',
    'we all know', 'have you ever wondered', 'have you ever', 'did you know', 'imagine a world',
    'picture this', 'in this article', 'in this post', 'in this blog post', 'in this guide',
    'in this tutorial', 'in this piece', 'this article will', 'this post will', 'this guide will',
    'in the following article', 'we will explore', "we'll explore", 'we will discuss', "we'll discuss",
    'we will look at', "we'll look at", "let's explore", "let's dive", "let's take a look", 'welcome to',
    'hello everyone', 'hi everyone', 'hey there', 'since the dawn of time', 'throughout history',
    'since time immemorial', 'from the beginning of time', 'for centuries', 'cannot be overstated',
    "can't be overstated", 'it is impossible to overstate', 'it is hard to overstate',
    'it is difficult to overstate', 'it goes without saying', 'needless to say', 'more and more',
    'increasingly important', 'becoming increasingly', 'more important than ever', 'now more than ever',
    "i've been thinking", 'i have been thinking', 'i decided to write', 'i wanted to share',
    'i want to share', 'i would like to share', "i'd like to share", 'i would like to talk',
    "i'd like to talk", 'as we all know', 'one of the most',
]
OUTRO_CLOSERS = [
    'in conclusion', 'to conclude', 'in summary', 'to summarize', 'to summarise', 'to sum up', 'summing up',
    '!all in all', '!overall', '!in the end', 'thank you for reading', 'thanks for reading',
    'thank you for your attention', "that's all", "that's it for", 'that is all', 'i hope this helps',
    'hope this helps', 'i hope you found', 'hope you found this', 'i hope this article', 'i hope this post',
    'i hope this guide', 'hope you enjoyed', 'happy coding', 'happy reading', 'stay tuned',
    'let me know in the comments', 'leave a comment', 'share your thoughts', 'let us know what you think',
    'feel free to reach out', 'if you have any questions', 'do not hesitate to contact',
    "don't hesitate to contact", 'as we have seen', "as we've seen", 'we have explored', "we've explored",
    'we have discussed', "we've discussed", 'we have looked at', 'only time will tell',
    'the future is bright', 'the future looks bright', 'the possibilities are endless', 'the sky is the limit',
    'the choice is yours', 'what are you waiting for',
    r'r:' + B + r'the future\s+(?:of\s+[a-z ]+?\s+)?(?:is|looks)\s+(?:bright|exciting|promising)' + E, r'r:^\W*the end\W*$', 'by following these',
    'with these tips',
]
CLICKBAIT = [
    'shocking', 'shock', "you won't believe", 'you will not believe', 'blow your mind', 'mind-blowing',
    'jaw-dropping', 'unbelievable', 'incredible', 'amazing', 'insane', 'crazy', 'epic', 'ultimate guide',
    'the ultimate', 'complete guide', 'the complete guide', 'definitive guide', 'the definitive',
    'everything you need to know', 'all you need to know', 'what no one tells you', 'nobody tells you',
    'no one is talking about', 'the truth about', 'the real reason', 'secret', 'secrets', 'little-known',
    'hack', 'hacks', 'this one trick', 'weird trick', 'trick', 'tricks', 'game-changer', 'game-changing',
    r'r:' + B + r'must-(?:read|know|have|see|try|watch)' + E, 'will change your life', 'changed my life', 'change everything',
    'changes everything', "here's why", "here's what", "here's how", 'this is why', 'this is what',
    'why you should', 'stop doing', 'stop using', 'never again', "before it's too late", 'goes viral',
    'went viral', 'broke the internet', 'breaks the internet', 'exposed', 'revealed', 'urgent', 'breaking news',
    r'r:^\W*breaking\s*:',
    'exclusive', 'sensational', 'nobody expected', 'no one expected', 'will make you', 'gone wrong',
    'mistakes everyone makes', 'reasons why',
    r'r:' + B + r'\d+\s+(?:things|ways|reasons|facts|mistakes|secrets|rules|tips|tricks|hacks|signs|steps|lessons|habits|tools|books|movies|films|places|ideas|examples|questions|myths|truths|lies|strategies|features|benefits)' + E,
]
ACRONYMS = set('''USA UK EU UN NATO NASA FBI CIA CDC WHO EPA FDA IRS HMRC NHS DVLA DWP GOV API URL HTML CSS JSON XML
YAML SQL PDF CSV FAQ CEO CTO CFO COO HR IT PR SEO UX UI AI ML LLM GPT SAAS B2B B2C ROI KPI OKR MVP CRM ERP SDK CLI
GUI IDE OS IOS CPU GPU RAM SSD HDD USB HDMI LED LCD GPS SMS MMS VPN DNS HTTP HTTPS TCP UDP IP SSH FTP AWS GCP MIT BSD
GPL CMS FEMA HUD FAA PC TV DIY ASAP FYI ETA OK NB PS AM PM BBC CNN NYC LA DC US MBA PHD MD RN ISO GDPR HIPAA PCI SOC
CCPA VAT GST GDP CPI NGO NPO LLC LTD INC PLC ATM PIN ID QR NFT CTA AR VR IOT SLA SLO SRE QA CI CD PRD RFC ADR TBD
TODO FIXME README NMW OECD IMF ONS CFR ANCSA BLM CMS EFT ACH IBAN SWIFT BIC NASDAQ NYSE ETF IPO SEC FCA ECB
COVID CHAPS NATO UNESCO UNICEF OFSTED OFGEM OFCOM HMCTS DVSA DEFRA DSIT BEIS FCDO NIST IEEE ANSI ASCII UTF
'''.split())
CAPS_HYPE = set('NEW FREE NOW WOW OMG BEST HUGE SALE MUST STOP HOT WIN YES NEVER EVER ALL GET BIG TOP WHY HOW '
                'WHAT'.split())

# T-NUMBERS, M-FACTS
FAKENUM = [
    re.compile(r'(?<![\d.,])\d{1,3}(?:\.\d+)?\s?(?:%|percent|per cent)\s+(?:of\s+)?(?:all\s+)?(?:the\s+)?(?:people|'
               r'users|customers|clients|americans|britons|brits|europeans|adults|women|men|employees|workers|'
               r'companies|businesses|firms|consumers|respondents|developers|parents|students|drivers|readers|'
               r'managers|executives|ceos|marketers|teams|organi[sz]ations|shoppers|buyers|patients|doctors|teachers|'
               r'children|kids|millennials|internet users|online shoppers|small businesses|startups|leaders)' + E),
    re.compile(B + r'(?:\d|nine|eight|seven|six|four|three)\s+(?:out\s+)?of\s+(?:10|ten|5|five)' + E +
               r'(?!\s*(?:steps|stars|points))'),
]
SOURCE = re.compile(r'according to\s+(?!(?:studies|research|experts|surveys|analysts|specialists|scientists|many|'
                    r'some|most)\b)[a-z"]|source:|sources:|survey by|study by|report by|data from|published|journal|'
                    r'census|gallup|pew|statista|nielsen|gartner|forrester|mckinsey|deloitte|ipsos|yougov|\bons\b|'
                    r'office for national statistics|bureau of|\boecd\b|world bank|\bimf\b|eurostat|\bet al\b|'
                    r'\(\d{4}\)|\[\d+\]|https?:|\]\(')
NOUSE = [
    r'r:' + B + r'we\s+(?:have|employ)\s+(?:over\s+|more than\s+|nearly\s+|almost\s+)?\d[\d,]*\+?\s+(?:employees|staff|people|specialists|engineers|experts|professionals|team members)' + E,
    'cups of coffee', 'lines of code',
    r'r:' + B + r'\d[\d,]*\+?\s+(?:calls|emails|e-mails|requests|tickets|orders|messages|meetings)\s+(?:a|per|every)\s+(?:day|week|month)' + E,
    r'r:' + B + r'(?:founded|established|incorporated)\s+in\s+\d{4}' + E,
    r'r:' + B + r'in\s+business\s+(?:since|for)\s',
]
UNITS = re.compile(r'(?<![a-z])\d+(?:[.,]\d+)?\s?(?:mah|ghz|mhz|gb|tb|mb|kb|gbps|mbps|kbps|mm|cm|kg|lbs?|oz|kw|kwh|'
                   r'lm|lumens|db|rpm|mph|km/h|kph|hz|nits|fps|mp|megapixels?|ip\d{2}|inch(?:es)?|cores?|watts?)'
                   r'(?![a-z])')
UNROUNDED = re.compile(r'(?<![\d.,$£€#+/-])(?:\d{2,3}(?:,\d{3})+|\d(?:,\d{3}){2,})(?:\.\d+)?(?![\d,]*\d)')
EXAMPLE_MARKERS = re.compile(B + r"(?:for example|for instance|e\.g\.|such as|imagine|suppose|let's say|say,|"
                             r"consider|picture this|case study|in practice|in my experience|when i|when we|"
                             r"last year|last week|last month|here is an example|here's an example|example:|"
                             r"to illustrate|as an illustration|like when|take the case)" + E)
RESTRICT = re.compile(B + r"(?:except|unless|only if|only when|provided that|as long as|no later than|not later than|"
                      r"must not|may not|cannot|can't|do not|don't|never|note|important|warning|caution|deadline|"
                      r"excluding|does not apply|not eligible|non-refundable|not refundable|subject to|penalty|"
                      r"penalties|fee|fees|at your own risk)" + E)
SEQUENCE = re.compile(B + r'(?:then|next|after that|afterwards|subsequently|finally|lastly|first|firstly|secondly|'
                      r'thirdly|step\s+\d+|stage\s+\d+|phase\s+\d+|at the next stage|in the next step|at this stage|'
                      r'in turn)' + E)
STOCK_WORDS = re.compile(r'business|success|team|handshake|light ?bulb|puzzle|gears?|cogs?|growth chart|'
                         r'business ?(?:m[ae]n|wom[ae]n)|smiling|happy|office|laptop|suit|stock|idea|teamwork|'
                         r'diverse|meeting|celebrat')
STOCK_SRC = re.compile(r'shutterstock|istock|depositphotos|freepik|unsplash|pexels|pixabay|gettyimages|'
                       r'dreamstime|123rf|stock\.adobe|google\.|bing\.|images\.|stock')
LIST_START_WEAK = re.compile(r'^(?:also|in addition|additionally|for example|for instance|however|moreover|'
                             r'furthermore|and|but|or|so|then|besides|plus|as well as)' + E)
NOMINAL_DENSE = re.compile(B + r'[a-z]{3,}(?:tion|sion|ment)s?' + E)
TRIAD = re.compile(B + r'((?:more\s+)?[a-z]+(?:-[a-z]+)?),\s+((?:more\s+)?[a-z]+(?:-[a-z]+)?),?\s+(?:and|or)\s+'
                   r'((?:more\s+)?[a-z]+(?:-[a-z]+)?)' + E)
TRIAD_ABSTRACT = re.compile(r'(?:ness|ity|ion|ment|ance|ence|ive|ful|ous|able|ible|ency|ancy|ism|ship|thy)$')
NOT_X_Y = re.compile(B + r"(?:(?:it|this|that|these|they|we|you|he|she)'(?:s|re)\s+not|(?:is|are|was|were)"
                     r"(?:n't|\s+not))\s+(?:(?:just|only|merely|simply)\s+|(?=(?:a|an|the|about|your|our|my|their|some|"
                     r"just|only|merely|simply)\s))(?:about\s+)?[^.!?;:—]{1,60}?\s*(?:[.;:—]|,)\s*(?:it|this|that|these|they|we|you|he|she)"
                     r"(?:'s|'re|\s+is|\s+are|\s+was|\s+were)\s+(?:about\s+)?[a-z]+")

# W-NOUNSTACK: words that cannot be part of a noun string.
NS_STOP = set('''a an the this that these those my your his her its our their whose which who whom what whatever
whichever i me we us you he him she they them it one ones myself yourself ourselves themselves itself himself
herself and or but nor so yet for if then than as because since although though while whereas unless until when
where why how whether once of in on at by to from with without within into onto over under above below between
among across through throughout during before after about against along around behind beyond near via per like
unlike toward towards upon off out up down is am are was were be been being have has had having do does did done
doing will would shall should can could may might must not no never also only just very too quite rather even
still already always often sometimes usually again ever here there now today tomorrow yesterday all any some each
every both either neither few many much more most less least several such other another same own enough please
yes ok okay two three four five six seven eight nine ten hundred thousand million billion first second third get
gets got make makes made take takes took give gives gave go goes went come comes came see sees saw know knows knew
think thinks thought say says said tell tells told find finds found want wants try tries ask asks keep keeps let
lets put puts show shows send sends click clicks select selects enter enters add adds remove removes delete deletes
create creates install installs apply applies allow allows provide provides include includes require requires
contain contains ensure ensures follow follows manage manages reduce reduces improve improves protect protects
prevent prevents receive receives submit submits choose chooses decide decides explain explains describe describes
understand understands mean means seem seems become becomes leave leaves bring brings hold holds begin begins
enable enables disable disables configure configures visit visits connect connects help helps need needs use uses
new old good bad big small large high low long short great little main major minor next last early late full free
easy hard simple clear sure able real right wrong true false whole open close private general specific special
common current recent final certain possible available necessary various top best better worse worst basic complex
quick fast slow safe secure ready likely unlikely daily weekly monthly yearly annual previous entire initial extra
further young hot cold warm dark light white black red green blue yellow rich poor cheap wide narrow deep strong
weak heavy nice fine happy sad busy empty dry wet clean dirty alive dead single double multiple separate similar
related relevant different important own etc'''.split())
VERB_TRIGGER = set('''i we you they to can could will would shall should must may might often always never usually
also just please not cannot don't doesn't didn't won't let that which who'''.split())
VERB_AFTER_PLURAL = set('''read scan host use need want get make take see find say know like prefer expect look come
go work help try buy pay visit write click search skim ignore leave feature include provide offer show tell ask
give keep start stop run live spend share choose follow report review agree think believe understand'''.split())
NOUN_AL = set('''animal animals rental rentals portal portals hospital hospitals manual manuals signal signals proposal
proposals approval approvals removal arrival arrivals capital journal journals terminal terminals principal total
totals interval intervals material materials tutorial tutorials rival rivals festival festivals criminal criminals
individual individuals official officials professional professionals metal metals pedal crystal canal canals goal
goals deal deals meal meals seal seals appeal appeals cereal trial trials dial scandal mammal medal medals
withdrawal disposal referral renewal survival denial refusal dismissal reversal retrieval rehearsal potential
editorial memorial testimonial aerial commercial initial'''.split())
ADJ_COMMON = set('''efficient different sufficient relevant significant recent current independent excellent
consistent apparent urgent frequent permanent prominent transparent convenient intelligent competent confident
dependent evident innocent constant distant elegant abundant redundant reluctant vibrant brilliant pleasant
ignorant arrogant dominant resistant compliant tolerant vacant fragrant radiant overall minimum maximum
popular regular familiar peculiar nuclear solar lunar polar public appropriate adequate accurate separate
immediate private ultimate legitimate approximate everyday
average moldy mouldy dusty rusty sticky
noisy windy rainy sunny cloudy icy salty spicy juicy tasty healthy wealthy lucky risky tricky messy sloppy shiny
sleepy hungry angry thirsty tiny pretty crazy lazy fancy handy catchy buggy flaky leaky hefty unhealthy damp
fresh quality'''.split())
PLURAL_MODIFIERS = set('''sales savings news goods parts systems arms sports customs earnings rights procedures
services operations communications resources materials standards records claims benefits payments assets accounts
needs skills students workers users customers employees veterans members programs programmes projects products
events results terms rules jobs works things affairs relations data media facilities utilities securities
'''.split())
NOUN_IAL = set('''material materials tutorial editorial memorial trial dial serial credential potential official
burial denial testimonial aerial commercial initial'''.split())
NOUN_ISH = set('english polish radish parish relish rubbish spanish swedish danish finnish turkish'.split())
IMPERATIVES = set('''write read use check call see ask tell make keep include avoid add remove update open click
choose select send put set give try start stop run test consider follow find contact apply pay report review
return fill complete enter type print sign save upload download install rotate delete create build take bring get
look go explain describe list define limit break group organize organise place move replace change cut drop omit
show state say plan prepare tighten attend visit protect engineer register'''.split())
NOUN_LY = set('family supply assembly reply apply anomaly monopoly butterfly ally rally italy july fly lily jelly '
              'belly bully folly holly'.split())
NOUN_ED = set('need speed feed seed bed shed hundred deed breed greed weed reed creed'.split())
NOUN_ING = set('''building training meeting processing testing planning funding housing learning marketing
engineering accounting banking manufacturing programming rendering logging routing caching scheduling monitoring
reporting pricing staffing hiring onboarding billing shipping packaging labeling labelling parking lighting heating
cooling plumbing clothing wedding painting drawing writing spelling warning booking licensing licencing printing
recycling farming mining fishing nursing teaching tracking mapping hosting streaming networking computing messaging
branding consulting financing lending spending sampling screening counseling counselling tutoring mentoring
coaching catering cleaning roofing flooring wiring welding rating ranking filing posting listing setting offering
opening ending beginning morning evening ceiling string thing king ring spring wing sibling'''.split())
NOUN_IVE = set('''objective executive directive initiative incentive alternative representative detective archive
perspective motive native relative drive hive olive five live adhesive explosive narrative collective cooperative
derivative preservative additive locomotive prerogative operative'''.split())
NOUN_ABLE = set('table cable variable deliverable vegetable stable receivable payable timetable constable fable '
                'bible'.split())
NOUN_EST = set('request interest forest contest protest harvest digest manifest conquest inquest behest arrest '
               'guest chest quest test west'.split())
COMPARATIVES = set('''better bigger larger higher lower faster slower newer older smaller greater longer shorter
easier harder simpler safer cheaper wider deeper stronger weaker earlier later never ever however whether either
neither other rather further together over under after sooner clearer fewer lesser closer richer poorer smarter
quicker broader narrower tighter looser louder quieter brighter darker younger'''.split())

# ---------------------------------------------------------------- parsing the text

PROTECT = ''
ABBR_ANYCASE = re.compile(r'(?<![\w.])(?:e\.g|i\.e|cf|vs|viz|et al|approx|incl|esp|resp)\.', re.I)
ABBR_TITLES = re.compile(r'(?<![\w.])(?:Mr|Mrs|Ms|Mx|Dr|Prof|St|Mt|Ft|Gen|Col|Lt|Capt|Cmdr|Sgt|Gov|Sen|Rep|Rev|Hon|'
                         r'Pres|Supt|Messrs|Mmes)\.')
ABBR_NUMBER = re.compile(r'(?<![\w.])(?:no|nos|fig|figs|p|pp|ch|chap|sec|vol|vols|art|para|eq|ex|ref|v|ver|op|ca|c|'
                         r'est|tel|ext|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\.(?=\s*\d)', re.I)
INITIAL = re.compile(r'(?<![\w])[A-Z]\.(?=\s*[A-Z])')
SENT_END = re.compile(r'[.!?…]+["\'”’)\]*_`]*(\s+)(?=["\'“‘(\[*_`]*\s*[A-Z0-9])')
LIST_ITEM = re.compile(r'^(\s*)(?:[-*+•—–]|\d{1,3}[.)])\s+')
HEADING = re.compile(r'^(#{1,6})\s+')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]*)\)')
LINK_URL = re.compile(r'\]\(([^)]*)\)')
CODE_SPAN = re.compile(r'`[^`\n]*`')
BARE_URL = re.compile(r'(?:https?://|www\.)\S+|\S+@\S+\.[a-z]{2,}')
TABLE_SEP = re.compile(r'^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$')
SKIP_LINE = re.compile(r'^(?:\{:.*\}|\{::?/?[a-z]*\}|</?[A-Za-z][^>]*>|<!--.*-->)$')
WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
TOKEN = re.compile(r"[A-Za-z][A-Za-z'’-]*|\d+|[^\sA-Za-z\d]")
NORM_TABLE = {ord('’'): "'", ord('‘'): "'", ord('“'): '"', ord('”'): '"', ord('–'): '—', ord(' '): ' '}


def split_sentences(text):
    """English sentence spans; abbreviations, initials, decimals, versions, URLs and file names survive."""
    prot = text
    for rx in (ABBR_ANYCASE, ABBR_TITLES, ABBR_NUMBER, INITIAL):
        prot = rx.sub(lambda m: m.group(0).replace('.', PROTECT), prot)
    spans, start = [], 0
    for m in SENT_END.finditer(prot):
        spans.append((start, m.start(1)))
        start = m.end(1)
    spans.append((start, len(prot)))
    return [(a, b) for a, b in spans if text[a:b].strip()]


def normalize(text):
    """Lower case, straight quotes, — for dashes; markup, URLs and code spans blanked (length kept)."""
    t = ''.join(c.lower() if len(c.lower()) == 1 else c for c in text).translate(NORM_TABLE)
    t = LINK_URL.sub(lambda m: '](' + ' ' * len(m.group(1)) + ')', t)
    t = CODE_SPAN.sub(lambda m: ' ' * len(m.group(0)), t)
    t = BARE_URL.sub(lambda m: ' ' * len(m.group(0)), t)
    t = re.sub(r'(?<=\s)-(?=\s)', '—', t)
    return re.sub(r'[*_`#>|]', ' ', t)


class Block(object):
    def __init__(self, n, kind, text, line, level=0):
        self.n, self.kind, self.text, self.line, self.level = n, kind, text, line, level
        self.meta_title = False     # the YAML front matter has a title
        self.norm = normalize(text)
        self.sents = split_sentences(text) if kind not in ('table', 'image') else [(0, len(text))]

    def sent_of(self, pos):
        for i, (a, b) in enumerate(self.sents, 1):
            if a <= pos < b:
                return i
        return len(self.sents)

    def line_of(self, pos):
        return self.line + self.text[:pos].count('\n')


class _Buffer(object):
    """Lines of the current paragraph, quote or table until a blank line."""

    def __init__(self):
        self.lines, self.kind, self.line = [], 'para', 0


def parse_blocks(text):
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    has_blank = any(not l.strip() for l in lines[1:-1])
    # YAML front matter is not text
    skip_until = 0
    if lines and lines[0].strip() == '---':
        for i in range(1, min(len(lines), 60)):
            if lines[i].strip() == '---':
                skip_until = i + 1
                break
    meta_title = any(re.match(r'\s*title\s*:\s*\S', l) for l in lines[1:skip_until])
    # pipe tables without a leading "|": a header line followed by a --- | --- line
    table_lines = set()
    for i, l in enumerate(lines):
        if TABLE_SEP.match(l) and '|' in l:
            j = i - 1
            if j >= 0 and '|' in lines[j]:
                table_lines.add(j)
            j = i
            while j < len(lines) and lines[j].strip() and '|' in lines[j]:
                table_lines.add(j)
                j += 1
    blocks = []
    buf = _Buffer()
    in_code = False

    def flush():
        if buf.lines:
            blocks.append(Block(len(blocks) + 1, buf.kind, '\n'.join(buf.lines), buf.line))
        buf.lines = []

    def add(kind, line_no, content, level=0):
        flush()
        blocks.append(Block(len(blocks) + 1, kind, content, line_no, level))

    for no, raw in enumerate(lines, 1):
        if no <= skip_until:
            continue
        s = raw.rstrip()
        st = s.strip()
        if st.startswith('```') or st.startswith('~~~'):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not st or SKIP_LINE.match(st):
            flush()
            continue
        m = HEADING.match(st)
        if m:
            add('heading', no, st[m.end():].strip(), len(m.group(1)))
            continue
        if IMAGE.fullmatch(st):
            add('image', no, st)
            continue
        if (no - 1) not in table_lines and LIST_ITEM.match(s) and not TABLE_SEP.match(s):
            add('item', no, LIST_ITEM.sub('', s, count=1).strip())
            continue
        kind = ('quote' if st.startswith('>') else
                'table' if st.startswith('|') or (no - 1) in table_lines else 'para')
        content = st.lstrip('>').strip() if kind == 'quote' else st
        if not has_blank and kind == 'para':
            add('para', no, content)
            continue
        if buf.lines and buf.kind != kind:
            flush()
        if not buf.lines:
            buf.kind, buf.line = kind, no
        buf.lines.append(content)
    flush()
    if blocks and blocks[0].kind == 'para' and '\n' not in blocks[0].text and len(blocks) > 1:
        t = blocks[0].text
        if len(t) <= 120 and not t.endswith(('.', ':', ';', ',')):
            blocks[0].kind, blocks[0].level = 'heading', 1
    for b in blocks:
        b.meta_title = meta_title
    return blocks


# ---------------------------------------------------------------- matching

WB = '[a-z0-9]'


def compile_marker(m):
    """Marker → (regex, isolated)."""
    if m.startswith('r:'):
        return re.compile(m[2:]), False
    isolated = m.startswith('!')
    if isolated:
        m = m[1:]
    m = m.lower().translate(NORM_TABLE)
    parts = []
    for tok in m.split():
        if tok in ('—', '-'):
            parts.append(r'\s*[—-]\s*')
            continue
        esc = re.escape(tok).replace(r'\*', WB + '*').replace(r'\-', '[- ]?')
        parts.append(esc)
    body = r'\s+'.join(parts)
    if isolated:
        return re.compile(r'(^["\'(\[\s—]*|[,;(—:]\s*)(' + body + r')(?=\s*[,;:)—.!?]|\s*$)'), True
    return re.compile(r'(?<!' + WB + r')(?<!' + WB + r'-)' + body + r'(?!' + WB + r')(?!-' + WB + r')'), False


class Finder(object):
    def __init__(self, blocks):
        self.blocks = blocks
        self.findings = []
        self.claimed = {}

    def add(self, code, block, start, end, note='', claim=True, strength='strong'):
        if code not in TITLES:
            raise KeyError('code not in the entalk catalogue: %s' % code)
        for f in self.findings:
            if f['code'] == code and f['block'] == block.n and f.get('_span') and \
                    start < f['_span'][1] and end > f['_span'][0]:
                return
        if claim:
            key = (block.n,)
            for a, b in self.claimed.get(key, []):
                if start < b and end > a:
                    return
            self.claimed.setdefault(key, []).append((start, end))
        s = block.sent_of(start)
        sa, sb = block.sents[s - 1] if block.sents else (0, len(block.text))
        lo, hi = max(sa, start - 45), min(sb, end + 45)
        ctx = block.text[lo:start] + '[' + block.text[start:end] + ']' + block.text[end:hi]
        ctx = ('…' if lo > sa else '') + ctx.replace('\n', ' ').strip() + ('…' if hi < sb else '')
        self.findings.append(OrderedDict([
            ('code', code), ('title', TITLES[code]), ('block', block.n), ('sentence', s),
            ('line', block.line_of(start)), ('match', block.text[start:end].replace('\n', ' ')),
            ('context', ctx), ('note', note), ('strength', strength), ('_span', (start, end)),
        ]))

    def add_block(self, code, block, note, strength='strong'):
        if code not in TITLES:
            raise KeyError('code not in the entalk catalogue: %s' % code)
        self.findings.append(OrderedDict([
            ('code', code), ('title', TITLES[code]), ('block', block.n), ('sentence', None),
            ('line', block.line), ('match', ''), ('context', block.text[:90].replace('\n', ' ') +
                                                   ('…' if len(block.text) > 90 else '')),
            ('note', note), ('strength', strength),
        ]))

    def add_text(self, code, note):
        if code not in TITLES:
            raise KeyError('code not in the entalk catalogue: %s' % code)
        self.findings.append(OrderedDict([
            ('code', code), ('title', TITLES[code]), ('block', None), ('sentence', None),
            ('line', None), ('match', ''), ('context', 'whole text'), ('note', note), ('strength', 'strong'),
        ]))


def iter_sentences(block):
    for i, (a, b) in enumerate(block.sents, 1):
        yield i, a, b, block.norm[a:b]


_COMPILED = {}


def _rx(m):
    if m not in _COMPILED:
        _COMPILED[m] = compile_marker(m)
    return _COMPILED[m]


def scan_markers(fd, block, code, markers, claim=True, note='', skip=None):
    taken = fd.claimed.get((block.n,), []) if claim else []
    for _, a, b, sent in iter_sentences(block):
        if skip and skip(block.text[a:b]):
            continue
        hits = []
        for tier in ('strong', 'weak'):
            for m in markers.get(tier, []):
                rx, iso = _rx(m)
                for mt in rx.finditer(sent):
                    s, e = (mt.span(2) if iso else mt.span())
                    if e <= s or any(a + s < y and a + e > x for x, y in taken):
                        continue      # empty, or the place already belongs to a code with higher priority
                    if tier == 'weak' and s > 0 and block.text[a + s].isupper():
                        continue      # capitalized mid-sentence: part of a name ("the Open Door Initiative")
                    hits.append((a + s, a + e, tier))
        strong = [h for h in hits if h[2] == 'strong']
        weak = [h for h in hits if h[2] == 'weak']
        use = strong + (weak if len(hits) >= 2 and weak else [])
        for s, e, tier in sorted(use, key=lambda h: (h[0], -h[1])):
            fd.add(code, block, s, e, note=note, claim=claim, strength=tier)


# ---------------------------------------------------------------- grammar heuristics

def has_source(raw):
    return bool(SOURCE.search(raw.lower()))


def is_participle(w):
    if w in PASSIVE_EXCLUDE or w in NOT_PARTICIPLE:
        return False
    if w in IRREGULAR:
        return True
    return len(w) >= 4 and w.endswith('ed') and not w.startswith('un')


def word_is_verbish(w, plural=False):
    if not w:
        return False
    if w in AUX:
        return True
    if w.endswith('ed') and w not in NOT_PARTICIPLE and len(w) > 3:
        return True
    if plural:
        return w in PLURAL_VERBS or w in BASE_VERBS
    return w.endswith('s') and len(w) > 2 and not w.endswith(('ss', 'us', 'is')) and w not in NOUN_S


def referent_hit(sent, first_in_block):
    """Return a note when the sentence opens with a bare this/that/these/those/it/which + verb."""
    m = REF_START.match(sent)
    if not m:
        return None
    word, contr, w2, w3 = m.group(1), m.group(2), m.group(3) or '', m.group(4) or ''
    if word == 'which':
        return None if sent.rstrip().endswith('?') else 'sentence opens with "which": which thing?'
    if word == 'it':
        if not first_in_block:
            return None
        if contr or w2 in AUX or word_is_verbish(w2):
            return 'paragraph opens with "it": what does it refer to?'
        return None
    if word == 'that' and (w2 in ('is', 'said') and w3 == ','):
        return None
    if contr:
        return 'sentence opens with "%s%s": what does it refer to?' % (word, contr)
    plural = word in ('these', 'those')
    if w2 in AUX:
        return 'sentence opens with bare "%s %s"' % (word, w2)
    if w2.endswith('ed') and w2 not in NOT_PARTICIPLE and (w3 in FUNC_AFTER or w3 in ',.;:!?' and w3):
        return 'sentence opens with bare "%s %s"' % (word, w2)
    if plural:
        if w2 in PLURAL_VERBS:
            return 'sentence opens with bare "%s %s"' % (word, w2)
        return None
    if word_is_verbish(w2) and not w2.endswith('ed'):
        return 'sentence opens with bare "%s %s"' % (word, w2)
    return None


def glued_hits(sent, raw):
    """Comma-splice candidates: (start, end, note) within the sentence."""
    out = []
    for mt in GLUE_ADV.finditer(sent):
        if len(WORD.findall(sent[:mt.start()])) >= 3:
            out.append((0, mt.end(), 'comma before "%s": two sentences?' % mt.group(0).strip(', ').split()[0]))
    for rx in (GLUE_PRON, GLUE_POSS):
        for mt in rx.finditer(sent):
            cut = max(sent.rfind(c, 0, mt.start()) for c in ';:—')
            first = sent[cut + 1:mt.start()]
            raw_part = raw[cut + 1:mt.start()]
            words = WORD.findall(first)
            if len(words) < 4 or SUBORD_ANY.search(sent[:mt.start()]) or GLUE_INTRO_END.search(first) or \
                    not GLUE_FINITE.search(first) or raw_part.count('"') % 2 or \
                    raw_part.count('“') > raw_part.count('”'):
                continue
            w0 = words[0].lower()
            raw_first = WORD.findall(raw_part)
            capitalized = raw_first and raw_first[0][:1].isupper()
            if w0 not in GLUE_START and not (capitalized and w0 not in NON_SUBJECT_OPENERS and
                                             not w0.endswith(('ly', 'ing', 'ed'))):
                continue
            if rx is GLUE_PRON:
                subj, contr, verb = mt.group(1), mt.group(2), mt.group(3) or ''
                after = sent[mt.end():mt.end() + 2].strip()
                if verb in SPEECH or (not contr and after[:1] in (',', '.', '') and verb in AUX | BASE_VERBS):
                    continue
                if contr:
                    ok = True
                elif subj in ('i', 'we', 'you', 'they'):
                    ok = verb in AUX or verb in BASE_VERBS or (verb.endswith('ed') and verb not in NOT_PARTICIPLE)
                elif subj in ('these', 'those'):
                    ok = word_is_verbish(verb, plural=True)
                else:
                    ok = word_is_verbish(verb)
                if not ok:
                    continue
            out.append((0, mt.end(), 'comma joins two sentences?'))
            break
    return out[:1]


def _noun_like(low):
    last = low.split('-')[-1]
    return not (
        low in NS_STOP or last in NS_STOP or last in ADJ_COMMON or
        last.endswith(('ical', 'ular')) or (last.endswith('ial') and last not in NOUN_IAL) or
        (last.endswith('al') and len(last) > 5 and last not in NOUN_AL) or
        (last.endswith('ish') and len(last) > 5 and last not in NOUN_ISH) or
        (last.endswith('ly') and last not in NOUN_LY) or
        (last.endswith('ed') and last not in NOUN_ED) or
        (last.endswith('ing') and last not in NOUN_ING) or
        last.endswith(('ous', 'ful', 'less')) or
        (last.endswith('ive') and last not in NOUN_IVE) or
        (last.endswith(('able', 'ible')) and last not in NOUN_ABLE) or
        (last.endswith('est') and len(last) > 5 and last not in NOUN_EST) or
        last in COMPARATIVES or len(last) < 2)


def noun_stacks(block, a, b):
    """Runs of 4+ noun-like words (PLAIN "Avoid noun strings"): list of (start, end, count).

    No tagger: a word is noun-like unless it is a function word, a common verb or adjective, or has an
    adverb/adjective/participle ending. A plural inside a run is read as a verb ("regulation governs
    disaster assistance") unless it is a usual plural modifier ("animal rights protection"); a word
    right after a pronoun, modal or "to" is read as a verb ("they handle building materials").
    """
    out, runs, run = [], [], []
    prev = ''
    first = True
    for mt in TOKEN.finditer(block.text, a, b):
        tok = mt.group(0)
        start, end = mt.span()
        noun = False
        low = ''
        if tok[0].isalpha() and block.norm[start] != ' ':
            low = tok.lower().replace('’', "'")
            if "'" in low or prev in VERB_TRIGGER:
                noun = False
            elif first and low in IMPERATIVES:
                noun = False                       # "Write plain language links"
            elif run and low in VERB_AFTER_PLURAL and (run[-1][2] == 'people' or (
                    run[-1][2].endswith('s') and not run[-1][2].endswith(('ss', 'us', 'is')))):
                noun = False                       # "people read government websites"
            elif tok[0].isupper() and not first and not tok.isupper():
                noun = False                       # a name: "the Red Cross", "Open Door Forums"
            elif tok in ACRONYMS:
                noun = True
            else:
                noun = _noun_like(low)
            prev = low
            first = False
        else:
            prev = ''
        if noun:
            run.append((start, end, low))
        else:
            runs.append(run)
            run = []
    runs.append(run)
    for r in runs:
        # split at an inner plural that is more likely a verb than a modifier
        piece = []
        for k, (s, e, w) in enumerate(r):
            inner = k < len(r) - 1
            if inner and piece and w.endswith('s') and not w.endswith(('ss', 'us', 'is')) and \
                    w not in PLURAL_MODIFIERS:
                if len(piece) >= 4:
                    out.append((piece[0][0], piece[-1][1], len(piece)))
                piece = []
                continue
            piece.append((s, e, w))
        if len(piece) >= 4:
            out.append((piece[0][0], piece[-1][1], len(piece)))
    return out


# ---------------------------------------------------------------- the scan

# Claim order. W-NOMINAL comes before the single-word codes so that "the implementation of" is a hidden
# verb, not jargon; W-VAGUE-NUM comes before W-VAGUE so that "approximately 12%" is one span.
WORD_CODES = ['T-HIDE', 'T-BS', 'T-PERSONAL', 'T-TERMS', 'W-PROP', 'W-LLM', 'W-CORP', 'W-CLICHE', 'W-BUREAU',
              'W-NOMINAL', 'W-INTRO', 'W-INTENS', 'W-EVAL', 'W-ZAUM', 'W-VAGUE-NUM', 'W-VAGUE']


def scan(text):
    blocks = parse_blocks(text)
    fd = Finder(blocks)
    body = [b for b in blocks if b.kind in ('para', 'item', 'quote')]
    paras = [b for b in blocks if b.kind == 'para']
    headings = [b for b in blocks if b.kind == 'heading']

    # --- dictionary codes (one place, one code, in priority order)
    for b in blocks:
        if b.kind == 'image':
            continue
        for mt in NOT_X_Y.finditer(b.norm):
            fd.add('W-LLM', b, mt.start(), mt.end(), note='"it\'s not X — it\'s Y"')
        for code in WORD_CODES:
            scan_markers(fd, b, 'W-VAGUE' if code == 'W-VAGUE-NUM' else code, DICT[code],
                         skip=has_source if code == 'T-BS' else None)
            if code != 'W-NOMINAL':
                continue
            for i, a, e, sent in iter_sentences(b):
                for mt in NOM_LIGHT.finditer(sent):
                    noun = mt.group(2)
                    if noun not in NOM_STRONG_EXCLUDE and noun[:-1] not in NOM_STRONG_EXCLUDE:
                        fd.add('W-NOMINAL', b, a + mt.start(), a + mt.end(),
                               note='verb hidden in "%s"' % mt.group(2))
                for mt in NOM_THE_OF.finditer(sent):
                    if mt.group(1) not in THE_OF_EXCLUDE and mt.group(1)[:-1] not in THE_OF_EXCLUDE:
                        fd.add('W-NOMINAL', b, a + mt.start(), a + mt.end(),
                               note='verb hidden in "%s of"' % mt.group(1))
        scan_markers(fd, b, 'P-INACTION', STATE_VERBS, claim=False)

    # --- reflexive triads of abstract words (W-LLM, weak)
    for b in body:
        for i, a, e, sent in iter_sentences(b):
            for mt in TRIAD.finditer(sent):
                if re.search(r'(?:such as|including|like|e\.g\.|for example)\s*$', sent[:mt.start()]):
                    continue
                items = [x.split()[-1] for x in mt.groups()]
                nxt = re.match(r'\s*([a-z]+)', sent[mt.end():])
                if nxt and nxt.group(1) not in NS_STOP:
                    continue      # "visual, cognitive or mobility impairments": modifiers, not a triad
                if any(x in NS_STOP or len(x) < 4 for x in items) or \
                        any(w[:1].isupper() for w in WORD.findall(b.text[a + mt.start():a + mt.end()])):
                    continue
                if sum(1 for x in items if TRIAD_ABSTRACT.search(x) and len(x) > 4) >= 2 and len(set(items)) == 3:
                    fd.add('W-LLM', b, a + mt.start(), a + mt.end(), note='triad of abstract words?',
                           claim=False, strength='weak')

    # --- density of hollow words: 3+ evaluation and cliché markers in one block
    hollow_codes = ('W-EVAL', 'W-INTENS', 'W-CORP', 'W-CLICHE', 'W-LLM')
    for b in body:
        n = sum(1 for f in fd.findings if f['block'] == b.n and f['code'] in hollow_codes)
        if n >= 3:
            fd.add_block('M-HOLLOW', b, '%d evaluation, buzzword and cliché markers in the block: '
                                        'are there facts behind them?' % n)

    # --- politeness: 2+ formulas in one block
    pol = [_rx(m)[0] for m in POLITE]
    for b in body:
        hits = sorted(set(mt.span() for rx in pol for mt in rx.finditer(b.norm)))
        if len(hits) >= 2:
            for s, e in hits:
                fd.add('W-POLITE', b, s, e, note='%d politeness formulas in the block' % len(hits), claim=False)

    # --- grammar: passive, empty openers, unclear referents, noun strings, nominal density
    for b in body:
        for i, a, e, sent in iter_sentences(b):
            for mt in PASSIVE.finditer(sent):
                if is_participle(mt.group(1)):
                    fd.add('W-PASSIVE', b, a + mt.start(), a + mt.end(), claim=False)
            expletive_at = None
            for mt in THERE_BE.finditer(sent):
                rest = ' '.join(sent[mt.end():].split()[:12])
                if re.search(B + r'(?:that|who|which|whom)' + E, rest):
                    fd.add('P-EXPLETIVE', b, a + mt.start(), a + mt.end(), note='"there is/are … that/who"',
                           claim=False)
                else:
                    fd.add('P-EXPLETIVE', b, a + mt.start(), a + mt.end(), note='bare "there is/are"',
                           claim=False, strength='weak')
                expletive_at = mt.start() if expletive_at is None else min(expletive_at, mt.start())
            for rx, note in ((IT_ADJ, '"it is … to/that"'), (IT_NOUN, '"it is a … that/to"'),
                             (STRUNK_WHO, '"he is a man who" (Strunk 13)')):
                for mt in rx.finditer(sent):
                    if rx is IT_ADJ and mt.group(1) in IT_ADJ_EXCLUDE:
                        continue
                    fd.add('P-EXPLETIVE', b, a + mt.start(), a + mt.end(), note=note, claim=False)
                    expletive_at = mt.start() if expletive_at is None else min(expletive_at, mt.start())
            note = referent_hit(sent, i == 1)
            if note and not (expletive_at is not None and expletive_at <= 6):
                head = re.match(r'^[\W_]*\w+(?:\'\w+)?(?:\s+[\w\'-]+)?', sent)
                fd.add('P-REFERENT', b, a, a + (head.end() if head else 4), note=note, claim=False,
                       strength='weak')
            for s, t, n in noun_stacks(b, a, e):
                fd.add('W-NOUNSTACK', b, s, t, note='%d nouns in a row?' % n, claim=False,
                       strength='strong' if n >= 5 else 'weak')
            noms = [w for w in NOMINAL_DENSE.findall(sent) if w not in NOM_EXCLUDE]
            if len(noms) >= 4:
                fd.add('W-NOMINAL', b, a, e, note='%d -tion/-sion/-ment words in one sentence' % len(noms),
                       claim=False, strength='weak')

    # --- sentences: length, nesting, splices, inline lists, fragments
    for b in body:
        short_run = []
        for i, a, e, sent in iter_sentences(b):
            raw = b.text[a:e]
            words = WORD.findall(raw)
            commas = raw.count(',')
            subs = len(SUBORD.findall(sent))
            if len(words) > 25 or commas >= 4:
                fd.add('SIGNAL-LONG', b, a, e, note='%d words, %d commas' % (len(words), commas), claim=False)
            if subs >= 3:
                fd.add('P-NESTED', b, a, e, note='%d subordinate clauses' % subs, claim=False)
            for s, t, note in glued_hits(sent, raw):
                fd.add('P-GLUED', b, a + s, a + t, note=note, claim=False)
            semis = raw.count(';')
            mark = INLINE_LIST_MARK.search(sent)
            if semis >= 2:
                fd.add('P-INLINELIST', b, a, e, note='%d semicolons' % semis, claim=False)
            elif mark and commas >= 3:
                fd.add('P-INLINELIST', b, a + mark.start(), a + mark.end(), note='%d commas' % commas, claim=False)
            else:
                ser = SERIAL_LIST.search(sent)
                if ser and commas >= 3:
                    fd.add('P-INLINELIST', b, a + ser.start(), a + ser.end(), note='a list of 4+ items in a sentence',
                           claim=False)
            question = raw.rstrip().endswith(('?', ':'))
            if re.match(r'^["\'(\[\s—]*which' + E, sent) and not question:
                fd.add('P-PARCEL', b, a, e, note='sentence opens with "which"', claim=False)
            elif FRAGMENT_START.match(sent) and len(words) <= 12 and not question:
                fd.add('P-PARCEL', b, a, e, note='sentence opens like a fragment', claim=False)
            elif SUBCLAUSE_START.match(sent) and ',' not in raw and len(words) <= 8 and not question:
                fd.add('P-PARCEL', b, a, e, note='subordinate clause without a main clause?', claim=False)
            if len(words) <= 3:
                short_run.append((a, e))
            else:
                if len(short_run) >= 3:
                    fd.add('P-PARCEL', b, short_run[0][0], short_run[0][1],
                           note='%d very short sentences in a row' % len(short_run), claim=False)
                short_run = []
        if len(short_run) >= 3:
            fd.add('P-PARCEL', b, short_run[0][0], short_run[0][1],
                   note='%d very short sentences in a row' % len(short_run), claim=False)

    # --- numbers: fake precision, useless facts, specs, unrounded numbers
    for b in body:
        for i, a, e, sent in iter_sentences(b):
            raw_low = b.text[a:e].lower()
            for rx in FAKENUM:
                for mt in rx.finditer(sent):
                    if not SOURCE.search(raw_low):
                        fd.add('T-NUMBERS', b, a + mt.start(), a + mt.end(), note='no source in the sentence',
                               claim=False)
            for m in NOUSE:
                for mt in _rx(m)[0].finditer(sent):
                    fd.add('M-FACTS', b, a + mt.start(), a + mt.end(), note='a fact about the company: does the '
                                                                            'reader need it?', claim=False)
            units = list(UNITS.finditer(sent))
            if units:
                fd.add('M-FACTS', b, a + units[0].start(), a + units[-1].end(),
                       note='specs in units: translated into what the reader gets?', claim=False)
            for mt in UNROUNDED.finditer(sent):
                if not mt.group(0).endswith(',000'):
                    fd.add('W-VAGUE', b, a + mt.start(), a + mt.end(),
                           note='unrounded number: does the reader need every digit?', claim=False)

    # --- headings
    for h in headings:
        raw = h.text
        caps = [w for w in re.findall(r'\b[A-Z]{3,}\b', raw)
                if w not in ACRONYMS and (len(w) >= 5 or w in CAPS_HYPE)]
        if caps:
            fd.add_block('S-CLICKBAIT', h, 'words in capitals: ' + ', '.join(caps))
        if re.search(r'[!?]\s*[!?]|!\s*$|(?:\.\.\.|…)\s*$', raw):
            fd.add_block('S-CLICKBAIT', h, 'exclamation or ellipsis in the title')
        for m in CLICKBAIT:
            mt = _rx(m)[0].search(h.norm)
            if mt:
                fd.add('S-CLICKBAIT', h, mt.start(), mt.end(), claim=False)
        if re.search(r'["“][^"”]*(?:\.\.\.|…)[^"”]*["”]', raw) or \
                re.search(r':\s*["“][^"”\s]+(?:\s+[^"”\s]+){0,2}["”]\s*$', raw):
            fd.add_block('T-TITLE', h, 'clipped quote in the title: is the meaning kept?')
        if re.search(r'\b[A-Z]{4,}!', raw):
            fd.add_block('T-TITLE', h, 'verb in capitals with an exclamation mark')
    title = headings[0] if headings and headings[0].n == 1 else None
    # a short fragment, letter or post needs no title (catalogue, S-TITLE "Not an error if")
    if body and not title and not blocks[0].meta_title and sum(len(b.text) for b in body) >= 1000:
        fd.add_text('S-TITLE', 'the text has %d characters and no title (the first block is not a heading)'
                    % sum(len(b.text) for b in body))

    # --- introduction and conclusion
    content = [b for b in blocks if b.kind in ('para', 'quote', 'item')]
    if content:
        first = content[0]
        for m in INTRO_OPENERS:
            for mt in _rx(m)[0].finditer(first.norm):
                fd.add('S-INTRO', first, mt.start(), mt.end(), note='formula in the first paragraph', claim=False)
        for last in content[-2:]:
            for m in OUTRO_CLOSERS:
                rx, iso = _rx(m)
                for mt in rx.finditer(last.norm):
                    s, t = mt.span(2) if iso else mt.span()
                    fd.add('S-OUTRO', last, s, t, note='formula at the end of the text', claim=False)

    # --- paragraphs, subheadings, lists
    total = sum(len(b.text) for b in body)
    for b in paras + [x for x in blocks if x.kind == 'quote']:
        nw = len(WORD.findall(b.text))
        if (len(b.sents) > 5 and nw >= 80) or nw > 150:
            fd.add_block('S-WALL', b, '%d sentences, %d words (GOV.UK: up to 5 sentences; PLAIN: up to 150 words, '
                                      'never over 250)' % (len(b.sents), nw))
    if total >= 1500 and len(paras) <= 2:
        fd.add_text('S-WALL', 'a text of %d characters with almost no paragraph breaks (%d paragraphs)'
                    % (total, len(paras)))
    subheads = [h for h in headings if not (title and h.n == title.n)]
    if total >= 2000 and len(paras) >= 6 and not subheads:
        fd.add_text('S-SUBHEADS', 'a text of %d characters, %d paragraphs and no subheadings' % (total, len(paras)))
    if subheads:
        marks = [h.n for h in subheads] + [len(blocks) + 1]
        prev = subheads[0].n
        sections = []
        for nxt in marks[1:]:
            sections.append((prev, sum(1 for b in paras if prev < b.n < nxt)))
            prev = nxt
        before = sum(1 for b in paras if b.n < subheads[0].n)
        for start, cnt in sections:
            if cnt > 10:
                fd.add_block('S-SUBHEADS', blocks[start - 1], '%d paragraphs under one subheading '
                                                              '(about one subheading per 5–10)' % cnt)
        if before > 10:
            fd.add_text('S-SUBHEADS', '%d paragraphs before the first subheading' % before)
        # an outline (headings with little text under most of them) is not overload
        filled = sum(1 for _, cnt in sections if cnt)
        if len(subheads) >= 3 and filled * 2 >= len(sections) and len(paras) / float(len(subheads)) < 2:
            fd.add_text('S-SUBHEADS', '%d subheadings for %d paragraphs: too many subheadings?'
                        % (len(subheads), len(paras)))

    runs, cur = [], []
    for b in blocks:
        if b.kind == 'item':
            cur.append(b)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    for run in runs:
        if len(run) > 7:
            fd.add_block('S-LIST', run[0], '%d items in the list' % len(run))
        for it in run:
            if len(it.text) > 300 or len(it.sents) > 2:
                fd.add_block('S-LIST', it, 'long item: %d characters, %d sentences' % (len(it.text), len(it.sents)))
            mt = LIST_START_WEAK.search(it.norm.strip())
            if mt:
                fd.add_block('S-LIST', it, 'item opens with "%s": connected text cut into items?' % mt.group(0))

    # --- buried conditions
    for b in paras:
        if len(b.text) >= 500:
            cut = int(len(b.text) * 0.6)
            for mt in RESTRICT.finditer(b.norm):
                if mt.start() >= cut:
                    fd.add('S-BURIED', b, mt.start(), mt.end(), note='condition at the end of a long paragraph',
                           claim=False)

    # --- examples
    if total >= 2000 and not any(EXAMPLE_MARKERS.search(b.norm) for b in body):
        fd.add_text('M-NOEXAMPLE', 'a text of %d characters without a single example marker '
                                   '("for example", "for instance", "imagine", "suppose"…)' % total)

    # --- illustrations
    has_visual = set(b.n for b in blocks if b.kind in ('image', 'table'))
    for b in blocks:
        for mt in IMAGE.finditer(b.text):
            alt, src = mt.group(1).lower(), mt.group(2).lower()
            if STOCK_WORDS.search(alt):
                fd.add('V-DECOR', b, mt.start(), mt.end(), note='alt text looks like a generic stock image: %s' % alt,
                       claim=False)
            if STOCK_SRC.search(src):
                fd.add('V-RIGHTS', b, mt.start(), mt.end(), note='source looks like a photo bank or a search engine',
                       claim=False)
            if not alt.strip():
                fd.add('V-DECOR', b, mt.start(), mt.end(), note='image without a description: check what it shows',
                       claim=False)
    for b in paras:
        seq = len(SEQUENCE.findall(b.norm))
        ifs = len(re.findall(B + r'if' + E, b.norm))
        near = any(abs(b.n - n) <= 2 for n in has_visual)
        if (seq >= 4 or ifs >= 3) and not near:
            fd.add_block('V-NOSCHEME', b, '%d sequence words, %d "if"s; no diagram or table nearby' % (seq, ifs))

    return blocks, fd.findings


# ---------------------------------------------------------------- output

class Stats(object):
    def __init__(self, blocks):
        body = [b for b in blocks if b.kind in ('para', 'item', 'quote')]
        sents = [(b, i) for b in body for i in range(len(b.sents))]
        lens = [len(WORD.findall(b.text[b.sents[i][0]:b.sents[i][1]])) for b, i in sents]
        self.chars = sum(len(b.text) for b in body)
        self.words = sum(len(WORD.findall(b.text)) for b in body)
        self.blocks = len(blocks)
        self.kinds = OrderedDict()
        for b in blocks:
            self.kinds[b.kind] = self.kinds.get(b.kind, 0) + 1
        self.sentences = len(sents)
        self.avg = round(sum(lens) / float(len(lens)), 1) if lens else 0.0
        self.longest_loc, self.longest_len = '', 0
        if lens:
            k = max(range(len(lens)), key=lambda j: lens[j])
            self.longest_loc = '¶%d.%d' % (sents[k][0].n, sents[k][1] + 1)
            self.longest_len = lens[k]

    def as_dict(self):
        return OrderedDict([
            ('chars', self.chars), ('words', self.words), ('blocks', self.blocks), ('kinds', self.kinds),
            ('sentences', self.sentences), ('avg_sentence_words', self.avg),
            ('longest', [self.longest_loc, self.longest_len]),
        ])


KIND_EN = {'heading': 'heading', 'para': 'paragraph', 'item': 'item', 'quote': 'quote', 'table': 'table',
           'image': 'image'}


def loc(f):
    if f['block'] is None:
        return 'whole text'
    s = '¶%d' % f['block'] + ('.%d' % f['sentence'] if f['sentence'] else '')
    return s + (' (line %d)' % f['line'] if f['line'] else '')


def render(blocks, findings, limit):
    st = Stats(blocks)
    out = ['MECHANICAL PRE-PASS — candidates, not verdicts.',
           'Check every hit against its meaning and the "Not an error if" section in error-patterns.md.', '']
    kinds = ', '.join('%s: %d' % (KIND_EN.get(k, k), v) for k, v in st.kinds.items())
    out.append('Text: %d characters, %d words, %d blocks (%s), %d sentences.' % (
        st.chars, st.words, st.blocks, kinds, st.sentences))
    if st.longest_len:
        out.append('Average sentence: %s words; longest: %s — %d words.' % (
            st.avg, st.longest_loc, st.longest_len))
    out += ['', '== Block map ==']
    for b in blocks:
        head = ('%s %d' % (KIND_EN[b.kind], b.level)) if b.kind == 'heading' else KIND_EN.get(b.kind, b.kind)
        info = '' if b.kind in ('heading', 'image', 'table') else ', %d sent., %d chars' % (len(b.sents), len(b.text))
        preview = b.text.replace('\n', ' ')
        out.append('¶%-3d [%s%s] %s%s' % (b.n, head, info, preview[:70], '…' if len(preview) > 70 else ''))
    out += ['', '== Candidates by code ==']
    by_code = OrderedDict()
    for f in findings:
        by_code.setdefault(f['code'], []).append(f)
    order = list(TITLES.keys())
    for code in sorted(by_code, key=lambda c: order.index(c) if c in order else 999):
        items = sorted(by_code[code], key=lambda f: ((f['block'] or 0), (f['sentence'] or 0)))
        out.append('')
        out.append('%s · %s — %d' % (code, TITLES.get(code, code), len(items)))
        for f in items[:limit] if limit else items:
            note = ('  — ' + f['note']) if f['note'] else ''
            weak = ' (weak)' if f['strength'] == 'weak' else ''
            text = f['context'] if f['context'] else ''
            out.append('  %s: %s%s%s' % (loc(f), text, note, weak))
        if limit and len(items) > limit:
            out.append('  … %d more (run with --all)' % (len(items) - limit))
    if not findings:
        out.append('No mechanical candidates found. That does not mean there are no errors.')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description='Mechanical pre-pass for the text reviewer')
    ap.add_argument('path', help='text file, or "-" for stdin')
    ap.add_argument('--json', action='store_true', help='print JSON')
    ap.add_argument('--all', action='store_true', help='do not limit the number of lines per code')
    args = ap.parse_args()
    text = sys.stdin.read() if args.path == '-' else open(args.path, encoding='utf-8').read()
    blocks, findings = scan(text)
    if args.json:
        data = OrderedDict([
            ('stats', Stats(blocks).as_dict()),
            ('blocks', [OrderedDict([('n', b.n), ('kind', b.kind), ('line', b.line), ('sentences', len(b.sents)),
                                     ('chars', len(b.text)), ('preview', b.text[:80])]) for b in blocks]),
            ('findings', [OrderedDict((k, v) for k, v in f.items() if not k.startswith('_')) for f in findings]),
        ])
        print(json.dumps(data, ensure_ascii=False, indent=1))
    else:
        print(render(blocks, findings, None if args.all else 25))


if __name__ == '__main__':
    main()
