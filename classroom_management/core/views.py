from django.shortcuts import render, redirect
from .models import Assignment, Submission, Resource, Notification,Teacher,AssignmentSubmission,StudentProgress
from .forms import AssignmentForm, SubmissionForm, ResourceForm ,AssignmentSubmissionForm,GradeFeedbackForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Student, Notification
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm 
from django.shortcuts import render
from .decorators import teacher_required, student_required
from django.contrib.auth.views import LoginView,LogoutView
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')
            user.save()  # Save the User object

            # Check if a profile already exists before creating one
            if user_type == 'teacher':
                Teacher.objects.get_or_create(user=user)
            elif user_type == 'student':
                Student.objects.get_or_create(user=user)

            # Log in the user and redirect to the appropriate dashboard
            login(request, user)
            if user_type == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if hasattr(user, 'teacher'):
                    return redirect('teacher_dashboard')
                elif hasattr(user, 'student'):
                    return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        if hasattr(self.request.user, 'teacher'):  # Check if the user has a teacher profile
            return reverse('teacher_dashboard')
        elif hasattr(self.request.user, 'student'):  # Check if the user has a student profile
            return reverse('student_dashboard')
        else:
            return reverse('login')  # Fallback in case the user has no profile
        

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)   
        
@login_required
@teacher_required
def teacher_dashboard(request):
    return render(request, 'core/teacher_dashboard.html')

@login_required
@student_required
def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')

@login_required
def manage_assignments(request):
    # Retrieve the Teacher profile if it exists
    try:
        teacher_profile = request.user.teacher
    except Teacher.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    # Fetch assignments for the teacher
    assignments = Assignment.objects.filter(teacher=teacher_profile)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher_profile  # Assign the teacher profile
            assignment.save()
            return redirect('manage_assignments')
    else:
        form = AssignmentForm()

    return render(request, 'core/manage_assignments.html', {'form': form, 'assignments': assignments})

@login_required
@teacher_required  # Restrict access to teachers only
def manage_submissions(request, assignment_id):
    # Fetch the assignment by ID and confirm it's associated with the logged-in teacher
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user.teacher)
    
    # Retrieve all submissions for this specific assignment
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    
    return render(request, 'core/manage_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
    })
    
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Update StudentProgress
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()

            # Update or create progress entry
            progress, created = StudentProgress.objects.update_or_create(
                student=request.user,
                assignment=assignment,
                defaults={
                    'is_submitted': True,
                    'submission_date': timezone.now()
                }
            )
            return redirect('student_dashboard')  # Redirect to dashboard after submission
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'core/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
    })
    
@login_required
@teacher_required  # Ensure only teachers can access
def track_student_progress(request):
    # Retrieve all StudentProgress entries with related student and assignment data
    progress = StudentProgress.objects.all().select_related('student', 'assignment')

    if request.method == 'POST':
        # Retrieve the specific StudentProgress entry
        progress_id = request.POST.get("progress_id")
        progress_entry = get_object_or_404(StudentProgress, id=progress_id)
        
        # Initialize form with the specific StudentProgress instance
        form = GradeFeedbackForm(request.POST, instance=progress_entry)

        # Save only if fields are still editable
        if form.is_valid() and progress_entry.grade is None and not progress_entry.feedback:
            form.save()  # Save the form data to update grade and feedback
            return redirect('track_student_progress')  # Refresh page after saving

    # Display all progress entries along with a fresh form for rendering fields
    return render(request, 'core/track_student_progress.html', {
        'progress': progress,
    })
    
@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("You do not have permission to view this page.")
    
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    return render(request, 'core/view_submissions.html', {'assignment': assignment, 'submissions': submissions})

@login_required
def add_resources(request):
    # Ensure the logged-in user is a teacher
    try:
        teacher_profile = request.user.teacher
    except Teacher.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher = teacher_profile  # Associate the resource with the teacher
            resource.save()
            return redirect('teacher_dashboard')
    else:
        form = ResourceForm()
    
    return render(request, 'core/add_resources.html', {'form': form})

@login_required
def view_resources(request):
    resources = Resource.objects.all()  # Retrieve all resources
    return render(request, 'core/view_resources.html', {'resources': resources})

@login_required
def notify_students(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    students = User.objects.filter(groups__name='Students')  # Assuming students are in a 'Students' group

    for student in students:
        Notification.objects.create(
            recipient=student,
            sender=request.user,  # The teacher sending the notification
            message=f"New update on assignment '{assignment.title}' by {request.user.username}."
        )

    return redirect('teacher_dashboard')

@login_required
def assignment_page(request):
    assignments = Assignment.objects.all()
    return render(request, 'core/assignment_page.html', {'assignments': assignments})

@login_required
def notification_page(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'core/notification_page.html', {'notifications': notifications})

@login_required
def list_assignments(request):
    assignments = Assignment.objects.all()  # Get all assignments
    return render(request, 'core/list_assignments.html', {'assignments': assignments})