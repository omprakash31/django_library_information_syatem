from django.db import models
from datetime import date

# Create your models here.
class book(models.Model):
    title=models.CharField(max_length=30)
    author=models.CharField(max_length=30)
    copies=models.IntegerField(default=1)
    description=models.TextField()
    ebook_url=models.CharField(max_length=2000,default="None")
    cover_url=models.CharField(max_length=2000,default="None")
    def __str__(self):
        return str(self.title)+"__"+str(self.id)+"__"+str(self.copies)
class available_books(models.Model):
    title=models.CharField(max_length=30)
    ISBN=models.IntegerField(default=2000,unique=True)
    def __str__(self):
        return str(self.title)+"__"+str(self.ISBN)


class users(models.Model):
    user_name=models.CharField(max_length=30)
    email=models.EmailField()
    mobile=models.IntegerField()
    gender=models.CharField(max_length=6,default="N/A")
    user_id=models.IntegerField(unique=True)
    category=models.CharField(max_length=20)
    limit=models.IntegerField()
    duration=models.IntegerField()
    penalty=models.IntegerField()
    count=models.IntegerField()
    register_date=models.DateField(default=date.today(),null=True)
    def __str__(self):
        return str(self.user_id)

class book_transaction(models.Model):
    user_id=models.ForeignKey('users',to_field='user_id',on_delete=models.CASCADE)
    ISBN=models.IntegerField(default=2000,unique=True)
    title=models.CharField(max_length=30)
    issue_date=models.DateField(default=date.today(),null=True)
    deadline=models.DateField(default=date.today(),null=True)
    def __str__(self):
        return str(self.user_id)+"__"+str(self.title)

class invoice_history(models.Model):
    user_id=models.IntegerField()
    penalty=models.IntegerField()
    pay_date=models.DateField(default=date.today(),null=True)
# cd LibraryManagementSystem