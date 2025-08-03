#!/usr/bin/env python
import os
import sys
import django

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memojjang.settings')
django.setup()

from apps.memos.forms import MemoForm

form = MemoForm()
print('Priority field choices:')
for value, label in form.fields['priority'].choices:
    print(f'  {value}: {label}')
print(f'Priority initial value: {form.fields["priority"].initial}')
