import requests
from typing import Optional
from pydantic import EmailStr
from eth_account import Account
from eth_account.messages import encode_defunct
from time import time


class Client():

    def __init__(
        self,
        api_key: Optional[str] = None
    ):
        self.user_id = api_key.split('--')[0]
        self.api_key = api_key
        self.endpoint = 'https://api.xentropy.co'

    @classmethod
    def create_account(cls, user_id: str, email: EmailStr):
        response = requests.post(
            'https://api.xentropy.co/user',
            json={
                'email': email,
                'user_id': user_id
            }
        ).json()

        return response

    def reset_api_key(self, email: EmailStr):
        response = requests.post(
            f'{self.endpoint}/reset_api_key',
            json={
                'email': email,
                'user_id': self.user_id
            }
        ).json()

        return response

    def summary(self):
        response = requests.get(
            f'{self.endpoint}/user',
            headers={
                'Api-Key': self.api_key
            }
        ).json()

        return response

    def modify_tool(self, tool, key, value):
        response = requests.put(
            f'{self.endpoint}/tool/{tool}',
            json={key: value},
            headers={
                'Api-Key': self.api_key
            }
        )
        return response.json()

    def delete_tool(self, tool):
        response = requests.delete(
            f'{self.endpoint}/tool/{tool}',
            headers={
                'Api-Key': self.api_key
            }
        )
        return response.json()

    def register_ethereum_address(self, account: Account):
        timestamp = int(time())
        message = f'{self.user_id}-{timestamp}'
        message_hash = encode_defunct(text=message)
        signature = account.sign_message(message_hash).signature.hex()

        response = requests.post(
            f'{self.endpoint}/register_ethereum_address',
            json={
                'user_id': self.user_id,
                'address': account.address,
                'timestamp': timestamp,
                'signature': signature
            },
            headers={
                'Api-Key': self.api_key
            }
        )
        return response

    def stable_coin_payout(self, amount: int, address: str, stable_coin: str):
        response = requests.post(
            f'{self.endpoint}/stable_coin_payout',
            json={
                'amount': amount,
                'address': address,
                'stable_coin': stable_coin,
            },
            headers={
                'Api-Key': self.api_key
            }
        ).json()

        return response

    def transfer_payout_to_balance(self, amount: int):
        response = requests.post(
            f'{self.endpoint}/balance_transfer',
            params={
                'amount': amount,
            },
            headers={
                'Api-Key': self.api_key
            }
        ).json()

        return response

    def log(
        self,
        parent_id: Optional[str] = None,
        tool: Optional[str] = None,
        start_after: Optional[float] = None,
        limit: int = 8,
    ):
        headers = {
            'Api-Key': self.api_key
        }

        if parent_id != None:
            response = requests.get(
                f'{self.endpoint}/log/{parent_id}',
                headers=headers,
            )
            return response.json()

        else:
            response = requests.get(
                f'{self.endpoint}/log',
                headers=headers,
                params={
                    'tool_id': tool,
                    'start_after': start_after,
                    'limit': limit,
                }
            )
            return response.json()
