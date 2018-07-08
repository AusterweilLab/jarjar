
import requests
import json
import time
import os
import imp
import warnings
import copy

_EXPECTED_CONFIG = ['channel', 'webhook', 'message']
_NO_MESSAGE_WARN = (
    '''
    Slow down cowboy! You didn't provide a message and there is
    no default in your .jarjar, so I'll just wing it.
    '''
    .strip()
    .replace('\n', ' ')
    .replace('\t', ' ')
    .replace('  ', ' ')
)


def read_config_file(filename):
    """Find expected fields in a config file.

    Return nones if it does not exist, otherwise, load the file as a module
    and getattr for each.
    """

    # red recursively
    if isinstance(filename, (list, tuple)):
        return [read_config_file(i) for i in filename]

    # Nones if the file does not exist
    if not os.path.exists(filename):
        return dict((i, None) for i in _EXPECTED_CONFIG)

    # laod it up, remove compiled file if its there
    cfg = imp.load_source('_tmp', filename)
    try:
        os.remove(filename + 'c', )
    except OSError:
        pass

    # grab expected values
    return dict((i, getattr(cfg, i, None)) for i in _EXPECTED_CONFIG)


class jarjar(object):
    """A jarjar slack messenger.

    This is largely a wrapper around functionality in ``requests.post()`` with
    facilities to store and set default values for the desired message to
    send, channel to post within, and slack team webhook.

    Inference for these values proceeds as follows.

    1. Any argument provided to :func:`~jarjar.jarjar.text` or
       :func:`~jarjar.jarjar.attach` supersedes all defaults.
    2. Any argument provided to this class at initialization.
    3. Defaults within a config file at a user-specified path (``config='...').
    4. Defaults within a config file ``.jarjar``, within the working directory.
    5. Defaults within ``.jarjar``, located in the user's home directory.

    The config files (for numbers 3-5) look like:

    .. code::

        channel="@username"
        message="Custom message"
        webhook="https://hooks.slack.com/services/your/teams/webhook"

    3. Arguments provided  at initialization supersede those in ``~/.jarjar``.
       If the channel or webhook arguments are never provided, an error is
       raised. If the channel and webhook are provided but not a message or
       attachment, jarjar will make something up.

    Methods
    -------
    attach(attach, channel=None, webhook=None, message=None)
        Send an attachment. User may also include a text message.
    text(message, channel=None, webhook=None, attach=None)
        Send a text message. User may also include an attachment.
    set_webhook(webhook)
        Set jarjar's default webhook.
    set_channel(channel)
        Set jarjar's default channel.
    set_message(message)
        Set jarjar's default message.

    Parameters
    ----------
    message : str
        Optional. Default message to send.
    channel : str,  list
        Optional. Name of the default channel to post within.
    webhook : str
        Optional. Webhook URL for the default slack team.

    """

    # defaults; exposed for the user
    _final_default_message = 'Meesa Jarjar Binks!'
    headers = {'Content-Type': 'application/json'}

    def __init__(self, config=None, **defaults):

        # check unexpected args
        for k, _ in defaults.items():
            if k in _EXPECTED_CONFIG:
                continue
            warnings.warn('Recieved unexpected kwarg: `%s`.' % k)

        # paths listed in order of precedent
        expected_config_files = [
            os.path.join(os.getcwd(), '.jarjar'),
            os.path.join(os.path.expanduser('~'), '.jarjar'),
        ]

        # add user path if needed. insert to the _front_
        if config is not None:
            if isinstance(config, list):
                expected_config_files = config + expected_config_files
            else:
                expected_config_files.insert(0, config)

        # read configs and set defaults
        configs = read_config_file(expected_config_files)

        # add inline defaults to the front
        configs.insert(0, defaults)
        for i in configs:
            print(i)
        # set attrs
        for val in _EXPECTED_CONFIG:
            setattr(
                self,
                'default_%s' % val,
                next((i[val] for i in configs if i.get(val, None)), None)
            )

        # default attach and payload args
        self.attachment_args = dict(
            fallback="New attachments are ready!",
            color="#36a64f",
            fields=[]
        )
        self.payload_args = dict()

    def _infer_kwargs(self, **kwargs):
        """Infer kwargs for later method calls."""
        def _get(arg):
            """Return provided arg if it exists. Otherwise, infer."""
            if arg in kwargs and kwargs[arg] not in ('', None):
                return kwargs[arg]

            # No support for default attach ATM.
            if arg == 'attach':
                return None

            # get a default
            default = getattr(self, 'default_{}'.format(arg))

            # return defaults for channel and webhook
            if arg in ['channel', 'webhook']:
                if not default:
                    raise NameError('No {} provided!'.format(arg))
                else:
                    return default

            # return default message if provided
            if self.default_message is not None:
                return self.default_message

            # no message is allowed if there is an attach
            if 'attach' in kwargs and kwargs['attach']:
                return None

            # otherwise use a super-default and warn the user.
            warnings.warn(_NO_MESSAGE_WARN)
            return self._final_default_message

        # check unexpected args
        for k, _ in kwargs.items():
            if k in _EXPECTED_CONFIG:
                continue
            warnings.warn('Recieved unexpected kwarg: `%s`.' % k)

        result = dict()
        for arg in ['message', 'attach', 'channel', 'webhook']:
            result[arg] = _get(arg)
        return result

    def _attachment_formatter(self, attach):
        """Format a dict to become a slack attachment."""
        attachments = copy.deepcopy(self.attachment_args)
        attachments['ts'] = time.time()

        for key in attach:

            if isinstance(attach[key], str):
                outval = attach[key]
            else:
                try:
                    outval = str(attach[key])
                except UnicodeEncodeError:
                    outval = unicode(attach[key])
                except Exception:
                    raise

            attachments['fields'].append(dict(
                title=key,
                value=outval,
                short=len(outval) < 20
            ))
        return [attachments]

    def attach(self, attach=None, **kwargs):
        """Send an attachment.

        This method is largely identical to :func:`~jarjar.jarjar.text`,
        only differing in the first argument (``attach``), which is expected
        to be a dictionary.

        Parameters
        ----------
        attach : dict
            Attachment data. Optional *but weird if you don't provide one*.
            All values are converted to string for the slack payload so don't
            sweat it.
        message : str
            Text to send. Optional. If attach is None and there is no
            default *and* you don't provide one here, jarjar just wings it.
        channel : str,  list
            Optional. Name of the channel to post within.
            Can also be a list of channel names; jarjar will post to each.
        webhook : str
            Optional. Webhook URL for the slack team.

        Returns
        -------
        response : requests.models.Response
            Requests response object for the POST request to slack.

        """
        if attach is None:
            warnings.warn(
                'You called `attach` but there is no attachment? Weird.'
            )
        kwargs = self._infer_kwargs(attach=attach, **kwargs)
        return self.text(**kwargs)

    def text(self, message=None, **kwargs):
        """Send a text message.

        This method is largely identical to :func:`~jarjar.jarjar.attach`, only
        differing in the first argument (``message``), which is expected to be
        a string.

        Parameters
        ----------
        message : str
            Text to send. Optional *but weird if you don't provide one*.
            If attach is None and there is no default *and* you don't provide
            one here, jarjar just wings it.
        attach : dict
            Attachment data. Optional. All values are converted to string for
            the slack payload so don't sweat it.
        channel : str,  list
            Optional. Name of the channel to post within.
            Can also be a list of channel names; jarjar will post to each.
        webhook : str
            Optional. Webhook URL for the slack team.

        Returns
        -------
        response : requests.models.Response
            Requests response object for the POST request to slack.

        """
        kwargs = self._infer_kwargs(message=message, **kwargs)
        return self._post(**kwargs)

    def post(self, *args, **kwargs):
        """**DEPRECATED**. Pass args to .text and raises a warning."""
        warnings.warn(
            'jarjar.post() is deprecated! I\'ll let this slide ' +
            'but you should switch to text or attach'
        )
        return self.text(*args, **kwargs)

    def _post(self, message=None, attach=None, channel=None, webhook=None):
        """Send a message to slack.

        Arguments are not inferred and all must be provided. Use the `text` or
        `attach` methods for argument inference.

        Parameters
        ----------
        message : str, NoneType
            Text to send.

        attach : dict, NoneType
            Attachment data.

        channel : str,  list
            Optional. Name of the channel to post within.
            Can also be a list of channel names; jarjar will post to each.
        webhook : str
            Optional. Webhook URL for the slack team.

        Returns
        -------
        response : requests.models.Response
            Requests response object for the POST request to slack.

        """
        def _check_arg(arg, name, types, noneable=False):
            """Ensure arguments are valid."""
            # NoneType handler
            if arg is None:
                if not noneable:
                    raise NameError(
                        'User did not provide kwarg `{}`.'.format(name)
                    )
                else:
                    return

            if not isinstance(arg, types):
                raise TypeError(
                    'Kwarg `{0}` has invalid type. Options: ({1})'
                    .format(name, ','.join(map(str, types)))
                )

        # ensure message or attach is provided
        if message is None and attach is None:
            raise NameError('user must provide a message or attachment.')

        # define tupe of string types
        # try/except is control for python 3.
        try:
            str_types = (str, unicode)
        except Exception:
            str_types = (str,)

        # check kwargs
        _check_arg(message, 'message', str_types, noneable=True)
        _check_arg(attach, 'attach', (dict,), noneable=True)
        _check_arg(channel, 'channel', str_types + (list, ))
        _check_arg(webhook, 'webhook', str_types)

        # recursively post to all channels in array of channels
        if isinstance(channel, list):
            status = []
            for c in channel:
                status.append(
                    self._post(
                        message=message,
                        attach=attach,
                        channel=c,
                        webhook=webhook
                    )
                )
            return status

        # construct a payload
        payload = copy.deepcopy(self.payload_args)
        payload['channel'] = channel

        # add text and attachments if provided
        if message is not None:
            payload['text'] = message

        if attach is not None:
            payload['attachments'] = self._attachment_formatter(attach)

        # convert payload to json and return
        payload = json.dumps(payload)
        return requests.post(webhook, data=payload, headers=self.headers)

    def set_webhook(self, webhook):
        """Set default webhook.

        Parameters
        ----------
        webhook : str
            Webhook URL for the slack team.

        """
        self.default_webhook = webhook

    def set_channel(self, channel):
        """Set default channel.

        Parameters
        ----------
        channel : str
            Name of the channel to post within.

        """
        self.default_channel = channel

    def set_message(self, message):
        """Set default message.

        Parameters
        ----------
        message : str
            Default message to send.

        """
        self.default_message = message
