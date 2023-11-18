from typing import *
import pygame
from pygame.locals import *
import head
import string
import copy
import easing
from dummy import *
from math import *
class new:...
class delete:...
class delany:...
def getPath(root,path:List | Any)->Any:
    n=root
    for i in path:
        if type(n) in (list,dict):
            if type(i) is list:
                i=getPath(head.root,i)
            if callable(i):
                n=i(n)
                return n
            n=n[i]
        else:
            if type(i) is list:
                i=getPath(head.root,i)
            if callable(i):
                n=i(n)
                return n
            n=n.__getattribute__(i)
    return n
def dec(path)->None:
    setPath(path,getPath(head.root,path)-1)
def inc(path)->None:
    setPath(path,getPath(head.root,path)+1)
def setPath(path:List | Any,*val) -> None:
    if type(path) is tuple:
        for p,v in zip(path,val):
            setPath(p,*v)
    if isinstance(path,List):
        n:List=getPath(head.root,path[:-1])
        m=getPath(head.root,path[:-2])
        if type(n) in (list,dict):
            
            if path[-1] == new:
                n.append(copy.deepcopy(val[0]))
                return
            elif path[-1]==delete:
                if m[:-1]:
                    del m[path[-2]]
                    if val:dec([val[0]])
                return
            elif path[-1]==delany:
                del m[path[-2]]
                return
            n[path[-1]]=val[0]
        elif type(m) in (list,dict):
            if path[-1]==delete:
                if m[:-1]:
                    if type(path[-2]) is list:n=getPath(head.root,path[-2])
                    else:n=path[-2]
                    del m[n]
                    dec([val[0]])
                return
            elif path[-1]==delany:
                del m[path[-2]]
                head.root["menu"].clear()
                return
            n.__setattr__(path[-1],val[0])
        else:
            
            n.__setattr__(path[-1],val[0])
    else:
        match path:
            case "newb":
                v=val[:]
                for i in v:
                    newButton(head.root["menu"],*i)
                    if (i[0]) in (head.GBUTTON_TEXT,head.GBUTTON_INT,head.GBUTTON_FLOAT,head.GBUTTON_TIME):
                        head.root["menu"][-1].fro=i[1]
            case "delm":
                head.root["menu"].clear()
def timeToList(x:str) -> List:
    r=[0,0,0];i=0
    for n in x:
        if n ==":":i=1
        elif n=="/":i=2
        else:r[i]=r[i]*10+int(n)
    if r[2]==0:r[2]=1
    return r
def listToFloat(x:List)->float:
    return x[0]+x[1]/x[2]
def listToTime(x:List) -> str:
    return f"{x[0]}:{x[1]}/{x[2]}"
def floatToList(x:float|int)->List[int]:
    f=int(x)
    p=x-f
    for i in range(1,9):
        if abs(round(p*i)-p*i)<1e-10:
            return [f,int(p*i),i]
    return [f,int(p*100),100]
