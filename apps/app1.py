import os
import time
import random
import logging


logname = os.path.basename(__file__)[:-3]
logpath = os.path.join(os.path.dirname(__file__), '..', 'log')
logging.basicConfig(
    filename="%s\\%s.log"%(logpath, logname),
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s >> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
print = logging.info




##### HERE YOU APP
# ...

# example
for i in range(random.randint(3, 10)):
    print('This is test output no %s'%(i))
    time.sleep(1)
    