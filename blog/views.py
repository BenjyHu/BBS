from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import auth
from blog import models
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
import json,os
from BBS.settings import BASE_DIR
from bs4 import BeautifulSoup
from io import BytesIO
from blog.check_code import check_code
# Create your views here.


def code(request):
    img,ran_code = check_code()
    request.session['ran_code'] = ran_code
    s = BytesIO()
    img.save(s,'png')
    return HttpResponse(s.getvalue())


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    dic = {'status': 0}
    code = request.session.get('ran_code')
    if code != request.POST.get('code').upper():

        dic['msg'] = '验证码错误'
        return JsonResponse(dic)

    if request.is_ajax():

        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        print(name,pwd)
        user_obj = auth.authenticate(username=name, password=pwd)
        if user_obj:
            auth.login(request, user_obj)
            dic['status'] = 1
            # return redirect(reverse('index'))
        return JsonResponse(dic)



def register(request):
    pass


def index(request):
    # if request.user.is_authenticated:
    #     return render(request, 'index.html')
    # return redirect(reverse('login'))
    article_list = models.Article.objects.all()
    return render(request, 'index.html', {'article_list':article_list})


def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def my_site(request,name,**kwargs):

    # 查找当前访问的博主对象
    user_obj = models.UserInfo.objects.filter(username=name).first()
    if user_obj:
        # 查找博主的站点标题
        title = user_obj.theme.title
        # 查找当前博主的所有文章
        article_list = models.Article.objects.filter(author=user_obj)

        subName = kwargs.get('subName')
        arg = kwargs.get('arg')

        if subName and arg:
            if subName == 'category':
                article_list = article_list.filter(category__title=arg)
            elif subName == 'tag':
                article_list = article_list.filter(tags__tag_name=arg)
            else:
                year,month = arg.split('/')
                article_list = article_list.filter(create_time__year=year,create_time__month=month)


        # 查找当前访问博主文章的所有分类
        # category_list = models.Category.objects.filter(blog__title=title)
        # 查询当前博主的每一个分类的文章数量
        # category_list = models.Category.objects.filter(blog__title=title).annotate(num=Count('article')).values('title','num')
        # 查询当前博主的每一个标签的文章数量
        # tag_list = models.Tag.objects.filter(blog__title=title).annotate(num=Count('article')).values('tag_name','num')
        # 查询当前博主每个月发表的文章的数量
        # date_article_count = models.Article.objects.filter(author=user_obj).extra(select={"article_date":"strftime('%%Y/%%m',create_time)"}).values('article_date').annotate(num=Count('pk')).values('article_date','num')
        # return render(request, 'my_site.html',
        #               {'article_list':article_list,'name':name,'title':title,'category_list':category_list,'tag_list':tag_list,'date_article_count':date_article_count})
        return render(request, 'my_site.html', {'article_list':article_list,'title':title,'name':name})
    return render(request, 'not_found.html')


def article_info(request,name,article_id):
    user_obj = models.UserInfo.objects.filter(username=name).first()
    title = user_obj.theme.title
    article_obj = models.Article.objects.filter(id=article_id).first()
    if user_obj and article_obj:
        # 获得文章所有的评论
        comment_list = models.Comment.objects.filter(article=article_obj)
        return render(request, 'article_info.html', {'article_obj':article_obj,'name':name,'title':title,'comment_list':comment_list})
    return render(request, 'not_found.html')


def up_down(request):
    if request.is_ajax():
        # 判断点赞人是否为登陆状态
        if request.user.is_authenticated:
            # 获取点赞人是谁
            user_name = request.user.username
            user_obj = models.UserInfo.objects.filter(username=user_name).first()
            # 获取当前文章的id
            article_id = request.POST.get('article_id')
            # 判断其是否已经点过赞或踩过
            is_user = models.UpDown.objects.filter(user=user_obj,article_id=article_id).first()
            if is_user:
                return JsonResponse({'status':0,'handel':is_user.is_up})
            # 判断是否给自己点赞
            elif models.Article.objects.filter(id=article_id,author=user_obj):
                return JsonResponse({'status': 1})

            # 是点赞还是踩
            down_up = json.loads(request.POST.get('is_up'))
            with transaction.atomic():
                # 将点赞记录添加到点赞表中
                models.UpDown.objects.create(user=user_obj, article_id=article_id,is_up=down_up)
                if down_up:
                    # 更新文章表里的点赞数
                    models.Article.objects.filter(id=article_id).update(up_count=F('up_count')+1)
                else:
                    models.Article.objects.filter(id=article_id).update(down_count=F('down_count') + 1)

            return JsonResponse({'status':1})

        return JsonResponse({'status':0})


