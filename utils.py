import json
import requests
import threading


def get_address_info(address="0:efdc359a587e9d2677ca859a55507a3c46ba325b4ebd05ddf3738cbcb03b78f1"):
    search_url = "https://testnet-api.venomscan.com/v1/search"
    token_url = "https://testnet-tokens.venomscan.com/v1/balances"

    headers = {
        "content-type": "application/json",
    }

    search_payload = json.dumps({
        "query": address
    })

    token_payload = json.dumps({
        "ownerAddress": address,
        "limit": 1000,
        "offset": 0,
        "ordering": "amountdescending"
    })

    address_info = {
        "address": address,
        "balance": "",
        "tokens": []
    }

    def get_search_response():
        response_search = requests.post(
            search_url, data=search_payload, headers=headers).json()[0]
        address_info['balance'] = int(
            response_search['data']['balance']) / (10 ** 9)

    def get_token_response():
        response_tokens = requests.post(
            token_url, data=token_payload, headers=headers).json()
        for token in response_tokens['balances']:
            address_info['tokens'].append({
                "name": token['token'],
                "address": token['rootAddress'],
                "balance": token['amount']
            })

    # Create threads for making the API calls concurrently
    search_thread = threading.Thread(target=get_search_response)
    token_thread = threading.Thread(target=get_token_response)

    # Start both threads
    search_thread.start()
    token_thread.start()

    # Wait for both threads to finish
    search_thread.join()
    token_thread.join()

    return address_info


def get_address_info_graphql(address):
    reqUrl = "https://gql-testnet.venom.foundation/graphql"

    headersList = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "query": "query($address: String!){ blockchain{ account(address:$address){ info{ balance(format:DEC) } } }}",
        "variables": {
            "address": address
        }
    })

    response = requests.request(
        "POST", reqUrl, data=payload,  headers=headersList).json()
    balance = int(response["data"]["blockchain"]
                  ["account"]["info"]["balance"]) / (10 ** 9)
    address_info = {
        "address": address,
        "balance": balance,
    }
    return address_info


if __name__ == "__main__":
    # Call the function
    result = get_address_info_graphql('0:efdc359a587e9d2677ca859a55507a3c46ba325b4ebd05ddf3738cbcb03b78f1')
    print(result)
