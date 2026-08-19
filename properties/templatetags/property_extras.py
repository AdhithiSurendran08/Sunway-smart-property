from django import template

register = template.Library()

TINTS = {
    'Condominium': '#1F4D3A',
    'Serviced Apartment': '#2C6B50',
    'Apartment': '#255A44',
    'Terrace House': '#A84B2A',
    'Landed': '#A84B2A',
    'Townhouse': '#C98A2C',
    'SOHO': '#173D2C',
}


@register.filter
def type_tint(property_type):
    return TINTS.get(property_type, '#1F4D3A')


@register.filter
def initials(name):
    words = [w for w in name.replace("'", "").split(' ') if w]
    letters = [w[0].upper() for w in words if w[0].isalpha()]
    return ''.join(letters[:2]) if letters else '?'


@register.filter
def rating_color(rating):
    return {
        'Platinum': '#6B7280',
        'Gold': '#C98A2C',
        'Silver': '#8B95A5',
        'Bronze': '#A84B2A',
    }.get(rating, '#8B95A5')
