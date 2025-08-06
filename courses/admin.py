from django.contrib import admin
from .models import Category, Course, Lesson, UserCourse, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'instructor', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['category', 'instructor']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'instructor', 'price', 'image', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_free', 'duration', 'created_at', 'has_video']
    list_filter = ['course', 'is_free', 'created_at']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']
    autocomplete_fields = ['course']
    readonly_fields = ['created_at', 'video_preview']

    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description', 'order', 'duration', 'is_free')
        }),
        ('Video', {
            'fields': ('video_url', 'video_file', 'video_preview'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def has_video(self, obj):
        return bool(obj.video_file or obj.video_url)
    has_video.boolean = True
    has_video.short_description = "Video mavjud"

    def video_preview(self, obj):
        if obj.video_file:
            return f"<a href='{obj.video_file.url}' target='_blank'>🎬 Video faylni ochish</a>"
        elif obj.video_url:
            return f"<a href='{obj.video_url}' target='_blank'>🌐 Video URL'ni ochish</a>"
        return "Video yo‘q"
    video_preview.allow_tags = True
    video_preview.short_description = "Video ko‘rish"


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'purchased_at']
    list_filter = ['purchased_at']
    search_fields = ['user__username', 'course__title']
    autocomplete_fields = ['user', 'course']
    readonly_fields = ['purchased_at']
    ordering = ['-purchased_at']

    fieldsets = (
        (None, {
            'fields': ('user', 'course')
        }),
        ('Timestamps', {
            'fields': ('purchased_at',),
        }),
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'course__title']
    autocomplete_fields = ['user', 'course']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('user', 'course', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
