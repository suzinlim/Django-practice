from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import PostBaseForm, PostCreateForm, PostDetailForm
from .models import Post

def index(request):
    post_list = Post.objects.all().order_by('-created_at') # Post 전체 데이터 조회
    context = {
        'post_list': post_list,
    }
    return render(request, 'index.html', context)

def post_list_view(request):
    # post_list = Post.objects.all() # Post 전체 데이터 조회
    post_list = Post.objects.filter(writer = request.user) # Post.writer가 현재 로그인인 것 조회
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail_view(request, id):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return redirect('index')
    else:
        return redirect('/accounts/login')
    context = {
        'post': post,
        'form': PostDetailForm(),
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html')
    else:
        image = request.FILES.get('image')
        content = request.POST.get('content')
        print(image)
        print(content)
        Post.objects.create(
           image = image,
           content = content,
           writer = request.user
        )
        return redirect('index')
    
@login_required
def post_create_form_view(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {'form': form}
        return render(request, 'posts/post_form2.html', context)
    else:
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid(): # 폼 유효성 검사
            Post.objects.create(
                image = form.cleaned_data['image'],
                content = form.cleaned_data['content'],
                writer = request.user,
            )
        else:
            return redirect('posts:post-create')
        return redirect('index')
        #Post.objects.create(
        #    image = image,
        #    content = content,
        #    writer = request.user
        #)

@login_required
def post_update_view(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id, writer=request.user)

    if request.method == 'GET':
        context = { 'post': post }
        return render(request, 'posts/post_form.html', context)
    elif request.method == 'POST':
        new_image = request.FILES.get('image')
        content = request.POST.get('content')
        print(new_image)
        print(content)
        if new_image:
            post.image.delete()
            post.image = new_image
        
        post.content = content
        post.save()
        return redirect('posts:post-detail', post.id)
    
@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    # post = get_object_or_404(Post, id=id, writer=request.user)
    if request.user != post.writer:
        raise Http404('잘못된 접근입니다.')
    
    if request.method == 'GET':
        context = { 'post': post }
        return render(request, 'posts/post_confirm_delete.html', context)
    else:
        post.delete()
        return redirect('index')
    




# Create your views here.
def url_view(request):
    print('url_view()')
    data = {'code': '001', 'msg':'OK'}
    return HttpResponse('<h1>url_view</h1>')
    # return JsonResponse(data)

def url_parameter_view(request, username):
    print(username)
    print(request.GET)
    print(f'request.GET: {request.GET}')
    return HttpResponse(username)

def function_view(request):
    print(f'request.method: {request.method}')

    if request.method == 'GET':
        print(f'request.GET: {request.GET}')
    elif request.method == 'POST':
        print(f'request.POST: {request.POST}')
    return render(request, 'view.html')

class class_view(ListView):
    model = Post
    ordering = ['-id']
    # template_name = 'cbv_view.html'

# 함수 기반 뷰
def function_list_view(request):
    object_list = Post.objects.all().order_by('-id')
    return render(request, 'cbv_view.html', {'object_list': object_list})