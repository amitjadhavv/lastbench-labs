from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile, ScreeningSession
from .ai_utils import get_screening_agent_response
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
import json

def home(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        if profile.screening_status in ['PENDING', 'SCREENING']:
            # Find the latest active session or create a new one
            session = profile.sessions.filter(is_active=True).first()
            if session:
                return redirect('screening_chat', session_id=session.id)
            else:
                return redirect('start_screening')
    return render(request, 'home.html')

class StaffLoginView(LoginView):
    template_name = 'core/staff_login.html'
    
    def get_success_url(self):
        return '/dashboard/'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile_setup(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('start_screening')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'core/profile_setup.html', {'form': form})

@login_required
def start_screening(request):
    profile = request.user.profile
    # Create a new session
    session = ScreeningSession.objects.create(profile=profile)
    return redirect('screening_chat', session_id=session.id)

@login_required
def screening_chat(request, session_id):
    session = ScreeningSession.objects.get(id=session_id, profile=request.user.profile)
    profile = request.user.profile
    skills = [s.name for s in profile.skills.all()]
    
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            # Add user message to history
            session.chat_history.append({"role": "user", "parts": [user_message]})
            
            # Get AI response
            ai_response_text = get_screening_agent_response(session.chat_history, skills)
            
            # Add AI message to history
            session.chat_history.append({"role": "model", "parts": [ai_response_text]})
            
            # Check if evaluation is in response
            if "[EVALUATION]" in ai_response_text:
                session.is_active = False
                session.completed_at = timezone.now()
                profile.screening_status = 'COMPLETED'
                profile.ai_screening_report = ai_response_text
                profile.save()
                # Log out the candidate so their session is cleared
                logout(request)
            
            session.save()
            
    return render(request, 'core/screening.html', {
        'session': session,
        'chat_history': session.chat_history
    })

@staff_member_required(login_url='staff_login')
def admin_dashboard(request):
    evaluators = Profile.objects.filter(user__is_staff=False).order_by('-created_at')
    staff_members = Profile.objects.filter(user__is_staff=True).order_by('-created_at')
    return render(request, 'core/admin_dashboard.html', {
        'evaluators': evaluators,
        'staff_members': staff_members
    })

@staff_member_required(login_url='staff_login')
def candidate_detail(request, profile_id):
    candidate = get_object_or_404(Profile, id=profile_id)
    latest_session = candidate.sessions.order_by('-started_at').first()
    return render(request, 'core/candidate_detail.html', {
        'candidate': candidate,
        'session': latest_session
    })
