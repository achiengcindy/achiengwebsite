from django.urls import path , re_path 
from .views import register, accounts_edit, activate, account_activation_sent
urlpatterns = [
    path('register/', register, name='register'),
    path('accounts_edit/', accounts_edit, name='accounts_edit'),
    #re_path('activate/?P<uidb64>[0-9A-Za-z_\-]+/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>)/', activate, name='activate'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
   
]

