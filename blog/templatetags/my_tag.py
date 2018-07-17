from django import template
from blog import models
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('left_bar.html')
def sub_data(username,name):
    # 查找当前访问的博主对象
    user_obj = models.UserInfo.objects.filter(username=name).first()
    # 查找博主的站点标题
    title = user_obj.theme.title
    # 查询当前博主的每一个分类的文章数量
    category_list = models.Category.objects.filter(blog__title=title).annotate(num=Count('article')).values('title',
                                                                                                            'num')
    # 查询当前博主的每一个标签的文章数量
    tag_list = models.Tag.objects.filter(blog__title=title).annotate(num=Count('article')).values('tag_name', 'num')
    # 查询当前博主每个月发表的文章的数量
    date_article_count = models.Article.objects.filter(author=user_obj).extra(
        select={"article_date": "strftime('%%Y/%%m',create_time)"}).values('article_date').annotate(
        num=Count('pk')).values('article_date', 'num')
    return {'name': name, 'title': title, 'category_list': category_list,'username':username,
                   'tag_list': tag_list, 'date_article_count': date_article_count}