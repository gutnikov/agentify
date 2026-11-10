# -*- coding: utf-8 -*-
"""Briefs for the writing agent. dev: tune the prompt; test: measure the result once.

English adaptations of rutalk's briefs: the same facts, the same gaps and the same traps
(vague numbers, empty quotes, missing "what if" answers). Names, currencies and places are adapted.
"""
import json, os

B = []

def add(id, split, genre, task, context):
    B.append(dict(id=id, split=split, genre=genre, task=task.strip(), context=context.strip()))

# ---------------------------------------------------------------- dev

add('d01', 'dev', 'newsletter about a new feature', """
Write a newsletter email to customers about the launch of joint accounts. Facts: from 4 November, customers can open a joint account in the app; up to 4 members; each member gets their own card (a virtual one straight away, a physical one on request, delivered in 5–7 days); the account owner sets spending limits for each member; only bank customers over 18 can be members; free on the Prime plan, €2.99 a month on Standard; to open one: Accounts → "+" → "Joint account" → invite by phone number. Marketing wants to stress that this is an innovative and convenient solution for families and friends that will make shared finances transparent and simple. Length: up to 1,500 characters.
""", "a bank's newsletter to customers about a new feature; reader: a mobile banking customer; goal: understand what a joint account is, who it is for, what it costs and how to open one")

add('d02', 'dev', 'about the company', """
We need a text for the "About us" page on our website. We are Codelab, a dynamic, fast-growing company, a team of professionals, an individual approach to every client, full-cycle turnkey development. Facts: founded in 2014 in Leeds; 45 developers; we build mobile apps and back ends for retail and logistics; we built a loyalty app for the supermarket chain Basket (2.1 million installs) and a courier tracking system for the delivery service Runner (a pilot in Yorkshire); stack: Kotlin, Swift, Go; every project starts with a two-week audit for £3,000, and its cost counts towards the price of the project; 12-month warranty on bug fixes. We'd like the text to sell.
""", "the \"About us\" page on an IT contractor's website; reader: a manager in retail or logistics who is choosing a contractor; goal: understand what the company does and for whom, and decide whether to get in touch")

add('d03', 'dev', 'outage notice', """
Write an email to customers about yesterday's outage. Draft from PR: "Dear customers, On 23 October, due to technical works on the side of a partner, minor difficulties were observed in the processing of certain transactions. We apologise for any inconvenience caused. At the present time, all services are functioning as normal." Facts: on 23 October from 14:10 to 16:40 Berlin time, card payments in shops and online did not go through — about 12% of transactions were declined; the cause was an equipment failure at our card-processing partner; transfers and cash withdrawals worked; money for declined transactions was not taken, but some customers may have had the amount temporarily blocked — it will be released automatically within 5 business days; if it has not been released, write to support in the in-app chat; by the end of the year we will connect a backup processing partner, so that if one fails, payments go through the other.
""", "email to bank customers about a card payment outage; reader: a customer whose payment may have been declined; goal: understand what happened, what is happening with their money and what to do")

add('d04', 'dev', 'price increase notice', """
Message to customers about a price increase for a plan. From 1 January 2027 the Standard plan will cost €2.99 a month instead of €0. The reason: the payment networks have raised their card fees, and the customer checks the regulator requires have become more expensive. The plan stays free if the customer spends €500 or more a month by card. The Prime plan does not change (€9.99 a month). Customers can switch plans or close their account free of charge until 31 December in Profile → Plan. If they do nothing, the fee will be charged automatically from 1 January. Management asks for gentle wording so that customers don't leave.
""", "notice to bank customers about a change to their plan; reader: a customer on the Standard plan; goal: understand what changes and when, how to keep paying nothing and what to do if they disagree")

add('d05', 'dev', 'how-to guide', """
Write a help centre article: how to dispute a card transaction. Facts: a customer can dispute a transaction they did not make, or one where the goods were not delivered or the service was not provided; for goods that were not delivered, they must first write to the seller; in the app: open the transaction → "Dispute transaction" → choose a reason → attach documents (correspondence with the seller, receipt, proof that the goods were returned) → send; if the customer did not make the transaction, they must first block the card in the app; a dispute can be filed within 120 days of the transaction date; review takes up to 45 days, sometimes up to 90; during the review the amount may be temporarily returned to the account, and if the dispute is decided in the seller's favour, it may be taken again; the status of a dispute can be checked in the support chat.
""", "help centre article of a mobile bank; reader: a customer with a transaction they want to dispute; goal: understand whether it can be disputed and file the dispute correctly")

