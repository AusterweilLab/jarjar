import time
from jarjar import jarjar

jj = jarjar()

@jj.decorate(message='Hi!', channel='sleepy-gary-says')
def f(a=1):
    time.sleep(a)
    kfkdfsk


f(3)
