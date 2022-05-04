from django.urls import path
from.views import (
    SenderWalletView,
    PublicWalletView,
    CreateSenderWalletView,
    CreatePublicWalletSendView,
    CreatePublicWalletSearchView,
    RecentPublicWalletView,
    GetPublicWallet,
    ActiveSenderWalletView
)

urlpatterns = [
    path('create-sender-wallet', CreateSenderWalletView.as_view()),
    path('create-public-wallet-send', CreatePublicWalletSendView.as_view()),
    path('create-public-wallet-search', CreatePublicWalletSearchView.as_view()),
    path('list-sender-wallets', SenderWalletView.as_view()),
    path('list-active-sender-wallet', ActiveSenderWalletView.as_view()),
    path('list-public-wallets', PublicWalletView.as_view()),
    path('list-recent-public-wallets', RecentPublicWalletView.as_view()),
    path('get-public-wallet', GetPublicWallet.as_view()),
]
