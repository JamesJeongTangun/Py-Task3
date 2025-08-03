from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# 임시 뷰들 (Phase 4에서 완전히 구현예정)

@login_required
def memo_list(request):
    return HttpResponse("메모 목록 페이지 (Phase 4에서 구현 예정)")

@login_required
def memo_create(request):
    return HttpResponse("메모 작성 페이지 (Phase 4에서 구현 예정)")

@login_required
def memo_detail(request, pk):
    return HttpResponse(f"메모 상세 페이지 (ID: {pk}) (Phase 4에서 구현 예정)")

@login_required
def memo_edit(request, pk):
    return HttpResponse(f"메모 수정 페이지 (ID: {pk}) (Phase 4에서 구현 예정)")

@login_required
def memo_delete(request, pk):
    return HttpResponse(f"메모 삭제 페이지 (ID: {pk}) (Phase 4에서 구현 예정)")
