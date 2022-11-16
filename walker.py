import requests
import time
import sys

from typing import Final
from exceptions.empty_content_exception import EmptyContentException
from util import is_empty

ADDRESS_ENDPOINT_PREFIX: Final = "https://blockchain.info/rawaddr/"
TRANSACTIONS_ENDPOINT_PREFIX: Final = ""


class Walker:

    def __init__(self, start_address, end_address, depth = 0):
        self.__startAddress = start_address
        self.__endAddress = end_address
        self.__depth = depth

    def walk_blockchain(self, checked_transactions=[]):
        start_address_response = requests.get(f"{ADDRESS_ENDPOINT_PREFIX}{self.__startAddress}")
        start_address_content = start_address_response.json()
        if is_empty(start_address_content):
            raise EmptyContentException(f"Empty content found for address: {self.__startAddress}")

        transactions = self.__find_transactions_for_address(start_address_content)
        self.__verify_transactions(transactions, checked_transactions)

    def __verify_transactions(self, transactions, checked_transactions):
        for transaction in transactions:
            transaction_hash = transaction['hash']
            if transaction_hash in checked_transactions:
                continue
            checked_transactions.append(transaction_hash)

            outputs = transaction['out']
            output_addresses = self.__find_unique_output_addresses(outputs)
            if self.__endAddress in output_addresses:
                sys.exit(f">> Relation found between {self.__startAddress} and {self.__endAddress} with a depth of "
                         f"{self.__depth}. Latest transaction hash for this relation: {transaction_hash}: "
                         f"https://www.blockchain.com/btc/tx/{transaction_hash}")
            else:
                print(f"No relation found in transaction hash {transaction_hash}")

            if self.__startAddress in output_addresses:
                # We are not interested outputs that are the same as the start addresses, since we only want
                # to verify the end address
                continue

            # Search end address in output addresses to verify whether there is a relation between them
            for output_address in output_addresses:
                print("Wait 10 seconds due to api limitations...")
                time.sleep(10)

                walker = Walker(output_address, self.__endAddress, self.__depth)
                walker.walk_blockchain(checked_transactions)

            exit(f">> Done. No relation found between {self.__startAddress} and {self.__endAddress}")

    def __find_transactions_for_address(self, data):
        address = data['address']
        transactions = data['txs']
        if is_empty(transactions):
            raise Exception(f"Empty transactions for address: {address}")
        number_transactions = data['n_tx']
        if number_transactions > 50:
            # For now, we limit the scope. Ultimately, we want to pass the offset, so we can walk over more transactions
            print(f"Address {address} contains more than 50 transactions. Limit scope to recent 50 transactions")
        return transactions

    def __find_unique_output_addresses(self, outputs):
        output_addresses = []
        for output in outputs:
            output_address = output['addr']
            if output_address not in output_addresses:
                output_addresses.append(output_address)
        return output_addresses
