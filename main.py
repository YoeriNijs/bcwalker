import argparse

from exceptions.invalid_argument_exception import InvalidArgumentException
from util import is_empty
from walker import Walker

parser = argparse.ArgumentParser()
parser.add_argument('-start', '--start')
parser.add_argument('-end', '--end')

args = parser.parse_args()
start_address = args.start
end_address = args.end

if is_empty(start_address):
    raise InvalidArgumentException("Start address is invalid")

if is_empty(end_address):
    raise InvalidArgumentException("End address is invalid")

try:
    walker = Walker(start_address, end_address)
    walker.walk_blockchain()

except Exception as e:
    print(f"Cannot walk over start '{start_address}' and end '{end_address}':", e)
