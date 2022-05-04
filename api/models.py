from django.db import models

class Wallet(models.Model):
    address = models.CharField(max_length=50, default="",)
    balance = models.IntegerField(null=False, default=0)
    unconfirmed_balance = models.IntegerField(null=False, default=0)
    total_received = models.IntegerField(null=False, default=0)
    total_sent = models.IntegerField(null=False, default=0)

    class Meta:
        abstract = True

class SenderWallet(Wallet):
    name = models.CharField(max_length=50, default="")
    public = models.CharField(max_length=150, default="")
    private = models.CharField(max_length=150, default="")
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

class PublicWallet(Wallet):
    last_updated = models.DateTimeField(auto_now_add=True)
