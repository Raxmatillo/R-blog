from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import Post
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import ProfileUpdateForm, RegisterForm, UserUpdateForm
# Create your views here.

def profile(request, pk):
    user = get_object_or_404(User, id=pk)
    
    posts = Post.objects.filter(author=user)

    count = 0
    print(posts.values('likes'))

    for c in posts.values('likes'):
        if c['likes'] is not None:
            print(
                int(c['likes'])
            )
            count += int(c['likes'])


    likes = count
    stars_count = user.profile.stars.count
    
    

    context = {'user':user, 'posts':posts, 'stars_count':stars_count, 'likes':likes}
    return render(request, 'accounts/profile.html', context)

def startView(request, pk):
    user = get_object_or_404(User, id=pk)
    stars = False
    
    if user.profile.stars.filter(id=request.user.id).exists():
        user.profile.stars.remove(request.user)
    else:
        user.profile.stars.add(request.user)
        start = True
    
    return HttpResponseRedirect(reverse('user-profile', args=[str(pk)]))

@login_required
def profileUpdate(request):
    if request.POST:
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form and profile_form:
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profil tahrirlandi')
            return redirect('user-profile', request.user.profile.pk)
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request, 'accounts/profileUpdate.html', context)


class LoginView(SuccessMessageMixin, LoginView):
    success_url = 'home'
    success_message = 'Assalomu alaykum'
    template_name = 'registration/login.html'

class LogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Siz saytdan mufaqiyatli chiqdiz!"
    template_name = 'registration/logout.html'


class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'