import pyodbc, logging

logger = logging.getLogger(__name__)

def initdb(dbx=None, autocommit=True, user=None, pwd=None):
    db = dbx
    if dbx is None:
        if user is not None:
            db = DbHelper(user=user, pwd=pwd)
            
        else:
            db = DbHelper()
            
        db.connect(autocommit=autocommit)
    
    return db

class DbHelper(object):
    
    def __init__(self, server='192.168.138.172', db='NewIddGateway', user='gksys', pwd='R@dtone168'):
        self.constr = self.getconstr(server, db, user, pwd)
        self.con = None
        self.cur = None
        
    def connect(self, autocommit=True):
        self.con = pyodbc.connect(self.constr, autocommit=autocommit)
        self.cur = self.con.cursor()
        
    def commit(self):
        self.con.commit()
    
    def dispose(self):
        if self.cur is not None:
            self.cur.close()
            
        if self.con is not None:
            self.con.close()
            
    def getconstr(self, server, db, user, pwd):
        s = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3};APP=GatewayReg_py'.format(server, db, user, pwd)
        # s = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3};APP=GatewayReg_py'.format(server, db, user, pwd)

        return s
