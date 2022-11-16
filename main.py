import argparse
import sys
import time

from exceptions.invalid_argument_exception import InvalidArgumentException
from util import is_empty
from walker import Walker


class BcWalker:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-start', '--start')
        parser.add_argument('-end', '--end')
        parser.add_argument('-silent', action='store_true')

        args = parser.parse_args()

        start_address = args.start
        if is_empty(start_address):
            raise InvalidArgumentException("Start address is invalid")
        self.__start_address = start_address

        end_address = args.end
        if is_empty(end_address):
            raise InvalidArgumentException("End address is invalid")
        self.__end_address = end_address

        is_silent = args.silent
        self.__is_silent = False \
            if is_empty(is_silent) \
            else True

    def start(self):
        print(f"Running BcWalker in {'silent' if self.__is_silent else 'verbose'} mode")

        log_file_name = f"results/log_{time.time()}.txt"
        if self.__is_silent:
            with open(log_file_name, 'w') as lf:
                sys.stdout = lf
                self.__run_walker()
                sys.exit(f"Done. No relations found. See logs for details: {log_file_name}")
        else:
            self.__run_walker()
            sys.exit(f"Done. No relations found.")

    def __run_walker(self):
        print(f"Start analyzing blockchain for start '{self.__start_address}' and end '{self.__end_address}'...")
        try:
            walker = Walker(self.__start_address, self.__end_address)
            walker.walk_blockchain()
        except Exception as e:
            sys.exit(f"Cannot walk over start '{self.__start_address}' and end '{self.__end_address}':", e)


# Fire it up!
app = BcWalker()
app.start()
