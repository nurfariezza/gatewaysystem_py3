PAGE_SIZE = 50
LIST_SIZE = 20
ALLOWCALLSHOPTOPUP = 1
KIOSKCALLERIDBLOCKINGTYPE = [601,602,603,608,630,631]
VKIOSKTYPE = 650
CALLSHOPSUBTYPE1 = 610
CALLSHOPSUBTYPE2 = 619
VIRTUALKIOSKTYPE = 650
PAYLATER = 2
REFUND = 3
MISC = 4
CREDIT_TRANSFER = 5
TOPDOWN = 7
FREE_AIRTIME = 8
PAYLATER_SETTLEMENT = 9
TERMINATION_REFUND = 10
BUDGETLCR = 10
BUDGETRATE = 43
EMPTY_WHOLESALER = ['0', '', None]
REDTONE_WHOLESALER = [1, 73]

class GWID(object):
    GWALL = 0
    GWCP = 1
    GWPD = 2
    GWAM = 3
    GWKLP = 4
    GWSB = 5
    GWPDDB2 = 6

# GWID_GWALL = 0
# GWID_GWCP = 1
# GWID_GWPD = 2
# GWID_GWAM = 3
# GWID_GWKLP = 4
# GWID_GWSB = 5
# GWID_GWPDDB2 = 6

class FEATUREBIT(object):
    ADDNEW = 0
    UPDATE = 1
    SHOW015PASSWORD = 2
    CHECKCALLERIDLIST = 3
    TOPUPREPORT = 4
    CONTACTLIST = 5
    DELETE = 6
    MORE = 7
    TECHNICALINFO = 8
    MAX = 8

# FEATUREBIT_ADDNEW = 0
# FEATUREBIT_UPDATE = 1
# FEATUREBIT_SHOW015PASSWORD = 2
# FEATUREBIT_CHECKCALLERIDLIST = 3
# FEATUREBIT_TOPUPREPORT = 4
# FEATUREBIT_CONTACTLIST = 5
# FEATUREBIT_DELETE = 6
# FEATUREBIT_MORE = 7
# FEATUREBIT_TECHNICALINFO = 8
# FEATUREBIT_MAX = 8

class ACCESS(object):
    NEW = 'ACCESS_NEW'
    UPDATE = 'ACCESS_UPDATE'
    TOPUPREPORT = 'ACCESS_TOPUPREPORT'
    DELETE = 'ACCESS_DELETE'
    OTHER = 'ACCESS_OTHER'
    CHANGEGATETYPE = 'ACCESS_CHANGEGATETYPE'
    ADDREMARK = 'ACCESS_ADDREMARK'

# ACCESS_NEW = 'ACCESS_NEW'
# ACCESS_UPDATE = 'ACCESS_UPDATE'
# ACCESS_TOPUPREPORT = 'ACCESS_TOPUPREPORT'
# ACCESS_DELETE = 'ACCESS_DELETE'
# ACCESS_OTHER = 'ACCESS_OTHER'
# ACCESS_CHANGEGATETYPE = 'ACCESS_CHANGEGATETYPE'
# ACCESS_ADDREMARK = 'ACCESS_ADDREMARK'

VER = '1.36'
