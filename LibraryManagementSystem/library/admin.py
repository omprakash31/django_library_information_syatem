from django.contrib import admin
from library.models import book,users,available_books,book_transaction

admin.site.register(book)
admin.site.register(users)
admin.site.register(available_books)
admin.site.register(book_transaction)
# Register your models here.
