import time
from jarjar import jarjar

jj = jarjar()

@jj.decorate
def fun(a=1):
    time.sleep(a)
    int('a')


fun(3)
