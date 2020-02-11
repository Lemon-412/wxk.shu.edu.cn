from django.shortcuts import render
from myWEB.models import CalculatorTable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect


def home(request):
    print('用户名:', request.user.username)
    return render(request, 'home.html')


@login_required
def index(request):
    return render(request, "index.html")


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect("/index")
            else:
                context["msg"] = "用户已被锁定，请联系管理员"
                return render(request, "home.html", context=context)
        else:
            context["msg"] = "用户名或密码错误"
            return render(request, "home.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def calculate(request):
    if request.method == 'GET':
        return render(request, 'calculate.html')
    a = request.POST['value_A']
    b = request.POST['value_B']
    c = str(int(a) + int(b))
    CalculatorTable.objects.create(value_A=a, value_B=b, value_C=c)
    return render(request, 'calculate.html', context={'a': a, 'b': b, 'c': c})


def calculate_history(request):
    history = CalculatorTable.objects.all()
    return render(request, 'calculate_history.html', context={'data': history})
