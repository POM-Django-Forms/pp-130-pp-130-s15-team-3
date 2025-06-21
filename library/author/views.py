from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .models import Author
from .forms import AuthorForm

def is_librarian(user):
    return user.is_authenticated and user.role == 1

@user_passes_test(is_librarian)
def author_list_view(request):
    authors = Author.get_all()
    return render(request, 'author/author_list.html', {'authors': authors})

@user_passes_test(is_librarian)
def author_create_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author:author_list')
    else:
        form = AuthorForm()
    return render(request, 'author/author_form.html', {'form': form, 'title': 'Create Author'})

@user_passes_test(is_librarian)
def author_delete_view(request, author_id):
    author = Author.get_by_id(author_id)
    if not author:
        return HttpResponseForbidden("Author not found.")

    if author.books.exists():
        return HttpResponseForbidden("Cannot delete author with books attached.")

    author.delete()
    return redirect('author:author_list')

@user_passes_test(is_librarian)
def author_edit_view(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author:author_list')
    else:
        form = AuthorForm(instance=author)
        
    return render(request, 'author/author_form.html', {'form': form, 'title': 'Edit Author'})

@user_passes_test(is_librarian)
def author_detail_view(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author/author_detail.html', {'author': author})
