from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)  # blakc=True이므로 필수는 아님
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        # f-string
        # 문자열을 쉽게 formatting 한다.
        # 1. 변수 치환(e.g. x가 1일 때):
        #  f'x는{x}.' --> 'x는 1'
        # 2. 함수 호출(e.g. tmp가 "abc"일 때):
        #   f'tmp의 길이는{len(tmp)}' --> 'tmp의 길이는 3'
        # 3. 객체 치환(.__str__()호출)
        #   f'{datetime.date.today()}' --> '2023-01-07'
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
