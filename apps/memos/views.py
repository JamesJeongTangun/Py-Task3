from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
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
