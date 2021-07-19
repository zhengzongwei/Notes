import sys 
sys.path.append("..")
import json

from api.vm import *

##########################################
####### API Snapshot  Test
##########################################


def print_result(ret):
    print json.dumps(ret,indent=4)


def snapshot_test(ip,uuids):
    snapshotname = "init_zzw_test"
    snapshotmemory =False
    VM_SnapshotCreateInit(ip,uuids,snapshotname,snapshotmemory)
    print_result(snapshot_list(uuid))

ip = '192.168.50.24'
win7_uuid = "291fd1d8-ed1e-11eb-9ba2-0cc47a0c5910"
snapshot_test(ip ,[win7_uuid])