add('d06', 'dev', 'explainer article', """
Blog article for investing beginners: what an ETF is and how buying an ETF differs from buying individual shares. Length: 3,000–4,000 characters. What matters to get across: an ETF is a fund that buys many securities by a set rule (for example, it tracks an index); if you buy one share of it, you get a small piece of all the fund's securities; the fund's fee (TER) is usually 0.05–0.5% a year; risks: an ETF falls together with the market, and there is currency risk; an ETF on the S&P 500 index includes about 500 companies; in our app you can buy ETFs from €1. The readers understand nothing about investing.
""", "article on a bank's blog; reader: a beginner with no investing experience; goal: understand what an ETF is, how it differs from buying individual shares and what its risks are")

add('d07', 'dev', 'cold sales email', """
Cold email to the finance director of a small company (20–100 employees) offering our corporate cards. Facts: we issue a virtual card to an employee in one minute and deliver a physical card in 3–5 days; a limit can be set on each card; the employee photographs the receipt in the app, and the receipt is attached to the transaction; transactions export to DATEV and CSV; €5 a month per card, the first 3 months free; we offer a 20-minute demo call. We want to show that we are the market leader and a reliable partner.
""", "cold sales email; reader: the finance director of a small company who did not expect the email; goal: understand which of their problems the offer solves and agree to a demo")

add('d08', 'dev', 'job ad', """
Job ad for a Senior Backend Developer (Kotlin). From HR: "We're a close-knit team of professionals with ambitious challenges, a modern stack, free cookies and room to grow. We're looking for a responsible, sociable candidate who thrives under pressure and has a real fire in their belly." Facts: the product is a payment service for small businesses; the payments team has 8 people; stack: Kotlin, Spring Boot, PostgreSQL, Kafka, Kubernetes; tasks for the next six months: rewrite the fee calculation service and add two new payment methods; required: at least 4 years of experience with Kotlin or Java and experience with high-load systems; salary €6,000–7,500 a month before tax; remote from the EU or in the Berlin office; 30 days of holiday; €1,500 a year for learning.
""", "job ad; reader: an experienced backend developer who is choosing a job; goal: understand what the job is and what the terms are, and decide whether to apply")

add('d09', 'dev', 'internal email', """
Email to all staff from the office administration team. From 10 November the office moves from the 3rd to the 5th floor of the same building (Friedrichstraße 68). Old passes will stop working on 10 November. A new pass must be collected from reception on the ground floor between 3 and 7 November, from 9:00 to 18:00; bring an ID document. Anyone on holiday or working remotely can collect their pass from security on 10 November from 8:00. Personal items on desks must be packed into boxes (handed out on 6 November) and labelled by 17:00 on 7 November. Parking spaces stay the same. Questions: Anna Schulz, anna.schulz@company.de.
""", "internal email to all staff; reader: an office employee; goal: understand what to do for the move and by when")

add('d10', 'dev', 'news post', """
News post for the company blog on third-quarter results. Facts: the number of customers grew to 1.2 million (18% more than in the second quarter); revenue was €14.3 million (second quarter: €11.9 million); we launched in the Netherlands and Portugal; we released joint accounts and ETF investing; 61% of customers use their card every week; the average account balance rose from €820 to €1,040. The CEO says: "We are proud of our team and grateful to our customers for their trust."
""", "news post on a fintech company's blog; reader: customers, journalists and partners; goal: learn the main results of the quarter")

add('d11', 'dev', 'support reply', """
Reply in the support chat. The customer writes: "You've blocked my account without any explanation!!! My salary is in there, I have nothing to pay my rent with. This is theft, I'm going to complain!" Facts: the account is restricted (incoming payments are accepted; outgoing payments and the card don't work) because of a check the bank is required to carry out under anti-money-laundering law; we can't name the specific reason for the check; to lift the restriction, the customer needs to upload a document showing where the money comes from (for example, an employment contract or the last three payslips) in the app under Profile → Documents; the check takes 3–5 business days after the upload; an urgent rent payment can be made through support: if the customer sends the landlord's invoice, we will make the transfer manually within the day; a complaint can be filed through the form on the website, but it won't speed up the check.
""", "a bank's support reply in chat; reader: an upset customer whose account is restricted; goal: understand what happened, what to do to lift the restriction and how to pay the rent now")

