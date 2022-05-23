from django.contrib import admin
from .models import Music, Easy, Normal, Hard, Expert, Master, Account#, Person
# Register your models here.

admin.site.register(Account)
#admin.site.register(Music)
#admin.site.register(Author)
#admin.site.register(Easy)
#admin.site.register(Normal)
#admin.site.register(Hard)
#admin.site.register(Expert)
#admin.site.register(Master)

class MusicInline(admin.TabularInline):
    model = Music

@admin.register(Easy)
class EasyAdmin(admin.ModelAdmin):
    inlines = [MusicInline]

    class meta:
        orders = ['Difficulty']
@admin.register(Normal)
class NormalAdmin(admin.ModelAdmin):
    inlines = [MusicInline]
@admin.register(Hard)
class HardAdmin(admin.ModelAdmin):
    inlines = [MusicInline]
@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    inlines = [MusicInline]
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = [MusicInline]

class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'easy', 'normal', 'hard', 'expert', 'master')
    list_filter = ('easy', 'normal', 'hard', 'expert', 'master')
#    fields = ['title', ('easy', 'normal', 'hard', 'expert', 'master')]
    fieldsets = (
        (None, {'fields': ('title','num')}),
        ('Difficulty', {'fields': ('easy', 'normal', 'hard', 'expert', 'master')}),
        ('Availbality', {'fields': ('lover',)})
        )
#    inlines = [MusicInstanceInline]
admin.site.register(Music, MusicAdmin)
'''
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user','music_names')
    fieldsets = ((None, {'fields' : ('user','musics',)}),)
'''