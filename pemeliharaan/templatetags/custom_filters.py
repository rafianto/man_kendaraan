from django import template

register = template.Library()


@register.filter(name='rupiah')
def rupiah(value):
    """Format angka menjadi format Rupiah."""
    try:
        val = float(value)
        return f"Rp {val:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "Rp 0"


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='jenis_badge')
def jenis_badge(value):
    badges = {
        'mobil': 'primary',
        'motor': 'success',
        'sepeda_listrik': 'info',
    }
    return badges.get(value, 'secondary')