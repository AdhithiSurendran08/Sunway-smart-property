from django.db import models


class Property(models.Model):

    PROPERTY_TYPES = [
        ('Condominium', 'Condominium'),
        ('Serviced Apartment', 'Serviced Apartment'),
        ('Apartment', 'Apartment'),
        ('Terrace House', 'Terrace House'),
        ('Landed', 'Landed'),
        ('Townhouse', 'Townhouse'),
        ('SOHO', 'SOHO'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('New Launch', 'New Launch'),
        ('Completed', 'Completed'),
        ('Sold Out', 'Sold Out'),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_size = models.IntegerField(null=True, blank=True)
    max_size = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    freehold = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)

    def __str__(self):
        return self.feature


class Sustainability(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='sustainability')
    green_certification = models.CharField(max_length=200, blank=True)
    solar_panels = models.BooleanField(default=False)
    rainwater_harvesting = models.BooleanField(default=False)
    recycling = models.BooleanField(default=False)
    ev_charging = models.BooleanField(default=False)
    green_space = models.BooleanField(default=False)
    water_efficient = models.BooleanField(default=False)
    motion_sensor_lighting = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.name} Sustainability"


class NearbyPlace(models.Model):
    CATEGORY_CHOICES = [
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Hospital', 'Hospital'),
        ('School', 'School'),
        ('Park', 'Park'),
        ('Food', 'Food'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='nearby_places')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    distance = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GreenRECertification(models.Model):
    """
    Sourced manually from GreenRE's public certification listing
    (greenre.org/projects/green-buildings-and-townships/), since GreenRE
    does not expose a public API. Re-check and refresh periodically —
    ratings carry expiry dates and renewals.
    """

    RATING_CHOICES = [
        ('Platinum', 'Platinum'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
    ]

    CERT_TYPE_CHOICES = [
        ('Final Certification', 'Final Certification'),
        ('Provisional Certification', 'Provisional Certification'),
        ('Renewal 1', 'Renewal 1'),
        ('Renewal 2', 'Renewal 2'),
    ]

    # Optional link to a Property in this app, when the GreenRE project
    # is one of ours. Many GreenRE entries are hotels, offices, malls,
    # schools etc. that aren't in the Property table at all.
    property = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='greenre_certifications'
    )

    project_name = models.CharField(max_length=250)
    certification_type = models.CharField(max_length=50, choices=CERT_TYPE_CHOICES)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    developer = models.CharField(max_length=250, blank=True)
    building_category = models.CharField(max_length=150, blank=True)
    date_certified = models.DateField(null=True, blank=True)
    date_expiry = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')

    class Meta:
        ordering = ['-date_certified']

    def __str__(self):
        return f"{self.project_name} — GreenRE {self.rating}"
