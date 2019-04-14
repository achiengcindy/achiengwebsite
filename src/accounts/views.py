from django.conf import settings
from django.contrib.auth import get_user_model,login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage

from .forms import RegistrationForm , ProfileEditForm, UserEditForm
from .tokens import account_activation_token
from .models import Profile

User= get_user_model()


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False
            # Save the User object
            user.save()
            # Create the user profile
            #profile = Profile.objects.create(user=user)
            #send one time activation email
            current_site = get_current_site(request)
            subject = 'Confirm your Account'
            sender = 'mail@achiengcindy.com'
            message = render_to_string('accounts/account_activation_email.html', {
                'user':  user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes( user.pk)).decode(),
                'token':account_activation_token.make_token( user),
            })
            print( message)
            # https://stackoverflow.com/questions/40655802/how-to-implement-email-user-method-in-custom-user-model
            # email = EmailMessage(subject, message,sender, [user.email])
            # print(email)
            # email.send()
            user.email_user(subject=subject, message=message)
            return redirect('account_activation_sent')  

    else:
        user_form = RegistrationForm()
    return render(request, 'accounts/register.html',{'user_form': user_form})

def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token, backend='accounts.authentication.EmailAuthBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, 'accounts.authentication.EmailAuthBackend')
        return redirect('login')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token, backend='accounts.authentication.EmailAuthBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, 'accounts.authentication.EmailAuthBackend')
        return redirect('login')
    else:
        return render(request, 'accounts/account_activation_invalid.html')



@login_required
def accounts_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('/')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {'user_form': user_form,'profile_form': profile_form})
   
# @login_required
# def order_detail(request):
#     orders = Order.objects.filter(customer=request.user)
#     return render(request,"orders/order/history.html", {'orders':orders})


