from django.core.management.base import BaseCommand
from core.models import Skill

class Command(BaseCommand):
    help = 'Seeds the database with specialized AI screening tasks'

    def handle(self, *args, **kwargs):
        skills = [
            "LLM evaluation", "RLHF", "AI QA", "coding evaluation", 
            "hallucination detection", "agent reliability testing", 
            "computer vision annotation", "segmentation", "data labeling", 
            "multimodal evaluation", "speech evaluation", "synthetic data QA", 
            "model benchmarking", "edge-case discovery", "safety evaluation"
        ]
        
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {skill_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skill already exists: {skill_name}'))
