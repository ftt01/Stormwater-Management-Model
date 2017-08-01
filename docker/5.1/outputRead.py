#!/usr/bin/python

import os
import sys
import shutil
import struct
import datetime

recordSize = 4
outFile = sys.argv[1]
#open the file output
with open(outFile, "rb+") as openedFile:
    data = openedFile.seek(0, 2)
    if openedFile.tell() < 14*recordSize: error = 1

#read the data from the end of file
    openedFile.seek(-5*recordSize, 2)
    #print(openedFile.tell())
    offsetZero = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(offsetZero)
    startPos = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(startPos)
    SWMM_nPeriods = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(SWMM_nPeriods)
    errorCode = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(errorCode)
    magicTwo = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(magicTwo)

#read the magic number from the beginning of the file
    openedFile.seek(0, 0)
    magicOne = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(magicOne)

#check for errors
    if magicOne != magicTwo:
        errorFlag = 1
        #print(errorFlag)
    elif errorCode != 0:
        errorFlag = 1
        #print(errorFlag)
    elif SWMM_nPeriods == 0: 
        errorFlag = 1
        #print(errorFlag)
    else: errorFlag = 0

    if errorFlag == 1:
        openedFile.close()
        openedFile = 0
        error = errorFlag

    #print(errorFlag)
    #print(error)

#read the other metadata
    version = struct.unpack('i', openedFile.read(recordSize*1))[0]
    SWMM_flowUnits = struct.unpack('i', openedFile.read(recordSize*1))[0]
    SWMM_nSubcatch = struct.unpack('i', openedFile.read(recordSize*1))[0]
    SWMM_nNodes = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(SWMM_nNodes)
    SWMM_nLinks = struct.unpack('i', openedFile.read(recordSize*1))[0]
    SWMM_nPollutsLinks = struct.unpack('i', openedFile.read(recordSize*1))[0]
   
#evaluate skip over saved input values
    offset = (SWMM_nSubcatch+2)*recordSize +    \
            (3*SWMM_nNodes+4)*recordSize +      \
            (5*SWMM_nLinks+6)*recordSize            
    offset = offsetZero + offset
    #print(offset)  

#create the directory tree
    if os.path.exists(sys.argv[2]):
        shutil.rmtree(sys.argv[2])
    os.mkdir(sys.argv[2], 0o444)
    os.chdir(sys.argv[2])
    os.mkdir('./subcatchments', 0o444)
    os.mkdir('./nodes', 0o444)
    os.mkdir('./links', 0o444)

#create the files with ID names
    subcatchmentsName = []
    for i in range(SWMM_nSubcatch):
        varLength = struct.unpack('i', openedFile.read(recordSize*1))[0]
        varName = openedFile.read(varLength)
        
        subcatchmentsName.append(varName.decode())
        #print(subcatchmentsName[0])

        os.chdir('./subcatchments')
        tmpFile = open(varName, 'w')
        tmpFile.close()
        os.chdir('../')
    
    nodesName = []
    for i in range(SWMM_nNodes):
        varLength = struct.unpack('i', openedFile.read(recordSize*1))[0]
        varName = openedFile.read(varLength)

        nodesName.append(varName.decode())
        #print(subcatchmentsName[0])

        os.chdir('./nodes')
        tmpFile = open(varName, 'w')
        tmpFile.close()
        os.chdir('../')
    
    linksName = []
    for i in range(SWMM_nLinks):
        varLength = struct.unpack('i', openedFile.read(recordSize*1))[0]
        varName = openedFile.read(varLength)
        
        linksName.append(varName.decode())
        #print(subcatchmentsName[0])

        os.chdir('./links')
        tmpFile = open(varName, 'w')
        tmpFile.close()
        os.chdir('../')

    openedFile.seek(offset, 0)

#read number and codes of computed variables
    #subcatch variables
    subcatchVars = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(subcatchVars)
    openedFile.seek(subcatchVars*recordSize, 1)
    #node variables
    nodeVars = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(nodeVars)
    openedFile.seek(nodeVars*recordSize, 1)
    #link variables
    linkVars = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(linkVars)
    openedFile.seek(linkVars*recordSize, 1)   
    #system variables
    sysVars = struct.unpack('i', openedFile.read(recordSize*1))[0]
    #print(sysVars)


#read data just before the output results
    offset = startPos - 3*recordSize
    openedFile.seek(offset, 0) 
    SWMM_startDate = struct.unpack('d', openedFile.read(8))[0]
#    print(SWMM_startDate)
    days = int(SWMM_startDate)
    seconds = (SWMM_startDate - days)*86400
    startDate = datetime.datetime(1899, 12, 30) + \
                datetime.timedelta(days=days, seconds=seconds)
#    print(startDate)
    SWMM_reportStep = struct.unpack('i', openedFile.read(recordSize*1))[0]
