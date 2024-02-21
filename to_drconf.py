#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json



def sig_to_drconfig(sigpath, output):
    output_fd = file(output, "w+")
    func_sig_tables = json.loads(file(sigpath).read())
    for k, v in func_sig_tables.items():
        arr = []
        arr.append(v["ret"])
        arr.append(k)

        remove_const_arr = []
        for arg in v["args"]:
            t = arg.replace("const ", "").replace("unsigned char", "char")
            remove_const_arr.append(t)
        arr = arr + remove_const_arr
        s = "|".join(arr) + "\n"
        output_fd.write(s)


def main():
    sig_to_drconfig(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()


