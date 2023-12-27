from django import template
import math
from django.db.models import Sum
from app.models import *
register = template.Library()

@register.simple_tag
def discount_price(price,discount):
    if discount == 0:
        return price
    p = price - (int(price) * int(discount) / 100)
    return int(p)

@register.simple_tag
def cartSubTotal(price,dis,qty):
    p = price
    if dis == 0:
        p = price
    else:
        p = price - (int(price) * int(dis) / 100)

    return int(qty) * int(p)


@register.simple_tag
def cartTotal(cart):
    total = 0
    for c in cart:
        total += cartSubTotal(c.product.price, c.product.discount, c.quantity)

    return total

