#!/usr/bin/env python

fvpc=open('../original/D_mel_wt__atlas_r2.vpc', 'r')
datafname='../intermediate/BDTNPVirtualEmbryo.tsv'
colinfofname='../intermediate/BDTNPColumnInfo.txt'
nucleusfname='../intermediate/BDTNPNucleusNeighbours.tsv'

fdata=open
while(fvpc):
    line = fvpc.readline()

    if line.startswith("# cohort_names"):
        line=line[line.find("[")+1:line.find("]")]
        numCohorts=len(line.split(","))
        print "There are "+str(numCohorts)+" cohorts."

    # write out colinfo
    elif line.startswith("# column_info"):
       line=line[line.find('[')+1:line.find(']')]
       colnames=["x","y","z","Nx","Ny","Nz"]
       fcolinfo=open(colinfofname,'w')
       for idmeta in line.split(";"):
           coldata=idmeta.strip()
           fcolinfo.write(coldata+"\n")
           colnames.append(coldata.split(",")[0].strip("\""))
       fcolinfo.close()

    # get colpos
    elif line.startswith("# column"):
       colpos=[]
       for i in range(numCohorts):
           colpos.append([])
       len_colnames=len(colnames)
       check=0
       for colentry in line[line.find('[')+6:line.find(']')].split(","):
           colid=colentry.strip("\"").split("__")
           cohort=int(colid[1])
           if(cohort<check):
               raise ValueError,"The col names don't go in ascending order for cohort."
           elif(cohort>check):
               check=cohort
           colpos[cohort-1].append(colnames.index(colid[0]))
#       print colpos
      
    elif not line.startswith("#"):
        break


# The vpc file (fvpc) has one line per nucleus
# This script writes out a line for each nucleus per cohort in fdatafile
# fnucleusinfo has one line per nucleus to contain the neighbours of each nucleus id

fdatafile=open(datafname,'w')
fnucleusinfo=open(nucleusfname,'w')
fdatafile.write("nucleus_id\tcohort\t"+"\t".join(colnames)+"\n")
fnucleusinfo.write("nucleus_id\tnum neighbours\tneighbours\n")
count=0
while(True):
    data=line.split(",")
 #   print data
    i=1
    for cohort in range(1,numCohorts+1):
        fdatafile.write(data[0]+"\t"+str(cohort)+"\t")
        trData=[]
        for pos in colpos[cohort-1]:
            trData.extend((pos-len(trData))*["NA"]+[data[i]])
            i=i+1
        fdatafile.write("\t".join(trData)+"\n")
    fnucleusinfo.write(data[0]+"\t"+"\t".join(data[i:]))
    count=count+1
    line = fvpc.readline()
    if(line==""): break  
   
fdatafile.close()
fvpc.close()
fnucleusinfo.close()

           
           




       