#    print(SWMM_reportStep)

#compute number of bytes of results values used per time period
    bytesPerPeriod = 2*recordSize +                 \
                    (SWMM_nSubcatch*subcatchVars +  \
                    SWMM_nNodes*nodeVars +          \
                    SWMM_nLinks*linkVars +          \
                    sysVars)*recordSize

#    openedFile.close()

#open and write a new csv file
#subcatchments
    os.chdir('./subcatchments')
    for iIndex in range(SWMM_nSubcatch):
        reportStep = SWMM_reportStep 
        with open(subcatchmentsName[iIndex], 'a') as subFile:
            subFile.write('time,'+'rainfall,'+'snow_depth,'+'evap_loss,'+ \
                    'infiltr_loss,'+'runoff_rate,'+'gw_out_rate,'+'gw_elev,'+ \
                    'unsat_moisture,'+'poll_conc'+'\n')
##add pollution if necessary
            for period in range(1,SWMM_nPeriods+1):
                outDate = startDate + datetime.timedelta(seconds=reportStep)
                subFile.write(outDate.strftime("%x %X")+',')
                for vIndex in range(subcatchVars):   
                    offsetZero = startPos + (period - 1)*bytesPerPeriod + 2*recordSize
                    offset = offsetZero + recordSize*(iIndex*subcatchVars + vIndex)
                    openedFile.seek(offset, 0)
                    temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                    subFile.write(str(round(temporaryValue,4))+',')
                offsetZero = startPos + (SWMM_nPeriods - 1)*bytesPerPeriod + 2*recordSize
                offset = offsetZero + recordSize*(iIndex*subcatchVars + subcatchVars)
                openedFile.seek(offset, 0)
                temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                subFile.write(str(round(temporaryValue,4))+'\n')
                reportStep += SWMM_reportStep
        subFile.close()
#nodes
    os.chdir('../nodes')
    for iIndex in range(SWMM_nNodes):
        reportStep = SWMM_reportStep 
        with open(nodesName[iIndex], 'a') as nodeFile:
            nodeFile.write('time,'+'invert_depth,'+'hydraulic_head,'+'volume,'+ \
                    'lateral_inflow,'+'total_inflow,'+'flow_lost,'+'poll_conc'+'\n')
##add pollution if necessary
            for period in range(1,SWMM_nPeriods+1):
                outDate = startDate + datetime.timedelta(seconds=reportStep)
                nodeFile.write(outDate.strftime("%x %X")+',')
                for vIndex in range(nodeVars):
                    offsetZero = startPos + (period - 1)*bytesPerPeriod + 2*recordSize
                    offset = offsetZero + recordSize*(SWMM_nSubcatch*subcatchVars + iIndex*nodeVars + vIndex)
                    openedFile.seek(offset, 0)
                    temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                    nodeFile.write(str(round(temporaryValue,4))+',')
                offsetZero = startPos + (SWMM_nPeriods - 1)*bytesPerPeriod + 2*recordSize
                offset = offsetZero + recordSize*(SWMM_nSubcatch*subcatchVars + iIndex*nodeVars + nodeVars)
                openedFile.seek(offset, 0)
                temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                nodeFile.write(str(round(temporaryValue,4))+'\n')
                reportStep += SWMM_reportStep
        nodeFile.close()
#links
    os.chdir('../links')
    for iIndex in range(SWMM_nLinks):
        reportStep = SWMM_reportStep 
        with open(linksName[iIndex], 'a') as linkFile:
            linkFile.write('time,'+'flow_rate,'+'flow_depth,'+'flow_velocity,'+ \
                    'flow_volume,'+'filled_area,'+'poll_conc'+'\n')
##add pollution if necessary
            for period in range(1,SWMM_nPeriods+1):
                outDate = startDate + datetime.timedelta(seconds=reportStep)
                linkFile.write(outDate.strftime("%x %X")+',')
                for vIndex in range(linkVars):   
                    offsetZero = startPos + (period - 1)*bytesPerPeriod + 2*recordSize
                    offset = offsetZero + recordSize*(SWMM_nSubcatch*subcatchVars + \
                            SWMM_nNodes*nodeVars + iIndex*linkVars + vIndex)
                    openedFile.seek(offset, 0)
                    temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                    linkFile.write(str(round(temporaryValue,4))+',')
                offsetZero = startPos + (SWMM_nPeriods - 1)*bytesPerPeriod + 2*recordSize
                offset = offsetZero + recordSize*(SWMM_nSubcatch*subcatchVars + \
                        SWMM_nNodes*nodeVars + iIndex*linkVars + linkVars)
                openedFile.seek(offset, 0)
                temporaryValue = struct.unpack('f', openedFile.read(recordSize*1))[0]
                linkFile.write(str(round(temporaryValue,4))+'\n')
                reportStep += SWMM_reportStep
        linkFile.close()
