# BCWalker
A simple Python tool to find relations between given bitcoin addresses. The walker uses the api provided by Blockchain.com.

## Install
Just create a small Docker container with BCWalker in it:
- Install Docker
- `docker build -t bcwalker .`

## Run BCWalker
- `docker run bcwalker --start <first bc address> --end <last bc address>`

<i>For example: `docker run bcwalker --start bc1qv2347rjn8vrs4dzcznjr73q32za7u579zcsh7y --end bc1q9l9qzk2s9hvfwzz3mzucepamf5ue5m5rzvv9ut`</i>

By default, BCWalker results are visible on stdout. If you do not want this, just pass the silent flag:
- `docker run bcwalker --start <first bc address> --end <last bc address> -silent`

## Todo
- Execute more than one request every ten seconds (currently an api limitation).