from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from author.models import Author


def book_list(request):
    books = Book.objects.all()
    
    # Filtering
    query = request.GET.get('q')
    author_id = request.GET.get('author')
    
    if query:
        books = books.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if author_id:
        books = books.filter(authors__id=author_id)
    
    authors = Author.objects.all()
    
    context = {
        'books': books,
        'authors': authors,
        'search_query': query or '',
        'selected_author': int(author_id) if author_id else None
    }
    return render(request, 'book/book_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
        'available': book.count > 0
    }
    return render(request, 'book/book_detail.html', context)


@login_required
def user_books(request, user_id):
    if not request.user.is_librarian() and request.user.id != user_id:
        return redirect('book_list')
        
    from order.models import Order
    orders = Order.objects.filter(user_id=user_id, end_at__isnull=True)
    books = [order.book for order in orders]
    
    context = {
        'books': books,
        'user_books': True,
        'user_id': user_id
    }
    return render(request, 'book/book_list.html', context)
