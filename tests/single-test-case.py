#! /usr/bin/env python

from jarjar import jarjar

args = dict(
    message='Test',
    attach={'a': u'Unicode \ua000'},
    channel=u'#sleepy-gary-says',
    webhook=None,
)

jj = jarjar()
# jj.text(**args)
print('here')

ddd
