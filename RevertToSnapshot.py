from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom
import mysql.connector

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

domName = raw_input('Enter domain name: ')

def domain_restore():
    dom = conn.lookupByName(domName) 
    if dom == None:
        print('Failed to find the domain %s', domName)
        exit(1)
    dom.shutdown()
    snap = dom.snapshotLookupByName('BASE_SNAPSHOT')
    dom.revertToSnapshot(snap)
    print('reverted to base snapshot')
'''
def update_table_domainInfo():
    domains = conn.listAllDomains(0)
    if len(domains) != 0:
        clear = "TRUNCATE TABLE domains.domainInfo"
        mycursor.execute(clear)
        mydb.commit()
        for domain in domains:
            state, reason = domain.state()       
            sql = "INSERT INTO domainInfo (UUID, domainID, name, state) VALUES (%s, %s, %s, %s)"
            val = (domain.UUIDString(), domain.ID(), domain.name(), domain_state(state))
            mycursor.execute(sql, val)
            mydb.commit()
'''

domain_restore()