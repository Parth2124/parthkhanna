from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import HeroSection, Project, Service, Experience, SocialMedia, ContactMessage, Subscriber

def index(request):
    hero_sections = HeroSection.objects.all()


    # Add a new attribute `skills_list` for each hero
    for hero in hero_sections:
        if hero.skills:  # check it's not empty
            hero.skills_list = [s.strip() for s in hero.skills.split(",")]
        else:
            hero.skills_list = []
    experiences = Experience.objects.all()

      # Prepare experience details as a list
     # Split experience details into a list
    for exp in experiences:
        exp.details_list = exp.details.splitlines() # split by newlines

    projects = Project.objects.all()
    services = Service.objects.all()
    socials = SocialMedia.objects.all()
    for sc in socials:
        sc.details_list = sc.description.splitlines() # split by newlines

    return render(request, 'core/index.html', {
        'hero_sections': hero_sections,
        'projects': projects,
        'services': services,
        'experiences': experiences,
        'socials': socials,
    })






def get_specific_options(request):
    purpose = request.GET.get('purpose')
    options = []

    if purpose == "Project":
        options = [p.title for p in Project.objects.all()]
    elif purpose == "Service":
        options = [s.title for s in Service.objects.all()]
    elif purpose == "Job Offer":
        options = ["Internship", "Full-time"]  # static options

    return JsonResponse({'options': options})

def contact(request):
    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        purpose = request.POST.get('purpose')
        specific = request.POST.get('specific')
        message = request.POST.get('message')

        # Save contact message
        contact_msg = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            purpose=purpose,
            specific=specific,
            message=message
        )

        # Prepare email content
        projects = Project.objects.all()
        services = Service.objects.all()
        whatsapp_link = "https://wa.me/8130112728"  # replace with your WhatsApp number

        subject = "Thanks for connecting with us!"
        html_content = render_to_string('emails/contact_reply.html', {
            'name': name,
            'projects': projects,
            'services': services,
            'whatsapp_link': whatsapp_link
        })

        email_msg = EmailMultiAlternatives(subject, "", "parthkhannaa@gmail.com", [email])
        email_msg.attach_alternative(html_content, "text/html")
        try:
            email_msg.send()
        except Exception as e:
            logger.error(f"Failed to send contact email to {email}: {e}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send email.'})

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def subscribe(request):
    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)
        email = request.POST.get('email')
        subscriber, created = Subscriber.objects.get_or_create(email=email)

        if created:
            # Send welcome email
            subject = "Welcome to Parth's Updates!"
            html_content = render_to_string('emails/welcome_subscribe.html', {'email': email})
            email_msg = EmailMultiAlternatives(subject, "", "parthkhannaa@gmail.com", [email])
            email_msg.attach_alternative(html_content, "text/html")
            try:
                email_msg.send()
            except Exception as e:
                logger.error(f"Failed to send welcome email to {email}: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to send email.'})

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
