from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})
