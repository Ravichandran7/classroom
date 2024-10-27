
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student  # Import Student model directly here

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'student'):
        Student.objects.create(user=instance)