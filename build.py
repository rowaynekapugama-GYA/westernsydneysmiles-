#!/usr/bin/env python3
"""Builds the Western Sydney Smiles Google Ads landing pages into ./site"""
import os, html

OUT = os.path.dirname(os.path.abspath(__file__))
PHONE = "(02) 9623 7333"
TEL = "tel:0296237333"
ADDRESS = "7/370 Great Western Hwy, St Marys NSW 2760"
MAPS = "https://www.google.com/maps/place/Western+Sydney+Smiles+-+Dentist+St+Marys/@-33.7701599,150.7706231,17z/data=!3m1!4b1!4m5!3m4!1s0x6b129aac30421427:0x8fbea03fccc22ecb!8m2!3d-33.7701644!4d150.7728118"
MAP_EMBED = "https://www.google.com/maps?q=Western+Sydney+Smiles+7/370+Great+Western+Hwy+St+Marys+NSW+2760&output=embed"
GTM_ID = "GTM-XXXXXXX"   # replace with the Western Sydney Smiles container before go-live
FORM_ENDPOINT = ""       # SmileOx / webhook endpoint for the call-back form — leave blank to run in demo mode (redirects to thank-you page)
BOOKING_URL = "https://booking.au.hsone.app/soe/new/Western%20Sydney%20Smiles?pid=AUPNO01"   # Henry Schein One online scheduler
BOOKING_MODE = "embed"   # "embed" = scheduler iframed on the page under the banner; "popup" = big CTA that opens it in a new window

# ---------- icons ----------
I = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
 "tick": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 7"/></svg>',
 "tickc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14M3 11l2-6h14l2 6M5 11h14v6H5z"/><circle cx="7.5" cy="17" r="1.5"/><circle cx="16.5" cy="17" r="1.5"/></svg>',
 "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
 "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
 "dollar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
 "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "tooth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3c-2.5 0-4 2-4 5 0 4 2 6 2.5 9.5S7 22 8 22s1.5-5 4-5 3 5 4 5 2-1 2.5-4.5S21 12 21 8c0-3-1.5-5-4-5-2 0-3 1-5 1S9 3 7 3z"/></svg>',
 "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h8l-1 8 10-12h-8z"/></svg>',
 "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>',
 "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
 "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "scan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2M7 12h10"/></svg>',
}

TEAM = [
 ("ramesh","Dr Ramesh Harichandran","Principal Dentist"),
 ("nisha","Dr Nisha Jacob","Dentist"),
 ("rumesh","Dr Rumesh Wanaguru","Dentist"),
 ("michael","Dr Michael Chen","Dentist"),
 ("sue","Dr Sue Jean Lee","Dentist"),
 ("katrina","Dr Katrina Nhan","Dentist"),
 ("bernie","Bernie McAlary","Denture Technician"),
]

NIB_PARTNERS = [
 ("nib.png","nib","sm"),("nib-first-choice.svg","nib First Choice","tall"),("gu-health.svg","GU Health",""),
 ("real.svg","Real Insurance",""),("australian-seniors.svg","Australian Seniors","tall"),("qantas.svg","Qantas Insurance",""),
 ("apia.svg","Apia","tall"),("aami.svg","AAMI","tall"),("suncorp.png","Suncorp",""),
 ("iman.png","IMAN Australian Health Plans","tall"),("ing.png","ING Health Insurance",""),
]

# ---------- shared blocks ----------
def head(title, desc, page_class=""):
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="https://westernsydneysmiles.com.au/wp-content/uploads/2022/02/favicon-1.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
</head>
<body class="{page_class}">
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
'''

def topbar(msg):
    return f'''<div class="topbar"><div class="wrap">
  <span><i class="dot"></i>{msg}</span>
  <span class="hide-m">{I["pin"]} {ADDRESS} &nbsp;·&nbsp; Parking via Sainsbury Rd</span>
</div></div>'''

def header(cta_text="Book Online", cta_href="#book"):
    return f'''<header class="site"><div class="wrap">
  <a class="logo" href="#top" aria-label="Western Sydney Smiles"><img src="img/logo.png" alt="Western Sydney Smiles" width="300" height="89"></a>
  <nav>
    <a class="phone js-call" href="{TEL}">{I["phone"]}<span><small>Call us now</small>{PHONE}</span></a>
    <a class="btn btn-yellow js-book" href="{cta_href}">{I["cal"]} {cta_text}</a>
  </nav>
