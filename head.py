import pygame
from pygame.locals import *
import pygame.freetype
from typing import *
from dummy import *
from ruamel.yaml import YAML
import os
from easing import code2FuncDict
from glob import glob
pygame.freetype.init()
pygame.mixer.init()
font=pygame.freetype.Font("SmileySans-Oblique.ttf",32)
GBUTTON_TEXT:int=0
GBUTTON_BUTTON:int=1
GBUTTON_CHOOSE:int=2
GBUTTON_BOOL:int=3
GBUTTON_INT:int=4
GBUTTON_FLOAT:int=5
GBUTTON_TIME:int=6
NOTE_WIDTH:int=100
SCRN_WIDTH=1600
SCRN_HEIGHT=900
EASINGS=[]
for i in range(29):
    EASINGS.append(code2FuncDict[i].__name__)
buttonList:List[Button]=[]
mainList:List[Button]=[]
nowList:List[Button]=[]
clk:pygame.time.Clock=pygame.time.Clock()
filepath="resources\\"+input("谱面路径:(相对于resources文件夹):")
print(os.getcwd())
if not filepath:
    print("未输入内容，正在退出...")
try:
    f=open(f"{filepath}\\info.txt",encoding="utf-8")
except OSError:
    pass
else:
    try:
        r=YAML(typ="safe").load(f)
    finally:
        f.close()
    os.rename(f"{filepath}\\{r['Song']}",f"{filepath}\\music.{r['Song'].split('.')[-1]}")
    os.rename(f"{filepath}\\{r['Picture']}",f"{filepath}\\illustration.{r['Picture'].split('.')[-1]}")
    os.rename(f"{filepath}\\{r['Chart']}",f"{filepath}\\chart.json")
    os.remove(f"{filepath}\\info.txt")
for i in glob(f"{filepath}\\illustration.*"):
    background:pygame.Surface=(
        pygame.transform.smoothscale(
            pygame.image.load(
                i
            ),
            (1200,900)
        )
    )
    break
COLORS:Dict[Type,Tuple[int|float]]={Tap:(0,255,255),Flick:(255,0,0),Drag:(255,255,0),Hold:(0,255,0)}
background.set_alpha(127)
rb=pygame.Surface((1200,900))
rb.fill((0,0,0))
rb.blit(background,(0,0))
background=rb
del rb
pygame.display.set_icon(pygame.image.load("OpenPhiGenerator.ico"))
pygame.display.set_caption("OpenPhiGenerator")
os.environ["SDL_IME_SHOW_UI"] = "1"
rscreen:pygame.Surface=pygame.display.set_mode((1600,900),RESIZABLE)
screen:pygame.Surface=pygame.Surface((1600,900))
game:pygame.Surface=pygame.Surface((1200,900)).convert_alpha()
lines:List[Line]=[]

BPMs:List[InstantEvent]=[]
MODE_PLAY:int=0
MODE_EDIT:int=1
MODE_EVENT:int=2
MODE_FOLLOW:int=3
root:Dict={"mode":MODE_PLAY,"BPMs":BPMs,"Lines":lines,"offset":0,
"meta":{
    "title":"",
    "composer":"",
    "charter":"",
    "illustrator":"",
    "level":""
    },
"lineno":0,"BPMno":0,"time":0,"hlines":4,"vlines":15,"timem":1,"menu":nowList}
