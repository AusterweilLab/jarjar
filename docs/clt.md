# Using the jarjar command line tool

The CLT provides basic posting functionality like in the python API but it also provides a useful task execution facility.

## Posting to your team

The jarjar CLT offers all the functionality of the python API, except for posting attachments (sorry). Posting messages is super easy though!


You can use your defaults from .jarjar
```sh
jarjar --message 'Meesa jarjar binks!'
```

Or not.

```sh
jarjar -m 'Hi, everyone!!' --webhook '<your-url>' --channel '#general'
```

## Running processes with jarjar

We use jarjar to run a lot of longer processes when we don't want to keep our terminal sessions around. You can use jarjar for this sort of thing.

```sh
jarjar sleep 3600
```

Now you can head out for some lunch. Here's what's going on under the hood:

1. **Start up a [screen](https://www.gnu.org/software/screen/)**. The screen can have a custom name (using the `-S` or  `--screen_name` flags) but if you don't provide one it'll be named using the program you provide. Above, the screen was named `sleep_3600`.
2. **Run your process in that screen**. If you want you can attach to the screen (using the `-a`, `-r`, or  `--attach` flags) and see the magic happen.
3. **Send a message when the process is complete**. If you specified a message (using the `-m` or  `--message` flags) jarjar will send it. Jarjar will then kill your screen if:
    * You don't tell it to keep the screen (using the `--no-exit` flag).
    * You didn't attach to it (using the `-a`, `-r`, or  `--attach` flags).
    * The program you ran exited with status 0.

### Examples

```sh
# send a custom message
jarjar python run-simulations.py --message 'Simulations Complete!'

# name your screen
jarjar sleep 1 --screen-name 'snooze'

# watch the magic happen
jarjar <program> --attach

# keep the screen around for debugging
jarjar <program> --no-exit

# show jarjar version
jarjar --version

# get help
jarjar --help
```

## Argument Reference

- `-h`, `--help`. Show help message.
- `-v`, `--version`. Show jarjar version.
- `-m`, `--message`. Specify message to send. This best done in single-quotes (`jarjar -m 'hi'`) but jarjar rolls with the punches (like `jarjar -m hi`).
- `-w`, `--webhook`. Specify webhook to post to.
- `-c`, `--channel`. Specify channel to post to. Unlike in the python module, only one channel can be supplied at a time. Since `#` is interpreted as a shell comment, you'll want to put this in single quotes (`jarjar -c '#general'`).
- `-a`, `-r`, `--attach`. Attach to the screen once the program has started running. If you didn't provide a program jarjar will think you are weird.
- `-S`, `--screen_name`. Specify the name of the screen created for the program. If you didn't provide a program jarjar will think you are weird.
- `--no-exit`. Don't exit the screen even if the program exited successfully. If you didn't provide a program jarjar will think you are weird.
- `--no-jarjar`. Run a program but don't send a slack message about it. In this case jarjar is just acting as a screen generator. If you didn't provide a program jarjar will think you are weird.

