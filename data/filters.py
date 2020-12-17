import django_filters
from django_filters import CharFilter
from .models import *

class AlumniFilter(django_filters.FilterSet):
	first = CharFilter(field_name = 'first_name', lookup_expr = 'icontains')
	last = CharFilter(field_name = 'last_name', lookup_expr = 'icontains')
	email = CharFilter(field_name = 'email', lookup_expr = 'icontains')
	class Meta:
		model = User
		fields = ['first_name','last_name', 'email'] 
		exclude = ['first_name', 'last_name']