import requests as r
import datetime
from collections import defaultdict
import binascii
import base64
from hashlib import sha256
URL = 'https://api.dev.walletone.com/p2p'
SignatureKey = 'KgX5SOAwqPgiGnjKR0TGKTyBEGp5E8baCpovOP6bgkXQhfH3kdSQ9P'
time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

body = {
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

# signature = base64.b64encode(sha256(str(URL+time+SignatureKey)))


headers = {
'X-Wallet-PlatformId': 'startrek1',
    'X-Wallet-Signature': 'KgX5SOAwqPgiGnjKR0TGKTyBEGp5E8baCpovOP6bgkXQhfH3kdSQ9P',
    'X-Wallet-Timestamp': time
}

page = r.post(URL, headers=headers, data=body)
print(page)

