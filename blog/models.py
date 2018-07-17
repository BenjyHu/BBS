from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

'''
表一：日志样式表（BlogTheme）
字段：
    id
    blog_title
    theme(url)
'''
class BlogTheme(models.Model):
    title = models.CharField(max_length=32, verbose_name='个人博客标题')
    theme = models.CharField(max_length=32, verbose_name='博客主题')
    site_name = models.CharField(max_length=32, verbose_name='站点名称')

    def __str__(self):
        return self.title


'''
表二：用户详细信息表（UserInfo）
字段：
    id
    tel_number
    user(一对一关联User表)
    theme(一对一关联样式表)
'''
class UserInfo(AbstractUser):
    telephone = models.CharField(max_length=11)
    create_time = models.DateTimeField(auto_now_add=True)
    portrait = models.FileField(upload_to='portrait/',default='portrait/default.jpg')
    theme = models.OneToOneField('BlogTheme', on_delete=models.CASCADE, null=True)


'''
表三：文章分类表（Category）
字段：
    id
    种类字段名
    ...
'''
class Category(models.Model):
    title = models.CharField(max_length=32)
    blog = models.ForeignKey('BlogTheme', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


'''
表四：文章标签表（Tag）
字段：
    id
    标签名
'''
class Tag(models.Model):
    tag_name = models.CharField(max_length=32)
    blog = models.ForeignKey('BlogTheme', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name

'''
表五：文章表（Article）
字段：
    id
    title
    content
    category(一对多关联文章分类表)
    tags(多对多关联文章标签表)
'''
class Article(models.Model):
    title = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', through='ArticleToTag')
    author = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ArticleToTag(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    def __str__(self):
        return self.article.title + '--' + self.tag.tag_name

'''
表六：文章点赞/踩数量表（UpDown）
字段：
    id
    user_id(一对多关联用户表)
    article_id(一对多关联文章表)
    is_up(点赞)
    is_down(踩)
'''
class UpDown(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)


'''
表七：评论表（comment）
字段：
    id
    user_id(一对多关联用户表)
    article_id(一对多关联文章表)
    parent_id(父评论的id,可以为空,自关联id)
    comment_time(评论的时间)
    content(评论内容)
'''
class Comment(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=150)
