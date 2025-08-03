from django.db import models
from django.contrib.auth.models import User

# Django의 기본 User 모델을 사용
# 필요시 추후 CustomUser로 확장 가능

# User 모델에 추가 필드가 필요한 경우를 위한 예시
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     
#     def __str__(self):
#         return f'{self.user.username}의 프로필'
