from django.shortcuts import render
from myWEB.models import CalculatorTable

# Create your views here.


def index(request):
    return render(request, 'index.html')


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
