from django.contrib import admin
from .models import Profile, Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'screening_status', 'is_verified', 'ai_screening_score', 'created_at')
    list_filter = ('screening_status', 'is_verified')
    search_fields = ('user__username', 'user__email', 'bio')
    actions = ['verify_profiles']

    def verify_profiles(self, request, queryset):
        queryset.update(is_verified=True, screening_status='VERIFIED')
    verify_profiles.short_description = "Mark selected profiles as Verified"
