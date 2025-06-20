from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .models import Author
from book.models import Book

def is_librarian(user):
    return user.is_authenticated and user.role == 'librarian'

@user_passes_test(is_librarian)
def author_list_view(request):
    authors = Author.get_all()
    return render(request, 'author/author_list.html', {'authors': authors})

@user_passes_test(is_librarian)
def author_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')
        Author.create(name=name, surname=surname, patronymic=patronymic)
        return redirect('author_list')
    return render(request, 'author/author_create.html')

@user_passes_test(is_librarian)
def author_delete_view(request, author_id):
    author = Author.get_by_id(author_id)
    if not author:
        return HttpResponseForbidden("Author not found.")

    if author.books.exists():
        return HttpResponseForbidden("Cannot delete author with books attached.")

    author.delete()
    return redirect('author_list')
