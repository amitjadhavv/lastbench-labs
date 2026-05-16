from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Registration'),
        ('SCREENING', 'In AI Screening'),
        ('COMPLETED', 'Screening Completed'),
        ('VERIFIED', 'Verified Expert'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)
    
    # Portfolio Links
    portfolio_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    
    # Screening Info
    screening_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ai_screening_score = models.FloatField(null=True, blank=True)
    ai_screening_report = models.TextField(blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ScreeningSession(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sessions')
    chat_history = models.JSONField(default=list) # Stores the list of messages
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session for {self.profile.user.username} at {self.started_at}"

# Signals to automatically create profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
