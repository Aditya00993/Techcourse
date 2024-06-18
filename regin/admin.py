from django.contrib import admin
from.models import *
# Register your models here

class wii_TabularInline(admin.TabularInline):
    model = wii

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements
class Video_TabularInline(admin.TabularInline):
    model = Video    
class Course_admin(admin.ModelAdmin):
    inlines = (wii_TabularInline,Requirements_TabularInline,Video_TabularInline)  


admin.site.register(Categoties),
admin.site.register(Author),
admin.site.register(Course,Course_admin),
admin.site.register(Zara),
admin.site.register(Requirements),
admin.site.register(wii),
admin.site.register(Lesson),
admin.site.register(Langauge),
admin.site.register(Payment),
