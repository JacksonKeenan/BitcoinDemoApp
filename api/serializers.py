from rest_framework import serializers
from .models import SenderWallet
from .models import PublicWallet

class SenderWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderWallet
        fields = ('id', 'name', 'public', 'private', 'address', 'balance', 'unconfirmed_balance', 'total_received','total_sent', 'created',)

class CreateSenderWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderWallet
        fields = ('name',)

class PublicWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicWallet
        fields = ('id', 'address', 'balance', 'unconfirmed_balance', 'total_received','total_sent', 'last_updated',)
class CreatePublicWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicWallet
        fields = ('address',)
