from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Memo


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
        memo1 = Memo.objects.create(
            title='첫 번째 메모',
            content='첫 번째 내용',
            author=self.user
        )
        memo2 = Memo.objects.create(
            title='두 번째 메모',
            content='두 번째 내용',
            author=self.user
        )
        
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
