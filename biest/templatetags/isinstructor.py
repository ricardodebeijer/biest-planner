from django import template

register = template.Library()


@register.filter(name='isinstructor')
def isinstructor(input):
    red = 'artikel-red'
    yellow = 'artikel-yellow'
    activiteit = 'artikel-none'
    if input.startswith('*Instructeur'):
        if input == '*Instructeur':
            return red
        else:
            return yellow
    else:
        return activiteit
