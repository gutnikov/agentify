<!-- Source: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/technical-a-to-z/ — Contains public sector information licensed under the Open Government Licence v3.0. Fetched 2026-11-04. -->



#  Technical A to Z style guide

This section only covers style conventions for technical content on GOV.UK.

If you cannot find something, look at the [style guide A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/) which covers style conventions for all content on GOV.UK.

If you want to suggest a change, read the [guidance on how to use the style guide](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/how-to-use/).

## A

### API

Do not expand the abbreviation for technical users.

### API endpoints

Use `methodname endpoint` for an API endpoint. Do not include the base path. Use {CAPS_WITH_UNDERSCORES_INSIDE_CURLY_BRACKETS} for placeholder parameters in endpoints.

For example:

GET /v1/payments/{PAYMENT_ID}/

Replace:

- `{PAYMENT_ID}` with the ID of the payment you’re checking
- `{REFUND_ID}` with the ID of the refund you’re checking

### API headers

There are lots of HTTP and API headers, so use code style and the exact name of API headers, to make it clear which header you mean. For example:

- `Authorisation` header
- `Content-type` header - not `Content header` because there are several different content headers

Example:

You must include an `Authorisation` header in your request.

### API key

Do not expand the abbreviation for technical users. Use:

- create an API key – not generate
- revoke an API key

### API parameters and fields

Use:

- parameter for API request items, not ‘option’
- field for API response items, not ‘variable’
- object, not ‘dictionary’ or ‘array’ – for example: If the `status` in the `refund_summary` object is `available`…
- key
- value
- key-value pair

Parameters are required or optional. Do not use ‘you do not need’ (which is ambiguous) or ‘you can leave out’.

### API requests

Use ‘API request’ not ‘API call’.

Tell users they can ‘include’ a parameter in an API request, not that they can ‘supply’ a parameter.

[Back to top]

## B

### backend

Not ‘back-end’ or ‘back end’.

### bold

