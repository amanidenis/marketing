from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .models import Account
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            original_username = username
            counter = 1
            while Account.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Registration successful. Please check your email to activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors and try again.')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_items:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        cart_items = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id_list = []
                        for item in cart_items:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id_list.append(item.id)

                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id_list[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_items = CartItem.objects.filter(cart=cart)
                                for item in cart_items:
                                    item.user = user
                                    item.save()
                except Exception as e:
                    print(e)  # Log the exception for debugging
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                url = request.META.get('HTTP_REFERER', None)
                try:
                    if url:
                        query = requests.utils.urlparse(url).query
                        
                        params = dict(x.split('=') for x in query.split('&'))
                        if 'next' in parms:
                            nextPage = params['next']
                            return redirect(nextPage)
                        
                except :
                    return redirect('dashboard')
                    
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('login')
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')
