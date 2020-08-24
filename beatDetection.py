import pyaudio
import wave
import time
import numpy as np
import math
def beatDetection(filename):
    beatLst=beatAnalysis(filename)
    newLst=[]
    for i in range (1,len(beatLst)-1):
        #previous2Beat=beatLst[i-2][1]
        previousBeat=beatLst[i-1][1]
        nextBeat=beatLst[i+1][1]
        #next2Beat=beatLst[i+2][1]
        currentBeat=beatLst[i][1]
        if ((previousBeat<currentBeat or currentBeat<nextBeat)):
            newLst.append((beatLst[i][0],beatLst[i][1]))
    i=0
    finalLst=[]
    while i<len(newLst):
        n=0
        beatLst=[]
        while i+n<len(newLst) and abs(newLst[n+i][1]-newLst[i][1])<=newLst[i][1]**0.5:
            beatLst.append(newLst[i+n][1])
            n+=1
        maxBeat=max(beatLst)
        for j in range (len(beatLst)):
            if beatLst[j]==maxBeat:
                index=j
        finalLst.append(newLst[i+j])
        i=i+n
    return finalLst

def beatAnalysis(filename):
    CHUNK_SIZE=2048
    FORMAT=pyaudio.paInt16
    RATE=44100
    CHANNEL=1
    wf=wave.open(filename,"rb")
    p=pyaudio.PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data=wf.readframes(CHUNK_SIZE)
    total=0
    instantHistory=[0 for i in range (43)]
    timeList=[]
    while len(data)!=0:
        total+=2048
        result=np.fromstring(data, dtype=np.int16).astype(np.int)
        instantE=np.dot(result,result) / 0xffffffff
        aveLocalE=0
        for i in range (43):
            aveLocalE+=instantHistory[i]
        aveLocalE/=43
        varE=0
        #formula from http://archive.gamedev.net/archive/reference/programming/features/beatdetection/index.html
        for i in range (43):
            varE+=(instantHistory[i]-aveLocalE)**2
        varE/=43
        c=(-0.0000015*varE)+1.5142857 #constant from http://mziccard.me/2015/05/28/beats-detection-algorithms-1/
        instantHistory.pop()
        instantHistory.insert(0,instantE)
        diff=int(abs(instantE)-abs(aveLocalE))
        time=round(total/44100,1)
        # if diff>0:
        #     timeList.append((time,instantE))
        if abs(instantE)>abs(c*aveLocalE) and abs(instantE)>1:
            time=round(total/44100,1)
            if timeList==[]:
                timeList.append((time,diff))
            else:
                if time!=timeList[-1][0] and diff!=timeList[-1][1]:
                    timeList.append((time,instantE))
        data=wf.readframes(CHUNK_SIZE)
    p.terminate()
    return timeList

def beatLevel(list):
    (minBeat,maxBeat)=(100,0)
    for beat in list:
        if beat[1]<minBeat:
            minBeat=beat[1]
        if beat[1]>maxBeat:
            maxBeat=beat[1]
    beatDiff=maxBeat-minBeat
    level0=minBeat
    level1=minBeat+beatDiff*0.6
    level2=level1+beatDiff*0.2
    level3=level2+beatDiff*0.1
    return (level0,level1,level2,level3)