from django import forms
from .models import Memo


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'content', 'priority', 'is_pinned']
        labels = {
            'title': '제목',
            'content': '내용',
            'priority': '중요도',
            'is_pinned': '상단 고정',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '메모 제목을 입력하세요',
                'maxlength': 200
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '메모 내용을 입력하세요'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['content'].required = True
        self.fields['priority'].help_text = '메모의 중요도를 설정하세요'
        self.fields['is_pinned'].help_text = '체크하면 메모가 목록 상단에 고정됩니다'
        
        # priority 필드의 초기값 명시적 설정
        if not self.instance.pk:  # 새 메모 생성시에만
            self.fields['priority'].initial = 'normal'
