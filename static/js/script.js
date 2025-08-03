// 메모짱 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 알림 메시지 자동 숨김
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5초 후 자동 숨김
    });
    
    // 확인 대화상자
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('정말로 삭제하시겠습니까?')) {
                e.preventDefault();
            }
        });
    });
    
    // 폼 제출 시 버튼 비활성화 (중복 제출 방지)
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 처리 중...';
            }
        });
    });
});

// 유틸리티 함수들
function showToast(message, type = 'info') {
    // Bootstrap Toast 기능 (추후 구현)
    console.log(`${type}: ${message}`);
}

function confirmDelete(message = '정말로 삭제하시겠습니까?') {
    return confirm(message);
}
