import json
import time
from jarjar import jarjar
from itertools import product
import requests

TEST_NUMBER = 576  # where to start tests

'''
TESTS

1. All combos of arguments that i can think of
2. Provided at init or at request time
3. To either the attach or test methods
'''

# define a jarjar to get the defaults
jj = jarjar()

# timeout between requests in case slack is watching that sort of thing.
TIMEOUT = 2.0

# define test space
MESSAGES = ['Test', '', None, False, True, 123, dict(a=1), u'Unicode \ua000', jj.default_message]
ATTACHES = ['Test', '', None, False, True, 123, dict(a=1), u'Unicode \ua000']
CHANNELS = [jj.default_channel, '#jarjar', None, '', 'jarjar', 'undefined_channel']
WEBHOOKS = [jj.default_webhook, '', None, 'https://invalid_url.com']
METHODS = ['text', 'attach']
AT_INIT = [True, False]

def Test(message, attach, channel, webhook, method, at_init):
	"""Perform a test."""

	# print the test
	print('-----------------TEST %d-----------------' % TEST_NUMBER)
	print(
		' message %r\n attach %r\n channel %r\n webhook %r\n method %r\n at_init\t%r' %
		(message, attach, channel, webhook, method, at_init)
	)

	if at_init:
		jj = jarjar(message=message, channel=channel, webhook=webhook)
	else:
		jj = jarjar()

	method = getattr(jj, method)

	request_sent = False
	try:
		res = method(message=message, attach=attach, channel=channel, webhook=webhook)
		time.sleep(TIMEOUT)
		request_sent = True
	except TypeError:
		# expected if:
		# - attach is not a dict
		if not isinstance(attach, dict):
			pass
		else:
			raise
	except NameError:
		raise
	except requests.exceptions.ConnectionError:
		# expected if
		# - the webhook is not valid
		if webhook=='https://invalid_url.com':
			pass
		else:
			raise

	if not request_sent:
		return

	# bad status expected if:
	# - undefined channel
	if res.status_code != 200:
		if channel == 'undefined_channel':
			pass
		else:
			raise Exception('Bad status for unknown reason.')

	data = json.loads(res.request.body)
	url = res.url

	# print dir(res)
	# print data, url

	# check webhook
	if webhook:
		assert url == webhook
	else:
		assert url == jj.default_webhook

	# check channel
	if channel:
		assert data['channel'] == channel
	else:
		assert data['channel'] == jj.default_channel

	# check message
	if message:
		assert data['text'] == message
	elif jj.default_message:
		assert data['text'] == jj.default_message
	else:
		assert data['text'] == jj._final_default_message

	# check attach
	if attach:
		print data
		lll

# iterate thbrough all combos of args and test each.
combos = product(MESSAGES, ATTACHES, CHANNELS, WEBHOOKS, METHODS, AT_INIT)

for args in list(combos)[TEST_NUMBER:]:
	Test(*args)
	TEST_NUMBER +=1