class Button:
    def __init__(self,x:int|float,y:int|float,width:int|float,height:int|float,title:str,type:int,input:Any,data:Iterable,path:Iterable) -> None:
        self.x:int|float=x
        self.y:int|float=y
        self.width:int|float=width
        self.height:int|float=height
        self.title:str=title
        self.type:int=type
        self.input:Any=input
        self.data:Iterable=data
        self.path:Iterable=path
        self.bind:int=0
        self.fro:List=None
        pass
    def drawText(self,dest:pygame.Surface,v) -> None:
        if type(v) is list:v=getPath(head.root,v)
        s:pygame.Surface=head.font.render(v[:min(15,len(v))],(0,0,0))[0]
        dest.blit(s,(self.x-s.get_width()/2,self.y-s.get_height()/2))
    def draw(self,dest:pygame.Surface) -> None:
        pygame.draw.rect(dest,(127+8*self.bind,127+8*self.bind,127+8*self.bind),(self.x-self.width/2,self.y-self.height/2,self.width,self.height))
        if type(self.input)is list:self.input=getPath(head.root,self.input)
        head.font.render_to(dest,(20,self.y-16),self.title,(255,255,255))
        match self.type:
            case head.GBUTTON_TEXT|head.GBUTTON_INT|head.GBUTTON_FLOAT|head.GBUTTON_TIME:
                self.drawText(dest,self.input if self.input else self.data[0])
            case head.GBUTTON_BUTTON:
                self.drawText(dest,self.input)
            case head.GBUTTON_CHOOSE:
                if self.input>=len(self.data):self.input=len(self.data)-1
                self.drawText(dest,self.data[self.input] if type(self.data[self.input]) is str else str(self.input))
            case head.GBUTTON_BOOL:
                pygame.draw.rect(dest,(255-255*(int(self.input)),self.input*255,0),
                (self.x+self.width*(1/2*int(self.input)-1/2),self.y-self.height/2,self.width*1/2,self.height))
                self.drawText(dest,self.data[0])
    def __bool__(self) -> bool:return True
    def update(self,mse,kbd:Sequence[str],kmod:Dict,inp:str) -> None:
        
        match self.type:
            case head.GBUTTON_TEXT|head.GBUTTON_INT|head.GBUTTON_FLOAT|head.GBUTTON_TIME:
                caps=kmod["capslock"]
                caps=(caps or kmod["shift"])and(not(caps and kmod["shift"]))
                if inp:
                    self.input+=inp
                    return
                for key in kbd:
                    if key=="backspace":
                        if self.input:
                            self.input=self.input[:-1]
                    elif len(key)==1:
                        if key =="c":
                            if kmod["control"]:
                                pygame.scrap.put(pygame.SCRAP_TEXT,self.input.encode("utf-8"))
                            else:
                                if caps:self.input+=key.capitalize()
                                else:self.input+=key
                        elif key =="v":
                            if kmod["control"]:
                                try:
                                    self.input+=pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")
                                except UnicodeDecodeError:
                                    self.input+=pygame.scrap.get(pygame.SCRAP_TEXT).decode("gbk")
                            else:
                                if caps:self.input+=key.capitalize()
                                else:self.input+=key
                try:
                    match self.type:
                        case head.GBUTTON_TEXT:
                            setPath(self.path,self.input)
                        case head.GBUTTON_INT:
                            setPath(self.path,int(self.input if self.input.isnumeric() else 0))
                        case head.GBUTTON_FLOAT:
                            setPath(self.path,float(self.input if self.input and not (
                                self.input[0] in (".","") 
                                or self.input[-1] in ("-",".") 
                                )else 0.)) 
                        case head.GBUTTON_TIME:
                            setPath(self.path,timeToList(self.input))
                except Exception:
                    ...
            case head.GBUTTON_BUTTON:
                if mse.press[0]:setPath(self.path,*self.data)
            case head.GBUTTON_CHOOSE:
                if mse.press[0]:self.input+=1
                if "up" in kbd:
                    self.input-=1
                if "down" in kbd:
                    self.input+=1
                if self.input<0:
                    self.input=len(self.data)-1
                if self.input>=len(self.data):
                    self.input=0
                setPath(self.path,self.input)
            case head.GBUTTON_BOOL:
                if mse.press[0]:
                    self.input=1- self.input
                setPath(self.path,int(self.input))
def newButton(buttonList,title:str,type:int,input:Any,data:Iterable,path:Iterable) -> Button:
    buttonList.append(
        Button(
            250,
            50+50*(
                len(
                    buttonList
                )
            ),
            200,
            45,
            title,
            type,input,data,path
        )
    )

def newMenu(*buttons:Sequence[Tuple]):
    l=[]
    for button in buttons:
        newButton(l,*button)
    return l
    ...
class Note:
    time:Time
    x:int|float
    isFake:bool
    above:bool
    def __init__(self,time:Time=[0,0,1],x:int|float=0,isFake:bool=False) -> None:
        self.time=time
        self.x=x
        self.isFake=isFake
class Tap(Note):
    __slots__=["time","x","isFake","above"]
    def __init__(self, time: Time = [0, 0, 1], x: int | float = 0, isFake: bool = False) -> None:
        super().__init__(time, x, isFake)
    ...
class Flick(Note):
    __slots__=["time","x","isFake","above"]
    def __init__(self, time: Time = [0, 0, 1], x: int | float = 0, isFake: bool = False) -> None:
        super().__init__(time, x, isFake)
    ...
