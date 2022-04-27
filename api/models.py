from django.db import models

#'id', 'address', 'balance', 'unconfirmed_balance', 'total_received',' total_sent', 'last_updated',

# Create your models here.
class SenderWallet(models.Model):
    name = models.CharField(max_length=50, default="")
    public = models.CharField(max_length=150, default="")
    private = models.CharField(max_length=150, default="")
    address = models.CharField(max_length=150, default="")
    balance = models.IntegerField(null=False, default=0)
    unconfirmed_balance = models.IntegerField(null=False, default=0)
    total_received = models.IntegerField(null=False, default=0)
    total_sent = models.IntegerField(null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)

class ActiveSenderWallet(models.Model):
    name = models.CharField(max_length=50, default="")
    public = models.CharField(max_length=150, default="")
    private = models.CharField(max_length=150, default="")
    address = models.CharField(max_length=150, default="")
    balance = models.IntegerField(null=False, default=0)
    unconfirmed_balance = models.IntegerField(null=False, default=0)
    total_received = models.IntegerField(null=False, default=0)
    total_sent = models.IntegerField(null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)

class PublicWallet(models.Model):
    address = models.CharField(max_length=50, default="",)
    balance = models.IntegerField(null=False, default=0)
    unconfirmed_balance = models.IntegerField(null=False, default=0)
    total_received = models.IntegerField(null=False, default=0)
    total_sent = models.IntegerField(null=False, default=0)
    last_updated = models.DateTimeField(auto_now_add=True)
