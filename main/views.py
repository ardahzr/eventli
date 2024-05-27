from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse
from .models import Category,Etkinlik,EtkinlikKatilim,Rating,Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm,EtkinlikForm,  RatingForm,CommentForm
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


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EtkinlikForm(request.POST, request.FILES)
        if form.is_valid():
            etkinlik = form.save(commit=False)
            etkinlik.user = request.user  # Oluşturan kullanıcıyı atayalım
            etkinlik.save()
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



from django.shortcuts import render
from .models import Category

def etkinlikler(request):
    categories = Category.objects.all()
    etkinlikler = Etkinlik.objects.filter(isActive=True).order_by('date')

    category_id = request.GET.get('category')
    if category_id:
        category = Category.objects.get(id=category_id)
        if category:
            # Eğer seçili kategori bir alt kategori değilse, o kategoriye ait etkinlikleri getir
            if category.parent is None:
                etkinlikler = etkinlikler.filter(category=category)
            # Eğer seçili kategori bir alt kategori ise, alt kategoriye ait etkinlikleri getir
            else:
                etkinlikler = etkinlikler.filter(category__in=category.get_descendants(include_self=True))

    return render(request, 'etkinlikler.html', {'etkinlikler': etkinlikler, 'categories': categories})


def etkinlik_detay(request, etkinlik_slug):
    etkinlik = get_object_or_404(Etkinlik, slug=etkinlik_slug)
    kayitli_kullanici_sayisi = EtkinlikKatilim.objects.filter(etkinlik=etkinlik_slug).count()
    katilimcilar = EtkinlikKatilim.objects.filter(etkinlik=etkinlik)
    comments = etkinlik.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.etkinlik = etkinlik
            new_comment.author = request.user
            new_comment.save()
            return redirect('etkinlik_detay', etkinlik_slug=etkinlik.slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'etkinlik_detay.html', {'etkinlik': etkinlik , 'kayitli_kullanici_sayisi': kayitli_kullanici_sayisi, 'katilimcilar': katilimcilar, 'comments': comments, 'comment_form': comment_form})

def delete_comment(request, etkinlik_slug, comment_id):
    # Etkinlik ve yorum nesnelerini al
    etkinlik = get_object_or_404(Etkinlik, slug=etkinlik_slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    # Yorumu silme yetkisi kontrolü
    if request.user == comment.author:
        comment.delete()

    # Yorum silindikten sonra etkinlik detayına geri dön
    return redirect('etkinlik_detay', etkinlik_slug=etkinlik_slug)


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
    

@login_required
def rate_user(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()
            return redirect('home')  # Burada uygun yönlendirmeyi yapmalısınız.
    else:
        form = RatingForm()
    return render(request, 'registration/profile.html', {'form': form})

def category_events(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # Seçilen kategoriye ait, level 1 olan tüm alt kategorileri filtreleyin.
    subcategories = category.get_children().filter(level=1) 
    etkinlikler = Etkinlik.objects.filter(category__in=subcategories, isActive=True).order_by('date') 
    context = {
        'category': category,
        'etkinlikler': etkinlikler,
    }
    category_id = request.GET.get('category')
    if category_id:
        etkinlikler = etkinlikler.filter(category_id=category_id)
    return render(request, 'etkinlikler.html', {'etkinlikler': etkinlikler, 'categories': category})


def etkinlik_duzenle(request, slug):
    etkinlik = Etkinlik.objects.get(slug=slug)
    if request.method == 'POST':
        form = EtkinlikForm(request.POST, request.FILES, instance=etkinlik)
        if form.is_valid():
            form.save()
            return redirect('etkinlik_detay', etkinlik_slug=slug)
    else:
        form = EtkinlikForm(instance=etkinlik)
    return render(request, 'etkinlik_duzenle.html', {'form': form})
