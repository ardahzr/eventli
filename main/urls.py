from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.etkinlikler),
    path('search/', views.search, name='search'),
    path("about",views.about),
    path("contact",views.contact),
    path('etkinlikler/', views.etkinlikler, name='etkinlikler'),
    path('etkinlikler/<slug:etkinlik_slug>/', views.etkinlik_detay, name='etkinlik_detay'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('etkinlik/<slug:etkinlik_slug>/kayit/', views.etkinlik_kayit, name='etkinlik_kayit'),
    path('create_event/', views.create_event, name='create_event'),
    path('delete_event/<slug:etkinlik_slug>/', views.delete_event, name='delete_event'),
    path('delete_etkinlik_katilim/<slug:etkinlik_slug>/', views.delete_etkinlik_katilim, name='delete_etkinlik_katilim'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)