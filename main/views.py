from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse
from .models import Category,Etkinlik,EtkinlikKatilim
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm,EtkinlikForm
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    categories = Category.objects.all()
    etkinlikler = Etkinlik.objects.all()
    context = {'etkinlikler': etkinlikler, 'categories': categories}
    return render(request, 'registration/profile.html', context)



def create_event(request):
    if request.method == 'POST':
        form = EtkinlikForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = EtkinlikForm()  

    return render(request, 'create_event.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('etkinlikler')

def search(request):

    query = request.GET.get("q")
    if query:
        etkinlikler = Etkinlik.objects.filter(title__icontains=query)
        return render(request, 'search_results.html', {'etkinlikler': etkinlikler, 'query': query})
    else:
        return render(request, 'search_results.html', {'query': query})

def etkinlikler(request):
    categories = Category.objects.all()
    etkinlikler = Etkinlik.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        etkinlikler = etkinlikler.filter(category_id=category_id)

    return render(request, 'etkinlikler.html', {'etkinlikler': etkinlikler, 'categories': categories})


def etkinlik_detay(request, etkinlik_slug):
    etkinlik = get_object_or_404(Etkinlik, pk=etkinlik_slug)
    return render(request, 'etkinlik_detay.html', {'etkinlik': etkinlik})



@login_required
def etkinlik_kayit(request, etkinlik_slug):
    etkinlik = Etkinlik.objects.get(slug=etkinlik_slug)
    EtkinlikKatilim.objects.get_or_create(user=request.user, etkinlik=etkinlik)
    return redirect('profile',)

def delete_event(request, etkinlik_slug):
    if request.method == 'POST':
        etkinlik = get_object_or_404(Etkinlik, slug=etkinlik_slug)
        etkinlik.delete()
    return redirect('profile')
def delete_etkinlik_katilim(request, etkinlik_slug):
    if request.method == 'POST':

        etkinlik_katilim = EtkinlikKatilim.objects.get(etkinlik__slug=etkinlik_slug, user=request.user)

        etkinlik_katilim.delete()
        return redirect('profile')  
    else:
        return redirect('home')  