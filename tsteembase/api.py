# -*- coding: utf-8 -*-

from pprint import pprint
import json
import math
import hashlib

from .rpc_client import RpcClient
from .broadcast import Tx
from .key import Key
from .storage import time_format, asset_precision, 			rus_d, rus_list, prefix

from datetime import datetime, timedelta
from time import sleep, time
from random import randint



class Api():

	app = 'thallid'

	def __init__(self, **kwargs):

		# Пользуемся своими нодами или новыми
		nodes = kwargs.pop("nodes", None)
		report = kwargs.pop("report", False)
		if nodes:
			self.rpc = RpcClient(nodes = nodes, report = report)
		else:
			self.rpc = RpcClient(report = report)

		#config_steem = self.rpc.call('get_config')
		#self.STEEMIT_BANDWIDTH_PRECISION = int(config_steem["STEEMIT_BANDWIDTH_PRECISION"])
		#self.chain_id = config_steem["STEEM_CHAIN_ID"]
		
		
		#chain_properties = self.rpc.call('get_chain_properties')
		#self.account_creation_fee = chain_properties["account_creation_fee"]
		#self.create_account_min_golos_fee = chain_properties["create_account_min_golos_fee"]
		#self.create_account_min_delegation = chain_properties["create_account_min_delegation"]
		
		# "account_creation_fee": "1.000 GOLOS",
		# "create_account_min_golos_fee": "0.030 GOLOS",
		# "create_account_min_delegation": "0.150 GOLOS",
		
		#self.resolve_url = resolve_url
		#self.rus_d = rus_d
		#self.asset_precision = asset_precision
		
		self.broadcast = Tx(self.rpc)
		self.finalizeOp = self.broadcast.finalizeOp
		
		self.key = Key()
		
	##### ##### ##### ##### #####
	
	def get_key_references(self, public_key):
			
		'''
		Позволяет узнать какому логину соответсвует публичный ключ
		#public_key = 'GLS6RGi692mJSNkdcVRunY3tGieJdTsa7AZeBVjB6jjqYg98ov5NL'
		Но не позволяет если есть авторити у аккаунта
		'''
		
		res = self.rpc.call('get_key_references', [public_key])
		if res:
			return(res[0])		# list
		else:
			#pprint(res)
			return False


	def check_login(self, login):

		if len(login) > 16:	## скорректировать под параметр блокчейна в инициализации
			return False
		if login[0] not in list('abcdefghijklmnopqrstuvwxyz'):
			return False
		for l in list(login[1:]):
			if l not in list('abcdefghijklmnopqrstuvwxyz0123456789.-'):
				return False
			
		return True

		
	def is_login(self, login):

		#Проверка существования логина
		account = self.rpc.call('get_accounts', [login])
		#account = self.get_accounts([login])
		if account:
			public_key = account[0]["memo_key"]
			return(public_key)
			
		return False
		
		
	def is_posting_key(self, login, public_key):
		account = self.rpc.call('get_accounts', [login])
		if account:
			keys = [key for key, auth in account[0]["posting"]["key_auths"]]
			if public_key in keys:
				return True
		return False

		
		
