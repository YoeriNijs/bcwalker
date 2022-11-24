# BCWalker
A simple Python tool to find relations between given Bitcoin classic and Bitcoin cash addresses. The walker uses the api provided by Haskoin.com.

## Install
Just create a small Docker container with BCWalker in it:
- Install Docker
- `docker build -t bcwalker .`

## Run BCWalker
To run BCWalker, you must provide at least three types of arguments: the start address, the end address and the bitcoin type (i.e. 'btc' or 'bth')

- `docker run bcwalker --start <first bc address> --end <last bc address> -type btc`

<i>For example: `docker run bcwalker --start bc1qv2347rjn8vrs4dzcznjr73q32za7u579zcsh7y --end bc1q9l9qzk2s9hvfwzz3mzucepamf5ue5m5rzvv9ut -type btc`</i>

It is also possible to search a relation for multiple addresses. Just add a pipe:
<i>For example: `docker run bcwalker --start <address 1> -end <address 2>|<address 3>|<address 4> -type btc`</i>
