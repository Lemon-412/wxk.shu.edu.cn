from django.shortcuts import render
from .models import CalculatorTable, StudentTable, TeacherTable, ClassTable, ScoreTable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'home.html')


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


def get_user_info(request):
    ret = {}
    result = StudentTable.objects.filter(xh=request.user.username)
    if result.exists():
        ret = {'xh': result[0].xh, 'xm': result[0].xm, 'yydj': result[0].yydj}
        return 'student', ret
    result = TeacherTable.objects.filter(gh=request.user.username)
    if result.exists():
        ret = {'gh': result[0].gh, 'xm': result[0].xm, 'xl': result[0].xl}
        return 'teacher', ret
    return 'admin', ret


@login_required
def index(request):  # 主页
    status, context = get_user_info(request)
    if status == 'student':
        return render(request, "index.html", context=context)
    return HttpResponseRedirect("/")


@login_required
def logout_view(request):  # 安全退出
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def xk(request):  # 学生选课
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':  # 首次访问
        result = ScoreTable.objects.filter(xq='2019-2020学年冬季学期', xh=request.user.username)
        classtable = []
        for kc in result:
            classtable.append(
                {
                    'kh': kc.kh.kh, 'gh': kc.gh.gh, 'xm': kc.gh.xm,
                    'km': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].km,
                    'sksj': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].sksj,
                }
            )
        context['classtable'] = classtable
        return render(request, 'xk.html', context=context)
    elif request.method == 'POST':  # 填表选课
        for i in range(1, 5):
            kh = context['kh' + str(i)] = request.POST['kh' + str(i)]
            gh = context['gh' + str(i)] = request.POST['gh' + str(i)]
            if len(kh) and len(gh):
                result = ClassTable.objects.filter(xq='2019-2020学年冬季学期', kh=kh, gh=gh)
                if not result.exists():
                    context['result' + str(i)] = '选课失败：不存在该课程'
                    continue
                result = ScoreTable.objects.filter(
                    xh=request.user.username,
                    xq='2019-2020学年冬季学期',
                    kh=ClassTable.objects.filter(xq='2019-2020学年冬季学期', kh=kh)[0]
                )
                if result.exists():
                    context['result' + str(i)] = '选课失败：已选同类型课程'
                    continue
                item = ScoreTable(
                    xq='2019-2020学年冬季学期',
                    gh=TeacherTable.objects.filter(gh=gh)[0],
                    kh=ClassTable.objects.filter(xq='2019-2020学年冬季学期', kh=kh)[0],
                    xh=StudentTable.objects.filter(xh=request.user.username)[0]
                )
                item.save()
                context['result' + str(i)] = '选课成功'
            elif len(kh) or len(gh):
                context['result' + str(i)] = '选课失败：课程号或工号未填写完整'
            result = ScoreTable.objects.filter(xq='2019-2020学年冬季学期', xh=request.user.username)
            classtable = []
            for kc in result:
                classtable.append(
                    {
                        'kh': kc.kh.kh, 'gh': kc.gh.gh, 'xm': kc.gh.xm,
                        'km': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].km,
                        'sksj': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].sksj,
                    }
                )
            context['classtable'] = classtable
        return render(request, 'xk.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def tk(request):  # 学生退课
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        result = ScoreTable.objects.filter(xq='2019-2020学年冬季学期', xh=request.user.username)
        classtable = []
        for kc in result:
            classtable.append(
                {
                    'kh': kc.kh.kh, 'gh': kc.gh.gh, 'xm': kc.gh.xm,
                    'km': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].km,
                    'sksj': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].sksj,
                }
            )
        context['classtable'] = classtable
        return render(request, 'tk.html', context=context)
    elif request.method == 'POST':
        kh = request.POST['kh']
        gh = request.POST['gh']
        if len(kh) and len(gh):
            result = ScoreTable.objects.filter(xh=request.user.username, xq='2019-2020学年冬季学期',
                                               kh=ClassTable.objects.filter(xq='2019-2020学年冬季学期', kh=kh)[0],
                                               gh=TeacherTable.objects.filter(gh=gh)[0]
                                               )
            if not result.exists():
                context['result'] = '退课失败：未选此门课程'
            else:
                result.delete()
                context['result'] = '退课成功'
        elif len(kh) or len(gh):
            context['result'] = '退课失败：课程号或工号未填写完整'
        result = ScoreTable.objects.filter(xq='2019-2020学年冬季学期', xh=request.user.username)
        classtable = []
        for kc in result:
            classtable.append(
                {
                    'kh': kc.kh.kh, 'gh': kc.gh.gh, 'xm': kc.gh.xm,
                    'km': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].km,
                    'sksj': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].sksj,
                }
            )
        context['classtable'] = classtable
        return render(request, 'tk.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def kbcx(request):  # 学生课表查询
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    result = ScoreTable.objects.filter(xh=request.user.username, xq='2019-2020学年冬季学期')
    classtable = []
    for kc in result:
        classtable.append(
            {
                'kh': kc.kh.kh, 'gh': kc.gh.gh, 'xm': kc.gh.xm, 'pscj': kc.pscj, 'kscj': kc.kscj, 'zpcj': kc.zpcj,
                'km': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].km,
                'sksj': ClassTable.objects.filter(kh=kc.kh.kh, gh=kc.gh.gh, xq='2019-2020学年冬季学期')[0].sksj,
            }
        )
    context['classtable'] = classtable
    return render(request, 'kbcx.html', context=context)


@login_required
def kccx(request):  # 学生课程查询
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        return render(request, 'kccx.html', context=context)
    elif request.method == 'POST':
        result = ClassTable.objects.all()
        context['xq'] = request.POST['xq']
        if context['xq']:
            result = result.filter(xq__contains=context['xq'])
        context['kh'] = request.POST['kh']
        if context['kh']:
            result = result.filter(kh__startswith=context['kh'])
        context['km'] = request.POST['km']
        if context['km']:
            result = result.filter(km__contains=context['km'])
        context['gh'] = request.POST['gh']
        if context['gh']:
            result = result.filter(gh=context['gh'])
        context['jsmc'] = request.POST['jsmc']
        if context['jsmc']:
            result = result.filter(gh__in=TeacherTable.objects.filter(xm__contains=context['jsmc']))
        context['sksj'] = request.POST['sksj']
        if context['sksj']:
            result = result.filter(sksj__contains=context['sksj'])
        classtable = []
        for kc in result:
            classtable.append(
                {'kh': kc.kh, 'km': kc.km, 'gh': kc.gh.gh, 'jsmc': kc.gh.xm, 'sksj': kc.sksj, 'xq': kc.xq}
            )
        context['classtable'] = classtable
        return render(request, 'kccx.html', context=context)
    return HttpResponseRedirect("/")
