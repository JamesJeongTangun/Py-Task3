from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Memo
from .forms import MemoForm


class MemoListView(LoginRequiredMixin, ListView):
    model = Memo
    template_name = 'memos/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Memo.objects.filter(author=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MemoDetailView(LoginRequiredMixin, DetailView):
    model = Memo
    template_name = 'memos/memo_detail.html'
    context_object_name = 'memo'
    
    def get_queryset(self):
        return Memo.objects.filter(author=self.request.user)


class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memos/memo_form.html'
    success_url = reverse_lazy('memos:list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '메모가 성공적으로 작성되었습니다.')
        return super().form_valid(form)


class MemoUpdateView(LoginRequiredMixin, UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memos/memo_form.html'
    
    def get_queryset(self):
        return Memo.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '메모가 성공적으로 수정되었습니다.')
        return super().form_valid(form)


class MemoDeleteView(LoginRequiredMixin, DeleteView):
    model = Memo
    template_name = 'memos/memo_confirm_delete.html'
    success_url = reverse_lazy('memos:list')
    context_object_name = 'memo'
    
    def get_queryset(self):
        return Memo.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '메모가 성공적으로 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)


# 함수형 뷰들 (클래스형 뷰와 동일한 기능)
memo_list = MemoListView.as_view()
memo_detail = MemoDetailView.as_view()
memo_create = MemoCreateView.as_view()
memo_edit = MemoUpdateView.as_view()
memo_delete = MemoDeleteView.as_view()


# AJAX 검색 뷰
@login_required
@require_GET
def memo_search_ajax(request):
    """AJAX 메모 검색 API"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'results': [], 'count': 0})
    
    # 사용자의 메모만 검색
    memos = Memo.objects.filter(
        author=request.user
    ).filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).order_by('-updated_at')[:10]  # 최대 10개 결과
    
    results = []
    for memo in memos:
        results.append({
            'id': memo.pk,
            'title': memo.title,
            'content': memo.content[:100] + '...' if len(memo.content) > 100 else memo.content,
            'created_at': memo.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': memo.updated_at.strftime('%Y-%m-%d %H:%M'),
            'url': memo.get_absolute_url(),
        })
    
    return JsonResponse({
        'results': results,
        'count': len(results),
        'query': query
    })


# 메모 통계 뷰
@login_required
def memo_stats(request):
    """사용자 메모 통계"""
    user_memos = Memo.objects.filter(author=request.user)
    
    # 기본 통계
    total_count = user_memos.count()
    total_words = sum(len(memo.content.split()) for memo in user_memos)
    
    # 최근 활동
    recent_memos = user_memos.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()
    
    # 월별 통계 (최근 6개월)
    monthly_stats = []
    for i in range(6):
        date = timezone.now() - timezone.timedelta(days=30*i)
        month_count = user_memos.filter(
            created_at__year=date.year,
            created_at__month=date.month
        ).count()
        monthly_stats.append({
            'month': date.strftime('%Y-%m'),
            'count': month_count
        })
    
    import json
    context = {
        'total_count': total_count,
        'total_words': total_words,
        'recent_count': recent_memos,
        'monthly_stats': monthly_stats[::-1],  # 오래된 순으로 정렬
        'monthly_stats_json': json.dumps(monthly_stats[::-1]),
        'avg_words_per_memo': total_words // total_count if total_count > 0 else 0,
    }
    
    return render(request, 'memos/memo_stats.html', context)
