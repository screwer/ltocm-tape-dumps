#!/usr/bin/env python3

#import sys
import os
import re

#-----------------------------------------------------------------

def search_list(str_list, substr):
    idx = 0
    for s in str_list:
        if substr in s:
            return idx
        idx += 1

#-----------------------------------------------------------------

def cmp_files(root, fname_1, fname_2):

    if len(fname_1) > len(fname_2):
        fname_1, fname_2 = fname_2, fname_1


    msg = f'At "{root}" comparing "{fname_1}" and "{fname_2}": '

    fpath_1 = os.path.join(root, fname_1)
    with open(fpath_1, 'rb') as f:
        bin_1 = f.read()
    sz_1 = len(bin_1)

    fpath_2 = os.path.join(root, fname_2)
    with open(fpath_2, 'rb') as f:
        bin_2 = f.read()
    sz_2 = len(bin_2)

    sz_min = min(sz_1, sz_2)
    if bin_1[:sz_min] != bin_2[:sz_min]:
        for idx in range(sz_min):
            if bin_1[idx] != bin_2[idx]:
                msg += 'Difference found at: %x' % idx
                return msg
    
    if sz_1 > sz_min:
        sz_pad = sz_1 - sz_min
        if bin_1[sz_min:] == b'\x00':
            msg += 'Equal, but first is zero-padded'
            return msg

        msg += 'First have some data in tail'
        return msg


    elif sz_2 > sz_min:
        sz_pad = sz_2 - sz_min
        if bin_2[sz_min:] == b'\x00':
            msg += 'Equal, but second is zero-padded'
            return msg

        msg += 'Second have some data in tail'
        return msg

    msg += 'Equal'
    return msg

#-----------------------------------------------------------------

def walk_dumps():

    re_serial_text = '^(hf-lto-|L[1-6]-|CLN-)?(?P<serial>[0-9a-fA-F]+).*.bin$'
    re_serial = re.compile(re_serial_text)

    for root, dirs, files in os.walk("."):
        #
        # Skip git folders
        #
        if root.startswith('./.git'): continue

        #
        # Process only ".bin" files
        #
        names = [name for name in files if name.endswith('.bin')]
        if not names: continue
              
        while names:
            name = names.pop()
            m = re_serial.match(name)
            if not m:
                print('WARNING! Serial number not found for: "%s"' % name)
                continue

            serial = m.group('serial')
            if len(serial) > 8:
                #
                # proxmark3 generates 10-char serials
                #
                serial = serial[:8]

            idx = search_list(names, serial)
            if idx is None:
                #print('WARNING! Pair file for "%s" not found! (at "%s")' % (name, root))
                continue

            msg = cmp_files(root, name, names[idx])
            if msg:
                print(msg)

            del names[idx]

#-----------------------------------------------------------------

def main():
    walk_dumps()

#-----------------------------------------------------------------

main()