#!/usr/bin/python
import sys
from optparse import OptionParser
from operator import itemgetter
#from Colours import *

parser = OptionParser(usage="usage: %prog <final state> [options]")


parser.add_option("-f", "--full", dest="full",
                  action="store_true",
                  default=False,
                  help="Full cross-check, default is False")

parser.add_option("-t", "--type", dest="Type",
                  default="",
                  help="Type of cross-check, default is ''. Chose between nJets, m4l")

(options, args) = parser.parse_args()

full     = options.full
Type     = options.Type




Index = 0;

if    Type == "nJets":  Index = 7
elif  Type == "m4l":    Index = 4
elif  Type == "mZ1":    Index = 5
elif  Type == "mZ2":    Index = 6
elif  Type == "jet1pt": Index = 8
elif  Type == "jet2pt": Index = 9



def channels(listIn):
    iseeee = False
    ismmmm = False
    iseemm = False
    eeee = []
    eemm = []
    mmmm = []
    llll = []
    
    for i,evlist in enumerate(listIn):
        ev = evlist.split(":")
        if  not ev or ev[0]=="" or ev[0]=="#" or ev[0]=="\n": continue
        if    ev[3] == "eeee":  eeee.append(ev)
        elif  ev[3] == "mmmm":  mmmm.append(ev)
        elif  ev[3] == "eemm":  eemm.append(ev)
        llll.append(ev)

    eeee=sorted(eeee, key=itemgetter(2))
    eeee=sorted(eeee, key=itemgetter(1))
    eeee=sorted(eeee, key=itemgetter(0))
    eemm=sorted(eemm, key=itemgetter(2))
    eemm=sorted(eemm, key=itemgetter(1))
    eemm=sorted(eemm, key=itemgetter(0))
    mmmm=sorted(mmmm, key=itemgetter(2))
    mmmm=sorted(mmmm, key=itemgetter(1))
    mmmm=sorted(mmmm, key=itemgetter(0))
    llll=sorted(llll, key=itemgetter(2))
    llll=sorted(llll, key=itemgetter(1))
    llll=sorted(llll, key=itemgetter(0))

    return eeee,eemm,mmmm,llll


def Diff(list1,list2,Type=""):


    isIn = lambda x,c:[y for y in c if (y[0]==x[0] and y[1]==x[1] and y[2]==x[2])]
    diff = lambda c,d:[x for x in c if not len(isIn(x,d))]

    if    Type == "":   return diff(list1,list2)
    else:
        diffList = diff(list1,list2) 
        for i,j in enumerate(diffList):
            list1.remove(j)

    isIn = lambda x,c:[y for y in c if (y[0]==x[0] and y[1]==x[1] and y[2]==x[2] and x[Index]==y[Index])]

    return diff(list1,list2)



def ChechList(lines1,lines2,Type):
    EEEE_1,EEMM_1,MMMM_1,LLLL_1 = channels(lines1)
    EEEE_2,EEMM_2,MMMM_2,LLLL_2 = channels(lines2)
    
    EEEE12_diff = Diff(EEEE_1,EEEE_2,Type)       
    EEEE21_diff = Diff(EEEE_2,EEEE_1,Type)
    EEMM12_diff = Diff(EEMM_1,EEMM_2,Type)
    EEMM21_diff = Diff(EEMM_2,EEMM_1,Type)
    MMMM12_diff = Diff(MMMM_1,MMMM_2,Type)
    MMMM21_diff = Diff(MMMM_2,MMMM_1,Type)
    


    if Type=="":
        print "File 1 eeee",len(EEEE_1),"eemm",len(EEMM_1),"mmmm",len(MMMM_1)
        print "File 2 eeee",len(EEEE_2),"eemm",len(EEMM_2),"mmmm",len(MMMM_2)
        print "event in file 1 not in file2"

        for fin, fin_str in zip((EEEE12_diff,EEMM12_diff,MMMM12_diff),("eeee:","eemm:","mmmm:")):
            print fin_str
            if Type=="": 
                for i in fin:
                    for j in i: 
                        print j,
            else: 
                for i in fin: 
                    for l,j in enumerate(i):
                        if l==Index: print Red(j),
                        else: print j,

        
        print "event in file 2 not in file 1"
        for fin, fin_str in zip((EEEE21_diff,EEMM21_diff,MMMM21_diff),("eeee:","eemm:","mmmm:")):
            print fin_str
            if Type=="":
                for i in fin:
                    for j in i:
                        print j,
            else:
                for i in fin:
                    for l,j in enumerate(i):
                        if l==Index: print Red(j),
                        else: print j,

    else:

        for fin_1, fin_2, fin_str in zip((EEEE12_diff,EEMM12_diff,MMMM12_diff),(EEEE21_diff,EEMM21_diff,MMMM21_diff),("eeee:","eemm:","mmmm:")):
            print fin_str

            for i,j in zip(fin_1,fin_2):
                print "file1",
                for l,m in enumerate(i):
                    if l==Index: print Red(m),
                    else: print m,
                print "file2",
                for l,m in enumerate(j):
                    if l==Index: print Red(m),
                    else: print m,
                print "\n"

filename1 = sys.argv[1]
filename2 = sys.argv[2]


try:
    f = open(filename1, "r")
    g = open(filename2, "r")
    
    try:
        lines1 = f.readlines()
        lines2 = g.readlines()
        print "Difference in events:" 
        ChechList(lines1,lines2,"")
        if Type!="":
            print "Difference in events for ",Type 
            ChechList(lines1,lines2,Type)
        f.close()
        g.close()
    finally:
        g.close()
        f.close()
except IOError:
    pass


