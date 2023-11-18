import pygame
from pygame.locals import *
from head import *
from solve import *
import pygame.gfxdraw as gfx
import sys
from easing import beziers
from math import *
import json
from typing import *
import timeit
from testaudio import *
import threading
import trans
# 初始化:
pygame.init()
pygame.scrap.init()
pygame.key.set_repeat(500, 50)

notename = {Tap: "tap", Hold: "hold", Flick: "flick", Drag: "drag"}
try:
    with open(filepath+"\\chart.json",encoding="utf-8") as f:
        d = json.load(f)
        if "META" in d and "RPEVersion" in d["META"]:
            d=trans.RPE2OPG(d)
        for BPM in d["BPMs"]:
            root["BPMs"].append(InstantEvent())
            root["BPMs"][-1].time = BPM["time"]
            root["BPMs"][-1].value = BPM["value"]

        root["offset"] = d["offset"]
        for f in d["meta"]:
            root["meta"][f] = d["meta"][f]
        for line in d["Lines"]:
            root["Lines"].append(Line())
            root["Lines"][-1].color = tuple(line["color"])
            root["Lines"][-1].notes = []
            for ev in line["notes"]:
                if ev["type"] == "tap":
                    root["Lines"][-1].notes.append(Tap())
                    root["Lines"][-1].notes[-1].time = ev["time"]
                    root["Lines"][-1].notes[-1].x = ev["x"]
                    root["Lines"][-1].notes[-1].isFake = ev["isFake"]
                    root["Lines"][-1].notes[-1].above = ev["above"]
                elif ev["type"] == "flick":
                    root["Lines"][-1].notes.append(Flick())
                    root["Lines"][-1].notes[-1].time = ev["time"]
                    root["Lines"][-1].notes[-1].x = ev["x"]
                    root["Lines"][-1].notes[-1].isFake = ev["isFake"]
                    root["Lines"][-1].notes[-1].above = ev["above"]
                elif ev["type"] == "drag":
                    root["Lines"][-1].notes.append(Drag())
                    root["Lines"][-1].notes[-1].time = ev["time"]
                    root["Lines"][-1].notes[-1].x = ev["x"]
                    root["Lines"][-1].notes[-1].isFake = ev["isFake"]
                    root["Lines"][-1].notes[-1].above = ev["above"]
                if ev["type"] == "hold":
                    root["Lines"][-1].notes.append(Hold())
                    root["Lines"][-1].notes[-1].time = ev["time"]
                    root["Lines"][-1].notes[-1].end = ev["end"]
                    root["Lines"][-1].notes[-1].x = ev["x"]
                    root["Lines"][-1].notes[-1].isFake = ev["isFake"]
                    root["Lines"][-1].notes[-1].above = ev["above"]
            root["Lines"][-1].notes.sort(key=lambda e: listToFloat((e.time)))
            for iv in line["xEvents"]:
                root["Lines"][-1].xEvents.append(Event())
                root["Lines"][-1].xEvents[-1].startTime = iv["startTime"]
                root["Lines"][-1].xEvents[-1].endTime = iv["endTime"]
                root["Lines"][-1].xEvents[-1].start = iv["start"]
                root["Lines"][-1].xEvents[-1].end = iv["end"]
                root["Lines"][-1].xEvents[-1].easing = iv["easing"]
            for iv in line["yEvents"]:
                root["Lines"][-1].yEvents.append(Event())
                root["Lines"][-1].yEvents[-1].startTime = iv["startTime"]
                root["Lines"][-1].yEvents[-1].endTime = iv["endTime"]
                root["Lines"][-1].yEvents[-1].start = iv["start"]
                root["Lines"][-1].yEvents[-1].end = iv["end"]
                root["Lines"][-1].yEvents[-1].easing = iv["easing"]
            for iv in line["rotateEvents"]:
                root["Lines"][-1].rotateEvents.append(Event())
                root["Lines"][-1].rotateEvents[-1].startTime = iv["startTime"]
                root["Lines"][-1].rotateEvents[-1].endTime = iv["endTime"]
                root["Lines"][-1].rotateEvents[-1].start = iv["start"]
                root["Lines"][-1].rotateEvents[-1].end = iv["end"]
                root["Lines"][-1].rotateEvents[-1].easing = iv["easing"]
            for iv in line["alphaEvents"]:
                root["Lines"][-1].alphaEvents.append(Event())
                root["Lines"][-1].alphaEvents[-1].startTime = iv["startTime"]
                root["Lines"][-1].alphaEvents[-1].endTime = iv["endTime"]
                root["Lines"][-1].alphaEvents[-1].start = iv["start"]
                root["Lines"][-1].alphaEvents[-1].end = iv["end"]
                root["Lines"][-1].alphaEvents[-1].easing = iv["easing"]
            for iv in line["speedEvents"]:
                root["Lines"][-1].speedEvents.append(InstantEvent())
                root["Lines"][-1].speedEvents[-1].time = iv["time"]
                root["Lines"][-1].speedEvents[-1].value = iv["value"]

