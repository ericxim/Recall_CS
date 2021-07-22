from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Community)
admin.site.register(CommunityMember)
admin.site.register(Question)
admin.site.register(QuestionResponse)
admin.site.register(Comment)
admin.site.register(User)
