from django.shortcuts import render

TECH_STACK = ['Python', 'Django', 'React', 'TypeScript', 'PostgreSQL',
              'GitHub Actions', 'Jest', 'Node.js', 'Linux CLI', 'REST APIs']

def home(request):
    return render(request, 'pages/home.html', {'tech_stack': TECH_STACK})

def about(request):
    return render(request, 'pages/about.html')
