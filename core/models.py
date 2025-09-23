# models.py
from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hero_images/')
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(help_text="Enter skills separated by commas")

    def __str__(self):
        return self.title
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    front_content = models.TextField()
    back_content = models.TextField()
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome class e.g., 'fas fa-laptop-code'")
    price = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.title

class SocialMedia(models.Model):
    platform = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    image = models.ImageField(upload_to='social_images/', null=True, blank=True)

    def __str__(self):
        return self.platform


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    purpose = models.CharField(max_length=100)
    specific = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Project, Service, Subscriber

@receiver(post_save, sender=Project)
def notify_new_project(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscriber.objects.all()
        for sub in subscribers:
            subject = f"New Project: {instance.title}"
            html_content = render_to_string('emails/new_project_notify.html', {'project': instance})
            email_msg = EmailMultiAlternatives(subject, "", "parthkhannaa@gmail.com", [sub.email])
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

@receiver(post_save, sender=Service)
def notify_new_service(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscriber.objects.all()
        for sub in subscribers:
            subject = f"New Service: {instance.title}"
            html_content = render_to_string('emails/new_service_notify.html', {'service': instance})
            email_msg = EmailMultiAlternatives(subject, "", "parthkhannaa@gmail.com", [sub.email])
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()
