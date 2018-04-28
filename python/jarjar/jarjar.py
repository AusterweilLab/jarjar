import requests
import json
import time
import os
import imp
import warnings

# a warning for if the defaultiest message is used
_no_message_warn = (
	'''
	Slow down cowboy! You didn't provide a message and there is
	no default in your .jarjar, so I'll just wing it.
	'''
	.strip()
	.replace('\n', ' ')
	.replace('\t', ' ')
	.replace('  ', ' ')
)


class jarjar():

	def __init__(self, channel=None, webhook=None, message=None):

		# read config file, set defaults
		self._read_config()
		self._set_defaults(channel=channel, webhook=webhook, message=message)

		# headers for post request
		self.headers = {'Content-Type': 'application/json'}

	def _set_defaults(self, channel=None, webhook=None, message=None):
		"""Set the default channel and webhook and message."""
		# set default channel
		if channel is None:
			self.default_channel = self.cfg_channel
		else:
			self.default_channel = channel

		if webhook is None:
			self.default_webhook = self.cfg_webhook
		else:
			self.default_webhook = webhook

		if message is None:
			self.default_message = self.cfg_message
		else:
			self.default_message = message

	def _read_config(self):
		"""Read the .jarjar file for defaults."""
		# get .jarjar path
		filename = os.path.join(os.path.expanduser('~'), '.jarjar')

		# make empty .jarjar if needed
		if not os.path.exists(filename):
			open(filename, 'a').close()

		# load config
		cfg = imp.load_source('_jarjar', filename)

		# assign variables
		for field in ['channel', 'webhook', 'message']:

			# read from config, or set to none
			if hasattr(cfg, field):
				data = getattr(cfg, field)
			else:
				data = None

			# set value
			setattr(self, 'cfg_%s' % field, data)

	def _infer_kwargs(self, **kwargs):
		"""Infer kwargs for later method calls."""
		def _get(arg):
			"""Return provided arg if it exists. Otherwise, infer."""
			if arg in kwargs and kwargs[arg]:
				return kwargs[arg]

			# No support for default attach ATM.
			if arg == 'attach':
				return None

			# get a default
			default = getattr(self, 'default_{}'.format(arg))

			# return defaults for channel and webhook
			if arg in ['channel', 'webhook']:
				if not default:
					raise Exception('No {} provided!'.format(arg))
				else:
					return default

			# return default message if provided
			if self.default_message is not None:
				return self.default_message

			# no message is allowed if there is an attach
			if 'attach' in kwargs and kwargs['attach']:
				return None

			# otherwise use a super-default and warn the user.
			warnings.warn(_no_message_warn)
			return 'Meesa Jarjar Binks!'

		result = dict()
		for arg in ['message', 'attach', 'channel', 'webhook']:
			result[arg] = _get(arg)
		return result

	@staticmethod
	def _attachment_formatter(attach):
		"""Format a dict to become a slack attachment."""
		attachments = dict(
			fallback="New attachments are ready!",
			color="#36a64f",
			ts=time.time(),
			fields=[]
		)

		for key in attach:

			if isinstance(attach[key], str):
				outval = attach[key]
			else:
				outval = str(attach[key])

			attachments['fields'].append(dict(
				title=key,
				value=outval,
				short=len(outval) < 20
			))

		return [attachments]

	def attach(self, attach=None, **kwargs):
		"""Send an attachment.

		This is a convenience function which wraps around .post. Arguments
		not explicitly provided are inferred.

		Arguments

		* message (str; optional): Text to send. If attach is None and there is no
		default, jarjar just makes it up.
		* attach (dict; optional): Attachment data. All values are converted to str.
		* channel (str or list; optional): Name of the channel to post within.
		Can also be a list of channel names; jarjar will post to each.
		* webhook (str; optional): Webhook URL for the slack team.

		Returns a requests object for the POST request.
		"""
		if attach is None:
			warnings.warn('You called `attach` but there is no attachment? Weird.')
		kwargs = self._infer_kwargs(attach=attach, **kwargs)
		return self.text(**kwargs)

	def text(self, message=None, **kwargs):
		"""Send a text message.

		This is a convenience function which wraps around .post. Arguments
		not explicitly provided are inferred.

		Arguments

		* message (str; optional): Text to send. If attach is None and there is no
		default, jarjar just makes it up.
		* attach (dict; optional): Attachment data. All values are converted to str.
		* channel (str or list; optional): Name of the channel to post within.
		Can also be a list of channel names; jarjar will post to each.
		* webhook (str; optional): Webhook URL for the slack team.

		Returns a requests object for the POST request.
		"""
		kwargs = self._infer_kwargs(message=message, **kwargs)
		return self.post(**kwargs)

	def post(self, message=None, attach=None, channel=None, webhook=None):
		"""Send a message to slack.

		Arguments are not inferred and all must be provided. Use the `text` or
		`attach` methods for argument inference.

		Arguments

		* message (str; optional): Text to send. Must be provided if attach is None.
		* attach (dict; optional): Attachment data. All values are converted to str.
		Must be provided if message is None.
		* channel (str or list): Name of the channel to post within. Can also be a
		list of channel names; jarjar will post to each.
		* webhook (str; optional): Webhook URL for the slack team.

		Returns a requests object for the POST request.
		"""
		def _check_arg(arg, name, types, noneable=False):
			"""Ensure arguments are valid."""
			# NoneType handler
			if arg is None:
				if not noneable:
					raise Exception('User did not provide kwarg `{}`.'.format(name))
				else:
					return

			if not isinstance(arg, types):
				raise Exception(
					'Kwarg `{0}` has invalid type. Options: ({1})'
					.format(name, ','.join(map(str, types)))
				)

		# ensure message or attach is provided
		if message is None and attach is None:
			raise Exception('user must provide a message or attachment.')

		# check kwargs
		_check_arg(message, 'message', (str,), noneable=True)
		_check_arg(attach, 'attach', (dict,), noneable=True)
		_check_arg(channel, 'channel', (str, list))
		_check_arg(webhook, 'webhook', (str,))

		# recursively post to all channels in array of channels
		if isinstance(channel, list):
			status = []
			for c in channel:
				status.append(
					self.post(message=message, attach=attach, channel=c, url=webhook)
				)
			return status

		# construct a payload
		payload = dict(channel=channel)

		# add text and attachments if provided
		if message is not None:
			payload['text'] = message

		if attach is not None:
			payload['attachments'] = self._attachment_formatter(attach)

		# convert payload to json and return
		payload = json.dumps(payload)
		return requests.post(webhook, data=payload, headers=self.headers)

	def set_webhook(self, webhook):
		"""Set default webhook."""
		self.default_webhook = webhook

	def set_channel(self, channel):
		"""Set default channel."""
		self.default_channel = channel

	def set_message(self, message):
		"""Set default message."""
		self.default_message = message
