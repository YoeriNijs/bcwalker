import argparse
import sys
import time
import logging
import os

from typing import Final
from exceptions.invalid_argument_exception import InvalidArgumentException
from util import is_empty
from walker import Walker

TRANSACTION_ENDPOINT: Final = "https://api.haskoin.com/{}/transaction/{}"


class BcWalker:

    def __init__(self):
        self.__log_file = f"{os.getcwd()}/results/bcwalker_log_{time.time()}.txt"
        logging.basicConfig(filename=self.__log_file,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        parser = argparse.ArgumentParser()
        parser.add_argument('-start', '--start')
        parser.add_argument('-end', '--end')
        parser.add_argument('-type', '--type')

        args = parser.parse_args()

        start_address = args.start
        if is_empty(start_address):
            raise InvalidArgumentException("Start address is invalid")
        self.__start_address = start_address.strip()

        end_addresses = args.end
        if is_empty(end_addresses):
            raise InvalidArgumentException("End address is invalid")
        splitted_end_addresses = end_addresses.split('|')
        self.__end_addresses = []
        for splitted_end_address in splitted_end_addresses:
            self.__end_addresses.append(splitted_end_address.strip())

        bitcoin_type = args.type
        if is_empty(bitcoin_type) or (bitcoin_type != 'btc' and bitcoin_type != 'bth'):
            raise InvalidArgumentException(f"Bitcoin type is invalid: should be 'btc' or 'bth', but is: {bitcoin_type}")
        self.__bitcoin_type = bitcoin_type

    def start(self) -> None:
        logging.info(f"Start analyzing blockchain for start '{self.__start_address}' and end '{self.__end_addresses}'...")
        try:
            walker = Walker(self.__start_address, self.__end_addresses, self.__bitcoin_type)
            walker.walk_blockchain()
        except Exception as e:
            logging.error(f"Cannot walk over start '{self.__start_address}' and end '{self.__end_addresses}':", e)
        logging.info(f"Done. No relations found.")
        sys.exit(f"Logfile written to {self.__log_file}")


# Fire it up!
app = BcWalker()
app.start()
