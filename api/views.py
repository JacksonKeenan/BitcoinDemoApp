from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics, status
from .serializers import SenderWalletSerializer, CreateSenderWalletSerializer, PublicWalletSerializer, CreatePublicWalletSerializer
from .models import SenderWallet, PublicWallet
from rest_framework.views import APIView
from rest_framework.response import Response
from blockcypher import get_address_overview, create_unsigned_tx, make_tx_signatures, broadcast_signed_transaction, get_blockchain_overview
import requests
import json
import os
import sys

## Blockcypher API Token
API_KEY = os.environ.get('BC_API')

## Verifies and Searches for a given address. If valid stores the information for the address
def SearchAddress(address):
    try:
        blockcypherResponse = get_address_overview(address, 'btc-testnet');
    except:
        return Response({'Error': 'Error: Invalid Address'}, status=status.HTTP_400_BAD_REQUEST)

    queryset = PublicWallet.objects.filter(address=address)

    ## Checks if a Wallet with the given address already exists
    ## If Yes: Updates that Wallet's information if the data is older than the set threshold
    if queryset.exists():
        publicWallet = queryset[0]

        ## time_threshold indicates if address needs to be updated (Default: minutes=30)
        time_threshold = timezone.now() - timezone.timedelta(seconds=5)
        queryset = queryset.filter(last_updated__gt=time_threshold)

        if not queryset.exists() :
            publicWallet.balance = blockcypherResponse['balance']
            publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
            publicWallet.total_received = blockcypherResponse['total_received']
            publicWallet.total_sent = blockcypherResponse['total_sent']
            publicWallet.last_updated = timezone.now()
            publicWallet.save(update_fields=['balance', 'unconfirmed_balance', 'total_received', 'total_sent', 'last_updated'])

        return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_200_OK)

    ## If No: Adds Wallet's information to the database
    else:
        publicWallet = PublicWallet(address=address)
        publicWallet.balance = blockcypherResponse['balance']
        publicWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
        publicWallet.total_received = blockcypherResponse['total_received']
        publicWallet.total_sent = blockcypherResponse['total_sent']
        publicWallet.last_updated = timezone.now()
        publicWallet.save()
        return Response(PublicWalletSerializer(publicWallet).data, status=status.HTTP_201_CREATED)

