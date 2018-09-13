# Python API Workflows

Jarjar is great for letting you know when a snippet of code has finished
executing, but configuring things properly can be a little bit of a hassle.

A common workflow involves writing your code and then throwing a jarjar call
at the end:

```python
from jarjar import jarjar
jj = jarjar()

def fun(long_list):
  results = []
  for i in long_list:
    if i == 'something':
      results.append('something')
    else:
      results.append('something else')
  return results

# run the process, notify on completion
results = fun(a_long_list)
jj.text('Process complete!')
```

That looks good, but what if an exception was raised on the way? So maybe you
edit like so:

```python
try:
  results = fun(my_long_list)
  jj.text('Process complete!')
except Exception:
  jj.text('Process Failed?')
```

That's great. But what if you want to run many such processes? Or what if you
want to run the same process twice, getting a notification each time? What if
you wanted to include the traceback within the message if there was an
exception?

You can end up writing a lot more code just to handle jarjar notifications.
Luckily, we wrote that code for you.

## Jarjar decorator

You can decorate a function and jarjar will handle exceptions for you. You'll
get a notification whenever the function exits, and it will include the
traceback if there was an exception:

```python
@jj.decorate
def fun(long_list):
  # ...

results = fun(my_long_list)
```

## Jupyter cell magic

Jupyter notebooks are becoming a standard in scientific work. Packaged with
jarjar is a Jupyter magic so that users can be notified about a cell's
execution.

You first need to register the magic, and then you can use it freely. In one
cell:

```python
from jarjar import jarjar
jj = jarjar()
jj.register_magic()
```

Then in a later cell:

```python
%%jarjar
results = fun(my_long_list)
```

You'll get a notification whether your cell executed successfully or not, and it
will include the traceback if there was an exception.
