from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserModelTest(TestCase):
    def test_user_creation(self):
        """사용자 생성 테스트"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_superuser_creation(self):
        """슈퍼유저 생성 테스트"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_user_str_representation(self):
        """사용자 문자열 표현 테스트"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view(self):
        """로그인 페이지 접근 테스트"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '로그인')
    
    def test_login_functionality(self):
        """로그인 기능 테스트"""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # 로그인 후 메모 목록으로 리다이렉트되는지 확인
        self.assertRedirects(response, reverse('memos:list'))
    
    def test_logout_confirmation_page(self):
        """로그아웃 확인 페이지 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '로그아웃 하시겠습니까?')
        self.assertContains(response, 'testuser')
    
    def test_logout_functionality(self):
        """로그아웃 기능 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # POST 요청으로 로그아웃
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # 로그아웃 후 다시 로그인 페이지 접근 가능한지 확인
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_quick_logout(self):
        """빠른 로그아웃 기능 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('users:quick_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
    
    def test_logout_without_login(self):
        """로그인하지 않은 상태에서 로그아웃 접근 테스트"""
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
    
    def test_register_view(self):
        """회원가입 페이지 접근 테스트"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '회원가입')
