from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserCreateForm, SignUpForm

# from users.models import User 
# 사용자 계정이 있는지 확인

# Create your views here.
def signup_view(request):
    # GET 요청 시 HTML 응답
    if request.method == 'GET':
        form = SignUpForm
        context = {'form':form}
        return render(request, 'accounts/signup.html', context)
    else:
        # POST 요청 시 데이터 확인 후 회원 생성
        form = SignUpForm(request.POST)

        if form.is_valid():
            # 회원가입 처리
            instance = form.save()
            return redirect('index')
        else:
            # 리다이렉트
            return redirect('accounts:signup')
        
def login_view(request):
    # GET, POST 분리
    if request.method == 'GET':
        # 로그인 HTML 응답
        return render(request, 'accounts/login.html', {'form':AuthenticationForm()})
    else:
        # 데이터 유효성 검사
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 비즈니스 로직 처리 - 로그인 처리
            login(request, form.user_cache) # 비즈니스 로직 처리
            return redirect('index')
        else:
            # 비즈니스 로직 처리 - 로그인 실패
            # 응답
            return render(request, 'accounts/login.html', {'form':form}) # 출력
        
        # username = request.POST.get('username')
        # if username == '' or username == None:
        #     pass
        # user = User.objects.get(usernmae = username)
        # if user == None:
        #     pass
        # password = request.GET.get('password')

def logout_view(request):
    # 데이터 유효성 검사
    # 로그인일 때
    if request.user.is_authenticated:
        logout(request)
    # 비즈니스 로직 처리 - 로그아웃
    # 응답
    return redirect('index')