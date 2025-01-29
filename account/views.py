from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            subject = 'Activate your account'
            context = {
                'user': user, 'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            }
            message = render_to_string('account/registration/email-verification.html', context)
            user.email_user(subject=subject, message=message)
            

            return redirect('email-verification-sent')

    
    return render(request, 'account/registration/register.html', {'form': form})


def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    # SUCCESS
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    # FAILED
    return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)

                return redirect('dashboard')
            
    
    context = {'form': form}
    return render(request, 'account/login.html', context=context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect ('store')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, 'Account Updated successfully')
            return redirect('dashboard')
    

    context = {'user_form': user_form}

    return render(request, 'account/profile-management.html', context)

@login_required(login_url='login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Account deleted successfully')
        return redirect('store')
    
    return render(request, 'account/delete-account.html')


def manage_shipping(request):
    try:
        user_shipment = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        user_shipment = None
    form = ShippingForm(instance=user_shipment)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=user_shipment)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'account/manage-shipping.html', context)