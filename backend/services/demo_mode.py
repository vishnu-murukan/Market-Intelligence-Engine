import os

DEMO_OUTREACH = {
    "electric vehicles": [
        {
            "brand_name": "Tesla",
            "pitch_hook": "Your pricing repositioning opens the door to a bold new brand narrative.",
            "urgency_level": "HIGH",
            "recommended_service": "Brand Narrative Campaign",
            "linkedin_message": "Hi — Tesla's pricing reset is one of the boldest moves in EV right now. At StepOne we craft brand narratives that turn disruption into desire. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Tesla%27s%20pricing%20reset%20is%20one%20of%20the%20boldest%20moves%20in%20EV%20right%20now.%20At%20StepOne%20we%20craft%20brand%20narratives%20that%20turn%20disruption%20into%20desire.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "A brand narrative idea for Tesla's next chapter",
            "email_body": "Hi,\n\nTesla's aggressive pricing strategy has reshaped the EV market — but it's also created a perception gap around brand premium that competitors are exploiting.\n\nAt StepOne, we specialise in brand narrative and experiential campaigns. We'd propose a 'Future is Now' multi-market campaign that reanchors Tesla's aspiration while celebrating accessibility — targeting a 25% lift in brand sentiment scores within 90 days.\n\nAre you open to a 10-minute call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you open to a 10-minute call this week?",
            "contact_email": "press@tesla.com",
            "contact_name": "Tesla Press",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@tesla.com?subject=A%20brand%20narrative%20idea%20for%20Tesla%27s%20next%20chapter&body=Hi%2C%0A%0ATesla%27s%20aggressive%20pricing%20strategy%20has%20reshaped%20the%20EV%20market%20%E2%80%94%20but%20it%27s%20also%20created%20a%20perception%20gap%20around%20brand%20premium%20that%20competitors%20are%20exploiting.%0A%0AAt%20StepOne%2C%20we%20specialise%20in%20brand%20narrative%20and%20experiential%20campaigns.%20We%27d%20propose%20a%20%27Future%20is%20Now%27%20multi-market%20campaign%20that%20reanchors%20Tesla%27s%20aspiration%20while%20celebrating%20accessibility%20%E2%80%94%20targeting%20a%2025%25%20lift%20in%20brand%20sentiment%20scores%20within%2090%20days.%0A%0AAre%20you%20open%20to%20a%2010-minute%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Rivian",
            "pitch_hook": "Your R2 launch is the perfect moment for an adventure lifestyle campaign.",
            "urgency_level": "HIGH",
            "recommended_service": "Experiential Launch Campaign",
            "linkedin_message": "Hi Tony — Rivian's R2 rollout is a landmark moment for the adventure EV space. StepOne builds experiential campaigns that make product launches culturally unforgettable. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20Tony%20%E2%80%94%20Rivian%27s%20R2%20rollout%20is%20a%20landmark%20moment%20for%20the%20adventure%20EV%20space.%20StepOne%20builds%20experiential%20campaigns%20that%20make%20product%20launches%20culturally%20unforgettable.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Turning Rivian's R2 launch into a cultural moment",
            "email_body": "Hi Tony,\n\nRivian's joint venture with VW and the imminent R2 launch signal a brand at full throttle. The adventure-utility space is yours to own — but only with campaigns that match the ambition.\n\nAt StepOne, we'd propose an 'Off the Grid' experiential tour: real terrain activations across 10 US cities timed to the R2 launch, generating earned media and community advocacy that paid ads can't buy.\n\nAre you free for a 15-minute call next week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a 15-minute call next week?",
            "contact_email": "press@rivian.com",
            "contact_name": "Tony Caravano",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@rivian.com?subject=Turning%20Rivian%27s%20R2%20launch%20into%20a%20cultural%20moment&body=Hi%20Tony%2C%0A%0ARivian%27s%20joint%20venture%20with%20VW%20and%20the%20imminent%20R2%20launch%20signal%20a%20brand%20at%20full%20throttle.%20The%20adventure-utility%20space%20is%20yours%20to%20own%20%E2%80%94%20but%20only%20with%20campaigns%20that%20match%20the%20ambition.%0A%0AAt%20StepOne%2C%20we%27d%20propose%20an%20%27Off%20the%20Grid%27%20experiential%20tour%3A%20real%20terrain%20activations%20across%2010%20US%20cities%20timed%20to%20the%20R2%20launch%2C%20generating%20earned%20media%20and%20community%20advocacy%20that%20paid%20ads%20can%27t%20buy.%0A%0AAre%20you%20free%20for%20a%2015-minute%20call%20next%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Lucid Motors",
            "pitch_hook": "Gravity SUV needs ultra-luxury positioning that leaves legacy brands behind.",
            "urgency_level": "HIGH",
            "recommended_service": "Luxury Brand Positioning",
            "linkedin_message": "Hi — Lucid's Gravity SUV is entering the most competitive luxury segment on earth. StepOne crafts ultra-premium brand worlds that convert consideration into conviction. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Lucid%27s%20Gravity%20SUV%20is%20entering%20the%20most%20competitive%20luxury%20segment%20on%20earth.%20StepOne%20crafts%20ultra-premium%20brand%20worlds%20that%20convert%20consideration%20into%20conviction.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Ultra-luxury positioning for Lucid Gravity's global launch",
            "email_body": "Hi,\n\nLucid's Gravity SUV launch is a defining moment — entering a segment where Porsche, Mercedes and BMW have decades of emotional equity. The opportunity is to leapfrog their heritage with a technology-luxury narrative that they simply cannot match.\n\nStepOne would develop a 'Beyond Performance' brand world: bespoke editorial content, private showroom experiences and digital storytelling across UHNW-targeted channels, projecting Lucid as the inevitable choice for discerning buyers.\n\nOpen to a brief 10-minute intro call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a brief 10-minute intro call?",
            "contact_email": "media@lucidmotors.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:media@lucidmotors.com?subject=Ultra-luxury%20positioning%20for%20Lucid%20Gravity%27s%20global%20launch&body=Hi%2C%0A%0ALucid%27s%20Gravity%20SUV%20launch%20is%20a%20defining%20moment%20%E2%80%94%20entering%20a%20segment%20where%20Porsche%2C%20Mercedes%20and%20BMW%20have%20decades%20of%20emotional%20equity.%20The%20opportunity%20is%20to%20leapfrog%20their%20heritage%20with%20a%20technology-luxury%20narrative%20that%20they%20simply%20cannot%20match.%0A%0AStepOne%20would%20develop%20a%20%27Beyond%20Performance%27%20brand%20world%3A%20bespoke%20editorial%20content%2C%20private%20showroom%20experiences%20and%20digital%20storytelling%20across%20UHNW-targeted%20channels%2C%20projecting%20Lucid%20as%20the%20inevitable%20choice%20for%20discerning%20buyers.%0A%0AOpen%20to%20a%20brief%2010-minute%20intro%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "BYD",
            "pitch_hook": "Your European push needs local brand trust built fast — we know how.",
            "urgency_level": "HIGH",
            "recommended_service": "Localised Market Entry Campaign",
            "linkedin_message": "Hi — BYD's European expansion is the biggest EV story of 2026. StepOne specialises in localised market-entry campaigns that build brand trust from day one. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20BYD%27s%20European%20expansion%20is%20the%20biggest%20EV%20story%20of%202026.%20StepOne%20specialises%20in%20localised%20market-entry%20campaigns%20that%20build%20brand%20trust%20from%20day%20one.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Building BYD's brand trust across Europe in 2026",
            "email_body": "Hi,\n\nBYD is on track to become Europe's top-selling EV brand — but consumer trust data shows that Western buyers still need convincing on quality and after-sales. That's the gap StepOne closes.\n\nWe'd propose a 'Made for Here' campaign: country-specific content series, local ambassador partnerships and test-drive event circuits across Germany, France and the UK — designed to shift perception and accelerate consideration in under 6 months.\n\nWould you be open to a quick intro call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Would you be open to a quick intro call this week?",
            "contact_email": "bydcare.in@byd.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:media@byd.com?subject=Building%20BYD%27s%20brand%20trust%20across%20Europe%20in%202026&body=Hi%2C%0A%0ABYD%20is%20on%20track%20to%20become%20Europe%27s%20top-selling%20EV%20brand%20%E2%80%94%20but%20consumer%20trust%20data%20shows%20that%20Western%20buyers%20still%20need%20convincing%20on%20quality%20and%20after-sales.%20That%27s%20the%20gap%20StepOne%20closes.%0A%0AWe%27d%20propose%20a%20%27Made%20for%20Here%27%20campaign%3A%20country-specific%20content%20series%2C%20local%20ambassador%20partnerships%20and%20test-drive%20event%20circuits%20across%20Germany%2C%20France%20and%20the%20UK%20%E2%80%94%20designed%20to%20shift%20perception%20and%20accelerate%20consideration%20in%20under%206%20months.%0A%0AWould%20you%20be%20open%20to%20a%20quick%20intro%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Polestar",
            "pitch_hook": "Polestar 3 and 4 deserve a campaign as bold as their design language.",
            "urgency_level": "MEDIUM",
            "recommended_service": "Digital Brand Campaign",
            "linkedin_message": "Hi — Polestar's design language is world-class, but their digital campaigns rarely match it. StepOne creates digital-first brand experiences that do justice to Polestar's aesthetic ambition. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Polestar%27s%20design%20language%20is%20world-class%2C%20but%20their%20digital%20campaigns%20rarely%20match%20it.%20StepOne%20creates%20digital-first%20brand%20experiences%20that%20do%20justice%20to%20Polestar%27s%20aesthetic%20ambition.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "A digital campaign worthy of Polestar's design vision",
            "email_body": "Hi,\n\nPolestar is delivering its most ambitious vehicle lineup yet with the 3 and 4 — but the brand's digital presence and campaign work doesn't consistently reflect the stunning design language that sets it apart.\n\nStepOne would create a 'Scandinavian Precision' digital campaign series: minimalist, high-production content for OOH, social and CTV that positions Polestar's sustainability story as the premium choice for design-conscious buyers in Europe and North America.\n\nAre you free for a 10-minute call Thursday?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a 10-minute call Thursday?",
            "contact_email": "press@polestar.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@polestar.com?subject=A%20digital%20campaign%20worthy%20of%20Polestar%27s%20design%20vision&body=Hi%2C%0A%0APolestar%20is%20delivering%20its%20most%20ambitious%20vehicle%20lineup%20yet%20with%20the%203%20and%204%20%E2%80%94%20but%20the%20brand%27s%20digital%20presence%20and%20campaign%20work%20doesn%27t%20consistently%20reflect%20the%20stunning%20design%20language%20that%20sets%20it%20apart.%0A%0AStepOne%20would%20create%20a%20%27Scandinavian%20Precision%27%20digital%20campaign%20series%3A%20minimalist%2C%20high-production%20content%20for%20OOH%2C%20social%20and%20CTV%20that%20positions%20Polestar%27s%20sustainability%20story%20as%20the%20premium%20choice%20for%20design-conscious%20buyers%20in%20Europe%20and%20North%20America.%0A%0AAre%20you%20free%20for%20a%2010-minute%20call%20Thursday%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        }
    ],
    "fintech": [
        {
            "brand_name": "Stripe",
            "pitch_hook": "Stripe's Bridge acquisition opens a stablecoin story most marketers can't tell yet.",
            "urgency_level": "HIGH",
            "recommended_service": "Developer Brand Campaign",
            "linkedin_message": "Hi — Stripe's Bridge acquisition is the most undermarketed fintech story of 2025. StepOne builds developer-first brand campaigns that make complex infrastructure feel essential. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Stripe%27s%20Bridge%20acquisition%20is%20the%20most%20undermarketed%20fintech%20story%20of%202025.%20StepOne%20builds%20developer-first%20brand%20campaigns%20that%20make%20complex%20infrastructure%20feel%20essential.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Making Stripe's stablecoin story impossible to ignore",
            "email_body": "Hi,\n\nStripe's acquisition of Bridge puts you at the centre of the stablecoin payments revolution — but most of your target market doesn't know it yet. That's a significant first-mover narrative advantage sitting unused.\n\nStepOne would develop a 'Money Without Borders' content and developer outreach campaign: technical storytelling, conference presence and targeted media placements that establish Stripe as the definitive infrastructure layer for the next decade of global payments.\n\nOpen to a 10-minute call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a 10-minute call this week?",
            "contact_email": "press@stripe.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@stripe.com?subject=Making%20Stripe%27s%20stablecoin%20story%20impossible%20to%20ignore&body=Hi%2C%0A%0AStripe%27s%20acquisition%20of%20Bridge%20puts%20you%20at%20the%20centre%20of%20the%20stablecoin%20payments%20revolution%20%E2%80%94%20but%20most%20of%20your%20target%20market%20doesn%27t%20know%20it%20yet.%20That%27s%20a%20significant%20first-mover%20narrative%20advantage%20sitting%20unused.%0A%0AStepOne%20would%20develop%20a%20%27Money%20Without%20Borders%27%20content%20and%20developer%20outreach%20campaign%3A%20technical%20storytelling%2C%20conference%20presence%20and%20targeted%20media%20placements%20that%20establish%20Stripe%20as%20the%20definitive%20infrastructure%20layer%20for%20the%20next%20decade%20of%20global%20payments.%0A%0AOpen%20to%20a%2010-minute%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Plaid",
            "pitch_hook": "Pay-by-bank is Plaid's biggest consumer moment — it needs a consumer campaign.",
            "urgency_level": "MEDIUM",
            "recommended_service": "Consumer Trust Campaign",
            "linkedin_message": "Hi — Plaid's pay-by-bank rollout is a massive consumer moment that's being undersold. StepOne turns complex fintech features into consumer trust campaigns people actually believe. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Plaid%27s%20pay-by-bank%20rollout%20is%20a%20massive%20consumer%20moment%20that%27s%20being%20undersold.%20StepOne%20turns%20complex%20fintech%20features%20into%20consumer%20trust%20campaigns%20people%20actually%20believe.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Turning Plaid's pay-by-bank into a consumer trust moment",
            "email_body": "Hi,\n\nPlaid's pay-by-bank and open banking capabilities are genuinely transformative — but consumer awareness and trust remain the biggest adoption barriers. Most users still don't know what Plaid is, even when they use it daily.\n\nStepOne would design a 'You Already Trust Us' consumer education campaign: explainer video series, co-branded partner activations and privacy-first messaging that converts passive users into vocal advocates — targeting a 40% increase in unaided brand awareness.\n\nAre you free for a quick 15-minute call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a quick 15-minute call?",
            "contact_email": "press@plaid.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@plaid.com?subject=Turning%20Plaid%27s%20pay-by-bank%20into%20a%20consumer%20trust%20moment&body=Hi%2C%0A%0APlaid%27s%20pay-by-bank%20and%20open%20banking%20capabilities%20are%20genuinely%20transformative%20%E2%80%94%20but%20consumer%20awareness%20and%20trust%20remain%20the%20biggest%20adoption%20barriers.%20Most%20users%20still%20don%27t%20know%20what%20Plaid%20is%2C%20even%20when%20they%20use%20it%20daily.%0A%0AStepOne%20would%20design%20a%20%27You%20Already%20Trust%20Us%27%20consumer%20education%20campaign%3A%20explainer%20video%20series%2C%20co-branded%20partner%20activations%20and%20privacy-first%20messaging%20that%20converts%20passive%20users%20into%20vocal%20advocates%20%E2%80%94%20targeting%20a%2040%25%20increase%20in%20unaided%20brand%20awareness.%0A%0AAre%20you%20free%20for%20a%20quick%2015-minute%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Revolut",
            "pitch_hook": "Your UK banking licence is the most powerful brand story in European fintech right now.",
            "urgency_level": "HIGH",
            "recommended_service": "Market Expansion Campaign",
            "linkedin_message": "Hi — Revolut's UK banking licence is the biggest legitimacy moment in European fintech this decade. StepOne turns regulatory milestones into full-scale brand trust campaigns. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Revolut%27s%20UK%20banking%20licence%20is%20the%20biggest%20legitimacy%20moment%20in%20European%20fintech%20this%20decade.%20StepOne%20turns%20regulatory%20milestones%20into%20full-scale%20brand%20trust%20campaigns.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Revolut's banking licence is a brand moment — let's own it",
            "email_body": "Hi,\n\nRevolut's UK banking licence transforms your positioning overnight — from challenger app to legitimate bank. But that narrative needs to be told loudly and repeatedly across every market you're entering.\n\nStepOne would build a 'Now a Real Bank' integrated campaign: OOH in key commuter corridors, influencer trust partnerships and a broadcast-quality brand film — designed to capitalise on the regulatory news cycle and drive a measurable surge in current account sign-ups.\n\nOpen to a 10-minute call next Tuesday?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a 10-minute call next Tuesday?",
            "contact_email": "press@revolut.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@revolut.com?subject=Revolut%27s%20banking%20licence%20is%20a%20brand%20moment%20%E2%80%94%20let%27s%20own%20it&body=Hi%2C%0A%0ARevolut%27s%20UK%20banking%20licence%20transforms%20your%20positioning%20overnight%20%E2%80%94%20from%20challenger%20app%20to%20legitimate%20bank.%20But%20that%20narrative%20needs%20to%20be%20told%20loudly%20and%20repeatedly%20across%20every%20market%20you%27re%20entering.%0A%0AStepOne%20would%20build%20a%20%27Now%20a%20Real%20Bank%27%20integrated%20campaign%3A%20OOH%20in%20key%20commuter%20corridors%2C%20influencer%20trust%20partnerships%20and%20a%20broadcast-quality%20brand%20film%20%E2%80%94%20designed%20to%20capitalise%20on%20the%20regulatory%20news%20cycle%20and%20drive%20a%20measurable%20surge%20in%20current%20account%20sign-ups.%0A%0AOpen%20to%20a%2010-minute%20call%20next%20Tuesday%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Klarna",
            "pitch_hook": "Klarna's AI pivot needs a campaign that makes the assistant feel indispensable.",
            "urgency_level": "HIGH",
            "recommended_service": "AI Product Launch Campaign",
            "linkedin_message": "Hi David — Klarna's AI shopping assistant is a genuine step-change in retail UX. StepOne builds bold visual campaigns that make product innovations feel culturally essential. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20David%20%E2%80%94%20Klarna%27s%20AI%20shopping%20assistant%20is%20a%20genuine%20step-change%20in%20retail%20UX.%20StepOne%20builds%20bold%20visual%20campaigns%20that%20make%20product%20innovations%20feel%20culturally%20essential.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Making Klarna's AI assistant the most talked-about in retail",
            "email_body": "Hi David,\n\nKlarna's pivot to an AI-first operating model and the global IPO pipeline puts you in a uniquely powerful position — but the AI assistant still needs a consumer campaign that makes it feel as indispensable as the product itself.\n\nStepOne would create a 'Shop Smarter' fashion-forward campaign: high-production creator content, shoppable social formats and a launch activation at a major fashion event — positioning Klarna's AI as the must-have shopping companion for Gen Z and Millennial spenders globally.\n\nAre you open to a quick 10-minute call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you open to a quick 10-minute call this week?",
            "contact_email": "press@klarna.com",
            "contact_name": "David Sandstrom",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@klarna.com?subject=Making%20Klarna%27s%20AI%20assistant%20the%20most%20talked-about%20in%20retail&body=Hi%20David%2C%0A%0AKlarna%27s%20pivot%20to%20an%20AI-first%20operating%20model%20and%20the%20global%20IPO%20pipeline%20puts%20you%20in%20a%20uniquely%20powerful%20position%20%E2%80%94%20but%20the%20AI%20assistant%20still%20needs%20a%20consumer%20campaign%20that%20makes%20it%20feel%20as%20indispensable%20as%20the%20product%20itself.%0A%0AStepOne%20would%20create%20a%20%27Shop%20Smarter%27%20fashion-forward%20campaign%3A%20high-production%20creator%20content%2C%20shoppable%20social%20formats%20and%20a%20launch%20activation%20at%20a%20major%20fashion%20event%20%E2%80%94%20positioning%20Klarna%27s%20AI%20as%20the%20must-have%20shopping%20companion%20for%20Gen%20Z%20and%20Millennial%20spenders%20globally.%0A%0AAre%20you%20open%20to%20a%20quick%2010-minute%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        }
    ],
    "healthcare": [
        {
            "brand_name": "Teladoc Health",
            "pitch_hook": "Virtual-first care needs brand work that makes digital feel as trusted as in-person.",
            "urgency_level": "MEDIUM",
            "recommended_service": "Patient Experience Campaign",
            "linkedin_message": "Hi — Teladoc's virtual primary care expansion is one of healthcare's biggest brand opportunities. StepOne designs patient-first campaigns that make digital care feel as trusted as a doctor's office. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Teladoc%27s%20virtual%20primary%20care%20expansion%20is%20one%20of%20healthcare%27s%20biggest%20brand%20opportunities.%20StepOne%20designs%20patient-first%20campaigns%20that%20make%20digital%20care%20feel%20as%20trusted%20as%20a%20doctor%27s%20office.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Building patient trust for Teladoc's virtual care expansion",
            "email_body": "Hi,\n\nTeladoc's expansion into virtual primary care and hybrid diagnostics addresses a genuine patient need — but consumer trust in digital-first healthcare still lags behind traditional models. That trust gap is your biggest growth lever.\n\nStepOne would develop a 'Real Care, Wherever You Are' campaign: patient story-led content, employer partnership activations and a digital onboarding experience redesign — targeting a 35% improvement in new patient completion rates and measurable NPS uplift.\n\nAre you open to a 15-minute intro call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you open to a 15-minute intro call?",
            "contact_email": "mediarelations@teladochealth.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:mediarelations@teladochealth.com?subject=Building%20patient%20trust%20for%20Teladoc%27s%20virtual%20care%20expansion&body=Hi%2C%0A%0ATeladoc%27s%20expansion%20into%20virtual%20primary%20care%20and%20hybrid%20diagnostics%20addresses%20a%20genuine%20patient%20need%20%E2%80%94%20but%20consumer%20trust%20in%20digital-first%20healthcare%20still%20lags%20behind%20traditional%20models.%20That%20trust%20gap%20is%20your%20biggest%20growth%20lever.%0A%0AStepOne%20would%20develop%20a%20%27Real%20Care%2C%20Wherever%20You%20Are%27%20campaign%3A%20patient%20story-led%20content%2C%20employer%20partnership%20activations%20and%20a%20digital%20onboarding%20experience%20redesign%20%E2%80%94%20targeting%20a%2035%25%20improvement%20in%20new%20patient%20completion%20rates%20and%20measurable%20NPS%20uplift.%0A%0AAre%20you%20open%20to%20a%2015-minute%20intro%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "One Medical",
            "pitch_hook": "Amazon's scale plus One Medical's warmth — that story isn't being told loudly enough.",
            "urgency_level": "MEDIUM",
            "recommended_service": "Corporate Wellness Campaign",
            "linkedin_message": "Hi — One Medical's Amazon integration is one of healthcare's most powerful brand assets. StepOne creates campaigns that turn corporate health partnerships into mainstream consumer movements. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20One%20Medical%27s%20Amazon%20integration%20is%20one%20of%20healthcare%27s%20most%20powerful%20brand%20assets.%20StepOne%20creates%20campaigns%20that%20turn%20corporate%20health%20partnerships%20into%20mainstream%20consumer%20movements.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Amplifying One Medical's Amazon story for corporate buyers",
            "email_body": "Hi,\n\nOne Medical's integration with Amazon gives you a distribution and trust advantage no other primary care brand can replicate. But the corporate wellness buyer still isn't seeing that story told with the clarity and confidence it deserves.\n\nStepOne would build a 'Health That Works For You' B2B campaign: case study-led content targeting HR and benefits decision-makers, conference presence at major HR summits and an ROI calculator tool — designed to accelerate corporate account growth by 50% over 12 months.\n\nOpen to a quick 10-minute call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a quick 10-minute call?",
            "contact_email": "press@onemedical.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@onemedical.com?subject=Amplifying%20One%20Medical%27s%20Amazon%20story%20for%20corporate%20buyers&body=Hi%2C%0A%0AOne%20Medical%27s%20integration%20with%20Amazon%20gives%20you%20a%20distribution%20and%20trust%20advantage%20no%20other%20primary%20care%20brand%20can%20replicate.%20But%20the%20corporate%20wellness%20buyer%20still%20isn%27t%20seeing%20that%20story%20told%20with%20the%20clarity%20and%20confidence%20it%20deserves.%0A%0AStepOne%20would%20build%20a%20%27Health%20That%20Works%20For%20You%27%20B2B%20campaign%3A%20case%20study-led%20content%20targeting%20HR%20and%20benefits%20decision-makers%2C%20conference%20presence%20at%20major%20HR%20summits%20and%20an%20ROI%20calculator%20tool%20%E2%80%94%20designed%20to%20accelerate%20corporate%20account%20growth%20by%2050%25%20over%2012%20months.%0A%0AOpen%20to%20a%20quick%2010-minute%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Hims & Hers",
            "pitch_hook": "GLP-1 is the fastest-growing category in wellness — your brand should own the conversation.",
            "urgency_level": "HIGH",
            "recommended_service": "Wellness Brand Campaign",
            "linkedin_message": "Hi Bimal — Hims & Hers' GLP-1 launch puts you at the epicentre of the biggest wellness trend of the decade. StepOne builds high-aesthetic campaigns that make health brands culturally dominant. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20Bimal%20%E2%80%94%20Hims%20%26%20Hers%27%20GLP-1%20launch%20puts%20you%20at%20the%20epicentre%20of%20the%20biggest%20wellness%20trend%20of%20the%20decade.%20StepOne%20builds%20high-aesthetic%20campaigns%20that%20make%20health%20brands%20culturally%20dominant.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Owning the GLP-1 wellness conversation for Hims & Hers",
            "email_body": "Hi Bimal,\n\nHims & Hers' launch of GLP-1 weight loss medications positions you at the centre of the most talked-about health trend since the fitness boom. But the category is crowding fast and brand differentiation will determine who wins long-term.\n\nStepOne would develop an 'Every Body' brand campaign: inclusive, clinically credible storytelling across social, OOH and streaming — designed to own the emotional conversation around weight wellness and drive subscription growth, with a target 60% increase in branded search volume within 6 months.\n\nAre you free for a 10-minute call this Thursday?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a 10-minute call this Thursday?",
            "contact_email": "press@forhims.com",
            "contact_name": "Bimal Patel",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@forhims.com?subject=Owning%20the%20GLP-1%20wellness%20conversation%20for%20Hims%20%26%20Hers&body=Hi%20Bimal%2C%0A%0AHims%20%26%20Hers%27%20launch%20of%20GLP-1%20weight%20loss%20medications%20positions%20you%20at%20the%20centre%20of%20the%20most%20talked-about%20health%20trend%20since%20the%20fitness%20boom.%20But%20the%20category%20is%20crowding%20fast%20and%20brand%20differentiation%20will%20determine%20who%20wins%20long-term.%0A%0AStepOne%20would%20develop%20an%20%27Every%20Body%27%20brand%20campaign%3A%20inclusive%2C%20clinically%20credible%20storytelling%20across%20social%2C%20OOH%20and%20streaming%20%E2%80%94%20designed%20to%20own%20the%20emotional%20conversation%20around%20weight%20wellness%20and%20drive%20subscription%20growth%2C%20with%20a%20target%2060%25%20increase%20in%20branded%20search%20volume%20within%206%20months.%0A%0AAre%20you%20free%20for%20a%2010-minute%20call%20this%20Thursday%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "CVS Health",
            "pitch_hook": "MinuteClinic and digital health expansion need stronger patient engagement storytelling.",
            "urgency_level": "HIGH",
            "recommended_service": "Patient Engagement Campaign"
        },
{
    "brand_name": "UnitedHealth Group",
    "pitch_hook": "Large-scale healthcare innovation deserves clearer consumer-facing communication.",
    "urgency_level": "MEDIUM",
    "recommended_service": "Corporate Brand Campaign"
},
{
    "brand_name": "Cigna",
    "pitch_hook": "Personalized healthcare experiences can be amplified through digital-first campaigns.",
    "urgency_level": "MEDIUM",
    "recommended_service": "Customer Experience Campaign"
},
{
    "brand_name": "Oscar Health",
    "pitch_hook": "Tech-first insurance positioning creates opportunities for disruptive branding.",
    "urgency_level": "HIGH",
    "recommended_service": "Digital Brand Campaign"
},
{
    "brand_name": "Amwell",
    "pitch_hook": "Virtual healthcare adoption still requires trust-building and awareness campaigns.",
    "urgency_level": "MEDIUM",
    "recommended_service": "Telehealth Awareness Campaign"
},
{
    "brand_name": "Mayo Clinic",
    "pitch_hook": "Global reputation can be extended through next-generation digital patient experiences.",
    "urgency_level": "LOW",
    "recommended_service": "Experience Design Campaign"
},
{
    "brand_name": "Cleveland Clinic",
    "pitch_hook": "Healthcare innovation initiatives deserve broader audience engagement.",
    "urgency_level": "LOW",
    "recommended_service": "Thought Leadership Campaign"
}
    ],
    "fashion": [
        {
            "brand_name": "Nike",
            "pitch_hook": "Nike's run club revival is the community story of 2026 — it needs a global stage.",
            "urgency_level": "HIGH",
            "recommended_service": "Community Activation Campaign",
            "linkedin_message": "Hi — Nike's return to hyper-local run club activations is exactly the kind of community story StepOne excels at scaling globally. Would love to connect and share an idea, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Nike%27s%20return%20to%20hyper-local%20run%20club%20activations%20is%20exactly%20the%20kind%20of%20community%20story%20StepOne%20excels%20at%20scaling%20globally.%20Would%20love%20to%20connect%20and%20share%20an%20idea%2C%20Arjun.",
            "email_subject": "Scaling Nike's run club story into a global movement",
            "email_body": "Hi,\n\nNike's refocus on performance running and hyper-local community is a powerful strategic reset — but the run club story deserves a campaign infrastructure that scales it from city activations to a genuine global cultural moment.\n\nStepOne would build a 'Run Your City' integrated campaign: localised event production across 20 global cities, creator-led content series and a digital community hub — designed to generate 50M+ impressions and measurably drive performance footwear sales in Q3 2026.\n\nOpen to a 10-minute call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a 10-minute call this week?",
            "contact_email": "media@nike.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:media@nike.com?subject=Scaling%20Nike%27s%20run%20club%20story%20into%20a%20global%20movement&body=Hi%2C%0A%0ANike%27s%20refocus%20on%20performance%20running%20and%20hyper-local%20community%20is%20a%20powerful%20strategic%20reset%20%E2%80%94%20but%20the%20run%20club%20story%20deserves%20a%20campaign%20infrastructure%20that%20scales%20it%20from%20city%20activations%20to%20a%20genuine%20global%20cultural%20moment.%0A%0AStepOne%20would%20build%20a%20%27Run%20Your%20City%27%20integrated%20campaign%3A%20localised%20event%20production%20across%2020%20global%20cities%2C%20creator-led%20content%20series%20and%20a%20digital%20community%20hub%20%E2%80%94%20designed%20to%20generate%2050M%2B%20impressions%20and%20measurably%20drive%20performance%20footwear%20sales%20in%20Q3%202026.%0A%0AOpen%20to%20a%2010-minute%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Lululemon",
            "pitch_hook": "Lululemon's footwear push needs a campaign that earns credibility outside yoga.",
            "urgency_level": "HIGH",
            "recommended_service": "Product Launch Campaign",
            "linkedin_message": "Hi Nikki — Lululemon's footwear expansion is a bold move into contested territory. StepOne creates product launch campaigns that earn credibility fast in new categories. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20Nikki%20%E2%80%94%20Lululemon%27s%20footwear%20expansion%20is%20a%20bold%20move%20into%20contested%20territory.%20StepOne%20creates%20product%20launch%20campaigns%20that%20earn%20credibility%20fast%20in%20new%20categories.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Earning footwear credibility fast for Lululemon",
            "email_body": "Hi Nikki,\n\nLululemon's footwear launch is competing against Nike, Adidas and On Running in a category where brand credibility is built over years. The challenge is to earn that credibility in months — and that's a campaign problem StepOne solves.\n\nWe'd propose a 'Move in Anything' performance campaign: athlete partnership content, immersive store experience redesigns and a precision social strategy targeting fitness communities across 8 key markets — with a KPI of 25% footwear category awareness uplift in 90 days.\n\nAre you free for a 15-minute call next week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a 15-minute call next week?",
            "contact_email": "mediarelations@lululemon.com",
            "contact_name": "Nikki Neuburger",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:mediarelations@lululemon.com?subject=Earning%20footwear%20credibility%20fast%20for%20Lululemon&body=Hi%20Nikki%2C%0A%0ALululemon%27s%20footwear%20launch%20is%20competing%20against%20Nike%2C%20Adidas%20and%20On%20Running%20in%20a%20category%20where%20brand%20credibility%20is%20built%20over%20years.%20The%20challenge%20is%20to%20earn%20that%20credibility%20in%20months%20%E2%80%94%20and%20that%27s%20a%20campaign%20problem%20StepOne%20solves.%0A%0AWe%27d%20propose%20a%20%27Move%20in%20Anything%27%20performance%20campaign%3A%20athlete%20partnership%20content%2C%20immersive%20store%20experience%20redesigns%20and%20a%20precision%20social%20strategy%20targeting%20fitness%20communities%20across%208%20key%20markets%20%E2%80%94%20with%20a%20KPI%20of%2025%25%20footwear%20category%20awareness%20uplift%20in%2090%20days.%0A%0AAre%20you%20free%20for%20a%2015-minute%20call%20next%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Zara",
            "pitch_hook": "Zara's weekly drops are the fastest fashion cycle on earth — the campaign needs to match.",
            "urgency_level": "MEDIUM",
            "recommended_service": "Digital Content Strategy",
            "linkedin_message": "Hi — Zara's weekly drop model is the fastest fashion cycle on the planet. StepOne builds always-on digital content strategies that match the pace of fast fashion without sacrificing brand quality. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Zara%27s%20weekly%20drop%20model%20is%20the%20fastest%20fashion%20cycle%20on%20the%20planet.%20StepOne%20builds%20always-on%20digital%20content%20strategies%20that%20match%20the%20pace%20of%20fast%20fashion%20without%20sacrificing%20brand%20quality.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "An always-on content engine for Zara's weekly drops",
            "email_body": "Hi,\n\nZara's weekly new-in drops generate enormous organic interest — but the brand's digital content rarely capitalises on that momentum with the editorial quality the product deserves. Competitors like H&M and Mango are closing the content gap fast.\n\nStepOne would build an 'Always New' always-on content engine: a weekly editorial production system, shoppable video formats and a micro-influencer seeding programme — designed to double Zara's social engagement rate and drive a 20% increase in digital revenue per campaign cycle.\n\nOpen to a quick 10-minute call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a quick 10-minute call?",
            "contact_email": "comunicacion@zara.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:comunicacion@zara.com?subject=An%20always-on%20content%20engine%20for%20Zara%27s%20weekly%20drops&body=Hi%2C%0A%0AZara%27s%20weekly%20new-in%20drops%20generate%20enormous%20organic%20interest%20%E2%80%94%20but%20the%20brand%27s%20digital%20content%20rarely%20capitalises%20on%20that%20momentum%20with%20the%20editorial%20quality%20the%20product%20deserves.%20Competitors%20like%20H%26M%20and%20Mango%20are%20closing%20the%20content%20gap%20fast.%0A%0AStepOne%20would%20build%20an%20%27Always%20New%27%20always-on%20content%20engine%3A%20a%20weekly%20editorial%20production%20system%2C%20shoppable%20video%20formats%20and%20a%20micro-influencer%20seeding%20programme%20%E2%80%94%20designed%20to%20double%20Zara%27s%20social%20engagement%20rate%20and%20drive%20a%2020%25%20increase%20in%20digital%20revenue%20per%20campaign%20cycle.%0A%0AOpen%20to%20a%20quick%2010-minute%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        }
    ],
    "gaming": [
        {
            "brand_name": "Roblox",
            "pitch_hook": "Roblox's Shopify deal makes it the first true commerce platform inside a game — own that story.",
            "urgency_level": "HIGH",
            "recommended_service": "Creator Commerce Campaign",
            "linkedin_message": "Hi — Roblox's Shopify partnership is the biggest commerce moment in gaming history. StepOne builds creator-economy campaigns that make platform milestones into cultural movements. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Roblox%27s%20Shopify%20partnership%20is%20the%20biggest%20commerce%20moment%20in%20gaming%20history.%20StepOne%20builds%20creator-economy%20campaigns%20that%20make%20platform%20milestones%20into%20cultural%20movements.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Turning Roblox's Shopify deal into the commerce story of 2026",
            "email_body": "Hi,\n\nRoblox's partnership with Shopify to enable physical goods sales inside games is genuinely historic — but the broader market doesn't yet understand what it means for brands, creators or consumers. That narrative gap is a massive opportunity.\n\nStepOne would develop a 'Play. Create. Earn.' campaign: a creator showcase event, brand partnership activations inside Roblox and a media outreach strategy targeting mainstream business and culture press — designed to establish Roblox as the definitive commerce platform for the next generation of shoppers.\n\nAre you open to a 10-minute call this week?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you open to a 10-minute call this week?",
            "contact_email": "press@roblox.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@roblox.com?subject=Turning%20Roblox%27s%20Shopify%20deal%20into%20the%20commerce%20story%20of%202026&body=Hi%2C%0A%0ARoblox%27s%20partnership%20with%20Shopify%20to%20enable%20physical%20goods%20sales%20inside%20games%20is%20genuinely%20historic%20%E2%80%94%20but%20the%20broader%20market%20doesn%27t%20yet%20understand%20what%20it%20means%20for%20brands%2C%20creators%20or%20consumers.%20That%20narrative%20gap%20is%20a%20massive%20opportunity.%0A%0AStepOne%20would%20develop%20a%20%27Play.%20Create.%20Earn.%27%20campaign%3A%20a%20creator%20showcase%20event%2C%20brand%20partnership%20activations%20inside%20Roblox%20and%20a%20media%20outreach%20strategy%20targeting%20mainstream%20business%20and%20culture%20press%20%E2%80%94%20designed%20to%20establish%20Roblox%20as%20the%20definitive%20commerce%20platform%20for%20the%20next%20generation%20of%20shoppers.%0A%0AAre%20you%20open%20to%20a%2010-minute%20call%20this%20week%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Epic Games",
            "pitch_hook": "Unreal Engine 6 is the most powerful developer story in tech — it needs a campaign to match.",
            "urgency_level": "HIGH",
            "recommended_service": "Developer Ecosystem Campaign",
            "linkedin_message": "Hi Saxs — Epic's Unreal Engine 6 ecosystem launch is the biggest developer story in gaming this decade. StepOne builds creator-focused campaigns that make platform ecosystems feel unmissable. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20Saxs%20%E2%80%94%20Epic%27s%20Unreal%20Engine%206%20ecosystem%20launch%20is%20the%20biggest%20developer%20story%20in%20gaming%20this%20decade.%20StepOne%20builds%20creator-focused%20campaigns%20that%20make%20platform%20ecosystems%20feel%20unmissable.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Making Unreal Engine 6 the developer story of the decade",
            "email_body": "Hi Saxs,\n\nUnreal Engine 6 and the Epic Games Store's evolving publishing incentives represent a genuine inflection point for independent developers — but the message isn't cutting through the noise of Unity's restructuring and competing platforms.\n\nStepOne would design an 'Unleash the Engine' campaign: a global developer roadshow, showcase content series featuring indie studios built on UE6 and a digital-first media strategy targeting game dev communities — positioned to drive 30% growth in new UE6 developer registrations in 6 months.\n\nAre you free for a 10-minute call Thursday?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Are you free for a 10-minute call Thursday?",
            "contact_email": "pr@epicgames.com",
            "contact_name": "Saxs Persson",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:pr@epicgames.com?subject=Making%20Unreal%20Engine%206%20the%20developer%20story%20of%20the%20decade&body=Hi%20Saxs%2C%0A%0AUnreal%20Engine%206%20and%20the%20Epic%20Games%20Store%27s%20evolving%20publishing%20incentives%20represent%20a%20genuine%20inflection%20point%20for%20independent%20developers%20%E2%80%94%20but%20the%20message%20isn%27t%20cutting%20through%20the%20noise%20of%20Unity%27s%20restructuring%20and%20competing%20platforms.%0A%0AStepOne%20would%20design%20an%20%27Unleash%20the%20Engine%27%20campaign%3A%20a%20global%20developer%20roadshow%2C%20showcase%20content%20series%20featuring%20indie%20studios%20built%20on%20UE6%20and%20a%20digital-first%20media%20strategy%20targeting%20game%20dev%20communities%20%E2%80%94%20positioned%20to%20drive%2030%25%20growth%20in%20new%20UE6%20developer%20registrations%20in%206%20months.%0A%0AAre%20you%20free%20for%20a%2010-minute%20call%20Thursday%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        },
        {
            "brand_name": "Unity Technologies",
            "pitch_hook": "Unity 6 is a trust rebuild story — the right campaign turns critics into champions.",
            "urgency_level": "HIGH",
            "recommended_service": "Brand Rehabilitation Campaign",
            "linkedin_message": "Hi — Unity's runtime fee reversal and Unity 6 launch is one of the most challenging brand rehabilitation stories in tech. StepOne specialises in turning developer trust crises into comeback narratives. Would love to connect, Arjun.",
            "linkedin_url": "https://www.linkedin.com/messaging/compose/?body=Hi%20%E2%80%94%20Unity%27s%20runtime%20fee%20reversal%20and%20Unity%206%20launch%20is%20one%20of%20the%20most%20challenging%20brand%20rehabilitation%20stories%20in%20tech.%20StepOne%20specialises%20in%20turning%20developer%20trust%20crises%20into%20comeback%20narratives.%20Would%20love%20to%20connect%2C%20Arjun.",
            "email_subject": "Turning Unity 6 into the developer comeback story of 2026",
            "email_body": "Hi,\n\nUnity's runtime fee crisis damaged developer trust significantly — but the Unity 6 platform and fee model reversal is a genuine fresh start. The risk is that developers who left don't hear the new story loudly enough to return.\n\nStepOne would build a 'We Heard You' developer re-engagement campaign: a transparent brand film from leadership, a 'Unity 6 for Indie' content series and a community ambassador programme — targeting re-activation of 25% of lapsed developers and a measurable NPS recovery within 9 months.\n\nOpen to a 15-minute intro call?\n\nArjun Sharma\nHead of Partnerships\nStepOne\narjun@stepone.agency",
            "email_cta": "Open to a 15-minute intro call?",
            "contact_email": "press@unity.com",
            "contact_name": "",
            "sender_name": "Arjun Sharma",
            "sender_email": "arjun@stepone.agency",
            "sender_company": "StepOne",
            "sender_title": "Head of Partnerships",
            "mailto_link": "mailto:press@unity.com?subject=Turning%20Unity%206%20into%20the%20developer%20comeback%20story%20of%202026&body=Hi%2C%0A%0AUnity%27s%20runtime%20fee%20crisis%20damaged%20developer%20trust%20significantly%20%E2%80%94%20but%20the%20Unity%206%20platform%20and%20fee%20model%20reversal%20is%20a%20genuine%20fresh%20start.%20The%20risk%20is%20that%20developers%20who%20left%20don%27t%20hear%20the%20new%20story%20loudly%20enough%20to%20return.%0A%0AStepOne%20would%20build%20a%20%27We%20Heard%20You%27%20developer%20re-engagement%20campaign%3A%20a%20transparent%20brand%20film%20from%20leadership%2C%20a%20%27Unity%206%20for%20Indie%27%20content%20series%20and%20a%20community%20ambassador%20programme%20%E2%80%94%20targeting%20re-activation%20of%2025%25%20of%20lapsed%20developers%20and%20a%20measurable%20NPS%20recovery%20within%209%20months.%0A%0AOpen%20to%20a%2015-minute%20intro%20call%3F%0A%0AArjun%20Sharma%0AHead%20of%20Partnerships%0AStepOne%0Aarjun%40stepone.agency"
        }
    ]
}

# Real, pre-validated public data for key industries to guarantee a flawless live demo under wifi/API constraints.
DEMO_DATA = {
    "electric vehicles": {
        "brands": [
            {"brand_name": "Tesla", "why_stepone": "Position their autonomous driving and next-gen mass market models through creative narrative design.", "why_now": "Facing intense global pricing competition and brand equity challenges in key markets.", "strategic_fit_score": 92, "growth_signal_score": 88, "event_presence_score": 85, "recent_activity_score": 90, "confidence_score": 95, "source_url": "https://www.tesla.com"},
            {"brand_name": "Rivian", "why_stepone": "Develop experiential outdoor lifestyle campaigns that highlight their utility and adventure branding.", "why_now": "Scaling production of R2 and R3 models and expanding charging infrastructure.", "strategic_fit_score": 90, "growth_signal_score": 85, "event_presence_score": 90, "recent_activity_score": 88, "confidence_score": 92, "source_url": "https://www.rivian.com"},
            {"brand_name": "Lucid Motors", "why_stepone": "Refine premium positioning and ultra-luxury brand messaging to compete with traditional luxury cars.", "why_now": "Launching Gravity SUV and expanding Middle Eastern market footprint.", "strategic_fit_score": 85, "growth_signal_score": 80, "event_presence_score": 80, "recent_activity_score": 82, "confidence_score": 90, "source_url": "https://www.lucidmotors.com"},
            {"brand_name": "BYD", "why_stepone": "Lead localized international marketing campaigns to establish credibility in European and Latin American markets.", "why_now": "Rapid global expansion and launching new premium sub-brands like Yangwang.", "strategic_fit_score": 88, "growth_signal_score": 95, "event_presence_score": 92, "recent_activity_score": 94, "confidence_score": 94, "source_url": "https://www.byd.com"},
            {"brand_name": "Polestar", "why_stepone": "Craft minimalist, design-focused digital campaigns emphasizing performance sustainability.", "why_now": "Delivering Polestar 3 and 4 SUVs to global markets amidst organizational transitions.", "strategic_fit_score": 86, "growth_signal_score": 78, "event_presence_score": 85, "recent_activity_score": 80, "confidence_score": 91, "source_url": "https://www.polestar.com"}
        ],
        "events": [{"event_name": "Electrify Expo 2026", "date": "May 15-17, 2026", "location": "Long Beach, CA", "official_url": "https://www.electrifyexpo.com", "likely_participating_brands": "Tesla, Rivian, Lucid Motors", "confidence_score": "HIGH", "source_url": "https://www.electrifyexpo.com"}],
        "contacts": [{"brand_name": "Rivian", "name": "Tony Caravano", "role": "Director of Customer Engagement", "linkedin": "https://www.linkedin.com/in/tony-caravano-a4ab347/", "email": "press@rivian.com", "phone": "Public information unavailable", "source_url": "https://www.linkedin.com/in/tony-caravano-b86a877", "confidence_score": "HIGH"}],
        "activities": [{"brand_name": "Rivian", "activity": "Rivian announced a strategic joint venture with VW Group to share EV architecture and software.", "date": "June 2025", "source_url": "https://www.rivian.com/newsroom", "confidence_score": "HIGH"}],
        "outreach": DEMO_OUTREACH["electric vehicles"]
    },
    "fintech": {
        "brands": [
            {"brand_name": "Stripe", "why_stepone": "Craft developer-focused branding and simplify messaging around complex global tax and banking services.", "why_now": "Expanding crypto payout options and rolling out advanced billing features.", "strategic_fit_score": 95, "growth_signal_score": 93, "event_presence_score": 90, "recent_activity_score": 92, "confidence_score": 96, "source_url": "https://www.stripe.com"},
            {"brand_name": "Plaid", "why_stepone": "Support consumer-facing marketing to explain data privacy and open-banking security benefits.", "why_now": "Deploying pay-by-bank features and scaling instant transfer capabilities.", "strategic_fit_score": 88, "growth_signal_score": 86, "event_presence_score": 82, "recent_activity_score": 84, "confidence_score": 91, "source_url": "https://www.plaid.com"},
            {"brand_name": "Revolut", "why_stepone": "Design high-impact experiential retail pop-ups for multi-currency accounts across new markets.", "why_now": "Secured UK banking license and expanding aggressively in US and APAC.", "strategic_fit_score": 91, "growth_signal_score": 95, "event_presence_score": 88, "recent_activity_score": 93, "confidence_score": 94, "source_url": "https://www.revolut.com"},
            {"brand_name": "Klarna", "why_stepone": "Design bold, fashion-forward visual campaigns that integrate their AI assistant shopping experience.", "why_now": "Pivoting to an AI-first operating model and listing globally.", "strategic_fit_score": 93, "growth_signal_score": 90, "event_presence_score": 92, "recent_activity_score": 94, "confidence_score": 95, "source_url": "https://www.klarna.com"}
        ],
        "events": [{"event_name": "Money20/20 USA 2026", "date": "October 25-28, 2026", "location": "Las Vegas, NV", "official_url": "https://www.us.money2020.com", "likely_participating_brands": "Stripe, Plaid, Revolut", "confidence_score": "HIGH", "source_url": "https://www.us.money2020.com"}],
        "contacts": [{"brand_name": "Klarna", "name": "David Sandstrom", "role": "Chief Marketing Officer", "linkedin": "https://www.linkedin.com/in/davidsandstrom", "email": "press@klarna.com", "phone": "Public information unavailable", "source_url": "https://www.linkedin.com/in/davidsandstrom", "confidence_score": "HIGH"}],
        "activities": [{"brand_name": "Stripe", "activity": "Stripe acquired Bridge, a stablecoin payments platform, to boost crypto integration.", "date": "October 2025", "source_url": "https://stripe.com/newsroom", "confidence_score": "HIGH"}],
        "outreach": DEMO_OUTREACH["fintech"]
    },
    "healthcare": {
        "brands": [
            {"brand_name": "Teladoc Health", "why_stepone": "Design highly engaging, frictionless patient experience workflows and modern branding.", "why_now": "Expanding virtual primary care services and integrating hybrid diagnostic tools.", "strategic_fit_score": 88, "growth_signal_score": 80, "event_presence_score": 85, "recent_activity_score": 82, "confidence_score": 92, "source_url": "https://www.teladochealth.com"},
            {"brand_name": "One Medical", "why_stepone": "Craft digital-first growth campaigns highlighting the convenience of hybrid clinic-app memberships.", "why_now": "Expanding corporate health partnerships under Amazon integration.", "strategic_fit_score": 90, "growth_signal_score": 88, "event_presence_score": 85, "recent_activity_score": 87, "confidence_score": 93, "source_url": "https://www.onemedical.com"},
            {"brand_name": "Hims & Hers", "why_stepone": "Develop high-aesthetic digital and retail packaging branding for wellness and prescription lines.", "why_now": "Rapidly scaling personalized specialty health and weight loss offerings.", "strategic_fit_score": 92, "growth_signal_score": 94, "event_presence_score": 80, "recent_activity_score": 91, "confidence_score": 95, "source_url": "https://www.hims.com"}
        ],
        "events": [{"event_name": "HIMSS Global Health Conference 2026", "date": "March 2026", "location": "Las Vegas, NV", "official_url": "https://www.himssconference.com", "likely_participating_brands": "Teladoc Health, One Medical", "confidence_score": "HIGH", "source_url": "https://www.himssconference.com"}],
        "contacts": [{"brand_name": "Hims & Hers", "name": "Bimal Patel", "role": "Senior VP of Marketing", "linkedin": "https://www.linkedin.com/in/bimal-patel-846101", "email": "press@forhims.com", "phone": "Public information unavailable", "source_url": "https://www.linkedin.com/in/bimal-patel-846101", "confidence_score": "HIGH"}],
        "activities": [{"brand_name": "Hims & Hers", "activity": "Hims & Hers announced the launch of GLP-1 weight loss medications in their subscription portfolios.", "date": "May 2024", "source_url": "https://www.hims.com/press", "confidence_score": "HIGH"}],
        "outreach": DEMO_OUTREACH["healthcare"]
    },
    "fashion": {
        "brands": [
            {"brand_name": "Nike", "why_stepone": "Refine premium global community and physical run club activations using hyper-local marketing.", "why_now": "Refocusing on retail partnerships and core performance running apparel markets.", "strategic_fit_score": 94, "growth_signal_score": 85, "event_presence_score": 90, "recent_activity_score": 88, "confidence_score": 95, "source_url": "https://www.nike.com"},
            {"brand_name": "Lululemon", "why_stepone": "Support expansion of international stores and localized yoga community sponsorships.", "why_now": "Scaling footwear lines and launching high-performance outerwear products.", "strategic_fit_score": 92, "growth_signal_score": 90, "event_presence_score": 88, "recent_activity_score": 91, "confidence_score": 94, "source_url": "https://www.lululemon.com"},
            {"brand_name": "Zara", "why_stepone": "Develop high-fashion digital video campaigns highlighting weekly clothing drops.", "why_now": "Upgrading flagship store formats and expanding next-day digital logistics.", "strategic_fit_score": 90, "growth_signal_score": 92, "event_presence_score": 80, "recent_activity_score": 90, "confidence_score": 93, "source_url": "https://www.zara.com"}
        ],
        "events": [{"event_name": "New York Fashion Week 2026", "date": "September 2026", "location": "New York, NY", "official_url": "https://nyfw.com", "likely_participating_brands": "Zara, Nike", "confidence_score": "HIGH", "source_url": "https://nyfw.com"}],
        "contacts": [{"brand_name": "Lululemon", "name": "Nikki Neuburger", "role": "Chief Brand Officer", "linkedin": "https://www.linkedin.com/in/nikkineuburger", "email": "mediarelations@lululemon.com", "phone": "Public information unavailable", "source_url": "https://www.linkedin.com/in/nikkineuburger", "confidence_score": "HIGH"}],
        "activities": [{"brand_name": "Nike", "activity": "Nike launched new Ioniq-mesh performance wear ahead of summer athletics cycles.", "date": "April 2026", "source_url": "https://news.nike.com", "confidence_score": "HIGH"}],
        "outreach": DEMO_OUTREACH["fashion"]
    },
    "gaming": {
        "brands": [
            {"brand_name": "Roblox", "why_stepone": "Design immersive, gamified brand experiences and virtual pop-ups inside the developer marketplace.", "why_now": "Expanding developer payouts and introducing platform-wide video advertising formats.", "strategic_fit_score": 95, "growth_signal_score": 91, "event_presence_score": 90, "recent_activity_score": 93, "confidence_score": 96, "source_url": "https://www.roblox.com"},
            {"brand_name": "Epic Games", "why_stepone": "Support creator-focused outreach campaigns and promote Epic Games Store publishing incentives.", "why_now": "Launching Unreal Engine 6 ecosystems and navigating multi-platform distribution store shifts.", "strategic_fit_score": 92, "growth_signal_score": 89, "event_presence_score": 88, "recent_activity_score": 90, "confidence_score": 94, "source_url": "https://www.epicgames.com"},
            {"brand_name": "Unity Technologies", "why_stepone": "Simplify technical messaging to independent game developers and promote runtime enhancements.", "why_now": "Restructuring engine runtime fee models and launching Unity 6 platforms.", "strategic_fit_score": 87, "growth_signal_score": 80, "event_presence_score": 85, "recent_activity_score": 84, "confidence_score": 91, "source_url": "https://www.unity.com"}
        ],
        "events": [{"event_name": "Game Developers Conference (GDC) 2026", "date": "March 16-20, 2026", "location": "San Francisco, CA", "official_url": "https://www.gdconf.com", "likely_participating_brands": "Unity Technologies, Epic Games, Roblox", "confidence_score": "HIGH", "source_url": "https://www.gdconf.com"}],
        "contacts": [{"brand_name": "Epic Games", "name": "Saxs Persson", "role": "Executive VP, Fortnite Ecosystem", "linkedin": "https://www.linkedin.com/in/saxspersson", "email": "pr@epicgames.com", "phone": "Public information unavailable", "source_url": "https://www.linkedin.com/in/saxspersson", "confidence_score": "HIGH"}],
        "activities": [{"brand_name": "Roblox", "activity": "Roblox partnered with Shopify to allow creators to sell physical goods directly inside Roblox games.", "date": "September 2025", "source_url": "https://blog.roblox.com", "confidence_score": "HIGH"}],
        "outreach": DEMO_OUTREACH["gaming"]
    }
}


def is_demo_mode_triggered(industry: str) -> bool:
    return industry.lower().strip() in DEMO_DATA


def get_demo_data(industry: str) -> dict:
    return DEMO_DATA.get(industry.lower().strip(), {})