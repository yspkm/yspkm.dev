from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    # 카테고리명은 유일하게
    name = models.CharField(max_length=50, unique=True)
    # allow_unicode: 한글 사용 URL
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        # 이렇게 안하면 admin 페이지에서 Categorys라고 뜸
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)  # blakc=True이므로 필수는 아님
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 다대다 관게
    # null=True는 디폴트로 설정되어 있음
    tags = models.ManyToManyField(Tag, blank=True)

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

    def get_content_markdown(self):
        return markdown(self.content)
