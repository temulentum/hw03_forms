from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from pytz import timezone
from .models import Post, Group, User
from .forms import PostForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def index(request):
    # post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    # post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    post_list = Post.objects.filter(group=group)
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
        'text': slug,
        'group': group,
    }
    return render(request, template, context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    # posts_of_user = get_list_or_404(Post, author = username)
    user = get_object_or_404(User, username=username)
    posts_of_user = Post.objects.filter(author=user)
    paginator = Paginator(posts_of_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, id=post_id)
    # post = Post.objects.get(id=post_id)
    number_of_posts = Post.objects.count()

    context = {
        'post': post,
        'number_of_posts': number_of_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = Post()
            new_post.author = request.user
            new_post.text = form.cleaned_data['text']
            new_post.group = form.cleaned_data['group']
            new_post.pub_date = datetime.now()
            new_post.save()
            username = request.user.username
            # return HttpResponse(username)
            return redirect('posts:profile', username=username)

    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
        if post.author.id == request.user.id:
            context = {'form': form,
                       'is_edit': True,
                       'post_id': post_id}
            return render(request, 'posts/create_post.html', context)
        else:
            # return post_detail(request, post_id)
            return redirect('posts:post_detail', post_id=post_id)

    elif request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        # if post.author.id == request.user.id:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Post.objects.filter(id=post_id).update(text =
            # form.cleaned_data['text'], group = form.cleaned_data['form'],
            #  pub_date = datetime.now())
            post = form.save(commit=False)
            post.author = request.user
            # post.text = form.cleaned_data['text']
            # post.group = form.cleaned_data['group']
            post.pub_date = timezone.now()  # datetime.now()
            # post.username = request.user.username
            # post.pk = None
            # post._state.adding = False
            post.save()
            # return HttpResponse('asfasdasdasd')
            return redirect('posts:post_detail', post_id=post.pk)
            # return post_detail(request, post_id)
    # return render(request, 'posts/create_post.html', context)
    # return HttpResponse(post.author.id)
