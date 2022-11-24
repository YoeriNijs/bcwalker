import requests
import sys
import logging

from typing import Final
from threading import Thread

ADDRESS_ENDPOINT_PREFIX: Final = "https://blockchain.info/rawaddr/"
ADDRESS_TRANSACTIONS_ENDPOINT: Final = "https://api.haskoin.com/{}/address/{}/transactions/full"
TRANSACTION_ENDPOINT: Final = "https://api.haskoin.com/{}/transaction/{}"


class Walker:

    def __init__(self, start_address, end_addresses, bitcoin_type, depth=0):
        self.__start_address = start_address
        self.__end_addresses = end_addresses
        self.__depth = depth
        self.__bitcoin_type = bitcoin_type

    def walk_blockchain(self, checked_transactions=[]) -> None:
        url = ADDRESS_TRANSACTIONS_ENDPOINT.format(self.__bitcoin_type, self.__start_address)
        transactions = requests.get(url).json()
        for transaction in transactions:
            transaction_id = transaction['txid']
            logging.info(f"Checking transaction id: {transaction_id}")

            if transaction_id in checked_transactions:
                logging.debug(f"Transaction id {transaction_id} is in checked transactions, so skip")
                continue

            checked_transactions.append(transaction_id)

            self.__depth += 1

            outputs = transaction['outputs']
            for output in outputs:
                self.__check_output(output, transaction_id, checked_transactions)

    def __check_output(self, output, transaction_id, checked_transactions) -> None:
        output_address = output['address'].strip()
        if output_address == self.__start_address:
            logging.debug(f"Output address {output_address} is the same as the start address, so skip")
            return

        if output_address in self.__end_addresses:
            log = f"Relation found between {self.__start_address} and {output_address} with a depth of " \
                  f"{self.__depth}. Latest transaction hash for this relation: {transaction_id}. Details: " \
                  f"{TRANSACTION_ENDPOINT.format(self.__bitcoin_type, transaction_id)}"
            logging.info(log)
            sys.exit(log)

        thread = Thread(target=self.__threaded_walk,
                        args=(output_address, self.__end_addresses,
                              self.__bitcoin_type, self.__depth, checked_transactions))
        thread.start()
        thread.join()

    def __threaded_walk(self, output_address, end_addresses, bitcoin_type, depth, checked_transactions) -> None:
        walker = Walker(output_address, end_addresses, bitcoin_type, depth)
        walker.walk_blockchain(checked_transactions)
