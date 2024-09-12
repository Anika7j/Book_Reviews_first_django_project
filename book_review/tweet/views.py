from django.shortcuts import render
from .models import Review
from .forms import BookForm, UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def book_list(request):
    books = Review.objects.all().order_by()
    return render(request, 'book_list.html', {'books': books})

@login_required
def book_review(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_review.html', {'form': form})

@login_required
def review_edit(request,review_id):
    review = get_object_or_404(Review, pk=review_id, user = request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES,instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=review)
    return render(request, 'book_review.html', {'form': form})

@login_required
def review_delete(request,review_id):
    review = get_object_or_404(Review, pk=review_id, user = request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('book_list')
    return render(request, 'book_review_delete.html', {'review': review})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})