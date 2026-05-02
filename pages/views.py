from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse

TECH_STACK = ['Python', 'Django', 'React', 'TypeScript', 'PostgreSQL',
              'GitHub Actions', 'Jest', 'Node.js', 'Linux CLI', 'REST APIs']

def home(request):
    return render(request, 'pages/home.html', {'tech_stack': TECH_STACK})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            try:
                send_mail(
                    subject=f'[Portfolio Contact] {subject or "New message"} from {name}',
                    message=f'From: {name} <{email}>\n\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message was sent! I\'ll get back to you soon.')
            except Exception:
                messages.error(request, 'Failed to send message. Please email me directly at dallas8000@gmail.com.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        return redirect('contact')
    return render(request, 'pages/contact.html')

def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /accounts/password/',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')

def sitemap_xml(request):
    base = f'{request.scheme}://{request.get_host()}'
    urls = [
        ('/', '1.0', 'weekly'),
        (reverse('about'), '0.8', 'monthly'),
        (reverse('post_list'), '0.9', 'daily'),
        (reverse('contact'), '0.7', 'monthly'),
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, priority, freq in urls:
        xml.append(f'  <url><loc>{base}{loc}</loc><priority>{priority}</priority><changefreq>{freq}</changefreq></url>')
    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type='application/xml')
