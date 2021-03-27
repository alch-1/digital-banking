from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
import requests, json


# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "login.html", {"form": form, "msg" : msg})



def signup_view(request):
    msg = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # tBank API here
            tbank_authen = False
            OTP = '999999'
            PIN = raw_password
            serviceName = 'loginCustomer'
            userID = username
            headerObj = {
                       'Header': {
                       'serviceName': serviceName,
                       'userID': userID,
                       'PIN': PIN,
                       'OTP': OTP
                                }
                       }
            final_url="{0}?Header={1}".format("http://tbankonline.com/SMUtBank_API/Gateway",json.dumps(headerObj))
            response = requests.post(final_url)
            serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
            errorCode = serviceRespHeader['GlobalErrorID']
            print(errorCode)
            if errorCode == '010000':
                LoginOTPAuthenticateResponseObj = response.json()['Content']['ServiceResponse']['Login_OTP_Authenticate-Response']
                print('CustomerID: {}'.format(LoginOTPAuthenticateResponseObj['CustomerID']))
                print('BankID: {}'.format(LoginOTPAuthenticateResponseObj['BankID']))
                tbank_authen = True
            elif errorCode == '010041':
                msg = "OTP has expired.\nYou will receiving a SMS"
            else:
                msg = serviceRespHeader['ErrorText']
            
            if tbank_authen:
                user = authenticate(username=username, password=raw_password)
                login(request, user)

                return redirect('/')

            else:
                msg = "Invalid tbank credentials"
        else:
            print("invalid code")
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, "msg": msg})

def homepage_view(request):
    return render(request,'index.html')
