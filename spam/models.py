from django.db import models

# Create your models hy
# ere.
class RegisteredUser(models.Model):
  user = models.CharField(max_length = 100)
  phone_no = models.IntegerField(null=False,unique=True)
  password = models.CharField(max_length=50)
  email = models.CharField(max_length = 50, null=True)

  spam = models.BooleanField(default=False)



class Contacts(models.Model):
  name = models.CharField(max_length = 100,default="", editable=False)
  phone_no = models.IntegerField(null=False)
  email = models.CharField(max_length=50, null=True)
  spam = models.BooleanField(default=False)


class ContactList(models.Model):
   name = models.CharField(max_length=100)
   phone_no = models.IntegerField(null=False)
   userId = models.IntegerField(null=False)



