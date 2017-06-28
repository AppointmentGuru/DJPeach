from django import template
register = template.Library()

@register.inclusion_tag('copyandpay/payment-form.html', takes_context=True)
def copyandpay(context):
    return context