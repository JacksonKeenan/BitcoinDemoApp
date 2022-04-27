from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics, status
from .serializers import SenderWalletSerializer, CreateSenderWalletSerializer
from .serializers import PublicWalletSerializer, CreatePublicWalletSerializer
from .models import SenderWallet
from .models import ActiveSenderWallet
from .models import PublicWallet
from rest_framework.views import APIView
from rest_framework.response import Response
from blockcypher import get_address_overview
from blockcypher import create_unsigned_tx
from blockcypher import make_tx_signatures
from blockcypher import broadcast_signed_transaction
import requests
import json
import binascii

class CreateSenderWalletView(APIView):
    serializer_class = CreateSenderWalletSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')

            queryset = SenderWallet.objects.filter(name=name)
            if queryset.exists():
                senderWallet = queryset[0]

                try:
                    blockcypherResponse = get_address_overview(senderWallet.address, 'btc-testnet');
                except:
                    return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)
                if("error" in blockcypherResponse):
                    return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)

                senderWallet.balance = blockcypherResponse['balance']
                senderWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                senderWallet.total_received = blockcypherResponse['total_received']
                senderWallet.total_sent = blockcypherResponse['total_sent']
                senderWallet.save(update_fields=['balance', 'unconfirmed_balance', 'total_received', 'total_sent',])

                activeQueryset = ActiveSenderWallet.objects.all()
                if activeQueryset.exists():
                    activeSenderWallet = activeQueryset[0]
                    activeSenderWallet.name = name
                    activeSenderWallet.public = senderWallet.public
                    activeSenderWallet.private = senderWallet.private
                    activeSenderWallet.address = senderWallet.address
                    activeSenderWallet.balance = blockcypherResponse['balance']
                    activeSenderWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                    activeSenderWallet.total_received = blockcypherResponse['total_received']
                    activeSenderWallet.total_sent = blockcypherResponse['total_sent']
                    activeSenderWallet.save(update_fields=['name', 'public', 'private', 'address', 'balance', 'unconfirmed_balance', 'total_received', 'total_sent',])
                else:
                    activeSenderWallet = ActiveSenderWallet(name=name, public=senderWallet.public, private=senderWallet.private, address=senderWallet.address, balance=blockcypherResponse['balance'], unconfirmed_balance=blockcypherResponse['unconfirmed_balance'], total_received=blockcypherResponse['total_received'], total_sent=blockcypherResponse['total_sent'])
                    activeSenderWallet.save()


                return Response(SenderWalletSerializer(senderWallet).data, status=status.HTTP_200_OK)
            else:
                newWallet = requests.post('https://api.blockcypher.com/v1/btc/test3/addrs')
                newWallet = newWallet.text
                newWallet = json.loads(newWallet)

                try:
                    blockcypherResponse = get_address_overview(newWallet['address'], 'btc-testnet');
                except:
                    return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)
                if("error" in blockcypherResponse):
                    return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)

                senderWallet = SenderWallet(name=name, public=newWallet['public'], private=newWallet['wif'], address=newWallet['address'], balance=blockcypherResponse['balance'], unconfirmed_balance=blockcypherResponse['unconfirmed_balance'], total_received=blockcypherResponse['total_received'], total_sent=blockcypherResponse['total_sent'])
                senderWallet.save()

                activeQueryset = ActiveSenderWallet.objects.all()
                if activeQueryset.exists():
                    activeSenderWallet = activeQueryset[0]
                    activeSenderWallet.name = name
                    activeSenderWallet.public = newWallet['public']
                    activeSenderWallet.private = newWallet['private']
                    activeSenderWallet.address = newWallet['address']
                    activeSenderWallet.balance = blockcypherResponse['balance']
                    activeSenderWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                    activeSenderWallet.total_received = blockcypherResponse['total_received']
                    activeSenderWallet.total_sent = blockcypherResponse['total_sent']
                    activeSenderWallet.save(update_fields=['name', 'public', 'private', 'address', 'balance', 'unconfirmed_balance', 'total_received', 'total_sent',])


                return Response(SenderWalletSerializer(senderWallet).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CreatePublicWalletSearchView(APIView):
    serializer_class = CreatePublicWalletSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            address = serializer.data.get('address')

            try:
                blockcypherResponse = get_address_overview(address, 'btc-testnet');
            except:
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)
            if("error" in blockcypherResponse):
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = PublicWallet.objects.filter(address=address)
            if queryset.exists():
                publicWallet = queryset[0]
                time_threshold = timezone.now() - timezone.timedelta(seconds=5) ###### Chnage before demo!!!!!!!
                queryset = queryset.filter(last_updated__gt=time_threshold)

                if not queryset.exists() :
                    publicWallet.balance = blockcypherResponse['balance']
                    publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                    publicWallet.total_received = blockcypherResponse['total_received']
                    publicWallet.total_sent = blockcypherResponse['total_sent']
                    publicWallet.last_updated = timezone.now()
                    publicWallet.save(update_fields=['balance', 'unconfirmed_balance', 'total_received', 'total_sent', 'last_updated'])

                return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_200_OK)
            else:
                publicWallet = PublicWallet(address=address)
                publicWallet.balance = blockcypherResponse['balance']
                publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                publicWallet.total_received = blockcypherResponse['total_received']
                publicWallet.total_sent = blockcypherResponse['total_sent']
                publicWallet.last_updated = timezone.now()
                publicWallet.save()
                return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CreatePublicWalletSendView(APIView):
    serializer_class = CreatePublicWalletSerializer

    def post(self, request, format=None):


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            address = serializer.data.get('address')
            amount = request.data['amount']
            print(amount)

            try:
                blockcypherResponse = get_address_overview(address, 'btc-testnet');
            except:
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)
            if("error" in blockcypherResponse):
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)

            activeQueryset = ActiveSenderWallet.objects.all()
            if activeQueryset.exists():
                activeSenderWallet = activeQueryset[0]

                ### Create Unsigned Transaction ###
                inputs = [{'address': activeSenderWallet.address}, ]
                outputs = [{'address': address, 'value': int(amount)}]
                try:
                    unsigned_tx = create_unsigned_tx(api_key=API_KEY, inputs=inputs, outputs=outputs, coin_symbol='btc-testnet', preference='zero')
                except:
                    return Response({'error': 'Bad Transaction (Unsigned)'}, status=status.HTTP_400_BAD_REQUEST)
                if("error" in blockcypherResponse):
                    print("\n" + unsigned_tx + "\n")
                    return Response({'error': 'Bad Transaction (Unsigned)'}, status=status.HTTP_400_BAD_REQUEST)

                ### Create Public & Private Key Lists ( Size of unsigned_tx['tosign'] ) ###
                privkey_list = [activeSenderWallet.private,]
                pubkey_list = [activeSenderWallet.public,]

                ### Create Transaction Signatures ###
                try:
                    tx_signatures = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=privkey_list, pubkey_list=pubkey_list)
                except:
                    return Response({'error': 'Bad Transaction Signatures'}, status=status.HTTP_400_BAD_REQUEST)
                if("error" in blockcypherResponse):
                    print("\n" + unsigned_tx + "\n")
                    return Response({'error': 'Bad Transaction Signatures'}, status=status.HTTP_400_BAD_REQUEST)

                ### Send Transaction ###
                try:
                    sent_tx = broadcast_signed_transaction(api_key=API_KEY, coin_symbol='btc-testnet', unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=pubkey_list)
                except:
                    return Response({'error': 'Bad Transaction (Signed)'}, status=status.HTTP_400_BAD_REQUEST)
                if("error" in blockcypherResponse):
                    print("\n" + unsigned_tx + "\n")
                    return Response({'error': 'Bad Transaction (Signed)'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                blockcypherResponse = get_address_overview(address, 'btc-testnet');
            except:
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)
            if("error" in blockcypherResponse):
                return Response({'Bad Request': 'Bad Address'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = PublicWallet.objects.filter(address=address)
            if queryset.exists():
                publicWallet = queryset[0]
                time_threshold = timezone.now() - timezone.timedelta(seconds=5) ###### Chnage before demo!!!!!!!
                queryset = queryset.filter(last_updated__gt=time_threshold)

                if not queryset.exists() :
                    publicWallet.balance = blockcypherResponse['balance']
                    publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                    publicWallet.total_received = blockcypherResponse['total_received']
                    publicWallet.total_sent = blockcypherResponse['total_sent']
                    publicWallet.last_updated = timezone.now()
                    publicWallet.save(update_fields=['balance', 'unconfirmed_balance', 'total_received', 'total_sent', 'last_updated'])

                return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_200_OK)
            else:
                publicWallet = PublicWallet(address=address)
                publicWallet.balance = blockcypherResponse['balance']
                publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                publicWallet.total_received = blockcypherResponse['total_received']
                publicWallet.total_sent = blockcypherResponse['total_sent']
                publicWallet.last_updated = timezone.now()
                publicWallet.save()
                return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SenderWalletView(generics.ListAPIView):
    queryset = SenderWallet.objects.all()
    serializer_class = SenderWalletSerializer

class ActiveSenderWalletView(generics.ListAPIView):
    queryset = ActiveSenderWallet.objects.all()
    serializer_class = SenderWalletSerializer

class PublicWalletView(generics.ListAPIView):
    queryset = PublicWallet.objects.all()
    serializer_class = PublicWalletSerializer

class RecentPublicWalletView(generics.ListAPIView):
    time_threshold = timezone.now() - timezone.timedelta(minutes=30)
    queryset = PublicWallet.objects.filter(last_updated__gt=time_threshold)
    serializer_class = PublicWalletSerializer

class GetPublicWallet(APIView):
    serializer_class = PublicWalletSerializer
    lookup_url_kwarg = 'address'

    def get(self, request, format=None):
        address = request.GET.get(self.lookup_url_kwarg)
        if address != None:
            wallet = PublicWallet.objects.filter(address=address)
            if len(wallet) > 0:
                data = PublicWalletSerializer(wallet[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Wallet Address'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'No Wallet Address Given'}, status=status.HTTP_400_BAD_REQUEST)
