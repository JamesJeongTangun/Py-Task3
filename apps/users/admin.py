from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Django 기본 User 모델 사용
# 필요시 추가 설정 가능

# 사용자 관리 페이지 커스터마이징 예시
# class CustomUserAdmin(UserAdmin):
#     list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
#     list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
#     search_fields = ['username', 'first_name', 'last_name', 'email']

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
