from django import template
from gatewaynum import constants

register = template.Library()

@register.filter(name='hasaccess_addremark')
def hasaccess_addremark(access):
    return True if constants.ACCESS.ADDREMARK in access else False
