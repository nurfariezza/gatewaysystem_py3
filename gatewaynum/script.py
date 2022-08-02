import xml.etree.ElementTree as ET
from xml.dom import minidom

root = ET.Element("RTSMS_sp_User_New", master_id="1140", name="wfsiew", login_id="wf001", \
                  password="wf002", email="wf@redtone.org", mobile="", level="1", month_limit="100", admin_id="0")

ls = ['<RTSMS_sp_User_New']
ls.append(' master_id="{0}"'.format(1140))
ls.append(' name="{0}"'.format('wfsiew'))
ls.append(' login_id="{0}"'.format('wf001'))
ls.append(' password="{0}"'.format('wf002'))
ls.append(' email="{0}"'.format('wf@redtone.org'))
ls.append(' mobile="{0}"'.format(''))
ls.append(' level="{0}"'.format(1))
ls.append(' month_limit="{0}"'.format(100))
ls.append(' admin_id="{0}"'.format(0))
ls.append('></RTSMS_sp_User_New>')
k = ''.join(ls)

doc = minidom.Document()
root = doc.createElement('RTSMS_sp_User_New')
root.setAttribute('master_id', '1140')
root.setAttribute('name', 'wfsiew')
root.setAttribute('login_id', 'wf001')
root.setAttribute('password', 'wf002')
root.setAttribute('email', 'wf@redtone.ord')
root.setAttribute('mobile', '')
root.setAttribute('level', '1')
root.setAttribute('month_limit', '100')
root.setAttribute('admin_id', '0')

txt = doc.createTextNode('')
root.appendChild(txt)

doc.appendChild(root)
t = doc.toprettyxml(encoding='UTF-8')
print t