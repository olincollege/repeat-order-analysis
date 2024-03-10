import requests

KEYSTRING = "xm01cxk1qnki67tzfe77r61m"

token = {
    "access_token": "314203756.n9GBGl7tKXcShEXME3RaeCZRFfeZXaqFcNAcyoV6zeq7MnPrGVxK3wXfY6N9Hrr0Ox_4HQhDZ3YxtXgNvex1uI8AcD",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "314203756.MOeUzMslCK5IyxaFBue9pd_85lRK8Tpm0bP_SX_CRmuL9o0Gn0-e7Ft1tHEx42cxYziHA-EUlpiWgHS7FSm2V-FtDH",
}

headers = {
    "Authorization": f"Bearer {token['access_token']}",
    "x-api-key": KEYSTRING,
}

SHOP_ID = 23574688
orders_url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/receipts"
response = requests.get(orders_url, headers=headers, timeout=10)

print(response.status_code)
