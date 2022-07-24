from datetime import date,timedelta
import smtplib
import email,math
from itertools import count
from unicodedata import category
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import users,book_transaction,available_books,book,invoice_history
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def library_home_view(request):
    # return HttpResponse("<h1>hello</h1>")
    return render(request,"home/home.html")

@ csrf_exempt
def all_books(request):
    books=book.objects.all()
    books={"books":books}
    return render(request,"book/book.html",books)

def add_user(request):
    return render(request,"user/add_user.html")

@ csrf_exempt
def create_user(request):
    
    first_name=request.POST["firstname"]
    last_name=request.POST["lastname"]
    user_name=first_name+" "+last_name
    email=request.POST["email"]
    gender=request.POST["gender"]
    mobile_no=request.POST["mob"]
    category=request.POST["category"]
    user_id=request.POST["user_id"]
    limit=0
    duration=0
    penalty=0
    count=0
    if category=="Under Graduate":
        limit=2
        duration=1
    elif category=="Post Graduate":
        limit=4
        duration=1
    elif category=="Research Scholar":
        limit=6
        duration=3
    elif category=="Faculty Member":
        limit=10
        duration=6

    users.objects.create(user_name=user_name,gender=gender,email=email,mobile=mobile_no,category=category,limit=limit,duration=duration,penalty=penalty,count=count,user_id=user_id)
    return HttpResponseRedirect("/")

def all_user_view(request):
    user=users.objects.all()
    user_dict={"users":user}
    return render(request,"user/all_user.html",user_dict)


@ csrf_exempt
def edit_user(request):
    userid=request.POST["edit_user_detail"]
    name=users.objects.get(pk=userid).user_name.split()
    if(len(name)==1):
        name.append(" ")
    user={"user":users.objects.get(pk=userid),"firstname":name[0],"lastname":name[1]}
    return render(request,"user/edit_user.html",user)

@ csrf_exempt
def update_user(request):
    id=request.POST["id"]
    user=users.objects.get(pk=id)
    user.email=request.POST["email"]
    user.mobile=request.POST["mob"]
    user.save()
    return HttpResponseRedirect("/")


@ csrf_exempt
def profile_view(request):
    id=request.POST["id"]
    name=users.objects.get(pk=id).user_name.split()[0]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    books_issued=book_transaction.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)

@ csrf_exempt
def add_book_to_user(request):
    id=request.POST["id"]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    # print(user_id)
    isbn=request.POST["isbn"]
    title=available_books.objects.filter(ISBN=isbn).values_list("title").get()[0]
    issue_date=date.today()
    deadline=issue_date - timedelta(days = 1)
    # deadline=issue_date+relativedelta(months=users.objects.filter(user_id=user_id).values_list("duration").get()[0])
    # print(deadline,title,issue_date)
    count=users.objects.filter(pk=id).values_list("count").get()[0]
    limit=users.objects.filter(pk=id).values_list("limit").get()[0]
    print(count,limit)
    if count<limit:
        book_transaction.objects.create(user_id=users.objects.get(id=id) ,ISBN=isbn,title=title,issue_date=issue_date,deadline=deadline)
        available_books.objects.filter(ISBN=isbn).delete()
        book_added=book.objects.get(title=title)
        book_added.copies-=1
        book_added.save()
        u=users.objects.get(pk=id)
        u.count+=1
        u.save()
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)



@ csrf_exempt
def delete_book(request):
    isbn=request.POST["isbn"]
    transaction_user_id=book_transaction.objects.filter(ISBN=isbn).values_list("user_id").get()[0]
    id=users.objects.filter(user_id=transaction_user_id).values_list("id").get()[0]
    # print(user_id)
    # isbn=request.POST["isbn"]
    title=book_transaction.objects.filter(ISBN=isbn).values_list("title").get()[0]

    return_date=date.today()
    deadline=book_transaction.objects.filter(ISBN=isbn).values_list("deadline").get()[0]
    r=(return_date-deadline).days
    print(isbn)
    u=users.objects.get(pk=id)
    if r>0:
        u.penalty+=r
    available_books.objects.create(title=title,ISBN=isbn)
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    book_transaction.objects.get(ISBN=isbn).delete()
    book_added=book.objects.get(title=title)
    book_added.copies+=1
    book_added.save()
    
    u.count-=1
    u.save()
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)

@ csrf_exempt
def send_reminder(request):
    transaction=book_transaction.objects.all()
    # server = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
    # 222222222222222
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login("website.tester.django@gmail.com", "bikibiki")
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
            send_mail("library book overdue", message, "website.tester.django@gmail.com", [u], fail_silently=True)
            # terminating the session

    # s.quit()
    return HttpResponseRedirect("/")
    # return redirect('/')


@ csrf_exempt
def bill_view(request):
    id=request.POST["id"]
    user=users.objects.get(pk=id)
    invoice=invoice_history.objects.count()
    user={"user":user,"invoice":invoice+1}
    return render(request,"invoice/invoice.html",user)

@csrf_exempt
def bill_paid(request):
    id=request.POST["id"]
    user_id=users.objects.get(pk=id).user_id
    penalty=users.objects.get(pk=id).penalty
    user=users.objects.get(pk=id)
    user.penalty-=1
    user.save()
    pay_date=date.today()
    invoice_history.objects.create(user_id=user_id,penalty=penalty,pay_date=pay_date)
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)
