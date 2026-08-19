from django.shortcuts import render, get_object_or_404
from .models import Property, Sustainability, GreenRECertification


def home(request):
    stats = {
        'total_properties': Property.objects.count(),
        'green_townships': 2,
        'green_buildings': 61,
    }
    return render(request, 'home.html', {'stats': stats})


def finder(request):

    if request.method == 'POST':

        budget = float(request.POST.get('budget') or 0)
        property_type = request.POST.get('property_type')
        transport = request.POST.get('transport')
        green = request.POST.get('green')

        properties = Property.objects.filter(status__in=['Available', 'New Launch'])

        results = []

        for prop in properties:
            score = 0

            if prop.price:
                if float(prop.price) <= budget:
                    score += 30
                elif float(prop.price) <= budget * 1.1:
                    score += 15

            if property_type:
                if prop.property_type == property_type:
                    score += 20

            if transport == 'yes':
                transport_exists = prop.features.filter(
                    feature__icontains='LRT'
                ).exists() or prop.nearby_places.filter(category='Transport').exists()
                if transport_exists:
                    score += 20

            if green == 'yes':
                try:
                    sustainability = prop.sustainability
                    if sustainability.green_space:
                        score += 15
                    if sustainability.solar_panels:
                        score += 5
                    if sustainability.ev_charging:
                        score += 5
                except Sustainability.DoesNotExist:
                    pass

            if prop.status == 'Available':
                score += 10

            if prop.freehold:
                score += 5

            results.append({'property': prop, 'score': min(score, 100)})

        results.sort(key=lambda x: x['score'], reverse=True)
        results = results[:5]

        return render(request, 'results.html', {'results': results})

    return render(request, 'finder.html')


def explore(request):
    properties = Property.objects.all().order_by('name')

    property_type = request.GET.get('property_type')
    if property_type:
        properties = properties.filter(property_type=property_type)

    return render(request, 'explore.html', {'properties': properties})


def property_detail(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    greenre = prop.greenre_certifications.first()
    return render(request, 'property_detail.html', {'property': prop, 'greenre': greenre})


def sustainability(request):
    properties = Property.objects.all()
    greenre_certs = GreenRECertification.objects.all().order_by('-date_certified')
    return render(request, 'sustainability.html', {
        'properties': properties,
        'greenre_certs': greenre_certs,
    })


def assistant(request):
    return render(request, 'assistant.html')


def assistant_query(request):
    import re
    from django.http import JsonResponse

    message = request.GET.get('q', '').lower()

    # crude budget extraction: "600k", "rm600,000", "600000"
    budget = None
    m = re.search(r'(\d[\d,]*)\s*k\b', message)
    if m:
        budget = float(m.group(1).replace(',', '')) * 1000
    else:
        m = re.search(r'(\d[\d,]{4,})', message.replace(',', ''))
        if m:
            budget = float(m.group(1))

    wants_transport = any(w in message for w in ['lrt', 'mrt', 'transport', 'train', 'station'])
    wants_green = any(w in message for w in ['green', 'sustainable', 'eco', 'solar', 'ev charging'])

    type_keywords = {
        'condo': 'Condominium', 'condominium': 'Condominium',
        'serviced apartment': 'Serviced Apartment',
        'apartment': 'Apartment',
        'terrace': 'Terrace House',
        'townhouse': 'Townhouse',
        'soho': 'SOHO',
    }
    wanted_type = None
    for kw, val in type_keywords.items():
        if kw in message:
            wanted_type = val
            break

    properties = Property.objects.filter(status__in=['Available', 'New Launch'])

    scored = []
    for prop in properties:
        score = 0
        if budget and prop.price:
            if float(prop.price) <= budget:
                score += 40
            elif float(prop.price) <= budget * 1.1:
                score += 20
        elif not budget:
            score += 10

        if wanted_type and prop.property_type == wanted_type:
            score += 25

        if wants_transport:
            if prop.nearby_places.filter(category='Transport').exists() or \
               prop.features.filter(feature__icontains='LRT').exists():
                score += 25

        if wants_green:
            try:
                s = prop.sustainability
                if s.green_space or s.solar_panels or s.ev_charging:
                    score += 25
            except Sustainability.DoesNotExist:
                pass

        if prop.location.lower() in message:
            score += 20

        if score > 0:
            scored.append({
                'id': prop.id,
                'name': prop.name,
                'location': prop.location,
                'property_type': prop.property_type,
                'price': float(prop.price) if prop.price else None,
                'score': min(score, 100),
                'url': f'/property/{prop.id}/',
            })

    scored.sort(key=lambda x: x['score'], reverse=True)

    return JsonResponse({
        'results': scored[:3],
        'understood': {
            'budget': budget,
            'wants_transport': wants_transport,
            'wants_green': wants_green,
            'wanted_type': wanted_type,
        }
    })
