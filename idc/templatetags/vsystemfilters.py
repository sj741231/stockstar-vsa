# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django.core.serializers import serialize
from django.db.models.query import QuerySet
import simplejson
from django.template import Library

register = Library()

def jsonify(object):
    if isinstance(object,QuerySet):
        return serialize('json',QuerySet)
    return simplejson.dumps(object,indent=4)

register.filter('jsonify',jsonify)