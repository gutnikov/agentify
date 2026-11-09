# Error catalogue

A catalogue for an agent reviewer of English texts: what errors to look for, how to recognise them, and when a pattern is not an error. It is built on the open sources kept in [`sources/`](sources/README.md), not on Ilyakhov's books that rutalk uses:

- **PLAIN** — the US Federal Plain Language Guidelines and the plainlanguage.gov before-and-after examples, [`sources/plain/`](sources/README.md)
- **GOV.UK** — "Writing to GOV.UK standards": the writing guidelines, the A to Z style guide and the technical A to Z, [`sources/govuk/`](sources/README.md)
- **Strunk** — William Strunk Jr., *The Elements of Style* (1918/1920): section III, Elementary Principles of Composition (rules 8–18, numbered as in the source file), and section V, Words and Expressions Commonly Misused, [`sources/strunk/`](sources/README.md)

Copyrighted books — Orwell, Williams, Pinker, Minto, Zinsser, Fowler — are cited by name and chapter only, never quoted. The catalogue describes errors, not fixes: how to fix an error is told by the source its entry links to.

**Status.** entalk carries this catalogue over from rutalk: the codes, base severities, exceptions and search marking are rutalk's, re-grounded in the English sources and rewritten with English-language phenomena. **Nothing here is measured yet.** rutalk's results belong to rutalk and to Russian; entalk's catalogue waits for its own measurement in `lab/`. Codes marked **(new)** are entalk's additions: they are not in rutalk and have no measurement behind them at all. Two rutalk codes are dropped: W-PARTIC (Russian participial and gerund constructions) and P-SPLITCONJ (split paired conjunction, weak in English).

## How to read an entry

- **Code** (`W-EVAL`) is what the reviewer writes in the report. The first letter is the level: **M** — purpose and meaning, **T** — truth and trust, **S** — structure and delivery, **P** — sentence, **W** — words, **V** — illustrations. **(new)** marks a code entalk added.
- The title line gives the error's name, its **severity**, its **search** method and its **sources**: links into `sources/`, and sometimes a **classic** — a book cited by name and chapter, not copied.
- **Rule** — the norm the error breaks.
- **What goes wrong** — what is wrong and how it harms the reader.
- **Signs** — how to recognise the error in a text.
- **Not an error if** — exceptions. They filter out false positives.
- **Example** — quoted verbatim from a source file, with a link to it. Where the sources give no sample of faulty text and only describe the error, the field is called **How the sources describe it** and paraphrases or quotes that description. No example in this catalogue is invented.
- **Severity** — the base score; in brackets, when it goes higher or lower.
- **Search**: "script" — `text_scan.py` finds candidates and the reviewer checks them; "reading" — the error shows only on careful reading.
- Numeric thresholds (words per sentence, sentences per paragraph) point at candidates to look at, never at verdicts (G4). Where a threshold is rutalk's, converted from characters to words, the entry says so.

## Severity scale

| Score | Name | Meaning |
|---|---|---|
| 1 | critical | The text misleads the reader or fails its purpose |
| 2 | serious | The key point does not get through or gets lost: the reader will give up, will not understand, or will understand it wrong |
| 3 | noticeable | Gets in the way locally or undermines trust, but the meaning gets through overall |
| 4 | polish | A small thing worth fixing once everything else is done |

## General rules

- **G1. A rule is a tool, not a law.** If a "fix" by the rule would make the text more mechanical or less natural, or would throw out something that matters, it is not an error. Strunk limits his own rules: omitting needless words "requires not that the writer make all his sentences short, or that he avoid all detail and treat his subjects only in outline, but that he make every word tell" ([Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md)); the active-voice rule "does not, of course, mean that the writer should entirely discard the passive voice, which is frequently convenient and sometimes necessary" ([Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md)). PLAIN says the same of contractions: "Don't use them wherever possible, but wherever they sound natural" ([PLAIN "Use contractions"](sources/plain/guidelines/conversational/use-contractions.md)). Orwell ends his six rules with the same point (Orwell, "Politics and the English Language", rule 6: break the rules rather than write something barbarous).
- **G2. The reader and the genre decide.** Terms are fine in a text for specialists: "Where you need to use specialist terms, you can. They’re not always jargon" ([GOV.UK "Use clear language"](sources/govuk/clear-language.md)); "Don't write for an 8th-grade class if your audience is composed of PhD candidates" ([PLAIN "Write for your audience"](sources/plain/guidelines/audience/index.md)). In law and regulation the wording may be fixed: PLAIN accepts the passive "when the law is the actor" ([PLAIN "Use active voice"](sources/plain/guidelines/conversational/use-active-voice.md)), and GOV.UK answers legal jargon with "a plain English summary", not a rewrite ([GOV.UK A to Z "Legal content"](sources/govuk/a-to-z-style-guide.md)). Narrative lives by its own rules: "The brief paragraphs of animated narrative, however, are often without even this semblance of a topic sentence" ([Strunk 9](sources/strunk/3-principles-of-composition.md)). Where the sources disagree because their genres differ — PLAIN recommends question headings for regulations, GOV.UK bans them on web pages — the reviewer applies the one that fits the text in front of it.
- **G3. Simplification and a chosen angle are not errors in themselves.** No text says everything: "It is not that every detail is given; that would be impossible, as well as to no purpose; but that all the significant details are given" ([Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md)). The sources ask for exactly this selection: "Publish only what’s needed to meet that user need and nothing more" ([GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md)); for most readers "it's not necessary to understand all possibilities and conditions, only those that apply to the reader's situation" ([PLAIN "Use tables to make complex material easier to understand"](sources/plain/guidelines/design/use-tables-to-make-complex-material-easier-to-understand.md)). Simplification becomes an error only through the specific distortions described in the T codes.
- **G4. No quotas.** The share of passive verbs, the number of adjectives or the average sentence length is not a criterion by itself. "There’s no maximum or minimum overall page length. It’s most important that you write well" ([GOV.UK "Use clear language"](sources/govuk/clear-language.md)); "There is nothing wrong with an occasional one-sentence paragraph", and paragraphs all of one size make writing "choppy" ([PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md)); "There is no absolute rule about where to put exceptions and conditions" ([PLAIN "Place the main idea before exceptions and conditions"](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md)). The numbers in this catalogue (25 words, 5 sentences, 150 words) mark candidates: GOV.UK itself says "Check sentences with more than 25 words to see if you can split them to make them clearer" ([GOV.UK A to Z "Sentence length"](sources/govuk/a-to-z-style-guide.md)).
- **G5. Someone else's text is not judged as the author's.** Quotations, direct speech, examples of errors under discussion and legally agreed wording are judged only by how they are built into the text. GOV.UK exempts tribunal decisions from its rule on offensive words "because decisions include quotes from people involved in a case" ([GOV.UK "Use the right tone"](sources/govuk/right-tone.md)), and keeps double quotes "for direct quotations of something that a person has said or written" ([GOV.UK A to Z "Quotes and speech marks"](sources/govuk/a-to-z-style-guide.md)).

## Summary table

