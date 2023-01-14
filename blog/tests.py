from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
# 테스트는 새로운 데이터베이스에서 실행됨
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_test0 = User.objects.create_user(username='user_test0', password='somepassword')
        self.user_test1 = User.objects.create_user(username='user_test1', password='somepassword')
        self.category_test0 = Category.objects.create(name='CategoryTest0', slug='category_test_0')
        self.category_test1 = Category.objects.create(name='CategoryTest1', slug='category_test_1')
        
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_test0,
            author=self.user_test0,
        )

        self.post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_test1,
            author=self.user_test1,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트 입니다.',
            content='category가 없는 경우',
            author=self.user_test1,
        )

    # 카테고리 페이지 테스트
    def category_page_test(self):
        response = self.client.get(self.category_test0.get_absolute_url())
        # 정상적으로 불러옴 (cf. 404면 실패)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_test0.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        # 카테고리명이 포함되고
        self.assertIn(self.category_test0.name, main_area.text)
        # 타이틀도 포함되어 있고
        self.assertIn(self.post_001.title, main_area.text)

        # 다른 포스트는 포함되면 실패
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    # 카테고리 카드 테스트
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_test0} ({self.category_test0.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_test1} ({self.category_test1.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류', categories_card.text)

    # 네비게이션바 테스트
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('yspkm.dev', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='yspkm.dev')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')


    # 포트스 리스트 페이지 테스트
    def test_post_list(self):
        # 포스트가 있는 상태(초기 3개)
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 계시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

        self.assertIn(self.user_test0.username.upper(), main_area.text)
        self.assertIn(self.user_test1.username.upper(), main_area.text)

        # 포스트 삭제한 후
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)


    # 포스트 상세 페이지 테스트
    def test_post_detail(self):
        # 1.1 포스트
        # 1.2 첫 포스트의 url은 '/blog/1'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번재 post url로 접근하면 정상적으로 작동한다. (status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        self.navbar_test(soup)
        # 카테고리 테스트
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트ㅡ이 제목(title)이 웹 브라우저 탭 타이틀에 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_test0.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_test0.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
