from jarjar import jarjar

args = dict(
    message='Test',
    attach={'a': u'Unicode \ua000'},
    channel=u'#jarjar',
    webhook=None,
)

jj = jarjar()
jj.text(**args)