# 评论功能函数
def comment(request):
    if request.is_ajax():
        user_id = request.user.pk
        pid = request.POST.get('pid')
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        with transaction.atomic():
            comment_obj = models.Comment.objects.create(user_id=user_id,article_id=article_id,parent_id=pid,content=content)
            models.Article.objects.filter(id=article_id).update(comment_count=F('comment_count')+1)
        timer = comment_obj.comment_time.strftime('%Y-%m-%d %X')
        username = comment_obj.user.username
        content = comment_obj.content
        return JsonResponse({'times':timer,'username':username,'content':content})


# 后台管理页面函数
def backend(request):
    if request.user.is_authenticated:
        # 获取用户的所有文章
        article_list = models.Article.objects.filter(author__username=request.user.username)
        return render(request, 'backend/backend.html', {'article_list':article_list})
    return redirect(reverse('login'))


# 添加文章函数
def add_article(request):
    if request.method == 'POST':
        author_obj = request.user
        article_title = request.POST.get('article_title')
        content = request.POST.get('article_content')
        category_id = request.POST.get('category')
        tag_id_list = request.POST.getlist('tag')
        # 对文章内容进行过滤
        soup = BeautifulSoup(content, 'html.parser')
        for i in soup.find_all():
            if i.name in ['script']:
                i.decompose()
        desc = soup.text[:150]
        with transaction.atomic():
            # 在数据库中创建文章
            article_obj = models.Article.objects.create(title=article_title,desc=desc,content=str(soup),category_id=category_id,author=author_obj)
            # 创建标签
            for tag_id in tag_id_list:
                models.ArticleToTag.objects.create(article=article_obj,tag_id=tag_id)
        return redirect(reverse('backend'))
    blog = models.BlogTheme.objects.filter(userinfo__username=request.user.username).first()
    # 获取用户所有分类
    category_list = models.Category.objects.filter(blog=blog)
    # 获取用户所有标签
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request, 'backend/add_article.html', {'category_list':category_list,'tag_list':tag_list})


# 上传图片函数
def upload(request):
    file_obj = request.FILES.get('upload_img')
    file_name = file_obj.name
    file_path = os.path.join(BASE_DIR,'static/upload',file_name)
    with open(file_path,'wb') as f:
        for line in file_obj:
            f.write(line)
    return JsonResponse({'error':0,'url':'/static/upload/'+file_name})


# 删除文章函数
def delete_article(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        # models.Article.objects.filter(id=pk).delete()
        return HttpResponse('OK')


# 编辑文章函数
def edit_article(request,pk):
    article_obj = models.Article.objects.filter(id=pk).first()
    if request.method == 'POST':
        author_obj = request.user
        article_title = request.POST.get('article_title')
        content = request.POST.get('article_content')
        category_id = request.POST.get('category')
        tag_id_list = request.POST.getlist('tag')
        # 对文章内容进行过滤
        soup = BeautifulSoup(content, 'html.parser')
        for i in soup.find_all():
            if i.name in ['script']:
                i.decompose()
        desc = soup.text[:150]
        with transaction.atomic():
            models.Article.objects.filter(id=pk).update(title=article_title, desc=desc, content=str(soup), category_id=category_id,
                                      author=author_obj)
            # 删除文章原有的标签
            models.ArticleToTag.objects.filter(article=article_obj).delete()
            # 重新创建
            for tag_id in tag_id_list:
                models.ArticleToTag.objects.create(article=article_obj,tag_id=tag_id)
        return redirect(reverse('backend'))

    # 获取文章的所有标签
    article_tag_list = models.Tag.objects.filter(articletotag__article=article_obj)
    blog = models.BlogTheme.objects.filter(userinfo__username=request.user.username).first()
    # 获取用户所有分类
    category_list = models.Category.objects.filter(blog=blog)
    # 获取用户所有标签
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request, 'backend/edit_article.html',{'article_tag_list':article_tag_list,'article_obj':article_obj,'category_list':category_list,'tag_list':tag_list})
