import os
from jarjar import jarjar


def writetofile(f, **kwargs):
    """write kwargs to a file"""
    s = ''
    for k, v in kwargs.items():
        s += '%s=\'%s\'\n' % (k, v)

    with open(f, 'w') as fh:
        fh.write(s)


jj = jarjar()
print('-- vanilla')
print('channel', jj.default_channel)
print('message', jj.default_message)
print('webhook', jj.default_webhook)
print()

writetofile('.jarjar', webhook='1', channel='2', message='3')
jj = jarjar()
print('-- inferred .jarjar')
print('channel', jj.default_channel)
print('message', jj.default_message)
print('webhook', jj.default_webhook)
print()
os.remove('.jarjar')

writetofile('.jjconfig', webhook='4', channel='5', message='6')
jj = jarjar(config='.jjconfig')
print('-- specified .jjconfig')
print('channel', jj.default_channel)
print('message', jj.default_message)
print('webhook', jj.default_webhook)
print()
os.remove('.jjconfig')
