from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('memos:list')


class CustomLogoutView(View):
    """로그아웃 처리"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'users/logout_confirm.html')
        return redirect('home')
    
    def post(self, request):
        username = request.user.username if request.user.is_authenticated else None
        logout(request)
        if username:
            messages.success(request, f'{username}님, 안전하게 로그아웃되었습니다.')
        return redirect('home')


def quick_logout(request):
    """즉시 로그아웃 (확인 없이)"""
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    if username:
        messages.info(request, f'{username}님, 로그아웃되었습니다.')
    return redirect('home')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('memos:list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'{self.object.username}님, 회원가입을 환영합니다!')
        return response


@login_required
def profile_view(request):
    """사용자 프로필 페이지"""
    return render(request, 'users/profile.html', {'user': request.user})
