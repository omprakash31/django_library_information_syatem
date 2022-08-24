from __future__ import absolute_import,unicode_literals
from time import time
from celery import shared_task
# from celery import task
from celery import Celery
from .models import book_transaction,users,book
from django.conf import settings
from django.core.mail import send_mail
from datetime import date

app = Celery('LibraryManagementSystem')

@shared_task
def send_email_to_user():

    print("email")
    transaction=book_transaction.objects.all()
    for t in transaction:
        return_date=date.today()
        deadline=t.deadline
        r=(return_date-deadline).days
        # print(return_date,deadline,r,t.ISBN)
        if r>0:
            message = str(t.title)+" book has been over_due !! try to return it ASAP"+"\n"+"The deadline was: "+str(t.deadline)
            # sending the mail
            #    email-password-----umhltstpuxcwmjcz
            # s.sendmail("website.tester.django@gmail.com", "bikisahoo02@gmail.com", message)
            user_id=str(t.user_id)
            u=users.objects.filter(user_id=user_id).values_list("email").get()[0]
            send_mail("library book overdue", message, "librarytester250@gmail.com", [u], fail_silently=True)
            # terminating the session

from django.views.decorators.csrf import csrf_exempt
# @ csrf_exempt
@shared_task
def send_book_to_user(user_id,id1):
    email=users.objects.get(user_id=user_id).email
    print(id,user_id,email)
    books=book.objects.get(pk=id1)
    title=books.title
    send_mail("E-book drive link", "You can download the book "+str(title)+" from the following link "+str(books.ebook_url), "website.tester.django@gmail.com", [email], fail_silently=True)
    print(title)

@app.task()
def scheduletask():
    print("successfully printed")



@shared_task
def add(x, y):
    return x + y

@shared_task
def print1():
    print("hello")
    return 0

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()