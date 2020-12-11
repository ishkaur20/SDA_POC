
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
    user="labadmin",
    password="C1sco12345",
    database="domains" )
    
mycursor = mydb.cursor()

domName = raw_input('Enter domain name: ')
dom = conn.lookupByName(domName) 
if dom == None:
    print('Failed to find the domain %s', domName)
    exit(1)

#in case I need to check domain status before creating snapshot
'''
domain_state(state):
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
'''

def is_qcow2(raw_xml):
    xml = minidom.parseString(raw_xml)
    diskTypes = xml.getElementsByTagName('driver')
    for diskType in diskTypes:
        print('disk: type='+diskType.getAttribute('type'))
        if diskType.getAttribute('type') == 'qcow2':
            return True
    return False

snapshot_name = raw_input('Name your snapshot file:')
def take_snapshot(vm):
    SNAPSHOT_XML_TEMPLATE = "<domainsnapshot><name>{}</name></domainsnapshot>".format(snapshot_name)
    snapshot = vm.snapshotCreateXML(
                SNAPSHOT_XML_TEMPLATE,
                libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC )

def create_snapshot():
    raw_xml = dom.XMLDesc(0) # Get xml from this object
    if is_qcow2(raw_xml): # Check if the driver for this vm is of type qcow2   
        take_snapshot(dom) # if it is then take a snapshot -> delegate this to method.
        print('Snapshot created')
    if not is_qcow2(raw_xml):
        print('This drive is not qcow2, cannot take snapshot')


def update_table_snapshotInfo():
    domains = conn.listAllDomains(0)
    if len(domains) != 0:
        clear = "TRUNCATE TABLE domains.snapshotInfo"
        mycursor.execute(clear)
        mydb.commit()
        for domain in domains:
            snapshots = domain.snapshotListNames()
            for snapshot in snapshots:
                sql = "INSERT INTO domains.snapshotInfo (name, snapshotName) VALUES (%s, %s)"
                val = (domain.name(), snapshot)
                mycursor.execute(sql, val)
                mydb.commit()
    else:
        print('None')

create_snapshot()
update_table_snapshotInfo()



conn.close()
exit(0)