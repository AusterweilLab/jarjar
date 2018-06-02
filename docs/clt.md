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
3. **Send a message when the process is complete**. If you specified a message (using the `-m` or  `--message` flags) jarjar will send it. Jarjar will also send some information on your process (elapsed time, final exit status) as an attachment. Then jarjar will kill the screen unless you say otherwise (using the `--no-exit` flag).

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
```