</div></header>'''

def collage():
    names = dict((a,b) for a,b,c in TEAM)
    cols = [["ramesh","sue"],["nisha","rumesh"],["michael","katrina"]]
    col_html = "".join('<div class="col">' + "".join(f'<img src="img/team-{k}.jpg" alt="{names[k]}" loading="eager">' for k in c) + '</div>' for c in cols)
    return f'<div class="collage">{col_html}</div>'

def hero(eyebrow, h1, lead, primary, secondary, trust, offer_float, show_rating=True):
    rating = f'''<div class="rating-float"><div class="g">G</div><div><b>4.9 ★★★★★</b><small>260+ Google reviews</small></div></div>''' if show_rating else ""
    return f'''<section class="hero" id="top"><div class="wrap">
  <div class="hero-copy">
    <div class="eyebrow"><i class="dot"></i>{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="ctas">{primary}{secondary}</div>
    <div class="trust">{trust}</div>
  </div>
  <div class="hero-visual">
    {rating}
    {collage()}
    {offer_float}
  </div>
</div></section>'''

def trust_items(items):
    return "".join(f'<span>{I[ic]} {t}</span>' for ic,t in items)

def booking(h2, lead, steps, incl_title, incl_items, incl_price, form_title, form_sub, service_opts, default_service, urgency=False, submit="Request a Call Back"):
    chips = "".join(f'<span class="chip">{I["tick"]} {x}</span>' for x in incl_items)
    opts = "".join(f'<option{" selected" if o==default_service else ""}>{o}</option>' for o in service_opts)
    urgency_field = """
      <div class="full"><label class="f">How urgent is it?</label>
        <div class="seg">
          <input type="radio" name="urgency" id="u1" value="I'm in pain now" checked><label for="u1">I'm in pain now</label>
          <input type="radio" name="urgency" id="u2" value="Within a few days"><label for="u2">Within a few days</label>
        </div></div>""" if urgency else ""
    if BOOKING_MODE == "embed":
        scheduler = f"""
    <div class="sched" id="scheduler">
      <div class="sched-head"><span class="tag">Live online booking</span><b>Pick your own day and time</b><span class="s">Real-time availability straight from our appointment book. Takes under a minute.</span></div>
      <div class="sched-frame"><iframe src="{BOOKING_URL}" title="Book online with Western Sydney Smiles" loading="eager" allow="payment" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
      <div class="sched-foot"><span>Booking window not loading?</span><a class="btn btn-navy js-sched-open" href="{BOOKING_URL}" target="_blank" rel="noopener">{I["cal"]} Open booking in a new window</a></div>
    </div>"""
    else:
        scheduler = f"""
    <div class="sched" id="scheduler">
      <div class="sched-cta">
        <span class="tag">Live online booking</span>
        <h3>Pick your own day and time</h3>
        <p>Our online booking shows real-time availability straight from our appointment book. Choose a time that suits you and you are done in under a minute.</p>
        <a class="btn btn-yellow btn-lg js-sched-open" href="{BOOKING_URL}" target="_blank" rel="noopener">{I["cal"]} Book Online Now</a>
      </div>
    </div>"""
    return f"""<section class="book" id="book"><div class="wrap">
  <div class="book-head">
    <span class="kicker">Book online in under a minute</span>
    <h2>{h2}</h2>
    <p class="lead">{lead}</p>
    <div class="pill-row incl-chips">{chips}</div>
  </div>
  {scheduler}
  <div class="book-under">
    <details class="callback" id="callback">
      <summary>{I["phone"]} Can't see a time that suits, or prefer we call you? <span>Request a call back</span></summary>
      <form class="form-card cb" id="bookingForm" method="post" action="{FORM_ENDPOINT or '#'}" novalidate>
        <h3>{form_title}</h3>
        <p class="sub">{form_sub}</p>
        <input type="hidden" name="source" value="Google Ads"><input type="hidden" name="page" value="{form_title}">
        <input type="text" name="website" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="form-grid">
          <div class="full"><label class="f">Are you a new or existing patient?</label>
            <div class="seg">
              <input type="radio" name="patient_type" id="pt-new" value="New patient" checked><label for="pt-new">New patient</label>
              <input type="radio" name="patient_type" id="pt-ex" value="Existing patient"><label for="pt-ex">Existing patient</label>
            </div></div>
          <div><label class="f" for="fname">First name</label><input class="inp" id="fname" name="first_name" required autocomplete="given-name" placeholder="Jane"></div>
          <div><label class="f" for="lname">Last name</label><input class="inp" id="lname" name="last_name" required autocomplete="family-name" placeholder="Smith"></div>
          <div><label class="f" for="mobile">Mobile</label><input class="inp" id="mobile" name="mobile" type="tel" inputmode="tel" required autocomplete="tel" placeholder="04xx xxx xxx"></div>
          <div><label class="f" for="email">Email</label><input class="inp" id="email" name="email" type="email" required autocomplete="email" placeholder="you@email.com"></div>
          <div class="full"><label class="f" for="service">What can we help with?</label><select class="inp" id="service" name="service">{opts}</select></div>
          {urgency_field}
          <div><label class="f" for="day">Preferred day</label><select class="inp" id="day" name="preferred_day"><option>Any day</option><option>Monday</option><option>Tuesday</option><option>Wednesday</option><option>Thursday</option><option>Friday</option><option>Saturday</option></select></div>
          <div><label class="f" for="time">Preferred time</label><select class="inp" id="time" name="preferred_time"><option>Any time</option><option>Morning</option><option>Midday</option><option>Afternoon</option><option>After 5pm</option></select></div>
          <div class="full"><label class="f" for="notes">Anything we should know? <span style="font-weight:500;color:var(--muted)">(optional)</span></label><textarea class="inp" id="notes" name="notes" placeholder="e.g. health fund, concerns, questions"></textarea></div>
        </div>
        <div class="form-msg" id="formMsg"></div>
        <button class="btn btn-navy btn-lg btn-block" type="submit" id="submitBtn">{I["phone"]} {submit}</button>
        <p class="fine">{I["lock"]}Your details are kept private and only used to arrange your appointment. Our team will call or text you back during opening hours.</p>
      </form>
    </details>
    <div class="or-call">Prefer to talk? <a class="js-call" href="{TEL}">{PHONE}</a><span class="dep">A $50 deposit secures your appointment and comes off your treatment on the day.</span></div>
  </div>
</div></section>"""

def offers_block(cards, kicker="Current offers", h2="Our current offers", lead=""):
    def card(c):
        cls = "offer-card hot" if c.get("hot") else "offer-card"
        badge = f'<span class="badge">{c["badge"]}</span>' if c.get("badge") else ""
        lis = "".join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in c.get("items",[]))
        price = c.get("price","")
        d = f'<p class="d">{c["d"]}</p>' if c.get("d") else ""
        return f'<div class="{cls}">{badge}<h3>{c["h"]}</h3>{price}{d}<ul>{lis}</ul><a class="btn {"btn-yellow" if c.get("hot") else "btn-navy"} js-book" href="#book">{c.get("cta","Book this offer")} {I["arrow"]}</a></div>'
    return f'''<section class="offers" id="offers"><div class="wrap">
  <div class="sec-h center"><span class="kicker">{kicker}</span><h2>{h2}</h2>{f'<p>{lead}</p>' if lead else ''}</div>
  <div class="grid-3">{"".join(card(c) for c in cards)}</div>
  <p class="fine" style="text-align:center;margin-top:22px">*Prices are a guide and may vary depending on your individual needs. We will always confirm your fee before any treatment begins.</p>
</div></section>'''

def nib_block():
    logos = "".join(f'<div><img src="img/{f}" alt="{a}" class="{c}"></div>' for f,a,c in NIB_PARTNERS)
    return f'''<section class="nib" id="nib"><div class="wrap">
  <div>
    <div class="nib-logo"><img src="img/nib-first-choice.svg" alt="nib First Choice"><span style="font-weight:800;color:var(--navy)">Official First Choice Dental Provider</span></div>
    <h2>nib members: <span style="color:var(--cyan-dark)">no gap</span> on your dental check-up</h2>
    <p>Western Sydney Smiles is now an nib First Choice dental provider. If you are an eligible nib member (or with one of nib's partner funds below), your preventative check-up and bitewing x-rays can be covered in full under First Choice, with nothing to pay on the day. Up to two check-ups and two bitewing x-rays each year.</p>
    <div class="nogap"><div class="ic">{I["shield"]}</div><div><b>No gap dental check-up for eligible nib members</b><span>Bring your membership card and we will claim it on the spot. Payments are subject to nib's Fund Rules, policy, waiting periods, annual limits and service limits.</span></div></div>
  </div>
  <div class="partners">
    <h3>First Choice applies to members of nib and these nib partner funds</h3>
    <div class="logos">{logos}</div>
    <p class="fine">Not sure if you are eligible? Call us on <a href="{TEL}" class="js-call" style="font-weight:800;color:var(--navy)">{PHONE}</a> and we will check for you.</p>
  </div>
</div></section>'''

def funds_block(h2="All major health funds accepted. <span>Claim on the spot</span> with HICAPS.", p="Bring your health fund card and we will process your claim before you leave, so you only pay the gap. Not insured? Ask us about our interest-free payment plans so you can start treatment now and pay over time."):
    return f'''<section class="funds" id="funds"><div class="wrap">
  <div>
    <span class="kicker">Health funds &amp; payment options</span>
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="pay-pills">
      <span>{I["tick"]} HICAPS on-the-spot claims</span>
      <span>{I["tick"]} nib First Choice provider</span>
      <span>{I["tick"]} Interest-free payment plans</span>
      <span>{I["tick"]} Afterpay &amp; Zip</span>
      <span>{I["tick"]} CDBS bulk-billed kids' dental</span>
    </div>
  </div>
  <div class="fund-logos">
    <div><img src="img/nib.png" alt="nib"></div>
    <div><img src="img/medibank.png" alt="Medibank"></div>
    <div><img src="img/hcf.png" alt="HCF"></div>
    <div><img src="img/hicaps.png" alt="HICAPS"></div>
    <div><img src="img/zipmoney.png" alt="Zip Money" class="sm"></div>
    <div><span style="font-weight:800;color:var(--navy);font-size:15px">Afterpay</span></div>
    <div><span style="font-weight:800;color:var(--navy);font-size:14px;text-align:center;line-height:1.2">Bupa, AHM,<br>Australian Unity</span></div>
    <div><span style="font-weight:800;color:var(--navy);font-size:14px;text-align:center;line-height:1.2">+ all other<br>major funds</span></div>
  </div>
</div></section>'''

def team_block(h2="Meet the team looking after your smile", lead="Six experienced dentists and an in-house denture technician under one roof in St Marys. That means more appointment times, continuity of care, and most treatments completed right here without a referral elsewhere."):
    cards = "".join(f'<div class="tm"><img src="img/team-{k}.jpg" alt="{n}" loading="lazy"><div class="c"><b>{n}</b><span>{r}</span>{"<span class=ah>AHPRA registered</span>" if r!="Denture Technician" else "<span class=ah>In-house dentures</span>"}</div></div>' for k,n,r in TEAM)
    return f'''<section class="team" id="team"><div class="wrap">
  <div class="sec-h center"><span class="kicker">Our team</span><h2>{h2}</h2><p>{lead}</p></div>
  <div class="team-grid">{cards}<div class="tm" style="background:var(--navy);color:#fff;display:flex;flex-direction:column;justify-content:center;padding:26px;border-color:var(--navy)"><b style="font-size:20px;line-height:1.2;margin-bottom:10px">Plus Michelle, Mya, Nadia, Tracey &amp; Nimra</b><span style="color:rgba(255,255,255,.75);font-size:14px">Our practice manager, reception and dental assistant team who will greet you, help with health fund claims and keep everything running smoothly.</span><a class="btn btn-cyan js-book" href="#book" style="margin-top:18px;align-self:flex-start;padding:12px 18px;font-size:14px">Book with our team</a></div></div>
  <div class="team-note"><span>{I["users"]} 6 dentists, more appointment times</span><span>{I["tooth"]} Dentures made in-house</span><span>{I["heart"]} Gentle with nervous patients</span><span>{I["scan"]} Digital x-rays &amp; OPG on site</span></div>
</div></section>'''

def why_block(h2="The new approach to dental care in St Marys", feats=None):
    feats = feats or [
      ("heart","","Passionate","We love what we do, and it shows in everything from the smallest procedure to complex treatment."),
      ("eye","y","Transparent","Our fees are published on our website and we are always upfront about costs before any treatment starts."),
      ("dollar","","Affordable","Fair pricing without compromising on the standard of care, plus payment plans and interest-free options."),
      ("clock","y","Convenient","Open six days with late appointments, Saturday mornings and same-day emergency appointments."),
    ]
    cards = "".join(f'<div class="feat"><div class="ic {y}">{I[ic]}</div><h3>{h}</h3><p>{p}</p></div>' for ic,y,h,p in feats)
    return f'''<section id="why" style="background:var(--bg)"><div class="wrap">
  <div class="sec-h center"><span class="kicker">Why Western Sydney Smiles</span><h2>{h2}</h2></div>
  <div class="grid-4">{cards}</div>
</div></section>'''

def rating_band():
    return f'''<div class="rating-band"><div class="wrap">
  <span class="g"><i class="b">G</i><i class="r">o</i><i class="y">o</i><i class="b">g</i><i class="gr">l</i><i class="r">e</i> Reviews</span>
  <span class="score"><span class="stars">★★★★★</span> 4.9 <small>from 260+ reviews</small></span>
  <span class="sep"></span>
  <span class="chip">{I["shield"]} nib First Choice provider</span>
  <span class="chip">{I["clock"]} Open 6 days incl. Saturdays</span>
  <span class="chip">{I["pin"]} Next to Astley Medical Centre, St Marys</span>
</div></div>'''

def faq_block(items, h2="Frequently asked questions"):
    lis = "".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(items))
    return f'''<section class="faq" id="faq"><div class="wrap">
  <div class="sec-h center"><span class="kicker">Good to know</span><h2>{h2}</h2></div>
  <div class="list">{lis}</div>
</div></section>'''

def location_block():
    return f'''<section class="loc" id="location"><div class="wrap">
  <div class="info">
    <div class="sec-h" style="margin-bottom:8px"><span class="kicker">Find us</span><h2 style="font-size:30px">Easy to get to, easy to park</h2></div>
    <div class="row"><div class="ic">{I["pin"]}</div><div><b>{ADDRESS}</b><span>Next to Astley Medical Centre on the Great Western Highway. <a href="{MAPS}" target="_blank" rel="noopener" style="color:var(--cyan-dark);font-weight:700">Get directions</a></span></div></div>
    <div class="row"><div class="ic">{I["car"]}</div><div><b>Free parking</b><span>Enter via Sainsbury Road. A short walk from St Marys station and bus stops.</span></div></div>
    <div class="row"><div class="ic">{I["clock"]}</div><div><b>Opening hours</b><div class="hours"><div><b>Mon to Thu</b><span>9:00am to 6:00pm</span></div><div><b>Friday</b><span>9:00am to 5:00pm</span></div><div><b>Saturday</b><span>8:00am to 1:00pm</span></div><div><b>Sunday</b><span>Closed</span></div></div></div></div>
    <div class="row"><div class="ic">{I["phone"]}</div><div><b><a class="js-call" href="{TEL}">{PHONE}</a></b><span>Serving St Marys, St Clair, Werrington, Ropes Crossing, Mount Druitt, Hebersham, Oxley Park &amp; surrounds.</span></div></div>
  </div>
  <div class="map"><iframe src="{MAP_EMBED}" loading="lazy" title="Map to Western Sydney Smiles" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''

def final_cta(h2, p, primary_text="Book Online Now"):
    return f'''<section class="final"><div class="wrap">
  <h2>{h2}</h2><p>{p}</p>
  <div class="ctas"><a class="btn btn-yellow btn-lg js-book" href="#book">{I["cal"]} {primary_text}</a><a class="btn btn-ghost btn-lg js-call" href="{TEL}">{I["phone"]} {PHONE}</a></div>
</div></section>'''

FOOT_NAV = '<nav class="fnav"><a href="index.html">New Patient Offer</a><a href="dental-implants.html">Dental Implants</a><a href="emergency-dentist.html">Emergency Dentist</a><a href="https://westernsydneysmiles.com.au" target="_blank" rel="noopener">Main website</a></nav>'

def footer(tc):
    return f'''<footer><div class="wrap">
  <img src="img/logo-white.png" alt="Western Sydney Smiles">
  {FOOT_NAV}
  <p>Western Sydney Smiles · {ADDRESS} · <a class="js-call" href="{TEL}">{PHONE}</a> · <a href="mailto:reception@westernsydneysmiles.com.au">reception@westernsydneysmiles.com.au</a><br><a href="https://westernsydneysmiles.com.au/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a> · <a href="https://westernsydneysmiles.com.au/terms-and-conditions/" target="_blank" rel="noopener">Terms &amp; Conditions</a></p>
  <div class="tc">{tc} Any surgical or invasive procedure carries risks. Before proceeding, you should seek a second opinion from an appropriately qualified health practitioner. © 2026 Western Sydney Smiles.</div>
</div></footer>
<div class="mcta"><a class="btn btn-outline js-call" href="{TEL}">{I["phone"]} Call now</a><a class="btn btn-yellow js-book" href="#book">{I["cal"]} Book online</a></div>
<script src="main.js"></script>
</body></html>'''

MAIN_JS = r'''
(function(){
  // reveal on scroll
  var els=document.querySelectorAll('.offer-card,.feat,.tm,.proc > div,.urgent-list > div,.row');
  els.forEach(function(e){e.classList.add('reveal')});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e)});
  }else{els.forEach(function(e){e.classList.add('in')})}

  // smooth anchor + focus first field when jumping to form
  document.querySelectorAll('a[href="#book"]').forEach(function(a){
    a.addEventListener('click',function(ev){
      var t=document.getElementById('book'); if(!t) return;
      ev.preventDefault(); t.scrollIntoView({behavior:'smooth',block:'start'});
      setTimeout(function(){var f=document.getElementById('fname'); if(f && window.innerWidth>960) f.focus({preventScroll:true})},600);
      window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'book_click'});
    });
  });
  document.querySelectorAll('.js-call').forEach(function(a){a.addEventListener('click',function(){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'call_click'})})});
  document.querySelectorAll('.js-sched-open').forEach(function(a){a.addEventListener('click',function(){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'scheduler_open'})})});

  // scheduler engagement: fires once when the visitor clicks into the embedded booking frame
  var fr=document.querySelector('.sched-frame iframe');
  if(fr){var fired=false; window.addEventListener('blur',function(){ if(!fired && document.activeElement===fr){fired=true; window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'scheduler_engaged'});} });}
  // open the call-back form if linked to directly
  if(location.hash==='#callback'){var cb=document.getElementById('callback'); if(cb) cb.open=true;}

  // booking form
  var form=document.getElementById('bookingForm'); if(!form) return;
  var msg=document.getElementById('formMsg'), btn=document.getElementById('submitBtn');
  function bad(el){el.style.borderColor='#E24B4B'; el.addEventListener('input',function(){el.style.borderColor=''},{once:true})}
  form.addEventListener('submit',function(ev){
    ev.preventDefault(); msg.className='form-msg'; msg.textContent='';
    if(form.website.value){return}  // honeypot
    var ok=true;
    ['first_name','last_name','mobile','email'].forEach(function(n){var el=form[n]; if(!el.value.trim()){bad(el);ok=false}});
    var m=form.mobile.value.replace(/\s+/g,''); if(m && !/^(\+?61|0)[2-9]\d{8}$/.test(m)){bad(form.mobile);ok=false}
    if(form.email.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.value)){bad(form.email);ok=false}
    if(!ok){msg.className='form-msg err';msg.textContent='Please check the highlighted fields and try again.';return}
    btn.disabled=true; btn.innerHTML='Sending your request…';
    var data={}; new FormData(form).forEach(function(v,k){data[k]=v}); data.page_url=location.href; data.submitted_at=new Date().toISOString();
    var endpoint=form.getAttribute('action');
    var done=function(){
      window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'booking_request',service:data.service,patient_type:data.patient_type});
      try{sessionStorage.setItem('wss_lead',JSON.stringify({first_name:data.first_name,service:data.service,preferred_day:data.preferred_day,preferred_time:data.preferred_time}))}catch(e){}
      location.href='thank-you.html';
    };
    if(!endpoint || endpoint==='#'){setTimeout(done,700);return}
    fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;done()}).catch(function(){
      btn.disabled=false; btn.innerHTML='Try again';
      msg.className='form-msg err'; msg.innerHTML='Something went wrong sending your request. Please call us on <a href="tel:0296237333" style="color:inherit;text-decoration:underline">(02) 9623 7333</a>.';
    });
  });
})();
'''

TC_NP = "*New Patient Offer: $199 for a comprehensive examination, scale and clean, fluoride treatment and all necessary x-rays (total value $425) for new patients only. Additional treatment, if required, is quoted separately. Not to be used with any other offer. nib First Choice no gap check-up applies to eligible members only and is subject to nib's Fund Rules, policy, waiting periods, annual and service limits."
TC_IMP = "**Dental implant from $4,490 includes a single implant fixture and crown. Some patients require additional procedures such as bone or tissue grafting, extractions or sinus lifts which are quoted separately after assessment. Payment plans are subject to credit approval."
TC_EM = "Same-day emergency appointments are subject to availability. Emergency fees depend on the treatment required and will be confirmed with you before treatment begins. Health fund rebates vary by fund and level of cover."

def finance_block():
    return f"""<section class="finance" id="finance"><div class="wrap">
  <div class="fin-grid">
    <div>
      <span class="kicker">Ways to pay</span>
      <h2>Implants within reach: <span>payment plans</span> and early release of super</h2>
      <p>You should not have to put off replacing missing teeth. Most of our implant patients spread the cost, and many use their superannuation to cover treatment. We will walk you through every option at your consultation.</p>
      <a class="btn btn-yellow js-book" href="#book" style="margin-top:22px">{I["cal"]} Book an implant consultation</a>
    </div>
    <div class="fin-cards">
      <div class="fin-card"><div class="ic">{I["dollar"]}</div><b>Interest-free payment plans</b><span>Approved on the spot in the practice. Spread your implant over manageable repayments with no interest.</span></div>
      <div class="fin-card hl"><div class="ic">{I["shield"]}</div><b>Early release of super</b><span>Dental implants can qualify for early access to superannuation on compassionate grounds through the ATO. We provide the treatment plan and quote you need to apply.</span></div>
      <div class="fin-card"><div class="ic">{I["tickc"]}</div><b>Afterpay &amp; Zip</b><span>Buy now, pay later options for smaller stages of treatment.</span></div>
      <div class="fin-card"><div class="ic">{I["heart"]}</div><b>Health fund rebates</b><span>We claim any eligible rebate on the spot with HICAPS, so you only pay the gap.</span></div>
    </div>
  </div>
  <p class="fine" style="text-align:center;margin-top:22px">Payment plans subject to credit approval. Early release of super is assessed by the ATO on compassionate grounds and is not guaranteed; we recommend seeking independent financial advice.</p>
</div></section>"""

def before_after_block():
    cards = "".join(f'<figure class="ba"><img src="img/ba-{i}.jpg" alt="Dental implant before and after, patient {i}" loading="lazy"><span class="l b">Before</span><span class="l a">After</span></figure>' for i in range(1,7))
    return f"""<section class="results" id="results"><div class="wrap">
  <div class="sec-h center"><span class="kicker">Real results</span><h2>Before and after dental implants</h2><p>From single missing teeth to full smile rebuilds. These are real patients who chose to replace missing or failing teeth with implants.</p></div>
  <div class="ba-grid">{cards}</div>
  <p class="fine" style="text-align:center;margin-top:18px">Photos shown with patient consent. Individual results vary. Any surgical or invasive procedure carries risks; a consultation is required to confirm suitability.</p>
  <div style="text-align:center;margin-top:24px"><a class="btn btn-navy btn-lg js-book" href="#book">{I["cal"]} Start my smile transformation</a></div>
</div></section>"""

# ================= PAGE 1: NEW PATIENTS =================
def page_new_patients():
    h = head("New Patient Offer $199 | Dentist St Marys | Western Sydney Smiles", "New patients: comprehensive check-up, clean, x-rays and fluoride for $199 (valued at $425). nib First Choice provider, all health funds, open Saturdays. Book online in 30 seconds.", "np")
    hero_html = hero(
        "New patient offer · St Marys",
        'Your complete check-up &amp; clean for <em>$199</em><span class="cy">*</span>',
        "Exam, scale and clean, fluoride and all necessary x-rays, valued at $425. Six gentle dentists, open six days, and we claim your health fund on the spot. nib members may pay nothing at all.",
        f'<a class="btn btn-yellow btn-lg js-book" href="#book">{I["cal"]} Book Online Now</a>',
        f'<a class="btn btn-ghost btn-lg js-call" href="{TEL}">{I["phone"]} {PHONE}</a>',
        trust_items([("shield","nib First Choice provider"),("tickc","All health funds, HICAPS on the spot"),("clock","Open Saturdays"),("users","6 dentists, 1 location")]),
        '<div class="offer-float"><span class="k">New patient offer</span><div class="v">$199 <small class="strike">$425</small></div><span class="d">Check-up, clean, fluoride + x-rays included</span></div>')
    book = booking(
        "Book your $199 new patient visit",
        "Choose a day and time that suits you from our live appointment book. No phone tag, no waiting for a reply.",
        [("Pick your time","See real availability and choose a slot, including Saturdays."),("Enter your details","Takes under a minute. Reception will call to take a $50 deposit that comes off your visit."),("Come in and smile","Bring your health fund card and we claim on the spot.")],
        "Everything included for $199*",
        ["Comprehensive examination with your dentist","Professional scale and clean","All necessary x-rays, including OPG (worth $160)","Fluoride treatment","Complimentary cosmetic consultation","Personal treatment plan with upfront pricing"],
        '<div class="price"><b>$199</b><s>$425 value</s><span>new patients only</span></div>',
        "New Patient Booking", "Request your appointment and we will lock in a time.",
        ["New patient check-up & clean ($199 offer)","nib no gap check-up","Check-up & clean (existing patient)","Children's dentistry / CDBS","Teeth whitening","Fillings or a sore tooth","Something else"],
        "New patient check-up & clean ($199 offer)")
    offers = offers_block([
        {"hot":True,"badge":"Most popular","h":"New Patient Check-up &amp; Clean","price":'<div class="price"><b>$199</b><s>$425</s></div>',"items":["Comprehensive exam and scale &amp; clean","All necessary x-rays including OPG","Fluoride treatment","Complimentary cosmetic consult"],"cta":"Claim the $199 offer"},
        {"badge":"nib members","h":"No Gap Dental Check-up","price":'<div class="price"><b>$0</b><small>out of pocket*</small></div>',"d":"Eligible nib and nib partner fund members pay no gap on preventative check-ups and bitewing x-rays under nib First Choice.","items":["Up to 2 check-ups per year","Up to 2 bitewing x-rays per year","Claimed on the spot with HICAPS"],"cta":"Book my no gap check-up"},
        {"badge":"Brighter smile","h":"In-Chair Teeth Whitening","price":'<div class="price"><b>From $499</b><s>$1,000</s></div>',"d":"Professional in-chair whitening with your dentist for a noticeably brighter smile in a single visit.","items":["Done safely by a dentist","Results in one appointment","Ask about adding a take-home kit"],"cta":"Book whitening"},
    ], "New patient offers", "Offers worth smiling about", "Transparent pricing with no surprises. Every offer includes a proper examination so you know exactly where your smile stands.")
    faq = faq_block([
        ("What does the $199 new patient offer include?","A comprehensive examination with one of our dentists, a professional scale and clean, fluoride treatment, and all necessary x-rays including an OPG. It is valued at $425 and available to new patients of Western Sydney Smiles."),
        ("I'm with nib. Do I still pay $199?","If you are an eligible nib member (or with an nib partner fund such as GU Health, Qantas, Apia, AAMI, Suncorp, Australian Seniors, Real, IMAN or ING), your preventative check-up and bitewing x-rays can be covered in full under First Choice, meaning no gap to pay on the day. Call us and we will check your eligibility before you come in."),
        ("Can I claim on my health fund?","Yes. We accept all major Australian health funds and claim on the spot through HICAPS, so you only pay any gap. Bring your health fund card to your appointment."),
        ("Is a deposit required to book?","A $50 deposit secures your appointment. Our team will take it over the phone when they confirm your booking. It comes off your treatment on the day or is fully refundable with more than 24 hours' notice."),
        ("Do you see children?","Absolutely. We are a family practice and bulk bill eligible children under the Child Dental Benefits Schedule (CDBS), which covers up to $1,132 of basic dental over two years."),
        ("I'm nervous about the dentist. Will you take it slow?","Many of our patients felt the same way before their first visit. Our dentists are gentle and will explain everything before they start. Let us know in the booking notes and we will make sure you are looked after."),
    ])
    body = (topbar("New patients: check-up, clean &amp; x-rays for $199*, valued at $425") + header() + hero_html + nib_block() + book + rating_band() + offers + funds_block() + team_block() + why_block() + faq + location_block()
            + final_cta('Ready for a healthier smile? <em>Book your $199 visit today.</em>', "Online in 30 seconds or call our friendly team. Saturday appointments available.") + footer(TC_NP))
    return h + body

# ================= PAGE 2: DENTAL IMPLANTS =================
def page_implants():
    h = head("Dental Implants from $4,490 | St Marys, Western Sydney | Western Sydney Smiles", "Replace missing teeth with dental implants from $4,490 including the crown. Experienced dentists, OPG on site, payment plans and health fund claims. Book your implant consultation in St Marys.", "imp")
    hero_html = hero(
        "Dental implants · Western Sydney",
        'Replace missing teeth with implants from <em>$4,490</em><span class="cy">**</span> including the crown',
        "A permanent, natural-looking tooth that lets you eat, speak and smile with confidence. Assessed, placed and restored by our experienced team in St Marys, with payment plans so you can start sooner.",
        f'<a class="btn btn-yellow btn-lg js-book" href="#book">{I["cal"]} Book an Implant Consultation</a>',
        f'<a class="btn btn-ghost btn-lg js-call" href="{TEL}">{I["phone"]} {PHONE}</a>',
        trust_items([("tickc","Implant + crown from $4,490"),("dollar","Payment plans &amp; early release of super"),("scan","OPG x-ray on site"),("users","6 experienced dentists")]),
        '<div class="offer-float"><span class="k">Single implant</span><div class="v">$4,490<small>**</small></div><span class="d">Implant fixture + crown. Payment plans available.</span></div>')
    book = booking(
        "Book your implant consultation",
        "Choose a consultation time from our live appointment book and find out whether implants are right for you, what is involved and exactly what it will cost.",
        [("Pick your time","Choose a consultation slot that suits you, including Saturdays."),("Consultation &amp; OPG x-ray","We assess your bone, gums and bite on site."),("Your plan and quote","A clear step-by-step plan with upfront pricing and payment options.")],
        "What is included in your implant",
        ["Titanium implant fixture placed by your dentist","Custom-made porcelain crown, colour matched","OPG imaging on site to plan placement","Healing checks and follow-up appointments","Upfront written quote before anything starts"],
        '<div class="price"><b>From $4,490</b><span>per implant incl. crown**</span></div>',
        "Implant Consultation", "Tell us about your missing tooth or teeth and we will book you in.",
        ["Single dental implant","Multiple implants","Implant-supported dentures / full arch","Not sure, I would like advice","Replace an old bridge or denture"],
        "Single dental implant")
    process = f'''<section class="process" id="process"><div class="wrap">
  <div class="sec-h center"><span class="kicker">How it works</span><h2>Your implant journey, step by step</h2><p>Most single implants are completed over three to six months. We walk you through every stage so there are no surprises.</p></div>
  <div class="proc">
    <div><h3>Consultation &amp; planning</h3><p>Examination and OPG x-ray to check your bone and gums, then a written plan and quote.</p></div>
    <div><h3>Implant placement</h3><p>A titanium fixture is gently placed into the jaw under local anaesthetic. Most patients are back to normal the next day.</p></div>
    <div><h3>Healing</h3><p>Over a few months the bone fuses to the implant, creating a strong foundation. We check in along the way.</p></div>
    <div><h3>Your new tooth</h3><p>A custom porcelain crown is fitted to the implant. Brush and floss it just like a natural tooth.</p></div>
  </div>
</div></section>'''
    pricing = f'''<section id="pricing" style="background:#fff"><div class="wrap">
  <div class="grid-2" style="align-items:center;gap:40px">
    <div>
      <span class="kicker">Transparent pricing</span>
      <h2 style="font-size:clamp(28px,3.4vw,40px)">Know the cost before you commit</h2>
      <p style="color:var(--muted);font-size:17px;margin:14px 0 22px">We publish our fees so you can plan with confidence. After your consultation you will receive an itemised quote covering everything your case needs. No hidden extras.</p>
      <div class="pill-row"><span class="chip">{I["tick"]} Interest-free plans, approved on the spot</span><span class="chip">{I["tick"]} Afterpay &amp; Zip</span><span class="chip">{I["tick"]} Health fund rebates claimed for you</span><span class="chip">{I["tick"]} Early release of super may apply</span></div>
      <a class="btn btn-navy js-book" href="#book" style="margin-top:26px">{I["cal"]} Get my implant quote</a>
    </div>
    <div class="pricetab"><table>
      <tr><th>Treatment</th><th>Our fee</th></tr>
      <tr class="hl"><td>Dental implant including crown**</td><td>From $4,490</td></tr>
      <tr><td>Implant consultation with OPG x-ray</td><td>Ask us</td></tr>
      <tr><td>Tooth extraction (if required)</td><td>Quoted at consult</td></tr>
      <tr><td>Bone or tissue graft (if required)</td><td>Quoted at consult</td></tr>
      <tr><td>Dental crown (non-implant)</td><td>From $1,550</td></tr>
      <tr><td>Dentures (made in-house)</td><td>Ask us</td></tr>
    </table><div class="note">**Some patients require additional procedures such as grafting or extractions before an implant can be placed. These are identified at your consultation and quoted separately.</div></div>
  </div>
</div></section>'''
    why = why_block("Why have your implant done at Western Sydney Smiles", [
        ("users","","Experienced team","Six dentists plus an in-house denture technician, so single implants through to implant-retained dentures are handled under one roof."),
        ("scan","y","Planned with imaging","OPG x-rays taken on site so your implant is planned around your bone and nerves, not guesswork."),
        ("dollar","","Honest pricing","Published fees, itemised quotes and payment plans. You decide with the full picture in front of you."),
        ("heart","y","Gentle, local care","Treatment and every follow-up appointment close to home in St Marys, with Saturday appointments available."),
    ])
    faq = faq_block([
        ("How much does a dental implant cost?","A single dental implant including the crown starts from $4,490 at Western Sydney Smiles. If you need an extraction, bone graft or other preparatory work, this is quoted separately after your consultation so you have one clear, itemised figure before you decide."),
        ("Does getting an implant hurt?","The implant is placed under local anaesthetic, so you should not feel pain during the procedure. Some tenderness and swelling for a few days afterwards is normal and is usually managed with simple pain relief."),
        ("How long do implants last?","With good oral hygiene and regular check-ups, dental implants can last many years and often decades. The crown on top may need replacing over time due to normal wear, just like a natural tooth."),
        ("Am I suitable for implants?","Most healthy adults with adequate jaw bone are suitable. Smoking, uncontrolled diabetes, gum disease and bone loss can affect success, which is why we assess you properly first. If bone is lacking, grafting can often make implants possible."),
        ("Can I use my health fund or a payment plan?","Yes. Health fund rebates for implants vary by fund and level of cover, and we can claim on the spot for you. We also offer interest-free payment plans with on-the-spot approval, plus Afterpay and Zip."),
        ("What about replacing all my teeth?","If you are missing many or all of your teeth, implant-retained dentures or a full-arch solution may be the best option. Our dentists and in-house denture technician work together on these cases. Book a consultation to discuss what suits you."),
    ], "Dental implant questions, answered")
    body = (topbar("Dental implants from $4,490** incl. crown · Payment plans available") + header("Book Consultation") + hero_html + finance_block() + book + rating_band() + before_after_block() + process + pricing + why + funds_block("Health fund rebates claimed for you. <span>Flexible payment plans</span> for the rest.", "We accept all major health funds and claim on the spot with HICAPS. For the balance, choose an interest-free payment plan approved on the spot, Afterpay or Zip, so you can start treatment now rather than later.") + team_block("The team behind your new smile", "Six experienced dentists and an in-house denture technician in St Marys, which means your implant is planned, placed and restored by one team who know your case.") + faq + location_block()
            + final_cta('Stop hiding your smile. <em>Book your implant consultation today.</em>', "Find out if implants are right for you and get a clear, itemised quote. Payment plans available.", "Book an Implant Consultation") + footer(TC_IMP))
    return h + body

# ================= PAGE 3: EMERGENCY =================
def page_emergency():
    h = head("Emergency Dentist St Marys | Same-Day Appointments | Western Sydney Smiles", "Toothache, broken tooth or swelling? Same-day emergency dental appointments in St Marys, open six days including Saturdays. Call (02) 9623 7333 or book online now.", "em")
    hero_html = hero(
        "Emergency dentist · St Marys",
        'In pain? We will see you <em>today</em><span class="cy">.</span>',
        "Same-day emergency appointments for toothache, broken teeth, swelling and knocked-out teeth. Six dentists on the roster means we can nearly always fit you in, including Saturdays. Call now or send a request and we will ring you straight back.",
        f'<a class="btn btn-yellow btn-lg js-call" href="{TEL}">{I["phone"]} Call {PHONE}</a>',
        f'<a class="btn btn-ghost btn-lg js-book" href="#book">{I["cal"]} Request a Call Back</a>',
        trust_items([("bolt","Same-day appointments"),("clock","Open 6 days, late appointments"),("tickc","Upfront fees, no surprises"),("shield","All health funds, HICAPS")]),
        '<div class="offer-float" style="background:var(--cyan)"><span class="k">Emergency care</span><div class="v">Same day</div><span class="d">Mon to Fri from 9am · Saturday from 8am</span></div>')
    callband = f'''<div class="call-band"><div class="wrap"><div><b>Severe pain, swelling or a knocked-out tooth?</b><span>Call us now so we can get you in as soon as possible. If you have a knocked-out tooth, keep it moist in milk and come straight in.</span></div><a class="btn btn-lg js-call" href="{TEL}">{I["phone"]} {PHONE}</a></div></div>'''
    book = booking(
        "Request an emergency appointment",
        "Grab the next available slot from our live appointment book, or request a call back and reception will ring you. If you are in severe pain, call us directly and we will fit you in.",
        [("Pick the next available time","Our appointment book updates in real time, so you can see today's openings."),("Or request a call back","Reception rings to confirm the earliest time we can see you."),("Relief, fast","Your dentist focuses on getting you out of pain first.")],
        "What to expect at your emergency visit",
        ["Seen as soon as possible, usually same day","Pain relief and diagnosis as the first priority","X-rays taken on site if needed","Clear quote before any treatment begins","Health fund claimed on the spot with HICAPS","Follow-up plan to fix the problem properly"],
        '<div class="price"><b>Fees from $180</b><span>fillings · emergency fee confirmed before treatment</span></div>',
        "Emergency Request", "We will ring you back as soon as we can to book you in.",
        ["Toothache or severe pain","Broken, chipped or cracked tooth","Lost filling or crown","Swelling or abscess","Knocked-out tooth","Wisdom tooth pain","Bleeding gums or trauma","Other emergency"],
        "Toothache or severe pain", urgency=True)
    urgent = f'''<section class="urgent" id="emergencies"><div class="wrap">
  <div class="sec-h center"><span class="kicker">What counts as an emergency</span><h2>If it hurts, it is worth a call</h2><p>Dental problems rarely fix themselves, and acting quickly usually means simpler, cheaper treatment. We treat all of these as emergencies.</p></div>
  <div class="urgent-list">
    <div><span class="ic">{I["alert"]}</span>Severe or throbbing toothache</div>
    <div><span class="ic">{I["alert"]}</span>Broken, chipped or cracked tooth</div>
    <div><span class="ic">{I["alert"]}</span>Knocked-out tooth</div>
    <div><span class="ic">{I["alert"]}</span>Swelling of the face, gums or jaw</div>
    <div><span class="ic">{I["alert"]}</span>Lost filling, crown or veneer</div>
    <div><span class="ic">{I["alert"]}</span>Abscess or infection</div>
    <div><span class="ic">{I["alert"]}</span>Wisdom tooth pain</div>
    <div><span class="ic">{I["alert"]}</span>Bleeding that will not stop</div>
    <div><span class="ic">{I["alert"]}</span>Broken denture or braces wire</div>
  </div>
</div></section>'''
    why = why_block("Why Western Sydney locals call us first", [
        ("bolt","","Same-day appointments","With six dentists on the roster we keep time aside every day for emergencies, so you are not left waiting in pain."),
        ("clock","y","Open 6 days","Late appointments Monday to Thursday and Saturday mornings from 8am. Easy parking via Sainsbury Road."),
        ("eye","","Upfront fees","We tell you the cost before we start. Fillings from $180, extractions and root canals quoted on the spot."),
        ("heart","y","Gentle with nervous patients","Emergencies are stressful. Our team will explain everything and get you comfortable first."),
    ])
    faq = faq_block([
        ("How quickly can you see me?","We keep emergency appointments available every day. Call us as soon as you can and we will usually see you the same day, or the next morning if you call late in the day. Saturday appointments are available from 8am."),
        ("How much does an emergency appointment cost?","It depends on what is needed. We will examine you, take any x-rays required and give you a clear quote before any treatment begins. As a guide, fillings start from $180 and root canal therapy from $840. Health fund rebates are claimed on the spot."),
        ("What should I do while I wait for my appointment?","Take over-the-counter pain relief as directed on the packet, rinse with warm salty water and avoid very hot, cold or sweet foods. For a knocked-out adult tooth, hold it by the crown (not the root), keep it in milk or saliva and come in immediately, ideally within the hour."),
        ("Can you help if I am not an existing patient?","Yes. We welcome new patients for emergency care. Just call or send a request and we will take your details over the phone."),
        ("Do you offer payment plans for emergency treatment?","Yes. If you need more extensive treatment such as a root canal or crown, we offer interest-free payment plans with on-the-spot approval, plus Afterpay and Zip, so you can get out of pain now and pay over time."),
        ("What if it is after hours?","Our hours are Monday to Thursday 9am to 6pm, Friday 9am to 5pm and Saturday 8am to 1pm. Send a request through this page at any time and we will call you first thing. If you have severe facial swelling, difficulty breathing or swallowing, go to your nearest hospital emergency department."),
    ], "Emergency dental questions")
    body = (topbar("Dental emergency? Same-day appointments · Call (02) 9623 7333") + header("Request Call Back") + hero_html + callband + nib_block() + book + rating_band() + urgent + why + funds_block() + team_block("Six dentists ready to help", "More dentists means more emergency appointment times. Whoever you see, you are in experienced, gentle hands.") + faq + location_block()
            + final_cta('Do not put up with the pain. <em>Call us now.</em>', "Same-day emergency appointments in St Marys, six days a week.", "Request a Call Back") + footer(TC_EM))
    return h + body

# ================= PAGE 4: THANK YOU =================
def page_thank_you():
    h = head("Appointment Confirmed | Western Sydney Smiles", "Your appointment with Western Sydney Smiles is confirmed.", "ty-page")
    body = f"""{topbar("Your appointment is confirmed")}
<header class="site"><div class="wrap">
  <a class="logo" href="https://westernsydneysmiles.com.au" aria-label="Western Sydney Smiles"><img src="img/logo.png" alt="Western Sydney Smiles" width="300" height="89"></a>
  <nav><a class="phone js-call" href="{TEL}">{I["phone"]}<span><small>Call us now</small>{PHONE}</span></a></nav>
</div></header>
<section class="ty"><div class="wrap">
  <div class="card">
    <div class="tick">{I["tick"]}</div>
    <span class="kicker" id="tyKicker">Booking confirmed</span>
    <h1 id="tyTitle">Your appointment is confirmed<span id="tyName"></span>!</h1>
    <p class="lead" id="tyLead">Thanks for booking with Western Sydney Smiles. You will receive a confirmation by SMS and email shortly, and our reception team will be in touch to finalise your booking.</p>
    <div class="next">
      <div><span class="n">1</span><b>Check your phone</b><span>A confirmation text and email with your appointment details is on its way. Save our number, {PHONE}, so you do not miss us.</span></div>
      <div><span class="n">2</span><b>Secure your spot</b><span>Reception will call to take a $50 deposit, which comes off your treatment on the day or is refunded with more than 24 hours' notice.</span></div>
      <div><span class="n">3</span><b>On the day</b><span>Arrive 10 minutes early with your health fund card, Medicare card and any recent x-rays. Free parking via Sainsbury Road.</span></div>
    </div>
    <div class="ctas"><a class="btn btn-outline" href="{MAPS}" target="_blank" rel="noopener">{I["pin"]} Get directions</a><a class="btn btn-yellow js-call" href="{TEL}">{I["phone"]} Need to change your time? Call us</a></div>
    <div class="deets">
      <div><b>Where to find us</b>{ADDRESS}<br>Next to Astley Medical Centre. Free parking via Sainsbury Road.</div>
      <div><b>Opening hours</b>Mon to Thu 9am to 6pm · Fri 9am to 5pm<br>Sat 8am to 1pm · Sun closed</div>
      <div><b>Bring with you</b>Health fund card (we claim on the spot with HICAPS), Medicare card for children's CDBS, and a list of any medications.</div>
      <div><b>Nervous about the dentist?</b>Let us know when you arrive. Our team is used to looking after anxious patients and will take things at your pace.</div>
    </div>
  </div>
  <div class="ty-more">
    <span class="kicker">While you wait</span>
    <div class="ty-links">
      <a href="index.html"><b>New patient offer</b><span>Check-up, clean &amp; x-rays for $199</span></a>
      <a href="dental-implants.html"><b>Dental implants</b><span>From $4,490 incl. crown</span></a>
      <a href="emergency-dentist.html"><b>Emergency dentist</b><span>Same-day appointments</span></a>
      <a href="https://westernsydneysmiles.com.au" target="_blank" rel="noopener"><b>Main website</b><span>Services, team and prices</span></a>
    </div>
  </div>
</div></section>
<footer><div class="wrap">
  <img src="img/logo-white.png" alt="Western Sydney Smiles">
  {FOOT_NAV}
  <p>Western Sydney Smiles · {ADDRESS} · <a class="js-call" href="{TEL}">{PHONE}</a> · <a href="https://westernsydneysmiles.com.au">westernsydneysmiles.com.au</a></p>
  <div class="tc">© 2026 Western Sydney Smiles.</div>
</div></footer>
<script>
  // Conversion: GTM listens for booking_complete on this page
  window.dataLayer=window.dataLayer||[]; window.dataLayer.push({{event:'booking_complete'}});
  // If the visitor arrived via the call-back form (not the live scheduler), switch to "request received" wording
  try{{var l=JSON.parse(sessionStorage.getItem('wss_lead')||'null'); if(l){{
    sessionStorage.removeItem('wss_lead');
    document.getElementById('tyKicker').textContent='Request received';
    document.getElementById('tyTitle').innerHTML='Thanks'+(l.first_name?' '+l.first_name:'')+', we will call you shortly';
    var when=(l.preferred_day&&l.preferred_day!=='Any day'?l.preferred_day:'')+(l.preferred_time&&l.preferred_time!=='Any time'?' '+l.preferred_time.toLowerCase():'');
    document.getElementById('tyLead').textContent='We have your request'+(l.service?' for '+l.service.replace(/\\s*\\(.*\\)/,'').toLowerCase():'')+(when?' ('+when.trim()+')':'')+'. Our reception team will call or text you to confirm a time that suits you. During opening hours this is usually within the hour.';
    var n=document.querySelectorAll('.next > div'); if(n[0]){{n[0].querySelector('b').textContent='We call you';n[0].querySelector('span:last-child').textContent='Reception will ring from {PHONE} to lock in your day and time. Save the number so you do not miss us.';}}
  }}}}catch(e){{}}
</script>
</body></html>"""
    return h + body

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages = {"index.html": page_new_patients(), "dental-implants.html": page_implants(), "emergency-dentist.html": page_emergency(), "thank-you.html": page_thank_you()}
    for name, content in pages.items():
        with open(os.path.join(OUT, name), "w") as f: f.write(content)
    with open(os.path.join(OUT, "main.js"), "w") as f: f.write(MAIN_JS)
    print("built:", ", ".join(pages))
