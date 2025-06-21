
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
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

#PREVIOUS VERSION
#def register_view(request):
#    if request.method == 'POST':
#        email = request.POST.get('email')
#        password1 = request.POST.get('password1')
#        password2 = request.POST.get('password2')
#        first_name = request.POST.get('first_name', '')
#        last_name = request.POST.get('last_name', '')
#        role = request.POST.get('role', '0')  # Default to guest (0)
#        
#        if password1 != password2:
#            messages.error(request, "Passwords don't match.")
#            return redirect('authentication:register')
#            
#        if CustomUser.objects.filter(email=email).exists():
#            messages.error(request, 'Email already exists.')
#            return redirect('authentication:register')
            
        # Create the user
#        user = CustomUser.objects.create_user(
#            email=email,
#            password=password1,
#            first_name=first_name,
#            last_name=last_name,
#            role=int(role)  # Convert to int as our model expects integer for role
#        )
        
        # Log the user in
#        user = authenticate(email=email, password=password1)
#        if user is not None:
#            login(request, user)
#            messages.success(request, 'Registration successful! Welcome to the library.')
#            next_page = request.POST.get('next', None)
#            if next_page:
#                return redirect(next_page)
#            return redirect('book:book_list')
    
    # Get role choices from the model
#    role_choices = [
#        {'value': CustomUser.ROLE_VISITOR, 'label': 'Guest User (Borrow Books)'},
#        {'value': CustomUser.ROLE_LIBRARIAN, 'label': 'Librarian (Manage Library)'}
#    ]
#    return render(request, 'registration/register.html', {'role_choices': role_choices})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the library.')
            return redirect(request.POST.get('next') or 'book:book_list')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

#PREVIOUS VERSION
#@login_required
#def profile(request):
#    if request.method == 'POST':
#        user = request.user
#        first_name = request.POST.get('first_name', '').strip()
#        last_name = request.POST.get('last_name', '').strip()
#        
#        # Update user's name if provided
#        if first_name or last_name:
#            if first_name:
#                user.first_name = first_name
#            if last_name:
#                user.last_name = last_name
#            user.save()
#            messages.success(request, 'Profile updated successfully!')
#            return redirect('authentication:profile')
    
    # Get role display name
#    role_display = dict(CustomUser.ROLE_CHOICES).get(request.user.role, 'Unknown')
    
#    context = {
#        'user': request.user,
#        'role_display': role_display,
#        'is_librarian': request.user.role == CustomUser.ROLE_LIBRARIAN
#    }
#    return render(request, 'registration/profile.html', context)

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