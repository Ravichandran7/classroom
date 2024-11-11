from django.contrib import admin
from .models import Teacher, Student  # Import models you need in the admin

admin.site.register(Teacher)
admin.site.register(Student)
