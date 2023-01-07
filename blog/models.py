from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #author: 추후 작성 예정

    def __str__(self):
        # f-string
        # 문자열을 쉽게 formatting 한다. 
        # 1. 변수 치환(e.g. x가 1일 때): 
        #  f'x는{x}.' --> 'x는 1'
        # 2. 함수 호출(e.g. tmp가 "abc"일 때): 
        #   f'tmp의 길이는{len(tmp)}' --> 'tmp의 길이는 3'
        # 3. 객체 치환(.__str__()호출) 
        #   f'{datetime.date.today()}' --> '2023-01-07'
        return f'[{self.pk}] {self.title}'