add('d12', 'dev', 'product description', """
Description of wireless headphones for a product page in an online shop. Model: SoundCore Q40. Specs: hybrid noise cancelling, up to −35 dB; 30 hours of playback with noise cancelling, 45 without; fast charging: 10 minutes gives 4 hours of music; weight 250 g; Bluetooth 5.3, connects to two devices at once; IPX4 splash resistance; foldable, case included; price £79.90. The buyers are people who commute by underground and fly a lot.
""", "product description in an online shop; reader: a shopper choosing headphones for travel; goal: understand whether these headphones suit them and decide whether to buy")

add('d13', 'dev', 'Telegram post', """
Post for the bank's Telegram channel: cashback categories for November. Facts: 5% on cafés and restaurants, 3% on taxis, 10% on cinemas (a new category), 1% on everything else; the cashback cap is €50 a month; cashback is paid on the 5th of the following month; customers must choose their categories in the app by 3 November (Cashback → Choose categories); with no choice, they get 1% on everything. The post should be bright and catchy.
""", "post in a bank's Telegram channel; reader: a channel subscriber who is a customer of the bank; goal: learn the November cashback categories and choose them in time")

add('d14', 'dev', 'landing page', """
Copy for a savings account landing page: headline, subheading, three benefit blocks (heading + 1–2 sentences), button text. Facts: 2.5% a year; interest is calculated every day and paid into the same account once a month; money can be withdrawn at any time without losing interest; the rate is guaranteed until 31 March 2027 and may change after that; deposits are protected by Germany's statutory deposit guarantee scheme up to €100,000; the account opens in 2 minutes in the app, with no branch visit; there is no minimum amount. We want it to sound modern and like a great deal.
""", "landing page for a savings account; reader: someone looking for a place to keep their savings at interest; goal: understand the terms and open an account")

add('d15', 'dev', 'tips article', """
Blog article: how to make a personal budget if you have never done it before. 3,000–4,000 characters. We want to give a practical step-by-step method. You can mention that our app has automatic spending categories and limits per category.
""", "article on a bank's blog; reader: someone who has never kept a budget; goal: start keeping a budget with a clear method")

add('d16', 'dev', 'feedback to an employee', """
Write written feedback for the half-year review of Tom, a developer (his manager will send it under their own name). Facts: of 5 tasks with a deadline, Tom delivered 2 on time and 3 late, by 1–3 weeks; colleagues wait an average of 4 days for his code reviews, against a norm of 1 day; at the same time, he mentors juniors well: the two juniors he mentored passed their probation, and both mention his help; he proposed and built caching that cut the load time of the home screen from 2.1 to 0.8 seconds. The manager thinks Tom is irresponsible but doesn't want to demotivate him. The agreements to reach: estimate deadlines together with the team lead, do code reviews within one working day.
""", "written feedback from a manager to an employee; reader: Tom, a developer; goal: understand what is going well, what needs to change and what was agreed")

add('d17', 'dev', 'invitation', """
Webinar invitation (email). Topic: taxes for freelancers in Germany. 14 November, 19:00 Berlin time, 60 minutes + 20 minutes for questions. Host: Maria Keller, tax adviser (Steuerberaterin), 12 years of practice. We'll cover: how to register as a freelancer, which expenses you can deduct, how to make advance tax payments, what happens if you file your tax return late. Free; registration via the link [link]; we'll send the recording to everyone who registers.
""", "email invitation to a webinar; reader: a freelancer in Germany who is a customer of the bank; goal: understand what the webinar offers and register")

add('d18', 'dev', 'release notes', """
Release notes for version 5.12 for the App Store, Google Play and the "What's new" section. Changes: 1) transaction search now searches by amount and by comment; 2) a statement for any period can be downloaded as a PDF right in the app; 3) we fixed a bug that delayed payment notifications by up to an hour for some Android users; 4) we removed the "Spending analytics" section — fewer than 3% of customers used it; spending categories are now shown in the transaction history instead; 5) the app no longer supports iOS 15 — users need to update to iOS 16 or later. Friendly tone.
""", "app release notes in the app stores and the \"What's new\" section; reader: an app user; goal: understand what has changed and what they need to do")

add('d19', 'dev', 'cover letter', """
Cover letter for an application for a product designer job at a fintech startup, in the first person. About the candidate: 6 years in product design; the last 3 years at a grocery delivery service, where he redesigned checkout and the cart abandonment rate fell from 31% to 22%; ran more than 40 user interviews; led the design system (120 components) and two junior designers; works in Figma and ProtoPie, knows basic SQL for analytics; wants to move into fintech because he is interested in complex scenarios involving money and regulation. The candidate considers himself creative, responsible and a good communicator.
""", "cover letter for a job application; reader: the hiring manager at a fintech startup; goal: decide whether to invite the candidate to an interview")

