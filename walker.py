import requests
import time
import sys

from typing import Final
from exceptions.empty_content_exception import EmptyContentException
from util import is_empty

ADDRESS_ENDPOINT_PREFIX: Final = "https://blockchain.info/rawaddr/"
TRANSACTIONS_ENDPOINT_PREFIX: Final = ""


class Walker:

    def __init__(self, start_address, end_address, depth=0):
        self.__startAddress = start_address
        self.__endAddress = end_address
        self.__depth = depth

    def walk_blockchain(self, checked_transactions=[], offset=0):
        url = f"{ADDRESS_ENDPOINT_PREFIX}{self.__startAddress}?offset={offset}"
        start_address_response = requests.get(url)
        print(f"Url: {url}")

        data = start_address_response.json()
        if is_empty(data):
            raise EmptyContentException(f"Empty content found for address: {self.__startAddress}")

        transactions = data['txs']
        self.__verify_transactions(transactions, checked_transactions)

        number_transactions = data['n_tx']
        if offset < number_transactions:
            print(f"No relation found in this set of 50 transactions. Try older set of 50 transactions")
            offset += 50
            self.__api_wait()
            self.walk_blockchain(checked_transactions, offset)

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

            self.__api_wait()

            # Search end address in output addresses to verify whether there is a relation between them
            for output_address in output_addresses:
                self.__api_wait()
                walker = Walker(output_address, self.__endAddress, self.__depth)
                walker.walk_blockchain(checked_transactions)

    def __find_unique_output_addresses(self, outputs):
        output_addresses = []
        for output in outputs:
            output_address = output['addr']
            if output_address not in output_addresses:
                output_addresses.append(output_address)
        return output_addresses

    def __api_wait(self):
        print("Wait 10 seconds due to api limitations...")
        time.sleep(10)
