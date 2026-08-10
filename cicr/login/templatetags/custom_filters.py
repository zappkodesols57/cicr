from django import template

register = template.Library()

@register.filter(name='month_name')
def month_name(month_number):
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    return month_names[month_number - 1] if 1 <= month_number <= 12 else 'Unknown'
