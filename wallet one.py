import requests as r
import datetime
from collections import defaultdict
import binascii
from hashlib import md5

URL = 'https://api.dev.walletone.com/p2p'


def get_signature(params, secret_key):
    """
    Base64(Byte(MD5(Windows1251(Sort(Params) + SecretKey))))
    params - list of tuples [('WMI_CURRENCY_ID', 643), ('WMI_PAYMENT_AMOUNT', 10)]
    """
    icase_key = lambda s: str(s, 'utf-8').lower()

    lists_by_keys = defaultdict(list)
    for key, value in params:
        lists_by_keys[key].append(value)

    str_buff = ''
    for key in sorted(lists_by_keys, key=icase_key):
        for value in sorted(lists_by_keys[key], key=icase_key):
            str_buff += str(value, 'utf-8').encode('1251')
    str_buff += secret_key
    md5_string = md5(str_buff).digest()
    return binascii.b2a_base64(md5_string)[:-1]


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



answer = r.post(url=URL + '/api/v3/deals', data=body)
print(answer)
