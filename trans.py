import math
NOTE_TYPES=["none","tap","hold","flick","drag"]
def RPE2OPG(d):
  o={}
  o["BPMs"]=[]
  for bpm in d["BPMList"]:
    o["BPMs"].append({"time":bpm["startTime"],"value":bpm["bpm"]})
  o["meta"]={
    "title":d["META"]["name"],
    "composer":d["META"]["composer"],
    "charter":d["META"]["charter"],
    "level":d["META"]["level"],
    "illustrator":"Unknown"
  }
  o["offset"]=-d["META"]["offset"]/1000
  o["Lines"]=[]
  for line in d["judgeLineList"]:
    l={"color":(line["extended"]["colorEvents"][0]["start"]
                if "extended" in line
                and "colorEvents" in line["extended"]
                and line["extended"]["colorEvents"]
                else (237,236,176)),
      "width":(line["extended"]["scaleXEvents"][0]["start"]*1200
                if "extended" in line
                and "scaleXEvents" in line["extended"]
                and line["extended"]["scaleXEvents"]
                else 3600),
      "notes":[],
      "xEvents":[],
      "yEvents":[],
      "rotateEvents":[],
      "alphaEvents":[],
      "speedEvents":[]
      }
    for evk,evs in line["eventLayers"][0].items():
      evk:str
      evs:list
      match evk:
        case "moveXEvents":
          evk="xEvents"
        case "moveYEvents":
          evk="yEvents"
      if evk=="speedEvents":
        for ev in evs:
          if ev["end"]!=ev["start"]:
            a=ev["startTime"][0]*ev["startTime"][2]+ev["startTime"][1]
            b=math.ceil(ev["endTime"][0]*ev["startTime"][2]+ev["endTime"][1]/ev["endTime"][2]*ev["startTime"][2])
            for t in range(a*8,b*8):
              e={"time":[int(t/8)//ev["startTime"][2],(t%(ev["startTime"][2]*8))/8,ev["startTime"][2]],"value":(ev["start"]+(ev["end"]-ev["start"])*(((t/8)-a)/(b-a)))*30}
              l[evk].append(e)
            e={"time":ev["endTime"],"value":ev["end"]*36}
            l[evk].append(e)
          else:
            e={"time":ev["startTime"],"value":ev["start"]*36}
            l[evk].append(e)
      else:
        for ev in evs:
          e={
            "startTime":ev["startTime"],
            "endTime":ev["endTime"],
            "start":ev["start"],
            "end":ev["end"],
            "easing":ev["easingType"]
          }
          if evk=="xEvents":
            e["start"]=e["start"]/135*120
            e["end"]=e["end"]/135*120
          l[evk].append(e)
    if "notes" in line:
      for note in line["notes"]:
        n={"time":note["startTime"],"x":note["positionX"],"isFake":note["isFake"],"above":note["above"]%2,"type":NOTE_TYPES[note["type"]]}
        if note["type"]==2:
          n["end"]=note["endTime"]
        l["notes"].append(n)
    o["Lines"].append(l)
  return o
