from typing import *
class Button:
    x:int|float
    y:int|float
    width:int|float
    height:int|float
    type:int
    input:Any
    data:Iterable
    path:Iterable
Time=Sequence[int]
class Note:
    time:Time
    x:int|float
    isFake:bool
class Tap(Note):
    ...
class Flick(Note):
    ...
class Drag(Note):
    ...

class Hold(Note):
    #__slots__=["time","x","end","isfake"]
    end:Time
class Event:
    #__slots__=["startTime","endTime","start","end","easing"]
    startTime:Time
    endTime:Time
    start:int|float
    end:int|float
    easing:int
    def getval(self,time:Time) -> int|float:
        ...
class InstantEvent:
    #__slots__=["time","value"]
    time:Time
    value:int|float
class Line:
    color:List[int|float]
    #__slots__=["x","y","rotation","color","width","alpha","color","notes","speed","xEvents","yEvents","rotateEvents","alphaEvents","speedEvents"]
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

