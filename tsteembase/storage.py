# -*- coding: utf-8 -*-

# https://steem.esteem.ws/												+ Interactive Steem API
# https://www.steem.center/index.php?title=Public_Websocket_Servers		+ Public Websocket Servers
# https://geo.steem.pl/													+ Steem API nodes ordered from the nearest to farthest

# https://developers.steem.io/apidefinitions/ 							+ Steem Developer Portal - API Definitions
# https://developers.steem.io/tutorials-recipes/plugin-and-api-list		+ Steem Developer Portal

# https://github.com/steemit/steem-js									+

# https://steemnow.com/
# https://status.steemnodes.com/										- steem seed nodes



nodes = [
		'https://api.steemit.com',
		'https://steemd.privex.io',
		'https://anyx.io',
		'https://steemd.minnowsupportproject.org',
		'https://rpc.usesteem.com',				# https://developers.steem.io/apidefinitions/
		#'https://api.steemitdev.com',
		#'https://api.steemitstage.com',
		
		#'https://api.steem.house',
		#'https://appbasetest.timcliff.com',
		
		
		#'https://rpc.steemviz.com',
		#'https://rpc.buildteam.io',
		#'https://rpc.steemliberator.com',
		]

prefix = 'STM'
chain_id = '0000000000000000000000000000000000000000000000000000000000000000'		# GOLOS
time_format = '%Y-%m-%dT%H:%M:%S'
time_format_utc = '%Y-%m-%dT%H:%M:%S%Z'
expiration = 60

asset_precision = {
					"STEEM": 3,
					"VESTS": 6,
					"SBD": 3,
					}

# Список транзакций по порядку для каждого БЧ он свой
# https://github.com/steemit/steem-js/blob/master/src/auth/serializer/src/ChainTypes.js
operations = {
				"vote": 0,
				"comment": 1,
				"transfer": 2,
				"transfer_to_vesting": 3,
				"withdraw_vesting": 4,
				"limit_order_create": 5,
				"limit_order_cancel": 6,
				"feed_publish": 7,
				"convert": 8,
				"account_create": 9,
				"account_update": 10,
				"witness_update": 11,
				"account_witness_vote": 12,
				"account_witness_proxy": 13,
				"pow": 14,
				"custom": 15,
				"report_over_production": 16,
				"delete_comment": 17,
				"custom_json": 18,
				"comment_options": 19,
				"set_withdraw_vesting_route": 20,
				"limit_order_create2": 21,
				"claim_account": 22,
				"create_claimed_account": 23,
				"request_account_recovery": 24,
				"recover_account": 25,
				"change_recovery_account": 26,
				"escrow_transfer": 27,
				"escrow_dispute": 28,
				"escrow_release": 29,
				"pow2": 30,
				"escrow_approve": 31,
				"transfer_to_savings": 32,
				"transfer_from_savings": 33,
				"cancel_transfer_from_savings": 34,
				"custom_binary": 35,
				"decline_voting_rights": 36,
				"reset_account": 37,
				"set_reset_account": 38,
				"claim_reward_balance": 39,
				"delegate_vesting_shares": 40,
				"account_create_with_delegation": 41,
				"witness_set_properties": 42,
				"account_update2": 43,
				"create_proposal": 44,
				"update_proposal_votes": 45,
				"remove_proposal": 46,
				"fill_convert_request": 47,
				"author_reward": 48,
				"curation_reward": 49,
				"comment_reward": 50,
				"liquidity_reward": 51,
				"interest": 52,
				"fill_vesting_withdraw": 53,
				"fill_order": 54,
				"shutdown_witness": 55,
				"fill_transfer_from_savings": 56,
				"hardfork": 57,
				"comment_payout_update": 58,
				"return_vesting_delegation": 59,
				"comment_benefactor_reward": 60,
			}

### OLD ver
#op_names = []
#: assign operation ids
#operations = dict(zip(op_names, range(len(op_names))))



rus_d = {
		'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
		'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
		'й': 'ij', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
		'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
		'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'cz', 'ч': 'ch',
		'ш': 'sh', 'щ': 'shch', 'ъ': 'xx', 'ы': 'y', 'ь': 'x',
		'э': 'ye', 'ю': 'yu', 'я': 'ya',

		'А': "A", 'Б': "B", 'В': "V", 'Г': "G", 'Д': "D",
		'Е': "E", 'Ё': "yo", 'Ж': "ZH", 'З': "Z", 'И': "I",
		'Й': "IJ", 'К': "K", 'Л': "L", 'М': "M", 'Н': "N",
		'О': "O", 'П': "P", 'Р': "R", 'С': "S", 'Т': "T",
		'У': "U", 'Ф': "F", 'Х': "KH", 'Ц': "CZ", 'Ч': "CH",
		'Ш': "SH", 'Щ': "SHCH", 'Ъ': "XX", 'Ы': "Y", 'Ь': "X",
		'Э': "YE", 'Ю': "YU", 'Я': "YA",
		' ': "-", '.': "-", ',': "-", ':': "-", ';': "-", 
		'(': "", ')': "", '!': "", '?': "", '"': "", "'": "", '[': "", ']': "", '|': "", '/': "", '_': "", '@': "", '$': "",  
		}

rus_list = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя., '