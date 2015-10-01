from django.contrib import admin

# from models import ProfileImage
# from models import Youtube
from models import Article,ExampleModel,Project
from models import Comment

# admin.site.register(ProfileImage)
# admin.site.register(Youtube)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ExampleModel)
admin.site.register(Project)