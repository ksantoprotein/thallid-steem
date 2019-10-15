# thallid-steem - Python Library for STEEM

Thallid-STEEM библиотека для блокчейна STEEM


# Installation

https://github.com/ksantoprotein/thallid-steem.git

# Documentation


# Usage examples

#### ***
``` python
from tsteembase.api import Api

b4 = Api()

```


#### Transfer
``` python
from tsteembase.api import Api

b4 = Api()


```

### Подключенные функции

``` python

b4.get_key_references(public_key)

b4.sm_token_transfer(to, amount, from_account, wif, asset = 'DEC')				#posting key

b4.ssc_token_transfer(to, amount, from_account, wif, asset = 'DEC', memo = '')	#active key

check_login(login)
is_login(login)

```