#############################	
		
		
	def get_transaction(self, trx_id):							# not work
		return(self.rpc.call('get_transaction', trx_id))
		
	def get_transaction_hex(self, trx_raw):						# not work
		return(self.rpc.call('get_transaction_hex', trx_raw))
		
	def get_accounts(self, accounts):
		return(self.rpc.call('get_accounts', accounts))

	def get_account(self, account):
		return(self.rpc.call('get_accounts', [account])[0])		### может быть ошибка если нет аккаунта
		
	def get_chain_properties(self):
		return(self.rpc.call('get_chain_properties'))
		
	def get_config(self):
		return(self.rpc.call('get_config'))
		
	def get_block(self, n):
		return(self.rpc.call('get_block', int(n)))
		
	def get_ops_in_block(self, n, ops = False):
		return(self.rpc.call('get_ops_in_block', int(n), ops))
		
	def get_dynamic_global_properties(self):			### доделать таймер

		# Returns the global properties
		for n in range(3):
			prop = self.rpc.call('get_dynamic_global_properties')
			if not isinstance(prop, bool):
				prop["now"] = datetime.strptime(prop["time"], time_format)
				for p in ["head_block_number", "last_irreversible_block_num"]:
					value = prop.pop(p)
					prop[p] = int(value)
				return(prop)
			sleep(3)
			
		return(False)
		
	def get_irreversible_block(self):
		info = self.get_dynamic_global_properties()
		if info:
			return(info["last_irreversible_block_num"])
		return False

	def get_head_block(self):
		info = self.get_dynamic_global_properties()
		if info:
			return(info["head_block_number"])
		return False
		
		

	##### ##### ##### ##### #####


	'''
	def vote(self, url, weight, voters, wif):
	
		#weight = -10000..10000
		#voters = list

		author, permlink = self.resolve_url(url)
		if not permlink:
			print('error url')
			return False
			
		ops = []
		for voter in voters:
			v = {
				"voter": voter,
				"author": author,
				"permlink": permlink,
				"weight": int(weight)
				}
			ops.append(['vote', v])
			
		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def transfer(self, to, amount, asset, from_account, wif, **kwargs):

		# to, amount, asset, from_account, [memo]
		memo = kwargs.pop('memo', '')

		ops = []
		t = {
			"from": from_account,
			"to": to,
			"amount": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			"memo": memo
			}
		ops.append(['transfer', t])
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def transfers(self, raw_ops, from_account, wif):

		# to, amount, asset, memo

		ops = []
		for op in raw_ops:
			to, amount, asset, memo = op
			t = {
				"from": from_account,
				"to": to,
				"amount": '{:.{precision}f} {asset}'.format(
							float(amount),
							precision = self.asset_precision[asset],
							asset = asset
							),
				"memo": memo
				}
			ops.append(['transfer', t])
		
		tx = self.finalizeOp(ops, wif)
		return tx


	def transfer_to_vesting(self, to, amount, from_account, wif, **kwargs):

		# to, amount, from_account
		asset = 'GOLOS'

		ops = []
		tv = {
			"from": from_account,
			"to": to,
			"amount": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			}
		ops.append(['transfer_to_vesting', tv])
		tx = self.finalizeOp(ops, wif)
		return tx


	def delegate_vesting_shares(self, delegatee, amount, delegator, wif, **kwargs):

		# делегируется не менее 0.010 GOLOS которые нужно перевести в GEST)
		vesting_shares = self.convert_golos_to_vests(amount)
		asset = 'GESTS'

		ops = []
		dvs = {
			"delegator": delegator,
			"delegatee": delegatee,
			"vesting_shares": '{:.{precision}f} {asset}'.format(
								vesting_shares,
								precision = self.asset_precision[asset],
								asset = asset
								),
			}
		ops.append(['delegate_vesting_shares', dvs])
		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def account_metadata(self, json_metadata, account, wif):
	
		ops = []
		jm = {
			"account": account,
			"json_metadata": json.dumps(json_metadata)
			}
		ops.append(['account_metadata', jm])

		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def follow(self, wtf, followings, followers, wif, **kwargs):
	
		# wtf = True (подписаться), False (отписаться), ignore - заблокировать
		# following - [] на кого подписывается
		# follower - [] кто подписывается
		
		if wtf == True and wtf != 'ignore':
			what = ['blog']						# подписаться
		elif wtf == 'ignore':
			what = ['ignore']					# заблокировать
		else:
			what = []							# отписаться

		ops = []
		for follower in followers:
			for following in followings:
			
				if follower != following:
					json_body = [
						'follow', {
							"follower": follower,
							"following": following,
							"what": what
							}
						]
				
					f = {
						"required_auths": [],
						"required_posting_auths": [follower],
						"id": 'follow',
						"json": json.dumps(json_body)
						}
					ops.append(['custom_json', f])

		tx = self.finalizeOp(ops, wif)
		return tx

		
	def post(self, title, body, author, wif, **kwargs):
	
		"""
		category = ''
		url = ''
		permlink = ''
		tags = []
		
		beneficiaries = 'login:10000'
		weight = 10000
		curation = max or int 5100..9000
		"""
	
		asset = 'GBG'
		
		parent_beneficiaries = 'thallid'
		category = kwargs.pop("category", parent_beneficiaries)
		app = kwargs.pop("app", parent_beneficiaries)
		beneficiaries = kwargs.pop("beneficiaries", False)
		
		if beneficiaries:
			a, w = beneficiaries.split(':')
			beneficiaries = [{"account": a, "weight": int(w)}]
		
		curation = kwargs.pop("curation", False)
		if curation == 'max':
			cur = self.get_curation_percent()
			if cur:
				curation = cur["max"]
			else:
				return False
		else:
			try:
				curation = int(curation)
			except:
				curation = False

		url = kwargs.pop("url", None)
		if url:
			parent_author, parent_permlink = self.resolve_url(url)			# comment
		else:
			parent_author, parent_permlink = '', category					# post
		
		permlink = kwargs.pop("permlink", None)
		if not permlink:
			# подготовить пермлинк самостоятельно
			permlink = ''.join([self.rus_d.get(s, s) for s in title.lower()]) + '-' + str( round(time()) )

		tags = kwargs.pop("tags", ['golos'])
		json_metadata = {"app": app, "tags": tags}
		
		max_accepted_payout = kwargs.pop("max_accepted_payout", 10000)
		allow_votes = kwargs.pop("allow_votes", True)
		allow_curation_rewards = kwargs.pop("allow_curation_rewards", True)
	
		ops = []
		c = {
				"parent_author": parent_author,
				"parent_permlink": parent_permlink,
				"author": author,
				"permlink": permlink,
				"title": title,
				"body": body,
				"json_metadata": json.dumps(json_metadata),
			}
		ops.append(['comment', c])
		
		extensions = []
		if beneficiaries:
			extensions.append([0, {"beneficiaries": beneficiaries}])
		if curation:
			extensions.append([2, {"percent": curation}])
		
		co = {
				"author": author,
				"permlink": permlink,
				"max_accepted_payout": '{:.{precision}f} {asset}'.format(
									float(max_accepted_payout),
									precision = self.asset_precision[asset],
									asset = asset
									),
				"percent_steem_dollars": 10000,
				"allow_votes": allow_votes,
				"allow_curation_rewards": allow_curation_rewards,
				"extensions": extensions
			}
		ops.append(['comment_options', co])

		tx = self.finalizeOp(ops, wif)
		return tx


	def replace(self, title, body, author, wif, **kwargs):
	
		parent_beneficiaries = 'thallid'
		category = kwargs.pop("category", parent_beneficiaries)

		url = kwargs.pop("url", None)
		if url:
			parent_author, parent_permlink = self.resolve_url(url)			# comment
		else:
			parent_author, parent_permlink = '', category					# post
		
		permlink = kwargs.pop("permlink", None)
		if not permlink:
			print('not permlink')
			return False

		app = kwargs.pop("app", parent_beneficiaries)
		tags = kwargs.pop("tags", ['golos'])
		json_metadata = {"app": app, "tags": tags}
	
		ops = []
		c = {
				"parent_author": parent_author,
				"parent_permlink": parent_permlink,
				"author": author,
				"permlink": permlink,
				"title": title,
				"body": body,
				"json_metadata": json.dumps(json_metadata),
			}
		ops.append(['comment', c])
		
		tx = self.finalizeOp(ops, wif)
		return tx

		
		

		
	def withdraw_vesting(self, amount, account, wif, **kwargs):

		# amount, account
		# понижается не менее 10х fee (сейчас 10 GOLOS которые нужно перевести в GEST)
		vesting_shares = self.convert_golos_to_vests(amount)
		asset = 'GESTS'

		ops = []
		wv = {
			"account": account,
			"vesting_shares": '{:.{precision}f} {asset}'.format(
								vesting_shares,
								precision = self.asset_precision[asset],
								asset = asset
								),
			}
		ops.append(['withdraw_vesting', wv])
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def account_create(self, login, password, creator, wif, **kwargs):

		create_with_delegation = False	###

		# login = account name must be at most 16 chars long, check if account already exists
		# roles = ["posting", "active", "memo", "owner"]
		paroles = self.key.get_keys(login, password)

		fee = self.account_creation_fee
		json_metadata = kwargs.pop("json_metadata", [])	###
			
		owner_key_authority = [ [paroles["public"]["owner"], 1] ]
		active_key_authority = [ [paroles["public"]["active"], 1] ]
		posting_key_authority = [ [paroles["public"]["posting"], 1] ]
		memo = paroles["public"]["memo"]
		
		owner_accounts_authority = []
		active_accounts_authority = [ [creator, 1] ]
		posting_accounts_authority = [ [creator, 1] ]
		#active_accounts_authority = []
		#posting_accounts_authority = []
		
		ops = []
		ca = {
			'fee': fee,
			'creator': creator,
			'new_account_name': login,
			'owner': {
				'weight_threshold': 1,
				'account_auths': owner_accounts_authority,
				'key_auths': owner_key_authority,
			},
			'active': {
				'weight_threshold': 1,
				'account_auths': active_accounts_authority,
				'key_auths': active_key_authority,
			},
			'posting': {
				'weight_threshold': 1,
				'account_auths': posting_accounts_authority,
				'key_auths': posting_key_authority,
			},
			'memo_key': memo,
			'json_metadata': json.dumps(json_metadata),
		}

		#if create_with_delegation:
		#	required_fee_vests = 0
		#	s["delegation"] = '%s GESTS' % required_fee_vests
		#	op = operations.AccountCreateWithDelegation(**s)
		#else:
		#	op = operations.AccountCreate(**s)
			
		ops.append(['account_create', ca])
		tx = self.finalizeOp(ops, wif)
		return tx
			

	def account_witness_proxy(self, account, proxy, wif):
	
		ops = []
		awp = {
			"account": account,
			"proxy": proxy,
			}
		ops.append(['account_witness_proxy', awp])
		tx = self.finalizeOp(ops, wif)
		return tx
		
	
	def repost(self, url, account, wif, **kwargs):	###
	
		#title = kwargs.pop("title", None)	
		#body = kwargs.pop("body", None)		
		#['title', 'body', 'json_metadata']
	
		author, permlink = resolve_url(url)
		ops = []
		json_body = [
			'reblog', {
				"account": account,
				"author": author,
				"permlink": permlink
				}
			]
	
		f = {
			"required_auths": [],
			"required_posting_auths": [account],
			"id": 'follow',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', f])

		tx = self.finalizeOp(ops, wif)
		return tx
		
	

	'''	
		
