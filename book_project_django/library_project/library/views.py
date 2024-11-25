from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

def book_list(request):
    """
    View to display a list of all books.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with a list of books.
    """
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, pk):
    """
    View to display the details of a single book.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the book to retrieve.

    Returns:
        HttpResponse: Rendered template with book details.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

def book_create(request):
    """
    View to handle the creation of a new book.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered form template or redirect to book list on successful save.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

def book_edit(request, pk):
    """
    View to handle editing an existing book.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the book to edit.

    Returns:
        HttpResponse: Rendered form template or redirect to book detail on successful save.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

def book_delete(request, pk):
    """
    View to handle the deletion of a book.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the book to delete.

    Returns:
        HttpResponse: Rendered confirmation template or redirect to book list on successful deletion.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})