except json.JSONDecodeError | OSError:
    setPath(["Lines", new], Line())
    root["Lines"][0].notes = []
    setPath(["BPMs", new], InstantEvent())
    BPMs[-1].value = 120


def obj2dict(x: object, excepts=list()):
    if hasattr(x, "__iter__"):
        return [obj2dict(n) for n in x if not n in excepts]
    elif type(x) is dict:
        return {n: obj2dict(x[n]) for n in x if not n in excepts}
    elif type(x) in (int, float, str):
        return x
    if hasattr(x, "__dict__") and x.__dict__:
        d = x.__dict__
        return {n: obj2dict(x.__getattribute__(n)) for n in d if not n in excepts and n[0] != "_"}
    else:
        return {n: obj2dict(x.__getattribute__(n)) for n in x.__slots__ if not n in excepts and n[0] != "_"}


isplay = 0


def save():
    with open(filepath+"\\chart.json") as f:
        with open(filepath+"\\chart copy.json", "w") as t:
            t.write(f.read())
    d = {"BPMs": [], "Lines": [],
         "meta": {}, "offset": root["offset"]}
    for BPM in root["BPMs"]:
        d["BPMs"].append(obj2dict(BPM))

    for f in root["meta"]:
        d["meta"][f] = root["meta"][f]
    for Line in root["Lines"]:
        d["Lines"].append(
            obj2dict(Line, ["x", "y", "rotation", "alpha", "speed"]))
        d["Lines"][-1]["notes"] = []
        for note in Line.notes:
            d["Lines"][-1]["notes"].append({**obj2dict(note),
                                           "type": notename[type(note)]})
        d["Lines"][-1]["notes"].sort(key=lambda e: listToFloat((e["time"])))

    with open(filepath+"\\chart.json", "w") as f:
        json.dump(d, f)
    screen.fill((0, 255, 0))
    rscreen.blit(pygame.transform.scale(
        screen, pygame.display.get_window_size()), (0, 0))
    pygame.display.flip()
    ...


mainList = newMenu((["编辑模式", GBUTTON_CHOOSE, root["mode"], ["播放", "音符编辑", "事件编辑"], ["mode"]]),
                   (["横线数", GBUTTON_INT, ["hlines", str], ["横线数"], ["hlines"]]),
                   (["竖线数", GBUTTON_INT, [
                    "vlines", str], ["竖线数"], ["vlines"]]),
                   (["播放倍速", GBUTTON_FLOAT, [
                    "timem", str], ["倍数"], ["timem"]]),
                   (["时间", GBUTTON_FLOAT, ["time", str], ["时间"], ["time"]]),
                   (["BPM列表:", GBUTTON_BUTTON, "展开", [
                       ["<", GBUTTON_BUTTON, "<返回", [], "delm"],
                       ["第N个", GBUTTON_CHOOSE, ["BPMno"],
                           root["BPMs"], ["BPMno"]],
                       ["时间", GBUTTON_TIME, ["BPMs", ["BPMno"], "time", listToTime], [
                           "时间:"], ["BPMs", ["BPMno"], "time"]],
                       ["BPM", GBUTTON_INT, ["BPMs", ["BPMno"], "value", str],
                           ["BPM:"], ["BPMs", ["BPMno"], "value"]],
                       ["删除", GBUTTON_BUTTON, "点击删除", [
                           "BPMno"], ["BPMs", ["BPMno"], delete]],
                       ["新建", GBUTTON_BUTTON, "新建", [
                           InstantEvent()], ["BPMs", new]]
                   ], "newb"]
),
    (["判定线列表", GBUTTON_BUTTON, "展开", [
        ["<", GBUTTON_BUTTON, "<返回", [], "delm"],
        ["序号", GBUTTON_CHOOSE, ["lineno"], root["Lines"], ["lineno"]],
        ["删除", GBUTTON_BUTTON, "点击删除", [
            "lineno"], ["Lines", ["lineno"], delete]],
        ["新建", GBUTTON_BUTTON, "新建", [Line()], ["Lines", new]]
    ], "newb"]
),
    (["信息", GBUTTON_BUTTON, "展开", [
        ["<", GBUTTON_BUTTON, "<返回", [], "delm"],
        ["标题", GBUTTON_TEXT, ["meta", "title"], ["标题:"], ["meta", "title"]],
        ["曲师", GBUTTON_TEXT, ["meta", "composer"],
            ["曲师:"], ["meta", "composer"]],
        ["谱师", GBUTTON_TEXT, ["meta", "charter"],
            ["谱师:"], ["meta", "charter"]],
        ["画师", GBUTTON_TEXT, ["meta", "illustrator"],
            ["画师:"], ["meta", "illustrator"]],
        ["难度", GBUTTON_TEXT, ["meta", "level"], ["难度:"], ["meta", "level"]],

    ], "newb"]
),
    (["偏移", GBUTTON_FLOAT, ["offset", str], ["偏移（秒）:"], ["offset"]])
)
_setPath = setPath
count = 0


