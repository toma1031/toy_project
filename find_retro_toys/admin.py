from django.contrib import admin
from .models import Message, MessageRoom, Post, ConditionTag, Like

class ConditionTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'condition_tag']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']

class MessageRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'inquiry_user', 'post_id', 'post_user', 'post']

# obj.post.userのようにすることで、外部キーで参照しているAuthorモデルのフィールドにアクセスできます
    def post_id(self, obj):
        return obj.post.id

    def post_user(self, obj):
        return obj.post.user

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_user', 'message_room_id', 'message']

    def message_room_id(self, obj):
        return obj.message_room.id

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'timestamp']

    def like_id(self, obj):
        return obj.id

admin.site.register(Post, PostAdmin)
admin.site.register(MessageRoom, MessageRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ConditionTag, ConditionTagAdmin)
admin.site.register(Like, LikeAdmin)