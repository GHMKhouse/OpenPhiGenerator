#!usr/bin/env python
#coding=utf-8
 
import pyaudio
import wave
from head import filepath
from io import BytesIO
from glob import glob
import ffmpy
#define stream chunk 
chunk = 1024
playing=0
#open a wav format music
n=0;x=""
for p in (a:=glob(filepath+"\\music.*")):
    if p.split(".")[-1]=="wav":
        n=1
        x=p
        break
if not n:
    ffmpy.FFmpeg(inputs={p:None},outputs={p.replace("."+p.split(".")[-1],".wav"):None}).run()
    x=p.replace("."+p.split(".")[-1],".wav")
with open(x,"rb") as f:
        byt=BytesIO(f.read())
        rb=wave.open(byt,"rb")
f1=rb.getframerate()
def fps():
    return rb.getframerate()
def alen():
    return rb.getnframes()/rb.getframerate()
def play(pos=0,mul=1):
    global playing,rb,chunk
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    rb.setpos(int(pos*fps()))
    #open stream
    stream = p.open(format = p.get_format_from_width(rb.getsampwidth()),
                    channels = rb.getnchannels(),
                    rate = int(rb.getframerate()*mul),
                    output = True)
    #read data
    data = rb.readframes(chunk)
    playing=1
    #paly stream
    while data != '' and playing:
        stream.write(data)
        data = rb.readframes(chunk)
    
    #stop stream
    stream.stop_stream()
    stream.close()
    
    #close PyAudio
    p.terminate()
    return 0
def stop():
    global playing
    playing=0
def gettime():
    global rb
    return rb.tell()