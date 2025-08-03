from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Memo(models.Model):
    PRIORITY_CHOICES = [
        ('low', '낮음'),
        ('normal', '보통'),
        ('high', '높음'),
        ('urgent', '긴급'),
    ]
    
    title = models.CharField('제목', max_length=200)
    content = models.TextField('내용')
    priority = models.CharField(
        '중요도',
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='normal'
    )
    is_pinned = models.BooleanField('상단 고정', default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = '메모'
        verbose_name_plural = '메모들'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('memos:detail', kwargs={'pk': self.pk})
    
    @property
    def priority_icon(self):
        icons = {
            'low': 'fas fa-arrow-down text-success',
            'normal': 'fas fa-minus text-secondary', 
            'high': 'fas fa-arrow-up text-warning',
            'urgent': 'fas fa-exclamation text-danger'
        }
        return icons.get(self.priority, 'fas fa-minus text-secondary')
    
    @property
    def priority_badge_class(self):
        classes = {
            'low': 'bg-success',
            'normal': 'bg-secondary',
            'high': 'bg-warning text-dark',
            'urgent': 'bg-danger'
        }
        return classes.get(self.priority, 'bg-secondary')
