# 获取 当前系统信息

import platform

import wmi
import pywin

def get_osinfo()->dict:
    """
    获取系统相关信息
    return dict 
    {
        'system': 'Windows', 
        'version': '6.1.7601', 
        'python_version': '3.8.3', 
        'sys_bit': 'AMD64'
    }
    """
    sysinfo={
        "system":platform.system(),
        "version":platform.version(),
        "python_version":platform.python_version(),
        "sys_bit":platform.machine()
        # "uname":platform.uname()
    }
    return sysinfo


def get_win_info():
    info = {}
    c = wmi.WMI()
    #获取主板序列号 
    # 硬盘序列号
    disk_sns =[]
    for physical_disk in c.Win32_DiskDrive():
        disk_sn = physical_disk.SerialNumber
        if disk_sn is None:
            continue
        disk_sns.append(disk_sn)
        info['disks_sn'] = disk_sns

    # CPU序列号
    cpus_sn =[]
    for cpu in c.Win32_Processor():
        cpu_sn = cpu.ProcessorId.strip()
        if cpu_sn is None:
            continue
        cpus_sn.append(cpu_sn)
        info['cpus_sn'] = cpus_sn

    # 主板序列号
    boards_sn =[]
    for board in c.Win32_BaseBoard():
        board_sn = board.SerialNumber
        
        if board_sn is None:
            continue
        boards_sn.append(board_sn)
        info['boards_sn'] = boards_sn

    # mac地址
    _mac =[]
    for mac in c.Win32_NetworkAdapter():
        macaddress = mac.MACAddress
        if macaddress is None:
            continue
        _mac.append(macaddress)
        info['mac'] = _mac

    # bios序列号
    bios_sn =[]
    for bios in c.Win32_BIOS():
        _bios_sn = bios.SerialNumber.strip()
        if _bios_sn is None:
            continue
        bios_sn.append(_bios_sn)
        info['bios_sn'] = bios_sn

    return info    

def get_linux_info():
    pass

def get_pc_info():
    system_info = get_osinfo()
    if system_info['system'] == 'Linux':
        get_win_info()
        pass
    elif system_info['system'] == 'Windows':
        pass

    else:
        print("Unknow system_info Error")

if __name__ == "__main__":
    # test()
    print(get_win_info())