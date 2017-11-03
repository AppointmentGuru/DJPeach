SUCCESS_PAYMENT = {
  "id": "8a82944a5d98b2fd015d9e37163300cf",
  "registrationId": "8a82944a5d98b2fd015d9d38d48c2612",
  "paymentType": "DB",
  "paymentBrand": "VISA",
  "amount": "400.00",
  "currency": "ZAR",
  "descriptor": "0394.0684.2530 AG01 Nedbank Recur",
  "merchantTransactionId": "1/1/3e9409f1-c52a-402f-a219-4f140ad576d7",
  "result": {
    "code": "000.100.110",
    "description": "Request successfully processed in 'Merchant in Integrator Test Mode'"
  },
  "card": {
    "bin": "411111",
    "last4Digits": "1111",
    "holder": "Joe Soap",
    "expiryMonth": "01",
    "expiryYear": "2018"
  },
  "customer": {
    "merchantCustomerId": '1',
    "givenName": "Joe",
    "companyName": "AppointmentGuru",
    "mobile": "+27832566533",
    "email": "christo@appointmentguru.co",
    "ip": "1.2.3.4",
    "ipCountry": "ZA"
  },
  "customParameters": {
    "CTPE_DESCRIPTOR_TEMPLATE": ""
  },
  "risk": {
    "score": "100"
  },
  "cart": {
    "items": [
      {
        "merchantItemId": "1",
        "name": "AppointmentGuru subscription",
        "quantity": "1",
        "price": "400",
        "originalPrice": "400"
      }
    ]
  },
  "buildNumber": "eb3636546fa6f04bfa9dc7231ed32730f6809b11@2017-08-01 09:24:55 +0000",
  "timestamp": "2017-08-01 14:33:16+0000",
  "ndc": "D9864FFA660816ABDFFE22238EAFA3D3.sbg-vm-tx02"
}

RECURRING_FAILURE = {'id': '8a8294495f587757015f811733d97f74', 'paymentType': 'PA', 'result': {'code': '100.150.101', 'description': 'invalid length for specified registration id (must be 32 chars)'}, 'buildNumber': '70bd28957756bc1b3459623aeaa957711b7e9336@2017-11-02 09:13:45 +0000', 'timestamp': '2017-11-03 08:55:02+0000', 'ndc': '8a82941858969fbc01589bff431c1e14_9e0dd9e5c3b04a91a5c99101c303420c'}
RECURRING_SUCCESS = {
  'amount': '10.00',
  'buildNumber': '70bd28957756bc1b3459623aeaa957711b7e9336@2017-11-02 09:13:45 +0000',
  'currency': 'ZAR',
  'descriptor': '4709.8902.5954 AG01 Nedbank Recur ',
  'id': '8a82944a5f5892d0015f81218f0e506c',
  'ndc': '8a82941858969fbc01589bff431c1e14_a4afc73f195c42b5904245528ac71d39',
  'paymentType': 'PA',
  'result': {
    'code': '000.100.110',
    'description': "Request successfully processed in 'Merchant in Integrator Test Mode'"
  },
  'risk': {'score': '100'},
  'timestamp': '2017-11-03 09:06:21+0000'
 }