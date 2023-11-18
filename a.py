import re
s:str="""        for i,e in enumerate(line.xEvents):
            if type(e) is InstantEvent:
                y=(listToFloat(e.time)-time)*800/root["hlines"]#floatToList((800-mse.y)*root["hlines"]/800+time)
                if y>800:break
                if gfx.rect(game,(255,255,255),(50,795-y,100,10),border_radius=1).collidepoint(mse.x-400,mse.y) and mse.press[0]:
                    setPath("newb",["<",GBUTTON_BUTTON,"<Event",[],"delm"])
                    setPath("newb",["Time",GBUTTON_TIME,["Lines",["lineno"],"xEvents",i,"time",listToTime],["time:"],["Lines",["lineno"],"xEvents",i,"time"]])
                    setPath("newb",["Value",GBUTTON_FLOAT,["Lines",["lineno"],"xEvents",i,"value",str],["value:"],["Lines",["lineno"],"xEvents",i,"value"]])
                    setPath("newb",["delete",GBUTTON_BUTTON,"delete",[4],["Lines",["lineno"],"xEvents",i,delany]])
            else:
                e:Event
                y1=(listToFloat(e.startTime)-time)*800/root["hlines"]
                if y1>800:break
                y2=(listToFloat(e.endTime)-time)*800/root["hlines"]
                if gfx.rect(game,(255,255,255),(50,795-y2,100,10+y2-y1),border_radius=1).collidepoint(mse.x-400,mse.y) and mse.press[0]:
                    setPath("newb",["<",GBUTTON_BUTTON,"<xEvent",[],"delm"])
                    setPath("newb",["StartTime",GBUTTON_TIME,["Lines",["lineno"],"xEvents",i,"startTime",listToTime],["startTime:"],["Lines",["lineno"],"xEvents",i,"startTime"]])
                    setPath("newb",["EndTime",GBUTTON_TIME,["Lines",["lineno"],"xEvents",i,"endTime",listToTime],["endTime:"],["Lines",["lineno"],"xEvents",i,"endTime"]])
                    setPath("newb",["Start",GBUTTON_FLOAT,["Lines",["lineno"],"xEvents",i,"start",str],["start:"],["Lines",["lineno"],"xEvents",i,"start"]])
                    setPath("newb",["End",GBUTTON_FLOAT,["Lines",["lineno"],"xEvents",i,"end",str],["end:"],["Lines",["lineno"],"xEvents",i,"end"]])
                    setPath("newb",["Easing",GBUTTON_CHOOSE,["Lines",["lineno"],"xEvents",i,"easing"],EASINGS,["Lines",["lineno"],"xEvents",i,"easing"]])
                    setPath("newb",["delete",GBUTTON_BUTTON,"delete",[7],["Lines",["lineno"],"xEvents",i,delany]])
                    """
l=["x","y","rotate","width","alpha","arc"]
for i in l:
    print(s.replace("x",i))