add('d20', 'dev', 'help article', """
Help centre article: why hasn't my transfer arrived yet. Facts: transfers between the bank's customers are instant; a SEPA transfer takes 1 business day if sent before 15:00 Berlin time, otherwise the next business day; SEPA Instant takes up to 10 seconds, but only if the recipient's bank supports it, otherwise the transfer goes as a regular SEPA transfer; regular SEPA transfers are not processed at weekends and on public holidays; international transfers (SWIFT) take 2–5 business days; a transfer may be held for a security check for up to 2 business days, in which case we let you know in the app; if more than 5 business days have passed, write to support and include the transfer number (it's in the transaction details).
""", "help centre article of a mobile bank; reader: a customer waiting for a transfer; goal: understand whether the delay is normal and what to do")

# ---------------------------------------------------------------- test (held out)

add('t01', 'test', 'welcome email', """
Welcome email to a new user of the fitness app Pulse after sign-up. Facts: the free trial lasts 14 days, then €7.99 a month; the subscription can be cancelled in the settings at any time before the trial ends, and then there will be no charges; the app has more than 300 workouts from 7 to 45 minutes long, no equipment needed; first steps: take the level test (3 minutes), choose a goal (weight loss, strength or flexibility), and the app will build a 4-week plan; workout reminders can be set up. We want the email to motivate.
""", "welcome email after sign-up to a fitness app; reader: a new user; goal: start the first workout and understand the terms of the trial")

add('t02', 'test', 'incident notice', """
Notice to the users of an online shop about a security incident. Facts: on 19 October, unauthorised people gained access to the database of our contractor's mailing service; the names and email addresses of about 40,000 users were exposed; passwords, card details and order history were not affected — they are stored in a different system; the contractor shut off the access on 20 October; we have reported it to the data protection authority; the risk is phishing emails in the shop's name; we never ask for a password or an SMS code in emails; what to do: don't click links in suspicious emails, and if in doubt, check your orders in the app; questions: privacy@shop.example. Legal asks us not to use the word "breach".
""", "notice to the users of an online shop about a security incident; reader: a user whose data may have been exposed; goal: understand what happened, what is at risk and what to do")

add('t03', 'test', 'explainer article', """
Article for people who have recently moved to Germany: what SCHUFA is and why it matters. 3,000–4,000 characters. Facts: SCHUFA is a private credit agency that holds data on loans, bank accounts, mobile phone contracts and late payments; landlords often ask for a SCHUFA report when they let a flat; banks check it before giving a loan and sometimes before issuing a credit card; newcomers have no history — this is not a bad score, but it raises questions with some landlords and banks; a free report (Datenkopie under Article 15 of the GDPR) can be ordered once a year on the SCHUFA website; the score is affected by late payments, the number of loans and the length of the credit history; requests for loan terms (Konditionsanfrage) don't affect the score.
""", "article on a bank's blog; reader: someone who has recently moved to Germany; goal: understand what SCHUFA is, why it matters and how to get a report")

add('t04', 'test', 'sales proposal', """
Sales proposal from the cleaning company Clean Slate to office managers in a business centre. From the director: "We are professionals with many years of experience, we use only high-quality products and modern equipment, a flexible discount system, an individual approach." Facts: daily office cleaning costs £1.50 per m² a month; the cleaner comes before 8:30 am or after 7 pm so as not to disturb staff; products certified with the EU Ecolabel; if something has not been cleaned, we clean it again free of charge within 2 hours; the contract can be ended with 14 days' notice; in business since 2016, currently cleaning 37 offices; the trial week is free.
""", "sales proposal; reader: an office manager choosing a cleaning company; goal: understand the terms and agree to a trial week")

add('t05', 'test', 'how-to guide', """
Help article: how to turn on two-factor login in the app. Facts: Settings → Security → Two-factor login → choose a method: an authenticator app (Google Authenticator, Authy and similar) or SMS; for an authenticator, scan the QR code and enter the 6-digit code from the app; be sure to save the 10 backup codes — without them, if you lose your phone, you can only regain access through an identity check with support, which takes up to 5 business days; if the code doesn't work, check that the time on the phone is set automatically; SMS may not arrive when roaming.
""", "help article; reader: an app user who wants to protect their account; goal: turn on two-factor login without losing access")

