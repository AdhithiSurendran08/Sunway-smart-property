from django.core.management.base import BaseCommand
from properties.models import Property, PropertyFeature, Sustainability, NearbyPlace


DATA = [
    {
        "name": "Sunway Flora 2", "location": "Cheras, Kuala Lumpur",
        "property_type": "Serviced Apartment", "price": 568000,
        "min_size": 850, "max_size": 1100, "bedrooms": 3,
        "status": "New Launch", "freehold": False,
        "description": "Township living with a covered walkway link to the LRT and retail conveniences within the neighbourhood.",
        "features": ["Covered walkway to LRT", "Retail conveniences", "Swimming pool", "Gymnasium", "24-hour security"],
        "sustainability": dict(green_certification="Green Township Initiative", solar_panels=True, green_space=True, ev_charging=True, recycling=True, water_efficient=True),
        "nearby": [("LRT Station", "Transport", "Covered walkway"), ("Neighbourhood retail", "Shopping", "Nearby"), ("Community park", "Park", "Nearby")],
    },
    {
        "name": "Sunway Flora Residences", "location": "Cheras, Kuala Lumpur",
        "property_type": "Condominium", "price": 610000,
        "min_size": 900, "max_size": 1250, "bedrooms": 3,
        "status": "Available", "freehold": False,
        "description": "Sister development to Sunway Flora 2 within the same township, with expanded facility decks.",
        "features": ["Sky facilities deck", "Co-working lounge", "Multi-tier security", "Children's playground"],
        "sustainability": dict(solar_panels=True, green_space=True, rainwater_harvesting=True, recycling=True),
        "nearby": [("LRT Station", "Transport", "8-min walk"), ("Retail podium", "Shopping", "Ground floor"), ("Clinic", "Hospital", "1.2km")],
    },
    {
        "name": "Sunway d'hill Residences", "location": "Kepong, Kuala Lumpur",
        "property_type": "Condominium", "price": 598000,
        "min_size": 950, "max_size": 1300, "bedrooms": 3,
        "status": "Available", "freehold": False,
        "description": "Elevated hillside condominium with landscaped tiers overlooking the surrounding greenery.",
        "features": ["Infinity pool", "Hillside jogging trail", "Clubhouse", "EV charging bays"],
        "sustainability": dict(green_space=True, ev_charging=True, water_efficient=True),
        "nearby": [("Kepong Sentral", "Transport", "1.5km"), ("Metro Prima", "Shopping", "2km"), ("Selayang Hospital", "Hospital", "4km")],
    },
    {
        "name": "Sunway Alishan", "location": "Cheras, Kuala Lumpur",
        "property_type": "Condominium", "price": 480000,
        "min_size": 750, "max_size": 1050, "bedrooms": 2,
        "status": "Available", "freehold": False,
        "description": "Established Cheras address close to Taman Mutiara MRT and EkoCheras Mall.",
        "features": ["Landscaped garden deck", "Swimming pool", "Function hall", "Surau"],
        "sustainability": dict(green_space=True, recycling=True),
        "nearby": [("Taman Mutiara MRT", "Transport", "800m"), ("EkoCheras Mall", "Shopping", "400m"), ("Cheras Primary School", "School", "1km")],
    },
    {
        "name": "Sunway Serene 2", "location": "Cheras South, Kuala Lumpur",
        "property_type": "Serviced Apartment", "price": 455000,
        "min_size": 700, "max_size": 950, "bedrooms": 2,
        "status": "New Launch", "freehold": False,
        "description": "Compact, well-priced apartments aimed at first-time buyers and young families.",
        "features": ["Rooftop garden", "Gymnasium", "Kids' pool", "24-hour security"],
        "sustainability": dict(green_space=True, solar_panels=True, motion_sensor_lighting=True),
        "nearby": [("Bus interchange", "Transport", "600m"), ("Wet market", "Food", "500m"), ("Community clinic", "Hospital", "1.8km")],
    },
    {
        "name": "Sunway Cochrane", "location": "Cochrane, Kuala Lumpur",
        "property_type": "Serviced Apartment", "price": 620000,
        "min_size": 880, "max_size": 1150, "bedrooms": 3,
        "status": "Available", "freehold": False,
        "description": "Transit-oriented development directly connected to Cochrane MRT station.",
        "features": ["Direct MRT link", "Sky lounge", "Co-working space", "Retail podium"],
        "sustainability": dict(green_space=True, ev_charging=True, recycling=True, water_efficient=True),
        "nearby": [("Cochrane MRT", "Transport", "Direct link"), ("Retail podium", "Shopping", "Ground floor"), ("International school", "School", "2.5km")],
    },
    {
        "name": "Sfera Residence", "location": "Jalan Ipoh, Kuala Lumpur",
        "property_type": "Serviced Apartment", "price": 520000,
        "min_size": 800, "max_size": 1080, "bedrooms": 2,
        "status": "New Launch", "freehold": False,
        "description": "New-launch community close to the Jalan Ipoh commercial corridor.",
        "features": ["Infinity edge pool", "Gymnasium", "Multi-purpose hall"],
        "sustainability": dict(solar_panels=True, green_space=True),
        "nearby": [("Jalan Ipoh LRT", "Transport", "1km"), ("Sunway Velocity Mall", "Shopping", "3.5km")],
    },
    {
        "name": "Sunway Velocity 3", "location": "Cheras / Jalan Peel, Kuala Lumpur",
        "property_type": "SOHO", "price": 545000,
        "min_size": 600, "max_size": 850, "bedrooms": 2,
        "status": "Available", "freehold": False,
        "description": "Latest tower in the Sunway Velocity integrated township, close to the mall and MRT.",
        "features": ["Integrated with Sunway Velocity Mall", "Co-working deck", "Rooftop pool"],
        "sustainability": dict(green_space=True, ev_charging=True, recycling=True),
        "nearby": [("Maluri LRT/MRT", "Transport", "700m"), ("Sunway Velocity Mall", "Shopping", "Connected"), ("Sunway Medical Centre Velocity", "Hospital", "Connected")],
    },
    {
        "name": "Sunway LakeHills", "location": "Semenyih, Selangor",
        "property_type": "Terrace House", "price": 780000,
        "min_size": 1800, "max_size": 2200, "bedrooms": 4,
        "status": "New Launch", "freehold": True,
        "description": "Landed township development set around a central lake and green corridor.",
        "features": ["Lakeside jogging track", "Gated & guarded", "Clubhouse", "Freehold titles"],
        "sustainability": dict(green_space=True, rainwater_harvesting=True, water_efficient=True),
        "nearby": [("Semenyih town centre", "Shopping", "3km"), ("UNIKL campus", "School", "2km"), ("Semenyih Hospital", "Hospital", "5km")],
    },
    {
        "name": "Sunway Majestic", "location": "Jalan Ipoh, Kuala Lumpur",
        "property_type": "Serviced Apartment", "price": 495000,
        "min_size": 720, "max_size": 980, "bedrooms": 2,
        "status": "Available", "freehold": False,
        "description": "City-fringe development with a retail podium and easy access to the Jalan Ipoh corridor.",
        "features": ["Retail podium", "Swimming pool", "Sky gym"],
        "sustainability": dict(green_space=True, recycling=True),
        "nearby": [("Sentul LRT", "Transport", "1.3km"), ("Local wet market", "Food", "400m")],
    },
    {
        "name": "Sunway Citrine Residence", "location": "Old Klang Road, Kuala Lumpur",
        "property_type": "Condominium", "price": 655000,
        "min_size": 950, "max_size": 1300, "bedrooms": 3,
        "status": "Available", "freehold": False,
        "description": "Established Old Klang Road community with mature landscaping and a full facility deck.",
        "features": ["Full condo facility deck", "24-hour security", "Multi-tier access control"],
        "sustainability": dict(green_space=True, solar_panels=True, ev_charging=True),
        "nearby": [("Old Klang Road LRT", "Transport", "1.8km"), ("Mid Valley Megamall", "Shopping", "4km")],
    },
    {
        "name": "Sunway Wellesley Serene Villas", "location": "Seberang Perai, Penang",
        "property_type": "Terrace House", "price": 890000,
        "min_size": 2000, "max_size": 2400, "bedrooms": 4,
        "status": "New Launch", "freehold": True,
        "description": "Landed villas within the Sunway Wellesley township on the Penang mainland.",
        "features": ["Gated & guarded", "Central park", "Freehold titles"],
        "sustainability": dict(green_space=True, rainwater_harvesting=True),
        "nearby": [("Butterworth station", "Transport", "6km"), ("Design Village Mall", "Shopping", "3km")],
    },
    {
        "name": "Sunway Dora", "location": "Ipoh, Perak",
        "property_type": "Terrace House", "price": 420000,
        "min_size": 1600, "max_size": 1900, "bedrooms": 4,
        "status": "Completed", "freehold": True,
        "description": "Completed landed community in Sunway City Ipoh, close to established amenities.",
        "features": ["Gated & guarded", "Playground", "Freehold titles"],
        "sustainability": dict(green_space=True, water_efficient=True),
        "nearby": [("Ipoh town centre", "Shopping", "5km"), ("Sunway City Ipoh clinic", "Hospital", "2km")],
    },
    {
        "name": "Sunway Bayu", "location": "Sunway City Ipoh, Perak",
        "property_type": "Apartment", "price": 350000,
        "min_size": 850, "max_size": 1050, "bedrooms": 3,
        "status": "Available", "freehold": False,
        "description": "Affordable apartment living within the Sunway City Ipoh master plan.",
        "features": ["Community pool", "Multi-purpose hall", "Playground"],
        "sustainability": dict(green_space=True),
        "nearby": [("Sunway City Ipoh commercial hub", "Shopping", "1.5km"), ("Falim Clinic", "Hospital", "3km")],
    },
    {
        "name": "Sunway Onsen Suites", "location": "Sunway City Ipoh, Perak",
        "property_type": "Serviced Apartment", "price": 468000,
        "min_size": 780, "max_size": 1020, "bedrooms": 2,
        "status": "New Launch", "freehold": False,
        "description": "Wellness-themed serviced suites next to Lost World of Tambun's hot springs.",
        "features": ["Onsen-inspired wellness deck", "Infinity pool", "Sky gym"],
        "sustainability": dict(solar_panels=True, water_efficient=True, green_space=True),
        "nearby": [("Lost World of Tambun", "Park", "Adjacent"), ("Sunway City Ipoh hub", "Shopping", "2km")],
    },
]


class Command(BaseCommand):
    help = "Loads ~15 demo Sunway-style properties (fictional prototype dataset)."

    def handle(self, *args, **options):
        created = 0
        for item in DATA:
            prop, was_created = Property.objects.update_or_create(
                name=item["name"],
                defaults=dict(
                    location=item["location"],
                    property_type=item["property_type"],
                    price=item["price"],
                    min_size=item["min_size"],
                    max_size=item["max_size"],
                    bedrooms=item["bedrooms"],
                    status=item["status"],
                    freehold=item["freehold"],
                    description=item["description"],
                ),
            )

            prop.features.all().delete()
            for f in item["features"]:
                PropertyFeature.objects.create(property=prop, feature=f)

            Sustainability.objects.filter(property=prop).delete()
            Sustainability.objects.create(property=prop, **item["sustainability"])

            prop.nearby_places.all().delete()
            for name, category, distance in item["nearby"]:
                NearbyPlace.objects.create(property=prop, name=name, category=category, distance=distance)

            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(DATA)} properties ({created} newly created)."
        ))
