import random

# A rotating pool of natural, conversational copy templates for social syndication
TEMPLATES = [
    # Helpful / Problem-Solving
    "If you're a {industry} constantly chasing down missed jobs or dealing with {pain}, you need a CRM that actually tracks things in real time. This one's been a game-changer for a lot of folks I know → {url}",
    "{industry} professionals: nothing worse than finishing killer work and then spending weeks dealing with {pain}. Found a CRM that automates reminders + tracks everything without feeling salesy. Worth a look if you're tired of that cycle → {url}",
    "{industry} — client no-shows or canceled bookings killing your schedule? There's actually decent CRM options built specifically for appointment flow + {pain} automation now. Broke down the best ones here: {url}",

    # Relatable / Pain-Point First
    "Real talk: trying to run a {industry} business without proper job tracking is a nightmare. Quotes forgotten, clients mad. Finally found CRMs that handle {pain} properly → {url}",
    "{industry} pros — ever lose a client because you forgot to follow up? Yeah… been there. These CRMs actually help keep that {pain} chaos under control → {url}",
    "{industry}: seasonal rush + emergency calls + paperwork hell = burnout. Switched to a CRM that handles {pain} way better. Saved my sanity → {url}",

    # Question / Engagement Style
    "Quick question for {industry} friends: what's your biggest system headache right now — scheduling, invoicing, or {pain}? I just compared the top CRMs that actually fix those → {url}",
    "Anyone else in {industry} tired of leads going cold because follow-up is manual? There are CRMs built exactly for {pain} workflows now. Curious what you guys use → {url}",
    "{industry} owners — how do you handle {pain} without losing your mind? Found a few CRMs that automate the annoying parts really well → {url}",

    # Short & Punchy / Meme-ish
    "{industry} when the CRM doesn't track leads: 😭\n{industry} when they find one that does: 🤑\nReal options here to fix {pain} → {url}",
    "{industry} life be like: finish job → send invoice → wait 47 days → cry\nThere's actually software that stops {pain} → {url}",
    "{industry}: 'Another no-show? Cool, more free time I guess'\nNah, fix {pain} with a proper CRM → {url}"
]

def generate_natural_post(industry, pain_point, url):
    """Selects a random template and injects the specific industry variables."""
    # Ensure variables flow smoothly in sentence format (lowercase except first word if applicable)
    industry_fmt = industry.strip().lower()
    pain_fmt = pain_point.strip().lower()
    
    template = random.choice(TEMPLATES)
    # Capitalize the first letter if the template starts with the industry or pain point
    return template.format(
        industry=industry_fmt,
        pain=pain_fmt,
        url=url
    ).capitalize() # Capitalizes the opening letter just in case