#############################

	'''
	def get_curation_percent(self):
		tx = self.rpc.call('get_witness_schedule')
		try:
			min = int(tx["median_props"]["min_curation_percent"])
			max = int(tx["median_props"]["max_curation_percent"])
			return({"min": min, "max": max})
		except:
			return False
			
		
	
	def account_update(self, new_password, account, old_password, **kwargs):

		create_with_delegation = False	###

		# login = account name must be at most 16 chars long, check if account already exists
		# roles = ["posting", "active", "memo", "owner"]
		old_paroles = self.key.get_keys(account, old_password)
		new_paroles = self.key.get_keys(account, new_password)

		json_metadata = kwargs.pop("json_metadata", {})	###
			
		owner_key_authority = [ [new_paroles["public"]["owner"], 1] ]
		active_key_authority = [ [new_paroles["public"]["active"], 1] ]
		posting_key_authority = [ [new_paroles["public"]["posting"], 1] ]
		memo = new_paroles["public"]["memo"]
		
		owner_accounts_authority = []
		#active_accounts_authority = [ [creator, 1] ]
		#posting_accounts_authority = [ [creator, 1] ]
		active_accounts_authority = []
		posting_accounts_authority = []
		
		ops = []
		au = {
			'account': account,
			'owner': {
				'weight_threshold': 1,
				'account_auths': owner_accounts_authority,
				'key_auths': owner_key_authority,
			},
			'active': {
				'weight_threshold': 1,
				'account_auths': active_accounts_authority,
				'key_auths': active_key_authority,
			},
			'posting': {
				'weight_threshold': 1,
				'account_auths': posting_accounts_authority,
				'key_auths': posting_key_authority,
			},
			'memo_key': memo,
			'json_metadata': json.dumps(json_metadata),
		}

			
		ops.append(['account_update', au])
		tx = self.finalizeOp(ops, old_paroles["private"]["owner"])
		return tx
	

	def get_account_history_comment(self, account, **kwargs):	###
	
		start_limit = kwargs.pop("start_limit", 1000)		#лимит одновременного запроса
		#age_max = kwargs.pop("age", 7*24*60*60)				#время в сек до какой операции сканировать

		raw_comment = []
					
		start_block, flag, n = 999999999, True, 0
		while flag:
			history = self.rpc.call('get_account_history', account, start_block, start_limit)

			for h in reversed(history):
				op = h[1]["op"][1]
				type_op = h[1]["op"][0]
				
				author = op.get("author")
				parent_author = op.get("parent_author")
				
				if type_op == 'comment' and author == account and parent_author:
				
					parent_permlink = op.get("parent_permlink")
					body = resolve_body_ru(op.get("body"))
					if body and parent_author not in ['upit']:
					
						if len(body) <= 50:
							with open(account + '.csv', 'a') as p:
								#p.write(';'.join([parent_author, parent_permlink, body, '\n']))
								p.write(';'.join([body, '\n']))
					
						#print(body)
						#input('next')

			start_block = h[0] - 1
			if start_block < start_limit:
				start_limit = start_block
			if start_limit <= 0:
				flag = False
			n += 1
			print(start_block, 'scan', n * start_limit)
	
		return(tx_vote)

		
	def get_account_count(self):	
		# Возвращает количество зарегестрированных пользователей
		return(int( self.rpc.call('get_account_count') ))

		
		
		
	def get_median_price(self):

		# Фид-прайс делегатов
		feed = self.rpc.call('get_feed_history')	# HF-18
		base = float(feed["current_median_history"]["base"].split()[0])
		quote = float(feed["current_median_history"]["quote"].split()[0])

		return(round(base / quote, asset_precision["GBG"]))
		

	def get_order_price(self):

		# усредненный прайс на внутренней бирже
		limit = 1
		feed = self.rpc.call('get_order_book', limit)
		ask = float(feed["asks"][0]["price"])
		bid = float(feed["bids"][0]["price"])

		return(round( (ask + bid) / 2, asset_precision["GBG"]))

		
	def convert_golos_to_vests(self, amount):
	
		info = self.get_dynamic_global_properties()
		if not info:
			print('error in global data')
			return False

		asset = 'GESTS'
		vests = round(float(amount) / info["golos_per_vests"], asset_precision[asset])
		
		return vests
		
		
	def get_accounts(self, logins, **kwargs):
	
		"""
		Перерасчитываются некоторые параметры по аккаунту
		"voting_power" - 1..10000 реальная батарейка
		"golos_power" - сила голоса с учетом делегирования
		"rshares" - сколько добавится шаров в пост при 100% батарейке
		"GOLOS", "GBG" - ликвидные токены
		"new_post_limit" - сколько постов можно опубликовать
		"new_post_time" - сколько осталось времени в минутах до публикации без штрафа
		"bandwidth" = {
			"avail" - всего доступно в кБ
			"used_forum" - использовано в кБ
			"used_market" - использовано в кБ
			"free_forum" - доступно в кБ
			"free_market" - доступно в кБ
			}
		"value" = {"GOLOS", "GBG"} - цена апвота по внутренней бирже
		"order" = {"GOLOS", "GBG"} - цена апвота по медиане
		"rating" = репутация в десятичном виде
		"""
		
		add_follow = kwargs.pop("follow", False)	###

		accounts = self.rpc.call('get_accounts', logins)
		median_price = self.get_median_price()
		order_price = self.get_order_price()

		info = self.get_dynamic_global_properties()
		if not info:
			print('error in global data')
			return False
		
		for account in accounts:

			# Определение реальной батарейки 1-10000

			VP = float(account["voting_power"])
			last_vote_time = datetime.strptime(account["last_vote_time"], time_format)
			age = (info["now"] - last_vote_time).total_seconds() / 1
			actualVP = VP + (10000 * age / 432000)

			if actualVP > 10000:
				account["voting_power"] = 10000
			else:
				account["voting_power"] = round(actualVP)

				
			# Определение golos_power (SP)

			vests = float(str(account["vesting_shares"]).split()[0])
			delegated = float(str(account["delegated_vesting_shares"]).split()[0])
			received = float(str(account["received_vesting_shares"]).split()[0])
			account["golos_power"] = round( (vests + received - delegated) * info["golos_per_vests"], asset_precision["GOLOS"])

			
			# Определение rshares

			vesting_shares = int(1e6 * account["golos_power"] / info["golos_per_vests"])

			max_vote_denom = info["vote_regeneration_per_day"] * (5 * 60 * 60 * 24) / (60 * 60 * 24)
			used_power = int((account["voting_power"] + max_vote_denom - 1) / max_vote_denom)
			rshares = ((vesting_shares * used_power) / 10000)
			account["rshares"] = round(rshares)
			account["add_reputation"] = round(rshares / 64)

			
			# Определение стоимости апвота

			value_golos = round(account["rshares"] * info["total_reward_fund_steem"] / info["total_reward_shares2"], asset_precision["GOLOS"])
			value_gbg = round(value_golos * median_price, asset_precision["GBG"])
			order_gbg = round(value_golos * order_price, asset_precision["GBG"])
			account["value"] = {"GOLOS": value_golos, "GBG": value_gbg}
			account["order"] = {"GOLOS": value_golos, "GBG": order_gbg}

			
			# Определение ликвидных токенов
			
			account["GOLOS"] = float(str(account["balance"]).split()[0])
			account["GBG"] = float(str(account["sbd_balance"]).split()[0])

			
			# Определение post_bandwidth
			
			account["new_post_time"] = 0	# minutes
			minutes_per_day = 24 * 60
			last_post_time = datetime.strptime(account["last_root_post"], time_format)
			age_after_post = (info["now"] - last_post_time).total_seconds() / 60		# minutes
			if age_after_post >= minutes_per_day:
				account["new_post_limit"] = 4
			else:
				new_post_bandwidth = int((((minutes_per_day - age_after_post) / minutes_per_day) * account["post_bandwidth"]) + 10000)
				
				if new_post_bandwidth > 40000:
					account["new_post_limit"] = 0
					account["new_post_time"] =  round(minutes_per_day - ((40000 - 10000) / (new_post_bandwidth - 10000)) * minutes_per_day)
				else:
					account["new_post_limit"] = int(4 - (new_post_bandwidth // 10000))

					
			# Определение update_account_bandwidth
			
			average_forum_bandwidth = int(account["average_bandwidth"])
			average_market_bandwidth = int(account["average_market_bandwidth"])

			info["max_virtual_bandwidth"] = int(info["max_virtual_bandwidth"]) / self.STEEMIT_BANDWIDTH_PRECISION
			
			average_seconds = 7 * 24 * 60 * 60
			
			last_forum_time = datetime.strptime(account["last_bandwidth_update"], time_format)
			last_market_time = datetime.strptime(account["last_market_bandwidth_update"], time_format)

			age_after_forum = int((info["now"] - last_forum_time).total_seconds() / 1)			# seconds
			age_after_market = int((info["now"] - last_market_time).total_seconds() / 1)		# seconds
			
			if age_after_forum >= average_seconds:
				new_account_forum_average_bandwidth = 0
			else:
				new_account_forum_average_bandwidth = ((average_seconds - age_after_forum) * average_forum_bandwidth) / average_seconds
			
			if age_after_market >= average_seconds:
				new_account_market_average_bandwidth = 0
			else:
				new_account_market_average_bandwidth = ((average_seconds - age_after_market) * average_market_bandwidth) / average_seconds
			
			avail = vesting_shares * info["max_virtual_bandwidth"]
			used_forum = new_account_forum_average_bandwidth * info["total_vesting_shares"]
			used_market = new_account_market_average_bandwidth * info["total_vesting_shares"]
			
			used_kb_forum = round(new_account_forum_average_bandwidth / self.STEEMIT_BANDWIDTH_PRECISION / 1024, 3)
			used_kb_market = round(new_account_market_average_bandwidth / self.STEEMIT_BANDWIDTH_PRECISION / 1024 , 3)
			avail_kb = round(vesting_shares / info["total_vesting_shares"] * info["max_virtual_bandwidth"] / self.STEEMIT_BANDWIDTH_PRECISION / 1024, 3)
			
			account["bandwidth"] = {
							"avail": avail_kb,
							"used_forum": used_kb_forum,
							"used_market": used_kb_market,
							"free_forum": round(avail_kb - used_kb_forum, 3),
							"free_market": round(avail_kb - used_kb_market, 3),
							}

			# Определение подписчиков
			
			#if add_follow:
			#	f = self.get_follow(account["name"])
			#	account["follower_count"] = f["follower_count"]
			#	account["following_count"] = f["following_count"]
			#	account["follower"] = f["follower"]
			#	account["following"] = f["following"]
			
			
			# Определение репутации
			#reputation, // <- Поле отсутствует, если выключен плагин follow

			rep = account.get("reputation", None)
			if not rep:
				rep = 0
			else:
				rep = int(rep)
			
			if rep == 0:
				account["rating"] = 25
			else:
				score = (math.log10(abs(rep)) - 9) * 9 + 25
				if rep < 0:
					score = 50 - score
				account["rating"] = round(score, 3)

		return(accounts)
		
		
	def get_all_accounts(self):
	
		n = self.get_account_count()
		limit = 1000
		print('find', n, 'accounts')
		
		accounts_dict = {}
		start_login = 'a'
		while True:
			print(start_login)
			logins = self.rpc.call('lookup_accounts', start_login, limit)
			
			if len(logins) == 1 and logins[0] == start_login:
				accounts = self.get_accounts(logins)
				for account in accounts:
					accounts_dict[account["name"]] = account
				break

			accounts = self.get_accounts(logins[:-1])
			for account in accounts:
				accounts_dict[account["name"]] = account

			start_login = logins[-1:][0]
	
		return accounts_dict

		
	def get_follow(self, account):
	
		follow = {"follower": [], "following": []}
		account_follow = self.rpc.call('get_follow_count', account)
		
		#account_follow["follower_count"]
		#account_follow["following_count"]
		
		start_follower = 'a'
		while True:
			tx = self.rpc.call('get_followers', account, start_follower, 'blog', 1000)
			
			if len(tx) == 1 and tx[0]["follower"] == start_follower:
				follow["follower"].append(start_follower)
				break

			for line in tx[:-1]:
				follow["follower"].append(line["follower"])
			start_follower = tx[-1:][0]["follower"]
			
		start_follower = 'a'
		while True:
			tx = self.rpc.call('get_following', account, start_follower, 'blog', 100)
			
			if len(tx) == 1 and tx[0]["following"] == start_follower:
				follow["following"].append(start_follower)
				break

			for line in tx[:-1]:
				follow["following"].append(line["following"])
			start_follower = tx[-1:][0]["following"]

		account_follow["follower"] = follow["follower"]
		account_follow["following"] = follow["following"]

		return account_follow

		

	def get_account_reputations(self, account):
	
		# Определяем репутацию аккаунта
		reputations = self.rpc.call('get_account_reputations', [account])
		rep = int(reputations[0]["reputation"])
		if rep == 0:
			reputation = 25
		else:
			score = (math.log10(abs(rep)) - 9) * 9 + 25
			if rep < 0:
				score = 50 - score
			reputation = round(score, 3)
			
		return(reputation)


		
	def get_content(self, url, **kwargs):
	
		vote_limit = str(kwargs.pop("vote_limit", 0))
	
		author, permlink = resolve_url(url)
		user_post = self.rpc.call('get_content', author, permlink, vote_limit)
		
		return user_post

		
		
		
	def get_ticker(self):
		ticker = self.rpc.call('get_ticker')
		try:
			t = {"bid": round(float(ticker["highest_bid"]), 6), "ask": round(float(ticker["lowest_ask"]), 6)}
		except:
			return False
		
		return(t)

		
	def get_tickers(self):
		ticker = self.rpc.call('get_ticker')
		try:
			bid = float(ticker["highest_bid"])
			ask = float(ticker["lowest_ask"])
			
			t = {"GOLOS_GBG": {"bid": bid, "ask": ask}, "GBG_GOLOS": {"bid": 1 / ask, "ask": 1 / bid} }
		except:
			return False
		
		return(t)
	
		
	'''	
	
	
