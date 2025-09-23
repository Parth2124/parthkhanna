# admin.py
from django.contrib import admin
from .models import HeroSection, Project, Service, Experience, SocialMedia,ContactMessage,Subscriber

admin.site.register(HeroSection)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Experience)
admin.site.register(SocialMedia)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)
