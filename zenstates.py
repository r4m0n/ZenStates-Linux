#!/usr/bin/python
import struct
import os
import glob
import argparse

pstates = range(0xC0010064, 0xC001006C)

def writemsr(msr, val, cpu = -1):
    try:
        if cpu == -1:
            for c in glob.glob('/dev/cpu/[0-9]*/msr'):
                f = os.open(c, os.O_WRONLY)
                os.lseek(f, msr, os.SEEK_SET)
                os.write(f, struct.pack('Q', val))
                os.close(f)
        else:
            f = os.open('/dev/cpu/%d/msr' % (cpu), os.O_WRONLY)
            os.lseek(f, msr, os.SEEK_SET)
            os.write(f, struct.pack('Q', val))
            os.close(f)
    except:
        raise OSError("msr module not loaded (run modprobe msr)")

def readmsr(msr, cpu = 0):
    try:
        f = os.open('/dev/cpu/%d/msr' % cpu, os.O_RDONLY)
        os.lseek(f, msr, os.SEEK_SET)
        val = struct.unpack('Q', os.read(f, 8))[0]
        os.close(f)
        return val
    except:
        raise OSError("msr module not loaded (run modprobe msr)")

def pstate2str(val):
    if val & (1 << 63):
        fid = val & 0xff
        did = (val & 0x3f00) >> 8
        vid = (val & 0x3fc000) >> 14
        ratio = 25*fid/(12.5 * did)
        vcore = 1.55 - 0.00625 * vid
        return "Enabled - FID = %X - DID = %X - VID = %X - Ratio = %.2f - vCore = %.5f" % (fid, did, vid, ratio, vcore)
    else:
        return "Disabled"

def setbits(val, base, length, new):
    return (val ^ (val & ((2 ** length - 1) << base))) + (new << base)

def setfid(val, new):
    return setbits(val, 0, 8, new)

def setdid(val, new):
    return setbits(val, 8, 6, new)

def setvid(val, new):
    return setbits(val, 14, 8, new)

def hex(x):
    return int(x, 16)

parser = argparse.ArgumentParser(description='Sets P-States for Ryzen processors')
parser.add_argument('-l', '--list', action='store_true', help='List all P-States')
parser.add_argument('-p', '--pstate', default=-1, type=int, choices=range(8), help='P-State to set')
parser.add_argument('--enable', action='store_true', help='Enable P-State')
parser.add_argument('--disable', action='store_true', help='Disable P-State')
parser.add_argument('-f', '--fid', default=-1, type=hex, help='FID to set (in hex)')
parser.add_argument('-d', '--did', default=-1, type=hex, help='DID to set (in hex)')
parser.add_argument('-v', '--vid', default=-1, type=hex, help='VID to set (in hex)')
parser.add_argument('--c6-enable', action='store_true', help='Enable C-State C6')
parser.add_argument('--c6-disable', action='store_true', help='Disable C-State C6')

args = parser.parse_args()

if args.list:
    for p in range(len(pstates)):
        print('P' + str(p) + " - " + pstate2str(readmsr(pstates[p])))
    print('C6 State - Package - ' + ('Enabled' if readmsr(0xC0010292) & (1 << 32) else 'Disabled'))
    print('C6 State - Core - ' + ('Enabled' if readmsr(0xC0010296) & ((1 << 22) | (1 << 14) | (1 << 6)) == ((1 << 22) | (1 << 14) | (1 << 6)) else 'Disabled'))

if args.pstate >= 0:
    new = old = readmsr(pstates[args.pstate])
    print('Current P' + str(args.pstate) + ': ' + pstate2str(old))
    if args.enable:
        new = setbits(new, 63, 1, 1)
        print('Enabling state')
    if args.disable:
        new = setbits(new, 63, 1, 0)
        print('Disabling state')
    if args.fid >= 0:
        new = setfid(new, args.fid)
        print('Setting FID to %X' % args.fid)
    if args.did >= 0:
        new = setdid(new, args.did)
        print('Setting DID to %X' % args.did)
    if args.vid >= 0:
        new = setvid(new, args.vid)
        print('Setting VID to %X' % args.vid)
    if new != old:
        if not (readmsr(0xC0010015) & (1 << 21)):
            print('Locking TSC frequency')
            for c in range(len(glob.glob('/dev/cpu/[0-9]*/msr'))):
                writemsr(0xC0010015, readmsr(0xC0010015, c) | (1 << 21), c)
        print('New P' + str(args.pstate) + ': ' + pstate2str(new))
        writemsr(pstates[args.pstate], new)

if args.c6_enable:
    writemsr(0xC0010292, readmsr(0xC0010292) | (1 << 32))
    writemsr(0xC0010296, readmsr(0xC0010296) | ((1 << 22) | (1 << 14) | (1 << 6)))
    print('Enabling C6 state')

if args.c6_disable:
    writemsr(0xC0010292, readmsr(0xC0010292) & ~(1 << 32))
    writemsr(0xC0010296, readmsr(0xC0010296) & ~((1 << 22) | (1 << 14) | (1 << 6)))
    print('Disabling C6 state')

if not args.list and args.pstate == -1 and not args.c6_enable and not args.c6_disable:
    parser.print_help()
