from django import template

from customers.models import CustomerPlan

register = template.Library()


@register.assignment_tag
def get_customer_plans():
    return CustomerPlan.objects.all()
