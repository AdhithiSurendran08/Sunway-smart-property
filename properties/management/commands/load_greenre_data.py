import datetime
from django.core.management.base import BaseCommand
from properties.models import Property, GreenRECertification


def d(s):
    if not s or s == '-':
        return None
    day, month, year = s.split('/')
    return datetime.date(int(year), int(month), int(day))


# Sourced manually from GreenRE's public listing:
# https://www.greenre.org/projects/green-buildings-and-townships/
# GreenRE does not offer a public API, so this is a manually maintained
# snapshot — re-check periodically, since ratings carry expiry dates.
ROWS = [
    ("Sunway International School Sunway City KL", "Final Certification", "Platinum", "Sunway Education Group Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.1)", "07/11/2024", "07/11/2027"),
    ("Sunway Medical Centre Ipoh", "Final Certification", "Silver", "Sunway Medical Center Ipoh Sdn Bhd", "HEALTHCARE FACILITIES (HC v1.0)", "09/07/2026", "08/07/2029"),
    ("Sunway Dora", "Final Certification", "Silver", "Sunway Tunas Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.2) (HIGHRISE)", "23/12/2025", "23/12/2028"),
    ("Sunway REIT Hypermarket – Putra Heights", "Final Certification", "Silver", "Sunway Real Estate Investment Trust", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.3)", "27/11/2025", "27/11/2028"),
    ("Sunway Pyramid Hotel", "Final Certification", "Platinum", "Sunway Real Estate Investment Trust", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.3)", "07/12/2025", "07/12/2028"),
    ("Sunway Enterprise Park Phase 2", "Provisional Certification", "Silver", "Emerald Tycoon Sdn Bhd", "INDUSTRIAL FACILITIES (IND v1.0)", "25/12/2023", None),
    ("Sunway Belfield Residence", "Final Certification", "Platinum", "Sunway Belfield Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.0)", "16/11/2025", "16/11/2028"),
    ("Sunway Putra Tower", "Final Certification", "Platinum", "Sunway REIT Management Sdn Bhd", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.3)", "27/11/2025", "27/11/2028"),
    ("Sunway GEO (Parcel CP4)", "Renewal 1", "Bronze", "Sunway Geo Sdn. Bhd.", "NON-RESIDENTIAL BUILDING (NRB v3.0)", "21/11/2023", "21/11/2026"),
    ("Sunway REIT Hypermarket – Ulu Kelang", "Final Certification", "Silver", "Sunway Real Estate Investment Trust", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.3)", "01/12/2025", "01/12/2028"),
    ("EQUALBASE SUNWAY 103 WAREHOUSE 3", "Provisional Certification", "Gold", "EQUALBASE SUNWAY 103 SDN. BHD", "INDUSTRIAL FACILITIES (IND v1.1)", "26/05/2025", None),
    ("Sunway Avila", "Final Certification", "Gold", "Sunglobal Resources Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "18/09/2024", "18/09/2027"),
    ("Sunway Wellesley 3A1", "Provisional Certification", "Gold", "Sunway Bintang Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.3) (HIGHRISE)", "07/12/2025", None),
    ("Sunway Serene", "Provisional Certification", "Gold", "Sunway Serene Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.0)", "08/07/2018", None),
    ("Sunway Onsen Suites", "Final Certification", "Silver", "Sunway City (Ipoh) Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "31/10/2023", "31/10/2026"),
    ("Sunway Putra Hotel", "Final Certification", "Gold", "Sunway REIT Management Sdn Bhd", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.3)", "15/12/2024", "15/12/2027"),
    ("Sunway Alishan (Taman Billion)", "Provisional Certification", "Gold", "Sunway Kinrara Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "24/01/2022", None),
    ("Sunway Lenang Heights", "Provisional Certification", "Silver", "Sunway City JB Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.2) (LANDED)", "10/01/2023", None),
    ("Sunway Carnival Mall 2 (New Mall)", "Final Certification", "Gold", "Sunway Reit Management Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.0)", "18/11/2025", "18/11/2028"),
    ("Sunway Flora Phase 2", "Provisional Certification", "Gold", "Sunway Flora Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.3) (HIGHRISE)", "15/04/2025", None),
    ("Sunway University - New University Block", "Final Certification", "Platinum", "Sunway REIT Management Sdn Bhd", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.2)", "22/12/2024", "22/12/2027"),
    ("Sunway South Quay Square - Office Tower 1 (OT1)", "Provisional Certification", "Platinum", "Sunway South Quay Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.2)", "08/11/2023", None),
    ("Sunway Big Box Retail Park", "Final Certification", "Bronze", "Sunway Marketplace Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.2)", "26/03/2025", "26/03/2028"),
    ("Sunway Visio Office", "Renewal 2", "Silver", "Sunway Integrated Properties Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.0)", "17/08/2026", "16/08/2029"),
    ("Sunway Mentari (YOLO)", "Provisional Certification", "Gold", "OCR Properties Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.0)", "01/12/2021", None),
    ("Sunway Resort Hotel", "Renewal 1", "Platinum", "Sunway REIT Management Sdn Bhd (as attorney for RHB Trustees Berhad)", "EXISTING NON-RESIDENTIAL BUILDING (ENRB v3.2)", "31/10/2023", "31/10/2026"),
    ("Sunway Cochrane", "Provisional Certification", "Gold", "Sunway Cochrane Sdn Bhd f.k.a. Sunway Rahman Putra Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.3) (HIGHRISE)", "10/11/2025", None),
    ("Sunway GRID Residence", "Final Certification", "Gold", "Sunway Iskandar Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "09/01/2024", "09/01/2027"),
    ("EQUALBASE SUNWAY 103 WAREHOUSE 1 & 2", "Provisional Certification", "Gold", "EQUALBASE SUNWAY 103 SDN. BHD.", "INDUSTRIAL FACILITIES (IND v1.1)", "26/05/2025", None),
    ("Sunway Wellesley", "Provisional Certification", "Bronze", "Sunway Bintang Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.2) (HIGHRISE)", "14/03/2024", None),
    ("Sunway Medical Centre Damansara", "Provisional Certification", "Gold", "Paradigm Fairview Sdn Bhd", "HEALTHCARE FACILITIES (HC v1.0)", "06/11/2025", None),
    ("Sunway CP2 - Office Tower 2", "Provisional Certification", "Platinum", "Sunway South Quay Sdn Bhd", "NON-RESIDENTIAL BUILDING (NRB v3.1)", "26/06/2023", None),
    ("Sunway Velocity Two Plot B", "Final Certification", "Gold", "Sunway Velocity Two Sdn Bhd", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "12/11/2025", "12/11/2028"),
    ("Sunway d'hill Residences (KD10)", "Provisional Certification", "Gold", "Sunway PKNS", "RESIDENTIAL BUILDING AND LANDED HOME (RES v3.1) (HIGHRISE)", "05/08/2021", None),
]

# Maps a GreenRE project_name -> the exact Property.name in load_sample_data.py,
# only where they clearly refer to the same development.
LINKS = {
    "Sunway Dora": "Sunway Dora",
    "Sunway Onsen Suites": "Sunway Onsen Suites",
    "Sunway Alishan (Taman Billion)": "Sunway Alishan",
    "Sunway Flora Phase 2": "Sunway Flora 2",
    "Sunway Cochrane": "Sunway Cochrane",
    "Sunway d'hill Residences (KD10)": "Sunway d'hill Residences",
}


class Command(BaseCommand):
    help = "Loads real GreenRE certification records (sourced from greenre.org) and links matching properties."

    def handle(self, *args, **options):
        GreenRECertification.objects.all().delete()

        linked = 0
        for project_name, cert_type, rating, developer, category, cert_date, expiry_date in ROWS:
            prop = None
            if project_name in LINKS:
                prop = Property.objects.filter(name=LINKS[project_name]).first()
                if prop:
                    linked += 1

            GreenRECertification.objects.create(
                property=prop,
                project_name=project_name,
                certification_type=cert_type,
                rating=rating,
                developer=developer,
                building_category=category,
                date_certified=d(cert_date),
                date_expiry=d(expiry_date),
                status="Active",
            )

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(ROWS)} GreenRE certifications ({linked} linked to existing properties)."
        ))
