from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Animals
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
# Create your views here.

class AnimalHome(DataMixin, ListView):
    model = Animals
    template_name = 'animals/index.html'
    context_object_name = 'posts'
#    extra_context = {'title': 'Main Page'}
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Home Page')
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Animals.objects.filter(is_published=True).select_related('cat')
    
class AnimalsCategory(DataMixin,ListView):
    model = Animals
    template_name = 'animals/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Animals.objects.filter(cat__slug=self.kwargs['cat_slug'],is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name), 
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

class ShowPost(DataMixin,DetailView):
    model = Animals
    template_name = 'animals/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class AddPage(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'animals/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Adding article')
        return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'animals/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Contact with us")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'animals/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'animals/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authentication')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

def about(request):
    context = {'title':'About page',  'menu':menu}
    return render(request, 'animals/about.html',context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page was not found</h1>")