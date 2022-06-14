from calendar import month_name
import datetime

from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.filter
def int_to_month_name(month_number):
    datetime_object = datetime.datetime.strptime(month_number, "%m")
    full_month_name = datetime_object.strftime("%B")
    return full_month_name


@register.filter
def str_to_month_name(month_number):
    return month_name[month_number]