class Drag(Note):
    __slots__=["time","x","isFake","above"]
    def __init__(self, time: Time = [0, 0, 1], x: int | float = 0, isFake: bool = False) -> None:
        super().__init__(time, x, isFake)
    ...    
class Hold(Note):
    __slots__=["time","x","end","isFake","above"]
    end:List[int]
    def __init__(self,time:Time=[0,0,1],end:Time=[0,0,1],x:int|float=0,isFake:bool=False) -> None:
        self.time=time
        self.x=x
        self.isFake=isFake
        self.end=end

class Event:
    __slots__=["startTime","endTime","start","end","easing"]
    startTime:List[int]
    endTime:List[int]
    start:int|float
    end:int|float
    easing:int
    def __init__(self,startTime:Time=[0,0,1],endTime:Time=[0,0,1],start:int|float=0,end:int|float=False,easing:int=1) -> None:
        self.startTime=startTime
        self.endTime=endTime
        self.start=start
        self.end=end
        self.easing=easing
    def getval(self,time):
        return easing.code2FuncDict[self.easing](listToFloat(self.startTime),listToFloat(self.endTime),self.start,self.end).calculate(time)

class InstantEvent:
    __slots__=["time","value"]
    time:List[int]
    value:int|float
    def __init__(self,time:Time=[0,0,1],value:int|float=0) -> None:
        self.time=time
        self.value=value
class Line:
    color:List[int|float]
    __slots__=["x","y","rotation","color","width","alpha","color","notes","speed","xEvents","yEvents","rotateEvents","alphaEvents","speedEvents"]
    x:int|float
    y:int|float
    rotation:int|float
    width:int|float
    alpha:int|float
    notes:List[Note]
    speed:int|float
    xEvents:List[Event]
    yEvents:List[Event]
    rotateEvents:List[Event]
    alphaEvents:List[Event]
    speedEvents:List[InstantEvent]
    def __init__(self) -> None:
        self.x=0
        self.y=0
        self.rotation=0
        self.width=3600
        self.alpha=0
        self.speed=0
        self.color=(255,255,255)
        self.notes=[]
        self.xEvents=[]
        self.yEvents=[]
        self.rotateEvents=[]
        self.alphaEvents=[]
        self.speedEvents=[]
        pass

    def update(self,time):
        self.x=EventLoad(self.xEvents,time)
        self.y=EventLoad(self.yEvents,time)
        self.rotation=EventLoad(self.rotateEvents,time)
        self.alpha=EventLoad(self.alphaEvents,time)
        self.speed=InstantEventsLoad(self.speedEvents,time,1)
def InstantEventsLoad(events:List[InstantEvent],time,mode):
    if not events:return 0
    if time is None:return 0
    events.sort(key=lambda e:listToFloat((e.time)))
    match mode:
        case 0:#event
            n=0
            
            for e in events:
                et=listToFloat((e.time))
                if time<et:return n
                n=e.value
            return n
        case 1:#speed
            n=0
            events=events+[InstantEvent([inf,0,1],events[-1].value)]
            for i,e in enumerate(events[:-1]):
                nt=listToFloat((events[i+1].time))
                et=listToFloat((e.time))
                if time <nt:return n+(time-et)*e.value
                n+=e.value*(nt-et)
            
        case 2:#BPM
            n=0
            events=events+[InstantEvent([inf,0,1],events[-1].value)]
            for i,e in enumerate(events[:-1]):
                if not e.value:return 0
                nt=listToFloat((events[i+1].time))
                et=listToFloat((e.time))
                if time <(nt-et)*e.value:return n+time*e.value/60
                n+=(nt-et)
                time-=(nt-et)/e.value*60
            ...
    return 0
def EventLoad(events:List[Event],time):
    if not events:return 0
    if time is None:return 0
    events.sort(key=lambda e:listToFloat((e.startTime)))
    le=Event()
    le.startTime=[-inf,0,1]
    le.endTime=[0,0,1]
    le.start=0
    le.end=0
    le.easing=1
    for e in events:
        st=listToFloat((e.startTime))
        et=listToFloat((e.endTime))
        if time>=st and time<et:return e.getval(time)
        elif time<st:return le.end
        le=e
    return events[-1].end
