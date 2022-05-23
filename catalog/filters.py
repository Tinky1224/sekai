from re import M
from .models import Music
import django_filters

class MusicFilter(django_filters.FilterSet):

    class Meta:
        model = Music
        fields = ['easy', 'normal', 'hard', 'expert', 'master']
