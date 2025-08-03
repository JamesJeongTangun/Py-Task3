from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Memo


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'priority_display', 'is_pinned', 'word_count', 'created_at', 'updated_at']
    list_filter = ['priority', 'is_pinned', 'created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'word_count', 'character_count']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-is_pinned', '-updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'author', 'content')
        }),
        ('설정', {
            'fields': ('priority', 'is_pinned'),
            'classes': ('collapse',)
        }),
        ('통계', {
            'fields': ('word_count', 'character_count'),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_pinned', 'make_unpinned', 'set_high_priority', 'set_normal_priority']
    
    def priority_display(self, obj):
        """중요도를 아이콘과 함께 표시"""
        priority_colors = {
            'low': '#28a745',
            'normal': '#6c757d',
            'high': '#ffc107',
            'urgent': '#dc3545'
        }
        color = priority_colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;"><i class="{}"></i> {}</span>',
            color,
            obj.priority_icon,
            obj.get_priority_display()
        )
    priority_display.short_description = '중요도'
    priority_display.admin_order_field = 'priority'
    
    def word_count(self, obj):
        """단어 수 계산"""
        return len(obj.content.split())
    word_count.short_description = '단어 수'
    
    def character_count(self, obj):
        """글자 수 계산"""
        return len(obj.content)
    character_count.short_description = '글자 수'
    
    # 관리자 액션들
    def make_pinned(self, request, queryset):
        """선택된 메모들을 상단에 고정"""
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'{updated}개의 메모가 상단에 고정되었습니다.')
    make_pinned.short_description = "선택된 메모를 상단에 고정"
    
    def make_unpinned(self, request, queryset):
        """선택된 메모들의 고정을 해제"""
        updated = queryset.update(is_pinned=False)
        self.message_user(request, f'{updated}개의 메모 고정이 해제되었습니다.')
    make_unpinned.short_description = "선택된 메모의 고정 해제"
    
    def set_high_priority(self, request, queryset):
        """선택된 메모들을 높은 우선순위로 설정"""
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated}개의 메모가 높은 우선순위로 설정되었습니다.')
    set_high_priority.short_description = "높은 우선순위로 설정"
    
    def set_normal_priority(self, request, queryset):
        """선택된 메모들을 보통 우선순위로 설정"""
        updated = queryset.update(priority='normal')
        self.message_user(request, f'{updated}개의 메모가 보통 우선순위로 설정되었습니다.')
    set_normal_priority.short_description = "보통 우선순위로 설정"
