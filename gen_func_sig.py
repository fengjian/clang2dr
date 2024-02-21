#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import clang.cindex
import json


def get_ts(source_path):
    index = clang.cindex.Index.create()
    return index.parse(source_path)


def gen_func_sig(source_path, func_sig_tables):
    ts = get_ts(source_path)
    child = ts.cursor.get_children()
    for cunit in child:
        if cunit.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            func_arg = {"args":[], "ret":None}
            func_arg["ret"] = cunit.type.get_result().spelling
            for arg in cunit.get_arguments():
                func_arg["args"].append(arg.type.spelling)
            func_sig_tables[cunit.spelling] = func_arg
                

def walk_dir(dirname, output):
    func_sig_tables = {}
    for cur, _dirs, files in os.walk(dirname):
        for f in files:
            if fnmatch.fnmatch(f, "*.h"):
                header_path = os.path.join(cur, f)
                gen_func_sig(header_path, func_sig_tables)

    jstr = json.dumps(func_sig_tables)
    fd = file(output, "w")
    fd.write(jstr)


def main():
    walk_dir(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
