#!/usr/bin/env python
#coding=utf-8

import os
import os.path
import sys

input_dir = '/mydata/pm25'
output_dir = '/mydata/pm25-new'

argc = len(sys.argv)
if argc == 3:
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
elif argc == 2:
    output_dir = sys.argv[1]

if not os.path.isdir(input_dir):
    print "input dir is error"
    quit()

def main():
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for root, dirs, files in os.walk(input_dir):
        for name in files:
            if name.endswith('.csv'):
                if name == 'stations.csv':
                    continue
                with open(os.path.join(root, name)) as f:
                    out = open(os.path.join(output_dir, name), 'w')
                    for line in f:
                        cc = line.split(',')
                        if len(cc) == 21:
                            newline = '\t'.join(cc)
                            out.write(newline)
                        elif len(cc) > 21:
                            newcc1 = cc[0:5]
                            newcc2 = [','.join(cc[5:-15])]
                            newcc3 = cc[-15:]
                            newcc = newcc1+newcc2+newcc3
                            newline = '\t'.join(newcc)
                            out.write(newline)
                        else:
                            out.write(line)
                    out.close()

if __name__ == '__main__':
    main()