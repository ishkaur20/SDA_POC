
#connect to a local QEMU hypervisor using a local URI

from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom
import mysql.connector

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="domains"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE domains")
#mycursor.execute("ALTER TABLE domainInfo ADD COLUMN name VARCHAR(255), ADD COLUMN state VARCHAR(255)")
#mycursor.execute("SHOW TABLES")


host = conn.getHostname()
print('Hostname:'+host)

print('Virtualization type: '+conn.getType())

VM = 'win2kr12'
dom = conn.lookupByName(VM)
if dom == None:
    print('Failed to find the domain '+ VM, file=sys.stderr)
    exit(1)

domName = dom.name()
print('The name of the domain is "' + domName +'".')

flag = dom.hasCurrentSnapshot()
print('The value of the current snapshot flag is ' + str(flag))

snap_list = dom.snapshotListNames()
print(snap_list)

domains = conn.listAllDomains(0)
flag = dom.isActive()
if flag == True:
    print('The domain is active.')
else:
    print('The domain is not active.')

def domain_state(state):
    if state == 0:
        return('NO STATE')
    elif state == 1:
        return('RUNNING')
    elif state == 2:
        return('BLOCKED')
    elif state == 3:
        return('PAUSED')
    elif state == 4:
        return('SHUTDOWN')
    elif state == 5:
        return('SHUTOFF')
    elif state == 6:
        return('CRASHED')
    elif state == 7:
        return('PMSUSPENDED')
    else:
        return('UNKNOWN')


print("All (active and inactive) domain names:")
domains = conn.listAllDomains(0)
if len(domains) != 0:
    for domain in domains:
        state, reason = domain.state()
        print('  '+  'domain UUID:' + domain.UUIDString() + '  domain ID:' + str(domain.ID()) + '  name:' + domain.name() + '  state:' + domain_state(state))
        sql = "INSERT INTO domainInfo (UUID, domainID, name, state) VALUES (%s, %s, %s, %s)"
        val = (domain.UUIDString(), domain.ID(), domain.name(), domain_state(state))
        mycursor.execute(sql, val)
        mydb.commit()
        
else:
    print('  None')



conn.close()
exit(0)