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


check_login(login)
is_login(login)

```

#### SteemMonsters
``` python
from tsteembase.api import SteemMonsters

sm = SteemMonsters()

# Tokens

sm.ssc_token_transfer(to, amount, from_account, wif, memo = '')
sm.sm_token_transfer(to, amount, from_account, wif)

# Battle

tx = sm.sm_find_match(login, wif)
id = tx["id"]

combo = [summoner, monsters]
sm.sm_submit_team(combo, id, login, wif)

# Cards

cards = [cards_ids]
sm.sm_gift_cards(to, cards, login, wif)

# Reward

sm.sm_claim_reward(id, login, wif)
sm.sm_claim_reward_season(id, login, wif)
sm.sm_start_quest(login, wif)
sm.sm_refresh_quest(login, wif)

```

