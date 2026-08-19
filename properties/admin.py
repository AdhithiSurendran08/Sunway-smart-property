from django.contrib import admin
from .models import Property, PropertyFeature, Sustainability, NearbyPlace, GreenRECertification


class PropertyFeatureInline(admin.TabularInline):
    model = PropertyFeature
    extra = 1


class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1


class SustainabilityInline(admin.StackedInline):
    model = Sustainability
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'property_type', 'price', 'status', 'freehold')
    list_filter = ('property_type', 'status', 'freehold')
    search_fields = ('name', 'location')
    inlines = [PropertyFeatureInline, NearbyPlaceInline, SustainabilityInline]


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('property', 'feature')


@admin.register(Sustainability)
class SustainabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'green_certification', 'solar_panels', 'ev_charging')


@admin.register(NearbyPlace)
class NearbyPlaceAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'category', 'distance')


@admin.register(GreenRECertification)
class GreenRECertificationAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'rating', 'certification_type', 'building_category', 'date_certified', 'status', 'property')
    list_filter = ('rating', 'certification_type', 'status')
    search_fields = ('project_name', 'developer')