##### ##### SteemMonsters ##### #####
	
class SteemMonsters(Api):

	app = 'thallid'

	def __init__(self, **kwargs):

		# Пользуемся своими нодами или новыми
		nodes = kwargs.pop("nodes", None)
		report = kwargs.pop("report", False)
		if nodes:
			self.rpc = RpcClient(nodes = nodes, report = report)
		else:
			self.rpc = RpcClient(report = report)


		self.broadcast = Tx(self.rpc)
		self.finalizeOp = self.broadcast.finalizeOp
		self.key = Key()	
		
		
	def sm_token_transfer(self, to, amount, from_account, wif, asset = 'DEC', active = False):
	
		sign_active = [from_account] if active else []
		sign_posting = [] if active else [from_account]

		ops = []
		json_body = {
						"to": to,
						"qty": str(amount),
						"token": asset,
						"type": 'withdraw',
						"app": self.app,
					}
	
		op = {
			"required_auths": sign_active,
			"required_posting_auths": sign_posting,
			"id": 'sm_token_transfer',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx

		
	def sm_find_match(self, login, wif):
	
		ops = []
		json_body = {
						"match_type": 'Ranked',
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_find_match',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx

		
	def sm_submit_team(self, combo, id, login, wif):
	
		m = hashlib.md5()
		secret = '12345'
		m.update((','.join(combo + [secret])).encode("utf-8"))
		team_hash = m.hexdigest()
		
		ops = []
		json_body = {
						"summoner": combo[0],
						"monsters": combo[1:],
						"trx_id": id,
						"app": self.app,
						"secret": secret,
						"team_hash": team_hash,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_submit_team',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def sm_gift_cards(self, to, cards, login, wif):
	
		ops = []
		json_body = {
						"to": to,
						"cards": cards,
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_gift_cards',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx

		
	def sm_claim_reward(self, id, login, wif):
	
		ops = []
		json_body = {
						"type": 'quest',
						"quest_id": id,
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_claim_reward',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		
	
	def sm_claim_reward_season(self, id, login, wif):
	
		ops = []
		json_body = {
						"type": 'league_season',
						"season": id,
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_claim_reward',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		
	
	def sm_start_quest(self, login, wif):
	
		ops = []
		json_body = {
						"type": 'daily',
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_start_quest',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx
	

	def sm_refresh_quest(self, login, wif):
	
		ops = []
		json_body = {
						"type": 'daily',
						"app": self.app,
					}
	
		op = {
			"required_auths": [],
			"required_posting_auths": [login],
			"id": 'sm_refresh_quest',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx
	

	def ssc_token_transfer(self, to, amount, from_account, wif, asset = 'DEC', memo = ''):
	
		ops = []
		json_body = {
						"contractName": 'tokens',
						"contractAction": 'transfer',
						"contractPayload": {
											"to": to,
											"quantity": str(amount),
											"symbol": asset,
											"memo": memo,
											"app": self.app,
											}
					}
	
		op = {
			"required_auths": [from_account],		#видимо потребуется активный ключ (((
			"required_posting_auths": [],
			"id": 'ssc-mainnet1',
			"json": json.dumps(json_body)
			}
		ops.append(['custom_json', op])

		tx = self.finalizeOp(ops, wif)
		return tx

		
#----- common def -----
def resolve_url(url):

	if '#' in url:
		url = url.split('#')[1]
	if '@' in url:
		url = url.split('@')[1]

	if url[-1:] == '/':
		url = url[:-1]

	if url.count('/') != 1:
		return([False, False])
	else:
		return(url.split('/'))
		
		
def resolve_body_ru(body):
	
	raw_body = []
	body = body.replace('#', '')
	body = body.replace('\n', '#')
	for s in body:
		if s in rus_list:
			raw_body.append(s)
		elif s == '#':
			#raw_body.append('\n')
			raw_body.append('#')
			
	if len(raw_body) == 0:
		return False
		
	return(''.join(raw_body))