## Creates and Updates Sender Wallets
## Generates New Address Endpoints for new Wallets
class CreateSenderWalletView(APIView):
    serializer_class = CreateSenderWalletSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            queryset = SenderWallet.objects.filter(name=name)

            ## Checks if a Wallet with the given name already exists
            ## If Yes: Sets that Wallet as the Active Wallet
            if queryset.exists():
                senderWallet = queryset[0]

                try:
                    blockcypherResponse = get_address_overview(senderWallet.address, 'btc-testnet');
                except:
                    return Response({'Error': 'Assertion Error: Invalid Address format for coin symbol'}, status=status.HTTP_400_BAD_REQUEST)

                activeQueryset = SenderWallet.objects.filter(is_active=True)
                if activeQueryset.exists():
                    activeSenderWallet = activeQueryset[0]
                    activeSenderWallet.is_active = False
                    activeSenderWallet.save(update_fields=['is_active',])

                senderWallet.balance = blockcypherResponse['balance']
                senderWallet.unconfirmed_balance = blockcypherResponse['unconfirmed_balance']
                senderWallet.total_received = blockcypherResponse['total_received']
                senderWallet.total_sent = blockcypherResponse['total_sent']
                senderWallet.is_active = True
                senderWallet.save(update_fields=['balance', 'unconfirmed_balance', 'total_received', 'total_sent', 'is_active',])

                return Response(SenderWalletSerializer(senderWallet).data, status=status.HTTP_200_OK)

            ## If No: Creates a new endpoint and stores the information as a new Wallet, then sets new Wallet as the Active Wallet
            else:
                newWallet = requests.post('https://api.blockcypher.com/v1/btc/test3/addrs')
                newWallet = newWallet.text
                newWallet = json.loads(newWallet)

                try:
                    blockcypherResponse = get_address_overview(newWallet['address'], 'btc-testnet');
                except:
                    return Response({'Error': 'Error: Invalid Address'}, status=status.HTTP_400_BAD_REQUEST)

                activeQueryset = SenderWallet.objects.filter(is_active=True)
                if activeQueryset.exists():
                    activeSenderWallet = activeQueryset[0]
                    activeSenderWallet.is_active = False
                    activeSenderWallet.save(update_fields=['is_active',])

                senderWallet = SenderWallet(name=name, public=newWallet['public'], private=newWallet['wif'], address=newWallet['address'], balance=blockcypherResponse['balance'], unconfirmed_balance=blockcypherResponse['unconfirmed_balance'], total_received=blockcypherResponse['total_received'], total_sent=blockcypherResponse['total_sent'], is_active=True)
                senderWallet.save()

                return Response(SenderWalletSerializer(senderWallet).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

## Creates Public Wallets
## Updates Stored Wallets Older than the given threshold
class CreatePublicWalletSearchView(APIView):
    serializer_class = CreatePublicWalletSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            address = serializer.data.get('address')
            blockcypherResponse = SearchAddress(address)
            return blockcypherResponse

        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

## Creates Public Wallets
## Updates Stored Wallets Older than the given threshold
## Sends a Transation to the Wallet
class CreatePublicWalletSendView(APIView):
    serializer_class = CreatePublicWalletSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            address = serializer.data.get('address')
            amount = request.data['amount']

            try:
                blockcypherResponse = get_address_overview(address, 'btc-testnet');
            except:
                return Response({'Error': 'Error: Invalid Address'}, status=status.HTTP_400_BAD_REQUEST)

            activeQueryset = SenderWallet.objects.filter(is_active=True)
            if activeQueryset.exists():
                activeSenderWallet = activeQueryset[0]

                ## Create Unsigned Transaction
                ## ! NOTE:  Currently this application is not including fees on transactions
                ## !!!!!!!  If this were to be modified an additional output would need to
                ## !!!!!!!  be added to prevent left over satoshis getting consumed by fees
                inputs = [{'address': activeSenderWallet.address}, ]
                outputs = [{'address': address, 'value': int(amount)},]
                try:
                    unsigned_tx = create_unsigned_tx(api_key=API_KEY, inputs=inputs, outputs=outputs, coin_symbol='btc-testnet', preference='zero')
                except AssertionError as e:
                    return Response({'Error': 'Error Creating Unsigned Transation: Invalid Address for Coin Symbol'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    print('\nError Creating Unsigned Transation: ' + str(sys.exc_info()[0]) + '\n')
                    return Response({'Error': 'Error Creating Unsigned Transation: Invalid API Key\n\nSee Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                if 'errors' in unsigned_tx and unsigned_tx['errors'][0] is not None:
                    return Response({'Error': 'Error Creating Transaction: ' + str(unsigned_tx['errors'][0]['error'])}, status=status.HTTP_400_BAD_REQUEST)

                ## Create Public & Private Key Lists ( Size of unsigned_tx['tosign'] )
                privkey_list = []
                pubkey_list = []

                for x in unsigned_tx['tosign']:
                    privkey_list.append(activeSenderWallet.private)
                    pubkey_list.append(activeSenderWallet.public)

                ## Create Transaction Signatures
                try:
                    tx_signatures = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=privkey_list, pubkey_list=pubkey_list)
                except AssertionError as e:
                    print('\nError Signing Transaction: \n' + 'Assertion Error (Run in debug mode for more information)' + '\n')
                    if 'errors' not in unsigned_tx:
                        return Response({'Error': 'Error Signing Transaction: See Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'Error': 'Error Signing Transaction: ' + str(unsigned_tx['errors'][0]['error']) + '\n\nSee Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    print('\nError Signing Transaction: ' + str(sys.exc_info()[0]) + '\n')
                    if 'errors' not in unsigned_tx:
                        return Response({'Error': 'Error Signing Transaction: See Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'Error': 'Error Signing Transaction: ' + str(unsigned_tx['errors'][0]['error']) + '\n\nSee Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)

                ## Send Transaction
                try:
                    sent_tx = broadcast_signed_transaction(api_key=API_KEY, coin_symbol='btc-testnet', unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=pubkey_list)
                except AssertionError as e:
                    print('\nError Sending Transaction: \n' + str(e) + '\n')
                    if 'errors' not in unsigned_tx:
                        return Response({'Error': 'Error Sending Transaction: See Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'Error': 'Error Sending Transaction: ' + str(unsigned_tx['errors'][0]['error']) + '\n\nSee Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    print('\nError Sending Transaction: ' + str(sys.exc_info()[0]) + '\n')
                    if 'errors' not in unsigned_tx:
                        return Response({'Error': 'Error Sending Transaction: See Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'Error': 'Error Sending Transaction: ' + str(unsigned_tx['errors'][0]['error']) + '\n\nSee Django Console for More Information'}, status=status.HTTP_400_BAD_REQUEST)

            if 'errors' in sent_tx:
                return Response({'Error': 'Error Sending Transaction: ' + str(sent_tx['errors'][0]['error'])}, status=status.HTTP_400_BAD_REQUEST)

            ## Getting Updated Balance for Receiving Wallet
            blockcypherResponse = SearchAddress(address)
            return blockcypherResponse

        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

## Retutns All Sender Wallets
class SenderWalletView(generics.ListAPIView):
    queryset = SenderWallet.objects.all()
    serializer_class = SenderWalletSerializer

## Retutns the Active Sender Wallets
class ActiveSenderWalletView(generics.ListAPIView):
    queryset = SenderWallet.objects.filter(is_active=True)
    serializer_class = SenderWalletSerializer

## Retutns All Public Wallets
## Optional Paramater 'delta' indicates if address is to be returned (Minutes)
class PublicWalletView(generics.ListAPIView):
    serializer_class = PublicWalletSerializer

    def get_queryset(self):
        delta = self.request.query_params.get('delta')
        if(delta and delta.isdigit()):
            time_threshold = timezone.now() - timezone.timedelta(minutes=int(delta))
            queryset = PublicWallet.objects.filter(last_updated__gt=time_threshold).order_by('-last_updated')
        else:
            queryset = PublicWallet.objects.all().order_by('-last_updated')
        return queryset

## Retruns a Public Wallet with the Given Address
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
