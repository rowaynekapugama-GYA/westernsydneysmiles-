# Western Sydney Smiles – Google Ads landing pages

Built by Generate Your Audience. Flat static site, no build step needed to deploy. Upload the whole folder to Vercel (or any static host) as-is.

## Pages
| File | Campaign | Primary conversion |
|---|---|---|
| `index.html` | New Patients ($199 offer, nib First Choice no gap) | Booking form → `thank-you.html` |
| `dental-implants.html` | Dental Implants (from $4,490 incl. crown) | Consultation form → `thank-you.html` |
| `emergency-dentist.html` | Emergency Dentist (same-day) | Call first, form as backup → `thank-you.html` |
| `thank-you.html` | Conversion page (all three forms land here) | Fires `booking_complete` dataLayer event |

Suggested final URLs: `book.westernsydneysmiles.com.au/`, `/dental-implants`, `/emergency-dentist`.

## Before go-live (two edits in `build.py`, or directly in the HTML)
1. **GTM container** – replace `GTM-XXXXXXX` with the Western Sydney Smiles container ID (appears in every page's `<head>` and `<noscript>`).
2. **Form endpoint** – set `FORM_ENDPOINT` to the SmileOx webhook / lead endpoint. The form POSTs JSON:
   `first_name, last_name, mobile, email, patient_type, service, urgency (emergency page only), preferred_day, preferred_time, notes, source, page, page_url, submitted_at`.
   With the endpoint blank the form runs in demo mode and simply redirects to the thank-you page.

## Tracking hooks (already wired)
- `.js-call` on every phone link → pushes `call_click`
- `.js-book` on every Book button → pushes `book_click`
- Successful form submit → pushes `booking_request` (with `service` and `patient_type`)
- Thank-you page load → pushes `booking_complete` ← use this as the Google Ads conversion trigger
- Honeypot field (`website`) blocks basic bots; AU mobile validation on the form

## Regenerating
`python3 build.py` rebuilds all four pages from the shared template (header, booking form, nib section, health funds, team, FAQ, footer are shared so changes apply everywhere).

## Content sources
Offers, fees, hours, team and nib First Choice details were taken from westernsydneysmiles.com.au (home, prices, team, book-online, contact pages) on 6 Oct 2026. Google rating 4.9 from 263 reviews (shown as 260+).
