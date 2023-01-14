from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from . models import Post, Category

# Create your views here.

# def index(request):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )

class PostList(ListView):
    model = Post
    # template_name = 'blog/index.html'
    ordering = '-pk'


    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        # 카테고리 전체
        context['categories'] = Category.objects.all()
        # 카테고리 미정의 포스트 개수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post,
#         }
#     )

# FBV 형태
def category_page(request, slug):
    category = Category.objects.get(slug=slug)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': Post.objects.filter(category=category),
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category':category,
        }
    )