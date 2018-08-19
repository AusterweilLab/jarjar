.. jarjar documentation master file, created by
   sphinx-quickstart on Sat Jun  2 13:53:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
Welcome to jarjar's documentation!
##################################

Jarjar is a python utility that makes it easy to send slack notifications to your teams.
You can import it as a python module or use our command line tool.

**************************
What Can Jarjar Do For Me?
**************************

Jarjar was developed at the `Austerweil Lab at UW-Madison <http://alab.psych.wisc.edu/>`_ as a tool
for scientists. We use it for all sorts of things, such as:

1. Sending a message so that we know when long-running processes have finished.

   .. image:: img/simulations-complete.png

2. Sending notices when scheduled tasks have failed.

   .. image:: img/backups-failed.png

3. Sending out daily positive vibes.

   .. image:: img/positive-vibes.png


**********
Quickstart
**********


Install
-------

:doc:`Installation </install>` is simple!

.. code-block:: shell

   pip install jarjar

My guess is that you'll want to create jarjar's config file, ``~/.jarjar``. This tells jarjar
what you'd like to use as a default for your slack team's webhook, the channel to post to,
and the message it sends. Don't worry, you can over-ride these anytime.

Edit this snippet and add it to ``~/.jarjar``:

.. code-block:: shell

   channel='@username'
   message='Custom message'
   webhook='https://hooks.slack.com/services/your/teams/webhook'

If you don't know your team's webhook, you might have to
`make one <https://my.slack.com/apps/A0F7XDUAZ-incoming-webhooks>`_.

Python API
----------

Use the :doc:`jarjar python api </api>` like:

.. code-block:: python

    from jarjar import jarjar

    # initialize a jarjar object
    jj = jarjar() # defaults from .jarjar
    jj = jarjar(channel='#channel', webhook='slack-webhook-url')
    jj = jarjar(webhook='slack-webhook-url')

    # send a text message
    jj.text('Hi!')
    jj.text('Hi!', channel=["@jeffzemla", "#channel"])

    # send an attachment
    jj.attach({'meesa': 'jarjar binks'}, message='Hello!')

Command Line Tool
-----------------

We also made a :doc:`command line tool </clt>` for use outside of python scripts.
The command line tool adds functionality to execute processes and send messages when they
are complete.

 .. code-block:: shell

   jarjar sleep 1 -m 'Meesa took a nap!'

And then in your slack team:

 .. image:: img/nap.png

Custom attachments are not supported in the CLT at this time, but everything else is:

 .. code-block:: shell

   jarjar -m 'Meesa jarjar binks!'
   jarjar -m 'Hi, everyone!!' --webhook '<your-url>' -c '#general'

********************
Detailed Documention
********************

.. toctree::
   :maxdepth: 1

   install
   clt
   api
