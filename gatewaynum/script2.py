import pyodbc, json

def getconstr():
    s = 'DRIVER={SQL Server Native Client 10.0};SERVER=192.168.138.120;DATABASE=HSBB_Billing;UID=CallBilling;PWD=CBPWD12345'
    return s

con = pyodbc.connect(getconstr())
cur = con.cursor()

q = "select top 9000 custid, name from customer"

rows = cur.execute(q).fetchall()
for r in rows:
    if isinstance(r.name, str):
        print r.custid

cur.close()
con.close()