from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Assignment, Submission, Resource
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from .models import Teacher, Student,StudentProgress
from .models import AssignmentSubmission


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        input_formats=['%d/%m/%Y', '%Y-%m-%d']  # Accept '27/10/2024' or '2024-10-27'
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_file']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file', 'description']
        
        

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']
        
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submission_file', 'comments']  # Include the comments field
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add any comments for the teacher...'}),
        }
class GradeFeedbackForm(forms.ModelForm):
    class Meta:
        model = StudentProgress
        fields = ['grade', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide feedback...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make grade and feedback read-only if they are already set
        if self.instance.grade is not None and self.instance.feedback:
            self.fields['grade'].widget.attrs['readonly'] = True
            self.fields['feedback'].widget.attrs['readonly'] = True
