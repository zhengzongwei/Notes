import os
import sys 
sys.path.append("..") 

from mod.vm.vm import *
import json


##########################################
####### Service Snapshot  Test
##########################################

def print_result(ret):
    print json.dumps(ret,indent=4)

def snapshot_test(uuid):
    # print_result(snapshot_list(uuid))

    snapshotname = 'init_zzw_test'
    snapshotmemory = False
    print_result(snapshot_create_init(uuid,snapshotname,snapshotmemory))
    # print_result(snapshot_list(uuid))


win7_uuid = "291fd1d8-ed1e-11eb-9ba2-0cc47a0c5910"
snapshot_test([win7_uuid])
