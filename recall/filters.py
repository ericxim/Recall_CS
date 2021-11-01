import django_filters
from django_filters import CharFilter
from .models import *

class QuestionResponseFilter(django_filters.FilterSet):
    title = CharFilter(field_name='question__title', lookup_expr='icontains', label='Title' )
    
    class Meta:
        model = QuestionResponse
        fields = ['is_complete']

class QuestionFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Title' )
    
    class Meta:
        model = Question
        fields = ['title']