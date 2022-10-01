from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(AnimalHome.as_view()), name='home'),
    #path('', AnimalHome.as_view(), name='home'),

    path('category/<slug:cat_slug>/', AnimalsCategory.as_view(), name='category'),
    
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),

    path('addpage/', AddPage.as_view(), name='add_page'),
    
    path('contact/', ContactFormView.as_view(), name='contact'),

    path('register/', RegisterUser.as_view(), name='register'),

    path('login/', LoginUser.as_view(), name='login'),
    
    path('logout/', logout_user, name='logout'),

    path('about/', about, name='about'),
    
]