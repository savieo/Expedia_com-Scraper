from useragent import get_ua
# REDIS_URL = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 1

# TIME_ZONE = 'UTC'
# RESUME = False
MAX_RETRY = 30
# UNIQUE_CHECK = True
THREADS = 2

# REQUEST_PROCESSOR = 'dragline.http:RequestProcessor'

DEFAULT_REQUEST_ARGS = {
	# 'allow_redirects': True,
	# 'auth': None,
	# 'cert': None,
	# 'cookies': None,
	# 'data': None,
	# 'files': None,
    # 'headers': {'User-Agent' : get_ua()},
	'headers':{'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			   'accept-encoding': 'gzip, deflate, br',
			   'accept-language': 'en-US,en;q=0.9',
			   'cache-control': 'max-age=0',
			   'upgrade-insecure-requests': '1',
			   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'},

	# 'json': None,
	# 'method': None,
	# 'params': None,
	# 'proxies': {'http': 'http://172.16.244.221:20017', 'https': 'http://172.16.244.221:20017'},
	# 'stream': False,
	'timeout': 100,
	# 'verify': False
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
		},
	},
	'handlers': {
		'default': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		}
	},
	'loggers': {
		'': {
			'handlers': ['default'],
			'level': 'INFO',
			'propagate': False
		},
		'dragline': {
			'handlers': ['default'],
			'level': 'INFO',
			'propagate': False
		},
		'2363_Expedia_com': {
			'handlers': ['default'],
			'level': 'INFO',
			'propagate': False
		}
	}
}

try:
	from local_settings import *
except:
	pass
