from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from posts.models import Post

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
                outbound = EmailMessage(
                    subject=f'[Portfolio Contact] {subject or "New message"} from {name}',
                    body=f'Name: {name}\nEmail: {email}\n\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email],
                )
                outbound.send(fail_silently=False)
                messages.success(request, 'Your message was sent! I\'ll get back to you soon.')
            except Exception:
                messages.error(request, 'Failed to send message. Please try again in a moment.')
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
        f'Feed: {request.scheme}://{request.get_host()}/posts/feed/',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')

def sitemap_xml(request):
    base = f'{request.scheme}://{request.get_host()}'
    static_urls = [
        ('/', '1.0', 'weekly'),
        (reverse('about'), '0.8', 'monthly'),
        (reverse('post_list'), '0.9', 'daily'),
        (reverse('contact'), '0.7', 'monthly'),
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, priority, freq in static_urls:
        xml.append(f'  <url><loc>{base}{loc}</loc><priority>{priority}</priority><changefreq>{freq}</changefreq></url>')

    posts = (
        Post.objects.select_related('status')
        .filter(status__name__iexact='published')
        .order_by('-created_on')
    )
    for post in posts:
        loc = reverse('post_detail', kwargs={'pk': post.pk})
        lastmod = post.created_on.date().isoformat()
        xml.append(
            f'  <url><loc>{base}{loc}</loc><lastmod>{lastmod}</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>'
        )

    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type='application/xml')