| Code | Error | Severity |
|---|---|---|
| **M** | **Purpose and meaning** | |
| [M-READER](#m-reader) | The text serves the author, not the reader | 1 |
| [M-GOAL](#m-goal) | No useful goal | 1 |
| [M-DIGRESS](#m-digress) | Digression from the goal | 3 (2) |
| [M-HOLLOW](#m-hollow) | Hollow text: words without information | 2 (1) |
| [M-ABSTRACT](#m-abstract) | Abstraction without a picture | 2 (3) |
| [M-NOEXAMPLE](#m-noexample) | Idea without an example | 2 (1, 3) |
| [M-EXAMPLE](#m-example) | Example does not support the idea | 3 (2) |
| [M-ORDER](#m-order) | Broken order of explanation | 2 (3) |
| [M-LEVEL](#m-level) | Wrong level for the reader: terms and detail | 2 (3) |
| [M-IDEAL](#m-ideal) | Advice for the ideal case only | 2 (1) |
| [M-OFFEND](#m-offend) | A jab at the reader | 2 (3) |
| [M-FACTS](#m-facts) | Facts that do not serve the reader | 3 (2) |
| [M-ROBOT](#m-robot) | Mechanical editing | 3 (2) |
| **T** | **Truth and trust** | |
| [T-BS](#t-bs) | Generalization or promise without facts | 2 (1) |
| [T-NUMBERS](#t-numbers) | Misleading numbers | 1 (3) |
| [T-HIDE](#t-hide) | Bad news hidden | 1 (4) |
| [T-TITLE](#t-title) | Title claims more than the facts | 1 |
| [T-METAPHOR](#t-metaphor) | Misleading analogy | 1 |
| [T-RATING](#t-rating) | Rating with rigged criteria | 1 |
| [T-TERMS](#t-terms) | Clever word in the wrong sense | 2 (1, 3) |
| [T-PERSONAL](#t-personal) | Judging the person, not the action | 2 |
| **S** | **Structure and delivery** | |
| [S-TITLE](#s-title) | Title does not say what the text is about | 2 (3) |
| [S-CLICKBAIT](#s-clickbait) | Clickbait title | 3 (2) |
| [S-SCAN](#s-scan) | The main point is invisible when skimming | 2 (3) |
| [S-SUBHEADS](#s-subheads) | Subheadings do not help the reader find their way | 2–4 |
| [S-MODULES](#s-modules) | Parts do not add up to a system | 2 (3, 4) |
| [S-INTRO](#s-intro) | Empty introduction | 3 (4) |
| [S-OUTRO](#s-outro) | Useless conclusion | 3 (4) |
| [S-WALL](#s-wall) | Wall of text | 2 (3) |
| [S-PARA-LEAD](#s-para-lead) | Paragraph does not lead with the point | 3 (2, 4) |
| [S-PARA-MIX](#s-para-mix) | Paragraph without a single topic | 3 (2) |
| [S-LIST](#s-list) | List in the wrong place | 3 (2, 4) |
| [S-BURIED](#s-buried) | Important information buried | 2 (1) |
| [S-EXAMPLES](#s-examples) | Examples not set apart, or crowding out the text | 3 (2) |
| **P** | **Sentence** | |
| [P-OVERLOAD](#p-overload) | Too many new ideas in one sentence | 2 (3) |
| [P-SPLIT](#p-split) | Main clause broken up by details | 2 |
| [P-INLINELIST](#p-inlinelist) | List crammed into a sentence | 2 (1) |
| [P-NESTED](#p-nested) | Clause inside a clause | 3 (2, 4) |
| [P-GLUED](#p-glued) | Run-on sentence or comma splice | 3 (4) |
| [P-INACTION](#p-inaction) | No action: abstract subject, state verb | 3 (2) |
| [P-FOCUS](#p-focus) | Wrong character in focus | 3 |
| [P-CLUMSY](#p-clumsy) | Sentence that trips the reader | 3 (2, 4) |
| [P-PARCEL](#p-parcel) | Sentence fragments | 3 (4) |
| [P-SYNONYMS](#p-synonyms) | Elegant variation and needless repetition | 4 (3) |
| [P-EXPLETIVE](#p-expletive) (new) | Empty opener: "there is", "it is … that" | 3 (4) |
| [P-REFERENT](#p-referent) (new) | Pronoun without a clear referent | 3 (2) |
| **W** | **Words** | |
| [W-INTRO](#w-intro) | Hedges and filler | 4 (3) |
| [W-PROP](#w-prop) | Prop instead of an argument | 3 (2) |
| [W-POLITE](#w-polite) | Fake politeness | 3 |
| [W-EVAL](#w-eval) | Evaluation instead of a fact | 3 |
| [W-INTENS](#w-intens) | Intensifier | 3 (4) |
| [W-CLICHE](#w-cliche) | Cliché or filler phrase | 3 (4, 2) |
| [W-CORP](#w-corp) | Corporate buzzword | 3 (2) |
| [W-BUREAU](#w-bureau) | Officialese | 3 (2) |
| [W-ZAUM](#w-zaum) | Jargon and long words | 3 (2) |
| [W-NOMINAL](#w-nominal) | Hidden verb (nominalization) | 3 (2) |
| [W-PASSIVE](#w-passive) | Passive voice | 3 (2) |
| [W-VAGUE](#w-vague) | Vagueness | 3 (4) |
| [W-NOUNSTACK](#w-nounstack) (new) | Noun string | 3 (2) |
| [W-LLM](#w-llm) (new) | Machine-text tells | 3 (2) |
| **V** | **Illustrations** | |
| [V-DECOR](#v-decor) | Decoration instead of illustration | 3 (2) |
| [V-SCREEN](#v-screen) | Screenshot or table not prepared | 3 (2) |
| [V-NOSCREEN](#v-noscreen) | Product behaviour without a screenshot | 2 (3) |
| [V-NOSCHEME](#v-noscheme) | Complex process in words only | 2 (3) |
| [V-SCHEME](#v-scheme) | Diagram that cannot be read | 2 (3) |
| [V-RIGHTS](#v-rights) | Someone else's image without rights | 3 |

---

## M — Purpose and meaning

### M-READER
**The text serves the author, not the reader** · severity 1 · search: reading · sources: [PLAIN "Write for your audience"](sources/plain/guidelines/audience/index.md); [PLAIN "Do your research"](sources/plain/guidelines/audience/do-your-research.md); [GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md)

**Rule.** The text solves the reader's problem; the author's goal is reached through it.

**What goes wrong.** The text is written for the goal of the author or the organisation: to sell what pays best, to reproach, to vent, to show off style, to report what the organisation is proud of. PLAIN's starting point is the opposite: "people only want to know what applies to them", and readers whose task the content does not help with "get frustrated and potentially leave" (PLAIN "Do your research"). PLAIN's planning questions ask for the best outcome for the agency and the best outcome for the audience separately; a text that answers only the first misses its reader. The reader does not find the answer to their question and leaves.

**Signs.**
- You cannot tell from the text which of the reader's problems it solves.
- The material follows the logic of the seller or the agency — departments, programmes, product lines, the order of the internal process — not the way the reader chooses and acts.
- Most of the space goes to what benefits the author: the organisation's values, attitude, achievements, initiatives.
- "We are committed to…", "Our mission is…", "We are proud to announce…" where the reader needs to know what to do.
- Reproach, shaming or threats aimed at the reader.
- The author's personal grievances and experiences from which the reader takes nothing for themselves.
- The text is pitched at experts, lawyers or management although they are not its readers: "Don't write to the experts, the lawyers, or your management, unless they are your intended audience" (PLAIN "Write for your audience").

**Not an error if:**
- the text has a commercial or institutional goal but is built around the reader's task: in PLAIN's rewrite of the example below the agency still wants feedback, only the point of view changes;
- a personal story is told so that it helps the reader — to avoid the author's mistakes, to get through something similar;
- the reader came for the organisation itself (an "About us" page, a policy statement) and gets it (G2).

**Example.** "The Open Door Initiative is a program based on a simple and fresh attitude: that the CMS desires to better hear and interact with those beneficiaries, providers, and other stakeholders interested in the delivery of quality healthcare for our nation's seniors and beneficiaries with disabilities." — rewritten for the reader as "We want to hear from you! Help us improve our service to you. Attend an Open Door forum near you." ([PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md), before and after).

### M-GOAL
**No useful goal** · severity 1 · search: reading · sources: [PLAIN "Organize the information"](sources/plain/guidelines/organize/index.md); [GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md); [PLAIN "Paraphrase testing"](sources/plain/guidelines/test/paraphrase-testing.md); [PLAIN "Controlled comparative studies"](sources/plain/guidelines/test/controlled-comparative-studies.md)

**Rule.** The text has a goal — what should change in the reader's head or actions after reading, a path from "A" to "B" — and that change is useful to the reader.

**What goes wrong.** Two cases. (a) There is no goal: the thoughts do not line up into a path, and the reader cannot say what the author meant. PLAIN's paraphrase test asks readers exactly this — "What do you think the writer was trying to do with this document?" — and a text without a goal leaves them with no answer. (b) There is a goal and the text leads to it, but this "B" gives the reader nothing: "to tell you about…", "to share my views on…", "to raise awareness of…" — what does the reader gain? A "B" that leaves the reader helpless ("the world is dangerous and you can do nothing") is no better, and "to convince" or "to motivate" are goals the author does not control. PLAIN asks the writer to "Start by stating your purpose and the bottom line" (PLAIN "Organize the information") and defines success as a change in what readers do: more applications returned, fewer errors on forms, fewer calls asking for clarification (PLAIN "Controlled comparative studies").

**Signs.**
- After reading, the main point cannot be put in one sentence; the text allows several readings.
- The text is made of observations, evaluations and rhetorical questions on a common theme, not of steps towards a conclusion.
- The final conclusion does not follow from the beginning.
- Digressions follow one another: "By the way…", "I forgot to mention…", "As I said before…".
- One thesis is repeated in different ways with stories of the same kind and ends in helplessness — not a word about what the reader can do.
- The text names its own goal: "to tell you about…", "to share…", "to raise awareness…", "to convince…".
- A concept is explained (what it is, why the organisation values it) when the reader needed to know what to do about it.

**Not an error if:**
- the goal is not stated outright but can be recovered from the text;
- there are one or two digressions and the line holds — that is [M-DIGRESS](#m-digress);
- the topic is heavy or frightening: the topic can stay, only the "B" has to give the reader something to understand or do.

**Example.** "Mitigation is the cornerstone of emergency management. It's the ongoing effort to lessen the impact disasters have on people's lives and property through damage prevention and flood insurance." — the rewrite gives the reader a goal and three actions under "Protect your community from natural disasters!" ([PLAIN example "Protect Yourself from Natural Disasters"](sources/plain/examples/natural-disasters.md), before and after).

### M-DIGRESS
**Digression from the goal** · severity 3 (2 — if there are many digressions or they argue against the thesis) · search: reading · sources: [GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md); [PLAIN "Repurpose print material for the web"](sources/plain/guidelines/web/repurpose-print-material.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md); [Strunk 9](sources/strunk/3-principles-of-composition.md)

**Rule.** Every part of the text leads the reader to the text's goal.

**What goes wrong.** A fragment touches a neighbouring topic but does not lead to "B". One digression knocks the reader off the path; many make the text heavy, because too much in it is not needed. Nielsen, quoted by PLAIN: "Web users want actionable content; they don't want to fritter away their time on (otherwise enjoyable) stories that are tangential to their current goals." Caveats and examples that argue against the thesis steer the text towards a different conclusion. Strunk names the worst place for it: "Ending with a digression, or with an unimportant detail, is particularly to be avoided" (Strunk 9).

**Signs.**
- Markers of departure and return: "by the way", "incidentally", "on a side note", "I digress", "but that's another story", "anyway", "as I was saying", "more on that later".
- A caveat weakens the thesis, and the text never comes back to it.
- An example contradicts the thesis, or grows details about its hero that the argument does not need.
- Emotional asides away from the line.
- Material that would be a footnote. GOV.UK's test: "If the information in the footnotes is important, include it in the body text. If it’s not, leave it out."
- A paragraph or a section ends on an unimportant detail.

**Not an error if:**
- the fragment seems far off but works as an argument or an example for the thesis;
- the text deliberately acknowledges other points of view and returns to its line;
- the genre is narrative or essay, where a detour is part of the pleasure: PLAIN contrasts the web with print, where "you can go into great detail about mundane things like eating breakfast. If you are a great writer, that can be an interesting story" (G2).

**How the sources describe it.** GOV.UK: "Publish only what’s needed to meet that user need and nothing more" ([GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md)). PLAIN on print stories moved to the web: "But those interesting stories don't work on the web. Instead they slow down web users who are trying to accomplish a task" ([PLAIN "Repurpose print material for the web"](sources/plain/guidelines/web/repurpose-print-material.md)).

### M-HOLLOW
**Hollow text: words without information** · severity 2 (1 — if the whole text or its key block is written this way) · search: reading; the script flags blocks with three or more evaluation and cliché markers · sources: [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md); [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md); [Strunk 14 "Avoid a succession of loose sentences"](sources/strunk/3-principles-of-composition.md) · classics: Orwell, "Politics and the English Language" (meaningless words); Zinsser, *On Writing Well*, ch. 3 "Clutter"

**Rule.** The text contains the information the reader needs: what, who, how much, where, on what terms.

**What goes wrong.** A paragraph or a whole text is assembled from evaluations, buzzwords, inflated series and general promises, with no facts behind them. GOV.UK warns that buzzwords "are too vague and can lead to misinterpretation or empty, meaningless text" (GOV.UK "Use clear language"); PLAIN keeps a list of "meaningless filler phrases" (PLAIN "Avoid jargon"). Strike out the evaluations and only a frame is left. The reader cannot picture what is meant, and the text would fit any other organisation unchanged.

**Signs.**
- Almost every statement rests on an evaluation, an intensifier or a buzzword; there are no numbers, names, dates, conditions or situations.
- Strike-out test: with evaluations and filler removed, almost nothing of the paragraph is left.
- Swap test: put another company's name in, and the text fits it just as well.
- Self-descriptions without content: "a dynamic, fast-growing company", "a team of passionate professionals", "an industry leader", "world-class", "best-in-class".
- Promises without a mechanism: "on the best possible terms", "a seamless experience", "unlocks value", "takes your business to the next level".
- A run of evaluative adjectives with no detail after it: "innovative, reliable and cost-effective solutions".
- The text is free of filler but still does not answer the reader's natural questions — what exactly, how much, when, on what terms.

**Not an error if:**
- the paragraph contains facts the reader understands and the evaluations stand alone — then they are separate [W-EVAL](#w-eval) findings, not hollow text;
- facts are there but the reader cannot judge them — that is [M-FACTS](#m-facts);
- a single machine-text word ("seamless", "robust") sits in an informative text — that is [W-LLM](#w-llm).

**Example.** "The former showed himself to be an artist of the first rank, while the latter proved itself fully deserving of its high reputation. The interest aroused by the series has been very gratifying to the Committee, and it is planned to give a similar series annually hereafter." — Strunk's verdict on the paragraph opens with "Apart from its triteness and emptiness" ([Strunk 14](sources/strunk/3-principles-of-composition.md)); "Integrating quality solutions", "Promoting an informed and synergistic teams" from PLAIN's list of "meaningless filler phrases" ([PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md)).

### M-ABSTRACT
**Abstraction without a picture** · severity 2 (3 — a single phrase in a text that is otherwise concrete) · search: reading · sources: [Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md); [PLAIN "Choose your words carefully"](sources/plain/guidelines/words/index.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md) · classic: Pinker, *The Sense of Style*, ch. 2 "A Window onto the World"

**Rule.** The main point is told so that the reader can picture it: what can be seen, what people do, what will happen.

**What goes wrong.** The text speaks in concepts that do not exist in the material world — "solutions", "framework", "management", "quality", "engagement", "outcomes" — and backs them with nothing concrete. The reader has to decode the abstraction first, and that is extra work. Strunk quotes Spencer: "when an abstract word is used, the hearer or reader has to choose, from his stock of images, one or more by which he may figure to himself the genus mentioned. In doing this, some delay must arise, some force be expended" (Strunk 12). A logically correct set of statements does not create a picture, and without a picture the reader neither understands nor remembers. Strunk: "the surest method of arousing and holding the attention of the reader is by being specific, definite, and concrete." For buzzwords GOV.UK gives the same remedy: "you can generally get rid of them by breaking the term into what you’re actually doing. Be open and specific."

**Signs.**
- Everything in the sentence is abstract except the name: "X is a people-management platform for small businesses."
- "Solutions for…", "in the area of…", "in terms of…", "efficient and cost-effective solutions", "drive outcomes".
- A promised benefit without showing what it looks like: "helps streamline some processes", "can be the key to unlocking growth".
- Actions named by a generalisation ("engaged in disruptive behaviour") instead of the actions themselves.
- Verbs of delivery and struggle with abstract objects: "deliver improvements", "tackle challenges", "foster collaboration" — GOV.UK: "pizzas, post and services are delivered - not abstract concepts like improvements" (GOV.UK A to Z "Words to avoid").
- A list of facts without links and reasons; a number without what it means for the reader.
- "Concrete" detail that only a specialist can picture, in a text for a general reader.

**Not an error if:**
- the abstraction sums up concrete material already shown;
- for this audience the terms are the picture — a developer and "role-based access control";
- it is a reference work, a glossary or a text for insiders, where no picture is built (G2).

**Example.** "A period of unfavorable weather set in." (for "It rained every day for a week."); "He showed satisfaction as he took possession of his well-earned reward." (for "He grinned as he pocketed the coin.") ([Strunk 12](sources/strunk/3-principles-of-composition.md)).

### M-NOEXAMPLE
**Idea without an example** · severity 2 (1 — the whole explanatory text is theses only; 3 — a secondary thesis, or only the counter-example is missing) · search: reading; the script flags a long text with no example markers · sources: [PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md); [Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md)

**Rule.** Every idea the reader must absorb or apply is shown on an example; where the reader can go wrong — on a counter-example too.

**What goes wrong.** Advice, a rule, a conclusion or a promise is given in general form. Such a sentence creates no picture; the reader does not live through it and forgets it within a minute. Even a true thesis turns into filler: those who understand the abstraction do not need the text, and those who need the text do not understand the abstraction. Without a counter-example the reader will not recognise the mistake they are being warned against. PLAIN: "Good examples can substitute for long explanations. The more complex the concept you are writing about, the more you should consider using an example."

**Signs.**
- Imperative advice without a situation: "review your settings regularly", "engage your stakeholders", "read the contract carefully".
- Vague words that beg "what does that mean?" — "regularly", "stay up to date", "appropriate", "best practice" — with no answer in the text.
- Promises of a result: "will significantly improve", "will be able to".
- A list of theses in which none is unpacked.
- Neither in the paragraph with the thesis nor next to it is there "for example", "for instance", "say", "imagine", "suppose", a character, a scene, a line of dialogue, numbers.
- Only "how to do it right" is shown; "how people get it wrong" is not.

**Not an error if:**
- the example stands in the neighbouring paragraph or a separate block, or is given as a counter-example or an illustration;
- the text is for readers who already have this experience;
- the sentence is a step of an instruction, a concrete fact or part of an example, not a conclusion to absorb;
- the sentence explains or teaches nothing: a requirement, a slogan, an opinion, a news report. An example is needed for an idea the reader must take away — advice, a rule, a conclusion, a promised result;
- the text is built around one running example.

**How the sources describe it.** "In spoken English, when you ask for clarification of something, people often respond by giving you an example. […] By giving your audience an example that's relevant to their situation, you help them relate to your writing" ([PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md)); "In exposition and in argument, the writer must likewise never lose his hold upon the concrete, and even when he is dealing with general principles, he must give particular instances of their application" ([Strunk 12](sources/strunk/3-principles-of-composition.md)).

### M-EXAMPLE
**Example does not support the idea** · severity 3 (2 — an example without a conclusion, from which the reader takes the wrong lesson) · search: reading · sources: [PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md); [GOV.UK A to Z "Bullet points and steps"](sources/govuk/a-to-z-style-guide.md); [GOV.UK technical A to Z "example code"](sources/govuk/technical-a-to-z.md); [Strunk 12](sources/strunk/3-principles-of-composition.md)

**Rule.** An example illustrates a stated idea, is understandable to the target reader, and is introduced so that it is clear what to look at in it.

**What goes wrong.** There is an example, but it does not do its job.
- **No conclusion.** The story falls apart, and the reader decides alone which lesson to draw.
- **For show.** A story about a famous company that has nothing to do with the thesis, or an example in which the reader does not recognise themselves. PLAIN asks for "an example that's relevant to their situation".
- **Drowned in detail.** Details about the hero hypnotise the reader and lead away from the idea. Strunk's standard is "not that every detail is given […] but that all the significant details are given" (Strunk 12).
- **Sudden change of world.** The reader is thrown into a new reality without a lead-in; examples from different fields replace each other, and each time the reader spends effort getting in. GOV.UK asks for a lead-in even before code: "Before you give example code, describe what it does or how to use it" (GOV.UK technical A to Z "example code").
- **Examples that over-reach.** A few examples are read as the whole set: "The number and type of examples in a list may lead the user to believe the list is exhaustive" (GOV.UK A to Z "Bullet points and steps").

**Signs.**
- A paragraph opens with "Say…", "Imagine…", "Suppose…" and ends on an event; there is no rule or conclusion before it or after.
- Next to the thesis stands a story about a well-known company (Apple, Amazon, Netflix) that does not unpack a single word of the thesis.
- Personal details of the hero unrelated to the thesis: his partner's name, the cat's name, the neighbourhood where he rents.
- "For example…" plunges straight into a new field with no bridging phrase; a series of examples without a preamble.
- Two or three of the commonest cases, introduced with "such as", where the rule also covers others the reader may be in.
- A code sample or a quoted passage dropped in with no sentence saying what it shows.

**Not an error if:**
- the conclusion comes before the story or a paragraph later, or is set by a preamble or a heading;
- the details are concrete and serve the thesis (prices, models, deadlines); a long example is relevant throughout;
- the genre expects detail and the author immerses the reader on purpose;
- the change of world is announced, even in a couple of words ("An example from advertising:"), or the task needs examples from different fields.

**How the sources describe it.** PLAIN shows the lead-in done right: its EPA regulation introduces its example with "The following example explains what it would mean for an area to be in compliance with this type of standard" ([PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md)). GOV.UK on examples that mislead: "The number and type of examples in a list may lead the user to believe the list is exhaustive" ([GOV.UK A to Z "Bullet points and steps"](sources/govuk/a-to-z-style-guide.md)).

### M-ORDER
**Broken order of explanation** · severity 2 (3 — the point can be found, but later than it should be) · search: reading · sources: [PLAIN "Organize the information"](sources/plain/guidelines/organize/index.md); [PLAIN "Have a topic sentence"](sources/plain/guidelines/organize/have-a-topic-sentence.md); [PLAIN "Make it easy to follow"](sources/plain/guidelines/organize/make-it-easy-to-follow.md); [PLAIN "Minimize definitions"](sources/plain/guidelines/words/minimize-definitions.md); [PLAIN "Write for your audience"](sources/plain/guidelines/audience/index.md) · classics: Minto, *The Pyramid Principle*, ch. 1 "Why a Pyramid Structure?"; Pinker, *The Sense of Style*, ch. 5 "Arcs of Coherence"

**Rule.** The explanation goes in the order in which the reader can take it in: context and interest → situation and subject → thesis → examples and counter-examples → evidence. In a document: the point first, background last.

**What goes wrong.** The parts of the explanation are all there, but the reader meets details, classifications and evidence before understanding what it is about and whether it concerns them. A newcomer has not been shown what the subject is and why to read on, and cannot picture it. PLAIN: "Establish a context for your audience before you provide them with the details. If you flood readers with details first, they become impatient and may resist hearing your message." In a document the point sits after formalities and background, and the reader has to dig for it; PLAIN's order is the reverse: "Put the most important information at the beginning and include background information (when necessary) toward the end." This code also covers an "exotic" scheme of explanation — a running example, a big analogy, a plot — that does not fit the material: the example does not cover all the points, a plot on a subject that is not about people looks forced.

**Signs.**
- The first paragraph is straight away a typology, selection criteria or the first step of an instruction: "First, you need to work out which type of X you need…".
- The key subject of the title is nowhere defined or shown.
- The text does not say whom it concerns and in what situation — PLAIN's model opening is "If you want a research grant, here's what you have to do."
- Evidence, statistics or the history of the question come before the thesis.
- In a simple topic, a long run-up with the thesis only at the end.
- A document opens with its legal basis ("Pursuant to section…", "Under the provisions of…"), a definitions section, who is to blame, or the background; the substance is in the third or fourth block. PLAIN: "Place definitions at the end, in spite of tradition."
- A process is told out of the order in which the reader will go through it: "Chronological order is best for process information" (PLAIN "Make it easy to follow").
- The reason to read is replaced by a threat: "This will definitely come up in your exam."

**Not an error if:**
- the text opens with a scene or a running example that itself introduces the situation;
- the topic is complex and the author deliberately approaches the idea from afar;
- the text does not teach, or the subject is familiar to the reader; a short introduction of one or two sentences is enough;
- the form of the document is set by regulation (G2).

**How the sources describe it.** "We often write the way we think, putting our premises first and then our conclusion. It may be the natural way to develop thoughts, but we wind up with the topic sentence at the end of the paragraph" ([PLAIN "Have a topic sentence"](sources/plain/guidelines/organize/have-a-topic-sentence.md)); "In placing definitions at the end, you allow your user to go right to the text, rather than having to go through less important material" ([PLAIN "Minimize definitions"](sources/plain/guidelines/words/minimize-definitions.md)).

### M-LEVEL
**Wrong level for the reader: terms and detail** · severity 2 (3 — one superfluous detail while the main point is clear) · search: reading · sources: [PLAIN "Write for your audience"](sources/plain/guidelines/audience/index.md); [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [PLAIN "Paraphrase testing"](sources/plain/guidelines/test/paraphrase-testing.md); [PLAIN "Minimize abbreviations"](sources/plain/guidelines/words/minimize-abbreviations.md); [GOV.UK A to Z "abbreviations, acronyms and initialisms"](sources/govuk/a-to-z-style-guide.md); [GOV.UK technical A to Z "breaking changes"](sources/govuk/technical-a-to-z.md) · classic: Pinker, *The Sense of Style*, ch. 3 "The Curse of Knowledge"

**Rule.** The text speaks at its reader's level: new concepts are introduced through familiar ones, details the reader's task does not need are left out, and what the reader already knows is not explained again.

**What goes wrong.** Authors who know a subject deeply do not feel they are saying anything difficult — for them it is simple (Pinker's curse of knowledge). PLAIN: "writers often fail to realize that terms they know well may be difficult or meaningless to their audience". In a text for an unprepared reader there are terms explained by other terms or not explained at all; the key advice is packed into one professional word, and if that word is not fully understood, the whole text is lost; the mechanism is described instead of the result; a list of subtypes stands where one general word would do. The passage is hard not because the ideas are hard but because of the density of the unfamiliar. A term of art can make readers act wrongly: in PLAIN's paraphrase testing, readers each had their own idea of "service-connected disability", and "several would have done something other than what VBA wanted". The opposite fault is talking down: "Don't write for an 8th-grade class if your audience is composed of PhD candidates" (PLAIN "Write for your audience").

**Signs.**
- Several terms and abbreviations in one or two sentences; an abbreviation in brackets instead of an explanation: "general-purpose input/output (GPIO) pins".
- A term explained with other terms.
- The main action or conclusion rests on a professional word with no explanation: "make sure the operation is idempotent", "budget for contingencies". Even insiders may not share a term: GOV.UK asks to explain "breaking changes" because "user research shows not all technologists immediately understand what it means".
- The mechanism where the reader cares about the result: "using an accelerometer and a vibration motor".
- A series of subtypes or near-synonyms instead of one word: "ransomware, spyware, viruses, worms and trojans" where "malware" would do.
- Abbreviations beyond the well-known ones, left unexplained; PLAIN's ceiling is "no more than three, and preferably two" per document, GOV.UK keeps a list of the ones that need no explanation (BBC, NHS, UK, VAT and so on).
- Over-explaining to a reader who knows: PLAIN mocks "Thank you for writing to the Federal Aviation Administration (FAA) about your concerns" in a letter from that agency.

**Not an error if:**
- the reader is a specialist for whom this is part of their experience (G2);
- the term is introduced step by step from something familiar, or explained nearby. GOV.UK: "You just need to explain what they mean the first time you use them";
- the detail is exactly what matters.

**Example.** "For purposes of this section, section 1250 capital gain means the capital gain (not otherwise treated as ordinary income) that would be treated as ordinary income if section 1250(b)(1) included all depreciation and the applicable percentage under section 1250(a) were 100 percent." — a definition built from other terms, which PLAIN offers as a section a user would have to "puzzle out" ([PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md)).

### M-IDEAL
**Advice for the ideal case only** · severity 2 (1 — if the whole instruction is built this way and acting on it is the main task of the text) · search: reading · sources: [PLAIN "Paraphrase testing"](sources/plain/guidelines/test/paraphrase-testing.md); [PLAIN "Write for your audience"](sources/plain/guidelines/audience/index.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md); [PLAIN "Avoid FAQs"](sources/plain/guidelines/web/avoid-faqs.md)

**Rule.** Instructions and advice take into account how things actually go: what to do if it did not work, what traps and difficulties await the reader.

**What goes wrong.** The instruction or advice describes how things should be, not how they are. Reality departs from the expectation, and the person acting falls back on their own understanding — or rings the helpline. General advice gets the reaction "everyone knows that" or is forgotten at the first obstacle. PLAIN's planning question is "What questions will my audience have?", and for FAQs it warns "Do not assume what kinds of questions people will have." GOV.UK reminds writers of the reader's real conditions: "Users may also be stressed or under pressure and want to find an answer quickly. For example, they could be on a busy train or be experiencing a difficult family event."

**Signs.**
- The instruction describes only the happy path: no "if this doesn't work…", "if you see the message…", "if you miss the deadline…".
- Similar but wrong options are not named, though the temptation is obvious.
- The text does not say when to go back to the author or to support.
- No warning about typical traps (the wrong version, extra purchases, failure on first run) or human obstacles (tiredness, lack of time, relapse).
- Timing or outcome is given only for the case where everything works: "shortly", "in due course", "you will receive".
- General imperatives nobody argues with: "eat well and exercise", "follow best practices".

**Not an error if:**
- the reader is independent in this matter;
- it is a reference instruction for a quick answer (G2);
- the text gives no practical recommendations: news, a description, an explanation of a concept.

**Example.** "You will receive the new check shortly." — readers "indicated that they would call if they didn't receive the check at the same time as the letter"; giving an approximate date "eliminated countless phone calls" ([PLAIN "Paraphrase testing"](sources/plain/guidelines/test/paraphrase-testing.md)).

### M-OFFEND
**A jab at the reader** · severity 2 (3 — a single case on a neutral topic) · search: reading · sources: [GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [PLAIN "Minimize abbreviations"](sources/plain/guidelines/words/minimize-abbreviations.md); [GOV.UK A to Z "disabled people", "ethnic minorities", "Gender"](sources/govuk/a-to-z-style-guide.md)

**Rule.** The text does not put the reader in an unpleasant role and does not hurt them without need.

**What goes wrong.** A carelessly chosen example, label or comparison triggers a stereotype, offence or a defence of the reader's view of the world. From that moment the reader stops taking in the information, however right the author is: they write an angry comment or leave without a word. A special case is a hypothetical example that casts the reader in a shameful role. English adds a quieter jab: telling the reader that a task is easy. GOV.UK bans "easy", "simple" and "quick" in technical writing because each "can demoralise users" who do not find it so. PLAIN, on over-explaining the obvious: "don't insult your users and waste their time".

**Signs.**
- A sweeping judgement of a group the reader may belong to: "millennials can't…", "people who still use X…".
- A label an ordinary reader fits: "non-technical folks", "laypeople", "normies".
- A comparison that reads as a dig at the reader's choice: "unlike teams still stuck in spreadsheets".
- A negative character in whom the typical reader recognises themselves.
- "Suppose you…", "Imagine you…", "Let's say you…" followed by a shameful, illegal or unpleasant act.
- "Simply", "just", "obviously", "of course", "as everyone knows", "it's easy", "any beginner can" before a step the reader may find hard.
- On a charged topic, an example or a word with a strong stereotyped association that the idea can do without; terms GOV.UK replaces ("the disabled" — use "disabled people"; "BAME"; "males" and "females" for women and men).

**Not an error if:**
- the topic is not emotional and the association does not provoke this audience;
- the unpleasant situation is described for a third person;
- a counter-example is used as a tool, as long as the reader does not recognise themselves in it;
- "easy" is a checkable statement about the product ("setup takes two steps"), not a judgement about how hard the reader will find it.

**How the sources describe it.** "easy or easily - this can demoralise users if they do not find it easy" ([GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md)); "When you're using a nickname for the main topic you're writing about, don't insult your users and waste their time" ([PLAIN "Minimize abbreviations"](sources/plain/guidelines/words/minimize-abbreviations.md)); "You must not use offensive words or terms in GOV.UK content" ([GOV.UK "Use the right tone"](sources/govuk/right-tone.md)).

### M-FACTS
**Facts that do not serve the reader** · severity 3 (2 — the main argument rests on such facts, or they crowd out the answer to the reader's question) · search: script partly, reading · sources: [PLAIN "Follow web standards"](sources/plain/guidelines/web/index.md); [GOV.UK "Write content to meet user needs"](sources/govuk/meet-user-needs.md); [PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md); [GOV.UK A to Z "billions", "Millions"](sources/govuk/a-to-z-style-guide.md)

**Rule.** Facts are chosen for the reader's questions and translated into the reader's experience.

**What goes wrong.** Two cases.
- **Numbers outside experience.** A height in metres, a screen in inches, a thickness in millimetres: what matters is not the facts themselves but whether the reader can take them in, and for a non-specialist they are a column of numbers that creates no sense of size.
- **Useless facts.** The number of developers, calls handled, servers or cups of coffee is entertaining, but the client wants to know whether the product will be built for them. PLAIN: "Use only the information your users need to achieve their top tasks. Omit unnecessary information." Its own case: the camper "needs to know whether there is an animal emergency plan, but not the details of the plan" (PLAIN "Minimize cross-references").

**Signs.**
- Technical specifications without a comparison with something familiar (a sheet of A4, the floors of a building, days without charging).
- Quantities in an unfamiliar scale. GOV.UK writes "£200 million" rather than "£0.2 billion" outside a sequence of billions; a column of specifications.
- Internal company metrics not linked to the reader's benefit; "fun" counters; "teams in 12 countries and 52 cities".
- After all the numbers, the main thing is still unclear: what the company does, for whom, how well.

**Not an error if:**
- the reader is a specialist or an enthusiast for whom the quantity is part of experience;
- a clear comparison stands next to the exact figure — the exact data need not be removed;
- the fact answers the reader's question or backs a promise that matters to them.

**How the sources describe it.** "Only necessary information: Use only the information your users need to achieve their top tasks. Omit unnecessary information." ([PLAIN "Follow web standards"](sources/plain/guidelines/web/index.md)); "the camper needs to know whether there is an animal emergency plan, but not the details of the plan contained in Section 52" ([PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md)).

### M-ROBOT
**Mechanical editing** · severity 3 (2 — the whole text sounds like this, or important meaning has been lost) · search: reading · sources: [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md); [Strunk 14 "Avoid a succession of loose sentences"](sources/strunk/3-principles-of-composition.md); [PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md); [PLAIN "Use contractions"](sources/plain/guidelines/conversational/use-contractions.md) · classic: Orwell, "Politics and the English Language", rule 6

**Rule.** The text sounds like natural speech and keeps the meaning it was written for; rules of form do not trespass on content.

**What goes wrong.** Rules have been applied by template, without taste or common sense. Either the text is formally "correct" but lifeless — Strunk's words for such prose are "mechanical symmetry and sing-song" (Strunk 14). Or the rules of form have eaten into the content: nuance, detail and purpose have been cleaned out, and the text is shorter but less useful. Strunk's own limit on cutting is that it "requires not that the writer make all his sentences short, or that he avoid all detail and treat his subjects only in outline" (Strunk 13). PLAIN warns that uniformity backfires: "if all paragraphs are the same size your writing will be choppy".

**Signs.**
- A run of short sentences of one pattern — actor, verb, object — with the same rhythm.
- Actors invented, or objects made to act, only to get an active verb, where nobody in fact acts.
- Obtrusive repetition of the subject and of words with the same root.
- A bare series of verbs with nothing behind them.
- A style rule applied to every case at once: every passive turned active, every "which" turned into "that", contractions everywhere or nowhere, whatever the sentence.
- The text lists what was done but not why or for whom.
- Read aloud, it sounds like a list, not like speech.

**Not an error if:**
- short simple sentences sound natural;
- the author departed from a formal rule for the sake of naturalness or a needed detail (G1). PLAIN on contractions: "Don't use them wherever possible, but wherever they sound natural."

**Example.** "Macbeth was very ambitious. This led him to wish to become king of Scotland. The witches told him that this wish of his would come true. The king of Scotland at this time was Duncan." — "a single complex idea, step by step, in a series of sentences" ([Strunk 13](sources/strunk/3-principles-of-composition.md)); the concert paragraph quoted under [M-HOLLOW](#m-hollow) is, in Strunk's words, "weak because of the structure of its sentences, with their mechanical symmetry and sing-song" ([Strunk 14](sources/strunk/3-principles-of-composition.md)).

---

## T — Truth and trust

### T-BS
**Generalization or promise without facts** · severity 2 (1 — if the main thesis or the title rests on it) · search: script + check · sources: [Strunk V "Fact"](sources/strunk/5-words-commonly-misused.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md)

**Rule.** A statement about a trend, a common opinion or an effect is backed by a fact and a source, or honestly presented as the author's opinion.

**What goes wrong.** Vague wording that is formally not a lie, but not the truth either: no facts are shown, and a trend or a universal opinion is passed off as a fact. An unprepared reader takes it for a fact; a prepared one is not convinced. Strunk keeps the word *fact* for "matters of a kind capable of direct verification, not of matters of judgment" (Strunk V "Fact"). The second form is an unverifiable promise — "dramatically improves your chances", "will become your indispensable assistant", "arguably the best" — in which, formally, the author promised nothing. GOV.UK asks to replace pledges with what will actually be done ("commit/pledge, use ‘plan to x’, or ‘we’re going to x’ where ‘x’ is a specific verb") and warns that adjectives "can be subjective and make the text sound more emotive and like spin". A common case is a single event blown up into a trend for the sake of a headline.

**Signs.**
- A trend without numbers or a source: "increasingly", "more and more", "is rapidly gaining popularity", "on the rise", "a growing number of".
- A universal opinion: "everyone is talking about", "it's no secret that", "few would disagree", "many believe", "it is widely accepted".
- Nameless authorities: "studies show", "research suggests", "experts agree", "scientists have found", "according to research" with no study named.
- Absolute generalisations: "no business can afford to ignore…", "everybody knows that…".
- A promise without a measure: "dramatically", "exponentially", "the key to lasting health", "game-changing", "who better than us".
- A pledge with no action behind it: "we are committed to…", "we pledge to…".
- Topic-swap test: the sentence is just as convincing, or unconvincing, with any other topic put into it.

**Not an error if:**
- a source of the data is named nearby — statistics, a survey, a publication, a book — even an imperfect one. GOV.UK's own "Research shows that…" carries a link to the research (GOV.UK "Use clear language");
- the author openly speaks for themselves: personal experience or opinion ("in my experience", "I think");
- the trend is confirmed by facts in the text itself;
- the statement is concrete and checkable — it says what, who, how much — even if no source is given: a concrete fact is what replaces an evaluation. A number that cannot have been measured or checked is [T-NUMBERS](#t-numbers);
- it reports an event or a state without a generalisation, trend or promise.

**How the sources describe it.** "Use this word only of matters of a kind capable of direct verification, not of matters of judgment. […] But such conclusions as that Napoleon was the greatest of modern generals, or that the climate of California is delightful, however incontestable they may be, are not properly facts" ([Strunk V "Fact"](sources/strunk/5-words-commonly-misused.md)); adjectives "can be subjective and make the text sound more emotive and like spin" ([GOV.UK "Use the right tone"](sources/govuk/right-tone.md)). The sources give no sample of an unsourced generalisation in running text.

### T-NUMBERS
**Misleading numbers** · severity 1 (3 — if the false conclusion from adjacent numbers is harmless) · search: script partly, reading · sources: [Strunk V "Fact"](sources/strunk/5-words-commonly-misused.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [PLAIN "Follow web standards"](sources/plain/guidelines/web/index.md) · classic: Huff, *How to Lie with Statistics*, ch. 3 "The Little Figures That Are Not There" and ch. 7 "The Semiattached Figure"

**Rule.** A number is measurable, has a source, and does not push the reader towards a wrong conclusion.

**What goes wrong.** Two cases.
- **Science-flavoured number.** The unmeasurable or the unmeasured is measured, as in a "99% of people… but only 1%…" pair about people in general. It is a figure of speech for "many" or "everyone" wrapped in a number, a cheap trick that undermines trust in the whole text.
- **Adjacent numbers.** The reader instinctively multiplies or divides numbers that stand side by side: an annual rate next to a four-year term reads as the total return; a budget next to a number of episodes reads as the cost of one episode.

**Signs.**
- Percentages about "people" in general without a source or a method; a "99% / 1%" pair.
- An over-precise, unrounded number where counting is impossible: a seven-digit count of "happy customers", microbeads counted to the unit.
- Two or three numbers side by side that invite arithmetic: rate × term, price ÷ quantity, change ÷ period.
- Figures built on different definitions compared as if they were alike.

**Not an error if:**
- the quantity was actually measured, and it is clear by whom and how — PLAIN's "In a 2008 study, based on analysis of 45,237 page views, Neilson found that web users only read about 18% of what's on the page";
- the conclusion the numbers invite is true and is the one the author wants the reader to draw.

**How the sources describe it.** The sources do not describe this error directly; they show the opposite practice. Each statistic on GOV.UK's writing pages carries a link to its study, with a caveat where the definitions differ: "The definition of ‘literacy skills’ varies by nation, but you can see that many people who will need to read GOV.UK will struggle unless language is kept simple" ([GOV.UK "Use clear language"](sources/govuk/clear-language.md)). Strunk restricts *fact* to "matters of a kind capable of direct verification" ([Strunk V "Fact"](sources/strunk/5-words-commonly-misused.md)). The two cases above are carried over from rutalk.

### T-HIDE
**Bad news hidden** · severity 1 (4 — an everyday euphemism that hides no problem) · search: script + check · sources: [Strunk 11 "Put statements in positive form"](sources/strunk/3-principles-of-composition.md); [PLAIN "Use active voice"](sources/plain/guidelines/conversational/use-active-voice.md); [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md) · classic: Orwell, "Politics and the English Language" (euphemism)

**Rule.** A problem, a mistake or bad news is stated directly: what happened, who did it, what it means for the reader.

**What goes wrong.** Something unpleasant is replaced by a harmless word, an official formula or a reassuring phrase: it sounds like criticism, yet nothing bad has been said. It is formally true and in effect no better than a lie: the reader does not see the problem, does not raise the alarm in time, or draws the opposite conclusion — that nothing needs doing and all is well. Strunk: "Use the word *not* as a means of denial or in antithesis, never as a means of evasion", and avoid "tame, colorless, hesitating, non-committal language" (Strunk 11). The passive helps hide the actor: "Passive voice obscures who is responsible for what" (PLAIN "Use active voice"). Orwell's essay describes the political version: pleasant names for brutal things.

**Signs.**
- A softened assessment in criticism: "not quite where we'd like it to be", "an area for development", "room for improvement", "did not fully meet expectations", "not very often on time".
- Bad news in abstract words, with no actor and no fact: "a decision has been made to pause the project", "due to unforeseen circumstances", "we are doing everything we can", "mistakes were made".
- Softening adverbs for large losses: "slightly lower", "somewhat higher"; a concession "despite…, we remain a strong and profitable company".
- Pleasant names for unpleasant things: "rightsizing", "workforce reduction", "negative growth", "streamlining" for job cuts. GOV.UK's "Words to avoid" lists several such verbs ("streamline", "slim down", "transform") and asks writers to "describe what you’re doing".
- Reassuring formulas without facts: "everything is under control", "there is no cause for concern".
- Retold in plain words, the passage sounds noticeably more alarming or shameful than the original.

**Not an error if:**
- the word is used in its direct meaning, not in place of a harsher one;
- the criticism is of an action and its consequences, not of a person — that is directness, not softening;
- the change really is small. Politeness is not an exception: softening that hides a problem still hides it.

**Example.** "He was not very often on time." (for "He usually came late."); "*The Taming of the Shrew* is rather weak in spots." ([Strunk 11](sources/strunk/3-principles-of-composition.md)); "Bonds will be withheld in cases of non-compliance with all permits and conditions." — the actor is gone; PLAIN's rewrite names it: "We will withhold your bond if you don't comply with all permit terms and conditions." ([PLAIN "Use active voice"](sources/plain/guidelines/conversational/use-active-voice.md)).

### T-TITLE
**Title claims more than the facts** · severity 1 · search: script partly, reading · sources: [GOV.UK "Write clear titles"](sources/govuk/clear-titles.md); [GOV.UK "Write clear summaries"](sources/govuk/summaries.md)

**Rule.** The title, read without the article, gives a correct idea of the facts.

**What goes wrong.** The author seizes on one fact, pulls it out of context and inflates it. Many people read only the title and share the piece without reading it; GOV.UK reminds writers that the title and the summary are "usually what users see in search results". A distorted title misinforms people who never reach the text, and can do real harm.

**Signs.**
- An emotive word hints at guilt or a scale the facts in the article do not support: "Horrific tragedy…", "slams", "destroys", "admits".
- A quotation stitched together with an ellipsis or cut down to one or two words.
- A verb or phrase that reads two ways ("X linked to Y" over a weak correlation, "Scientists warn…" over one researcher's remark).
- A categorical generalisation that the text narrows with caveats ("Coffee causes cancer" over a study in mice).
- A question headline whose honest answer, given in the text, is "no".

**Not an error if:** the title about a grave event conveys the facts accurately; a quotation in the title keeps the meaning of what was said.

**How the sources describe it.** The sources do not discuss distorted titles directly. GOV.UK requires a title to make sense "by itself" and "in search results", and to be descriptive "so that users can distinguish if it’s the right content for them" ([GOV.UK "Write clear titles"](sources/govuk/clear-titles.md)); the summary "should give them a clear indication of what the content is about" ([GOV.UK "Write clear summaries"](sources/govuk/summaries.md)). A title that holds only with the article's caveats fails that test. The signs are carried over from rutalk.

### T-METAPHOR
**Misleading analogy** · severity 1 (not an error if the false properties do not affect the reader's conclusions) · search: reading · sources: [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md); [Strunk V "Compare", "Literal, literally"](sources/strunk/5-words-commonly-misused.md)

**Rule.** An image helps the reader understand the subject, but does not lend the subject properties it lacks and does not serve as proof.

**What goes wrong.**
- **False properties.** Something complex is explained through a familiar image, and the reader involuntarily transfers to the subject properties of the image that the subject does not have. The reader is not just clear — too clear. The result can be costly: trusting a risky product because it was likened to a safe, familiar one.
- **Argument on a metaphor.** A conclusion about the subject is drawn from the properties of the image. With enough will a metaphor can "explain" any nonsense, and an elegant analogy is the most treacherous, because its elegance hides the gaps in the logic.

GOV.UK's general warning is that metaphors "do not say what you actually mean and lead to slower comprehension of your content". Strunk's definition marks the limit of any comparison: to *compare to* is "to point out or imply resemblances, between objects regarded as essentially of different order" — a resemblance, not an identity (Strunk V "Compare").

**Signs.**
- "X is like Y", "think of X as Y", "X is basically Y"; the image unfolded into several correspondences.
- The image has properties that matter for the reader's decisions and that the subject lacks: a safe, guaranteed everyday domain explains a risky one ("an investment fund is like a savings account").
- A conclusion follows the image: "so…", "that's why…", "in the same way…", "if X is Y, then…".
- A rhetorical question whose answer is obvious only inside the image.
- Metaphors of diagnosis and cure ("a cancer on the company", "the medicine the economy needs"); false numeric parallels ("the body is 60% water, so…").
- Apart from the image, nothing supports the thesis.

**Not an error if:**
- the image is close to reality and its side associations do not get in the way;
- the inaccuracies of the image do not lead to a wrong conclusion for the reader's task — the metaphor is good enough for the job at hand;
- the metaphor illustrates a conclusion established otherwise; the text analyses someone else's metaphor (G5).

A worn-out image such as "a red flag" is [W-CLICHE](#w-cliche).

**How the sources describe it.** "Avoid using metaphors - they do not say what you actually mean and lead to slower comprehension of your content" ([GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md)); *literally* is "Often incorrectly used in support of exaggeration or violent metaphor" ([Strunk V "Literal, literally"](sources/strunk/5-words-commonly-misused.md)). The sources warn against metaphor in general; the specific danger of an analogy that lends false properties or stands in for proof is carried over from rutalk.

### T-RATING
**Rating with rigged criteria** · severity 1 · search: reading · sources: [GOV.UK "Write effective links"](sources/govuk/add-links.md); [PLAIN example "Water Resources"](sources/plain/examples/water-resources.md)

**Rule.** A comparison shows the criteria that matter for the reader's choice and does not hide the weak sides of the favoured option.

**What goes wrong.** A table or scorecard makes the conclusion look obvious, but the author invents the criteria and the scores: the objectivity of the scores and the relevance of the criteria are almost impossible to check, and that leaves room for manipulation. Only what the favoured option is strong in goes into the rating, and the reader concludes it is the best on every count, though the rest simply is not shown. Obvious is not always right.

**Signs.**
- A comparison table or scorecard with points, stars, ticks and crosses.
- One option leads on every criterion, especially when the text sells it.
- Few criteria, vague or compound ones ("value for money", "ease of use"); parameters that matter for the category are missing.
- No word on where the scores come from.
- A vendor's or an affiliate's "independent comparison" that puts the vendor's product first.

**Not an error if:** the options win on different criteria; a rating as a device is normal; a selling angle is not an error by itself (G3); the basis of the scores is stated, as in PLAIN's report where "based on expert opinions, subjective assessments were provided as to conditions in terms of good, fair, poor, etc." ([PLAIN example "Water Resources"](sources/plain/examples/water-resources.md)).

**How the sources describe it.** The sources do not discuss rigged ratings. The nearest rule is GOV.UK's for links: "you must have a reason for linking to one commercial website instead of another if they provide similar information" ([GOV.UK "Write effective links"](sources/govuk/add-links.md)) — preferring one commercial option to a similar one needs a stated reason. The rest of this entry is carried over from rutalk.

### T-TERMS
**Clever word in the wrong sense** · severity 2 (1 — a factual error in advice; 3 — the meaning is not distorted) · search: script partly, reading · sources: [Strunk V "Words and expressions commonly misused"](sources/strunk/5-words-commonly-misused.md); [PLAIN "Minimize definitions"](sources/plain/guidelines/words/minimize-definitions.md); [PLAIN "Paraphrase testing"](sources/plain/guidelines/test/paraphrase-testing.md) · classic: Fowler, *A Dictionary of Modern English Usage*, "Popularized technicalities"

**Rule.** A term is used in its exact meaning and to the point.

**What goes wrong.** The author uses an impressive word or a term without knowing its exact meaning: confuses similar words, gives a term an everyday meaning, scatters terms from someone else's field to sound clever. A reader who knows catches the mistake, and the author looks foolish; the meaning of the sentence is distorted or cannot be recovered. Strunk's section V is a catalogue of such words; he asks the writer "to express accurately his own individual thought" instead of reaching for "a ready-made formula". A word can also mean different things to different readers: testing a form, PLAIN found that "readers used at least three different definitions of "gainful" employment".

**Signs.**
- The word's meaning does not fit the context: "literally" for emphasis, "phase" for "aspect", "fact" for an opinion, "begs the question" for "raises the question", "decimate" for "destroy", "exponential" for "fast", "ironic" for "unlucky", "disinterested" for "uninterested", "fortuitous" for "fortunate".
- Psychological, medical and scientific terms outside their field with a substituted meaning: "I'm so OCD about my desk", "a paradigm shift in the lunch menu", "a quantum leap" for a big step.
- A confident definition "X is…" with wrong content.
- A heap of grand words after which it is unclear what was meant.
- A common word defined to mean something it does not mean: "Never define a word to mean something other than its commonly accepted meaning" (PLAIN "Minimize definitions").

**Not an error if:** the term is used in its exact meaning in its own field; the word is in an informal register where the loose sense is idiomatic and nothing factual depends on it (G2).

**Example.** "A literal flood of abuse."; "Literally dead with fatigue" ([Strunk V "Literal, literally"](sources/strunk/5-words-commonly-misused.md)); "Another phase of the subject" — *phase* is "Not to be used for *aspect* or *topic*" ([Strunk V "Phase"](sources/strunk/5-words-commonly-misused.md)); "*Pages* means paper copies of standard office size or the dollar value equivalent in other media" — "Ten pages into the document, how do you think the average reader would respond if asked to define "page"?" ([PLAIN "Minimize definitions"](sources/plain/guidelines/words/minimize-definitions.md)).

### T-PERSONAL
**Judging the person, not the action** · severity 2 · search: script partly, reading · sources: [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [Strunk 11 "Put statements in positive form"](sources/strunk/3-principles-of-composition.md)

**Rule.** Criticism assesses the work, the action and their consequences, not the person.

**What goes wrong.** Directness turns into rudeness when the author judges a person as a whole. It is a label without facts: we do not know what the person is like, we only know that an action had consequences. Judging other people is neither the author's business nor their right. The addressee gets a label instead of a description of the problem, and the criticism does not land.

**Signs.** "He / she / you + a judgement of the person": "he's lazy", "she's useless", "they're incompetent", "he's an idiot"; "he has no taste", "she has no talent"; insults and guesses about motives ("he just wants attention"); a diagnosis used figuratively as an insult ("psycho", "narcissist").

**Not an error if:** the work or the action is judged, even harshly — "this is poor work"; the author describes the consequences of an action or how it affected them; the word is used in its literal meaning (a diagnosis in a clinical text).

**How the sources describe it.** The sources do not treat this error directly. GOV.UK's tone is "emotionless – adjectives can be subjective and make the text sound more emotive and like spin", and it bans offensive words ([GOV.UK "Use the right tone"](sources/govuk/right-tone.md)). Strunk's rewrite of an evasive criticism stays with behaviour: "He was not very often on time" becomes "He usually came late" ([Strunk 11](sources/strunk/3-principles-of-composition.md)). The rule itself is carried over from rutalk.

---

## S — Structure and delivery

### S-TITLE
**Title does not say what the text is about** · severity 2 (3 — the topic can be guessed with effort; a short standalone text has no title) · search: script (no title), reading · sources: [GOV.UK "Write clear titles"](sources/govuk/clear-titles.md); [GOV.UK A to Z "Titles"](sources/govuk/a-to-z-style-guide.md); [PLAIN "Usability testing"](sources/plain/guidelines/test/usability-testing.md)

**Rule.** A standalone text has a title, and the title answers "What is this about?" and "Do I need it?".

**What goes wrong.** With no title, or with a riddle for a title, the reader cannot tell whether the text concerns them and has to read the text to decode the title. A pun sounds clever but does not say what the piece is about: the reader wants to solve a problem, not admire the author's wit. If the title promises another topic or another audience, everything in the text that does not match becomes superfluous — or the right readers decide the text is not for them. GOV.UK: "By being general about a topic, you leave the user asking ‘what is this about?’"; "If people cannot find your page, they will not be able to act on it or know it’s for them."

**Signs.**
- A standalone text starts straight with a paragraph.
- The title is an exclamation, a metaphor, a proverb or a pun, with no words naming the topic.
- A comparison with a celebrity, or a conversational question, instead of the topic.
- The playful part comes first; the meaningful part comes after it and is vague.
- A bare label that says nothing by itself: "Regulations", "Update", "Overview", "New process".
- The type of content instead of the content: "Potato guidance".
- The title addresses another audience or goal than the text; the text covers what the title does not promise.
- Navigational titles (instructions, help pages, site sections) that are creative or use other words than the ones readers search for. GOV.UK: "The official or internal name may not be what the public calls it."

**Not an error if:**
- the title is plain, even banal, but names the topic;
- a question promises a clear benefit, in a genre that allows question titles (GOV.UK pages do not; G2);
- an idiom conveys the point directly;
- the review covers a fragment, or the body of an email whose subject line is set elsewhere.

**Example.** "Hazardous waste – new process" (GOV.UK's good version: "How to dispose of hazardous waste in your area"); "Potato guidance" ([GOV.UK "Write clear titles"](sources/govuk/clear-titles.md)); "People of Color Get Skin Cancer, Too" — readers "said that the title, "People of Color Get Skin Cancer, Too," made them think it was only for African-Americans" ([PLAIN "Usability testing"](sources/plain/guidelines/test/usability-testing.md)).

### S-CLICKBAIT
**Clickbait title** · severity 3 (2 — the text does not deliver what the title promises) · search: script + check · sources: [Strunk V "Interesting"](sources/strunk/5-words-commonly-misused.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [PLAIN "Highlight important concepts"](sources/plain/guidelines/design/highlight-important-concepts.md); [GOV.UK A to Z "Titles"](sources/govuk/a-to-z-style-guide.md)

**Rule.** A title attracts with the text's usefulness, not with tabloid tricks.

**What goes wrong.** Urgency, shock, intrigue, inflated value, a complex topic reduced to a listicle. Such titles attract the least careful readers and put off the rest. When everything grabs, nothing grabs; behind a loud promise there is often nothing, and trust is lost. Strunk's advice on the word "interesting" fits titles: "Instead of announcing that what you are about to tell is interesting, make it so" (Strunk V "Interesting"). Capitals read as shouting — "AND ONLINE, IT'S CONSIDERED SHOUTING" (PLAIN "Highlight important concepts").

**Signs.**
- "BREAKING", "SHOCKING", "You won't believe…", "…will blow your mind", "This one trick…", "Doctors hate him".
- Words in capitals, "!", "?!", an ellipsis at the end; intrigue instead of a name: "these two foods", "what happened next".
- Tags like "[PHOTOS]", "(VIDEO)", "[Full Guide]", "Everything you need to know about…", "The ultimate guide to…".
- "10 things you need to know about relationships" over a complex topic.
- The text does not deliver: "[PHOTOS]" over two pictures, an empty piece under a loud title.

**Not an error if:**
- a news item starts with the time of the event ("15:30 — …");
- a sensational fact is stated plainly: real news needs no shouting;
- "photos" and "infographic" are backed by the material;
- a number does not oversimplify a complex topic: "Three ways to tie a tie";
- a formula reveals a non-obvious benefit: the audience, the price, the time it takes;
- an exclamation belongs to a call to action, not to a title's promise — PLAIN's own rewrite opens with "We want to hear from you!" ([PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md)).

**How the sources describe it.** "Avoid this word as a perfunctory means of introduction. Instead of announcing that what you are about to tell is interesting, make it so" ([Strunk V "Interesting"](sources/strunk/5-words-commonly-misused.md)); "Do not use block capitals for large amounts of text. It’s hard to read and it can be understood as shouting" ([GOV.UK "Use the right tone"](sources/govuk/right-tone.md)). The sources give no sample of a clickbait title; the signs are carried over from rutalk.

### S-SCAN
**The main point is invisible when skimming** · severity 2 (3 — for a text of medium length, or a document the reader does not have to act on) · search: reading of the skeleton (the script prints the block map) · sources: [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md); [PLAIN "Follow web standards"](sources/plain/guidelines/web/index.md); [PLAIN "Have a topic sentence"](sources/plain/guidelines/organize/have-a-topic-sentence.md); [GOV.UK "Write clear summaries"](sources/govuk/summaries.md); [GOV.UK A to Z "bold"](sources/govuk/a-to-z-style-guide.md); [PLAIN "Highlight important concepts"](sources/plain/guidelines/design/highlight-important-concepts.md)

**Rule.** From the skeleton of the text — the title, subheadings, paragraph openings, emphasis, lists, captions, summary — it is clear what the text is about, what its main point is, whether the reader needs it and where to start.

**What goes wrong.** People mostly skim: GOV.UK cites research that most people "only read 20 to 28% of text on a webpage" and read in an "F" shape. If the skeleton does not carry the point, the reader does not know where to start and leaves. A long, complex document has no summary, although most readers need to grasp at once what is going on and what to do — or the summary has itself become a wall of text. Decoration for its own sake — emphasis everywhere, a pulled-out quote from the boss made of generalities — draws the eye and says nothing: "Only emphasize important information, otherwise you'll dilute its impact" (PLAIN "Highlight important concepts"); too much bold "will make it difficult for users to know which parts of your content they need to pay the most attention to" (GOV.UK A to Z "bold").

**Signs.**
- From the skeleton alone you cannot answer "what is this, what is the main point, do I need it, where do I start".
- The main point and the conclusions are only inside ordinary paragraphs.
- A document of many screens (an analysis of a law, a report, a policy) without a "Summary", "Key points" or "What you need to do" block at the start or the end.
- The summary is comparable in size to the document, or is itself written in solid paragraphs.
- Bold, capitals or call-outs spread so widely that nothing stands out; the most prominent element is a quote with no facts.
- The topic sentences, read in a row, give no general understanding. PLAIN: "Readers should be able to get good general understanding of your document by skimming your topic sentences."

**Not an error if:**
- the text is short, up to about two-thirds of a screen (≈ 300 words, rutalk's threshold converted to words);
- the text is by nature read straight through (an argument, a story): its skeleton says what it is about but need not give away every conclusion (G2);
- the summary stands at the end; a summary block is a recommendation for long complex texts, not a required element.

**How the sources describe it.** "People read content on the web differently. They will often skim it and not read every sentence" ([GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md)); "Users often scan pages in an F pattern focusing on the top left side of the page, headings, and the first few words of a sentence or list" ([PLAIN "Follow web standards"](sources/plain/guidelines/web/index.md)).

### S-SUBHEADS
**Subheadings do not help the reader find their way** · severity 2 (no subheadings in a text several screens long; playful subheadings, or ones unrelated to the title), 3 (too many; subheadings that depend on the title; a 300–600-word text without subheadings), 4 (bare topic labels) · search: script (presence and frequency), reading · sources: [PLAIN "Add useful headings"](sources/plain/guidelines/organize/add-useful-headings.md); [PLAIN "Effective headings"](sources/plain/guidelines/organize/effective-headings.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md); [PLAIN "Write short sections"](sources/plain/guidelines/concise/write-short-sections.md)

**Rule.** A text longer than about two-thirds of a screen is divided by subheadings. They come roughly every 5–10 paragraphs, are simple and informative, and together with the title tell the story.

**What goes wrong.** Without subheadings a long text is one long block that is hard to approach and in which the needed part cannot be found: "Well organized writing will still be difficult for users to follow if they can't see how it's organized" (PLAIN "Add useful headings"). Riddle subheadings make the reader spend time on the author's idea. Vague topic headings are no better: "Topic Headings such as "General," "Application," and "Scope" are so vague they may confuse the user." Subheadings that depend entirely on the title lose its modality: by the middle of the text the reader has forgotten whether it was "must" or "should". Headings that all start the same way hide their differences: when every heading began with "how to", "users could not easily find the right section because their eyes stayed on the "how to" and all the headings seemed the same" (PLAIN "Effective headings"). Too many subheadings chop the text into pieces.

**Signs.**
- More than ≈ 300 words and six paragraphs without a single subheading; a stretch of more than ≈ 10 paragraphs without one. The word thresholds are rutalk's "two-thirds of a screen" converted to words, not figures from the sources.
- A subheading over every one or two paragraphs throughout the text.
- Proverbs, puns, idioms; generic "Introduction", "Overview", "Final thoughts". GOV.UK asks for headings that are "descriptive – avoid generic headings like ‘Introduction’".
- The title and the subheadings, written out in a row, do not tell a story.
- The modality or the subject is only in the title ("Mistakes to avoid at a job interview"), while the subheadings are bare verb phrases that read as advice.
- All subheadings begin with the same words ("How to…", "Understanding…").
- In a document, paragraphs answer different questions (the basis, the substance, who is responsible, what happens next), but none is labelled.

**Not an error if:**
- the text is up to two-thirds of a screen, or borderline — about 300 words: there is no strict rule here;
- it is a section of a book or an article under its own heading and is itself below the threshold;
- bold key words at the start of paragraphs act as run-in subheadings; identical labels on parallel modules are normal;
- dependent subheadings work where the context cannot be forgotten;
- the subheadings are questions in a document readers come to with questions — PLAIN recommends them, GOV.UK bans them on its web pages (G2).

**Example.** "§ 254.11 Indian Rights / § 254.12 Applications / § 254.13 Multi-tribal grants / § 254.14 Administrative requirements / § 254.15 Appeals" — rewritten as questions such as "How do I apply for a grant under this part?" ([PLAIN "Add useful headings"](sources/plain/guidelines/organize/add-useful-headings.md)); "How to get a permit / How to fill out the permit / How to change your address" ([PLAIN "Effective headings"](sources/plain/guidelines/organize/effective-headings.md)).

### S-MODULES
**Parts do not add up to a system** · severity 2 (3 — inconsistent parallel modules; 4 — only the form of the subheadings differs) · search: reading (the script prints the block map) · sources: [PLAIN "Effective headings"](sources/plain/guidelines/organize/effective-headings.md); [PLAIN "Address separate audiences separately"](sources/plain/guidelines/audience/address-separate-audiences-separately.md); [PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md); [Strunk 15 "Express co-ordinate ideas in similar form"](sources/strunk/3-principles-of-composition.md); [Strunk 17 "In summaries, keep to one tense"](sources/strunk/3-principles-of-composition.md)

**Rule.** A long text is divided into self-contained parts by a principle that serves the reader's goal; parallel parts are built the same way.

**What goes wrong.**
- **No logic of division.** A wall of text to hack through; subheadings placed mechanically while the topics under them are mixed; division by a principle that does not serve the reader, such as chronology when the events repeat. Strunk advises a critic of several works "not to take them up singly in chronological order, but to aim from the beginning at establishing general conclusions" (Strunk 17). Material that belongs together ends up in distant sections tied by cross-references (PLAIN "Minimize cross-references"); audiences are mixed, and "By addressing different audiences in the same place, you make it harder for each audience to find the material that applies to them" (PLAIN "Address separate audiences separately"). Such a text puts readers off, and they cannot find what they need in it.
- **Inconsistent parallel modules.** Hotels, plans or products are each described in their own way, the subheadings do not match, the labels differ — the sense of order is lost and the items cannot be compared. "It takes more mental energy to switch back and forth in understanding when the structure of the headings keeps changing" (PLAIN "Effective headings"); Strunk asks that "expressions of similar content and function should be outwardly similar" (Strunk 15).
- **Modules where the text must be read straight through.** An argument or a story is cut into cards; the reader reads selectively and misses the thought.

**Signs.**
- One topic smeared across several sections; foreign topics inside a section.
- A section cannot be understood without the others; it keeps sending the reader elsewhere ("see section 4", "as described above"); the first paragraph of a section is unrelated to its subheading.
- Subheadings of one level in different grammar: a question, then a noun phrase, then a verb phrase.
- Parallel sections have different sets and orders of parts, different labels ("Atmosphere" in one, "Vibe" in another).
- Sections of a different nature (visas, money) wedged into a series of like ones.
- Instructions for different audiences mixed in one place under one "you".
- An argument cut into template cards, each leaning on the one before.

**Not an error if:**
- the text is short; the plot justifies chronology;
- the text could have been divided differently — there is no single right principle — but the chosen division serves the goal;
- parts different in nature are built differently; blocks that do not apply are left out;
- an argument has ordinary subheadings — that is not a modular structure;
- the form of the headings changes with their level: "the change from one structure to another signals a change from top level to subtopic" (PLAIN "Effective headings").

**Example.** "Do I need a permit? / Getting a permit / Filling out the permit / What if my address changes?" — "If we mix questions and verb phrases, it seems more confusing" ([PLAIN "Effective headings"](sources/plain/guidelines/organize/effective-headings.md)).

### S-INTRO
**Empty introduction** · severity 3 (4 — an interesting, well-organised text has no introduction) · search: script (phrases in the first paragraph), reading · sources: [Strunk V "One of the most", "Interesting"](sources/strunk/5-words-commonly-misused.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md); [GOV.UK "Write clear summaries"](sources/govuk/summaries.md) · classic: Minto, *The Pyramid Principle*, ch. 4 "Fine Points of Introductions"

**Rule.** An introduction does at least one job — takes the reader into the topic, reminds them of what they know, creates interest or trust — and makes clear what the text is about.

**What goes wrong.** The first paragraph is a strained claim that the topic matters, an attempt to stun with drama, or a personal story out of place. It is a prelude without which the article loses nothing: the first paragraph can be struck out at no cost. Drama can set a bad context for what follows; a story about the author raises "who are you to tell me this?". A flashy first part with no informative second part leaves the reader not knowing what the piece is about. Strunk calls the stock opening "One of the most…" "threadbare and forcible-feeble", and for "An interesting story is told of" his advice is "Tell the story without preamble" (Strunk V). GOV.UK: "Do not repeat the summary in the first paragraph."

**Signs.**
- "In today's world…", "In recent years, … has become increasingly important", "It's no secret that…", "We live in an age of…", "Since the dawn of time…", "Have you ever wondered…?".
- "One of the most important / interesting… is…" as the opening.
- "I've been meaning to write about this for a long time…".
- Shock piled up in the first paragraph.
- The substance begins only in the second paragraph.
- A striking scene with not a sentence about what the text is about.
- The first paragraph repeats the title or the summary.

**Not an error if:**
- it is a personal blog;
- the author's experience with the topic explains why they can be trusted;
- the introduction does at least one job; "This guide explains how to…" with a concrete benefit is the informative part, not filler;
- it is a short note or message (up to ≈ 150 words, rutalk's threshold converted to words) in which the first paragraph already is the point. Many readers skip introductions anyway, so the stakes are modest.

The opening phrase "in today's fast-paced world" on its own is a machine-text tell, [W-LLM](#w-llm); S-INTRO judges whether the paragraph does a job.

**Example.** "One of the most interesting developments of modern science is, etc."; "Switzerland is one of the most interesting countries of Europe." — "There is nothing wrong in this; it is simply threadbare and forcible-feeble" ([Strunk V "One of the most"](sources/strunk/5-words-commonly-misused.md)); "In connection with the anticipated visit of Mr. B. to America, it is interesting to recall that he" ([Strunk V "Interesting"](sources/strunk/5-words-commonly-misused.md)).

### S-OUTRO
**Useless conclusion** · severity 3 (4 — the formula comes after a substantive conclusion) · search: script (formulas at the end), reading · sources: [Strunk 9](sources/strunk/3-principles-of-composition.md); [Strunk 18 "Place the emphatic words of a sentence at the end"](sources/strunk/3-principles-of-composition.md); [Strunk 17](sources/strunk/3-principles-of-composition.md); [GOV.UK "Write effective links"](sources/govuk/add-links.md)

**Rule.** The conclusion consolidates the content: it turns the advice into a system, gives a cheat sheet, a "what next" or a new view of the topic.

**What goes wrong.** The conclusion repeats every point of the article, pours words around the topic, comes down to "That's all" and "Thanks for reading" — or there is none, and the article breaks off. Few readers reach the end, and to those who do, an empty ending gives nothing. The end is a prominent place: Strunk's principle "that the proper place for what is to be made most prominent is the end applies equally to the words of a sentence, to the sentences of a paragraph, and to the paragraphs of a composition" (Strunk 18).

**Signs.**
- The last paragraph restates the theses as they were, without system or conclusion: "In conclusion…", "To sum up…", "All in all…" followed by a retelling.
- General reflections without specifics.
- "Thanks for reading!", "That's all for today", "Hope this helps!", "Happy coding!", "Stay tuned".
- The text breaks off on its last substantive section.
- A module's conclusion repeats its first paragraph.
- A closing pile of links: GOV.UK asks writers not to "put all the links together at the bottom of the page" or to use "unsorted lists like ‘Further reading’ or ‘More information’" (GOV.UK "Write effective links").
- The text ends on a digression or an unimportant detail.

**Not an error if:**
- the ending is a cheat sheet, a list, a "what next", a piece of advice for the whole article, a strong image or a joke;
- the article ends with a call to share or to act;
- a sign-off stands at the end of a letter — that is not an article's conclusion. These are recommendations, not hard rules (G1).

**How the sources describe it.** For the paragraph, Strunk wants "the final sentence either emphasizes the thought of the topic sentence or states some important consequence. Ending with a digression, or with an unimportant detail, is particularly to be avoided" ([Strunk 9](sources/strunk/3-principles-of-composition.md)); for writing about several works, "an orderly discussion supported by evidence, not a summary with occasional comment" ([Strunk 17](sources/strunk/3-principles-of-composition.md)). The sources give no sample of an empty conclusion.

### S-WALL
**Wall of text** · severity 2 (the whole text or a large part of it in one block), 3 (a single long paragraph; uneven division) · search: script (length), reading · sources: [PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [PLAIN "Design for reading"](sources/plain/guidelines/design/index.md); [Strunk 8 "Make the paragraph the unit of composition"](sources/strunk/3-principles-of-composition.md)

**Rule.** The text is divided into paragraphs by topic; a paragraph is no longer than about 150 words (PLAIN) or five sentences (GOV.UK).

**What goes wrong.** Paragraphs let the reader glide through the text, decide from a paragraph's opening whether to dig in, and come back to the right place: "The beginning of each paragraph is a signal to him that a new step in the development of the subject has been reached" (Strunk 8). A solid block is one big hard text instead of many small simple ones. "Long paragraphs discourage users from even trying to understand your material" (PLAIN "Write short paragraphs"); "Dense, cluttered writing deters people from taking the time to read", and dense letters go on the "read later" pile (PLAIN "Design for reading"). Poor division shows, before a word is read, that the author is not in control of the material.

**Signs.**
- A paragraph over ≈ 150 words or more than five sentences. "Paragraphs should never be longer than 250 words" (PLAIN). On a phone screen or in a chat message, less.
- Several topics follow each other in one block, each developed over several sentences.
- Transitions are made with spoken connectives ("firstly", "next", "finally", "to sum up") instead of breaks.
- Uneven division: some thoughts in detail, others crammed.

**Not an error if:**
- a long paragraph is entirely about one topic and the excess is small — a text is divided by topic, not by length; Strunk's brief subjects are "best written in a single paragraph" (Strunk 8);
- the wording cannot be changed — legally agreed text (G5);
- it is code, a table or a quoted document. Rules about widows and orphans concern print only.

**Example.** "A specific vaccine for humans that is effective in preventing avian influenza is not yet readily available. Based upon limited data, the CDC has suggested that the anti-viral medication Oseltamivir (brand name-Tamiflu) may be effective in treating avian influenza. […]" — one block of 247 words and eight sentences on four topics, which PLAIN's rewrite splits under four headings ([PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md), "Flu Medication").

### S-PARA-LEAD
**Paragraph does not lead with the point** · severity 3 (2 — most paragraphs start this way, or the first paragraph of a letter, a news item or a proposal does; 4 — the closing sentence merely repeats the opening) · search: script (map of paragraph openings), reading · sources: [PLAIN "Have a topic sentence"](sources/plain/guidelines/organize/have-a-topic-sentence.md); [Strunk 9 "As a rule, begin each paragraph with a topic sentence"](sources/strunk/3-principles-of-composition.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md) · classic: Minto, *The Pyramid Principle*, ch. 1 "Why a Pyramid Structure?" (answer first)

**Rule.** In an informational text a paragraph opens with its main and useful point; the first sentences of consecutive paragraphs add up to a coherent story; a closing sentence adds something.

**What goes wrong.** The reader glides over paragraph openings and decides from them whether to dig in. If the first sentence is a run-up, an announcement, a connective or a generality, the reader does not learn what the paragraph is about and misses what matters. PLAIN: "If you flood readers with details first, they become impatient and may resist hearing your message"; "Don't make readers hold a lot of information in their heads before getting to the point." If the main point at the start cannot be understood without explanation, or is useless, the paragraph is not worth reading. A last sentence that repeats the first is a conclusion for decoration: the most memorable place is taken by a repeat.

**Signs.**
- The first sentence is a reflection on how hard the question is, an announcement ("In this section we will look at…", "Let's take a closer look at…"), a rhetorical question in a business text, or a generality about the subject.
- The paragraph begins with a connective or a caveat: "So, let's say…", "By the way…", "Now,…", "That said,…", "With that in mind,…".
- In an instruction the rule, the background or a term comes first, and the reader's action only in the second or third sentence.
- The first sentences of consecutive paragraphs do not make a sequential story.
- The last sentence repeats the first in the same words, often after "So…", "Thus…", "In short…".

**Not an error if:**
- the text is entertaining, or the paragraph is a kicker — the first paragraph of an article or section, meant to spark interest;
- the first sentence works for attention or as a transition, and the topic is set right after it: Strunk allows "one or more sentences of introduction or transition" before the topic sentence;
- the paragraph has no conclusion — that is normal;
- the closing sentence restates the opening in a stronger form — Strunk's model paragraph ends "in language amplified and heightened to form a strong conclusion" (Strunk 9);
- it is narrative: "The brief paragraphs of animated narrative, however, are often without even this semblance of a topic sentence" (Strunk 9).

**Example.** "Flood conditions contribute to the growth and transmission of many kinds of fungi, some of which can cause sickness. Cleanup workers are at increased risk of exposure to airborne fungi and their spores because they often handle moldy building materials, decaying vegetable matter, rotting waste material, and other fungus-contaminated debris." — the rewrite opens with what the reader must do: "Be careful when cleaning up after a flood." ([PLAIN example "Fungi Hazards and Flood Cleanup"](sources/plain/examples/fungi-hazards.md), before and after).

### S-PARA-MIX
**Paragraph without a single topic** · severity 3 (2 — stream of consciousness in an informational text) · search: reading · sources: [PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md); [Strunk 8 "Make the paragraph the unit of composition"](sources/strunk/3-principles-of-composition.md); [PLAIN "Use transition words"](sources/plain/guidelines/organize/use-transition-words.md) · classic: Pinker, *The Sense of Style*, ch. 5 "Arcs of Coherence"

**Rule.** One paragraph, one topic; its sentences are linked by logic, not by association.

**What goes wrong.**
- **A foreign topic.** The paragraph contains an alien sentence or several ideas. The reader judges the paragraph by its opening and does not expect another topic: it slips past or confuses. PLAIN: "Limit each paragraph or section to one topic to make it easier for your audience to understand your information."
- **Stream of consciousness.** Sentences follow by association — doubts, emotions, rhetorical questions. It is hard to read because every logical link has to be decoded, and the useful part is buried deep. PLAIN on links between sentences: "Being too familiar with our own material, we think they aren't needed. Readers, on the other hand, find them helpful in following our train of thought."

**Signs.**
- A sentence that cannot be assigned to the topic of the first one.
- A short paragraph of strung-together ideas; the last sentence opens a new topic.
- Pretty phrases and cute details unrelated to the topic.
- Rhetorical questions inside reasoning, "I mean", "honestly", remarks about the author's state of mind, several sentences in a row opening with "And…", "But…", "So…".
- The main point at the end of the paragraph, or never stated.

**Not an error if:**
- the first sentence is a hook and the next one sets the topic;
- the sentence develops the same topic: a cause, a consequence, an example, a piece of advice;
- it is fiction, where the stream of consciousness is deliberate (G2).

**Example.** "Notice of a bid advertisement shall be published in at least one local newspaper and in one trade publication at least 30 days in advance of sale. If applicable, the notice must identify the reservation within which the tracts to be leased are found. Specific descriptions of the tracts shall be available at the office of the superintendent. The complete text of the advertisement shall be mailed to each person listed on the appropriate agency mailing list." — two topics in one paragraph, which the rewrite splits into two ([PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md), "Cover one topic in each paragraph").

### S-LIST
**List in the wrong place** · severity 3 (2 — an argument is cut into a list and the main point depends on the links between items; 4 — no lead-in before the list) · search: script (item length and openings), reading · sources: [PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md); [GOV.UK A to Z "Bullet points and steps", "Lists"](sources/govuk/a-to-z-style-guide.md); [Strunk 15 "Express co-ordinate ideas in similar form"](sources/strunk/3-principles-of-composition.md)

**Rule.** A list carries homogeneous, independent information: short items of the same form, each following from the lead-in. Homogeneous items the reader needs to take in at once are not hidden in a solid paragraph.

**What goes wrong.** A list promises structured, homogeneous information that can be skimmed.
- **Connected text in bullets.** An argument is cut into a list, the items live their own lives, and the reader reconstructs the links alone.
- **Paragraph bullets.** When paragraph after paragraph is pushed into a list, the point of the list is lost. GOV.UK: "you do not use more than one sentence per bullet".
- **Items that do not belong.** An item breaks the pattern of the others and does not follow from the lead-in.
- **A list hidden in a paragraph.** Homogeneous properties, steps or conditions are given as a solid paragraph. The form promises connected reasoning that is not there, and how many actions there are, and which, cannot be seen at a glance. PLAIN: lists "Help readers skim and scan" and "Make it easy to identify all steps in a process".
- **Overuse.** "You can overuse lists. Remember to use them to highlight important information, not to overemphasize trivial matters" (PLAIN "Use lists").

A list squeezed into a single sentence is [P-INLINELIST](#p-inlinelist).

**Signs.**
- An item starts with a connective that points to its neighbour: "For example, if…", "Also note that…", "In addition,", "Therefore,".
- The items form a chain cause → consequence → conclusion; items are built differently; items do not fit the lead-in. PLAIN's test: "Make sure each of the bullets in a list can make a complete sentence if combined with the lead-in sentence."
- An item longer than one sentence or a couple of lines; the list is longer than the text around it.
- No lead-in line: PLAIN — "Always use a lead-in sentence to explain your lists"; GOV.UK — "you always use a lead-in line".
- A "Next steps", "Recommendations" or "Action items" paragraph written as running text with "first… second…" or "(1)… (2)…" inside.
- A paragraph of properties or conditions that could be rearranged in any order, each sentence starting the same way.
- Bullets for steps that must be done in order, or numbers where order does not matter. GOV.UK: "Use numbered steps instead of bullet points to guide a user through a process."

**Not an error if:**
- the items come from different areas but are equal and independent;
- a consequence stays inside its own item: "This will…";
- it is a numbered step-by-step instruction; three to five items of a couple of lines each are still fine;
- the items are linked by reasoning — then they belong in a paragraph; an enumeration inside a story or a description;
- a very long list of names is written as a paragraph with a lead-in, which GOV.UK allows: "‘The following countries are in the EU: Spain, France, Italy…’".

**Example.** "Medicaid: Apply if you are aged (65 years old or older), blind, or disabled and have low income and few resources. Apply if you are terminally ill and want to receive hospice services. Apply if you are aged, blind, or disabled; live in a nursing home; and have low income and limited resources. […]" — a list hidden in a paragraph ([PLAIN example "Medicaid Eligibility"](sources/plain/examples/medicaid-eligibility.md)); "You must submit: / Your application / Recommendation letter / Mail it express mail" — ""Mail it express mail" does not work with the rest of the list" ([PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md)).

### S-BURIED
**Important information buried** · severity 2 (1 — the missed detail changes the reader's actions or expectations) · search: script partly (limiters at the end of a long paragraph), reading · sources: [PLAIN "Place the main idea before exceptions and conditions"](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md); [PLAIN "Place words carefully"](sources/plain/guidelines/words/place-words-carefully.md); [GOV.UK "Create a clear structure for your content"](sources/govuk/clear-structure.md) · classic: Minto, *The Pyramid Principle*, ch. 1 "Why a Pyramid Structure?" (answer first)

**Rule.** A condition, a limitation, an exception, a deadline and other details that matter for the reader's actions stand in visible places — at the start of a paragraph, in a sentence or a paragraph of their own — and are built into the picture.

**What goes wrong.** The reader runs over headings, subheadings and paragraph openings and reads the rest on what attention is left, so whatever sits near the end of a paragraph is likely lost. GOV.UK: "The quicker you get to the point, the greater the chance your users will see the information you want them to." The detail is formally in the text, but the reader does not see it or forgets it, and draws a wrong conclusion. PLAIN: "If an exception or condition is just a few words, and seeing it first will avoid misleading users, put it at the beginning instead of the end."

**Signs.**
- Qualifiers — "except…", "unless…", "only if…", "provided that…", "subject to…", "excluding…" — in the second half of a long paragraph or in the tail of a long sentence.
- The meaning rests on one limiting word ("only", "not", "never") that is not repeated or emphasised, or stands in the wrong place: PLAIN's "you are only required to provide the following" for "you are required to provide only the following".
- A formally correct condition from which a convenient wrong conclusion is easy to draw.
- A form number, a date or a time as bare numbers the reader must remember and use.
- A key fact (who is not covered, what is not available) in the middle of a long paragraph about something else.
- Fees, cancellation terms or eligibility limits only in a footnote, in small print or in the last line ("Terms apply").

**Not an error if:**
- the nuance is secondary;
- the nuance is already set out separately, and the tail only adds detail;
- it is a law or a contract where every word matters (G2).

**Example.** "With your grant application you must submit a resume containing your undergraduate, graduate, and any other professional education, your work experience in the field of health care, and the name, and phone number of current and previous employers in the health care field, unless you have already submitted this information." ([PLAIN "Place the main idea before exceptions and conditions"](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md)); "We emphasize that this medication cannot be made available to private U.S. citizens abroad." — the fourth sentence of a 247-word paragraph about medication for government employees ([PLAIN "Write short paragraphs"](sources/plain/guidelines/concise/write-short-paragraphs.md), "Flu Medication").

### S-EXAMPLES
**Examples not set apart, or crowding out the text** · severity 3 (2 — examples take up almost all the space) · search: reading · sources: [PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md); [GOV.UK technical A to Z "code samples", "example code"](sources/govuk/technical-a-to-z.md); [GOV.UK A to Z "Quotes and speech marks"](sources/govuk/a-to-z-style-guide.md)

**Rule.** A long example is set apart from the argument; there is more main text with theses than there are examples.

**What goes wrong.** An example that is set apart sends a signal: this is an example, read it if you want to go deeper. An example running on inside a paragraph with theses turns the page into an endless wall of text. The opposite extreme is more examples than text: it is easier to skim abstract theses than to work through examples, and the reader ends up understanding little and leaves.

**Signs.**
- In a paragraph with theses, an example several sentences long, after which the paragraph goes back to the argument — with no separate paragraph, block quote or code block.
- In a section, the examples clearly outweigh the main text.
- The theses are reduced to connectives between long examples.
- A code sample, a sample letter or a quoted document set in running text without formatting.

**Not an error if:** a short example sits inside a sentence ("For example, if…"); the examples are roughly equal to the text in volume — borderline, but not yet an error.

**How the sources describe it.** PLAIN sets its regulation example apart in its own block, and inside it the example is introduced by a sentence that says what it shows: "The following example explains what it would mean for an area to be in compliance with this type of standard" ([PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md)). GOV.UK asks for code samples in "a fixed width font" ([GOV.UK technical A to Z "code samples"](sources/govuk/technical-a-to-z.md)) and for "block quotes for quotes longer than a few sentences" ([GOV.UK A to Z "Quotes and speech marks"](sources/govuk/a-to-z-style-guide.md)). The sources do not discuss examples crowding out the text; that half of the entry is carried over from rutalk.

## P — Sentence

### P-OVERLOAD
**Too many new ideas in one sentence** · severity 2 (3 — in a text for specialists the sentence goes over the limit by one idea) · search: script (long sentences), reading · sources: [PLAIN "Write short sentences"](sources/plain/guidelines/concise/write-short-sentences.md); [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md), "Keep paragraphs and sentences short"; [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md)

**Rule.** One new idea per sentence for a reader new to the subject; two if they are closely linked; up to three well-structured ones in a text for specialists.

**What goes wrong.** A new idea is meeting something unfamiliar, or two familiar things acting on each other. When a sentence introduces a concept and at once does something with it, or packs in every new entity at once, the reader has to hold all of it before the sentence closes: the words are plain, nothing is redundant, and the sentence still reads with effort. PLAIN states the rule directly: "Express only one idea in each sentence." Sentences "loaded with dependent clauses and exceptions confuse the audience by losing the main point in a forest of words" (PLAIN "Write short sentences"); "Nothing is more confusing to the user than long, complex sentences containing multiple phrases and clauses" (PLAIN "Be concise"). GOV.UK gives a working threshold: "Try to split up sentences that are over 25 words long." Numbers behave the same way: several numbers of different kinds in one sentence bury the one that matters.

**Signs.**
- Definition and action in one sentence: "X is …, which …", "X is the … to … through … and …".
- Chains of "through …", "by means of …", "as a result of …", "caused by …", "which is …".
- A row of entities new to the reader with no summarising word in front of it.
- Three or more numbers of different kinds (amounts, dates, percentages, counts) in one sentence.
- One sentence answers how, what, to whom and when at once.
- More than 25 words (GOV.UK) — a trigger to check, not an error by itself (G4).

**Not an error if:**
- the sentence lists familiar, like items, not ideas;
- the concepts are known to this audience or were introduced earlier;
- the row is preceded by a summary with a number ("three tools:");
- every number serves the purpose of the text;
- splitting would only chop one idea into a string of short sentences: Strunk 13 counts "the presentation of a single complex idea, step by step, in a series of sentences or independent clauses which might to advantage be combined into one" as a fault too (see [P-PARCEL](#p-parcel)).

**Example.** "If you take less than your entitled share of production for any month, but you pay royalties on the full volume of your entitled share in accordance with the provisions of this section, you will owe no additional royalty for that lease for prior periods when you later take more than your entitled share to balance your account." ([PLAIN "Write short sentences"](sources/plain/guidelines/concise/write-short-sentences.md); the source rewrites it as two sentences and a list.) "Mitigation is the cornerstone of emergency management. It's the ongoing effort to lessen the impact disasters have on people's lives and property through damage prevention and flood insurance." ([PLAIN example "Protect Yourself from Natural Disasters"](sources/plain/examples/natural-disasters.md))

### P-SPLIT
**Main clause broken up by details** · severity 2 · search: script (long sentences), reading · sources: [PLAIN "Keep the subject, verb, and object close together"](sources/plain/guidelines/concise/keep-the-subject-verb-and-object-close-together.md); [PLAIN "Place words carefully"](sources/plain/guidelines/words/place-words-carefully.md); [PLAIN "Place the main idea before exceptions and conditions"](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md); [PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md); [Strunk 16 "Keep related words together"](sources/strunk/3-principles-of-composition.md) · cited: Pinker, *The Sense of Style*, ch. "The Web, the Tree, and the String"

**Rule.** Subject and verb (the condition and the main action) stand together; details come after the main clause or in sentences of their own.

**What goes wrong.** Lists, qualifying phrases, conditions, provisos and references to rules stand between the main words, and the reader reads the sentence again in search of its meaning. "The natural word order of an English sentence is subject-verb-object… When you put modifiers, phrases, or clauses between two or all three of these essential parts, you make it harder for the user to understand you" (PLAIN). Strunk 16: the interposed phrase "needlessly interrupts the natural order of the main clause". An exception placed first means "The audience must absorb the exception, then the rule, and then usually has to go back to grasp the relationship between the two" (PLAIN "Place the main idea…"); a cross-reference moved to the end of the passage "is less disruptive to the user, and less annoying" (PLAIN "Minimize cross-references"). It happens when a sentence is built to say everything at once, or when the writer inserts qualifications into a finished sentence because it looks too bare.

**Signs.**
- Lists, participle phrases, chains of circumstances or parentheticals between subject and verb.
- The main clause at the very end, after a long "If …, for example, …, …", "Except as …", "Through measures such as …".
- A reference to a section, law or document in the middle of a thought: "pursuant to section …", "(see paragraph (b))", "as described in Section …".
- Stacked qualifications: "regularly, every year, without fail".
- The main verb arrives after a subject group of fifteen to twenty words or more.

**Not an error if:**
- the details have been moved to a list or to separate sentences;
- the interruption is a short relative clause or an apposition, or a deliberate periodic sentence that builds suspense (Strunk 16);
- a condition of a few words comes first because "seeing it first will avoid misleading users" (PLAIN "Place the main idea…");
- the short version only seems too bare to the author;
- an official genre is not an exception: the plain-language guidelines were written for regulations.

**Example.** "If any member of the board retires, the company, at the discretion of the board, and after notice from the chairman of the board to all the members of the board at least 30 days before executing this option, may buy, and the retiring member must sell, the member's interest in the company." ([PLAIN "Keep the subject, verb, and object close together"](sources/plain/guidelines/concise/keep-the-subject-verb-and-object-close-together.md); "In essence, the sentence says: The company may buy a retiring member's interest.") "Through measures such as, building safely within the floodplain or removing homes altogether; engineering buildings and infrastructures to withstand earthquakes: and creating and enforcing effective building codes to protect property from floods, hurricanes and other natural hazards, the impact on lives and communities is lessened." ([PLAIN example "Protect Yourself from Natural Disasters"](sources/plain/examples/natural-disasters.md))

### P-INLINELIST
**List crammed into a sentence** · severity 2 (1 — in rules, requirements or contracts the reader cannot tell whether all conditions must hold or any one is enough) · search: script partly, reading · sources: [PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md); [PLAIN "Place the main idea before exceptions and conditions"](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md); [GOV.UK A to Z "Bullet points and steps"](sources/govuk/a-to-z-style-guide.md); [PLAIN "Don't use slashes"](sources/plain/guidelines/conversational/dont-use-slashes.md)

**Rule.** An important list that the reader will check against or act on is taken out of the line, and it is clear whether all items are required or any one is enough.

**What goes wrong.** A list of documents, parties or conditions is written as one stretch of a sentence, often in the subject or the opening condition. The reader cannot tick items off. Lists "are an ideal way to present items, conditions, and exceptions" and "make it easy to identify all steps in a process" (PLAIN "Use lists"); "Use a list … if your sentence contains multiple conditions or exceptions" (PLAIN "Place the main idea…"). A long listing subject or condition hides the logic — all of them, or any one? GOV.UK: a list sometimes needs "a short phrase to clarify whether all or some of the points apply", and "The number and type of examples in a list may lead the user to believe the list is exhaustive." "And/or" pushes the decision onto the reader (PLAIN "Don't use slashes"). Trying to cover everyone adds needless detail.

**Signs.**
- Three to five developed, like items in one sentence, each with its own proviso: "if applicable, …", "if you have already paid".
- The list sits in the subject or the opening condition: "Employees, contractors, visitors and other persons …", "If a …, or a …, or …, the …".
- Tails: "as well as", "and other …", "or any part thereof", "including but not limited to", "etc.", "and/or".
- Conditions joined by "and" and "or" in the same run, with no word saying whether all or any apply.

**Not an error if:** the list is set out as a list; a short list of simple items comes after the main clause; the reader does not need to check against it.

**Example.** "Each completed well drilling application must contain a detailed statement including the following information: the depth of the well, the casing and cementing program, the circulation media (mud, air, foam, etc.), the expected depth and thickness of fresh water zones, and well site layout and design." ([PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md)) "If a deponent fails to answer a question propounded, or a party upon whom a request is made under § 4.70, or a party on whom interrogatories are served fails to adequately respond or objects to the request, or any part thereof, or fails to permit inspection as requested, the discovering party may move the administrative law judge for an order compelling a response or inspection in accordance with the request." ([PLAIN example "Wordiness Made Spare"](sources/plain/examples/wordiness.md))

### P-NESTED
**Clause inside a clause** · severity 3 (2 — the main point drowns in a chain of subordinate clauses, or an exception contains another exception; 4 — a single short reported clause such as "we believe that …") · search: script + check · sources: [PLAIN "Write short sentences"](sources/plain/guidelines/concise/write-short-sentences.md); [PLAIN "Use positive language"](sources/plain/guidelines/concise/use-positive-language.md), "Avoid exceptions to exceptions"; [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md) · cited: Pinker, *The Sense of Style*, ch. "The Web, the Tree, and the String"

**Rule.** A sentence has no more than one level of subordination; reported speech and opinion do not push the point into an extra subordinate clause.

**What goes wrong.** A complex sentence is normal; a subordinate clause that contains another one makes the reader hold too much at once. "Sentences loaded with dependent clauses and exceptions confuse the audience" (PLAIN). An exception inside an exception "is just another form of a double negative. That makes it even harder for the user to puzzle out" (PLAIN "Use positive language"). Superfluous subordination puts a clause where one noun would do: Strunk 13 turns "the fact that he had not succeeded" into "his failure". Reporting and thinking verbs — "said that", "we believe that", "I would like you to" — move the substance down a level.

**Signs.**
- A subordinate clause that depends on another: "which … although …", "that … which … if …", "if …, then …, because …".
- Exceptions inside exceptions: "except …, unless …", "other than …, provided that …".
- "The fact that", "the way in which", "the reason why … is that" as subject or object.
- "We believe that …", "It is expected that …", "The spokesperson said that …" in front of the substance.

**Not an error if:**
- the sentence has one level of subordination;
- it is direct speech in quotation marks;
- the reporting is itself the point (who said it matters to the story);
- it is a short sentence with one simple subordinate clause.

**Example.** "This form will be used by Federal agencies to obtain applicant certification that States which have established a review and comment procedure in response to Executive Order 12372 and have selected the program to be included in their process, have been given an opportunity to review the applicant's submission." ([PLAIN example "Application for Federal Assistance"](sources/plain/examples/application-federal-assistance.md)) "Applicants may be granted a permit to prospect for geothermal resources on any federal lands except lands in the National Park System, unless the applicant holds valid existing rights to the geothermal resources on the National Park System lands listed in the application." ([PLAIN "Use positive language"](sources/plain/guidelines/concise/use-positive-language.md))

### P-GLUED
**Run-on sentence or comma splice** · severity 3 (4 — the parts are related; splitting would only make reading easier) · search: script partly, reading · sources: [Strunk 5 "Do not join independent clauses by a comma"](sources/strunk/2-elementary-rules-of-usage.md); [Strunk 14 "Avoid a succession of loose sentences"](sources/strunk/3-principles-of-composition.md); [Strunk V "While", "But"](sources/strunk/5-words-commonly-misused.md); [GOV.UK A to Z "semicolons"](sources/govuk/a-to-z-style-guide.md)

**Rule.** Independent sentences that stand well on their own are not glued together with a comma or a stock connective.

**What goes wrong.** Complete sentences are joined by a comma with no conjunction (comma splice) or strung together with "and", "but", "so", "while" (run-on), and the more joints, the harder the reading. Worst of all when the parts are barely related — the first is about one thing, the second about another — and the sentence reads as assembled mechanically. Strunk 14 calls a paragraph of such sentences weak "because of the structure of its sentences, with their mechanical symmetry and sing-song". Strunk V "While": writers use it "as a substitute for and or but, either from a mere desire to vary the connective, or from uncertainty which of the two connectives is the more appropriate". GOV.UK prefers separate sentences even to semicolons: "Long sentences using semicolons should be broken up into separate sentences instead." Strunk 5 is the rule against the comma splice itself: clauses "grammatically complete and not joined by a conjunction" take a semicolon or a full stop, not a comma.

**Signs.**
- Two parts, each with its own subject and verb, joined by a comma only: "…, our clients are …", "…, we also offer …".
- The subject changes at the joint.
- "and", "but", "so", "while" joining clauses about different things; "while" used for "and" or "but".
- One "but" answering another: a contrast to a contrast (Strunk V "But").
- A chain of imperatives joined by commas.
- A paragraph made of "X, and Y" sentences one after another.

**Not an error if:** the clauses are very short and alike in form ("Man proposes, God disposes." — Strunk 5); both parts are about one subject and the second continues the first; the parts describe one scene; a colon introduces an explanation of the first part; "while" means "during the time that", or "although" without ambiguity (Strunk V "While"); it is a single compound sentence — Strunk 14 says single sentences of this type "may be unexceptionable".

**Example.** "The third concert of the subscription series was given last evening, and a large audience was in attendance. Mr. Edward Appleton was the soloist, and the Boston Symphony Orchestra furnished the instrumental music." ([Strunk 14](sources/strunk/3-principles-of-composition.md)) "The office and salesrooms are on the ground floor, while the rest of the building is devoted to manufacturing." ([Strunk V "While"](sources/strunk/5-words-commonly-misused.md))

### P-INACTION
**No action: abstract subject, state verb** · severity 3 (2 — a whole paragraph is built this way and it is unclear who does what) · search: script (state verbs) + check · sources: [PLAIN "Keep it conversational"](sources/plain/guidelines/conversational/index.md); [PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md); [PLAIN example "Register a Pesticide"](sources/plain/examples/register-pesticide.md); [Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md); [GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md) · cited: Williams, *Style: Lessons in Clarity and Grace*, lessons "Actions" and "Characters"

**Rule.** When someone acts in the sentence, the actor is the subject and the action is the verb: "someone + does + something" — Williams' characters as subjects, actions as verbs.

**What goes wrong.** The subject is an abstraction, a nominalisation or "the system", and the verb is a state verb: "is", "has", "includes", "provides", "allows". Sometimes such verbs mean nothing, sometimes they hide the action. The real actors sit in prepositional phrases or are not named at all. PLAIN: "Verbs tell your audience what to do. Make sure it's clear who does what." The reader gets a still life instead of a film and has to work out who does what; a reader new to the subject is the first to give up. Strunk 10 shows such a frame — "The reason that he left college was that his health became impaired" — collapsing into one active verb.

**Signs.**
- A subject ending in -tion, -ment, -ance, -ity, -ness, -ing, or "process", "system", "approach", "framework", "implementation", "availability".
- A state verb as predicate: "is", "are", "exists", "has", "includes", "involves", "consists of", "constitutes", "represents", "serves as", "provides", "allows", "enables", "ensures", "results in", "leads to", "takes place", "is responsible for", "is available".
- Frames: "One of the goals of X is …", "Our main advantage is …", "The reason … is that …", "X is characterized by …".
- An organisation, office or place as subject with a state verb: "Facilities … are available", "The department has …".
- The action is implied but there is no verb for it; the actor appears only after "by", "of", "for".

**Not an error if:**
- nothing happens: a state, a property or a result is described;
- it is a judgement after the actions have already been shown;
- the actor is obvious and unimportant, and the outcome is the point (GOV.UK allows the passive for this — see [W-PASSIVE](#w-passive));
- the subject is the real actor and the verb its action; whether it is the right actor is [P-FOCUS](#p-focus);
- a single hidden verb inside an otherwise active sentence — that is [W-NOMINAL](#w-nominal); P-INACTION is the sentence's skeleton, subject plus verb;
- the text is for specialists who read these nouns as the names of known operations, or vagueness is intended; there is no quota of "strong verbs" (G4);
- a frame such as "one of my tasks was to …" introduces a concrete action of a person.

**Example.** "EPA's review of this application includes assessment of the hazards to human health and the environment that may be posed by the pesticide." ([PLAIN example "Register a Pesticide"](sources/plain/examples/register-pesticide.md)) "Facilities in regional and district offices are available to the public during normal business hours for requesting copies of agency records." ([PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md)) "The reason that he left college was that his health became impaired." ([Strunk 10](sources/strunk/3-principles-of-composition.md); rewritten there as "Failing health compelled him to leave college.")

### P-FOCUS
**Wrong character in focus** · severity 3 · search: reading · sources: [Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md), "Use the active voice"; [GOV.UK "Use the right tone"](sources/govuk/right-tone.md), "Address the user directly" · cited: Williams, *Style*, lessons "Characters" and "Cohesion and Coherence"

**Rule.** The subject is the character on whom, given the purpose of the text, the reader's attention should rest.

**What goes wrong.** The subject draws attention to itself. Strunk 10 gives one fact in two forms — "The dramatists of the Restoration are little esteemed to-day" and "Modern readers have little esteem for the dramatists of the Restoration" — and says the first belongs in a paragraph about the dramatists, the second in one about readers' tastes: "The need of making a particular word the subject of the sentence will often … determine which voice is to be used." Put "we" or the organisation into the subject of a text that is about the user, and the text becomes about the organisation. GOV.UK keeps the passive available for exactly this: "when the writing is more user-centred". The issue is less grammar than steering the reader's attention. Often it is overcorrection: actors placed mechanically into every subject without asking what the text is about.

**Signs.** In a text for customers or users, nearly every subject is "we", "our team" or the organisation's name, and the reader appears only as an object; an obvious actor is made the subject of a text that is about the result.

**Not an error if:** the story really is about these actors; "we" appears, but the reader and their task stay at the centre; the text is the organisation's report on its own work.

**Example.** "The Home Office will tell you what you need to do when you apply" — GOV.UK gives it as the less user-centred version of "You'll be told what you need to do when you apply" ([GOV.UK "Use clear language"](sources/govuk/clear-language.md)).

### P-CLUMSY
**Sentence that trips the reader** · severity 3 (2 — the knots hide the point or allow a wrong reading; 4 — a single mechanical slip) · search: reading aloud; the script flags long sentences · sources: [Strunk 16 "Keep related words together"](sources/strunk/3-principles-of-composition.md); [Strunk 15 "Express co-ordinate ideas in similar form"](sources/strunk/3-principles-of-composition.md); [PLAIN "Place words carefully"](sources/plain/guidelines/words/place-words-carefully.md); [PLAIN "Use positive language"](sources/plain/guidelines/concise/use-positive-language.md); [Strunk V "But", "Participle for verbal noun"](sources/strunk/5-words-commonly-misused.md) · cited: Pinker, *The Sense of Style*, ch. "The Web, the Tree, and the String"

**Rule.** The sentence sounds like natural speech and can be read aloud in one breath, without going back.

**What goes wrong.** The words are poorly linked and the sentence stumbles: a modifier far from its word, like ideas in unlike forms, double negatives, a long parenthesis in the middle, time and place tacked on after the action. "Sloppy word placement can cause ambiguity" (PLAIN "Place words carefully"); a double negative requires "a mental switch from no to yes" (PLAIN "Use positive language", quoting Flesch); like ideas in unlike forms give "the impression that the writer is undecided or timid" (Strunk 15). The reader wades through and loses the point, and tangled syntax also hides errors of logic: once it is simplified, problems with the meaning show. If a thought can be said simply, it must not be made complicated.

**Signs.**
- A limiting word away from what it limits: "only", "just", "always", "not all" — "you are only required to provide the following" (PLAIN).
- A modifier that attaches to the wrong word and allows a second reading.
- Like ideas in unlike forms: "both a long ceremony and very tedious" (Strunk 15); list items that do not continue the lead-in (PLAIN "Use lists").
- Double negatives and negatives with negative words: "no … in the absence of", "not … unless", "may not … until", "not uncommon", "fail to … not".
- A long parenthesis or relative clause in mid-sentence; time, place and occasion strung after the action.
- Stacked "of the … of the … of the …".
- One "but" answering another; "the reason is because".
- An opening participle phrase whose implied actor is not the subject of the sentence (dangling modifier).
- The sentence cannot be read aloud in one breath: you lose the intonation.

**Not an error if:** it sounds natural read aloud; it is plain conversational speech; the thought is complex, not its expression; the negative is a real denial or antithesis — Strunk 11: "The antithesis of negative and positive is strong". If the harm is "what does this or it refer to?", the code is [P-REFERENT](#p-referent).

**Example.** "Major R. E. Joyce will give a lecture on Tuesday evening in Bailey Hall, to which the public is invited, on 'My Experiences in Mesopotamia' at eight P. M." ([Strunk 16](sources/strunk/3-principles-of-composition.md)) "No approval of any noise compatibility program, or any portion of a program, may be implied in the absence of the agency's express approval." ([PLAIN "Use positive language"](sources/plain/guidelines/concise/use-positive-language.md)) "If you are determined to have a disability, we will pay you the following:" ([PLAIN "Place words carefully"](sources/plain/guidelines/words/place-words-carefully.md))

### P-PARCEL
**Sentence fragments** · severity 3 (4 — a single case) · search: script + check · sources: [Strunk 6 "Do not break sentences in two"](sources/strunk/2-elementary-rules-of-usage.md); [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md); [GOV.UK A to Z "Bullet points and steps"](sources/govuk/a-to-z-style-guide.md)

**Rule.** In an informational text every sentence is complete and makes sense without its neighbours.

**What goes wrong.** A sentence is cut by full stops at arbitrary points, or a paragraph is a chain of incomplete sentences. It is a device of fiction and advertising; in an informational text it gives too many pauses and unnaturally broken phrases, and the reader has to stitch the pieces back together.

**Signs.** A sentence starting with "Which", "Who", "Because", "Or", "Plus", "Like" with no main clause of its own; a series of short fragments in a row; a phrase that means nothing out of context; verbless sentences outside headings and lists.

**Not an error if:** fiction; a single emotional beat followed by complete sentences, where the emphasis is warranted ("Again and again he called out. No reply." — Strunk 6); a short sentence that is complete in meaning; list items and headings — GOV.UK bullets are phrases that run on from the lead-in line; a one-word answer in a question-and-answer format; labels and captions.

**Example.** "I met them on a Cunard liner several years ago. Coming home from Liverpool to New York." "He was an interesting talker. A man who had traveled all over the world and lived in half a dozen countries." ([Strunk 6](sources/strunk/2-elementary-rules-of-usage.md): "In both these examples, the first period should be replaced by a comma.")

### P-SYNONYMS
**Elegant variation and needless repetition** · severity 4 (3 — a long row or several rows in a paragraph, or a varied term makes the reader wonder whether it is the same thing) · search: reading · sources: [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md), "Omit redundant words" and "Avoid doublets and triplets"; [PLAIN "Use the same terms consistently"](sources/plain/guidelines/words/use-the-same-terms-consistently.md); [Strunk 15 "Express co-ordinate ideas in similar form"](sources/strunk/3-principles-of-composition.md) · cited: Fowler, *A Dictionary of Modern English Usage*, "elegant variation"

**Rule.** Every word in a row of like items adds a distinction that matters to the reader; one thing keeps one name throughout the text.

**What goes wrong.** Two faults with one root: to the writer different words carry different shades, to the reader they are the same thing. Doublets, triplets and redundancy repeat one thought in several words — "English writers love to repeat the same concept by using different words that say the same thing" (PLAIN "Be concise") — and a row slows reading, because the reader has to take in and remember all of it. The writer who knows the subject well falls into this most easily. Elegant variation (Fowler) is the opposite move: the writer renames a thing to avoid repeating a word, and the reader wonders whether it is a different thing. "Using a different term may cause the reader to wonder if you're referring to the same group"; "You don't need to use synonyms to make your writing more interesting" (PLAIN "Use the same terms consistently"). Strunk 15 traces the habit to "a mistaken belief that he should constantly vary the form of his expressions".

**Signs.**
- Doublets and triplets: "due and payable", "cease and desist", "knowledge and information", "begin and commence" (PLAIN), "null and void", "each and every", "first and foremost", "full and complete", "any and all".
- Redundant modifiers: "joint" with "together", "close proximity", "successfully complete", "time period" (PLAIN "Use simple words and phrases"), "end result", "future plans", "past history".
- Rows of near-synonymous evaluative adjectives or adverbs.
- One object under several names in one text: "users", "customers", "clients", "account holders"; "the service", "the platform", "the tool"; "senior citizens", "the elderly", "the aged" (PLAIN).

**Not an error if:**
- the items differ in meaning and each carries information;
- for this audience they are different things (specialists who distinguish "error", "fault" and "failure");
- specific objects are listed;
- the same term is repeated for the same thing — that is the plain-language rule, not a fault;
- the form is varied on purpose to repeat a statement for emphasis (Strunk 15 allows this).

Do not delete mechanically — see [M-ROBOT](#m-robot).

**Example.** "The X Department and the Y Department worked together on a joint project to improve..." ([PLAIN "Be concise"](sources/plain/guidelines/concise/index.md): "'Joint' and 'together' are redundant."); "due and payable", "cease and desist", "begin and commence" (same source, "Avoid doublets and triplets"). For elegant variation PLAIN names the terms: a group called "senior citizens", then "the elderly" or "the aged" ([PLAIN "Use the same terms consistently"](sources/plain/guidelines/words/use-the-same-terms-consistently.md)).

### P-EXPLETIVE
**Empty opener: "there is", "it is … that"** · severity 3 (4 — a single opener in an otherwise direct text) · search: script + check · sources: [Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md); [Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md); [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md); [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md); [PLAIN example "Printer Recommendations"](sources/plain/examples/printer-recommendations.md)

*Added by entalk, not from rutalk; not measured.*

**Rule.** The sentence starts with its real subject; "there is/are" and "it is … that/to" are used only when nothing shorter carries the meaning.

**What goes wrong.** An expletive frame puts an empty "there" or "it" in the subject slot and pushes the real subject and action back. The sentence gets longer, the main word loses its place, and often the actor disappears ("it is recommended that"). Strunk 10 calls "there is" a "perfunctory expression" that a verb in the active voice can replace; PLAIN's word list says to omit "it is", "there is" and "there are"; Strunk 13 lists "there is no doubt but that", "he is a man who" and "this is a subject which" among needless words.

**Signs.**
- "There is/are/was/were/will be … that/who/which …"; "There is no doubt that"; "There is a need to/for".
- "It is + adjective + that/to": "It is important/essential/necessary/critical/possible that …", "It is important to …".
- "It is + past participle + that": "It is recommended/required/expected/believed/assumed that …".
- "X is a … who/which …": "he is a man who", "this is a subject which" (Strunk 13).
- A pseudo-cleft or cleft that only delays, with no contrast: "What we need to do is …", "It is … that …".

**Not an error if:**
- "there is/are" states that something exists or introduces it, and there is no shorter way; a lead-in line to a list ("There are 3 ways to …:");
- "it" refers to a real antecedent (if that antecedent is unclear, see [P-REFERENT](#p-referent));
- a cleft deliberately moves a contrasted element into an emphatic position — Strunk 18: the end and the beginning are the prominent places in a sentence;
- weather and time: "it is raining", "it is late";
- the opening phrase can be deleted whole and the rest is a complete sentence with the same meaning ("it should be noted that", "it is worth noting that"): that is a filler announcement, [W-INTRO](#w-intro). P-EXPLETIVE is the frame that forces the sentence to be rebuilt to bring the real subject forward;
- the harm is the hidden actor rather than the empty frame ("it is required that"): [W-PASSIVE](#w-passive).

**Example.** "There were a great number of dead leaves lying on the ground." ([Strunk 10](sources/strunk/3-principles-of-composition.md); "Dead leaves covered the ground.") "There is a general agreement among those who have enjoyed the experience that surf-riding is productive of great exhilaration." ([Strunk 12](sources/strunk/3-principles-of-composition.md)) "For local PC printing, it is recommended that you use a high-resolution laser or wax-transfer type printer for color reproductions, and that the printer have at least 1 MB of memory." ([PLAIN example "Printer Recommendations"](sources/plain/examples/printer-recommendations.md))

### P-REFERENT
**Pronoun without a clear referent** · severity 3 (2 — the wrong reading changes who must act, which condition applies or which object is meant) · search: script + check · sources: [PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md); [PLAIN example "Ambiguous Wording Rewritten"](sources/plain/examples/ambiguity.md); [Strunk 16 "Keep related words together"](sources/strunk/3-principles-of-composition.md); [PLAIN "Use transition words"](sources/plain/guidelines/organize/use-transition-words.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md), "Make it clear who has written the content"

*Added by entalk, not from rutalk; not measured.*

**Rule.** Every pronoun — "it", "they", "this", "that", "which", "we", "you" — points to one noun that the reader can name without going back.

**What goes wrong.** "Make sure you use pronouns that clearly refer to a specific noun. If a pronoun could refer to more than one person or object in a sentence, repeat the name of the person or object or rewrite the sentence" (PLAIN "Address the user"). The reader stops, reads back and picks a referent — sometimes the wrong one; in rules and specifications the wrong pick changes who does what. Strunk 16: "The relative pronoun should come, as a rule, immediately after its antecedent." Pointing words work when they "refer directly to something already mentioned" (PLAIN "Use transition words"); a bare "This" after a paragraph with several ideas leaves the reader to guess which one. "We" before the organisation is named: "Do not assume the audience will know who the 'we' is" (GOV.UK). "You" in a text for several audiences: PLAIN asks to define "you" in each context.

**Signs.**
- A sentence starting with a bare "This", "That", "These", "Those" or "It" directly followed by a verb ("This means", "This allows", "This is why", "It also …") after a sentence or paragraph with more than one candidate.
- "it", "they", "he or she", "the former", "the latter" with two nouns of the same number before it.
- "which" or "that" after a phrase with several nouns ("… for … caused by … that …"), or after a whole clause.
- "we", "our", "us" before the organisation has been named; "you" in a text that addresses several roles.
- "the above", "the same", "said", "such" pointing back across a paragraph.

**Not an error if:** there is only one candidate; the pronoun comes with a noun that echoes the referent ("this process", "these errors"); the referent is the immediately preceding noun and the only sensible one; "we" in the organisation's own pages where it is obvious who "we" is (GOV.UK); "it" in a fixed expression. If the harm is not "what does it refer to?" but a sentence that stumbles in general, the code is [P-CLUMSY](#p-clumsy).

**Example.** "After the Administrator appoints an Assistant Administrator, he or she must..." ([PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md)) "This rule proposes the Spring/Summer subsistence harvest regulations in Alaska for migratory birds that expire on August 31, 2003." ([PLAIN example "Ambiguous Wording Rewritten"](sources/plain/examples/ambiguity.md)) "This is a portrait of Benjamin Harrison, grandson of William Henry Harrison, who became President in 1889." ([Strunk 16](sources/strunk/3-principles-of-composition.md))

---

## W — Words

### W-INTRO
**Hedges and filler** · severity 4 (3 — a cluster of hedges; a hedge that turns a requirement into a suggestion; "by the way" in front of a glued-on promotion; important content in parentheses) · search: script + check · sources: [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md), "Cut excess modifiers"; [PLAIN "Choose your words carefully"](sources/plain/guidelines/words/index.md); [Strunk 11 "Put statements in positive form"](sources/strunk/3-principles-of-composition.md); [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md); [Strunk V "Interesting", "Kind of", "Case"](sources/strunk/5-words-commonly-misused.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md) · cited: Zinsser, *On Writing Well*, ch. "Clutter"; Orwell, "Politics and the English Language", rule 3; Pinker, *The Sense of Style*, ch. "A Window onto the World"

**Rule.** The text has no words or asides that can be deleted without loss of meaning.

**What goes wrong.** Hedges and filler give no useful information, take space on the page and pull attention from the point. Each kind has its own harm. Hedges make the writer sound unsure — Strunk 11: "Make definite assertions. Avoid tame, colorless, hesitating, non-committal language." Announcements tell the reader to pay attention instead of giving something worth it — Strunk V "Interesting": "Instead of announcing that what you are about to tell is interesting, make it so"; GOV.UK: "There's usually no need to say 'please' or 'please note'." Fillers such as "actually", "really", "quite", "totally" are "probably not necessary and may even be nonsensical" (PLAIN). "The fact that" "should be revised out of every sentence in which it occurs" (Strunk 13). "By the way" glues an unrelated piece onto the text, often an advert. Parentheses signal that their content is unimportant, even when it is important. A cluster of hedges makes a sentence heavy and hard to read aloud.

**Signs.**
- Hedges and fillers set off by commas or at the start of a sentence: "basically", "essentially", "actually", "in fact", "really", "literally" (not literal), "just", "simply", "quite", "rather", "somewhat", "fairly", "pretty", "kind of", "sort of", "a bit", "more or less", "in a sense", "to some extent", "arguably", "perhaps", "possibly", "it seems that", "it appears that", "generally", "typically", "as such", "in terms of", "with regard to".
- Announcements: "it should be noted that", "it is worth noting that", "it is important to note that", "it is interesting to note that", "note that", "please note", "I would like to point out that", "as mentioned above", "as stated earlier".
- Strunk's needless phrases: "the fact that", "the question as to whether", "in many cases", "it has rarely been the case that".
- "By the way", "Incidentally" in front of a recommendation of one's own product.
- Parentheses holding a hedge or an important part of the message.

**Not an error if:**
- without the word the meaning changes ("in fact" contrasting a fact with a belief; "generally" marking a real exception);
- the word does real work rather than padding: "just" meaning "only" or "a moment ago", "actually" contrasting the actual with the planned;
- a hypothetical has to be marked as an example: PLAIN recommends writing out "for example" and opens a split condition with "Suppose" ("Use examples", "Write short sentences");
- "first", "second", "finally", "however", "therefore" and other explicit connectives — PLAIN recommends them ("Use transition words");
- real uncertainty is stated once where the reader needs it (a forecast, an unconfirmed fact) — that is honesty, not a hedge;
- the frame cannot simply be deleted and the sentence has to be rebuilt to bring the subject forward — that is [P-EXPLETIVE](#p-expletive).

**Example.** "There is no escaping the fact that it is considered very important to note that a number of various available applicable studies ipso facto have generally identified the fact that additional appropriate nocturnal employment could usually keep juvenile adolescents off thoroughfares during the night hours, including but not limited to the time prior to midnight on weeknights and/or 2 a.m. on weekends." (Kathy McGinty's parody, quoted in [PLAIN "Choose your words carefully"](sources/plain/guidelines/words/index.md); the original: "More night jobs would keep youths off the streets.") "In connection with the anticipated visit of Mr. B. to America, it is interesting to recall that he" ([Strunk V "Interesting"](sources/strunk/5-words-commonly-misused.md))

### W-PROP
**Prop instead of an argument** · severity 3 (2 — used to present a disputed or unknown claim) · search: script + check · sources: [Strunk V "Fact", "Certainly"](sources/strunk/5-words-commonly-misused.md); [Strunk 13 "Omit needless words"](sources/strunk/3-principles-of-composition.md)

**Rule.** A claim rests on facts and reasons, not on an appeal to common knowledge, to the author's opinion or to the author's honesty.

**What goes wrong.** "As everyone knows", "it's no secret", "obviously" are a trap: if the fact really is known, there is no need to write it; if it is not known but is presented as known, the statement becomes untrue — and the reader who did not know it feels slow. "In my opinion" sounds unconvincing: everything the author writes is the author's opinion by default. "To be honest" invites the question whether the rest was dishonest. Strunk V draws the same line from another side: "fact" is for "matters of a kind capable of direct verification, not of matters of judgment", so "the fact is that" in front of a judgement props it up with a word; "certainly" is used "to intensify any and every statement".

**Signs.** "obviously", "clearly", "of course", "naturally", "needless to say", "it goes without saying", "as everyone knows", "as we all know", "it is well known that", "it's no secret that", "everyone agrees that", "undoubtedly", "there is no doubt that", "certainly", "the fact is that", "it is a fact that"; "in my opinion", "I believe", "I think", "I feel", "personally", "from my point of view"; "honestly", "frankly", "to be honest", "truth be told", "I have to say" — especially in front of a disputed claim, a stereotype or a generalisation with no source.

**Not an error if:** the author sets their own view against someone else's ("the survey found …, but in my view …"); "clearly" or "obviously" is an adverb of manner ("label it clearly"); "of course" answers a question in dialogue; "I think" marks a guess as a guess, once, in a genre of personal opinion.

**How the sources describe it.** The sources in `sources/` have no entry on "obviously" or "as everyone knows". The nearest are Strunk V "Fact" — only verifiable matters are facts; a judgement, "however incontestable", is not — and "Certainly", a mannerism that intensifies "any and every statement". The rest of the substance is carried over from rutalk's W-PROP.

### W-POLITE
**Fake politeness** · severity 3 · search: script (two or more formulas in one block) + check · sources: [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [GOV.UK A to Z "please"](sources/govuk/a-to-z-style-guide.md); [Strunk V "Thanking You in Advance"](sources/strunk/5-words-commonly-misused.md); [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md)

**Rule.** Politeness shows as care for the reader: a request says why it is needed, by when, with what, and where to get help.

**What goes wrong.** Many politeness formulas and no care: politeness becomes ritual, and the writer has done nothing to make the reader's job easier. Formality is mistaken for respect, but respect is in real care, not in words. GOV.UK: "There's usually no need to say 'please' or 'please note'. This includes when giving an instruction or explaining what a user needs to do"; its tone is "incisive (friendliness can lead to a lack of precision and unnecessary words) – but remain human", written "with the authority of someone who can actively help". Strunk on "Thanking You in Advance": "This sounds as if the writer meant, 'It will not be worth my while to write to you again.'"

**Signs.** Two or more of: "please" (repeated), "kindly", "we would be grateful if you could", "if it's not too much trouble", "if you don't mind", "sorry to bother you", "thank you in advance", "thanks in advance", "at your earliest convenience", "please do not hesitate to contact us", "should you have any questions", "thank you for your patience and understanding", "I hope this email finds you well" — in a short request that does not say why it is needed, why it is urgent, where to find the document or whom to contact.

**Not an error if:** the text shows real care — a reason, a deadline, the materials, a named contact — and then one "please" is fine; PLAIN even prefers "please" to "it is requested" or "addressees are requested"; greetings and sign-offs.

**Example.** "Please contact us" (GOV.UK gives it as a case of the "please" that is usually not needed, [GOV.UK "Use the right tone"](sources/govuk/right-tone.md)); "Thanking You in Advance" ([Strunk V](sources/strunk/5-words-commonly-misused.md)).

### W-EVAL
**Evaluation instead of a fact** · severity 3 · search: script + check · sources: [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md) ("easy", "quick", "simple"); [Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md); [Strunk V "Effect", "Worth while", "Clever"](sources/strunk/5-words-commonly-misused.md); [PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md) · cited: Orwell, "Politics and the English Language", "meaningless words"

**Rule.** A property is shown by facts from which the reader can judge for themselves.

**What goes wrong.** The writer names a thing by their own impression — "excellent", "effective", "high-quality" — and gives nothing the reader could judge by. Someone else's evaluation is empty sound to the reader: it neither informs nor builds trust, and to a sceptical reader it reads as need and insecurity. GOV.UK's tone is "emotionless – adjectives can be subjective and make the text sound more emotive and like spin". Strunk 12: "Prefer the specific to the general, the definite to the vague, the concrete to the abstract"; Strunk V on a vague evaluative "effect": "The writer who has a definite meaning to express will not take refuge in such vagueness." Evaluations of the reader's own task fail in a particular way: "easy", "simple", "quick" "can demoralise users if they do not find it" so (GOV.UK technical). Grand words do the same and also deprive the reader of reaching the conclusion themselves. Scare quotes are an evaluation too, and the author's tone in them is unclear.

**Signs.**
- Subjective adjectives and adverbs: "excellent", "outstanding", "amazing", "great", "high-quality", "effective", "efficient", "powerful", "innovative", "unique", "unforgettable", "perfectly", "instantly", "beautifully"; negative: "terrible", "awful", "horrible".
- Superiority built into the word: "world-class", "best-in-class", "state-of-the-art", "unparalleled", "unrivalled", "second to none".
- Evaluation in the name of a person or thing: "experts", "masters of their craft", "premium", "deluxe".
- Figurative adjectives: "crazy discounts", "flexible pricing".
- An abstract property nobody unpacks: "reliability", "quality", "sustainability", "durability".
- Grand words on an ordinary subject: "dramatic", "fundamental", "revolutionary", "unprecedented", "game-changing".
- "easy", "easily", "simple", "simply", "quick", "quickly", "effortless" about what the reader has to do.
- Vague approval: "nice", "interesting", "clever", "worth while", "a charming effect" (Strunk V).
- Scare quotes around an ordinary word to mock it.

**Not an error if:**
- the adjective states an objective, checkable property: "red", "steel", "free", "open-source";
- the evaluation is backed, in the same or the next sentence, by a fact or scenario the reader understands;
- it is honestly marked as the author's own opinion or feeling and not passed off as a property of the thing or as general opinion;
- the author reports other people's reaction as a fact, with its source;
- the pathos is deliberate and playful;
- quotation marks mark a name, a quotation, direct speech or a word discussed as a word;
- the evaluation is turned up by an intensifier ([W-INTENS](#w-intens)), is a jab at the reader ([M-OFFEND](#m-offend)), or is one of the machine-text tells ("seamless", "robust" — [W-LLM](#w-llm)).

**Example.** "The Open Door Initiative is a program based on a simple and fresh attitude: that the CMS desires to better hear and interact with those beneficiaries, providers, and other stakeholders interested in the delivery of quality healthcare for our nation's seniors and beneficiaries with disabilities." ([PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md)) "He showed satisfaction as he took possession of his well-earned reward." ([Strunk 12](sources/strunk/3-principles-of-composition.md); "He grinned as he pocketed the coin.") "His books are not worth while." ([Strunk V "Worth while"](sources/strunk/5-words-commonly-misused.md))

### W-INTENS
**Intensifier** · severity 3 (4 — a single intensifier in a neutral text) · search: script + check · sources: [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md), "Cut excess modifiers"; [Strunk V "Very", "So", "Certainly", "Literal, literally", "Lose out"](sources/strunk/5-words-commonly-misused.md) · cited: Zinsser, *On Writing Well*, ch. "Bits & Pieces"; Pinker, *The Sense of Style*, ch. "A Window onto the World"

**Rule.** Importance is shown by evidence, not by a word that turns up the evaluation.

**What goes wrong.** An intensifier is an evaluation laid on top of another evaluation: it pulls attention to itself, and the main word becomes secondary. To the reader it signals that the author is trying very hard to persuade; without proof it is nothing, and a person or product does not become more genuine for being called genuine. PLAIN: modifiers such as "absolutely", "completely", "really", "totally" and "very" are "probably not necessary and may even be nonsensical". Strunk V "Very": "Use this word sparingly. Where emphasis is necessary, use words strong in themselves." "Literally" is "Often incorrectly used in support of exaggeration or violent metaphor"; "lose out" is "Meant to be more emphatic than lose, but actually less so, because of its commonness."

**Signs.**
- "very", "really", "extremely", "incredibly", "highly", "hugely", "absolutely", "completely", "totally", "utterly", "entirely", "truly", "particularly", "especially", "so" as an intensifier, "certainly", "definitely", "literally" (not literal), "super-", "ultra-".
- "real", "true", "genuine", "authentic" about people and goods: "a true expert", "genuine quality".
- Reassurances: "It really works!", "Guaranteed results!", "100% satisfaction".
- Pressure next to a fact: "absolutely free", "only $29.99", "exclusive to us!".
- Stacks of intensifiers and exclamation marks.

**Not an error if:**
- the word restricts or specifies rather than intensifies, and removing it changes the facts: "only two mistakes", "almost all", "completely removed" as opposed to "partly removed";
- it is part of a term: "very high frequency", "real time", "true positive", "absolute path";
- "real" means "actual, not simulated" ("real data"); "true" means "not false";
- "so" introduces a clause (Strunk V "So").

**Example.** "Their claim was totally unrealistic." "Total disclosure of all facts is very important to make sure we draw up a total and completely accurate picture of the Agency's financial position." ([PLAIN "Be concise"](sources/plain/guidelines/concise/index.md)) "A literal flood of abuse." ([Strunk V "Literal, literally"](sources/strunk/5-words-commonly-misused.md))

### W-CLICHE
**Cliché or filler phrase** · severity 3 (4 — a single everyday cliché; 2 — a paragraph stuffed with clichés and no facts, see [M-HOLLOW](#m-hollow)) · search: script + check · sources: [Strunk V "One of the most", "Factor", "Feature", "Line, along these lines", "Interesting"](sources/strunk/5-words-commonly-misused.md); [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md) (metaphors); [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md); [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md) · cited: Orwell, "Politics and the English Language", rule 1 and "dying metaphors"; Zinsser, *On Writing Well*, ch. "Words"; Fowler, *A Dictionary of Modern English Usage*, "hackneyed phrases"

**Rule.** The thought is put in the writer's own words; the present is not stressed unless it is contrasted with the past or the future.

**What goes wrong.** A cliché is a stock phrase whose meaning is either unclear or could be said in one word. The reader knows it from press releases and school essays, feels the writer is padding, and loses interest; stock phrases also cover a lack of facts — much written, nothing said. Strunk V calls such expressions "threadbare and forcible-feeble" ("one of the most"), "hackneyed" ("factor", "feature"), "so much overworked" ("along these lines"), and traces them to "a ready-made formula that saves him the trouble" of expressing his own thought. GOV.UK on metaphors: "they do not say what you actually mean and lead to slower comprehension of your content". Time fillers ("nowadays", "in today's world", "at this point in time") report a present the reader already assumes and pump up a false urgency. A worn-out metaphor does little harm, but nothing is lost when it goes.

**Signs.**
- Worn images: "at the end of the day", "the tip of the iceberg", "a perfect storm", "the elephant in the room", "a double-edged sword", "a level playing field", "the bottom line", "time will tell", "few and far between", "last but not least".
- Several words for one: "along these lines", "in the process of", "on a regular basis" (PLAIN: omit).
- Threadbare openers: "One of the most …", "An interesting story is told of …", "Since the dawn of time", "Throughout history".
- Hackneyed nouns: "factor", "feature", "aspect", "phase" (Strunk V: "Not to be used for aspect or topic").
- Official metaphors (GOV.UK): "drive" (schemes, people), "drive out", "going forward", "moving forward", "ring fencing", "hub", "portal", "one-stop shop".
- Time fillers: "nowadays", "these days", "in this day and age", "in today's world", "in the modern world", "at this point in time", "at the present time", "currently" (PLAIN: omit, or "now"), "now more than ever".

**Not an error if:**
- the image is fresh and the writer's own;
- the words are used literally: "a network hub", "drive a vehicle", "portal" as part of a service's name — GOV.UK's own exceptions;
- the time marker contrasts the present with the past or the future;
- the time is concrete: "since 2021", "in the last five years";
- the phrase is one of the machine-text tells ("in today's fast-paced world", "navigate the landscape", "tapestry") — that is [W-LLM](#w-llm); a business buzzword is [W-CORP](#w-corp).

**Example.** "Switzerland is one of the most interesting countries of Europe." ([Strunk V "One of the most"](sources/strunk/5-words-commonly-misused.md)) "Heavy artillery has become an increasingly important factor in deciding battles." ([Strunk V "Factor"](sources/strunk/5-words-commonly-misused.md)) "Mr. B. also spoke along the same lines." ([Strunk V "Line, along these lines"](sources/strunk/5-words-commonly-misused.md))

### W-CORP
**Corporate buzzword** · severity 3 (2 — a text about the company or the project consists of such phrases, see [M-HOLLOW](#m-hollow)) · search: script + check · sources: [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md), "Business jargon"; [GOV.UK "Use clear language"](sources/govuk/clear-language.md), "Know about words to avoid"; [GOV.UK A to Z "Words to avoid"](sources/govuk/a-to-z-style-guide.md); [GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md); [PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md)

**Rule.** The text says what is actually being done, by whom, for whom and with what result — something true only of this company or project, and checkable.

**What goes wrong.** Phrases from websites, slide decks and status reports that any organisation says about itself. Swap in another company's name and nothing changes, and a text that could be about anyone is about no one. PLAIN lists business jargon as "meaningless filler phrases". GOV.UK: "Avoid government 'buzzwords' and jargon. Often, these words are too vague and can lead to misinterpretation or empty, meaningless text"; "you can generally get rid of them by breaking the term into what you're actually doing. Be open and specific." Behind the buzzword there is often a modest meaning, or a real condition the writer would rather not state.

**Signs.**
- Business jargon (PLAIN): "thinking outside the box", "value added", "best practice", "touch base", "integrating quality solutions", "synergistic"; and its relatives: "leverage", "synergy", "circle back", "reach out", "take offline", "move the needle", "low-hanging fruit", "deep dive", "bandwidth" (of people), "alignment", "deliverables", "action items", "drive value", "end-to-end", "value proposition", "paradigm shift", "win-win".
- GOV.UK "Words to avoid": "agenda" (not for a meeting), "advance", "collaborate", "combat", "commit", "pledge", "counter", "deliver" (abstract things), "deploy", "dialogue", "disincentivise", "empower", "facilitate", "focus", "foster", "impact" (as a verb), "incentivise", "initiate", "key", "land", "leverage", "liaise", "overarching", "progress" (as a verb), "promote", "slim down", "streamline", "strengthening", "tackle", "transform", "utilise"; technical: "action" (as verb or noun), "enable", "interrogate", "fulfil".
- Company self-description: "a team of dedicated professionals", "trusted partner", "industry-leading", "market leader", "customer-centric", "committed to excellence", "tailored solutions", "comprehensive solutions", "we go the extra mile", "your success is our priority".

**Not an error if:** the claim is backed by checkable facts that could not be moved into another company's text; the word is used in its literal or technical sense — GOV.UK's own exceptions: "leverage" in finance, "deploy" for military or software, "combat" for military, "foster" for children, "agenda" for a meeting, "impact" for a collision, "promote" for a campaign or a career, "land" for aircraft; an evaluative word stands inside a story told in facts. "Robust" and "seamless" go to [W-LLM](#w-llm) (GOV.UK lists "robust" too).

**Example.** "Integrating quality solutions", "Promoting an informed and synergistic teams" (from the list of "meaningless filler phrases", [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md)); "This increased emphasis on responsiveness is captured through an ongoing series of 'Open Door Forums' that provide a dialogue about both the many individual service areas and beneficiary needs within CMS." ([PLAIN example "Medicaid Open Door Initiative"](sources/plain/examples/medicaid-initiative.md))

### W-BUREAU
**Officialese** · severity 3 (2 — the reader cannot tell what is happening and what to do, or a formal clause hides an important restriction) · search: script + check · sources: [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md); [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md), "Legal language"; [PLAIN "Use 'must' to indicate requirements"](sources/plain/guidelines/conversational/use-must-to-indicate-requirements.md); [PLAIN "Shall and must"](sources/plain/guidelines/conversational/shall-and-must.md); [PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md), "The 'all-inclusive' cross-reference"; [PLAIN "Highlight important concepts"](sources/plain/guidelines/design/highlight-important-concepts.md); [GOV.UK "Use the right tone"](sources/govuk/right-tone.md); [PLAIN example "Wordiness Made Spare"](sources/plain/examples/wordiness.md)

**Rule.** Simple things are said simply; a notice or announcement explains what is happening, why, what the reader must do and whom to contact.

**What goes wrong.** Officialese — the stock phrases of bureaucrats and legal drafters — is unnatural and inflated: a simple meaning takes many words, the point gets lost, and no room is left for useful information. "Legal language is a major source of annoying jargon"; archaic words and formalisms "give legal writing its musty smell" (PLAIN "Avoid jargon"); "shall" tells the reader "this is deadly material" (PLAIN "Use 'must'…"). Formalism — keeping the form at the expense of use: a legally tidy clause is useless to the reader and can hide an important condition; the "all-inclusive" cross-reference "reflects a lazy writer" (PLAIN "Minimize cross-references"). A faceless author — "the Administration", "the undersigned", "this office" — cannot be contacted; GOV.UK wants a tone "serious but not pompous" and a named "we". Block capitals are read as shouting (PLAIN "Highlight important concepts"; GOV.UK).

**Signs.**
- Words from PLAIN's list: "pursuant to", "in accordance with", "in the event of", "in the amount of", "in order that", "in order to", "prior to", "subsequent to", "utilize/utilization", "commence", "terminate", "endeavor", "furnish", "render", "deem", "herein", "heretofore", "hereby", "herewith", "aforementioned", "above-mentioned", "the foregoing", "said" and "such" for "the", "notwithstanding", "inasmuch as", "with reference to", "with the exception of", "until such time as", "due to the fact that".
- "shall" for an obligation (PLAIN: use "must").
- Formulas: "please be advised that", "be advised" (PLAIN: omit), "you are hereby notified", "addressees are requested", "it is requested that", "we apologise for any inconvenience caused", "is strictly prohibited", "under no circumstances", "ATTENTION!" and whole sentences in capitals.
- A generic legal category instead of the concrete condition: "and all other applicable laws and regulations", "any and all", "including but not limited to", "or any part thereof".
- A faceless author: "the Administration", "the Management", "the undersigned" (PLAIN: "I"), "this office", "your office" (PLAIN: "you"), "the Company accepts no responsibility".

**Not an error if:**
- the word is the simplest way to say what is needed: many items on the list are common ("such", "in addition", "prior"), and their presence alone is not an error;
- a formal detail gives the reader a condition they need;
- it is a legal text where every word matters and the wording is fixed by law (G2);
- a polite formula stands in a text with real care;
- "the Administration" is a concrete department, and the text says how to reach it.

**Example.** "Any oil or gas lessee who wishes to use timber for fuel in drilling operations shall file an application therefor with the officer who issued the lease." ([PLAIN "Use 'must' to indicate requirements"](sources/plain/guidelines/conversational/use-must-to-indicate-requirements.md)) "When the process of freeing a vehicle that has been stuck results in ruts or holes, the operator will fill the rut or hole created by such activity before removing the vehicle from the immediate area." ([PLAIN example "Wordiness Made Spare"](sources/plain/examples/wordiness.md)) "As a permittee, you must comply with sections 542.6 and 543.10, and all other applicable laws and regulations." ([PLAIN "Minimize cross-references"](sources/plain/guidelines/design/minimize-cross-references.md))

### W-ZAUM
**Jargon and long words** · severity 3 (2 — the meaning, or the problem itself, is lost behind a chain of such words) · search: script + check · sources: [PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md); [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md); [PLAIN "Choose your words carefully"](sources/plain/guidelines/words/index.md) (Fowler's preferences from *The King's English*); [GOV.UK "Use clear language"](sources/govuk/clear-language.md); [GOV.UK technical A to Z](sources/govuk/technical-a-to-z.md); [PLAIN "Use examples"](sources/plain/guidelines/conversational/use-examples.md) · cited: Orwell, "Politics and the English Language", rules 2 and 5 and "pretentious diction"; Pinker, *The Sense of Style*, ch. "The Curse of Knowledge"

**Rule.** Where a plain, familiar word exists, it is used; a technical term only where it is needed.

**What goes wrong.** A bookish, Latinate or pseudo-scientific word stands where a plain one exists. "Jargon is unnecessarily complicated language used to impress, rather than to inform, your audience" (PLAIN). The reader who does not know the word will not understand it; the one who does will catch it misused. GOV.UK: "Do not use formal or long words when easy or short ones will do. Use 'buy' instead of 'purchase', 'help' instead of 'assist', and 'about' instead of 'approximately'." Specialists prefer plain words too: "the more educated the person and the more specialist their knowledge, the greater their preference for plain English" (GOV.UK). Jargon gives away an unsure writer — understanding shows in what you write about, not in the words — and sometimes it covers a problem until the problem cannot be seen. PLAIN quotes Fowler: "Prefer the familiar word to the far-fetched… Prefer the short word to the long. Prefer the Saxon word to the Romance word."

**Signs.**
- Long words from PLAIN's list where a short one exists: "utilize" (use), "facilitate" (help), "ascertain" (find out), "commence" (start), "methodology" (method), "parameters" (limits), "optimum" (best), "expedite" (speed up), "endeavor" (try), "demonstrate" (show), "remuneration" (pay), "proficiency" (skill), "prioritize" (rank), "magnitude" (size), "numerous" (many), "subsequently" (later), "approximately" (about), "purchase" (buy), "assist" (help), "possess" (have — Strunk V).
- Chains of such words linked by "of": "the impingement of entrained particulate matter".
- Pseudo-scientific and managerial words outside their field: "operationalize", "conceptualize", "ideate", "problematize", "paradigm", "modality", "granular", "holistic", "learnings".
- Latin and foreign tags: "ipso facto", "inter alia" (PLAIN: omit), "vis-à-vis", "per se", "mutatis mutandis"; "e.g." and "i.e." (PLAIN "Use examples": write "for example", "that is").
- Technical words used loosely (GOV.UK technical): "access" information (get), "issues" or "defects" (problems), "legacy" (explain it), "interrogate" (monitor, track), "consult" (check).
- A term from another field used for weight or as a metaphor: "quantum leap", "exponential" for "fast", "in our DNA".

**Not an error if:**
- the term is needed in its field: "there may not be another correct way to refer to a 'brinulator valve control ring'" (PLAIN);
- the word carries a shade the plain synonym lacks; if the reader may not know it, that is [M-LEVEL](#m-level), and GOV.UK's rule applies — explain a specialist term "the first time you use them";
- professional jargon in a text for insiders: "Special terms can be useful shorthand within a particular audience" (PLAIN);
- it is the word users "use themselves" (GOV.UK);
- deliberate play.

**Example.** "riverine avifauna" (river birds); "involuntarily undomiciled" (homeless); "Most refractory coatings to date exhibit a lack of reliability when subject to the impingement of entrained particulate matter in the propellant stream under extended firing durations." ([PLAIN "Avoid jargon"](sources/plain/guidelines/words/avoid-jargon.md); plain version: "The exhaust gas eventually damages the coating of most existing ceramics.")

### W-NOMINAL
**Hidden verb (nominalization)** · severity 3 (2 — a chain of hidden verbs hides who does what) · search: script + check · sources: [PLAIN "Avoid hidden verbs"](sources/plain/guidelines/words/avoid-hidden-verbs.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md), "Know about words to avoid"; [Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md); [PLAIN example "Register a Pesticide"](sources/plain/examples/register-pesticide.md) · cited: Williams, *Style*, lesson "Actions"; Pinker, *The Sense of Style*, ch. "A Window onto the World" ("zombie nouns"); Orwell, "Politics and the English Language", "verbal false limbs"

**Rule.** An action is named by a verb.

**What goes wrong.** The action is hidden in a noun. "A hidden verb (or nominalization) is a verb converted into a noun. It often needs an extra verb to make sense" (PLAIN) — "make", "conduct", "carry out", "perform", "give", "have", "take", "achieve", "effect", "reach" — and the phrase grows into a chain of nouns. Hidden verbs "make our writing weak and longer than necessary" and "often go hand in hand with passive verbs and combine to give an officious and longwinded style" (PLAIN). GOV.UK: "Words ending in '–ion' and '–ment' tend to make sentences longer and more complicated than they need to be." Strunk 10 names the common case: a noun "which expresses the entire action, leaving to the verb no function beyond that of completing the sentence". With few verbs the text is a still life.

**Signs.**
- Weak verb + action noun: "make a decision / an application / a payment / a recommendation / a change", "conduct an analysis / a review / an investigation", "carry out a review", "perform an assessment", "undertake the calculation of", "give consideration to", "provide assistance to", "take action", "reach a conclusion / an agreement", "have a discussion", "gain an understanding of", "effect modifications", "achieve compliance", "be responsible for the management of".
- "the + -tion/-ment/-sion/-ance/-ing + of": "the production of", "the assessment of" (PLAIN: the longer word placed "between the words 'the' and 'of'").
- An action noun as the subject of a passive or state verb: "A survey … was made", "Confirmation … cannot be obtained", "Implementation … is planned".
- "measures / activities / services for the + -tion of".

**Not an error if:** the noun names a thing or a result, not an action ("the application form", "a payment of £10" as an amount, "the building", "documentation" as documents); it refers back to an action just described ("this decision"); it names a concept ("inflation", "freedom"); it is a term ("garbage collection", "dependency injection"). If the whole sentence is built as abstract subject + state verb, the code is [P-INACTION](#p-inaction); if nouns are stacked as modifiers, [W-NOUNSTACK](#w-nounstack).

**Example.** "To trace the missing payment, we need to carry out a review of the Agency's accounts so we can gain an understanding of the reason the error occurred." "If you cannot make the payment of the $100 fee, you must make an application in writing before you file your tax return." ([PLAIN "Avoid hidden verbs"](sources/plain/guidelines/words/avoid-hidden-verbs.md)) "A survey of this region was made in 1900." ([Strunk 10](sources/strunk/3-principles-of-composition.md); "This region was surveyed in 1900.")

### W-PASSIVE
**Passive voice** · severity 3 (2 — the voice hides who acted or who must act, and the reader needs to know) · search: script + check · sources: [PLAIN "Use active voice"](sources/plain/guidelines/conversational/use-active-voice.md); [GOV.UK "Use clear language"](sources/govuk/clear-language.md), "Use the active voice"; [GOV.UK A to Z "Active voice"](sources/govuk/a-to-z-style-guide.md); [Strunk 10 "Use the active voice"](sources/strunk/3-principles-of-composition.md); [PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md); [PLAIN example "Application Due Date"](sources/plain/examples/application-due-date.md) · cited: Orwell, "Politics and the English Language", rule 4; Williams, *Style*, lesson "Characters"

**Rule.** The action is told from the side of whoever does it.

**What goes wrong.** The passive turns the action inside out. It is harder to read and adds words: "the passive voice results in long sentences and can make the content harder to read" (GOV.UK). Often it also hides the actor: "Passive voice obscures who is responsible for what and is one of the biggest problems with government writing"; "Not 'It must be done,' but 'You must do it.'" (PLAIN). Strunk 10: without "by me" the sentence "becomes indefinite: is it the writer, or some person undisclosed, or the world at large". In instructions the reader cannot tell whether they are the one who must act; in reports of results and failures the passive conceals who decided or who erred.

**Signs.**
- A form of "be" (or "get") + past participle: "is/are/was/were/be/been/being + -ed/-en" — "was proposed", "has been completed", "will be withheld", "must be included". PLAIN names the two features: "A form of the verb 'to be'" and "A past participle".
- An agent in a "by" phrase: "was polluted by the company".
- Instructions in the passive: "must be submitted", "should be completed", "is to be provided".
- "It is recommended / expected / believed / decided that" (see also [P-EXPLETIVE](#p-expletive)).
- Reports with no actor where the actor matters: "mistakes were made", "the decision was taken", "the data was deleted", "the budget was spent".
- One passive depending on another: "was not allowed to be exported", "has been proved to have been seen" (Strunk 10).

**Not an error if:**
- the outcome matters more than the agent — GOV.UK: "Biometric residence permits have been replaced by eVisas";
- the passive keeps the text centred on the user — GOV.UK prefers "You'll be told what you need to do when you apply" to naming the Home Office;
- the law is the actor, or it does not matter who acts — PLAIN: "If you do not pay the royalty on your mineral production, your lease will be terminated.";
- the subject is the topic of the paragraph (Strunk 10, the dramatists of the Restoration; see [P-FOCUS](#p-focus));
- a state, not an action: "the form is closed", "payment declined", "the battery is charged", "located in", "based on";
- it is the past tense in the active voice — "Don't confuse passive voice with past tense" (PLAIN).

**Example.** "The lake was polluted by the company." "New regulations were proposed." ([PLAIN "Use active voice"](sources/plain/guidelines/conversational/use-active-voice.md)) "The application must be completed by the applicant and received by the financial office by June 1st." ([PLAIN example "Application Due Date"](sources/plain/examples/application-due-date.md); plain version: "We must receive your application by June 1st.")

### W-VAGUE
**Vagueness** · severity 3 (4 — the word is decoration and hides nothing) · search: script + check · sources: [Strunk 12 "Use definite, specific, concrete language"](sources/strunk/3-principles-of-composition.md); [Strunk V "Etc.", "Nature", "Case"](sources/strunk/5-words-commonly-misused.md); [GOV.UK technical A to Z "Words to avoid"](sources/govuk/technical-a-to-z.md) ("periodically", "regularly"); [PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md); [PLAIN "Be concise"](sources/plain/guidelines/concise/index.md); [PLAIN "Use simple words and phrases"](sources/plain/guidelines/words/use-simple-words-phrases.md)

**Rule.** A number is given with the precision the reader needs; instead of "some" and "various", the text names what it means.

**What goes wrong.** Vague words give imprecise information instead of precise, so the reader cannot picture it. Strunk 12: "Prefer the specific to the general, the definite to the vague, the concrete to the abstract"; "the surest method of arousing and holding the attention of the reader is by being specific, definite, and concrete." GOV.UK on "periodically" and "regularly": "try to be specific".
- **Approximators.** "More than", "about", "almost" are skipped as noise, and they make serious figures look doubtful. A price "from $X" is a manipulation a careful reader sees through at once.
- **Excess precision.** A number to the last digit when the reader needs only its size.
- **Rankings.** "Among the top 10" is unclear and useless: the reader wants to know whether their problem gets solved.
- **Indefinite words.** "Some facts", "various products", "appropriate offices" stand where the real thing should be named. Strunk V: "etc." is "not to be used if … the reader would be left in doubt as to any important particulars".
- **Vague time.** "Soon", "in a timely manner", "regularly": the reader cannot plan.

**Signs.**
- "more than", "over", "about", "around", "approximately", "almost", "nearly", "up to", "at least", "no less than", "from $X", "starting at".
- Unrounded numbers of five or more digits where only the size matters.
- "among the top 10", "one of the leading", "one of the largest", "a leading provider".
- "some", "certain", "various", "a number of", "numerous", "several", "multiple", "many", "a lot of", "a range of", "a variety of", "a wide range of", "a host of", "etc.", "and so on", "and more"; "appropriate", "relevant", "applicable", "necessary", "related", "as needed", "where necessary".
- "soon", "shortly", "in the near future", "in due course", "at a later date", "recently", "in a timely manner", "promptly", "as soon as possible", "ASAP", "regularly", "periodically", "from time to time".

**Not an error if:**
- a number is rounded without an approximator — that is the norm;
- the exact number is needed for a calculation or a check;
- a ranking gives an exact place that matters to this reader;
- the uncertainty is itself the information (the source is unknown, and the text says so);
- phone numbers, IDs, years — they are not quantities;
- "etc." ends a list already given in full (Strunk V).

**Example.** "Individuals and organizations wishing to apply must file applications with the appropriate offices in a timely manner." ([PLAIN "Address the user"](sources/plain/guidelines/audience/address-the-user.md); plain version: "You must apply at least 30 days before you need the certification.") "A period of unfavorable weather set in." ([Strunk 12](sources/strunk/3-principles-of-composition.md); "It rained every day for a week.")

### W-NOUNSTACK
**Noun string** · severity 3 (2 — four or more nouns, or the reader cannot tell which noun is the head) · search: script + check · sources: [PLAIN "Avoid noun strings"](sources/plain/guidelines/words/avoid-noun-strings.md) · cited: Zinsser, *On Writing Well*, ch. "Bits & Pieces"

*Added by entalk, not from rutalk; not measured.*

**Rule.** A noun is not preceded by a string of other nouns; from three nouns in a row, the relations between them are spelled out with prepositions and articles.

**What goes wrong.** "Readability suffers when three words that are ordinarily separate nouns follow in succession. Once you get past three, the string becomes unbearable." Stacking turns all nouns but the last into adjectives, and "many users will think they've found the noun when they're still reading adjectives, and will become confused" (PLAIN). The relations — who protects what, for whom, at which stage — disappear, and the reader has to guess them. Russian has no such construction, so rutalk had no code for it; English technical and official writing produces it constantly.

**Signs.**
- Three or more nouns in a row with no article, preposition, verb or comma between them, the last one being the head: "[noun] [noun] [noun]".
- A possessive inside or in front of the string: "…'s automobile seat belt interlock rule".
- Strings ending in -tion, -ment, -ance or "process", "policy", "procedure", "framework", "requirements", "development".
- Ticket, spec and report titles made of noun strings.

**Not an error if:**
- the string is a proper name or official title (an agency, a product, a law);
- it is a fixed compound the reader knows as one unit: two-noun compounds ("seat belt", "credit card", "user ID") and established terms;
- the reader is a specialist for whom the string is a known term (G2);
- a verb has been turned into a noun ("make a decision") rather than nouns stacked as modifiers — that is [W-NOMINAL](#w-nominal); when both occur in one phrase, give the code that explains the harm.

**Example.** "Underground mine worker safety protection procedures development"; "Draft laboratory animal rights protection regulations" ([PLAIN "Avoid noun strings"](sources/plain/guidelines/words/avoid-noun-strings.md); plain versions: "Developing procedures to protect the safety of workers in underground mines", "Draft regulations to protect the rights of laboratory animals").

### W-LLM
**Machine-text tells** · severity 3 (2 — the tells cluster so that the text reads as generated and the reader stops trusting it, or "not X but Y" knocks down a claim nobody made) · search: script + check · sources: none

*Added by entalk, not from rutalk; not measured.*

**Rule.** The text uses none of the stock words and moves typical of language-model output.

**What goes wrong.** Language models — including the writer this package prompts — fall back on a recognisable set of words and moves. Each one alone is a cliché, a buzzword or an empty evaluation; together they tell the reader the text was generated without care, and the reader discounts the content along with the style. They also carry the harms of the neighbouring codes: grand words without facts ([W-EVAL](#w-eval)), worn images ([W-CLICHE](#w-cliche)), rows of three by habit ([P-SYNONYMS](#p-synonyms)), contrasts with a position nobody holds.

No file in `sources/` describes these patterns. The list comes from common observation of model output; it is entalk's hypothesis and is not measured. GOV.UK's "Words to avoid" lists "robust", "foster", "empower", "leverage" and "transform" as buzzwords — that grounds them as words to avoid, not as machine tells.

**Signs.**
- Strong tells (one is enough): "delve (into)", "tapestry", "navigate the landscape / the complexities", "the ever-evolving landscape", "in the realm of", "embark on a journey", "a testament to", "underscores the importance of", "unlock the potential / the power of", "seamless(ly)", "robust".
- Openers: "In today's fast-paced world", "In today's digital age", "In an ever-changing world", "In a world where …", "Whether you're a … or a …, …".
- Contrast frame: "It's not X — it's Y", "This isn't just X; it's Y", "Not only X, but Y" — where X is a view nobody put forward.
- Reflexive triads: rows of exactly three adjectives, nouns or clauses, paragraph after paragraph, where the three are not distinct.
- Signposts and wrap-ups: "Let's dive in", "Let's explore", "Here's the thing:", "The result?", "The best part?", and "In conclusion,", "Ultimately,", "Overall," closing a short text.
- Chatbot residue: "Great question!", "Certainly!", "I hope this helps", "Feel free to …", "Let me know if you'd like …", "As an AI …".
- Weak tells (count only when three or more appear in one paragraph): "pivotal", "crucial", "vital", "intricate", "multifaceted", "nuanced", "holistic", "dynamic", "vibrant", "bustling", "meticulous", "elevate", "harness", "unleash", "empower", "foster", "game-changer", "cutting-edge", "boasts".
- Typography: an em dash in most sentences; a bold label with a colon opening every bullet; emoji as bullets or in headings.

**Not an error if:**
- the word is used in its literal or technical sense: "robust statistics", "seamless pipe", "navigate to the Settings page", "landscape orientation", "tapestry" as a textile;
- the three items are genuinely different and the reader needs all three;
- the contrast is real: X is a view someone actually holds — Strunk 11: "The antithesis of negative and positive is strong";
- quoted text, including model output quoted for discussion (G5);
- a single weak tell in an otherwise concrete text.

Only the patterns listed here go to W-LLM; a general cliché stays [W-CLICHE](#w-cliche), a business buzzword [W-CORP](#w-corp), an ordinary evaluation [W-EVAL](#w-eval), a filler announcement [W-INTRO](#w-intro).

**How the sources describe it.** They do not. No file in `sources/` deals with model output, so this entry gives no example: rutalk's rule is that examples come from the sources, and none of them has one.

---

## V — Illustrations

V codes are checked only when the text has images, their descriptions, captions, alt texts, tables or diagram code. The exceptions are [V-NOSCHEME](#v-noscheme) and [V-NOSCREEN](#v-noscreen): they are visible from the text itself.

The English sources say little about illustrations: PLAIN's design guidelines and examples ground the use of visuals and tables, and GOV.UK's style guide covers tables. Where an entry says so, the description of the fault is carried over from rutalk (Ilyakhov, *Yasno, ponyatno*, the chapters on pictures, screenshots and diagrams).

### V-DECOR
**Decoration instead of illustration** · severity 3 (2 — the picture works against the text's message) · search: script (alt text, image source), reading · sources: [PLAIN "Consider using visuals"](sources/plain/guidelines/design/consider-using-visuals.md); [PLAIN "Design for reading"](sources/plain/guidelines/design/index.md); [PLAIN example "Car Safety"](sources/plain/examples/car-safety.md)

**Rule.** An image shows what the text is about and helps the reader understand it.

**What goes wrong.** A picture "on the topic" — a generic stock photo, a symbol, an ornament added so the page does not look like a wall of text — takes space and attention but tells nothing, and the text looks cheap and untrustworthy. Worse, a picture can give the opposite impression to the one intended, or show people and settings the audience does not recognise as theirs, and then the reader has no reason to trust the text. PLAIN shows the other kind: every illustration in "Consider using visuals" carries content that words would struggle with — mountainous areas under flight restrictions, areas around the White House where activities are controlled, the measurement procedure for carbon monoxide, an official mark; in "Car Safety" a warning label replaces a paragraph. PLAIN also warns: "Don't overuse layout and typographical devices."

**Signs.**
- Alt text or caption names a generic image of the topic: "business", "success", "teamwork", "people in a meeting", "technology", "abstract background".
- A symbol instead of content: light bulb, rising chart, gears, handshake, puzzle pieces, rocket, smiling faces.
- The picture could move to any article on the same topic without loss.
- A photo of the author organisation's building instead of the subject of the news.
- Pictures at regular intervals as dividers.
- People and settings from a different world than the audience's; the picture's tone contradicts the text's.

**Not an error if:**
- the picture lets the reader examine the subject of the text;
- it is a photo of the real people, places or object of the news;
- the drawing is rough but helps understanding;
- there are no pictures at all — that is not an error. Without alt text, a caption or a description the code is not given.

**How the sources describe it.** The English sources describe only useful illustrations (PLAIN "Consider using visuals", "Car Safety") and give no example of a decorative one. The description of the fault is carried over from rutalk's V-DECOR (Ilyakhov, *Yasno, ponyatno*, «Картинка или иллюстрация»).

### V-SCREEN
**Screenshot or table not prepared** · severity 3 (2 — an instruction depends on the screenshot) · search: reading · sources: [PLAIN "Use tables to make complex material easier to understand"](sources/plain/guidelines/design/use-tables-to-make-complex-material-easier-to-understand.md); [PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md); [GOV.UK A to Z "N/A", "Numbers"](sources/govuk/a-to-z-style-guide.md); [GOV.UK technical A to Z "placeholders"](sources/govuk/technical-a-to-z.md)

**Rule.** A screenshot, scan or table shows and says where to look; clutter is removed, and the text in the image is checked.

**What goes wrong.** At first glance the reader cannot tell where to look in a document, a screenshot or a table. Clutter — toolbars, tabs, pop-up warnings, empty fields — distracts and shrinks what matters. Text in the image shapes the impression: placeholder names reveal an unfinished product, open tabs and internal addresses expose the author, personal data leaks. For tables the English sources give the same rule from the text side: PLAIN's if-then table opens with a sentence saying what it shows ("The following table shows how we determine the amount of the deduction."); lists need "a lead-in sentence" (PLAIN), "a lead-in line" (GOV.UK); "Do not use N/A in empty cells in tables. Use 'no data' or 'not applicable' instead." and "In tables, use numerals throughout." (GOV.UK); placeholders in sample code are explained "under the code sample" (GOV.UK technical).

**Signs.**
- A caption such as "Screenshot", "Interface", "Figure 1" with no name of the element that matters.
- No pointer: "the field top right", a callout, a highlight.
- A table with no lead-in sentence saying what to compare or find in it; "N/A" or empty cells; mixed number formats.
- "See legend" far from the image.
- Small text, cluttered tabs, pop-up warnings; placeholder data ("Test User", "Lorem ipsum"), personal data, internal URLs, tokens.

**Not an error if:** the text says where to look and the important part is highlighted; the rest is faded; sensitive data is masked; real working data shows the subject of the text.

**How the sources describe it.** The English sources give no example of a bad screenshot; they cover tables (a lead-in sentence, no "N/A" in cells, numerals) and placeholders in code samples. The screenshot part is carried over from rutalk's V-SCREEN (Ilyakhov, *Yasno, ponyatno*, «Скриншоты, документы и таблицы»).

### V-NOSCREEN
**Product behaviour without a screenshot** · severity 2 (3 — the behaviour is mentioned in passing, and the text is about something else) · search: reading · sources: none directly; nearest: [PLAIN example "Car Safety"](sources/plain/examples/car-safety.md)

*Code added by the metarepo, not taken from the books (it came to entalk from rutalk); not measured in `lab/`.*

**Rule.** If the text describes what a user of the product sees and does — a page, a step, a message, a state — a screenshot of the real interface stands next to it, with a caption saying where to look.

**What goes wrong.** The reader has not seen the page in question and assembles it from words: "the button to the right of the field", "after you choose the card type, the address appears". Everyone builds a different picture, and a question about how the page behaves gets an answer about a page that does not exist. A screenshot shows the page at once, and the reader sees immediately whether the text describes it correctly. A description of a change needs both pages, "before" and "after": without "before" the reader cannot see what changed.

**Signs.**
- A page, its elements and their layout described in words: "field", "button", "tab", "dropdown", "toggle", "modal", "banner", "at the top", "at the bottom", "on the right", "in the sidebar".
- The user's steps in the interface: "the user opens …", "clicks / taps …", "sees …", "then … appears".
- A change in behaviour: "previously …, now …", "the page now asks for …".
- A question about how a page should behave, without the page.
- No screenshot nearby, or only "after" without "before".

**Not an error if:**
- the page cannot be captured and the text says why: no test user in the needed state, a product where capture is not possible;
- the behaviour is mentioned in one phrase and the text is about something else;
- a mock-up stands next to it and the text is about what the page should become, not what it is.

**How the sources describe it.** No source describes this case. PLAIN "Car Safety" makes the general point — "Sometimes a picture is worth a thousand words" — by replacing a paragraph of warnings with a label. rutalk's example for this code was written by the metarepo, not taken from a book, so entalk does not carry it over.

### V-NOSCHEME
**Complex process in words only** · severity 2 (3 — a moderately complex linear chain) · search: script (step and condition markers), reading · sources: [PLAIN "Use tables to make complex material easier to understand"](sources/plain/guidelines/design/use-tables-to-make-complex-material-easier-to-understand.md); [PLAIN "Keep the subject, verb, and object close together"](sources/plain/guidelines/concise/keep-the-subject-verb-and-object-close-together.md); [PLAIN "Consider using visuals"](sources/plain/guidelines/design/consider-using-visuals.md); [PLAIN example "Monthly Due Date"](sources/plain/examples/monthly-due-date.md); [Strunk 15 "Express co-ordinate ideas in similar form"](sources/strunk/3-principles-of-composition.md)

**Rule.** A multi-step, branching or multi-party process is shown as a diagram; a set of conditions and their outcomes as an if-then table.

**What goes wrong.** Diagrams are indispensable where the text describes complex abstract processes, especially ones stretched over time or with several possible outcomes. In words the reader has to keep stages, conditions and parties in their head, and the picture of the process never forms. "Tables help your audience see relationships that are often times hidden in dense text"; "If the provision is complex, and especially if there are several different 'if' provisions, use a different sentence for every 'if,' or consider using an if-then table" (PLAIN). Strunk 15, on a long run of similar statements: "he had best avoid difficulty by putting his statements in the form of a table." PLAIN's examples of visuals include a diagram of a measurement and calibration procedure.

**Signs.**
- A long chain "first … then … after that … finally".
- Branches "if … then …, otherwise …"; scripts "if they say this, answer that"; one sentence with several conditions and several outcomes.
- Many parties and hand-offs: "passes to", "approves", "depends on", "notifies", "escalates to"; state transitions, retries, timeouts.
- Two complex processes ("before" and "after") compared in words only.
- No diagram or table nearby.

**Not an error if:** the process is simple; the format allows no images and the text is broken into numbered steps or one sentence per condition; the diagram is attached.

**Example.** "We must receive your completed application form on or before the 15th day of the second month following the month you are reporting if you do not submit your application electronically or the 25th day of the second month following the month you are reporting if you submit your application electronically." ([PLAIN example "Monthly Due Date"](sources/plain/examples/monthly-due-date.md); the source replaces it with a two-row table.)

### V-SCHEME
**Diagram that cannot be read** · severity 2 (3 — decoration overloads a diagram that is clear on the whole) · search: reading · sources: [PLAIN "Design for reading"](sources/plain/guidelines/design/index.md); [PLAIN "Use lists"](sources/plain/guidelines/organize/use-lists.md)

**Rule.** A diagram is understood at first glance: its shape conveys the meaning of the process, nodes and links are labelled, colour carries information, and it shows only what matters to the reader.

**What goes wrong.** A diagram is good when the reader understands it at first glance; if the links are arranged confusingly, it misleads more than it helps. The reader takes in the shape before the labels: if the text promises "complicated before, simple after" and both diagrams are the same size, the main point does not get through. Realistic colours, decoration, shadows, every real step — and the diagram is overloaded and loses its clarity. PLAIN's design checks apply to diagrams as to pages: "Be sure it doesn't look visually confusing. Don't overuse layout and typographical devices."; "Use shading and borders only to accent graphs, charts, etc."; "Readers get lost when you use more than two or three levels".

**Signs.**
- Unlabelled nodes or arrows; crossing arrows; no overall direction.
- "Before" and "after" diagrams of the same complexity.
- A process the text calls cyclic drawn as a line; a hierarchy drawn as a flat chain; more than three levels of nesting.
- Every node a different colour; colour against meaning (good things in red).
- A route drawn over a political map; more steps than the reader needs.
- In diagram code (Mermaid, PlantUML, Graphviz): nodes shown by their IDs instead of labels; dozens of nodes in one diagram.

**Not an error if:** the diagram is tangled on purpose, to show chaos; it is rough but clear; it has no geography, no extra steps and no realistic colours.

**How the sources describe it.** The English sources have nothing on diagrams beyond PLAIN's general design checks quoted above. The description of the fault is carried over from rutalk's V-SCHEME (Ilyakhov, *Yasno, ponyatno*, «Схемы», «Типовые схемы»).

### V-RIGHTS
**Someone else's image without rights** · severity 3 · search: script (image source), question to the author · sources: none on images; [sources README](sources/README.md) (licence practice for text); [PLAIN "Consider using visuals"](sources/plain/guidelines/design/consider-using-visuals.md)

**Rule.** Images are the author's own or licensed.

**What goes wrong.** Every image on the internet belongs to someone, and by default the author has no right to use it in their work; the risk of a claim grows with the size of the organisation. Such a picture also cheapens the work: it reads as copy-paste.

**Signs.** The image source or URL is a search engine, someone else's site, or a stock site with no licence stated; memes, celebrity photos, other people's illustrations; captions such as "Image from the internet", "Source: Google", "Photo from open sources".

**Not an error if:** the image is bought, licensed, in the public domain or under an open licence with the required attribution; the idea of someone else's diagram is redrawn rather than the picture copied. A licence cannot be checked from the text — it is a question for the author.

**How the sources describe it.** No source in `sources/` covers image rights. The [sources README](sources/README.md) shows the standard for text — every file is public domain or under an open licence, with the licence stated, and copyrighted books are cited, not copied — and PLAIN "Consider using visuals" names the regulation each illustration comes from. The description of the fault is carried over from rutalk's V-RIGHTS (Ilyakhov, *Yasno, ponyatno*, «Типовые схемы»).

---

## Sources → codes

Generated from the links in the entries above: each source lists the codes and general rules whose entries cite it. Cited books are named, not copied.

| Source | Codes |
|---|---|
| PLAIN [Address separate audiences separately](sources/plain/guidelines/audience/address-separate-audiences-separately.md) | S-MODULES |
| PLAIN [Address the user](sources/plain/guidelines/audience/address-the-user.md) | P-INACTION, P-REFERENT, W-PASSIVE, W-VAGUE |
| PLAIN [Do your research](sources/plain/guidelines/audience/do-your-research.md) | M-READER |
| PLAIN [Write for your audience](sources/plain/guidelines/audience/index.md) | M-READER, M-ORDER, M-LEVEL, M-IDEAL, G2 |
| PLAIN [Be concise](sources/plain/guidelines/concise/index.md) | P-OVERLOAD, P-SYNONYMS, W-INTRO, W-INTENS, W-CLICHE, W-VAGUE |
| PLAIN [Keep the subject, verb, and object close together](sources/plain/guidelines/concise/keep-the-subject-verb-and-object-close-together.md) | P-SPLIT, V-NOSCHEME |
| PLAIN [Use positive language](sources/plain/guidelines/concise/use-positive-language.md) | P-NESTED, P-CLUMSY |
| PLAIN [Write short paragraphs](sources/plain/guidelines/concise/write-short-paragraphs.md) | M-ROBOT, S-WALL, S-PARA-MIX, S-BURIED, G4 |
| PLAIN [Write short sections](sources/plain/guidelines/concise/write-short-sections.md) | S-SUBHEADS |
| PLAIN [Write short sentences](sources/plain/guidelines/concise/write-short-sentences.md) | P-OVERLOAD, P-NESTED |
| PLAIN [Don’t use slashes](sources/plain/guidelines/conversational/dont-use-slashes.md) | P-INLINELIST |
| PLAIN [Keep it conversational](sources/plain/guidelines/conversational/index.md) | P-INACTION |
| PLAIN [Shall and must](sources/plain/guidelines/conversational/shall-and-must.md) | W-BUREAU |
| PLAIN [Use active voice](sources/plain/guidelines/conversational/use-active-voice.md) | T-HIDE, W-PASSIVE, G2 |
| PLAIN [Use contractions](sources/plain/guidelines/conversational/use-contractions.md) | M-ROBOT, G1 |
| PLAIN [Use examples](sources/plain/guidelines/conversational/use-examples.md) | M-NOEXAMPLE, M-EXAMPLE, S-EXAMPLES, W-ZAUM |
| PLAIN [Use “must” to indicate requirements](sources/plain/guidelines/conversational/use-must-to-indicate-requirements.md) | W-BUREAU |
| PLAIN [Consider using visuals](sources/plain/guidelines/design/consider-using-visuals.md) | V-DECOR, V-NOSCHEME, V-RIGHTS |
| PLAIN [Highlight important concepts](sources/plain/guidelines/design/highlight-important-concepts.md) | S-CLICKBAIT, S-SCAN, W-BUREAU |
| PLAIN [Design for reading](sources/plain/guidelines/design/index.md) | S-WALL, V-DECOR, V-SCHEME |
| PLAIN [Minimize cross-references](sources/plain/guidelines/design/minimize-cross-references.md) | M-LEVEL, M-FACTS, S-MODULES, P-SPLIT, W-BUREAU |
| PLAIN [Use tables to make complex material easier to understand](sources/plain/guidelines/design/use-tables-to-make-complex-material-easier-to-understand.md) | V-SCREEN, V-NOSCHEME, G3 |
| PLAIN [Add useful headings](sources/plain/guidelines/organize/add-useful-headings.md) | S-SUBHEADS |
| PLAIN [Effective headings](sources/plain/guidelines/organize/effective-headings.md) | S-SUBHEADS, S-MODULES |
| PLAIN [Have a topic sentence](sources/plain/guidelines/organize/have-a-topic-sentence.md) | M-ORDER, S-SCAN, S-PARA-LEAD |
| PLAIN [Organize the information](sources/plain/guidelines/organize/index.md) | M-GOAL, M-ORDER |
| PLAIN [Make it easy to follow](sources/plain/guidelines/organize/make-it-easy-to-follow.md) | M-ORDER |
| PLAIN [Place the main idea before exceptions and conditions](sources/plain/guidelines/organize/place-the-main-idea-before-exceptions-and-conditions.md) | S-BURIED, P-SPLIT, P-INLINELIST, G4 |
| PLAIN [Use lists](sources/plain/guidelines/organize/use-lists.md) | S-LIST, P-INLINELIST, V-SCREEN, V-SCHEME |
| PLAIN [Use transition words](sources/plain/guidelines/organize/use-transition-words.md) | S-PARA-MIX, P-REFERENT |
| PLAIN [Controlled comparative studies](sources/plain/guidelines/test/controlled-comparative-studies.md) | M-GOAL |
| PLAIN [Paraphrase testing](sources/plain/guidelines/test/paraphrase-testing.md) | M-GOAL, M-LEVEL, M-IDEAL, T-TERMS |
| PLAIN [Usability testing](sources/plain/guidelines/test/usability-testing.md) | S-TITLE |
| PLAIN [Avoid FAQs](sources/plain/guidelines/web/avoid-faqs.md) | M-IDEAL |
| PLAIN [Follow web standards](sources/plain/guidelines/web/index.md) | M-FACTS, T-NUMBERS, S-SCAN |
| PLAIN [Repurpose print material for the web](sources/plain/guidelines/web/repurpose-print-material.md) | M-DIGRESS |
| PLAIN [Avoid hidden verbs](sources/plain/guidelines/words/avoid-hidden-verbs.md) | W-NOMINAL |
| PLAIN [Avoid jargon](sources/plain/guidelines/words/avoid-jargon.md) | M-HOLLOW, M-LEVEL, W-CORP, W-BUREAU, W-ZAUM |
| PLAIN [Avoid noun strings](sources/plain/guidelines/words/avoid-noun-strings.md) | W-NOUNSTACK |
| PLAIN [Choose your words carefully](sources/plain/guidelines/words/index.md) | M-ABSTRACT, W-INTRO, W-ZAUM |
| PLAIN [Minimize abbreviations](sources/plain/guidelines/words/minimize-abbreviations.md) | M-LEVEL, M-OFFEND |
| PLAIN [Minimize definitions](sources/plain/guidelines/words/minimize-definitions.md) | M-ORDER, T-TERMS |
| PLAIN [Place words carefully](sources/plain/guidelines/words/place-words-carefully.md) | S-BURIED, P-SPLIT, P-CLUMSY |
| PLAIN [Use simple words and phrases](sources/plain/guidelines/words/use-simple-words-phrases.md) | P-EXPLETIVE, W-POLITE, W-CLICHE, W-BUREAU, W-ZAUM, W-VAGUE |
| PLAIN [Use the same terms consistently](sources/plain/guidelines/words/use-the-same-terms-consistently.md) | P-SYNONYMS |
| PLAIN example [Ambiguous Wording Rewritten](sources/plain/examples/ambiguity.md) | P-REFERENT |
| PLAIN example [Application Due Date](sources/plain/examples/application-due-date.md) | W-PASSIVE |
| PLAIN example [Application for Federal Assistance](sources/plain/examples/application-federal-assistance.md) | P-NESTED |
| PLAIN example [Car Safety](sources/plain/examples/car-safety.md) | V-DECOR, V-NOSCREEN |
| PLAIN example [Fungi Hazards and Flood Cleanup](sources/plain/examples/fungi-hazards.md) | S-PARA-LEAD |
| PLAIN example [Medicaid Eligibility](sources/plain/examples/medicaid-eligibility.md) | S-LIST |
| PLAIN example [Medicaid Open Door Initiative](sources/plain/examples/medicaid-initiative.md) | M-READER, S-CLICKBAIT, W-EVAL, W-CORP |
| PLAIN example [Monthly Due Date](sources/plain/examples/monthly-due-date.md) | V-NOSCHEME |
| PLAIN example [Protect Yourself from Natural Disasters](sources/plain/examples/natural-disasters.md) | M-GOAL, P-OVERLOAD, P-SPLIT |
| PLAIN example [Printer Recommendations](sources/plain/examples/printer-recommendations.md) | P-EXPLETIVE |
| PLAIN example [Register a Pesticide](sources/plain/examples/register-pesticide.md) | P-INACTION, W-NOMINAL |
| PLAIN example [Water Resources](sources/plain/examples/water-resources.md) | T-RATING |
| PLAIN example [Wordiness Made Spare](sources/plain/examples/wordiness.md) | P-INLINELIST, W-BUREAU |
| GOV.UK [A to Z style guide](sources/govuk/a-to-z-style-guide.md) | M-HOLLOW, M-ABSTRACT, M-EXAMPLE, M-LEVEL, M-OFFEND, M-FACTS, T-BS, T-HIDE, T-METAPHOR, S-TITLE, S-CLICKBAIT, S-SCAN, S-LIST, S-EXAMPLES, P-INLINELIST, P-GLUED, P-PARCEL, W-POLITE, W-CLICHE, W-CORP, W-PASSIVE, V-SCREEN, G2, G4, G5 |
| GOV.UK [Write effective links](sources/govuk/add-links.md) | T-RATING, S-OUTRO |
| GOV.UK [Use clear language](sources/govuk/clear-language.md) | M-HOLLOW, M-ABSTRACT, M-LEVEL, T-BS, T-NUMBERS, S-WALL, P-OVERLOAD, P-FOCUS, W-CORP, W-ZAUM, W-NOMINAL, W-PASSIVE, G2, G4 |
| GOV.UK [Create a clear structure for your content](sources/govuk/clear-structure.md) | M-DIGRESS, M-IDEAL, S-SCAN, S-SUBHEADS, S-INTRO, S-PARA-LEAD, S-BURIED |
| GOV.UK [Write clear titles](sources/govuk/clear-titles.md) | T-TITLE, S-TITLE |
| GOV.UK [Write content to meet user needs](sources/govuk/meet-user-needs.md) | M-READER, M-GOAL, M-DIGRESS, M-FACTS, G3 |
| GOV.UK [Use the right tone](sources/govuk/right-tone.md) | M-OFFEND, T-BS, T-PERSONAL, S-CLICKBAIT, P-FOCUS, P-REFERENT, W-INTRO, W-POLITE, W-EVAL, W-BUREAU, G5 |
| GOV.UK [Write clear summaries](sources/govuk/summaries.md) | T-TITLE, S-SCAN, S-INTRO |
| GOV.UK [Technical A to Z style guide](sources/govuk/technical-a-to-z.md) | M-EXAMPLE, M-LEVEL, M-OFFEND, S-EXAMPLES, P-INACTION, W-EVAL, W-CORP, W-ZAUM, W-VAGUE, V-SCREEN |
| Strunk [Sources](sources/README.md) | V-RIGHTS |
| Strunk [II. Elementary rules of usage](sources/strunk/2-elementary-rules-of-usage.md) | P-GLUED, P-PARCEL |
| Strunk [III. Elementary principles of composition](sources/strunk/3-principles-of-composition.md) | M-DIGRESS, M-HOLLOW, M-ABSTRACT, M-NOEXAMPLE, M-EXAMPLE, M-ROBOT, T-HIDE, T-PERSONAL, S-MODULES, S-OUTRO, S-WALL, S-PARA-LEAD, S-PARA-MIX, S-LIST, P-OVERLOAD, P-SPLIT, P-NESTED, P-GLUED, P-INACTION, P-FOCUS, P-CLUMSY, P-PARCEL, P-SYNONYMS, P-EXPLETIVE, P-REFERENT, W-INTRO, W-PROP, W-EVAL, W-NOMINAL, W-PASSIVE, W-VAGUE, V-NOSCHEME, G1, G2, G3 |
| Strunk [V. Words and expressions commonly misused](sources/strunk/5-words-commonly-misused.md) | T-BS, T-NUMBERS, T-METAPHOR, T-TERMS, S-CLICKBAIT, S-INTRO, P-GLUED, P-CLUMSY, W-INTRO, W-PROP, W-POLITE, W-EVAL, W-INTENS, W-CLICHE, W-VAGUE |
| George Orwell, "Politics and the English Language" (cited by name and chapter) | M-HOLLOW, M-ROBOT, T-HIDE, W-INTRO, W-EVAL, W-CLICHE, W-ZAUM, W-NOMINAL, W-PASSIVE, G1 |
| Joseph M. Williams, *Style* (cited by name and chapter) | P-INACTION, P-FOCUS, W-NOMINAL, W-PASSIVE |
| Steven Pinker, *The Sense of Style* (cited by name and chapter) | M-ABSTRACT, M-ORDER, M-LEVEL, S-PARA-MIX, P-SPLIT, P-NESTED, P-CLUMSY, W-INTRO, W-INTENS, W-ZAUM, W-NOMINAL |
| Barbara Minto, *The Pyramid Principle* (cited by name and chapter) | M-ORDER, S-INTRO, S-PARA-LEAD, S-BURIED |
| William Zinsser, *On Writing Well* (cited by name and chapter) | M-HOLLOW, W-INTRO, W-INTENS, W-CLICHE, W-NOUNSTACK |
| H. W. Fowler, *Modern English Usage* (cited by name and chapter) | T-TERMS, P-SYNONYMS, W-CLICHE, W-ZAUM |
| Darrell Huff, *How to Lie with Statistics* (cited by name and chapter) | T-NUMBERS |

Source files no entry cites yet (11): `sources/govuk/how-to-use.md`, `sources/govuk/writing-guidelines-index.md`, `sources/plain/examples/employment-assistance.md`, `sources/plain/examples/index.md`, `sources/plain/examples/lead-warning.md`, `sources/plain/examples/use-less-water.md`, `sources/plain/guidelines/conversational/use-the-present-tense.md`, `sources/plain/guidelines/index.md`, `sources/plain/guidelines/test/index.md`, `sources/plain/guidelines/web/avoid-pdf-overload.md`, `sources/plain/guidelines/web/write-effective-links.md`.