add('t06', 'test', 'press release', """
Press release: Nordbank and the pharmacy chain Health+ are launching a co-branded card. Facts: launch on 1 December; the card is free; 5% cashback in points at the chain's pharmacies (1 point = €1 to spend in the chain), 1% in money at other shops; the chain has 420 pharmacies in Germany and Austria; the card can be ordered in the bank's app or at a pharmacy checkout via a QR code; a quote from the bank's director of business development, Thomas Braun: "This is an important step in our strategy to get closer to our customers and offer them even more value." The press release will go to the media and on the website.
""", "press release; reader: journalists and customers; goal: understand what is being launched, when, and what the customer gets")

add('t07', 'test', 'feature shutdown notice', """
Notice to customers that crypto trading in the app is ending. Facts: from 15 January 2027 it will no longer be possible to buy crypto in the app; until 15 March 2027 customers can sell their crypto or withdraw it to an external wallet (withdrawals incur a network fee; our fee is 0); if a customer does nothing by 15 March, we will sell their crypto at the market price on 16 March and credit the euros to their main account, and tax may be due on any gains; the reason: our crypto custody partner is leaving the EU market, and we have not found a new partner that meets the requirements of the MiCA regulation. Write carefully so that customers don't panic.
""", "notice to bank customers about the end of crypto trading; reader: a customer who holds crypto in the app; goal: understand what will happen, by which dates, and what to do")

add('t08', 'test', 'fundraising page', """
Text for a fundraising page of the charity Warm Home. The goal is £18,000 to repair the roof and heating of a care home for older people in the village of Elmsworth in Cumbria, where 26 people live; last winter the temperature in the rooms dropped to 12 °C; the estimate: roof £11,000, boiler and pipes £7,000; the work must be finished by 1 December; £6,400 has been raised so far; when the work is done, the charity publishes a report with receipts on its website. We want the text to be moving.
""", "fundraising page; reader: someone deciding whether to help; goal: understand what the money is for and how much is left to raise, and donate")

add('t09', 'test', 'comparison article', """
Blog article: debit or credit card — which to choose. 3,000–4,000 characters. Facts about our products: the debit card is free, and with it you spend your own money; the credit card has a limit of up to €5,000 and an interest-free period of up to 50 days, then 14.9% a year; it has no monthly fee if you spend €300 or more a month on it, otherwise €4.99 a month; a credit card is needed to rent a car or book a hotel with a deposit — many rental companies don't accept debit cards; a credit card shows up in SCHUFA. Marketing's goal is to issue more credit cards.
""", "article on a bank's blog; reader: a customer choosing a type of card; goal: understand the difference and choose the right card")

add('t10', 'test', 'Slack message', """
A short message from HR in the company's general Slack channel: a request to take the annual engagement survey by Friday, 31 October. The survey is anonymous, 15 questions, about 7 minutes, link [link]. After last year's survey we introduced flexible hours on Fridays and a sports allowance. So far 38% of employees have taken the survey, and for the results by department to be reliable, we need at least 70%.
""", "message in a company's general Slack channel; reader: an employee; goal: take the survey by Friday")

add('t11', 'test', 'about us (café)', """
"About us" text for the website of the café Sushka in Edinburgh. From the owner: "A cosy café with a soulful atmosphere, where the tastiest home cooking is made with love." Facts: opened in 2021; the owners are a family from Novosibirsk, and the cooking is done by the owner's mother, Galina; on the menu: hand-made pelmeni (made every morning, about 600 of them), borscht, syrniki, blini; dough and fillings are made in-house, with no ready-made products; 28 seats; a lunch deal from 11:30 to 15:00 for £11.90 (soup, main course and mors, a berry drink); there is a children's corner; open every day except Monday, from 11:00 to 22:00.
""", "the \"About us\" page on a café's website; reader: an Edinburgh resident looking for somewhere to eat; goal: understand what kind of café it is and decide to come")

add('t12', 'test', 'rules', """
Rules for using a coworking space, for new members (they will be on the website and in the newsletter). Facts: 24/7 access with the member card; meeting rooms are booked in the app, for no more than 2 hours in a row, and a booking is cancelled if the member doesn't arrive within 15 minutes; make calls in the phone booths or in the kitchen — the open area is a quiet zone; guests are registered at reception, no more than 2 guests at a time, and a guest can't stay after 20:00; strong-smelling food only in the kitchen; wash your own dishes; fixed desks only on the Fix plan; a lost card costs €20. Signature: "Coworking management".
""", "rules of a coworking space for members; reader: a new member; goal: understand what is and isn't allowed without feeling that the rules exist for their own sake")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'briefs.jsonl')
    with open(out, 'w', encoding='utf-8') as f:
        for b in B:
            f.write(json.dumps(b, ensure_ascii=False) + '\n')
    print(len(B), 'briefs ->', out)
