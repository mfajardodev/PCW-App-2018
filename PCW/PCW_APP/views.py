from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your PCW APP Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            print(user.email)
            send_mail(subject, message, 'noreply@mail.pcwhousing.com', [user.email], fail_silently=False)
            # user.email_user(subject, message, fail_silently=False)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            return redirect('account_activation_sent')

            # login(request, user)
            # return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required(login_url='/')
def home(request):
    if (request.user.is_staff):
        return render(request, 'data.html')
    else: 
        return render(request, 'maps.html')

@staff_required(login_url='/')
def data(request):
    return render(request, 'data.html')

@login_required(login_url='/')
def maps(request):
    return render(request, 'maps.html')

@login_required(login_url='/')
def pamphlet(request):
    return render(request, 'pamphlet.html')

@login_required(login_url='/')
def schedule(request):
    return render(request, 'schedule.html')


def account_activation_sent(request):
    return render(request, 'account/account_activation_sent.html')