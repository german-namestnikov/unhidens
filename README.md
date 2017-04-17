# Unhidens

## Description:
Small DNS Recon utility, allows you to obtain some useful info about NS-servers placed behind relays, firewalls, etc.

Requires 'dig' utility!

## Examples:

```json
$ ./unhidens.py --server ns9.nic.ru
{
    "ns9.nic.ru": {
        "ip": "31.177.85.186", 
        "servers": [
            {
                "ip": "31.177.85.194", 
                "name": "ns9-1.nic.ru"
            }
        ], 
        "versions": []
    }
}

$ ./unhidens.py --domain yandex.ru                                
{
    "ns1.yandex.ru.": {
        "ip": "213.180.193.1",
        "servers": [
            {
                "ip": "178.154.243.251",
                "name": "bearberry.yandex.ru"
            },
            {
                "ip": "178.154.243.248",
                "name": "bilberry.yandex.ru"
            },
            {
                "ip": "178.154.243.252",
                "name": "blueberry.yandex.ru"
            },
            {
                "ip": "178.154.243.249",
                "name": "boysenberry.yandex.ru"
            }
        ],
        "versions": [
            "Yandex"
        ]
    },
    "ns2.yandex.ru.": {
        "ip": "93.158.134.1",
        "servers": [
            {
                "ip": "95.108.230.249",
                "name": "mulberry.yandex.ru"
            },
            {
                "ip": "95.108.230.247",
                "name": "mooseberry.yandex.ru"
            },
            {
                "ip": "95.108.230.248",
                "name": "gooseberry.yandex.ru"
            },
            {
                "ip": "95.108.230.250",
                "name": "dewberry.yandex.ru"
            }
        ],
        "versions": [
            "Yandex"
        ]
    }
}
```

