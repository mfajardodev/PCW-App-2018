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
from .models import *

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
            if User.objects.all().filter(email=form.cleaned_data['email']).exists() and not User.objects.get(email=form.cleaned_data['email']).is_active:
                user = User.objects.get(email=form.cleaned_data['email'])
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password1'])
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
    else:
        form = SignUpForm()
        for field in form:
            print(field)
    return render(request, 'account/signup.html', {'form': form})

@login_required(login_url='/')
def home(request):
    if (request.user.is_staff):
        return render(request, 'data.html')
    else: 
        events = list(Events.objects.all())
        for event in events:
            print(event.lat)
        # print(list(events))
        return render(request, 'maps.html', {Events: events})

@staff_required(login_url='/')
def data(request):
    akdp = Profile.objects.get(Organization = "alpha Kappa Delta Phi")
    akdp_in = list(akdp.filter(hostee=1).filter(signed_in=1))
    akdp_out = list(akdp.filter(hostee=1).filter(signed_in=0))

    bsu = Profile.objects.get(Organization = "Black Student Union")
    bsu_in = list(bsu.filter(hostee=1).filter(signed_in=1))
    bsu_out = list(bsu.filter(hostee=1).filter(signed_in=0))

    cdt = Profile.objects.get(Organization = "Chi Delta Theta")
    cdt_in = list(cdt.filter(hostee=1).filter(signed_in=1))
    cdt_out = list(cdt.filter(hostee=1).filter(signed_in=0))

    ccf = Profile.objects.get(Organization = "Chinese Christian Fellowship")
    ccf_in = list(akdp.filter(hostee=1).filter(signed_in=1))
    ccf_out = list(akdp.filter(hostee=1).filter(signed_in=0))

    ccc = Profile.objects.get(Organization = "Chinese Cultural Club")
    ccc_in = list(ccc.filter(hostee=1).filter(signed_in=1))
    ccc_out = list(ccc.filter(hostee=1).filter(signed_in=0))

    csa = Profile.objects.get(Organization = "Chinese Student Association")
    csa_in = list(csa.filter(hostee=1).filter(signed_in=1))
    csa_out = list(csa.filter(hostee=1).filter(signed_in=0))

    gza = Profile.objects.get(Organization = "Gamma Zeta Alpha")
    gza_in = list(gza.filter(hostee=1).filter(signed_in=1))
    gza_out = list(gza.filter(hostee=1).filter(signed_in=0))

    hhcc = Profile.objects.get(Organization = "Hip Hop Choreo Club")
    hhcc_in = list(hhcc.filter(hostee=1).filter(signed_in=1))
    hhcc_out = list(hhcc.filter(hostee=1).filter(signed_in=0))

    hsba = Profile.objects.get(Organization = "Hispanic Business Student Association")
    hsba_in = list(hsba.filter(hostee=1).filter(signed_in=1))
    hsba_out = list(hsba.filter(hostee=1).filter(signed_in=0))

    imagen = Profile.objects.get(Organization = "Imagen Y Espiritu Ballet Folklorico")
    imagen_in = list(imagen.filter(hostee=1).filter(signed_in=1))
    imagen_out = list(imagen.filter(hostee=1).filter(signed_in=0))

    jsa = Profile.objects.get(Organization = "Japanese Student Association")
    jsa_in = list(jsa.filter(hostee=1).filter(signed_in=1))
    jsa_out = list(jsa.filter(hostee=1).filter(signed_in=0))

    kasa = Profile.objects.get(Organization = "Korean American Student Association")
    kasa_in = list(kasa.filter(hostee=1).filter(signed_in=1))
    kasa_out = list(kasa.filter(hostee=1).filter(signed_in=0))

    lpe = Profile.objects.get(Organization = "Lambda Phi Epsilon")
    lpe_in = list(lpe.filter(hostee=1).filter(signed_in=1))
    lpe_out = list(lpe.filter(hostee=1).filter(signed_in=0))

    lsg = Profile.objects.get(Organization = "Lambda Sigma Gamma")
    lsg_in = list(lsg.filter(hostee=1).filter(signed_in=1))
    lsg_out = list(lsg.filter(hostee=1).filter(signed_in=0))

    ltn = Profile.objects.get(Organization = "Lambda Theta Nu")
    ltn_in = list(akdp.filter(hostee=1).filter(signed_in=1))
    ltn_out = list(akdp.filter(hostee=1).filter(signed_in=0))

    lia = Profile.objects.get(Organization = "Latinos in Agriculture")
    lia_in = list(lia.filter(hostee=1).filter(signed_in=1))
    lia_out = list(lia.filter(hostee=1).filter(signed_in=0))

    mexa = Profile.objects.get(Organization = "Movimiento Estudiantil Xicano de Azatlan")
    mexa_in = list(mexa.filter(hostee=1).filter(signed_in=1))
    mexa_out = list(mexa.filter(hostee=1).filter(signed_in=0))

    nsbe = Profile.objects.get(Organization = "National Society of Black Engineers")
    nsbe_in = list(nsbe.filter(hostee=1).filter(signed_in=1))
    nsbe_out = list(nsbe.filter(hostee=1).filter(signed_in=0))

    nak = Profile.objects.get(Organization = "Nu Alpha Kappa")
    nak_in = list(nak.filter(hostee=1).filter(signed_in=1))
    nak_out = list(nak.filter(hostee=1).filter(signed_in=0))

    oxd = Profile.objects.get(Organization = "Omega Xi Delta")
    oxd_in = list(oxd.filter(hostee=1).filter(signed_in=1))
    oxd_out = list(oxd.filter(hostee=1).filter(signed_in=0))

    pce = Profile.objects.get(Organization = "Pilipino Cultural Exchange")
    pce_in = list(pce.filter(hostee=1).filter(signed_in=1))
    pce_out = list(pce.filter(hostee=1).filter(signed_in=0))

    qtpc = Profile.objects.get(Organization = "Queer and Trans People of Color")
    qtpc_in = list(qtpc.filter(hostee=1).filter(signed_in=1))
    qtpc_out = list(qtpc.filter(hostee=1).filter(signed_in=0))

    son = Profile.objects.get(Organization = "Sigma Omega Nu")
    son_in = list(son.filter(hostee=1).filter(signed_in=1))
    son_out = list(son.filter(hostee=1).filter(signed_in=0))

    slo = Profile.objects.get(Organization = "SLO Breakers")
    slo_in = list(slo.filter(hostee=1).filter(signed_in=1))
    slo_out = list(slo.filter(hostee=1).filter(signed_in=0))

    shpe = Profile.objects.get(Organization = "Society of Hispanic Professional Engineers")
    shpe_in = list(shpe.filter(hostee=1).filter(signed_in=1))
    shpe_out = list(shpe.filter(hostee=1).filter(signed_in=0))

    tvsa = Profile.objects.get(Organization = "Thai Vietnamese Student Association")
    tvsa_in = list(tvsa.filter(hostee=1).filter(signed_in=1))
    tvsa_out = list(tvsa.filter(hostee=1).filter(signed_in=0))

    return render(request, 'data.html', {
        "akdp_in" : akdp_in,
        "akdp_out" : akdp_out,
        "bsu_in" : bsu_in,
        "bsu_out" : bsu_out,
        "cdt_in" : cdt_in,
        "cdt_out" : cdt_out,
        "ccf_in" : ccf_in,
        "ccf_out" : ccf_out,
        "ccc_in" : ccc_in,
        "ccc_out" : ccc_out,
        "csa_in" : csa_in,
        "csa_in" : csa_in,
        "gza_in" : gza_in,
        "gza_out" : gza_out,
        "hhcc_in" : hhcc_in,
        "hhcc_out" : hhcc_out,
        "hsba_in" : hsba_in,
        "hsba_out" : hsba_out,
        "imagen_in" : imagen_in,
        "imagen_out" : imagen_out,
        "jsa_in" : jsa_in,
        "jsa_out" : jsa_out,
        "kasa_in" : kasa_in,
        "kasa_out" : kasa_out,
        "lpe_in" : lpe_in,
        "lpe_out" : lpe_out,
        "lsg_in" : lsg_in,
        "lsg_out" : lsg_out,
        "ltn_in" : ltn_in,
        "ltn_out" : ltn_out,
        "lia_in" : lia_in,
        "lia_out" : lia_out,
        "mexa_in" : mexa_in,
        "mexa_out" : mexa_out,
        "nsbe_in" : nsbe_in,
        "nsbe_out" : nsbe_out,
        "nak_out" : nak_out,
        "nak_in" : nak_in,
        "oxd_in" : oxd_in,
        "oxd_out" : oxd_out,
        "pce_in" : pce_in,
        "pce_out" : pce_out,
        "qtpc_in" : qtpc_in,
        "qtpc_out" : qtpc_out,
        "son_in" : son_in,
        "son_out" : son_out,
        "slo_in" : slo_in,
        "slo_out" : slo_out,
        "shpe_in" : shpe_in,
        "shpe_out" : shpe_out,
        "tvsa_in" : tvsa_in,
        "tvsa_out" : tvsa_out,

        })

@login_required(login_url='/')
def maps(request):
    events = Events.objects.all()
    print(events)
    return render(request, 'maps.html', {Events: events})

@login_required(login_url='/')
def pamphlet(request):
    return render(request, 'pamphlet.html', {"range": range(31), "range2": range(1,32) })

@login_required(login_url='/')
def schedule(request):
    return render(request, 'schedule.html')

@login_required(login_url='/')
def profile(request):
    return render(request, 'profileview.html')


def account_activation_sent(request):
    return render(request, 'account/account_activation_sent.html')
