# Sunway Smart Property Finder

An academic prototype for intelligent property discovery, built as an
independent demo, **not affiliated with or endorsed by Sunway Property.**
Uses publicly available Sunway Property listing information as demonstration
data only.

Four features:
1.  **Find My Property** - scored, ranked recommendations from a form
2.  **Property Assistant** - chat interface backed by the real database
3.  **Sustainability Dashboard** - green features per development
4.  **Everything Around My Property** - transport / shopping / schools / etc.

Stack: **Django + Python** → **SQLite (default) or MySQL** → HTML/CSS/JS frontend.

---

## 1. Quick start (fastest way to see it running — uses SQLite, zero setup)

```bash
# unzip the project, then inside the sunway_smart folder:
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py load_sample_data      # loads 15 demo Sunway-style properties
python manage.py load_greenre_data     # loads real GreenRE certification data
python manage.py createsuperuser       # for the admin panel — pick your own login

python manage.py runserver
```

Open **http://127.0.0.1:8000/** - the whole site works immediately with SQLite,
no database server needed.

Open **http://127.0.0.1:8000/admin/** to add, edit, or remove properties.

---

## 2. Switching to MySQL

1. Create the database:
   ```sql
   CREATE DATABASE sunway_smart;
   ```
2. Install the MySQL driver:
   ```bash
   pip install mysqlclient
   # if that fails to build on Windows, use instead:
   pip install pymysql
   # and add this to the very top of sunway_smart/settings.py:
   #   import pymysql
   #   pymysql.install_as_MySQLdb()
   ```
3. Open `sunway_smart/settings.py`, find the `DATABASES` section, **comment
   out the SQLite block and uncomment the MySQL block**, then fill in your
   password:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'sunway_smart',
           'USER': 'root',
           'PASSWORD': 'YOUR_MYSQL_PASSWORD',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
4. Re-run: `python manage.py migrate` then `python manage.py load_sample_data`.

---

## 3. Project structure

```
sunway_smart/
├── manage.py
├── requirements.txt
├── sunway_smart/          project settings & root urls.py
├── properties/            the app: models, views, admin, urls
│   ├── models.py          Property, PropertyFeature, Sustainability, NearbyPlace
│   ├── views.py           home, finder (scoring), explore, property_detail,
│   │                      sustainability, assistant, assistant_query (JSON API)
│   ├── admin.py           inline editing of features / sustainability / nearby
│   ├── templatetags/      property_extras.py — thumbnail colour + initials
│   └── management/commands/load_sample_data.py   ← the 15 demo properties
├── templates/              base.html + one template per page
└── static/
    ├── css/style.css       full design system (see design notes below)
    └── js/app.js            card hover polish + live assistant chat
```

---

## 4. GreenRE certification data

`GreenRECertification` is a new model holding real certification records
manually sourced from [GreenRE's public project listing](https://www.greenre.org/projects/green-buildings-and-townships/)
(no public API exists for this data — see `load_greenre_data.py` for notes).
Run `python manage.py load_greenre_data` to load it. Entries whose project
name exactly matches one of the demo properties are auto-linked and show a
rating badge on that property's page; the rest appear only in the full table
on the Sustainability dashboard (many GreenRE entries are hotels, malls,
offices, etc. that aren't residential listings in this app at all).

To keep this current: re-visit the GreenRE listing periodically and update
`ROWS` in `properties/management/commands/load_greenre_data.py` — ratings
carry certification/expiry dates and get renewed.


## 5. Design notes

Palette is a canopy‑green / turmeric‑gold / clay‑rust set on a soft eucalyptus
background (tokens at the top of `style.css`) rather than a generic template
look. Headings use **Fraunces** (a display serif with some warmth, loaded from
Google Fonts), body text uses **Work Sans**, and data (scores, stats, prices)
uses **IBM Plex Mono** to visually separate "data" from "prose." The repeating
"ring" element (`.ring` in CSS) is the signature device — it's used for match
scores on results and for the 61-green-buildings stat on the homepage, tying
the numbers together visually across the site.

## 6. What this build deliberately leaves out

Per the original 1-day scope: no authentication, no payments, no real booking
flow, no live availability sync, no web scraping, no full Google Maps
integration, no deployment config. All good "phase 2" additions once the MVP
is working and demoed.

## 7. Demo script (for your presentation)

1. **Home** → click *Find My Property*.
2. Enter **budget RM600,000**, type **Serviced Apartment**, transport **Yes**,
   green **Yes** → submit.
3. Point out the ranked list with match-score rings.
4. Click into a result → show sustainability features + nearby places.
5. Go to **Sustainability** → point out the 2 townships / 61 buildings figures
   (these are Sunway's own published figures, shown as reference stats, not
   numbers this app calculates).
6. Go to **Assistant** → type "RM600k near LRT with green features" → show the
   live, database-backed matches.
