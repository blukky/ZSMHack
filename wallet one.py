import requests as r
import datetime


URL = 'https://api.dev.walletone.com/p2p'


time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

body = {
    'X-Wallet-PlatformId': 'startrek1',
    ' X-Wallet-Signature': 'KgX5SOAwqPgiGnjKR0TGKTyBEGp5E8baCpovOP6bgkXQhfH3kdSQ9P',
    'X-Wallet-Timestamp': time,
    "PlatformDealId": 'startrel1',
    "PlatformPayerId": "1",
    "PayerPhoneNumber": "+79123456789",
    "PayerPaymentToolId": 1,  # Опциональный параметр
    "PlatformBeneficiaryId": "1",
    "BeneficiaryPaymentToolId": 1,
    "Amount": 10.00,
    "CurrencyId": 643,
    "ShortDescription": "Оплата сделки",
    "FullDescription": "Полное описание",  # Опциональный параметр
    "DeferPayout": 'false'  # при значении false создается online (Instant) сделка
}


