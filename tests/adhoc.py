import time
from jarjar import jarjar

jj = jarjar()

@jj.decorate
def f(a=1):
    time.sleep(a)
    kfkdfsk


f(3)