Only use [bold in text from interfaces](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/#bold).

### breaking changes

‘Breaking changes’ are changes to one part of your software system that may cause other parts to fail. Do not use this term without explaining it – user research shows not all technologists immediately understand what it means.

[Back to top]

## C

### choose

Use ‘choose’ where there’s a genuine choice (like ‘choose what time you want your appointment’) and ‘select’ when you’re indicating the appropriate response (like ‘select your year of birth’).

### Cloud First policy

Capitalise Cloud First.

### Cloud Security Principles

Upper case.

### code samples

Format code samples or excerpts in a fixed width font. You usually do this by adding either:

- backticks (```) around code excerpts inside sentences
- 3 backticks (````````) above and below code blocks

### code styling

Use code styling for the following, which is based on the [code styling list in Google’s style guide](https://developers.google.com/style/code-in-text):

- classes, methods and functions
- terminal commands
- fields - names and values
- data types
- filenames, extensions, paths and folders
- HTML element names
- HTTP status codes
- HTTP methods - for example GET and PUT
- placeholder variables

### Components that control other components

Use:

- primary for a component that controls other components
- secondary for a component that’s controlled by the primary component

Do not use master or slave.

### conditions

Use:

- ‘you must’ for a requirement
- ‘you should’ for a recommendation
- ‘you can’ for an option or possibility

Do not use:

- it may be possible to - use ‘you can’
- you may want to - use ‘you can’
- where possible you - use ‘where you can’

Do not use block capitals. It’s an accessibility issue, and user research shows that it does not help users recognise and understand requirements.

### credential issuer

Write ‘credential issuer’ the first time you refer to a credential issuer. You can then use ‘issuer’ throughout the content.

Do not abbreviate ‘credential issuer’ to ‘CI’ or ‘CRI’.

### CSS

Do not expand the abbreviation.

### custom

We use this to mean ‘your own’, for example in:

- add a custom paragraph
- add custom metadata

[Back to top]

## D

### data type

Not ‘datatype’.

### data

Use the following:

- get data
- store data
- access data
- share data - not exchange data, unless data is going both ways

Treat data as a singular noun, so use ‘the data is accurate’ not ‘the data are accurate’.

### Digital Marketplace

Upper case.

### disable

See ‘turn on’.

### domain name

Lower case.

### Domain Name System (DNS)

Upper case.

### downtime

One word, lower case.

[Back to top]

## E

### elements

For example:

Using the correct elements in your HTML helps users of assistive technologies navigate through your pages.

### example code

Before you give example code, describe what it does or how to use it, for example: ‘Run the following code to…’

### enable

See turn on.

### existing technology

Be clear whether you mean the user’s existing technology, existing third-party technology or something else.

[Back to top]

## F

### filename

Not ‘file name’.

### fix

Not ‘address’.

### folder

Not ‘directory’.

### follow the guidance on

For example: follow the guidance on [naming and registering government websites] (link).

### frontend

Not ‘front-end’.

[Back to top]

## G

### get

Use instead of ‘receive’ for API responses, emails and so on.

### get started

Not .quickstart. or .quick start. - words like ‘quick’ can demoralise users if they do not find the task quick.

### Git

Capital ‘G’ (as used on [Git’s own website](https://git-scm.com/about/small-and-fast)), unless it’s the `git` command within code.

### GitHub

Capital ‘G’, capital ‘H’ - as used on the [GitHub website](https://github.com/about).

### Google Chrome

Not ‘Chrome’.

### GOV.UK Design System

Upper case.

### GOV.UK Forms

Upper case.

### GOV.UK One Login

Upper case.

### GOV.UK Pay

Upper case.

### GOV.UK Platform as a Service

Write out in full for first mention, then GOV.UK PaaS.

### GraphQL

One word.

[Back to top]

## H

### hackers

Use ‘hackers’ instead of ‘actors’ or ‘hostile actors’.

For example, ‘Set a password that hackers cannot guess’.

### HTTPS

Upper case. Do not expand the abbreviation.

### HTTP status codes

For example, a `200` HTTP status code. Use code styling for the status code.

### HTTP Strict Transport Security (HSTS)

Write out in full on first mention, then HSTS.

[Back to top]

## I

### Identity and Access Management (IAM)

Write out in full on first mention, then IAM.

### Internet Explorer

Not ‘IE’.

### iOS

Lower case i, capital OS.

### ID

Use ‘ID’ or ‘unique ID’, not ‘identifier’. Do not expand the abbreviation.

### information

- store information
- share information, not ‘exchange’
- get information, not ‘access’
- handle or contain information, not ‘hold’

### IP

Do not expand the abbreviation.

[Back to top]

## J

### JavaScript

Capital J, capital S.

### JAWS

Not ‘Jaws’.

[Back to top]

## L

### legacy

Make sure you explain what you mean by legacy.

For example: ‘Government uses a lot of older technology that’s tied into costly contracts. These technologies are known as legacy systems.’

[Back to top]

## M

### macOS

Lower case m.

### MD5

Do not expand the abbreviation.

### meet needs

Not suit needs.

### microservices

Not micro services or micro-services.

### Mozilla Firefox

Upper case.

[Back to top]

## N

### National Cyber Security Centre (NCSC)

Upper case.

### NVDA

NonVisual Desktop Access. Expand the abbreviation on first use, and consider linking to [information about NonVisual Desktop Access](https://www.nvaccess.org/about-nvda/) or GDS documentation that explains its use.

[Back to top]

## O

### onscreen

One word.

### Open Standards Board

Upper case.

### open standards

Lower case. For example: ‘use open standards’, or ‘follow open standards principles’.

[Back to top]

## P

### PHP

Do not expand the abbreviation.

### placeholders

Use < CAPS_WITH_UNDERSCORES_INSIDE_ANGLE_BRACKETS > for placeholders in sample code, and explain the placeholder under the code sample. For example:

```

Authorization: < API_KEY >

```

Replace `API_KEY` with the API key we sent you.

### problems

Not ‘issues’ or ‘defects’.

### Progressive web apps (PWAs)

Expand the abbreviation on first use.

### Python

Upper case.

[Back to top]

## R

### render

Use for HTML.

For example: ‘If the CSS or JavaScript fails, your user’s browser still renders the HTML correctly.’

### REST

Upper case. Do not expand the abbreviation if you’re writing for API developers.

Use ‘a REST API’ instead of ‘a RESTful API’. If you need to, include RESTful in brackets after the first use of REST. For example: ‘Our API follows REST principles (it’s ‘RESTful’)’.

### Ruby

Upper case.

### Ruby on Rails

If you say Ruby on Rails (‘Rails’) the first time, you can use just ‘Rails’ afterwards.

[Back to top]

## S

### screen reader

Not ‘screenreader’.

### service

Avoid ‘online service’ unless you’re distinguishing it from other kinds of service.

### set up

Not ‘instantiate’, ‘spin up’ or ‘stand up’.

For example: ‘Set up a server by…’

### smoke test

Lower case.

### SOAP

Do not expand the abbreviation if you’re writing for API development teams.

### SQL

Do not expand the abbreviation.

[Back to top]

## T

### (a) terminal

Not ‘the command-line’ or ‘the command-line interface’, or ‘Terminal’ (which is the macOS terminal specifically).

### test

Ask users to ‘run’ a test, not ‘conduct’, ‘execute’ or ‘perform’.

### test environment

Not ‘prototype environment’ - user research shows this causes confusion.

### third parties

For conciseness use only ‘a third party’ instead of ‘a third-party organisation’.

### Technology Code of Practice (TCoP)

Upper case. Write out in full for first mention, then use TCoP.

### turn on

Use:

- ‘turn on’, not ‘enable’
- ‘turn off’, not ‘disable’, ‘mute’ or ‘silence’

[Back to top]

## U

### uptime

One word, lower case.

[Back to top]

## V

### verifiable credential (VC)

Lower case.

### version

To avoid ambiguity, use:

- the latest version
- the latest stable version
- the previous version
- an earlier version
- a later version

### VoiceOver

One word.

[Back to top]

## W

### Web Content Accessibility Guidelines (WCAG)

Use the full name the first time on a page. Where you need to, specify the version, for example: “Public sector websites and applications must meet the Web Content Accessibility Guidelines (WCAG) version 2.1 AA standard”.

### Words to avoid

- action as a verb - use ‘do’
- action as a noun - use ‘task’
- allow - use ‘let’
- assets - use ‘files’ or ‘documents’
- consult - use ‘check’
- detail (as a verb) - use ‘explain’ or ‘tell’
- easy or easily - this can demoralise users if they do not find it easy
- enable - use ‘help’
- ensure - use ‘make sure’
- examine - use ‘check’, ‘assess’ or ‘review’
- fulfil - use ‘meet’
- in order to - use ‘so you can’
- inform - use ‘show’ or ‘tell’
- interrogate - use ‘monitor’ or ‘track’
- periodically - try to be specific
- quick - this can demoralise users if they do not find it quick
- refer to - use ‘Read more about [xxx]’ for an internal link or ‘You can find out how to [xxx] on the yyy website’ for an external link
- regularly - try to be specific
- requires - use ‘needs’
- should the - use ‘if the’
- simple - this can demoralise users if they do not find it simple
- take place - use ‘happen’, or use active voice to start with the verb
- underlying - this can usually be removed without losing the sentence’s meaning

[Back to top]

