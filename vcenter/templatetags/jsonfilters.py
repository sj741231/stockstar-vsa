# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django.core.serializers import serialize
from django.db.models.query import QuerySet
import simplejson
from django.template import Library


register = Library()

@register.filter('jsonify')
def jsonify(object):
    if isinstance(object,QuerySet):
        return serialize('json',object)
    try:
        object = simplejson.loads(object)
        return object
    except:
        pass
    # return simplejson.loads(object)


@register.filter('json_to_kv')
def json_to_kv(object):
    try:
        object = simplejson.loads(object)
        return object.items()
    except:
        return object