from django import template

register = template.Library()

@register.filter
def next_page_url(url):
    next_page = url # if has no next this value will get '/account/'
    if next_page != '/account/':
        return next_page.split('next=')[1]
    return 'None'
