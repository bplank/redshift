#/usr/bin/env python
import codecs
import sys

for line in codecs.open(sys.argv[1],encoding="utf-8"):
    line=line.strip()
    if line:
        idx,token,pos,head,label = line.split("\t")
        
        print "{0}\t{1}\t_\t{2}\t_\t_\t{3}\t{4}\t_\t_".format(int(idx)+1,token,pos,int(head)+1,label)
    else:
        print
