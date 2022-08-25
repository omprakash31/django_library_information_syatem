from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *
def tick():
    r=reserved_book.objects.all()
    for rbook in r:
        # rbook.
        r=(datetime.today().date()-rbook.reserve_date).days
        if r>=7:
            available_books.objects.create(title=rbook.title,ISBN=rbook.ISBN)
            book_added=book.objects.get(title=rbook.title)
            book_added.copies+=1
            book_added.save()
            reserved_book.objects.get(ISBN=rbook.ISBN).delete()
        print(rbook.user_id,datetime.now())
def tick1():
    print(1)
    send_mail("library book overdue", message, "librarytester250@gmail.com", [bikisahoo02@gmail.com], fail_silently=True)

def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(tick1, 'interval', seconds=10)
    # scheduler.add_job(tick, 'interval', minutes=5)
    # scheduler.add_job(tick, 'cron', hour='*')
    scheduler.add_job(tick, 'cron', hour=12, minute=1)
    scheduler.add_job(tick1, 'cron', hour=7, minute=18)
    scheduler.add_job(tick1, 'cron', hour=7, minute=19)
    scheduler.add_job(tick1, 'cron', hour=7, minute=20)
    # scheduler.add_job(tick, 'cron', hour="11.57")
    scheduler.start()
