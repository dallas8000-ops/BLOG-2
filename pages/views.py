from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
