import os
import sys

global_alloc_list = []
global_alloc_dict = {}

def file_lines(fname):
    i = 0
    with open(fname, encoding='gbk', errors='ignore') as f:
        for line in f:
            i = i+1
    return i + 1

def on_modified():
    global num_lines_before
    global global_alloc_list
    global global_alloc_dict
    global verbose
    line_now = 0
    print("Already index to line " + str(num_lines_before))
    local_alloc_list = []
    local_free_list = []
    tlist = []
    local_alloc_dict = {}
    local_free_dict = {}

    with open("/tmp/debug_dash.log", 'rb') as f:
        for line in f:
            line_now += 1
            if line_now > num_lines_before:
                if b'nng_alloc' in line: # pattern a,nng_alloc,b
                    tlist = line.decode('gbk').split(',')
                    local_alloc_list.append(tlist[1])
                    local_alloc_dict[tlist[1]] = line_now
                elif b'nng_free' in line: # pattern a,nng_free,b
                    tlist = line.decode('gbk').split(',')
                    local_free_list.append(tlist[1])
                    local_free_dict[tlist[1]] = line_now

    tlist.clear()
    for item in local_free_list:
        if item in local_alloc_list:
            tlist.append(item)

    for item in tlist:
        local_alloc_list.remove(item)
        local_free_list.remove(item)

    if len(local_alloc_list) != 0:
        print("New blocks without free:")
        if verbose:
            print("{" + str(len(local_alloc_list)) + "}")
            for i in local_alloc_list:
                print(i, end = "")
                print(" : ", end = "")
                print(local_alloc_dict[i])
        else:
            print("{" + str(len(local_alloc_list)) + "}", end = "")
            print(local_alloc_list)
        global_alloc_list += local_alloc_list
        for i in local_alloc_list:
            global_alloc_dict[i] = local_alloc_dict[i]
        local_alloc_list.clear()

    tlist.clear()
    for item in local_free_list:
        if item in global_alloc_list:
            tlist.append(item)

    for item in tlist:
        global_alloc_list.remove(item)
        local_free_list.remove(item)

    if len(tlist) != 0:
        print("New global blocks decrease:")
        if verbose:
            print("{" + str(len(tlist)) + "}")
            for i in tlist:
                print(i, end = "")
                print(" : ", end = "")
                print(local_free_dict[i], end=" -- ")
                print(global_alloc_dict[i])
                del global_alloc_dict[i]
        else:
            print("{" + str(len(tlist)) + "}", end = "")
            print(tlist)

    if len(local_free_list) != 0:
        print("Warning!!! NO MATCHING ALLOC!!!")
        if verbose:
            print("{" + str(len(local_free_list)) + "}")
            for i in local_free_list:
                print(i, end = "")
                print(" : ", end = "")
                print(local_free_list[i])
        else:
            print("{" + str(len(local_free_list)) + "}")
            print(local_free_list)
        local_free_list.clear()

    num_lines_before = line_now
    local_alloc_dict.clear()
    local_free_dict.clear()

if __name__ == "__main__":
    global num_lines_before
    global verbose
    path = "/tmp/debug_dash.log"
    verbose = 0

    if len(sys.argv) > 1:
        if sys.argv[1] == "v" or sys.argv[1] == "verbose" or sys.argv[1] == "-v":
            verbose = 1

    print("File path: " + path)
    print("Only check the log after runing this script.")

    num_lines_before = file_lines(path)

    try:
        while True:
            input("Enter:")
            on_modified()
            print("\n=============================\n")
    except KeyboardInterrupt:
        sys.exit(0)

"""
"""

