from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional teacher-specific fields
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:  # Assuming only staff members are teachers
        Teacher.objects.create(user=instance)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional student-specific fields
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'student'):
        # If you have a flag or condition for student users, add it here
        Student.objects.create(user=instance)

class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming `User` is used for students
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)  # Field for student comments

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"
    
class Resource(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Notification(models.Model):
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

