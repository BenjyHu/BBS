from django.contrib import admin
from blog import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.BlogTheme)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.UpDown)
admin.site.register(models.ArticleToTag)
admin.site.register(models.Comment)
