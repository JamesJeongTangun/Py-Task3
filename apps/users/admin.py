from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count
from apps.memos.models import Memo


# Django 기본 User 모델 확장
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'memo_count', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']
    
    def get_queryset(self, request):
        """메모 수를 포함한 쿼리셋 반환"""
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            memo_count=Count('memo', distinct=True)
        )
        return queryset
    
    def memo_count(self, obj):
        """사용자의 메모 수 표시"""
        count = getattr(obj, 'memo_count', 0)
        if count > 0:
            return format_html(
                '<a href="/admin/memos/memo/?author__id__exact={}" style="color: #007cba;">{} 개</a>',
                obj.pk,
                count
            )
        return '0 개'
    memo_count.short_description = '메모 수'
    memo_count.admin_order_field = 'memo_count'

# 기존 User admin 등록 해제 후 새로운 것으로 등록
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 관리자 사이트 제목 커스터마이징
admin.site.site_header = "메모짱 관리자"
admin.site.site_title = "메모짱 Admin"
admin.site.index_title = "메모짱 관리 대시보드"
