from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

import re

from .models import Employer, Freelancer, Project


# Create your views here.
def index(request):
    username = request.session.get('current_user')
    error_message = request.session.get('error_message')
    # messages = request.session.get('messages')
    role = request.session.get('role')
    email = request.session.get('email')

    try:
        del request.session['error_message']
        del request.session['messages']
    except Exception:
        print('Nincsenek ilyen session változók!')

    return render(request, 'Freelancers/index.html', {
        'current_user': username,
        'error_message': error_message,
        # 'messages': messages,
        'role': role,
        'email': email
    })


def projects(request):
    all_projects = Project.objects.all()
    # text = ""
    # for item in all_projects:
    #     text += str(item)
    #     text += "\n"

    # return HttpResponse("The projects are:\n" + text)
    return render(request, 'Freelancers/all_projects.html', {'projects': all_projects})


def freelancer_list(request):
    all_freelancers = Freelancer.objects.all()

    return render(request, 'Freelancers/freelancer_list.html', {'freelancer_list': all_freelancers})


def employer_list(request):
    all_employers = Employer.objects.all()

    return render(request, 'Freelancers/employer_list.html', {'employer_list': all_employers})


# A freelancer és az employer is ugyanazon a formon lép be.
def login(request):
    # TODO Login functionality
    login_user = None
    user_id = None

    email = str(request.POST['email']).strip()
    password = re.escape(str(request.POST['password']).strip())

    try:
        login_user = Freelancer.objects.get(email=email, password=password)
    except Exception:
        # request.session['error_message'] = 'Nincs ilyen felhasználó!'
        pass

    if not login_user:
        try:
            login_user = Employer.objects.get(email=email, password=password)
        except:
            request.session['error_message'] = 'Nincs ilyen felhasználó!'

    if login_user:
        request.session['current_user'] = login_user.fullname
        request.session['email'] = login_user.email

        if isinstance(login_user, Freelancer):
            request.session['role'] = 'freelancer'
        else:
            request.session['role'] = 'employer'

    # print('user:', login_user)

    return HttpResponseRedirect(reverse('freelancers:index'), request)


def register_freelancer(request):
    # TODO Escaping for register
    message_list = list()

    fullname = str(request.POST['fullname']).strip()
    email = str(request.POST['email']).strip()
    password = str(request.POST['password']).strip()
    password2 = str(request.POST['password2']).strip()
    skills = str(request.POST['skills']).strip()

    if Freelancer.objects.filter(email=email):
        message_list.append('Ez az email cím már foglalt!')

    if not password == password2:
        message_list.append('A két jelszó nem egyezik!')

    if len(message_list) == 0:
        new_freelancer = Freelancer()
        new_freelancer.fullname = fullname
        new_freelancer.email = email
        new_freelancer.password = password
        new_freelancer.skills = skills
        new_freelancer.save()
        message_list.append('Sikeres regisztráció!')

    request.session['messages'] = message_list
    # Fasza, átmegy az üzenet!
    return HttpResponseRedirect(reverse('freelancers:index'))


def register_employer(request):
    # TODO Employer register
    message_list = list()

    fullname = str(request.POST['fullname']).strip()
    email = str(request.POST['email']).strip()
    password = re.escape(str(request.POST['password']).strip())
    password2 = re.escape(str(request.POST['password2']).strip())

    if Employer.objects.filter(email=email):
        message_list.append('Ez az email cím már foglalt!')

    if not password == password2:
        message_list.append('A két jelszó nem egyezik!')

    # Ha nem üres, tehát ha volt hiba.
    if len(message_list) == 0:
        new_employer = Employer()
        new_employer.fullname = fullname
        new_employer.email = email
        new_employer.password = password
        new_employer.save()
        message_list.append('Sikeres regisztráció')

    request.session['messages'] = message_list

    return HttpResponseRedirect(reverse('freelancers:index'))


def emp_projects(request, emp_email):
    owner = get_object_or_404(Employer, email=emp_email)
    all_projects = Project.objects.all().filter(owner=owner)

    return render(request, 'Freelancers/emp_projects.html', {'projects': all_projects})


def fl_projects(request, fl_email):
    return render(request, 'Freelancers/fl_projects.html')


def logout(request):
    try:
        # del request.session['current_user']
        request.session.clear()
    except Exception:
        pass

    return render(request, 'Freelancers/index.html', {'current_user': None})