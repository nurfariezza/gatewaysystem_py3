from datetime import datetime
from dateutil.relativedelta import relativedelta

#k = datetime.now()
#j = k + relativedelta(minutes=-2)
#print k
#print j#

m, s = divmod(994, 60)
h, m = divmod(m, 60)
print ('{0:02d}:{1:02d}:{2:02d}'.format(h, m, s))
print ("%d:%02d:%02d" % (h, m, s))

from utils import simpledecrypt, simpleencrypt

m = simpledecrypt('6B60596A59292E2929', 8)
print(m)

i = simpleencrypt('frances321', 8)
print(i)
