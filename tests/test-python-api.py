from jarjar import jarjar

# define a jarjar
jj = jarjar()

# vanilla channel change
res = jj.text('1', channel='@nolan')

# unicode in message
res = jj.text(u'2 \ua000')

# unicode in attach
res = jj.attach({u'Unicode \ua000': u'Unicode \ua000'}, message='3')


# decorator
@jj.decorate(message='4', attach={'exception?': 'no!'})
def works():
    """Call that should work..."""
    return


@jj.decorate(message='5', attach={'exception?': '*YES*'})
def doesnt_work():
    """Call that should not work..."""
    jkfdskljfdkjl
    return


try:
    works()
    doesnt_work()
except Exception:
    pass

jj.text('*YOU SHOULD HAVE RECEIVED 5 TESTS*')

print('done')
