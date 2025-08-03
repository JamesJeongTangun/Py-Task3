from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Memo
from .forms import MemoForm


class MemoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_memo_creation(self):
        """메모 생성 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용입니다.',
            author=self.user
        )
        self.assertEqual(memo.title, '테스트 메모')
        self.assertEqual(memo.content, '테스트 내용입니다.')
        self.assertEqual(memo.author, self.user)
        self.assertTrue(memo.created_at)
        self.assertTrue(memo.updated_at)
    
    def test_memo_str_representation(self):
        """메모 문자열 표현 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용입니다.',
            author=self.user
        )
        self.assertEqual(str(memo), '테스트 메모')
    
    def test_memo_ordering(self):
        """메모 정렬 테스트 (최신순)"""
        from django.utils import timezone
        import datetime
        
        # 시간 차이를 두고 생성
        now = timezone.now()
        memo1 = Memo.objects.create(
            title='첫 번째 메모',
            content='첫 번째 내용',
            author=self.user
        )
        memo1.created_at = now - datetime.timedelta(minutes=1)
        memo1.save()
        
        memo2 = Memo.objects.create(
            title='두 번째 메모',
            content='두 번째 내용',
            author=self.user
        )
        memo2.created_at = now
        memo2.save()
        
        memos = Memo.objects.all()
        self.assertEqual(memos[0], memo2)  # 최신 메모가 첫 번째
        self.assertEqual(memos[1], memo1)
    
    def test_memo_absolute_url(self):
        """메모 절대 URL 테스트"""
        memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용입니다.',
            author=self.user
        )
        expected_url = reverse('memos:detail', kwargs={'pk': memo.pk})
        self.assertEqual(memo.get_absolute_url(), expected_url)


class MemoFormTest(TestCase):
    def test_memo_form_valid_data(self):
        """유효한 데이터로 메모 폼 테스트"""
        form = MemoForm(data={
            'title': '테스트 메모',
            'content': '테스트 내용입니다.'
        })
        self.assertTrue(form.is_valid())
    
    def test_memo_form_no_data(self):
        """데이터 없이 메모 폼 테스트"""
        form = MemoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)


class MemoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.memo = Memo.objects.create(
            title='테스트 메모',
            content='테스트 내용입니다.',
            author=self.user
        )
    
    def test_memo_list_view_requires_login(self):
        """메모 목록 뷰 로그인 필요 테스트"""
        response = self.client.get(reverse('memos:list'))
        self.assertEqual(response.status_code, 302)  # 리다이렉트
    
    def test_memo_list_view_authenticated(self):
        """인증된 사용자의 메모 목록 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memos:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
    
    def test_memo_detail_view(self):
        """메모 상세 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memos:detail', kwargs={'pk': self.memo.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.memo.title)
        self.assertContains(response, self.memo.content)
    
    def test_memo_create_view_get(self):
        """메모 작성 뷰 GET 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memos:create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '새 메모 작성')
    
    def test_memo_create_view_post(self):
        """메모 작성 뷰 POST 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('memos:create'), {
            'title': '새 테스트 메모',
            'content': '새 테스트 내용입니다.'
        })
        self.assertEqual(response.status_code, 302)  # 성공 후 리다이렉트
        self.assertTrue(Memo.objects.filter(title='새 테스트 메모').exists())
    
    def test_memo_update_view(self):
        """메모 수정 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('memos:edit', kwargs={'pk': self.memo.pk}), {
            'title': '수정된 제목',
            'content': '수정된 내용'
        })
        self.assertEqual(response.status_code, 302)
        self.memo.refresh_from_db()
        self.assertEqual(self.memo.title, '수정된 제목')
        self.assertEqual(self.memo.content, '수정된 내용')
    
    def test_memo_delete_view(self):
        """메모 삭제 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('memos:delete', kwargs={'pk': self.memo.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Memo.objects.filter(pk=self.memo.pk).exists())
    
    def test_memo_search(self):
        """메모 검색 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memos:list') + '?search=테스트')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
    
    def test_user_can_only_see_own_memos(self):
        """사용자는 자신의 메모만 볼 수 있는지 테스트"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_memo = Memo.objects.create(
            title='다른 사용자 메모',
            content='다른 사용자 내용',
            author=other_user
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memos:list'))
        self.assertContains(response, '테스트 메모')
        self.assertNotContains(response, '다른 사용자 메모')
