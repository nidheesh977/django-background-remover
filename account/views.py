from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser, OTP
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm, AccountForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import random
from django.conf import settings

# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("account:dashboard")
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
    def post(self, request):
        print("Post")
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user credentials
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('account:dashboard')  # Redirect to the dashboard or any other desired page
                
            form.add_error(None, 'Invalid email or password')
            print(form)
        
        return render(request, 'account/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('account:login')

class SignupView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("account:dashboard")
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = CustomUser.objects.create(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                email = form.cleaned_data["email"],
                mobile_number = form.cleaned_data["mobile_number"],
            )
            user.set_password(request.POST['password'])
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        return render(request, 'account/signup.html', {'form': form, "values": request.POST})
    
class ForgotPassword(View):
    def get(self, request):
        context = {
            "show_otp": False
        }
        return render(request, "account/forgot_password.html", context = context)

    def post(self, request):
        email = request.POST.get("email")
        otp = request.POST.get("otp")
        password = request.POST.get("password")
        if CustomUser.objects.filter(email = email).exists():
            user = CustomUser.objects.get(email = email)
            if otp:
                if OTP.objects.filter(user__email = email).exists():
                    print(otp)
                    print(OTP.objects.get(user__email = email).otp)
                    if str(OTP.objects.get(user__email = email).otp) == str(otp):
                        user.set_password(password)
                        user.save()
                        OTP.objects.filter(user__email = email).delete()
                        return redirect("account:login")
                    else:
                        message = "Invalid OTP. Try again"
                        show_otp = True
                else:
                    message = "Invalid OTP. Try again"
                    show_otp = True
            else:
                generated_otp = ""
                for i in range(6):
                    random_number = random.randint(0, 9)
                    generated_otp+=str(random_number)
                OTP.objects.filter(user__email = email).delete()
                OTP.objects.create(user = user, otp = generated_otp)
                subject = f'OTP to reset password'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                plaintext = get_template('email_templates/otp.txt')
                htmly     = get_template('email_templates/otp.html')

                d = { 
                    'username': user.first_name,
                    'otp': generated_otp,
                }

                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                message = "OTP have been send to your mail ID"
                show_otp = True
        else:
            message = "Email not registered"
            show_otp = False
        context = {
            "email": email,
            "message": message,
            "show_otp": show_otp
        }
        return render(request, "account/forgot_password.html", context = context)