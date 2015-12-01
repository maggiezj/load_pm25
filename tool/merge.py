#!/usr/bin/env python
#coding=utf-8

import os
import os.path
import sys

input_dir = ['/mydata/pm25']

argc = len(sys.argv)
if argc > 1:
    input_dir = sys.argv[1:]

# if not os.path.isdir(input_dir):
#     print "input dir is error"
#     quit()

def main():
    outputfile = ''
    for indir in input_dir:
        if os.path.isdir(indir):
            outputfile += os.path.basename(indir) + "_"
    outputfile = outputfile[0:-1]

    with open(outputfile + '.csv', 'w') as out:
        for indir in input_dir:
            if not os.path.isdir(indir):
                continue
            for root, dirs, files in os.walk(indir):
                for name in files:
                    if name.endswith('.csv'):
                        if name == 'stations.csv':
                            continue
                        with open(os.path.join(root, name)) as f:
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

if __name__ == '__main__':
    main()