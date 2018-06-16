# This file is modified from the screenutils Python module
# https://pypi.org/project/screenutils/
# https://github.com/Christophe31/screenutils

# -*- coding:utf-8 -*-
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the GNU Public License 2 or upper.
# Please ask if you wish a more permissive license.

try:
    from commands import getoutput
except Exception:
    from subprocess import getoutput
from os import system
from time import sleep


class ScreenNotFoundError(Exception):
    """Raised when the screen does not exists."""

    def __init__(self, message, screen_name):
        message += " Screen \"{0}\" not found".format(screen_name)
        self.screen_name = screen_name
        super(ScreenNotFoundError, self).__init__(message)


def list_screens():
    """List all the existing screens and build a Screen instance for each."""
    list_cmd = "screen -ls"
    return [
        Screen(".".join(l.split(".")[1:]).split("\t")[0])
        for l in getoutput(list_cmd).split('\n')
        if "\t" in l and ".".join(l.split(".")[1:]).split("\t")[0]
    ]


class Screen(object):
    """Represents a gnu-screen object.

    >>> s=Screen("screenName", initialize=True)
    >>> s.name
    'screenName'
    >>> s.exists
    True
    >>> s.state
    >>> s.send_commands("man -k keyboard")
    >>> s.kill()
    >>> s.exists
    False
    """

    def __init__(self, name, initialize=False):
        self.name = name
        self._id = None
        self._status = None
        if initialize:
            self.initialize()

    @property
    def id(self):
        """Return the identifier of the screen as string."""
        if not self._id:
            self._set_screen_infos()
        return self._id

    @property
    def status(self):
        """Return the status of the screen as string."""
        self._set_screen_infos()
        return self._status

    @property
    def exists(self):
        """Tell if the screen session exists or not."""
        # Parse the screen -ls call, to find if the screen exists or not.
        #  "    28062.G.Terminal    (Detached)"
        lines = getoutput("screen -ls").split('\n')
        return self.name in [
            ".".join(l.split(".")[1:]).split("\t")[0]
            for l in lines
            if self.name in l
        ]

    def initialize(self):
        """Initialize a screen, if does not exists yet."""
        if not self.exists:
            self._id = None
            # Detach the screen once attached, on a new tread.
            # support Unicode (-U),
            # attach to a new/existing named screen (-R).

            # ORIGINAL
            # Thread(target=self._delayed_detach).start()
            # system('screen -s sh -UR -S ' + self.name)

            # CUSTOM
            system('screen -d -m -S ' + self.name)

    def interrupt(self):
        """Insert CTRL+C in the screen session."""
        self._screen_commands("eval \"stuff \\003\"")

    def kill(self):
        """Kill the screen applications then close the screen."""
        self._screen_commands('quit')

    def detach(self):
        """Detach the screen."""
        self._check_exists()
        system("screen -d " + self.id)

    def send_commands(self, *commands):
        """Send commands to the active gnu-screen."""
        self._check_exists()
        for command in commands:

            # use single quote unless that is a part of the command
            if "'" in command:
                q = "\""
            else:
                q = "\'"

            self._screen_commands(
                'stuff {q}{c}{q}'.format(q=q, c=command),
                'eval "stuff \\015"'
            )

    def add_user_access(self, unix_user_name):
        """Allow to share your session with an other unix user."""
        self._screen_commands('multiuser on', 'acladd ' + unix_user_name)

    def _screen_commands(self, *commands):
        """Allow to insert generic screen specific commands."""
        self._check_exists()
        for command in commands:
            cmd = 'screen -x {0}.{1} -p 0 -X {2}'.format(self.id, self.name, command)
            system(cmd)
            sleep(0.02)

    def _check_exists(self, message="Error code: 404."):
        """Check whereas the screen exist. if not, raise an exception."""
        if not self.exists:
            raise ScreenNotFoundError(message, self.name)

    def _set_screen_infos(self):
        """Set the screen information related parameters."""
        if self.exists:
            line = ""
            for l in getoutput("screen -ls").split("\n"):
                if (
                    l.startswith('\t') and
                    self.name in l and
                    self.name == ".".join(l.split('\t')[1].split('.')[1:]) in l
                ):
                    line = l
            if not line:
                raise ScreenNotFoundError("While getting info.", self.name)
            infos = line.split('\t')[1:]
            self._id = infos[0].split('.')[0]
            if len(infos) == 3:
                self._date = infos[1][1:-1]
                self._status = infos[2][1:-1]
            else:
                self._status = infos[1][1:-1]

    def _delayed_detach(self):
        sleep(0.5)
        self.detach()

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.name)