def setPath(*args):
    global count
    count += 1
    if not count % 4:
        save()
    _setPath(*args)


COLORS: Dict[Type, Tuple[int | float]] = {Tap: (0, 255, 255), Drag: (
    255, 255, 0), Flick: (255, 0, 0), Hold: (0, 255, 0)}
procs = []
# 局部变量


class mse:  # 静态类
    x: int = 0
    y: int = 0
    down: list[int] = pygame.mouse.get_pressed()
    press: list[int]
    scrool: int = 0

import traceback
bind: Button | None = None
kbd: list[str] = []
def consoleThread():
    lock=threading.RLock()
    while threading.main_thread().is_alive():
        s=input(">> ")
        if not s:
            continue
        if s.rstrip()[-1]==':':
            k=1
            while k:
                t=input("...")
                if t.rstrip()[-1]==':':
                    k+=1
                elif (not t.strip()) or t.strip()=="pass":
                    k-=1
                s+="\n"+t
        lock.acquire()
        try:
            c=compile(s,"<string>","exec" if "\n" in s else "single")
            r=eval(c,globals(),locals())
        except Exception as err:
            traceback.print_exc()
            r=None
        finally:
            lock.release()
        if r:
            print(repr(r))
pinin=""
consTh=threading.Thread(target=consoleThread)
consTh.daemon=True
consTh.start()
pygame.key.set_text_input_rect(Rect(0,0,0,0))
while consTh.is_alive():
    # 计时
    clk.tick(60)
    if isplay:
        root["time"] = int((gettime()/fps()+root["offset"])*100)/100
    time = InstantEventsLoad(root["BPMs"], root["time"], 2)
    # 对绑定的点击型按钮减弱
    if bind:
        if bind.type == GBUTTON_BUTTON:
            bind.bind -= 1
            if not bind.bind:
                bind = None
    # 游戏界面刷新
    line: Line
    if root["mode"] == 0:
        for line in root["Lines"]:
            
            line: Line
            line.update(time)
            if line.alpha>0:
                r=-radians(line.rotation)
                gfx.filled_polygon(game,(
                     (600+line.x-line.width/2*cos(r)+2*-sin(r),
                      450-line.y+line.width/2*sin(r)+2*-cos(r)),
                     (600+line.x-line.width/2*cos(r)+2*sin(r),
                      450-line.y+line.width/2*sin(r)+2*cos(r)),
                     (600+line.x+line.width/2*cos(r)+2*sin(r),
                      450-line.y-line.width/2*sin(r)+2*cos(r)),
                     (600+line.x+line.width/2*cos(r)+2*-sin(r),
                      450-line.y-line.width/2*sin(r)+2*-cos(r))
                      ),(*(line.color), int(line.alpha)%256))
        for line in root["Lines"]:
            line: Line
            
            if line.alpha>=0:
                for i, note in enumerate(line.notes):
                    x = note.x
                    r = radians(line.rotation)
                    if (not note.isFake) and time>listToFloat(note.time):
                        tx = line.x+cos(r)*x
                        ty = line.y-sin(r)*x
                        if type(note) is Hold:
                            if time<listToFloat(note.end):
                                a=(100*(time-listToFloat(note.time))**(1/2))%50*2
                                gfx.rectangle(game,(600+tx-a/2,450-ty-a/2,a,a),(237,236,176))
                            elif time-listToFloat(note.end)<1:
                                a=100*(time-listToFloat(note.end))**(1/2)
                                gfx.rectangle(game,(600+tx-a/2,450-ty-a/2,a,a),(237,236,176))
                        else:
                            if time-listToFloat(note.time)<1:
                                a=100*(time-listToFloat(note.time))**(1/2)
                                gfx.rectangle(game,(600+tx-a/2,450-ty-a/2,a,a),(237,236,176))
                    if type(note) is Hold and listToFloat(note.end) < time:
                        continue
                    if (not type(note) is Hold) and listToFloat(note.time) < time:
                        continue
                    r = radians(line.rotation)
                    x = note.x
                    if type(note) is Hold and listToFloat(note.time) < time:
                        y = 0
                    else:
                        y = (InstantEventsLoad(line.speedEvents, listToFloat(
                            note.time), 1)-line.speed)
                        if not note.above:
                            y=-y
                    if y > 3200:
                        break
                    if type(note) is Hold:
                        y2 = (InstantEventsLoad(line.speedEvents, listToFloat(
                            note.end), 1)-line.speed)
                        if not note.above:
                            y2=-y2
                    else:
                        y2=y
                    ux=line.x+sin(r)*(y2+5)+cos(r)*x
                    uy=line.y+cos(r)*(y2+5)-sin(r)*x
                    dx=line.x+sin(r)*(y-5)+cos(r)*x
                    dy=line.y+cos(r)*(y-5)-sin(r)*x
                    # a = (600+tx-cos(r)*NOTE_WIDTH/2, 450-(ty+sin(r)*NOTE_WIDTH/2))
                    # b = (600+tx+cos(r)*NOTE_WIDTH/2, 450-(ty-sin(r)*NOTE_WIDTH/2))
                    lu=(600+ux-cos(r)*NOTE_WIDTH/2, 450-(uy+sin(r)*NOTE_WIDTH/2))
                    ru=(600+ux+cos(r)*NOTE_WIDTH/2, 450-(uy-sin(r)*NOTE_WIDTH/2))
                    ld=(600+dx-cos(r)*NOTE_WIDTH/2, 450-(dy+sin(r)*NOTE_WIDTH/2))
                    rd=(600+dx+cos(r)*NOTE_WIDTH/2, 450-(dy-sin(r)*NOTE_WIDTH/2))
                    # if type(note) is Hold:
                    #     y2 = (InstantEventsLoad(line.speedEvents, listToFloat(
                    #         note.end), 1)-line.speed)
                    #     if not note.above:
                    #         y2=-y2
                    #     ex = line.x+sin(r)*y2+cos(r)*x
                    #     ey = line.y+cos(r)*y2-sin(r)*x
                    #     gfx.line(game, COLORS[type(note)],
                    #             (600+tx, 450-ty), (600+ex, 450-ey), 10)
                    # else:
                    gfx.filled_polygon(game,(lu,ld,rd,ru),(COLORS[type(note)]))
    
        
    elif root["mode"] == 1:
        if not root["hlines"]:
            root["hlines"] = 1
        if root["vlines"] in (0, 1, 2) or root["vlines"] < 0:
            root["vlines"] = 3
        for i in range(0, 120001, 120000//(root["vlines"]-1)):
            pygame.draw.rect(game, (255 if round(i/100) == 600 else 0, 255,
                     255 if round(i/100) == 600 else 0), (i//100-2, 0, 4, 900))
        i = 0
        while 1:
            if i/root["hlines"] >= 2:
                break

            pygame.draw.rect(game, (0 if abs(round(i)-i) > 1e-10 else 255, 255 if abs(round(i)-i) > 1e-10 else 0, 255 if abs(round(i)-i) > 1e-10 else 0, 100),
                     (0,
                      798-800*i/root["hlines"] +
                      time % root["hlines"] /
                      root["hlines"]*800,
                      1200, 4), border_radius=1)
            if abs(round(i)-i) < 1e-10:
                s = f"{int(i)+root['hlines']*int(time/root['hlines'])}"
                game.blit(font.render(s, (255, 255, 255))[
                          0], (0, 780-800*i/root["hlines"]+time % root["hlines"]/root["hlines"]*800))
            i += 1/root["hlines"]
        pygame.draw.rect(game, (255, 255, 255), (0, 798, 1200, 4), border_radius=1)
        line = root["Lines"][root["lineno"]]
        if "q" in kbd and mse.x > 400:
            t = floatToList(
                round(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])
            x = round((mse.x-400)/1200 *
                      (root["vlines"]-1))*1200/(root["vlines"]-1)-600
            line.notes.append(Tap())
            line.notes[-1].x = x
            line.notes[-1].time = t
            line.notes[-1].isFake = 0
            line.notes[-1].above = 1
            line.notes.sort(key=lambda e: listToFloat((e.time)))
        if "e" in kbd and mse.x > 400:
            t = floatToList(
                round(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])
            x = round((mse.x-400)/1200 *
                      (root["vlines"]-1))*1200/(root["vlines"]-1)-600
            line.notes.append(Flick())
            line.notes[-1].x = x
            line.notes[-1].time = t
            line.notes[-1].isFake = 0
            line.notes[-1].above = 1
            line.notes.sort(key=lambda e: listToFloat((e.time)))
        if "w" in kbd and mse.x > 400:
            t = floatToList(
                round(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])
            x = round((mse.x-400)/1200 *
                      (root["vlines"]-1))*1200/(root["vlines"]-1)-600
            line.notes.append(Drag())
            line.notes[-1].x = x
            line.notes[-1].time = t
            line.notes[-1].isFake = 0
            line.notes[-1].above = 1
            line.notes.sort(key=lambda e: listToFloat((e.time)))
        if "r" in kbd and mse.x > 400:
            t = floatToList(
                round(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])
            x = round((mse.x-400)/1200 *
                      (root["vlines"]-1))*1200/(root["vlines"]-1)-600
            line.notes.append(Hold())
            line.notes[-1]: Hold
            line.notes[-1].x = x
            line.notes[-1].time = t
            line.notes[-1].end = (t[0]+1, t[1], t[2])
            line.notes[-1].isFake = 0
            line.notes[-1].above = 1
            line.notes.sort(key=lambda e: listToFloat((e.time)))

        for i, note in zip(range(len(line.notes)), line.notes):

            if type(note) is Hold:
                y1 = (listToFloat(note.time)-time)*800/root["hlines"]
                y2 = (listToFloat(note.end)-time)*800/root["hlines"]
                if y1 > 800:
                    break
                if pygame.draw.rect(game, COLORS[Hold], (550+note.x, 795-y2, 100, 10+y2-y1), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                    setPath("delm",[])
                    setPath("newb", ["<", GBUTTON_BUTTON, "<Hold", [], "delm"])
                    setPath("newb", ["开始时间", GBUTTON_TIME, ["Lines", ["lineno"], "notes", i, "time", listToTime], [
                            "开始时间:"], ["Lines", ["lineno"], "notes", i, "time"]])
                    setPath("newb", ["结束时间", GBUTTON_TIME, ["Lines", ["lineno"], "notes", i, "end", listToTime], [
                            "结束时间:"], ["Lines", ["lineno"], "notes", i, "end"]])
                    setPath("newb", ["X坐标", GBUTTON_FLOAT, ["Lines", ["lineno"], "notes", i, "x", str], [
                            "X:"], ["Lines", ["lineno"], "notes", i, "x"]])
                    setPath("newb", ["假音符？", GBUTTON_BOOL, ["Lines", ["lineno"], "notes", i, "isFake"], [
                            "假音符？"], ["Lines", ["lineno"], "notes", i, "isFake"]])
                    setPath("newb", ["判定线上方？", GBUTTON_BOOL, ["Lines", ["lineno"], "notes", i, "above"], [
                            "判定线上方？"], ["Lines", ["lineno"], "notes", i, "above"]])
                    setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [
                            7], ["Lines", ["lineno"], "notes", i, delany]])

                continue
            y = (listToFloat(note.time)-time)*800/root["hlines"]
            if y > 800:
                break
            if pygame.draw.rect(game, COLORS[type(note)], (note.x+550, 795-y, 100, 10), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", [
                        "<", GBUTTON_BUTTON, f"<{'Tap'if type(note) is Tap else ('Flick' if type(note) is Flick else 'Drag')}", [], "delm"])
                setPath("newb", ["时间", GBUTTON_TIME, ["Lines", ["lineno"], "notes", i, "time", listToTime], [
                        "时间:"], ["Lines", ["lineno"], "notes", i, "time"]])
                setPath("newb", ["X坐标", GBUTTON_FLOAT, ["Lines", ["lineno"], "notes", i, "x", str], [
                        "X:"], ["Lines", ["lineno"], "notes", i, "x"]])
                setPath("newb", ["假音符？", GBUTTON_BOOL, ["Lines", ["lineno"], "notes", i, "isFake"], [
                        "假音符？"], ["Lines", ["lineno"], "notes", i, "isFake"]])
                setPath("newb", ["判定线上方？", GBUTTON_BOOL, ["Lines", ["lineno"], "notes", i, "above"], [
                        "判定线上方？"], ["Lines", ["lineno"], "notes", i, "above"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [
                        6], ["Lines", ["lineno"], "notes", i, delany]])
    elif root["mode"] == 2:
        if not root["hlines"]:
            root["hlines"] = 1
        line = root["Lines"][root["lineno"]]
        if "q" in kbd and mse.x > 400:
            match (mse.x-275)//150:
                case 1:
                    t = floatToList(
                        int(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])

                    line.xEvents.append(Event())
                    line.xEvents[-1].startTime = t
                    line.xEvents[-1].endTime = [t[0]+1, t[1], t[2]]
                    line.xEvents[-1].start = 0
                    line.xEvents[-1].end = 0
                    line.xEvents[-1].easing = 0
                    line.xEvents.sort(key=lambda x:listToFloat(x.startTime))
                case 2:
                    t = floatToList(
                        int(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])

                    line.yEvents.append(Event())
                    line.yEvents[-1].startTime = t
                    line.yEvents[-1].endTime = [t[0]+1, t[1], t[2]]
                    line.yEvents[-1].start = 0
                    line.yEvents[-1].end = 0
                    line.yEvents[-1].easing = 0
                    line.yEvents.sort(key=lambda x:listToFloat(x.startTime))
                case 3:
                    t = floatToList(
                        int(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])

                    line.rotateEvents.append(Event())
                    line.rotateEvents[-1].startTime = t
                    line.rotateEvents[-1].endTime = [t[0]+1, t[1], t[2]]
                    line.rotateEvents[-1].start = 0
                    line.rotateEvents[-1].end = 0
                    line.rotateEvents[-1].easing = 0
                    line.rotateEvents.sort(key=lambda x:listToFloat(x.startTime))
                case 4:
                    t = floatToList(
                        int(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])

                    line.alphaEvents.append(Event())
                    line.alphaEvents[-1].startTime = t
                    line.alphaEvents[-1].endTime = [t[0]+1, t[1], t[2]]
                    line.alphaEvents[-1].start = 0
                    line.alphaEvents[-1].end = 0
                    line.alphaEvents[-1].easing = 0
                    line.alphaEvents.sort(key=lambda x:listToFloat(x.startTime))
                case 5:
                    t = floatToList(
                        int(((800-mse.y)*root["hlines"]/800+time)*root["hlines"])/root["hlines"])
                    line.speedEvents.append(InstantEvent())
                    line.speedEvents[-1].time = t
                    line.speedEvents[-1].value = 0
                    line.speedEvents.sort(key=lambda x:listToFloat(x.time))
        for i in range(100, 701, 150):
            pygame.draw.rect(game, (255, 255, 255), (i-2, 0, 4, 900))
        i = 0
        while 1:
            if i/root["hlines"] >= 2:
                break

            pygame.draw.rect(game, (0 if abs(round(i)-i) > 1e-10 else 255, 255 if abs(round(i)-i) > 1e-10 else 0, 255 if abs(round(i)-i) > 1e-10 else 0, 100),
                     (0,
                      798-800*i/root["hlines"] +
                      time % root["hlines"] /
                      root["hlines"]*800,
                      1200, 4), border_radius=1)
            if abs(round(i)-i) < 1e-10:
                s = f"{int(i)+root['hlines']*int(time/root['hlines'])}"
                game.blit(font.render(s, (255, 255, 255))[
                          0], (0, 780-800*i/root["hlines"]+time % root["hlines"]/root["hlines"]*800))
            i += 1/root["hlines"]
        pygame.draw.rect(game, (255, 255, 255), (0, 798, 1200, 4), border_radius=1)
        for i, e in enumerate(line.xEvents):

            e: Event
            y1 = (listToFloat(e.startTime)-time)*800/root["hlines"]
            if y1 > 800:
                break
            y2 = (listToFloat(e.endTime)-time)*800/root["hlines"]
            if y2 < -100:
                continue
            if pygame.draw.rect(game, (255, 0, 255), (50, 795-y2, 100, 10+y2-y1), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", ["<", GBUTTON_BUTTON, "x事件", [], "delm"])
                setPath("newb", ["开始时间", GBUTTON_TIME, ["Lines", ["lineno"], "xEvents", i, "startTime", listToTime], [
                        "开始时间:"], ["Lines", ["lineno"], "xEvents", i, "startTime"]])
                setPath("newb", ["结束时间", GBUTTON_TIME, ["Lines", ["lineno"], "xEvents", i, "endTime", listToTime], [
                        "结束时间:"], ["Lines", ["lineno"], "xEvents", i, "endTime"]])
                setPath("newb", ["开始值", GBUTTON_FLOAT, ["Lines", ["lineno"], "xEvents", i, "start", str], [
                        "开始值:"], ["Lines", ["lineno"], "xEvents", i, "start"]])
                setPath("newb", ["结束值", GBUTTON_FLOAT, ["Lines", ["lineno"], "xEvents", i, "end", str], [
                        "结束值:"], ["Lines", ["lineno"], "xEvents", i, "end"]])
                setPath("newb", ["缓动", GBUTTON_CHOOSE, ["Lines", [
                        "lineno"], "xEvents", i, "easing"], EASINGS, ["Lines", ["lineno"], "xEvents", i, "easing"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [
                        7], ["Lines", ["lineno"], "xEvents", i, delany]])
            if e.end!=e.start:
                font.render_to(game,(100,810-y2),str(int(e.end*100)/100),(255,255,0))
            font.render_to(game,(50,810-y1),str(int(e.start*100)/100),(255,255,0))
        for i, e in enumerate(line.yEvents):

            e: Event
            y1 = (listToFloat(e.startTime)-time)*800/root["hlines"]
            if y1 > 800:
                break
            y2 = (listToFloat(e.endTime)-time)*800/root["hlines"]
            if y2 < -100:
                continue
            if pygame.draw.rect(game, (255, 0, 255), (200, 795-y2, 100, 10+y2-y1), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", ["<", GBUTTON_BUTTON, "y事件", [], "delm"])
                setPath("newb", ["开始时间", GBUTTON_TIME, ["Lines", ["lineno"], "yEvents", i, "startTime", listToTime], [
                        "开始时间:"], ["Lines", ["lineno"], "yEvents", i, "startTime"]])
                setPath("newb", ["结束时间", GBUTTON_TIME, ["Lines", ["lineno"], "yEvents", i, "endTime", listToTime], [
                        "结束时间:"], ["Lines", ["lineno"], "yEvents", i, "endTime"]])
                setPath("newb", ["开始值", GBUTTON_FLOAT, ["Lines", ["lineno"], "yEvents", i, "start", str], [
                        "开始值:"], ["Lines", ["lineno"], "yEvents", i, "start"]])
                setPath("newb", ["结束值", GBUTTON_FLOAT, ["Lines", ["lineno"], "yEvents", i, "end", str], [
                        "结束值:"], ["Lines", ["lineno"], "yEvents", i, "end"]])
                setPath("newb", ["缓动", GBUTTON_CHOOSE, ["Lines", [
                        "lineno"], "yEvents", i, "easing"], EASINGS, ["Lines", ["lineno"], "yEvents", i, "easing"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [
                        7], ["Lines", ["lineno"], "yEvents", i, delany]])
            if e.end!=e.start:
                font.render_to(game,(250,810-y2),str(int(e.end*100)/100),(255,255,0))
            font.render_to(game,(200,810-y1),str(int(e.start*100)/100),(255,255,0))

        for i, e in enumerate(line.rotateEvents):

            e: Event
            y1 = (listToFloat(e.startTime)-time)*800/root["hlines"]
            if y1 > 800:
                break
            y2 = (listToFloat(e.endTime)-time)*800/root["hlines"]
            if y2 < -100:
                continue
            if pygame.draw.rect(game, (255, 0, 255), (350, 795-y2, 100, 10+y2-y1), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", ["<", GBUTTON_BUTTON,
                        "旋转事件", [], "delm"])
                setPath("newb", ["开始时间", GBUTTON_TIME, ["Lines", ["lineno"], "rotateEvents", i, "startTime", listToTime], [
                        "开始时间:"], ["Lines", ["lineno"], "rotateEvents", i, "startTime"]])
                setPath("newb", ["结束时间", GBUTTON_TIME, ["Lines", ["lineno"], "rotateEvents", i, "endTime", listToTime], [
                        "结束时间:"], ["Lines", ["lineno"], "rotateEvents", i, "endTime"]])
                setPath("newb", ["开始值", GBUTTON_FLOAT, ["Lines", ["lineno"], "rotateEvents", i, "start", str], [
                        "开始值:"], ["Lines", ["lineno"], "rotateEvents", i, "start"]])
                setPath("newb", ["结束值", GBUTTON_FLOAT, ["Lines", ["lineno"], "rotateEvents", i, "end", str], [
                        "结束值:"], ["Lines", ["lineno"], "rotateEvents", i, "end"]])
                setPath("newb", ["缓动", GBUTTON_CHOOSE, ["Lines", ["lineno"], "rotateEvents", i, "easing"], EASINGS, [
                        "Lines", ["lineno"], "rotateEvents", i, "easing"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [7], [
                        "Lines", ["lineno"], "rotateEvents", i, delany]])
            if e.end!=e.start:
                font.render_to(game,(400,810-y2),str(int(e.end*100)/100),(255,255,0))
            font.render_to(game,(350,810-y1),str(int(e.start*100)/100),(255,255,0))

        for i, e in enumerate(line.alphaEvents):

            e: Event
            y1 = (listToFloat(e.startTime)-time)*800/root["hlines"]
            if y1 > 800:
                break
            y2 = (listToFloat(e.endTime)-time)*800/root["hlines"]
            if y2 < -100:
                continue
            if pygame.draw.rect(game, (255, 0, 255), (500, 795-y2, 100, 10+y2-y1), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", ["<", GBUTTON_BUTTON,
                        "不透明度事件", [], "delm"])
                setPath("newb", ["开始时间", GBUTTON_TIME, ["Lines", ["lineno"], "alphaEvents", i, "startTime", listToTime], [
                        "开始时间:"], ["Lines", ["lineno"], "alphaEvents", i, "startTime"]])
                setPath("newb", ["结束时间", GBUTTON_TIME, ["Lines", ["lineno"], "alphaEvents", i, "endTime", listToTime], [
                        "结束时间:"], ["Lines", ["lineno"], "alphaEvents", i, "endTime"]])
                setPath("newb", ["开始值", GBUTTON_FLOAT, ["Lines", ["lineno"], "alphaEvents", i, "start", str], [
                        "开始值:"], ["Lines", ["lineno"], "alphaEvents", i, "start"]])
                setPath("newb", ["结束值", GBUTTON_FLOAT, ["Lines", ["lineno"], "alphaEvents", i, "end", str], [
                        "结束值:"], ["Lines", ["lineno"], "alphaEvents", i, "end"]])
                setPath("newb", ["缓动", GBUTTON_CHOOSE, ["Lines", ["lineno"], "alphaEvents", i, "easing"], EASINGS, [
                        "Lines", ["lineno"], "alphaEvents", i, "easing"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [7], [
                        "Lines", ["lineno"], "alphaEvents", i, delany]])
            if e.end!=e.start:
                font.render_to(game,(550,810-y2),str(int(e.end*100)/100),(255,255,0))
            font.render_to(game,(500,810-y1),str(int(e.start*100)/100),(255,255,0))

        for i, e in enumerate(line.speedEvents):
            e:InstantEvent
            y = (listToFloat(e.time)-time)*800/root["hlines"]
            if y > 800:
                break
            if y < -100:
                continue
            if pygame.draw.rect(game, (255, 0, 255), (650, 795-y, 100, 10), border_radius=1).collidepoint(mse.x-400, mse.y) and mse.press[0]:
                setPath("delm",[])
                setPath("newb", ["<", GBUTTON_BUTTON, "速度事件", [], "delm"])
                setPath("newb", ["时间", GBUTTON_TIME, ["Lines", ["lineno"], "speedEvents", i, "time", listToTime], [
                        "时间:"], ["Lines", ["lineno"], "speedEvents", i, "time"]])
                setPath("newb", ["值", GBUTTON_FLOAT, ["Lines", ["lineno"], "speedEvents", i, "value", str], [
                        "值:"], ["Lines", ["lineno"], "speedEvents", i, "value"]])
                setPath("newb", ["删除", GBUTTON_BUTTON, "删除", [4], [
                        "Lines", ["lineno"], "speedEvents", i, delany]])
                
            font.render_to(game,(650,810-y),str(int(e.value*100)/100),(255,255,0))
    # 绘制
    pygame.draw.rect(screen, (64, 64, 64), (0, 0, 400, 900))
    screen.blit(background, (400, 0))
    pygame.draw.rect(game, (255, 255, 255, 180), (0, 0, root["time"]*1200/alen(), 5))
    screen.blit(game, (400, 0))
    game.fill((0, 0, 0, 0))
    if nowList:
        buttonList = nowList
    else:
        buttonList = mainList
    for button in buttonList:
        button.draw(screen)
    # 屏幕刷新
    font.render_to(screen, (0, SCRN_HEIGHT-24), str(int(clk.get_fps()*100)/100), (255,255,255))
    font.render_to(screen, (mse.x, mse.y),
                   f"  {str(mse.x-1000)+','+str(450-mse.y) if mse.x>=400 else ''}", (255, 255, 255))
    font.render_to(screen,(0,0),pinin,(255,255,255))
    rscreen.blit(pygame.transform.scale(
        screen, pygame.display.get_window_size()), (0, 0))
    pygame.display.update()
    # 获取状态

    class mse:
        x: int
        y: int
        x, y = pygame.mouse.get_pos()
        down: list[int] = pygame.mouse.get_pressed()
        press: list[int] = list(map(lambda x: x[0] and (
            not x[1]), zip(pygame.mouse.get_pressed(), mse.down)))
        scrool: int = 0
    mse.x = int(mse.x/pygame.display.get_window_size()[0]*1600)
    mse.y = int(mse.y/pygame.display.get_window_size()[1]*900)
    # font.render_to(screen,(0,0),str(mse.press),(255,255,255))
    kbd: list[str] = []
    kmod: Dict[str, bool] = {"shift": False,
                             "control": False, "capslock": False}
    inp=""
    n = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            print(timeit.timeit(save, number=1))
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_F1:
                save()
            elif event.key == K_F5:
                isplay = 1-isplay
                if isplay:
                    n = 1
            kbd.append(pygame.key.name(event.key))
            kmod["shift"] = event.mod & pygame.KMOD_SHIFT
            kmod["control"] = event.mod & pygame.KMOD_CTRL
            kmod["capslock"] = event.mod & pygame.KMOD_CAPS
        elif event.type == MOUSEWHEEL:
            mse.scrool = event.y
            root["time"] += event.y/8
            if root["time"] < 0:
                root["time"] = 0
            isplay = 0
        elif event.type==TEXTINPUT:
            inp=event.text
        elif event.type==TEXTEDITING:
            pinin=event.text
    if kmod["control"] and "s" in kbd:
        save()
    if not bind:
        if "space" in kbd:
            isplay = 1-isplay
            if isplay:
                n = 1
    if n:
        procs.append(threading.Thread(
            target=play, args=(root["time"], root["timem"])))
        procs[-1].daemon = True
        procs[-1].start()
    if not isplay:
        stop()

    if mse.press[0]:
        n: bool = False
        for button in buttonList:
            if abs(mse.x-button.x) <= button.width/2 and abs(mse.y-button.y) <= button.height/2:
                n = button
                break
        if n:
            pygame.key.start_text_input()
            if bind:
                bind.bind = 0

            bind = n
            bind.bind = 16
        else:
            if bind:
                bind.bind = 0
                pygame.key.stop_text_input()
            bind = None
    if mse.down[0]:
        if mse.x > 400 and mse.y <= 5:
            root["time"] = (mse.x-400)/1200*alen()
    if not mainList[4].bind:
        mainList[4].input = str(root["time"])
    if bind:
        bind.update(mse, kbd, kmod,inp)
    if mse.press[0]:
        for i in buttonList:
            i.input = getPath(root, i.fro) if i.fro else i.input
pygame.quit()
