// 메모짱 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 페이지 애니메이션
    document.body.classList.add('fade-in');
    
    // 알림 메시지 자동 숨김
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && !alert.classList.contains('d-none')) {
                const bsAlert = new bootstrap.Alert(alert);
                if (bsAlert) {
                    bsAlert.close();
                }
            }
        }, 5000); // 5초 후 자동 숨김
    });
    
    // 확인 대화상자
    const deleteButtons = document.querySelectorAll('.btn-delete, [href*="delete"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = button.dataset.confirm || '정말로 삭제하시겠습니까?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // 폼 제출 시 버튼 비활성화 (중복 제출 방지)
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 처리 중...';
                
                // 3초 후 버튼 복원 (네트워크 오류 대비)
                setTimeout(function() {
                    if (submitBtn.disabled) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }
                }, 3000);
            }
        });
    });
    
    // 검색 폼 개선
    const searchForm = document.querySelector('form input[name="search"]');
    if (searchForm) {
        let searchTimeout;
        searchForm.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            // 실시간 검색 힌트 (추후 AJAX 구현 가능)
            if (query.length > 2) {
                searchTimeout = setTimeout(function() {
                    // console.log('검색 쿼리:', query);
                }, 500);
            }
        });
    }
    
    // 텍스트 애니메이션
    const animatedElements = document.querySelectorAll('.card, .alert');
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.transition = 'all 0.3s ease-out';
                
                setTimeout(function() {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(function(el) {
        observer.observe(el);
    });
    
    // 키보드 단축키
    document.addEventListener('keydown', function(e) {
        // Ctrl + / : 검색 폼 포커스
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Ctrl + N : 새 메모 작성 (메모 목록 페이지에서)
        if (e.ctrlKey && e.key === 'n' && window.location.pathname.includes('/memos/')) {
            e.preventDefault();
            const createLink = document.querySelector('a[href*="create"]');
            if (createLink) {
                window.location.href = createLink.href;
            }
        }
        
        // ESC : 모달 닫기, 검색 초기화
        if (e.key === 'Escape') {
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput && searchInput === document.activeElement) {
                searchInput.blur();
                if (searchInput.value) {
                    searchInput.value = '';
                }
            }
        }
    });
    
    // 툴팁 초기화
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 로컬 스토리지 활용 (검색 기록 등)
    const searchHistory = JSON.parse(localStorage.getItem('memoSearchHistory') || '[]');
    
    // 검색 기록 저장
    if (searchForm) {
        searchForm.closest('form').addEventListener('submit', function() {
            const query = searchForm.value.trim();
            if (query && !searchHistory.includes(query)) {
                searchHistory.unshift(query);
                searchHistory.splice(10); // 최대 10개만 보관
                localStorage.setItem('memoSearchHistory', JSON.stringify(searchHistory));
            }
        });
    }
});

// 유틸리티 함수들
const MemoUtils = {
    // 토스트 메시지 표시
    showToast: function(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || this.createToastContainer();
        const toast = this.createToast(message, type);
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    },
    
    createToastContainer: function() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    },
    
    createToast: function(message, type) {
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-' + type + ' border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        return toast;
    },
    
    // 확인 대화상자
    confirmDelete: function(message = '정말로 삭제하시겠습니까?') {
        return confirm(message + '\n\n삭제된 항목은 복구할 수 없습니다.');
    },
    
    // 문자열 유틸리티
    truncateText: function(text, length = 100) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    },
    
    // 날짜 포맷팅
    formatDate: function(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        
        if (days === 0) return '오늘';
        if (days === 1) return '어제';
        if (days < 7) return days + '일 전';
        
        return date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
};

// 전역 객체로 노출
window.MemoUtils = MemoUtils;

// 페이지 성능 모니터링
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData && perfData.loadEventEnd - perfData.loadEventStart > 3000) {
                console.warn('페이지 로딩이 느립니다:', perfData.loadEventEnd - perfData.loadEventStart + 'ms');
            }
        }, 0);
    });
    
    // 메모 카드 스타일링
    const memoCards = document.querySelectorAll('.memo-card');
    memoCards.forEach(function(card, index) {
        // 시차 애니메이션
        card.style.animationDelay = (index * 0.1) + 's';
        
        // 호버 효과 강화
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}
