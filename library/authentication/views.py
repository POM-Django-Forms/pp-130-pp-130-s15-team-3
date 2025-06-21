
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import CustomUserRegistrationForm, ProfileUpdateForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('book:book_list')

def custom_logout(request):
    next_page = request.GET.get('next', None)
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    if next_page:
        return redirect(next_page)
    return redirect('book:book_list')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful! Welcome to the library.')
            return redirect(request.POST.get('next') or 'book:book_list')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('authentication:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    role_display = dict(CustomUser.ROLE_CHOICES).get(request.user.role, 'Unknown')
    return render(request, 'registration/profile.html', {
        'form': form,
        'role_display': role_display
    })