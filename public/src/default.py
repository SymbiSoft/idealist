import sys
sys.stderr = open('c:\\idealist\\error.log','w')
sys.stdout = open('c:\\idealist\\output.log','w')

import sysinfo
initram = sysinfo.free_ram()

import appuifw2, TopWindow, appswitch, keycapture, audio, socket
import e32, key_codes, graphics, time, calendar, e32db, contacts, globalui, messaging, math, sysinfo, xprofile, logs, inbox, urllib, envy

from akntextutils import wrap_text_to_array

import cerealizer as pickle

try:
    envy.set_app_system(1)
except:
    appuifw2.note(u"Can't set a system app status!");

try:
    kalendarz = calendar.open()
except:
    appuifw2.note(u"calendar opening error!")
#0 
#1 silent
#2 alarm
#3 alarm, silent
        
screenObj=None
annivs=[]
annivs1=[]
annivs2=[]
#Importing all images needed for the application
logo = graphics.Image.open('C:\\idealist\\logo.png')
present = graphics.Image.open('C:\\idealist\\present.png')
bell = graphics.Image.open('C:\\idealist\\bell.png')
message = graphics.Image.open('C:\\idealist\\message.png')
phone = graphics.Image.open('C:\\idealist\\phone.png')
sms = graphics.Image.open('C:\\idealist\\sms.png')
silence = graphics.Image.open('C:\\idealist\\silence.png')
sound = graphics.Image.open('C:\\idealist\\sound.png')

WALUTY=["PLN","USD"]
mToggle=False
goods = [u"Meal", u"Food", u"Cloth", u"Fees", u"House", u"Car", u"Meds", u"Hardware",u"Party"]
countMerged=[]

class DrawStandby:
    
    def __init__(self):
        self.ifshown=0
        self.window = TopWindow.TopWindow()
        #Set its size
        self.window.size = (240, 160)
        #Set the position of it upper left corner
        self.window.position = (10, 40)
        self.img1 = graphics.Image.new((self.window.size[0]*2, 20))
        self.img1.clear(0xffe96e)
        self.img1.text((0,15), u"Today", 0x000000, font='title')
        self.window.add_image(self.img1, (0, 0))
        
        self.img2 = graphics.Image.new((self.window.size[0]*2, 20))
        self.img2.clear(0xffe96e)
        self.img2.text((0,15), u"Tomorrow", 0x000000, font='title')
        self.window.add_image(self.img2, (0, 100))
        
        
        #images used later on refresh
        self.img = graphics.Image.new((self.window.size[0]*2, 80))
        self.window.add_image(self.img, (0, 20))        
        self.img3 = graphics.Image.new((self.window.size[0]*2, 80))
        self.window.add_image(self.img3, (0, 120))
        #Account
        self.img4 = graphics.Image.new((self.window.size[0]*2, 26))
        self.window.add_image(self.img4, (0, 200))
            
    def hide(self):
        self.window.hide()
        self.ifshown=0
    def show(self):
        (size, position) = appuifw2.app.layout(appuifw2.EMainPane)
        self.window.size = (size[0],size[1]-15)
        self.window.position= (position[0],position[1]+15)
        self.refresh()
        self.window.show()
        self.ifshown=1

    def refresh(self):
        global wlist, wlist2, silence, fuckable, baby, money, annivs1, annivs2, w
        #global girls

        self.img1.clear(0xffe96e)
        self.img1.text((0,15), u"Today", 0x000000, font='title')
        if annivs1!=None and len(annivs1)>0:
            self.img1.rectangle((50,4,w,20), fill=0x000000)
            try:
                self.img1.blit(present, target=(50,5))
                napis = ""
                for i in annivs1:
                    napis+=i[0]+", "
                self.img1.text((70,18), unicode(napis[0:-2]), 0xeeeeee, font='annotation')
            except:
                pass
        
        self.img2.clear(0xffe96e)
        self.img2.text((0,15), u"Tomorrow", 0x000000, font='title')
        if annivs2!=None and len(annivs2)>0:
            self.img2.rectangle((80,4,w,20), fill=0x000000)
            try:
                self.img2.blit(present, target=(80,5))
                napis=""
                for i in annivs2:
                    napis+=i[0]+", "
                self.img2.text((100,18), unicode(napis[0:-2]), 0xeeeeee, font='annotation')
            except:
                pass
            
        #Write text on it
        #file = open('C:\\idealist\\wlist.txt','w')
        #file.write(str(wlist))
        #file.close()
        
        #girlsStatus=girls.showStatus()
        #if (girlsStatus!=None and girlsStatus!=[]):
        #[name, period day, avarage period length, min period length, max period length, ferility, if data is fresh]
        #    j=0
        #    for i in girlsStatus:
        #        fresh=""
        #       if i[-2]==-1:
        #            color=0x00dd00
                    #self.img1.blit(fuckable, target=(70 + 40*(j),0))
        #        elif i[-2]==0:
                    #self.img1.blit(period, target=(70 + 40*(j),0))
        #            color=0xdd0000
        #        elif i[-2]==1:
                    #self.img1.blit(baby, target=(70 + 40*(j),0))
        #            color=0x0000dd
        #        if not i[-1]:
        #            fresh="!"
                    #self.img1.text((90 + 40*(j),15), u"!", 0xf0000f, font='title')
        #        self.img1.text((55 + 40*(j),15), unicode(i[0][:2] + fresh), color, font='title')
        #        j+=1
        
        self.img.clear(0x000000)
        if wlist!=[]:
            if wlist[0][0]>=time.time():
                self.img.text((10,20), unicode(wlist[0][2]), 0xffffff, font='normal')
                self.img.text((25,35), unicode("begins in " +str(int((wlist[0][0]-time.time())/60)) +" minutes"), 0xdddddd, font='annotation')

            elif wlist[0][1]>=time.time():
                self.img.text((10,20), unicode(wlist[0][2]), 0xffffff,font='normal')
                self.img.text((25,35), unicode( "working on now, ends in: " +  str(int((wlist[0][1]-time.time())/60))+ " minutes") , 0xdddddd, font='annotation')
            elif int(wlist[0][4])%2!=1:
                del wlist[0]
            try:
                if wlist[0][4]%2==1:
                    self.img.blit(silence, target=(2,22))
            except:
                pass
            if len(wlist)>1:
                self.img.text((10,50), unicode(wlist[1][2]), 0xffffff, font='annotation')
                self.img.text((25,65), unicode("begins in " +str(int((wlist[1][0]-time.time())/60)) + " minutes"), 0xdddddd, font='annotation')
                try:
                    if wlist[1][4]%2==1:
                        self.img.blit(silence, target=(2,52))
                except:
                    pass
        else:
            pass
            #self.img.text((25,25), u"", 0xffffff, font='normal')
        #Add it to the window specifying coordinates for its upper left corner
        
        
        self.img3.clear(0x000000)
        if len(wlist2)>0:
            ile=0
            for i in wlist2:
                ile+=1   
                start=time.gmtime(i[0])
                end=time.gmtime(i[1])
                self.img3.text((10,ile*15), unicode(str(start[3]-start[-1])+":"+(str(start[4]),"0"+str(start[4]))[len(str(start[4]))==1] + "-"+ str(end[3]-start[-1])+":" + (str(end[4]),"0"+str(end[4]))[len(str(end[4]))==1]) +" "+ unicode(i[2]), 0xeeeeee, font='annotation')    
                if ile==5:
                    break
        else:
            pass
            #self.img3.text((25,25), u"***", 0xffffff, font='normal')
        
        self.img4.clear(0x0aaaaa)
        #self.img4.rectangle((62,6,w,26), fill=0x000000)
        self.img4.text((0,20), u"Account: ", 0xffffff, font='normal')
        if len(money[0])>0 and len(money[1])>0:
            try:
                self.img4.text((65,11), unicode(str(money[0][0]) + " " + WALUTY[0]), 0xffffff, font='annotation')
            except:
                pass
            try:
                self.img4.text((65,25), unicode(str(money[1][0]) + " " + WALUTY[1]), 0xffffff, font='annotation')
            except:
                pass
            #Make the window's background green
        #self.window.background_color = 0xffffff
        #Add a shadow effect
        #self.window.shadow = 4
        #Make the corners round
        #self.window.corner_type = 'corner5'
         
        #Display the window
        #self.window.show()
        
        #capturer=keycapture.KeyCapturer(self.cb_capture)
        #capturer.keys=(keycapture.EKey1,keycapture.EKey2)
        #capturer.start()
    
app_lock = e32.Ao_lock()
xprof=0

days=[u"Monday",u"Tuesday",u"Wednesday",u"Thursday",u"Friday",u"Saturday",u"Sunday"]
months=[u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December"]



messageinfo=u""
remindinfo=u""
annivsinfo=None

#Initializing time
tempek=list(time.localtime())
tempek[3]=tempek[4]=tempek[5]=0
tempek=tuple(tempek)
viewday=time.mktime(tempek)
currentday=float(viewday)
weekday=time.localtime().tm_wday
#All the variables used in app

remind=[]
#variables which specify if the Ideas menu should be visible
selected=0
start = 0
#The beginning of the day
dhstart=hstart=7
dhstop=hstop=23
newh=14
endh=13
m=0
snd=None
currentfont='dense'
missedcalls=0
unreadsms=0
atext=""
d=None
#0-select mode (multiple), 1-move mode (multiple), 2-adjust mode (single)
smsList=[]
projects=[]
recording=0
#Two most important variables
mode=0
inHand=0
voiceNote=None
commingSoon=u""
timer=e32.Ao_timer()
token=''
girlsDB=[]
#################################
#mode     #
#0        # normal
#1        # edit: move
#2        # edit: change order
#3        # edit: adjust

#################################
#inHand   #
#-2       # add new event
#-1       # add/edit message
# 0       # normal mode
# 1       # add/edit anniversary
# 2       # add/edit reminder
# 3       # add/edit voice message
ideacat=[[u'Work',(220,220,220)],[u'School',(200,200,70)],[u'Science',(200,200,70)],[u'Meal',(220,70,200)],[u'Physical Exercise',(100,70,100)],[u'Meeting',(70,100,100)],[u'Relax',(100,70,70)],[u'Shoping',(80,80,80)],[u'Cleanings',(90,90,90)]]
cati=len(ideacat)
path='C:\\idealist\\ideas.txt'
#Initialize the reading ideas from file
ideas=[]
anychange=0
#Define if alarms should be enabled
alarm = 1
#A variable for mode=2 event
eventCopy=0
eventsEmpty=[]
otherday=0
savelist=[]
hline=0
c1=0
dish=11
money=[[],[]]
#It's 1 if menu is opened
menu=0
wlist =[]
wlist2=[]

deltodo=[[],[]]
inboxx=inbox.Inbox()
def saveConfig():
    global ideacat, dhstart, dhstop, hstart, hstop, currentfont, alarm, token, deltodo, money, screenObj
    
    tosave=[ideacat,dhstart,dhstop,currentfont, alarm, token, deltodo, money, screenObj is not None]
    try:
        pickle.dump(tosave,open('C:\\idealist\\config.txt','w'))
    except:
        pass
        #idealistappuifw2.note(u"Can't save the config file")
    
def loadConfig():
    global ideacat, dhstart, dhstop, hstart, hstop, currentfont, alarm, token, deltodo, money, screenObj
    try:
        toload=pickle.load(open('C:\\idealist\\config.txt'))
        ideacat=toload[0]
        dhstart=hstart=toload[1]
        dhstop=hstop=toload[2]
        currentfont=toload[3]
        alarm = toload[4]
        token=toload[5]
        deltodo=toload[6]
        money=toload[7]
        if toload[8]:
            screenObj=DrawStandby()
            drawOnStandby()
        else:
            screenObj=None
    except:
        deltodo=[[],[]]
        #idealistappuifw2.note(u"[First run warnings]")
        #idealistappuifw2.note(u"Can't load the config file")
        pass
        
loadConfig()

try:
    smsList=pickle.load(open('C:\\idealist\\smses.txt'))
except:
    appuifw2.note(u"Can't load the planned sms db")
    try:
        pickle.dump([],open('C:\\idealist\\smses.txt','w'))
    except:
        pass

soundList=[]

try:
    soundList=pickle.load(open('C:\\idealist\\sounds.txt'))
except:
    appuifw2.note(u"Can't load the sound db")
    pickle.dump([],open('C:\\idealist\\sounds.txt','w'))


#Here we have scheme color table in the following order:

# 0 EVENT BUTTON 0
#1 EVENT BUTTON 1
# 2 HIGHLIGHT EVENT BUTTON
# 3 EVENT BUTTON FONT
# 4 HIGHLIGHT EVENT FONT
# 5 NEW BUTTON
# 6 NEW HIGHLIGHT BUTTON
# 7 NEW FONT
# 8 NEW FONT HIGHLIGHT
# 9 CURRENT BACKGROUND
# 10 CURRENT FONT
# 11 BACKGROUND
# 12 SPECIAL RED FOR RESIZING
# 13 DRAGGING GREEN
# 14 ORANGE
# 15 DARK BLUE

colors =[(0,200,220),(0,220,240), (0,0,0), (0,0,0),(255,255,255),(200,200,200),(0,0,0),(0,0,0),(255,255,255),(100,100,100),(220,220,220),(240,240,240),(150,0,0), (0,150,0), (150, 90, 0), (0,0,150)]

todo=None
def loadBase():
    global base
    try:
        cyk=pickle.load(open('C:\\idealist\\todo.txt'))
        base=[]
        for i in range(0,len(cyk)):
            base+=[[]]
            base[i]+=[cyk[i][0]]
            for j in range(1,len(cyk[i])):
                base[i]+=[[]]
                try:
                    base[i][j]=appuifw2.Item(cyk[i][j][0], id=cyk[i][j][2], priority=cyk[i][j][3], icon=appuifw2.Icon(u'C:\\idealist\\icons.mbm',int(cyk[i][j][3]),0))
                except:
                    base[i][j]=appuifw2.Item(cyk[i][j][0], id=None, priority=cyk[i][j][3], icon=appuifw2.Icon(u'C:\\idealist\\icons.mbm',int(cyk[i][j][3]),0))
                base[i][j].marked=cyk[i][j][1]
    except:
        appuifw2.note(u"Cannot load Todo file!")
        pickle.dump([[[]]],open('C:\\idealist\\todo.txt','w'))
        base=[[[]]]
        pass
    
loadBase()

def saveBase():
    global base
    tosave=[]
    for i in range(0,len(base)):
        tosave += [[]]
        tosave[i]+=[base[i][0]]
        for j in range(1,len(base[i])):
            try:
                tosave[i]+=[[base[i][j].title,base[i][j].marked,base[i][j].id,base[i][j].priority]]
            except:
                tosave[i]+=[[base[i][j].title,base[i][j].marked,False,base[i][j].priority]]
    try:
        pickle.dump(tosave,open('C:\\idealist\\todo.txt','w'))
    except:
        appuifw2.note(u"Cannot save the Todo file")
    


class ProgressBar(object):
    def __init__(self, start=0, end=100, color=(0,0,77), fill=(255,255,200), outline=(0,0,0)):
        global w,h
        screen_size = sysinfo.display_pixels()
        #sizes & positions
        self.height = 60
        self.width = w-20
        self.top = h - self.height - 15
        self.left = 15
        #ProgressBar size
        self.progress_margin = 5
        self.progress_w = self.width - (2 * self.progress_margin)
        self.progress_h = 18 #height of progressbar
        self.progress_l = self.progress_margin
        self.progress_t = self.height - self.progress_h - self.progress_margin
        #internal progressbar expects that external has 1px border
        self.internal_w_max = self.progress_w - 2
        self.internal_h = self.progress_h - 2
        self.internal_l = self.progress_l + 1
        self.internal_t = self.progress_t + 1
        self.internal_w = 0
        self.glow_h = int(self.internal_h / 2)
        #colors & values
        self.start = start
        self.end = end
        self.value = start
        self.color = color
        self.glow_color = self.color_combine(color, (255,255,255), 0.5)
        self.outline = outline
        self.fill = fill
        #text attributes
        self.caption = u""
        self.font = (u"dense", 12)
        self.text_top = self.progress_t - self.progress_margin - self.font[1]
        #create topwindow
        self.window = TopWindow.TopWindow()
        self.window.corner_type = 'square'
        self.window.position = (self.left, self.top)
        self.window.size = (self.width, self.height)
        self.canvas = graphics.Image.new(self.window.size)
        self.window.add_image(self.canvas,(0,0,self.width,self.height))
        #shows initial progressbar
        self.redraw()
        self.window.show()
    
    def close(self):
        #Closes the window and frees the image buffers memory
        try:
            del self.canvas
        except:
            pass
        try:
            self.window.hide()
        except:
            pass
        try:
            del self.window
        except:
            pass
    
    def set_text(self, text):
        self.caption = text
        self.redraw()
 
    def set_value(self, value):
        if value > self.end:
            value = self.end
        elif value < self.start:
            value = self.start
        self.value = value
        self.internal_w = int(((1.0 * self.value - self.start)/ (1.0 * self.end - self.start))* self.internal_w_max)
        self.redraw()
 
    def redraw(self):
        #You don't need call redraw on application. Just use set_value to redraw the progressbar
        #external window
        self.canvas.rectangle((0, 0, self.width, self.height), outline=self.outline, fill=self.fill)
        #progressbar external border
        self.canvas.rectangle((self.progress_l, self.progress_t, self.progress_l + self.progress_w, self.progress_t + self.progress_h), outline=self.outline, fill=self.fill)
        #progressbar core with glow
        self.canvas.rectangle((self.internal_l, self.internal_t, self.internal_l + self.internal_w, self.internal_t + self.internal_h), outline=None, fill=self.color)
        self.canvas.rectangle((self.internal_l, self.internal_t, self.internal_l + self.internal_w, self.internal_t + self.glow_h), outline=None, fill=self.glow_color)
        #window caption
        self.canvas.text((self.progress_margin, self.text_top),self.caption, fill = self.outline, font = self.font)
        #exchange images
        self.window.remove_image(self.window.images[0][0])
        self.window.add_image(self.canvas,(0,0,self.width,self.height))
        e32.ao_sleep(0.001)
    
    def color_combine(self, c1, c2, perc):
        c = map(lambda a,b: int(a*(1-perc)+0.5) + int(b*perc+0.5), c1, c2)
        return tuple(c)
    
class Todo:
    inside=0
    d=None
    def __init__(self,index=0,theid=0):
        #loadBase()
        #try:
        self.build(index)
        #except:
        #    idealistappuifw2.note(u"Can't load the todo gui")
        if theid!=0:
            self.newbox(theid)
    def left(self):
        if self.inside:
            copy=self.inside
            self.inside=0
            self.prepare()
            appuifw2.app.body.set_current(copy-1)
    def select(self):
        global base
        if base[self.inside]!=[]:
            if self.inside:
                try:
                    base[self.inside][self.nana.current()+1].marked=not base[self.inside][self.nana.current()+1].marked
                    temp=base[self.inside][1:]
                    temp.sort(self.cmpfunc)
                    base[self.inside]=[base[self.inside][0]] + temp
                except:
                    pass
            else:
                try:
                    self.inside=self.nana.current()+1
                    appuifw2.app.body.set_current(0)
                except:
                    pass
            self.prepare(self.inside)
    def newbox(self,id=0):
        if self.inside:
            number=None
            try:
                number=base[self.inside][self.nana.current()+1].priority
            except:
                pass
            a=appuifw2.query(u"Element name:", 'text', u"")
            if number==None:
                number=1
            if a!=u"" and a!=None:
                b=appuifw2.Item(a,id=None, priority=number, icon=appuifw2.Icon(u'C:\\idealist\\icons.mbm',number,0))
                b.marked=False
                base[self.inside].extend([b])
                
                temp=base[self.inside][1:]
                temp.sort(self.cmpfunc)
                base[self.inside]=[base[self.inside][0]] + temp
                
                self.prepare(self.inside)
        else:
            a=appuifw2.query(u"List name:", 'text', u"")
            if a!=u"" and a!=None:
                b=appuifw2.Item(a, id=None, priority=0, icon=appuifw2.Icon(u'C:\\idealist\\icons.mbm',0,0))
                b.marked=False
                base[0].extend([b])
                if id!=0:
                    base.extend([[[id]]])
                else:
                    base.extend([[[]]])
                self.inside=-1
                self.prepare(self.inside)

    def delbox(self):
        global deltodo
        if base[self.inside]!=[]:
            if self.inside:
                try:
                    deltodo[1].extend([[base[self.inside][self.nana.current()+1].id,base[0][self.inside].id]])
                    #idealistappuifw2.note(u"" + str([base[self.inside][self.nana.current()+1].id,base[0][self.inside].id]))
                    del base[self.inside][self.nana.current()+1]
                except:
                    pass
            else:
                try:
                    deltodo[0].extend([base[0][self.nana.current()+1].id])
                    del base[self.nana.current()+1]
                    del base[0][self.nana.current()+1]
                except:
                    pass
            self.prepare(self.inside)
    
    def edit(self):
        if base[self.inside]!=[]:
            if self.inside:
                try:
                    a=appuifw2.query(u"Edit","text",base[self.inside][self.nana.current()+1].title)
                    if a!=None and a!="":
                        z=appuifw2.Item(a, id=base[self.inside][self.nana.current()+1].id, priority=base[self.inside][self.nana.current()+1].priority, icon=base[self.inside][self.nana.current()+1].icon)
                        z.marked=base[self.inside][self.nana.current()+1].marked
                        base[self.inside][self.nana.current()+1]=z
                    else:
                        return 0
                except:
                    pass
            else:
                try:
                    a=appuifw2.query(u"Edit","text",base[0][self.nana.current()+1].title)
                    if a!=None and a!="":
                        z=appuifw2.Item(a, id=base[self.inside][self.nana.current()+1].id, priority=base[self.inside][self.nana.current()+1].priority, icon=base[self.inside][self.nana.current()+1].icon)
                        base[0][self.nana.current()+1] = z
                    else:
                        return 0
                except:
                    pass
            self.prepare(self.inside)
    def prepare(self, selec=0):
        global base
        #try:
        #    self.sprzataj()
        #except:
        #    appuifw2.note(u"Can't sort the list")
        try:
            appuifw2.app.body.clear()
            appuifw2.app.body.extend(base[selec][1:])
            if selec==0:
                mark=False
                appuifw2.app.navi_text=u'To-do lists'  + ": " + str(len(appuifw2.app.body))
                texxt=u"list"
            else:
                appuifw2.app.navi_text=base[0][selec].title  + ": " + str(len(appuifw2.app.body.marked())) + "/" + str(len(appuifw2.app.body))
                mark=True
                texxt=u"element"
    
            appuifw2.app.menu_key_text=u"Add " + texxt
        except:
            quit()
        #idealistappuifw2.note(unicode(idealistappuifw2.app.body.current()))
        #if idealistappuifw2.app.body.current()>len(idealistappuifw2.app.body)-1:
        #    try:
        
        #    except:

    def cmpfunc(self, x, y):
        #if ((type(x) is not idealistappuifw2.Item) or (type(y) is not idealistappuifw2.Item)):
        #    return 0
        if (int(x.marked)-int(y.marked))!=0:
            return int(x.marked)-int(y.marked)
            
        return x.priority-y.priority

    def sprzataj(self):
        global base
        temp=[]
        if len(base)!=0:
            for i in range(1,len(base)):
                temp=base[i][1:]
                temp.sort(self.cmpfunc)
                base[i]=[base[i][0]] + temp
            
    def p(self,prior):
        global base
        if base[self.inside]!=[]:
            base[self.inside][self.nana.current()+1]=appuifw2.Item(base[self.inside][self.nana.current()+1].title, marked=base[self.inside][self.nana.current()+1].marked,id=base[self.inside][self.nana.current()+1].id, priority=prior, icon=appuifw2.Icon(u'C:\\idealist\\icons.mbm',prior,0))
            if self.inside:
                temp=base[self.inside][1:]
                temp.sort(self.cmpfunc)
                base[self.inside]=[base[self.inside][0]] + temp
            self.prepare(self.inside)
    
    def send(self):
        message=u""
        if self.inside:
            message=unicode(base[self.inside][self.nana.current()+1].title)
        else:
            try:
                message+=unicode(str(base[0][self.nana.current()+1].title) + ":\r\n") 
            except:
                pass
            try:
                for i in base[self.nana.current()+1]:
                    try:
                        if i.marked:
                            message += u"+"
                        else:
                            message += u"-"
                    except:
                        message += u"-"
                    try:
                        message+=unicode(str(i.title) + "\r\n")
                    except:
                        pass
            except:
                appuifw2.note(u"Error on adding")
                    
        self.d=pickNumber()
        if self.d!=None:
            try:
                shortk=appuifw2.Text(text=unicode(message))
                appuifw2.app.screen='normal'
                appuifw2.app.exit_key_handler = self.cancelSend
                appuifw2.app.menu_key_text=u"Send"
                appuifw2.app.menu_key_handler=self.sendIt
                appuifw2.app.body=shortk
                #a=appuifw2.query(message, 'query')
            except:
                appuifw2.note(u"Error sending the list!")
                
    def cancelSend(self):
        copy=self.nana.current()+1
        self.build(self.inside)
        appuifw2.app.body.set_current(copy-1)
        appuifw2.app.exit_key_handler = quit
    
    def sendIt(self):
        
        if self.d.find("@")==-1:
            messaging.sms_send(self.d,appuifw2.app.body.get())
        else:
            messaging.mms_send(self.d,appuifw2.app.body.get(),attachment=None)
            #appuifw2.note(u"variable d not set to a number!")
        self.cancelSend()
        
    def put(self):
        global events, inHand, eventCopy, hstop, hstart, mode, eventsEmpty, selected, eventCopy
        
        if base[self.inside][self.nana.current()+1].title!=None:
            saveBase()
            predraw()
            buildCanvas()
            a=base[self.inside][self.nana.current()+1].title
            eventCopy= a
            eventsSpace(events)
            selected=0
            inHand=-2
            gradient()
            draw(events)
            drawRectangle(eventsEmpty)
                
    def build(self,selec=0):
        global base
        try:
            self.sprzataj()
        except Exception:
            appuifw2.note(u"Can't sort the list")
        
        self.nana=appuifw2.Listbox2(base[selec][1:], markable=True, icons=True)
        
            
        self.nana.set_empty_list_text=u"Empty list"
        appuifw2.app.body=self.nana
        appuifw2.app.screen='normal'
    #select the last selected item

        if selec==0:
            appuifw2.app.navi_text=u'To-do lists'  + ": " + str(len(appuifw2.app.body))
            texxt=u"list"
        else:
            appuifw2.app.navi_text=base[0][selec].title  + ": " + str(len(appuifw2.app.body.marked())) + "/" + str(len(appuifw2.app.body))
            texxt=u"element"
            
        self.nana.bind(key_codes.EKeyBackspace,self.delbox)
        self.nana.bind(key_codes.EKeySelect,self.select)
        self.nana.bind(key_codes.EKeyLeftArrow,self.left)
        self.nana.bind(key_codes.EKeyRightArrow,self.select)
        self.nana.bind(key_codes.EKeyYes,self.edit)
        self.nana.bind(key_codes.EKeyHash,self.send)
        self.nana.bind(key_codes.EKey5,self.put)
        self.nana.bind(key_codes.EKey1,lambda:self.p(1))
        self.nana.bind(key_codes.EKey2,lambda:self.p(2))
        self.nana.bind(key_codes.EKey3,lambda:self.p(3))
        self.nana.bind(key_codes.EKey4,lambda:self.p(4))
         
        appuifw2.app.menu_key_text=u"Add " + texxt
        appuifw2.app.menu_key_handler=self.newbox
        self.inside=selec
        appuifw2.app.menu=[]


class Connection:
    def __init__(self):
        self.setDefaultAP()
    def connect(self):
        pass       
    def setDefaultAP(self):
        apid = socket.select_access_point()
        if not apid:
            appuifw2.note(u"Could't find any access point.","error")
            return False
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)
        apo.start()
        x=Todoist(token)
        appuifw2.note(u"Starting upload")
        x.uploadBase()
        apo.stop()
        return True
    


class Todoist:
    def __init__(self, tokens):
        global token
        if tokens=="":
            appuifw2.note(u"Please enter a valid Todoist token.")
            token2=appuifw2.query(u"Set token",'text', unicode(str(tokens)))
            if token2!=None and token2!="":
                token=token2
                
                saveConfig()
        self.token=token
        appuifw2.note(u"Connecting using token: " + unicode(str(self.token)))
        self.baseurl = 'http://todoist.com/API/'

    def addItems(self, project_id, content,priority=4):
        
        try:
            xtra='addItem?content=%s&project_id=%s&priority=%s&token=%s' % (urllib.quote(content.encode("utf-8")), project_id, priority, self.token)
        except:
            appuifw2.note(u"error making new")
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
            #appuifw2.query(unicode(self.baseurl + xtra),'query')
            data=tapi.read().replace("\"","\"")
        except:
            appuifw2.note(u"error making new2")
        try:
            tapi.close()
            null=0
            data = eval(data)
        except:
            appuifw2.note(u"error 3 " + unicode(str(data)))
        return data['id']
        
        
    
    def getProjects(self):
        #retrun list of projects
        xtra = 'getProjects?token='
        proby=0

        while(proby<3):
            try:
                tapi = urllib.urlopen(self.baseurl+xtra+self.token)
                proby=3
                
            except:
                proby+=1
                appuifw2.note(unicode(proby) + " connection attempt")
                
        data=tapi.read().replace("\"","\"")
        tapi.close()
        null=0
        data = eval(data)
        if type(data) is str:
            appuifw2.note(unicode(data))
        return data
    
    def delProject(self,id):
        xtra = 'deleteProject?token=%s&project_id=%s' % (self.token, str(id))
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
        except:
            appuifw2.note(u"Connection error")
        try:
            data=tapi.read().replace("\"","\"")
            tapi.close()
        except:
            appuifw2.note(u"error 3 ")
    
    def delItem(self, id, project_id):
        xtra = 'deleteItems?token=%s&ids=[%s]&project_id=%s' % (self.token, str(id), str(project_id))
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
        except:
            appuifw2.note(u"Connection error")
        try:
            data=tapi.read().replace("\"","\"")
            tapi.close()
        except:
            appuifw2.note(u"error 3")
    
    
    
    def addProject(self, content, priority=0):
        xtra = 'addProject?token=%s&color=%s&name=%s' % (self.token, str(priority), urllib.quote(content.encode("utf-8")))
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
        except:
            appuifw2.note(u"Connection error")
        try:
            data=tapi.read().replace("\"","\"")
            null=0
            data=eval(data)
        except:
            appuifw2.note(u"error 3 " + unicode(str(data)))
        return data['id']
            
    def updateProject(self, content, priority, project_id):
        xtra = 'updateProject?token=%s&color=%s&name=%s&project_id=%s' % (self.token, str(priority), urllib.quote(content.encode("utf-8")), str(project_id))
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
        except:
            appuifw2.note(u"Connection error")
        try:
            data=tapi.read().replace("\"","\"")
            null=0
            data=eval(data)
        except:
            pass
        if (project_id == None or int(project_id)==0 or (unicode(str(data)[0], 'utf_8') == unicode("[", 'utf_8'))):
            try:
                tapi.close()
            except:
                pass
            project_id=self.addProject(content,priority)
        else:
            tapi.close()
        return project_id
        
    def updateItem(self, content, id,completed, priority, project_id):
        
        xtra = 'updateItem?id=%s&content=%s&priority=%s&token=%s' % (str(id), urllib.quote(content.encode("utf-8")), str(priority), self.token)
        try:
            tapi = urllib.urlopen(self.baseurl + xtra)
        except:
            appuifw2.note(u"Connection error")
        try:
            data=tapi.read().replace("\"","\"")
            data=eval(data)
        except:
            pass
            #appuifw2.note(u"strange bug")
        if (id == None or int(id)==0 or (unicode(str(data)[0], 'utf_8') == unicode("A", 'utf_8'))):
            try:
                tapi.close()
            except:
                pass
            id=self.addItems(project_id, content, priority)
            
            
        else:
            tapi.close()
        if completed:
            try:
                xtra = 'completeItems?ids=[%s]&token=%s' % (str(id), self.token)
                tapi = urllib.urlopen(self.baseurl + xtra)
                #data=tapi.read().replace("\"","\"")
                #data=eval(data)
                tapi.close()
            except:
                pass
        return id
        #data=tapi.read().replace("\"","'")
        
    
    def getUncompletedItems(self, project_id):

        xtra = 'getUncompletedItems?project_id=%s&token=%s' % (project_id, self.token)
        tapi = urllib.urlopen(self.baseurl+xtra)
        data=tapi.read().replace("\"","\"")
        tapi.close()
        null=0
        data=eval(data)
        return data
    

    def getCompletedItems(self, project_id):

        xtra = 'getCompletedItems?project_id=%s&token=%s' % (project_id, self.token)
        tapi = urllib.urlopen(self.baseurl+xtra)
        data=tapi.read().replace("\"","\"")
        tapi.close()
        null=0
        data=eval(data)
        return data

    def downloadBase(self, token=''):
        global base, todo
        pb = ProgressBar()
        pb.set_text(u"Getting project list")
        pb.set_value(0)
        try:
            projects=self.getProjects()
        except:
            pb.set_text(u"Error getting project list")
        pb.set_value(10)
        errors=0
        pb.set_text(u"Retriving todo-lists")
        pb.set_value(20)
        try:
            newprojects=[[[]]]
            for i in range(0,len(projects)):
                pb.set_value(20 + 80*i/(len(projects)+len(newprojects)))
                pb.set_text(u"Getting projects...")
                newprojects[0]+=[[unicode(projects[i]['name'],'utf_8'),0,projects[i]['id'],0]]
                #apppuifw2.note(unicode(str(i)) + "/" + unicode(str(len(projects))))
                try:
                    newprojects+=[[[]]]
                    todo=self.getUncompletedItems(projects[i]['id'])
                    for j in range(0,len(todo)):
                        newprojects[i+1]+=[[unicode(todo[j]['content'],'utf_8'),0,todo[j]['id'],int(todo[j]['priority'])]]
                    
                    todo=self.getCompletedItems(projects[i]['id'])
                    for j in range(0,len(todo)):
                        newprojects[i+1]+=[[unicode(todo[j]['content'],'utf_8'),1,todo[j]['id'],int(todo[j]['priority'])]]
                except:
                    errors+=1
                    appuifw2.note(u"Errors: " + str(errors))
            base=[]
            for i in range(0,len(newprojects)):
                pb.set_text(u"Getting new projects")
                pb.set_value(20 + 80*(i+len(projects))/(len(projects)+len(newprojects)))
                base+=[[]]
                base[i]+=[newprojects[i][0]]
                for j in range(1,len(newprojects[i])):
                    base[i]+=[[]]
                    try:
                        base[i][j]=appuifw2.Item(newprojects[i][j][0], id=newprojects[i][j][2], priority=newprojects[i][j][3])
                    except:
                        base[i][j]=appuifw2.Item(newprojects[i][j][0], id=None, priority=newprojects[i][j][3])
                    base[i][j].marked=newprojects[i][j][1]
            if errors==0:
                pb.set_text(u"Download succesful")
        except:
            pb.close()
            del pb
            odp=appuifw2.query(u"An error occured, try again?", 'query')
            if odp:
                self.downloadBase()
            else:
                pass
                loadBase()
        pb.close()
        del pb
        saveBase()
        try:
            del todo
        except:
            pass
        loadBase()
        
        
    def uploadBase(self):
        global base, deltodo
        
        length=0
        for i in base:
            length+=len(i)
            
        pb = ProgressBar(start=0, end=(len(deltodo[1])+len(deltodo[0])+length))
        pb.set_value(0)
        
        
        
        try:
            if deltodo[1]!=[]:
                pb.set_text(u"Deleting items from server")
                for i in deltodo[1]:
                    pb.set_value(i)
                    self.delItem(i[0],i[1])
                deltodo[1]=[]
        except:
            appuifw2.note(u"Delete unsuccesful")
        try:
            if deltodo[0]!=[]:
                pb.set_text(u"Deleting projects from server")
                for k in deltodo[0]:
                    pb.set_value((len(deltodo[1])+k))
                    self.delProject(k)
                deltodo[0]=[]
        except:
            appuifw2.note(u"Delete unsuccesful")
            
        pb.set_text(u"Sending list headers to todoist")
        #swiezo dopisane
        for i in range(1, len(base[0])):
            pb.set_value((len(deltodo[1])+len(deltodo[0])+i))
            try:
                base[0][i].id=self.updateProject(base[0][i].title, base[0][i].priority, base[0][i].id)
            except:
                appuifw2.note(u"Error on element " + i.title)
        
        total=0
        for j in range(1, len(base)):
            if base[0][j].id==None:
                continue
            pb.set_text(u"Sending List " + base[0][j].title)
            
            for i in range(1, len(base[j])):
                try:
                    base[j][i].id=self.updateItem(base[j][i].title, base[j][i].id, base[j][i].marked, base[j][i].priority, base[0][j].id)
                    
                    pb.set_value((len(deltodo[1])+len(deltodo[0])+len(base[0])+total))
                except:
                    appuifw2.note(u"Error on element " + i.title)
                total+=1
        saveBase()
        try:
            pb.close()
            del pb
        except:
            pass
        
        


def pickNumber():
    global atext
    showpeople=[]
    db = contacts.open()
    allo=[]
    for i in db.keys():
        showpeople+=[db.__getitem__(i).title]
        allo+=[i]
    b=appuifw2.selection_list(showpeople,1)
    if b!=None:
        atext=allo[b]
        mobile = db.__getitem__(allo[b]).find('mobile_number')
        phone = db.__getitem__(allo[b]).find('phone_number')
        email = db.__getitem__(allo[b]).find('email_address')
        lista=[]
        if len(mobile)>0:
            for i in mobile:
                lista.extend([i.value])
        if len(phone)>0:
            for i in phone:
                lista.extend([i.value])
        if len(email)>0:
            for i in email:
                lista.extend([i.value])
        if len(lista)>1:
            c=appuifw2.popup_menu(lista, u"Wybierz numer:")
            if c!=None:
                return lista[c]
            else:
                return None
        elif len(lista)==1:
            return lista[0]
        else:
            appuifw2.note(u"The contact doesn't contain a phone number or email!")
            return None
    else:
        return None
    
def buildRepeat(start, edit=0):
    global days, months
    posibles=['daily','weekly','monthly_by_days','monthly_by_dates','yearly_by_date','yearly_by_day']
    a=appuifw2.popup_menu([u'daily',u'weekly',u'monthly by days',u'monthly by dates',u'yearly by date',u'yearly by day'], u"Repeat it")
    if a==0:
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    elif a==1:
        replist=appuifw2.multi_selection_list(days)
        replist=list(replist)
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    elif a==2:
        selection=[]
        for i in range(0,5):
            for k in range(0,7):
                selection+=[str(i+1) + u" week " + str(days[k])]
        b=appuifw2.multi_selection_list(selection)
        b=list(b)
        if b!=[]:
            replist=[]
            for i in b:
                replist+=[{"week":i/7, "day": i%7}]
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    elif a==3:
        def uni(x):
            return unicode(x)
        mapped=map(uni,range(1,31))
        replist=appuifw2.multi_selection_list(mapped)
        replist=list(replist)
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    elif a==4:
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    elif a==5:
        selection=[]
        reals=[]
        for z in range(0,12):
            for i in range(0,5):
                for k in range(0,7):
                    selection+=[str(months[z]) + u" week "  + str(i+1) + u" day " +  str(days[k])]
                    reals+=[[z,i,k]]
        b=appuifw2.selection_list(selection)
        if b!=None:
            replist={"month":reals[b][0],"week":reals[b][1], "day": reals[b][2]}
        b=appuifw2.query(u"Interval",'number',1)
        if b<=0:
            b=1
        addexcept=appuifw2.query(u"Add an exception?", 'query')
        exclist=[]
        while addexcept:
            c=appuifw2.query(u"Exception day (Tomorow default)", 'date', viewday+3600*24)
            exclist.extend([c])
            if c==None:
                break
        if exclist==[None]:
            exclist=[]
        d=appuifw2.query(u"Repeat end (exit for forever)", 'date', viewday+3600*24*7)
        if d==None:
            d=2*start
        else:
            d-=3600*24
    else:
        return None
    repeat={"type":posibles[a],"exceptions":exclist,"start":start,"end":d,"interval":b}
    if a in [1,2,3,5]:
        repeat={"type":posibles[a],"days":replist,"exceptions":exclist,"start":start,"end":d,"interval":b}
    return repeat


def putIt():
    global ideacat, cati, inHand, c1, eventsEmpty
    which2=appuifw2.app.body.current()
    if cati==len(ideacat):
        c1=appuifw2.app.body.current()
    else:
        c1=0
        for i in ideas:
            if int(i[4])==int(cati):
                which2-=1
            c1+=1
            if which2==-1:
                break
        if which2!=-1:
            return 0
    c3=[u"Let me choose",u"Closest free time"]
    c2 = appuifw2.popup_menu(c3, u"Put it:") 
    if c2==0:
        c1=appuifw2.app.body.current()
        appuifw2.app.left_navi_arrow=False
        appuifw2.app.right_navi_arrow=False
        appuifw2.app.menu_key_handler=None
        appuifw2.app.menu_key_text=u'Options'
        predraw()
        buildcanvas('Landscape')
        gradient()
        draw(events)
        drawSms()
        eventsSpace(events)
        if eventsEmpty==[]:
            appuifw2.note(u"It's a past day, can't insert it here")
        inHand=2
    if c2==1:
        eventsSpace(events)
        for i in eventsEmpty:
            if viewday+i[2]*3600+i[3]*60>time.time():
                if viewday+i[0]*3600+i[1]*60<time.time():
                    if viewday+i[2]*3600+i[3]*60-time.time()>=ideas[c1][1]:
                        i[0]=int((time.time()-viewday)/3600)
                        i[1]=int(((time.time()-viewday)/60)%60)
                        make_event(ideas[c1],i,1)
                        del ideas[c1]
                        return 0
                    continue
                elif i[2]*3600+i[3]*60-i[0]*3600+i[1]*60>=ideas[c1][1]:
                    make_event(ideas[c1],i,1)
                    del ideas[c1]
                    return 0
            continue
        appuifw2.note(u"Sorry, no free space available on this day")
        
#Prepare a list of empty spaces [From events list creates eventsEmpty]
def eventsSpace(events):
    global eventsEmpty, hstart, hstop, viewday, countMerged
    #Checking if day is totaly free
    countMerged=[]
    if events==[[]]:
        #If time now is below the time schedule
        if time.time()-hstart*3600<viewday:
            eventsEmpty=[[hstart,0,hstop,0,unicode(str((hstop-hstart)*60)), u" minutes", 0, (hstop-hstart)*60]]
        #When time is somewhere in the middle
        elif time.time()>viewday+hstop*3600:
            eventsEmpty=[[hstart,0,hstop,0,unicode(str((hstop-hstart)*60)), u" minutes", 0, (hstop-hstart)*60]]
        else:
            eventsEmpty=[[hstart,0,int((time.time()-viewday)/3600),int(((time.time()-viewday)%3600)/60),unicode(int((time.time()-hstart*3600-viewday)/60+((time.time()-viewday)%3600)/60)), u" minutes", 0, int((time.time()-hstart*3600-viewday)/60+((time.time()-viewday)%3600)/60) ], [int((time.time()-viewday)/3600),int(((time.time()-viewday)%3600)/60),hstop,0,unicode(int((hstop*3600-time.time()+viewday)/60+((time.time()-viewday)%3600)/60)), u" minutes", 0, int((hstop*3600-time.time()+viewday)/60+((time.time()-viewday)%3600)/60)]]
    else:
        eventsEmpty=[]
        varr=[hstart,0]
        #Usual, unempty day
        #A loop over all events in the prepare() day
        k=0
        puste=0
        for i in events:
            #If time is below the timetable current loop event
            k+=1 
            dif=i[1]+(i[0]*60)-varr[0]*60-varr[1]
            if (dif>0):
                eventsEmpty.extend([[varr[0],varr[1],i[0],i[1],unicode(str(dif)),u" minutes",i[-1],dif]])
                countMerged.extend([puste])
            else:
                #countMerged+=1
                puste+=1
                
            #countMerged.extend(k*[countMerged[-1]])
            varr=[i[2],i[3]]
        countMerged.extend([puste])

        if ((hstop*60)-varr[0]*60-varr[1])>0:
            eventsEmpty.extend([[varr[0],varr[1],hstop,0, unicode(hstop*60-varr[0]*60-varr[1]),u" minutes",0,hstop*60-varr[0]*60-varr[1]]])

def makeEvent(idea,space, ok=0):
    #This function creates an event in standard calendar using given idea and space, optional options like spliting will be added soon
    global viewday, ideacat, alarm, c1
    b=calendar.open()
    c=b.add_appointment()
    c.content=idea[3]
    c.location=idea[4]
    
    if ok:
        c.set_time(viewday+space[0]*3600+space[1]*60,viewday+space[0]*3600+space[1]*60+ideas[c1][1])
    else:
        c.set_time(viewday+space[0]*3600+space[1]*60,viewday+space[2]*3600+space[3]*60)
    if not alarm:
        noyes=appuifw2.query( u"Set Alarm ?","query")
        if noyes:
            c.priority=2
            c.alarm=viewday+int(space[0])*3600+int(space[1])*60
        else:
            c.priority=0
    else:
        c.priority=2
        c.alarm=viewday+int(space[0])*3600+int(space[1])*60
    c.commit()
    forwatch()
    prepare(viewday)
    gradient()
    draw(events)
    drawSms()
    return c.id
    
def delEvent():
    global selected, events
    b=calendar.open()
    b.__delitem__(events[selected][-1])
    del events[selected]
    gradient()
    draw(events)
    
def editEvent():
    global selected, events, viewday
    a=[]
    for i in ideacat:
        a.extend([i[0]])

    data=[(u'Idea','text',events[selected][4]),(u'Category','combo', (a,int(events[selected][5]))),(u'Silent','combo', ([u"No",u"Yes"],int(events[selected][6]%2))),(u'Alarm','combo', ([u"No",u"Yes"],int(events[selected][6]/2))),(u'Event start','time',float(events[selected][0]*3600+events[selected][1]*60)),(u'Event end','time',float(events[selected][2]*3600+events[selected][3]*60)),(u'Event date','date',viewday)]
    flags = appuifw2.FFormEditModeOnly
    f=appuifw2.Form(data,flags)
    f.execute()
    events[selected][4]=f[0][2]
    events[selected][5]=f[1][2][1]
    events[selected][0]=int((f[4][2])/3600)
    events[selected][1]=int((f[4][2])%3600/60)
    events[selected][2]=int((f[5][2])/3600)
    events[selected][3]=int((f[5][2])%3600/60)
    events[selected][6]=int(f[2][2][1])+2*int(f[3][2][1])
    if f[6][2] != viewday:
        event=events[selected]
        viewday=f[6][2]
        prepare(viewday)
        if events==[[]]:
            events=[]
        events.extend([event])
        overwrite(-1)
        forwatch()
        events.sort()
        draw(events)
        drawRectangle(events)
        return 0
    
    overwrite(selected)
    forwatch()
    draw(events)
    drawRectangle(events)

def newEvent():
    global events, inHand, eventCopy, hstop, hstart, mode, eventsEmpty, selected, eventCopy, alarm
    a=appuifw2.query(u"Event name:",'text')
    if (a!="" and a!=None):
        eventCopy= a
        eventsSpace(events)
        selected=0
        inHand=-2
        gradient()
        draw(events)
        drawRectangle(eventsEmpty)
        
        

def newReminder():
    global inHand, events, viewday, hline, remindinfo
    a=appuifw2.query(u"Reminder name:",'text',remindinfo)
    if a!='' and a!=None:
        c=calendar.open()
        b=c.add_event()
        b.content=unicode(a)
        b.set_time(viewday+hline*60)
        b.alarm=viewday+hline*60
        b.commit()
        #appuifw2.note(u"New reminder succesfuly added")
        prepare(viewday)
    else:       
        appuifw2.note(u"Adding canceled")
    inHand=0
    drawSms()
    gradient()
    draw(events)
    drawRectangle(events)
    drawSignal()
    remindinfo=u""

def sendMessage():
    global inHand, events, viewday, hline, smsList, messageinfo, atext, d
    smsList.extend([[viewday+hline*60,d,appuifw2.app.body.get(),atext]])
    inHand = 0
    for i in range(0,len(smsList)):
        if smsList[i][0]<time.time():
            del smsList[i]
    smsList.sort()
    pickle.dump(smsList,open('C:\\idealist\\smses.txt','w'))
    messageinfo=u""
    d=None
    atext=None
    quit()

def newMessage():
    global messageinfo, atext, d
    if d==None:
        d = pickNumber()
    if d!=None:
        try:
            shortk=appuifw2.Text(text=unicode(messageinfo))
            appuifw2.app.screen='normal'
            appuifw2.app.menu_key_text=u"Save"
            appuifw2.app.menu_key_handler=sendMessage
            appuifw2.app.body=shortk
        except:
            appuifw2.note(u"Error sending message")

def newVoiceNote():
    global recording, snd, voiceNote
    voiceNote= str(int(time.time()))
    snd=audio.Sound.open("C:\\idealist\\"+ voiceNote +".wav")
    appuifw2.note(u"Talk after this message dissapears.")
    recording=1
    snd.record()

def newAnniversary():
    global viewday, events, inHand, annivsinfo, kalendarz
    if annivsinfo==None:
        a=appuifw2.popup_menu([u'Choose a person for birthday',u'Free text'],u'Aniversary...')
        if a==0:
            showpeople=[]
            db = contacts.open()
            allo=[]
            for i in db.keys():
                showpeople+=[db.__getitem__(i).title]
                allo+=[i]
            b=appuifw2.selection_list(showpeople,1)
            if b!=None:
                annivsinfo = unicode(showpeople[b])
        elif a==1:
            annivsinfo=appuifw2.query(u"Anniversary of...?", 'text',"")
        else:
            appuifw2.note(u"Adding canceled")
            
    else:
        annivsinfo=appuifw2.query(u"Anniversary of...?", 'text',annivsinfo)
    
    if annivsinfo!=None:
        b=kalendarz.add_anniversary()
        b.content=unicode(annivsinfo)
        b.set_time(viewday)
        #b.alarm=viewday+hstart*3600
        b.commit()
        #appuifw2.note(u"New anniversary succesfuly added")
        prepare(viewday)
        forwatch()
    inHand=0
    gradient()
    draw(events)
    drawRectangle(events)
    drawSms()
    drawSignal()
    annivsinfo=None    
def overwrite(michal=-2):
    global events, selected, start, viewday
    changed=0
    if michal==-2:
        michal=selected
        changed=1
    b=calendar.open()    
    c=b.__getitem__(events[michal][-1])
    c.begin()
    alarminfo=c.priority
    if c.get_repeat()!=None:
        choices = [u"This only", u"Future", u"All"]
        index = appuifw2.popup_menu(choices, u"Save "+events[michal][4])
        if index==0:
            #Make the old event end at the start day of the new one
            zz=c.get_repeat()
            zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
            c.set_repeat(zz)
            c.commit()
            #Make a new shit
            d=b.add_appointment()
            d.content=events[michal][4]
            d.location=events[michal][5]
            d.priority=events[michal][6]
            d.set_time(viewday+events[michal][0]*3600+events[michal][1]*60,viewday+events[michal][2]*3600+events[michal][3]*60)
            try:
                if int(alarminfo)/2>0:
                    d.alarm=viewday+events[michal][0]*3600+events[michal][1]*60
                else:
                    d.alarm=None
            except:
                pass
            d.commit()
        if index==1:
            #Make the old event end at the start day of the new one
            c.set_time(c.start_time,c.end_time)
            c.alarm=c.start_time
            zz=c.get_repeat()
            zzz=dict(zz)
            zz['end']=viewday-2*(24*3600)
            try:
                c.set_repeat(zz)
            except:
                b.__delitem__(events[michal][-1])
            c.commit()
            #Make a new shit
            c=b.add_appointment()
            c.content=events[michal][4]
            c.location=events[michal][5]
            c.priority=events[michal][6]
            c.set_time(viewday+events[michal][0]*3600+events[michal][1]*60,viewday+events[michal][2]*3600+events[michal][3]*60)
            try:
                if int(alarminfo)/2>0:
                    c.alarm=viewday+events[michal][0]*3600+events[michal][1]*60
                else:
                    c.alarm=None
            except:
                pass
            zzz['start']=viewday
            c.set_repeat(zzz)
            c.commit()
        elif index==2:
            #Make the old event end at the start day of the new one
            c.content=events[michal][4]
            c.location=events[michal][5]
            c.priority=events[michal][6]
            c.set_time(viewday+events[michal][0]*3600+events[michal][1]*60,viewday+events[michal][2]*3600+events[michal][3]*60)
            try:
                if int(alarminfo)/2>0:
                    c.alarm=viewday+events[michal][0]*3600+events[michal][1]*60
                else:
                    c.alarm=None
            except:
                pass
            c.commit()
    else:
        c.content=events[michal][4]
        c.location=events[michal][5]
        c.priority=events[michal][6]
        c.set_time(viewday+events[michal][0]*3600+events[michal][1]*60,viewday+events[michal][2]*3600+events[michal][3]*60)
        try:
            if int(alarminfo)/2>0:
                c.alarm=viewday+events[michal][0]*3600+events[michal][1]*60
            else:
                c.alarm=None
        except:
            pass
        c.commit()
    forwatch()
def delEvent(sel):
    global events
    #DELETE EVENT INTELI GENTLY
    b=calendar.open()
    c=b.__getitem__(events[sel][-1])
    zz=c.get_repeat()
    if zz!=None:
        choices=[u"Remove this only", u"Remove this & future", u"Remove all"]
        index = appuifw2.popup_menu(choices, u""+ events[sel][4])
        if index==2:
            b.__delitem__(events[sel][-1])
            del events[sel]
            forwatch()
        elif index==1:
            c.begin()
            zz['end']=viewday-2*(24*3600)
            c.set_repeat(zz)
            c.commit()
            del events[sel]
            forwatch()
        elif index==0:
            b=calendar.open()
            c.begin()
            zz=c.get_repeat()
            zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
            c.set_repeat(zz)
            c.commit()
            del events[sel]
            forwatch()
            return 1
        else:
            return 0
    else:
        yesno=appuifw2.query(u"Remove event "+ events[sel][4],"query")
        if yesno:
            b.__delitem__(events[sel][-1])
            del events[sel]
            forwatch()
            return 1
            #END DELETE EVENT INTELIGENTLY
        return 0
    

def move(time):
    global events, selected, hstop, hstart, anychange, savelist, inHand, eventCopy, anychange, viewday, mode, start, eventsEmpty, hline
    if inHand==0:
        if mode == 0:
            if time>0:
                selected+=1
            else:
                selected-=1
            gradient()
            draw(events)
            drawRectangle(events)
                
        elif mode==1:
            anychange = 1
            if (hstop*60<=eventCopy[2]*60+eventCopy[3]+time):
                time=hstop*60-eventCopy[2]*60-eventCopy[3]
            elif (hstart*60>=eventCopy[0]*60+eventCopy[1]+time):
                time=hstart*60-eventCopy[0]*60-eventCopy[1]
            eventCopy[0]+=((eventCopy[1]+time)/60)
            eventCopy[1]=((eventCopy[1]+time)%60)
            eventCopy[2]+=((eventCopy[3]+time)/60)
            eventCopy[3]=((eventCopy[3]+time)%60)
            gradient()
            draw(events)
            drawHalf()
        elif mode==2:
            anychange=1
            if selected not in savelist:
                savelist+=[selected]
            if (time>0):
                if selected==len(events)-1:
                    if (hstop*60<=events[selected][2]*60+events[selected][3]+time):
                        time=hstop*60-events[selected][2]*60-events[selected][3]
                    if events[selected][1]+time>=60:
                        events[selected][1]=events[selected][1]+time-60
                        events[selected][0]+=1
                        if events[selected][3]+time>=60:
                            events[selected][3]=events[selected][3]+time-60
                            events[selected][2]+=1
                        else:
                            events[selected][3]+=time
                    elif events[selected][3]+time>=60:
                        events[selected][3]=events[selected][3]+time-60
                        events[selected][2]+=1
                        events[selected][1]+=time
                    else:
                        events[selected][1]+=time
                        events[selected][3]+=time
                    
                elif (events[selected+1][0]*60+events[selected+1][1]-events[selected][2]*60-events[selected][3]<time):
                    if selected+1 not in savelist:
                        savelist+=[selected+1]
                    copysel = list(events[selected])
                    copysel1= list(events[selected+1])
                    events[selected]=list(events[selected+1])
                    events[selected+1]=list(copysel)
                    #setting hour for the missed event
                    events[selected][0]=events[selected+1][0]
                    events[selected][1]=events[selected+1][1]
                    events[selected][2]=copysel1[2]-copysel1[0]+events[selected+1][0]
                    events[selected][3]=copysel1[3]-copysel1[1]+events[selected+1][1]
                    if events[selected][3]>60:
                        events[selected][2]+=1
                        events[selected][3]= events[selected][3] % 60
                    events[selected+1][0]=events[selected][2]
                    events[selected+1][1]=events[selected][3]
                    events[selected+1][2]=copysel[2]-copysel[0]+events[selected+1][0]
                    events[selected+1][3]=copysel[3]-copysel[1]+events[selected+1][1]
                    if events[selected+1][3]>60:
                        events[selected+1][2]+=1
                        events[selected+1][3]= events[selected+1][3] % 60
                    selected+=1
                else:
                    if events[selected][1]+time>=60:
                        events[selected][1]=events[selected][1]+time-60
                        events[selected][0]+=1
                        if events[selected][3]+time>=60:
                            events[selected][3]=events[selected][3]+time-60
                            events[selected][2]+=1
                        else:
                            events[selected][3]+=time
                    elif events[selected][3]+time>=60:
                        events[selected][3]=events[selected][3]+time-60
                        events[selected][2]+=1
                        events[selected][1]+=time
                    else:
                        events[selected][1]+=time
                        events[selected][3]+=time
            elif (time<0):
                if selected==0:
                    if (hstart*60>=events[selected][0]*60+events[selected][1]+time):
                        time=hstart*60-events[selected][0]*60-events[selected][1]
                    if events[selected][1]+time<0:
                        events[selected][1]=60+time+events[selected][1]
                        events[selected][0]-=1
                        if events[selected][3]+time<0:
                            events[selected][3]=60+time+events[selected][3]
                            events[selected][2]-=1
                        else:
                            events[selected][3]+=time
                    elif events[selected][3]+time<0:
                        events[selected][3]=60+time+events[selected][3]
                        events[selected][2]-=1
                        events[selected][1]+=time
                    else:
                        events[selected][1]+=time
                        events[selected][3]+=time
                elif (events[selected][0]*60+events[selected][1]-events[selected-1][2]*60-events[selected-1][3]<-time):
                    if selected-1 not in savelist:
                        savelist+=[selected-1]
                    copysel = list(events[selected])
                    copysel1= list(events[selected-1])
                    events[selected]=list(events[selected-1])
                    events[selected-1]=list(copysel)
                    events[selected-1][0]=copysel1[0]
                    events[selected-1][1]=copysel1[1]
                    events[selected-1][2]=copysel[2]-copysel[0]+events[selected-1][0]
                    events[selected-1][3]=copysel[3]-copysel[1]+events[selected-1][1]
                    if events[selected-1][3]<0:
                        events[selected-1][2]-=1
                        events[selected-1][3]= events[selected-1][3] % 60
                    #setting hour for the missed event
                    events[selected][0]=events[selected-1][2]
                    events[selected][1]=events[selected-1][3]
                    events[selected][2]=copysel1[2]-copysel1[0]+events[selected][0]
                    events[selected][3]=copysel1[3]-copysel1[1]+events[selected][1]
                    if events[selected][3]<0:
                        events[selected][2]-=1
                        events[selected][3]= events[selected][3] % 60
                    selected-=1
                else:
                    if events[selected][1]+time<=0:
                        events[selected][1]=60+time+events[selected][1]
                        events[selected][0]-=1
                        if events[selected][3]+time<0:
                            events[selected][3]=60+time+events[selected][3]
                            events[selected][2]-=1
                        else:
                            events[selected][3]+=time
                    if events[selected][3]+time<0:
                        events[selected][3]=60+time+events[selected][3]
                        events[selected][2]-=1
                        events[selected][1]+=time
                    else:
                        events[selected][1]+=time
                        events[selected][3]+=time
            gradient()
            draw(events)
            drawOutline()
        elif mode==3:
            anychange=1
            if selected not in savelist:
                savelist+=[selected]
            if start:
                if (time > 0):
                    if (hstop*60<=events[selected][2]*60+events[selected][3]+time):
                        time=hstop*60-events[selected][2]*60-events[selected][3]
                    if selected==len(events)-1:
                        events[selected][2]+=((events[selected][3]+time)/60)
                        events[selected][3]=((events[selected][3]+time)%60)
                    elif (events[selected + 1][0]*60+events[selected+1][1]-events[selected][2]*60-events[selected][3]<time):
                        #Co jesli nastepne zdarzenie stanie sie zbyt krotkie?
                        if selected+1 not in savelist:
                            savelist+=[(selected+1)]
                        
                        roznica=events[selected+1][2]*60+events[selected+1][3]-events[selected][2]*60-events[selected][3]
                        if (roznica<=time):
                            backup=events[selected+1]
                            if (delEvent(selected+1)):
                                events[selected][2]=backup[2]
                                events[selected][3]=backup[3]
                            draw(events)
                            drawAdjust()
                        else:
                            events[selected][2]+=((events[selected][3]+time)/60)
                            events[selected][3]=((events[selected][3]+time)%60)
                            events[selected+1][0]=events[selected][2]
                            events[selected+1][1]=events[selected][3]
                    else:
                        events[selected][2]+=((events[selected][3]+time)/60)
                        events[selected][3]=((events[selected][3]+time)%60)
                #events[selected][2]+=time
                elif (time < 0):
                    if ((events[selected][2]*60+events[selected][3]-events[selected][0]*60-events[selected][1])<=-time):
                        delEvent(selected)
                        if events==[]:
                            events=[[]]
                            selection=0
                            mode=0
                            drawRectangle(selection)
                    else:
                        events[selected][2]+=((events[selected][3]+time)/60)
                        events[selected][3]=((events[selected][3]+time)%60)
            elif (not start):
                if (time < 0):
                    if (hstart*60>=events[selected][0]*60+events[selected][1]+time):
                        time=hstart*60-events[selected][0]*60-events[selected][1]
                    if selected==0:
                        events[selected][0]+=((events[selected][1]+time)/60)
                        events[selected][1]=((events[selected][1]+time)%60)
                    
                    elif (events[selected][0]*60+events[selected][1]-events[selected-1][2]*60-events[selected-1][3]<-time):
                        if (selected-1) not in savelist:
                            savelist+=[(selected-1)]
                        roznica =events[selected][0]*60+events[selected][1]-events[selected-1][0]*60-events[selected-1][1]
                        if (roznica<=-time):
                            backup=events[selected-1]
                            if (delEvent(selected-1)):
                                events[selected][0]=backup[0]
                                events[selected][1]=backup[1]
                            selected-=1
                            draw(events)
                            drawAdjust()

                        else:
                            events[selected][0]+=((events[selected][1]+time)/60)
                            events[selected][1]=((events[selected][1]+time)%60)
                            events[selected-1][2]=events[selected][0]
                            events[selected-1][3]=events[selected][1]
                    else:
                        events[selected][0]+=((events[selected][1]+time)/60)
                        events[selected][1]=((events[selected][1]+time)%60)
                elif (time>0):
                    if (events[selected][2]*60+events[selected][3]-events[selected][0]*60-events[selected][1]-time<=0):
                        delEvent(selected)
                        if events==[]:
                            events=[[]]
                            selection=0
                            mode=0
                            drawRectangle(selection)
                    else:
                        events[selected][0]+=((events[selected][1]+time)/60)
                        events[selected][1]=((events[selected][1]+time)%60)
            gradient()
            draw(events)
            drawAdjust()
    elif inHand==1:
        pass
    elif inHand==2:
        if hline+time<hstart*60:
            hline=hstart*60
        elif hline+time>hstop*60:
            hline=hstop*60
        else:
            hline+=time
        gradient()
        draw(events)
        drawHLine("reminder")
    elif inHand==-1:
        if hline+time<hstart*60:
            hline=hstart*60
        elif hline+time>hstop*60:
            hline=hstop*60
        else:
            hline+=time
        gradient()
        draw(events)
        drawHLine("message")
    elif inHand==3:
        if hline+time<hstart*60:
            hline=hstart*60
        elif hline+time>hstop*60:
            hline=hstop*60
        else:
            hline+=time
        gradient()
        draw(events)
        drawHLine("voice note")
        
    elif inHand==-2:
        if time>0:
            selected+=1
        else:
            selected-=1
        gradient()
        draw(events)
        drawRectangle(eventsEmpty)

def idea2event(i,idea):
    global viewday, alarm
    b=calendar.open()
    c=b.add_appointment()
    c.content=idea[4]
    c.location=idea[5]
    c.set_time(viewday+i[0]*3600+i[1]*60,viewday+i[2]*3600+i[3]*60)
    
    if not alarm:
        noyes=appuifw2.query( u"Set Alarm ?","query")
        if noyes:
            c.priority=2+(int(idea[6])%2)
            c.alarm=viewday+int(i[0])*3600+int(i[1])*60
        else:
            c.priority=0+(int(idea[6])%2)
    else:
        
        c.priority=0+(int(idea[6])%2)
        c.alarm=viewday+int(i[0])*3600+int(i[1])*60
    c.commit()
    forwatch()
    return c.id
    



def checkColisions():
    global eventCopy, events
    freespace=[]
    var=[eventCopy[0],eventCopy[1]]
    begining=eventCopy[0]*60 + eventCopy[1]
    end=eventCopy[2]*60 + eventCopy[3]
    if events==[[]]:
        freespace=[[hstart,0,hstop,0]]
        return freespace
    for i in events:
        if i[0]*60+i[1]<=end:
            if i[0]*60+i[1]>var[0]*60+var[1]:
                freespace.extend([[var[0],var[1],i[0],i[1]]])
            elif i[0]*60+i[1]==var[0]*60+var[1]:
                if i[2]*60 + i[3] > end:
                    return freespace
        if (i[2]*60+i[3]<=end) and (i[2]*60+i[3]>=begining):
            var=[i[2],i[3]]
        if ((i[0]*60+i[1]<=begining) and (i[2]*60 + i[3] >=end)):
            return freespace
    if (var[0]*60+var[1]<end and freespace==[]):
        freespace.extend([[var[0],var[1],eventCopy[2],eventCopy[3]]])
    return freespace
        
def handleRedraw(rect):
    if img: canvas.blit(img)

def quickEdit():
    global selected, inHand, viewday, events, mode, start, colors, anychange, ideacat, dhstop, dhstart, hstart, hstop, eventCopy, otherday, savelist, hline, cati, m, eventsEmpty, remind, smsList, messageinfo, remindinfo, annivs, annivsinfo, base, todo, missedcalls, unreadsms,weekday, menu, alarm
    b=calendar.open()
    alarminfo=0
    try:
        d=b.__getitem__(events[selected][-1])
        d.begin()
        alarminfo=int(d.priority)
        #d.close()
    except:
        appuifw2.note(u"Error building menu")
    if int(alarminfo)/2<1:
        label=u"Turn Alarm ON"
    else:
        label=u"Turn Alarm OFF"
    if int(alarminfo)%2==0:
        label2=u"Turn Silent ON"
    else:
        label2=u"Turn Silent OFF"
    
    b=appuifw2.popup_menu([u"Name",u"Category",u"Repeat rules",u"Color",label,label2,u"More"], u"Edit " + events[selected][4])
    if b==0:
        c=appuifw2.query(u"Name", 'text',unicode(events[selected][4]))
        selection=events[selected]
        if c != events[selected][4] and c!=None:
            selection[4]=c
            events[selected][4]=c
            b=calendar.open()
            d=b.__getitem__(events[selected][-1])
            d.begin()
            if d.get_repeat()!=None:
                choices = [u"This only",u"Future", u"All"]
                index = appuifw2.popup_menu(choices, u"Save on:")
                if index==0:
                    #Make the old event end at the start day of the new one
                    zz=d.get_repeat()
                    if zz!=None:
                        zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                    d.set_repeat(zz)
                    d.commit()
                    #Make a new shit
                    d=b.add_appointment()
                    d.content=selection[4]
                    d.location=selection[5]
                    d.set_time(viewday+selection[0]*3600+selection[1]*60,viewday+selection[2]*3600+selection[3]*60)
                    d.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            d.alarm=viewday+selection[0]*3600+selection[1]*60
                        else:
                            d.alarm=None
                    except:
                        pass
                elif index==1:
                    #Make the old event end at the start day of the new one
                    zz=d.get_repeat()
                    zzz=dict(zz)
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['end']=viewday-2*(24*3600)
                    d.set_repeat(zz)
                    d.commit()
                    #Make a new shit
                    d=b.add_appointment()
                    d.content=selection[4]
                    d.location=selection[5]
                    d.set_time(viewday+selection[0]*3600+selection[1]*60,viewday+selection[2]*3600+events[selected][3]*60)
                    d.priority=selection[6]
                    try:
                        if int(alarminfo)/2>0:
                            d.alarm=viewday+selection[0]*3600+selection[1]*60
                        else:
                            d.alarm=None
                    except:
                        pass
                    zzz['start']=viewday
                    d.set_repeat(zzz)
                elif index==2:
                    #Make the old event end at the start day of the new one
                    d.content=selection[4]
            else:
                d.content=selection[4]    
            
            d.commit()
            draw(events)
            drawRectangle(events)
            
    elif b==1:
        a=[]
        for i in ideacat:
            a.extend([i[0]])
        d=appuifw2.popup_menu(a, events[selected][4] + u" category")
        if d!= events[selected][5] and d!=None:
            events[selected][5]=d
            b=calendar.open()
            d=b.__getitem__(events[selected][-1])
            d.begin()
            if d.get_repeat()!=None:
                choices = [u"This only",u"Future", u"All"]
                index = appuifw2.popup_menu(choices, u"Save on:")
                if index==0:
                    #Make the old event end at the start day of the new one
                    
                    zz=d.get_repeat()
                    if zz!=None:
                        zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                    d.set_repeat(zz)
                    d.commit()
                    #Make a new shit
                    d=b.add_appointment()
                    d.content=events[selected][4]
                    d.location=events[selected][5]
                    d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                    d.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            d.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            d.alarm=None
                    except:
                        pass
                    d.commit()
                elif index==1:
                    #Make the old event end at the start day of the new one
                    
                    zz=d.get_repeat()
                    zzz=dict(zz)
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['end']=viewday-2*(24*3600)
                    d.set_repeat(zz)
                    d.commit()
                    #Make a new shit
                    d=b.add_appointment()
                    d.content=events[selected][4]
                    d.location=events[selected][5]
                    d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                    d.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            d.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            d.alarm=None
                    except:
                        pass
                    zzz['start']=viewday
                    d.set_repeat(zzz)
                    d.commit()
                elif index==2:
                    #Make the old event end at the start day of the new one
                    
                    d.location=events[selected][5]
                    d.commit()
            d.location=events[selected][5]
            d.commit()
            draw(events)
            drawRectangle(events)
    elif b==2:
        builded=buildRepeat(viewday+events[selected][0]*3600+events[selected][1]*60, 1)
        if builded != None:
            b=calendar.open()
            c=b.__getitem__(events[selected][-1])
            if c.get_repeat()!=None:
                choices = [u"Future", u"All",u"This only"]
                index = appuifw2.popup_menu(choices, u"Save on:")
                if index==0:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            c.alarm=c.start_time
                        else:
                            c.alarm=None
                    except:
                        pass
                    zz=c.get_repeat()
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['end']=viewday-2*(24*3600)
                    c.set_repeat(zz)
                    c.commit()
                    #Make a new shit
                    c=b.add_appointment()
                    c.content=events[selected][4]
                    c.location=events[selected][5]
                    c.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                    
                    c.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            c.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            c.alarm=None
                    except:
                        pass
                    c.set_repeat(builded)
                    c.commit()
                    return 0
                elif index==1:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            c.alarm=c.start_time
                        else:
                            c.alarm=None
                    except:
                        pass
                    c.set_repeat(builded)
                    c.commit()
                    return 0
                elif index==2:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            c.alarm=c.start_time
                        else:
                            c.alarm=None
                    except:
                        pass
                    zz=c.get_repeat()
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                    c.set_repeat(zz)
                    c.commit()
                    #Make a new shit
                    c=b.add_appointment()
                    c.content=events[selected][4]
                    c.location=events[selected][5]
                    c.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                    c.priority=events[selected][6]
                    try:
                        if int(alarminfo)/2>0:
                            c.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            c.alarm=None
                    except:
                        pass
                    c.commit()
                    return 0
            c.begin()
            c.set_repeat(builded)
            c.commit()
            return 0
        
    elif b==3:
        acolors=[(200,70,70),(70,200,70),(70,70,200),(200,200,70),(70,200,200),(200,70,200),(70,70,70)]
        d = appuifw2.popup_menu([u"Red",u"Green",u"Blue",u"Yellow",u"Sea",u"Violet",u"Black"], u"Choose:")
        if d!=None:
            try:
                ideacat[int(events[selected][5])][1]=acolors[d]
            except:
                appuifw2.note(u"Can't change color. Event doesn't belong to any category!")
    elif b==4:
        alarmek=None
        try:
            if int(alarminfo)/2 <1:
                alarmek=viewday+events[selected][0]*3600+events[selected][1]*60
        except:
            alarmek=None
            
        b=calendar.open()
        d=b.__getitem__(events[selected][-1])
        d.begin()
        if d.get_repeat()!=None:
            choices = [u"This only",u"Future", u"All"]
            index = appuifw2.popup_menu(choices, u"Save on:")
            if index==0:
                zz=d.get_repeat()
                if zz!=None:
                    zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                d.set_repeat(zz)
                d.commit()
                #Make a new shit
                d=b.add_appointment()
                d.content=events[selected][4]
                d.location=events[selected][5]
                d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                d.priority=(events[selected][6]+2)%4
                d.alarm=alarmek
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            elif index==1:
                #Make the old event end at the start day of the new one
                
                zz=d.get_repeat()
                zzz=dict(zz)
                #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                zz['end']=viewday-2*(24*3600)
                d.set_repeat(zz)
                d.commit()
                #Make a new shit
                d=b.add_appointment()
                d.content=events[selected][4]
                d.location=events[selected][5]
                d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                d.priority=(events[selected][6]+2)%4
                d.alarm=alarmek
                zzz['start']=viewday
                d.set_repeat(zzz)
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            elif index==2:
                d.priority=(events[selected][6]+2)%4
                d.alarm=alarmek
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            return 0
        
        d.alarm=alarmek
        d.priority=(events[selected][6]+2)%4
        d.commit()
        prepare(viewday)
        draw(events)
        drawRectangle(events)
    elif b==5:
        alarmek=None
        try:
            if int(alarminfo)/2 >0:
                alarmek=viewday+events[selected][0]*3600+events[selected][1]*60
        except:
            alarmek=None
            
        b=calendar.open()
        d=b.__getitem__(events[selected][-1])
        d.begin()
        if d.get_repeat()!=None:
            choices = [u"This only",u"Future", u"All"]
            index = appuifw2.popup_menu(choices, u"Save on:")
            if index==0:
                zz=d.get_repeat()
                if zz!=None:
                    zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                d.set_repeat(zz)
                d.commit()
                #Make a new shit
                d=b.add_appointment()
                d.content=events[selected][4]
                d.location=events[selected][5]
                d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                d.priority=(events[selected][6]+int(math.pow(-1,events[selected][6]%2)))%4
                d.alarm=alarmek
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            elif index==1:
                #Make the old event end at the start day of the new one
                
                zz=d.get_repeat()
                zzz=dict(zz)
                #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                zz['end']=viewday-2*(24*3600)
                d.set_repeat(zz)
                d.commit()
                #Make a new shit
                d=b.add_appointment()
                d.content=events[selected][4]
                d.location=events[selected][5]
                d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                dd.priority=(events[selected][6]+int(math.pow(-1,events[selected][6]%2)))%4
                d.alarm=alarmek
                zzz['start']=viewday
                d.set_repeat(zzz)
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            elif index==2:
                d.priority=(events[selected][6]+int(math.pow(-1,events[selected][6]%2)))%4
                d.alarm=alarmek
                d.commit()
                prepare(viewday)
                draw(events)
                drawRectangle(events)
                forwatch()
                return 0
            return 0
        
        d.alarm=alarmek
        d.priority=(events[selected][6]+int(math.pow(-1,events[selected][6]%2)))%4
        d.commit()
        prepare(viewday)
        draw(events)
        drawRectangle(events)
    elif b==6:
        editEvent()
    forwatch()

def menuUp():
    global menu
    menu=0
    choices = [u"Custom Event", u"Reminder", u"Anniversary", u"Message"]
    gradient()
    draw(events)
    drawRectangle(events)
    drawSms()
    drawSignal()
    handleRedraw(None)
    index = appuifw2.popup_menu(choices, u"Select:") 
    if index == 0 : 
        newEvent()
    elif index == 1 :
        appuifw2.note(u"Choose time for the reminder")
        selected=0
        
        inHand=-1
        if viewday<=time.time() and time.time()<=viewday+3600*24:
            hline=(time.time()-viewday)/60+30
        else:
            hline=((hstop-hstart)/2+hstart)*60
        draw(events)
        drawHLine("reminder")
        drawSms()
        handleRedraw(None)
    elif index == 2: 
        appuifw2.note(u"Choose a day for which the anniversary should be added")
        selected=0
        draw(events)
        inHand=0
    elif index == 3:
        selected=0
        inHand=-1
        if viewday<=time.time() and time.time()<=viewday+3600*24:
            hline=(time.time()-viewday)/60+30
        else:
            hline=((hstop-hstart)/2+hstart)*60
        draw(events)
        drawHLine("message")
        handleRedraw(None)
    return 0

def menuDown():
    global alarm, events, menu, token, screenObj
    if alarm:
        label=u"Turn Auto add alarm OFF"
    else:
        label=u"Turn Auto add alarm ON"
    if screenObj is not None:
        label2=u"Standby screen OFF"
    else:
        label2=u"Standby screen ON"
        
    menu=0
    menua=[u"Wake-sleep hours", u"Categories colors", u"Take a screenshot", u"Font", label, label2, u"Change language" ,u"App info",u"Todoist Web token", u"Update",u"Exit"]
    gradient()
    draw(events)
    drawRectangle(events)
    drawSms()
    drawSignal()
    handleRedraw(None)
    cc=appuifw2.popup_menu(menua,u"")
    if cc==0:
        setHours()
    elif cc==1:
        categoryConfig()
    elif cc==2:
        e32.ao_sleep(0.5)
        ss = graphics.screenshot()
        try:
            ss.save(u'C:\\idealist\\screenshot.png')
            decision = appuifw2.query(u"Send it by mms?","query")
            if decision:
                d=pickNumber()
                if d!=None:
                    try:
                        messaging.mms_send(d, u"Here - this is my day plan. Sent using Idealist.", u'C:\\idealist\\screenshot.png')
                    except:
                        appuifw2.note(u"The contact doesn't contain a mobile phone number!")
                appuifw2.app.screen='full'
                predraw()
                buildCanvas()
                gradient()
                draw(events)
                drawSms()
                handleRedraw(None)
        except:
            appuifw2.note(u"Can't make a screenshot")
    elif cc==3:
        changeFont()
    elif cc==4:
        alarm = not alarm
    elif cc==5:
        if screenObj is None:
            screenObj = DrawStandby()
            drawOnStandby()
        else:
            try:
                screenObj.hide()
                screenObj=None
            except:
                print "error hiding"
        saveConfig()
    elif cc==6:
        appuifw2.note(u"Sorry. This option will become available in next realese!")
    elif cc==7:
        menub=[u"Authors blog",u"Shortcut keys",u"Version info"]
        cd=appuifw2.popup_menu(menub,u"Info")
        if cd==0:
            website()
        elif cd==1:
            shortcuts()
        elif cd==2:
            version()
    elif cc==8:
        token2=appuifw2.query(u"Set token",'text', unicode(str(token)))
        if token2!=None:
            token=token2
            saveConfig()
    elif cc==9:
        update()
    elif cc==10:
        quit()
    return 0
def menuLeft():
    global menu, token, socket
    menu = 0
    gradient()
    draw(events)
    drawRectangle(events)
    drawSms()
    drawSignal()
    handleRedraw(None)
    appuifw2.note(unicode("Takes " + str((initram-sysinfo.free_ram())/1024)) + " kB")
    a=appuifw2.popup_menu([u"Upload",u"Download"], u"Sync direction")
    if a==0:
        apid = socket.select_access_point()
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)
        apo.start()
        x=Todoist(token)
        x.uploadBase()
        apo.stop()
        del x
    elif a==1:
        apid = socket.select_access_point()
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)
        apo.start()
        x=Todoist(token)
        x.downloadBase()
        apo.stop()
        del x
def menuRight():
    global menu
    menu=0
    try:
        del todo
    except:
        pass
    todo = Todo()
    return 0
def menuMiddle():
    global menu, remind, hline, remindinfo, inHand, mode, soundList, voiceNote, recording, snd, viewday, d, atext, messageinfo, annivsinfo
    menu=0
    choices = [u"This Event",u"Reminder",u"Anniversary", u"Message", u"Voice note"]
    gradient()
    draw(events)
    drawRectangle(events)
    drawSms()
    drawSignal()
    handleRedraw(None)
    index = appuifw2.popup_menu(choices, u"Select:")
    if index == 0:
        quickEdit()
    if index == 1:
        rnames=[]
        if remind!=[]:
            for i in remind:
                rnames.extend([unicode(str(i[0])+ ":" + str(i[1]) +" "+ i[2])])
            c1 = appuifw2.popup_menu(rnames,u"Reminder:")
            if c1!=None:
                a=calendar.open()
                a.__delitem__(remind[c1][-1])
                hline=remind[c1][0]*60+remind[c1][1]
                remindinfo=unicode(remind[c1][2])
                del remind[c1]
                selected=0
                inHand=2
                gradient()
                draw(events)
                drawSms()
                drawHLine("reminder")
                handleRedraw(None)
        else:
            appuifw2.note(u"No reminders found!")
    elif index == 2: 
        if annivs!=[]:
            names=[]
            for i in annivs:
                names.extend([i[0]])
            c1 = appuifw2.popup_menu(names,u"Anniversary:")
            if c1!=None:
                inHand=1
                appuifw2.note(u"Choose the day")
                annivsinfo=annivs[c1][0]
                a=calendar.open()
                a.__delitem__(int(annivs[c1][1]))
                del annivs[c1]
                gradient()
                draw(events)
                drawSms()
                handleRedraw(None)
        else:
            appuifw2.note(u"No anniversaries found!")
    elif index == 3:
        sms=[]
        if smsList!=[]:
            db=contacts.open()
            for i in smsList:
                if (0<=(int(i[0])-viewday)) and (3600*24 >(int(i[0])-viewday)):
                    sms.extend([unicode(int(i[0]-viewday)/3600)+":"+str(int((i[0]-viewday)%3600/60))+" "+db.__getitem__(int(i[3])).title+"-" +i[2]])
            c1 = appuifw2.popup_menu(sms,u"Sms list:")
            if c1!=None:
                hline=(smsList[c1][0]-viewday)/60
                selected=0
                messageinfo=unicode(smsList[c1][2])
                atext=smsList[c1][3]
                d=smsList[c1][1]
                del smsList[c1]
                smsList.sort()
                pickle.dump(smsList,open('C:\\idealist\\smses.txt','w'))
                selected=0
                inHand=-1
                gradient()
                draw(events)
                drawSms()
                drawHLine("message")
                handleRedraw(None)
        else:
            appuifw2.note(u"No messages found!")
    elif index == 4: 
        if soundList!=[]:
            s=[]
            for i in soundList:
                if (0<=(int(i[0])-viewday)) and (3600*24 >(int(i[0])-viewday)):
                    s.extend([unicode(str(time.gmtime(i[0])))])
            c1 = appuifw2.popup_menu(s,u"Voice notes list:")
            if c1!=None:
                hline=(soundList[c1][0]-viewday)/60
                selected=0
                inHand=3
                gradient()
                draw(events)
                drawSms()
                drawHLine("voice note")
                voiceNote=soundList[c1][1]
                del soundList[c1]
                soundList.sort()
                pickle.dump(smsList,open('C:\\idealist\\sounds.txt','w'))
                recording=1
                snd=audio.Sound.open("C:\\idealist\\"+ voiceNote +".wav")
                handleRedraw(None)
        else:
            appuifw2.note(u"No voice notes found!")
    return 0


def checkAndAdd():
    global eventCopy, selected, inHand, events, viewday, mode, eventsEmpty, ideacat, alarm, countMerged
    b=calendar.open()
    c=b.add_appointment()
    c.content=eventCopy
    
    b=[]
    for i in ideacat:
        b.extend([unicode(i[0])])
        
    category=appuifw2.popup_menu(b,u"Choose a category")
    if category!=None:
        c.location=category
    else:
        c.location=0
    start=eventsEmpty[selected][0]*3600+eventsEmpty[selected][1]*60
    end=eventsEmpty[selected][2]*3600+eventsEmpty[selected][3]*60
    if (end -start)>3600:
        much=(end-start-3600)/2
        start+=much
        end-=much
    c.set_time(viewday + start,viewday+end)
    
    if not alarm:
        noyes=appuifw2.query( u"Set Alarm ?","query")
        if noyes:
            c.priority=2
            c.alarm=viewday + start
        else:
            c.priority=0
    else:
        c.priority=2
        c.alarm=viewday + start
    
    
    c.commit()
    #this was added tonight
    try:
        selected=selected + countMerged[selected]
    except:
        pass
    countMerged=[]
    prepare(viewday)
    gradient()
    drawSms()
    #if (viewday + start>=time.time()):
    #    selected+=1
    inHand=0
    mode=3
    drawSignal()
    draw(events)
    drawAdjust()
    forwatch()
#This thing handles buttons which are being clicked
def handleEvent(event):
    global selected, ideas,inHand, viewday, events, mode, start, clors, anychange, ideacat, dhstop, dhstart, hstart, hstop, eventCopy, otherday, savelist, hline, cati, m, eventsEmpty, remind, smsList, messageinfo, remindinfo, annivs, annivsinfo, base, todo, missedcalls, unreadsms,weekday, menu, alarm, screenObj, snd, voiceNote, soundList, recording, girls, money, mToggle, goods
    ev = event['keycode']
    pi = event['scancode']
#This part in part used to be a redraw triggerer in past - not needed anymore
#    if event['type'] == idealistappuifw2.EEventKeyDown: 
#        gradient()
#        draw(events)
    if pi == key_codes.EScancodeEdit:
        if inHand==0:
            if mode==0:
                try:
                    if events[selected]==[]:
                        appuifw2.note(u"Nothing to edit!")
                        return 0
                except:
                    pass
                gradient()
                mode=1
                eventCopy=list(events[selected])
                del events[selected]
                otherday=viewday
                draw(events)
                drawHalf()
    
    elif ev == key_codes.EKey1:
        if mode==0 or mode==1:
            a=appuifw2.query(u"Go to:", 'date', currentday)
            if viewday!=a and a!=None:
                weekday+=int((a-viewday)/86400)
                weekday=weekday%7
                viewday=a
                prepare(viewday)
                gradient()
                draw(events)
                drawSms()
                drawSignal()
                if mode==1:
                    anychange = 1
                    drawHalf()
                elif inHand==-1:
                    drawHLine("message")
                elif inHand==2:
                    drawHLine("reminder")
                elif inHand==-2:
                    eventsSpace(events)
                    drawRectangle(eventsEmpty)
                elif inHand==0:
                    drawRectangle(events)
        else:
            return 0
                
    elif ev == key_codes.EKey3 and inHand==0 and mode==0:
        newEvent()
        return 0
    
    elif ev == key_codes.EKey0 and inHand==0 and mode==0:
        if len(base[0][1:])<1:
            todo=Todo(theid=1)
            saveBase()    
        args=[]
        for i in base[0][1:]:
            args+=[i.title]
        c=appuifw2.popup_menu(args,u"")
        if c!=None:
            todo=Todo(index=(c+1))
        loadBase()
        return 0
    
    elif ev == key_codes.EKey2 and inHand==0 and mode==0:
        """
        if len(money[mToggle])<1:
            a=appuifw2.query(unicode(WALUTY[mToggle]+ " Startup" ), "float")
            if a!=None and a>0:
                money[mToggle].extend([float(a)])
            return 0
        else:
            b=appuifw2.popup_menu(goods, u"Spent on:")
            if b==None:
                b=appuifw2.query(u"Spent on:","text",u"")
                if b==None:
                    return 0
            a=appuifw2.query(unicode(WALUTY[mToggle] + " Cost" ), "float")
            if a!=None and a>0:
                money[mToggle][0]-=float(a)
                money[mToggle].extend([(-float(a),unicode(b),time.time())])
            saveConfig()
        return 0
        """ 
    elif ev == key_codes.EKey5 and inHand==0 and mode==0:
        """
        if len(money[mToggle])<1:
            a=appuifw2.query( unicode(WALUTY[mToggle] +" Startup"), "float")
            if a!=None and a>0:
                money[mToggle].extend([float(a)])
            return 0
        else:
            b=appuifw2.query(u"Earned on:","text",u"")
            if b==None:
                return 0
            a=appuifw2.query(unicode(WALUTY[mToggle] + u" Amount"), "float")
            if a!=None and a>0:
                money[mToggle][0]+=float(a)
                money[mToggle].extend([(float(a),unicode(b),time.time())])
            saveConfig()
        return 0
        """
    elif ev == key_codes.EKey8 and inHand==0 and mode==0:
        """
        mToggle=not mToggle
        if not mToggle:
            appuifw2.note(u"PLN...")
        else:
            appuifw2.note(u"USD...")
        return 0
        """
    elif ev == key_codes.EKey6 and inHand==0 and mode==0:
        inHand=2
        gradient()
        draw(events)
        current=time.time()-viewday
        if current>0 and current<3600*24:
            hline=(time.time()-viewday)/60 + 30
        else:
            hline=(hstart*60+(hstop-hstart)*30)
        drawSignal()
        drawHLine("reminder")
        return 0
        
    elif ev == key_codes.EKey9 and inHand==0 and mode==0:
        inHand=1
        gradient()
        draw(events)
        return 0
    elif ev==key_codes.EKeyStar and inHand==0 and mode==0:
        inHand=3
        gradient()
        draw(events)
        current=time.time()-viewday
        if current>0 and current<3600*24:
            hline=(time.time()-viewday)/60 + 30
        else:
            hline=(hstart*60+(hstop-hstart)*30)
        drawHLine("voice note")
        return 0
    
    elif ev==key_codes.EKey7 and inHand==0 and mode==0:
        try:
            if events[selected]==[]:
                appuifw2.note(u"Nothing to copy!")
                return 0
        except:
            pass
        gradient()
        mode=1
        eventCopy=list(events[selected])
        eventCopy[-1]=None
        otherday=viewday
        draw(events)
        drawHalf(u"Copy")
    
    elif ev==key_codes.EKeyHash and inHand==0 and mode==0:
        inHand=-1
        gradient()
        draw(events)
        current=time.time()-viewday
        if current>0 and current<3600*24:
            hline=(time.time()-viewday)/60 + 30
        else:
            hline=(hstart*60+(hstop-hstart)*30)
        drawHLine("message")
        return 0
        
    elif ev == key_codes.EKeyUpArrow:
        if menu:
            menuUp()
        #Movement
        move(-30)

    elif ev == key_codes.EKeyDownArrow:
        if menu:
            menuDown()
        move(30)
        
    
    #SUPER SCROLL UP
    elif ev == key_codes.EKey2:
        move(-60)
        
    #SUPER SCROLL DOWN
    elif ev == key_codes.EKey0:
        move(60)
        
    #GENTLE SCROLL UP
    elif ev == key_codes.EKey5:
        move(-5)
        
    #GENTLE SCROLL DOWN
    elif ev == key_codes.EKey8:
        move(5)
        
    #Middle Button
    elif ev == key_codes.EKeySelect:
        if menu:
            menuMiddle()
        elif recording and inHand==3:
            try:
                snd.stop()
            except:
                pass
            snd.play()
            q=appuifw2.query(u"Is it ok?","query")
            if not q:
                try:
                    snd.stop()
                    snd.close()
                except:
                    pass
                try:
                    os.remove("C:\\idealist\\"+ voiceNote +".wav")
                except:
                    pass
                newVoiceNote()
            else:
                snd.stop()
                snd.close()
                appuifw2.note(u"Added succesfully")
                inHand = 0
                try:
                    soundList.extend([[viewday+hline*60,voiceNote]])
                except:
                    appuifw2.note(u"Can't add the voice note.")
                try:
                    for i in range(0,len(soundList)):
                        if soundList[i][0]<time.time():
                            del soundList[i]
                except:
                    pass
                soundList.sort()
                pickle.dump(soundList,open('C:\\idealist\\sounds.txt','w'))
                gradient()
                draw(events)
                drawRectangle(events)
                drawSms()
                drawSignal()
                handleRedraw(None)
                recording=0
        elif inHand==-1:
            newMessage()
        elif inHand==3:
            newVoiceNote()
        elif inHand==-2:
            if eventsEmpty==[]:
                appuifw2.note(u"There's nothing to choose from at this day")
                inHand=0
            else:
                checkAndAdd()
        elif inHand==2:
            newReminder()
            
        elif inHand==0:
            #Pretty much awesome function!
            if mode==0 and events[selected]!=[]:
                try:
                    del todo
                except:
                    pass
                theid=events[selected][-1]
                for i in range(1,len(base)):
                    if theid in base[i][0]:
                        todo=Todo(index=i)
                        return 0
                b=appuifw2.popup_menu([u"Connect with Todo",u"New Todo"],u"Choose")
                if len(base[0][1:])<1:
                    b=1
                if b==0:
                    args=[]
                    for i in base[0][1:]:
                        args+=[i.title]
                    c=appuifw2.popup_menu(args,u"")
                    if c!=None:
                        base[c+1][0].extend([theid])
                        saveBase()
                    todo=Todo(index=(c+1))
                    
                elif b==1:
                    todo=Todo(theid=theid)
                    saveBase()
                loadBase()
            elif mode==1:
                if anychange:
                    colisions = checkColisions()
                    if len(colisions)==1 and (eventCopy[2]*60+eventCopy[3]-eventCopy[0]*60-eventCopy[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
                        if eventCopy[-1]!=None:
                            events.extend([eventCopy])
                            overwrite(-1)
                        else:
                            idea2event(colisions[0],eventCopy)
                
                    elif len(colisions)==0:
                        #IN FUTURE MAKE IT POSIBLE TO ADD IT HERE AFTER A WARNING BY SPLITING UP OTHERS AND ADDING THEM TO Todo
                        appuifw2.note(u"You can't add it here!")
                        return 0
                    else:
                        if eventCopy[-1]!=None:
                            a=calendar.open()
                            a.__delitem__(eventCopy[-1])
                        
                        much=0
                        best=0
                        for i in colisions:
                            if (i[2]*60+i[3]-i[0]*60-i[1])>much:
                                best=i
                                much=i[2]*60+i[3]-i[0]*60-i[1]
                        idea2event(best,eventCopy)
                            
                    if otherday == viewday:
                        try:
                            if eventCopy[-1]!=None:
                                del events[selected]
                        except:
                            pass
                    anychange=0
                    prepare(viewday)
                    mode=0
                    gradient()
                    drawSignal()
                    draw(events)
                    drawRectangle(events)
                    handleRedraw(None)
                    return 0
                if otherday==viewday:
                    prepare(viewday)
                gradient()
                mode=2
                draw(events)
                drawOutline()
                handleRedraw(None)
            elif mode ==2:
                if anychange:
                    for i in savelist:
                        try:
                            overwrite(i)
                        except:
                            pass
                    anychange= not anychange
                    savelist=[]
                    prepare(viewday)
                    mode=0
                    gradient()
                    drawSignal()
                    draw(events)
                    drawRectangle(events)
                    handleRedraw(None)
                    return 0
                gradient()
                mode =3
                drawSignal()
                draw(events)
                drawAdjust()
                handleRedraw(None)
            elif mode==3:
                if anychange:
                    k=0
                    for i in savelist:
                        try:
                            overwrite(i)
                        except:
                            pass
                    anychange= not anychange
                    savelist=[]
                    prepare(viewday)
                    mode=0
                    gradient()
                    drawSignal()
                    draw(events)
                    drawRectangle(events)
                    handleRedraw(None)
                    return 0
                mode=0
                gradient()
                drawSignal()
                draw(events)
                drawRectangle(events)
                handleRedraw(None)
            else:
                try:
                    if events[selected]==[] and mode!=1:
                        appuifw2.note(u"Nothing to edit!")
                        return 0
                except:
                    pass
        elif inHand==1:
            newAnniversary()
            return 0
        
        
    #Left arrow handler
    elif ev == key_codes.EKeyLeftArrow:
        if menu:
            menuLeft()
        
        elif inHand==0:
            if mode==0:
                viewday-=3600*24
                weekday-=1
                weekday=weekday%7
                prepare(viewday)
                selected=0
                gradient()
                draw(events)
                drawSms()
                drawSignal()
                drawRectangle(events)
            
            elif mode==1:
                viewday-=3600*24
                weekday-=1
                weekday=weekday%7
                prepare(viewday)
                if events==[[]]:
                    events=[[]]
                elif otherday==viewday:
                    del events[selected]
                anychange = 1
                gradient()
                draw(events)
                drawSms()
                drawSignal()
                drawHalf()

            elif mode==2:
                selected-=1
                gradient()
                draw(events)
                drawSignal()
                drawOutline()
            
            elif mode==3:
                if start == 0:
                    selected -= 1
                gradient()
                start = not start
                draw(events)
                drawSignal()
                drawAdjust()

        elif inHand==2:
            viewday-=3600*24
            weekday-=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("reminder")
            drawSms()
            drawSignal()
        elif inHand==-1:
            viewday-=3600*24
            weekday-=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("message")
            drawSms()
            drawSignal()
        elif inHand==3:
            viewday-=3600*24
            weekday-=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("voice note")
            drawSms()
            drawSignal()
        
        elif inHand==-2:
            viewday-=3600*24
            weekday-=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            eventsSpace(events)
            draw(events)
            drawRectangle(eventsEmpty)
            drawSms()
            drawSignal()
        elif inHand==1:
            viewday-=3600*24
            weekday-=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawSms()
            drawSignal()

        
            
    #Right arrow handler
    elif ev == key_codes.EKeyRightArrow:
        if menu:
            menuRight()
        
        elif inHand==0:
            if mode==0:
                viewday+=3600*24
                weekday+=1
                weekday=weekday%7
                prepare(viewday)
                selected=0
                gradient()
                draw(events)
                drawSms()
                drawSignal()
                drawRectangle(events)
            
            elif mode==1:
                viewday+=3600*24
                weekday+=1
                weekday=weekday%7
                prepare(viewday)
                if events==[[]]:
                    events=[[]]
                elif otherday==viewday:
                    del events[selected]
                anychange = 1
                gradient()
                draw(events)
                drawSms()
                drawSignal()
                drawHalf()

            elif mode==2:
                selected+=1
                gradient()
                draw(events)
                drawSignal()
                drawOutline()
            
            elif mode==3:
                if start == 1:
                    selected += 1
                gradient()
                start = not start
                draw(events)
                drawSignal()
                drawAdjust()

        elif inHand==2:
            viewday+=3600*24
            weekday+=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("reminder")
            drawSms()
            drawSignal()
        
        elif inHand==-1:
            viewday+=3600*24
            weekday+=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("message")
            drawSms()
            drawSignal()
            
        elif inHand==-1:
            viewday+=3600*24
            weekday+=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawHLine("voice note")
            drawSms()
            drawSignal()
        
        elif inHand==-2:
            viewday+=3600*24
            weekday+=1
            weekday=weekday%7
            prepare(viewday)
            eventsSpace(events)
            gradient()
            draw(events)
            drawRectangle(eventsEmpty)
            drawSms()
            drawSignal()
        elif inHand==1:
            viewday+=3600*24
            weekday+=1
            weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(events)
            drawSms()
            drawSignal()    
   
    elif ev== key_codes.EKeyYes and inHand==0:
        quickEdit()

    #Deletes an event from the calendar
    elif ev == key_codes.EKeyBackspace and inHand==0 and mode==0:
        delEvent(selected)
        if events==[]:
            events=[[]]
            selected=0
        gradient()
        draw(events)
        drawRectangle(events)
    elif ev==key_codes.EKey4 and inHand==0 and mode==0:
        try:
            del todo
        except:
            pass
        todo = Todo()
    handleRedraw(None)

#Function preparing events db [From internal calendar -> inside the app]
def prepare(datetime):
    global events, annivs, remind, kalendarz
    try:
        c=kalendarz.daily_instances(datetime, appointments=1, events=0, anniversaries=0,todos=0)
    except:
        appuifw2.note(u"Error preparing events.")
    d=[]
    events=[]
    
    offset=(time.localtime()[3] - time.gmtime()[3])%24

    #idealistappuifw2.note(unicode(str(offset)))
    for i in c:
        if i.values()[1]<=datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=kalendarz.__getitem__(k)
        start=time.gmtime(z.start_time)
        end=time.gmtime(z.end_time)
        events.extend([[start[3]+offset,start[4],end[3]+offset,end[4],z.content,z.location,z.priority,z.id]])
    if events==[]:
        events=[[]]
    
    annivs=[]
    c=kalendarz.daily_instances(datetime-3600*24, appointments=0, events=0, anniversaries=1,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <= datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=kalendarz.__getitem__(k)
        annivs.extend([[z.content,z.id]])
        
    remind=[]
    c=kalendarz.daily_instances(datetime, appointments=0, events=1, anniversaries=0,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <= datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=kalendarz.__getitem__(k)
        start=time.gmtime(z.start_time)
        remind.extend([[start[3]+offset,start[4],z.content,z.id]])
    #del b
    return events


def forwatch():
    global wlist, currentday, wlist2, kalendarz, annivs1, annivs2
    try:
        kalendarz = calendar.open()
    except:
        appuifw2.note(u"Error re-opening calendar")
        
    wlist=[]
    wlist2=[]
    c=kalendarz.daily_instances(currentday, appointments=1, events=0, anniversaries=0,todos=0)
    c2=kalendarz.daily_instances(currentday+24*3600, appointments=1, events=0, anniversaries=0,todos=0)
    
    for k in c:
        z=kalendarz.__getitem__(k['id'])
        if k['datetime']+z.end_time-z.start_time>time.time():
            wlist.extend([[k['datetime'],k['datetime']+z.end_time-z.start_time,z.content,z.location,z.priority,z.id]])
    for k in c2:
        z=kalendarz.__getitem__(k['id'])
        wlist2.extend([[k['datetime'],k['datetime']+z.end_time-z.start_time,z.content,z.location,z.priority,z.id]])
        
    annivs1=[]
    c=kalendarz.daily_instances(currentday-24*3600, appointments=0, events=0, anniversaries=1,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <= currentday+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=kalendarz.__getitem__(k)
        annivs1.extend([[z.content,z.id]])
        
    annivs2=[]
    c=kalendarz.daily_instances(currentday, appointments=0, events=0, anniversaries=1,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <=currentday+48*3600:
            d.append(i.values()[0])
    for k in d:
        z=kalendarz.__getitem__(k)
        annivs2.extend([[z.content,z.id]])
        
forwatch()
canvas=None
img=None
w=0
h=0



def drawOnStandby():
    global screenObj
    current =""
    while(screenObj):
        e32.ao_sleep(0.04)
        e32.ao_yield()
        current=appswitch.application_list(1)[0]
        if (current=="Standby mode"):
            screenObj.show()
        else:
            #if screenObj.ifshown:
            screenObj.hide()

def watchout():
    #Timer function
    global events, wlist, img, currentday, smsList,w, h,missedcalls, inboxx,currentfont, unreadsms, phone, message, xprof, menu, mode, eventsEmpty, soundList, screenObj, timer
    e32.ao_yield()
    if currentday+24*3600<=time.time():
        currentday+=24*3600*math.floor((time.time()-currentday)/(24*3600))
        forwatch()
        #girlsStatus=girls.showStatus()
        
    elif currentday>=time.time():
        currentday+=24*3600*math.floor((time.time()-currentday)/(24*3600))
        forwatch()
        #girlsStatus=girls.showStatus()
    
    timex=int(time.time()/60)
    if smsList!=[]:
        try:
            if int(smsList[0][0]/60)==timex:
                if (smsList[0][1].find("@")==-1):
                    messaging.sms_send(smsList[0][1],smsList[0][2])
                else:
                    messaging.mms_send(smsList[0][1],smsList[0][2],attachment=None)
                del smsList[0]
                smsList.sort()
                pickle.dump(smsList,open('C:\\idealist\\smses.txt','w'))
            if int(smsList[0][0]/60)<timex:
                del smsList[0]
                smsList.sort()
                pickle.dump(smsList,open('C:\\idealist\\smses.txt','w'))
        except:
            pass
    if soundList!=[]:
        try:
            if int(soundList[0][0]/60)==timex:
                try:
                    snd=audio.Sound.open("C:\\idealist\\"+ soundList[0][1] +".wav")
                    snd.play()
                    appuifw2.note(u"Voice note!")
                    while (snd.state()==2):
                        e32.ao_sleep(1)
                    
                except:
                    appuifw2.note(u"A voice note couldn't been played!")
                del soundList[0]
            
            if int(soundList[0][0]/60)<timex:
                del soundList[0]
            
            soundList.sort()
            snd.close()
            pickle.dump(soundList,open('C:\\idealist\\sounds.txt','w'))
        except:
            pass
    
    #globalui.global_note(unicode(str(wlist[0])))
    if wlist!=[]:
        try:
            if int(wlist[0][1]/60)==timex and (int(wlist[0][4])%2==1):
                xprofile.set_ap(0)
                del wlist[0]
            if int(wlist[0][0]/60)==timex and (int(wlist[0][4])%2==1):
                xprofile.set_ap(1)
        except:
            print "I couldn't check if it's needed to turn profile."
    
    #This lines display a new message when it comes
    unreadsms=0
    try:
        if inboxx.unread(inboxx.sms_messages()[0])<>0:
            unreadsms=1
    except:
        pass
    #Displays missed calls
    try:
        l=logs.calls(mode='missed')  #The dictionary for the latest missed call
        missedcalls=0
        if len(l)>0 and l[0]["flags"]==0:
            missedcalls=1
        else:
            missedcalls=0
    except:
        print "problem with taking call log"
    

    try:
        del l
    except:
        pass
    gradient()
    draw(events)
    drawSms()
    drawSignal()
    #print "watchout " + unicode(e32db.format_time(viewday))
    #appuifw2.note(unicode(e32db.format_time(time.now())))
    if menu:
        mainMenu()
    elif mode==1:
        drawHalf()
    elif mode==2:
        drawOutline()
    elif mode==3:
        drawAdjust()
    elif inHand==1:
        pass
    elif inHand==2:
        drawHLine("reminder")
    elif inHand==-2:
        drawRectangle(eventsEmpty)
    elif inHand==-1:
        drawHLine("message")
    elif inHand==3:
        drawHLine("voice note")
    else:
        drawRectangle(events)
    #handleRedraw(None)
    
    timer.after(60, watchout)
    
def gradient():
    global img, h, w, currentday, newh
    z=(h-newh-endh)*1./50
    #anglehour=(2*math.pi*((time.time()-currentday)/3600)/24)
    #coshour=math.cos(anglehour)
    for i in range(0,50):
        img.rectangle((12,int(i*z+newh),w,int((i+1)*z+newh)), fill=(240-2*i,240-2*i,240-2*i))

def quit():
    
    global inHand, mode, viewday,anychange, running, events, img, selected, menu, inboxx, snd, recording, voiceNote

    if menu:
        menu=0
        gradient()
        draw(events)
        drawRectangle(events)
        drawSms()
        drawSignal()
        handleRedraw(None)
        return 0
    elif appuifw2.app.screen != 'full':
        saveBase()
        predraw()
        buildCanvas()
    elif inHand == 2 or inHand==-1 or inHand==-2 or inHand==1 or inHand==3:
        inHand =0
        if recording:
            try:
                snd.stop()
                snd.close()
                try:
                    os.remove("C:\\idealist\\"+ voiceNote +".wav")
                except:
                    pass
            except:
                pass
            recording=0
        appuifw2.note(u"Deleted.")
        prepare(viewday)
        forwatch()
        gradient()
        draw(events)
        drawRectangle(events)
        drawSms()
        drawSignal()
        handleRedraw(None)
        return 0
    elif (mode==1 or mode == 2 or mode==3):
        mode=0
        prepare(viewday)
        gradient()
        draw(events)
        drawRectangle(events)
        drawSms()
        drawSignal()
        handleRedraw(None)
        anychange=0
        return 0
    else:
        e=appuifw2.query(u"Exit Idealist?", 'query')
        if e:
            try:
                saveConfig()
            except:
                appuifw2.note(u"Error saving config file")
                
            appuifw2.app.menu_key_handler=None
            try:
                timer.cancel()
            except:
                appuifw2.note(u"Can't cancel timer")
            try:
                del inboxx
                #snd.close()
            except:
                appuifw2.note(u"Can't del inbox object")
            
            #idealistappuifw2.app.set_exit()
            try:
                #idealistenvy.is_app_system(0)
                if (appswitch.fg_appname()==u'IdeaList'):
                    appuifw2.app.set_exit()
                    app_lock.signal()
            except:
                appuifw2.note(u"Now you have to kill idealist ;]")



#THE DRAWING PART
vadjust=(h-newh-endh)/(hstop-hstart)
def vAdjustRefresh():
    global newh, h, hstop, hstart, vadjust, hline, dish, endh
    vadjust=(h-newh-endh)/(hstop-hstart)

def resizeCanvas(rect):
    global canvas, img, w,h, events
    if not canvas: return

    # Initialize drawing coordinate
    if img: del img
    img = graphics.Image.new(canvas.size, mode='RGB')
    w, h = canvas.size
    try:
        vAdjustRefresh()
        gradient()
        draw(events)
        drawSms()
        drawSignal()
    except:
        pass
    

def predraw():
    global w,h, img, canvas
    img = None
    canvas = appuifw2.Canvas(\
                  redraw_callback = handleRedraw,\
                  event_callback = handleEvent,
                  resize_callback= resizeCanvas)
    appuifw2.app.body = canvas
    appuifw2.app.title = u"IdeaList"
    appuifw2.app.screen = 'full'
        
predraw()

def changeFont():
    global currentfont, events
    fonty=appuifw2.available_fonts()
    del fonty[-1]
    a=appuifw2.popup_menu(fonty,u"Choose a font")
    if a!=None:
        currentfont=fonty[a]
        draw(events)
        drawRectangle(events)
        
def setHours():
    global hstart, hstop, dhstart, dhstop, events
    a=appuifw2.query(u"Wake-up hour","time",float(dhstart*3600))
    b=appuifw2.query(u"Go to sleep hour", "time", float(dhstop*3600))
    if a!=None and b!=None:
        hstart=dhstart=int(a/3600)
        hstop=dhstop=int(b/3600)
        vAdjustRefresh()
        gradient()
        draw(events)
        drawSms()

def website():
    e32.start_exe('BrowserNG.exe', ' "4 http://www.masteranza.wordpress.com/ 1"', 1)

def categoryConfig():
    global ideacat
    appuifw2.app.screen='normal'
    b=[]
    for i in ideacat:
        b.extend([unicode(i[0]+": "+str(i[1]))])
    a=appuifw2.selection_list(b)
    if a!=None:
        colors=[(200,70,70),(70,200,70),(70,70,200),(200,200,70),(70,200,200),(200,70,200),(70,70,70)]
        d = appuifw2.popup_menu([u"Red",u"Green",u"Blue",u"Yellow",u"Sea",u"Violet",u"Black"], u"Choose:")
        if d!=None:
            ideacat[a][1]=colors[d]
        categoryConfig()
    appuifw2.app.screen='full'
    
def mainMenu():
    global currentfont, w, h, menu, events
    gradient()
    draw(events)
    drawSms()
    drawSignal()
    img.polygon((40,h/2,w/2,h/2-w/2+40,w-40,h/2,w/2,h/2+w/2-40),fill=(0,0,0), outline=(200,200,200), width=4)
    img.rectangle((20+w/4,h/2-w/4+20,w-20-w/4,h/2+w/4-20),outline=(200,200,200), width=4)
    img.text((w/2-12,h/2+5),u"Edit",fill=(255,255,255), font=currentfont)
    img.text((w/2-10,h/2-w/4+10),u"New",fill=(255,255,255), font=currentfont)
    img.text((w/4-12,h/2+5),u"Sync",fill=(255,255,255), font=currentfont)
    img.text((w-12-w/4,h/2+5),u"Todo",fill=(255,255,255), font=currentfont)
    img.text((w/2-20,h/2+w/4-5),u"Settings",fill=(255,255,255), font=currentfont)
    menu=1
    handleRedraw(None)

def version():
    appuifw2.note(u"Idealist 1.5\nby Ranza's Research",'info')
    
def shortcuts():
    shortk=appuifw2.Text(text=u"Green Key - Quick Edit\nPencil Key - Enter Edit mode\n1 - Jump to date\n2 - New Event\n3 - New Idea\n4 - Opens IdeaList\n5 - New Reminder\n6 - Opens Todo\n\nHowever if you're in edit mode the keys:\n2 & 0 - move selection quickly [30 min]\n5 & 8 - move selection slowly [1 min]")
    #shortk=idealistappuifw2.Text(text=u"Green Key - Quick Edit\nPencil Key - Toggle Edit mode\n1 - Jump to date\n2 - Money spent input dialog\n3 - New Event\n4 - Opens Todo lists\n5 - Show money on account\n6 - New Reminder\n6 - Copy mode\n8- Money earned input dialog\n9- Add anniversary\birthday\n*- Add new voice note\n0- Add QUICK idea\birthday\n#- Add scheduled sms message\n\nHowever if you're in edit mode the keys:\n2 & 0 - move selection quickly [30 min]\n5 & 8 - move selection slowly [1 min]")
    appuifw2.app.screen='normal'
    appuifw2.app.body=shortk

def buildCanvas():
    global w,h, img, canvas, selected
    appuifw2.app.screen = 'full'
    appuifw2.app.menu_key_handler = mainMenu
    appuifw2.app.menu = None
    appuifw2.app.exit_key_handler = quit
    w, h = canvas.size
    img = graphics.Image.new((canvas.size[0], canvas.size[1]), mode='RGB')
    try:
        gradient()
        selected=0
        draw(events)
        drawSms()
        drawSignal()
        drawRectangle(events)
        #watchout()
        handleRedraw(None)
    except:
        pass



events=[[]]
events=prepare(viewday)
buildCanvas()



    
def draw(list):
    global vadjust, newh, currentask, viewday, ideacat, hstart, hstop, annivs, w, h, currentday, logo, present, smsList, inHand, currentfont, weekday, days
    if events!=[[]]:
        for i in range(0,len(list)):
            #The height in pixels of an event
            hsize=int((list[i][2]+(list[i][3]*1./60)-list[i][0]-(list[i][1]*1./60))*vadjust)/2
            #a rectangle height
            difk=int(hsize/12)
            #how many blocks
            if difk==0:
                difk=1
            split=int(hsize/difk)+2
            if split==0:
                split=2
            #color jump
            cjump=int(70/split)
            #the start position
            cc=(list[i][0]+(list[i][1]*1./60)-hstart)*vadjust
            try:
                clor=ideacat[int(list[i][5])][1]
            except:
                clor=(70,70,70)
            for j in range(0,split):
                clor=tuple(map(lambda x: x-cjump,clor))
                img.rectangle((12,int(cc+difk*j+newh),w+100,int(cc+difk*(j+1)+newh)),fill=clor)
            if split==0:
                split=1
            img.rectangle((12,int(cc+hsize+difk+newh),w,int(cc+2*(hsize)+newh)), fill=clor)
            img.line((12,cc+newh,w,cc+newh), outline=(30,30,30), width=1)
            img.line((12,cc+newh+2*(hsize),w,cc+newh+2*(hsize)), outline=(30,30,30),width=1)
            #img.line((12,int(cc+split*difk+newh),w,int(cc+split*difk+newh)), outline=(100,100,100), width=1)
            category=list[i][5]
            
            try:
                category=ideacat[int(category)][0]
            except:
                category=str(list[i][5])
            #When the text should be displayed
            linecount=int((list[i][2]+list[i][3]*1./60-list[i][1]*1/60.-list[i][0])*vadjust/dish)
            zzz=1
            if linecount>=2:
                zzz=0
            long_str=unicode(list[i][4] +" | " + category)
            lines = wrap_text_to_array(long_str, currentfont, w-41-zzz*29)
            addy=0
            time0=str(list[i][0])
            time1=str(list[i][1])
            time2=str(list[i][2])
            time3=str(list[i][3])
            if len(time0)==1:
                time0="0"+time0
            if len(time1)==1:
                time1="0"+time1
            if len(time2)==1:
                time2="0"+time2
            if len(time3)==1:
                time3="0"+time3
            if linecount!=0:
                textpos=int((list[i][2]+list[i][3]*1./60-list[i][1]*1/60.-list[i][0])*vadjust-(len(lines)*dish))/2
                if len(lines)>linecount:
                    textpos=1
                if linecount>=2:
                    img.text((w-26,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(240,230,230))
                    img.text((w-26,cc+10+dish+newh+addy),unicode(time2 +":" + time3), font=currentfont , fill=(240,230,230))
                else:
                    img.text((w-58,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(240,230,230))
                for line in lines:
                    if linecount==0:
                        break
                    img.text((13,cc+10+textpos+newh+addy), line, font=currentfont,fill = (240,240,240))
                    addy+= dish
                    linecount-=1
            else:
                try:
                    if int((list[i+1][0]+list[i+1][1]*1./60-list[i][3]*1/60.-list[i][2])*vadjust/dish)>0:
                        img.text((13,cc+10+newh), lines[0], font=currentfont,fill = (10,10,10))
                        img.text((15,cc+12+newh), lines[0], font=currentfont,fill = (10,10,10))
                        img.text((14,cc+11+newh), lines[0], font=currentfont,fill = (240,240,240))
                        
                        img.text((w-58,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(10,10,10))
                        img.text((w-58,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(240,230,230))
                except:
                    img.text((13,cc+10+newh), lines[0], font=currentfont,fill = (10,10,10))
                    img.text((15,cc+12+newh), lines[0], font=currentfont,fill = (10,10,10))
                    img.text((14,cc+11+newh), lines[0], font=currentfont,fill = (240,240,240))
                    img.text((w-58,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(10,10,10))
                    img.text((w-58,cc+10+newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=currentfont , fill=(240,230,230))
    #current hour line
    img.line((11,newh+((time.time()-viewday)/3600-hstart)*vadjust,w,newh+((time.time()-viewday)/3600-hstart)*vadjust), (250,50,0),width=2)
    if inHand==1:
        img.rectangle((12,h-endh-endh,170,h-endh),fill=(0,0,0))
        img.text((11,h-endh-1),u"Choose day by pressing select",fill=(255,255,255))    
    
        
def drawSms():
    global smsList, remind, soundList, sound, message, bell, viewday, hstart, hstop, vadjust, newh
    #draws the hours line
    img.rectangle((0,1,12,h),fill=(0,0,0))
    for i in range(0,hstop-hstart+1):
        img.line((8,newh+i*vadjust,12,newh+i*vadjust),(250,250,250), width = 1)
        img.text((0,newh+i*vadjust), unicode(i+hstart),(200,200,200))
    #Draws reminders icons
    if len(remind) > 0:
        for y in remind:
            img.line((10,(int(y[0])+(int(y[1])*1./60)-hstart)*vadjust+newh,13,(int(y[0])+(int(y[1])*1./60)-hstart)*vadjust+newh),outline = (250,250,250), width = 2)
            img.blit(bell, target=(0,(int(y[0])+(int(y[1])*1./60)-hstart)*vadjust+newh))
    #Draws Sms icons
    if len(smsList) > 0:
        for y in smsList:
            if (y[0]-viewday)>0 and (y[0]-viewday)<3600*24:
                img.line((10,((y[0]-viewday)/3600-hstart)*vadjust+newh,16,((y[0]-viewday)/3600-hstart)*vadjust+newh),outline = (250,250,100), width = 2)
                img.blit(message, target=(0,((y[0]-viewday)/3600-hstart)*vadjust+newh))
    #Draws voice note icons
    if len(soundList) > 0:
        for y in soundList:
            if (y[0]-viewday)>0 and (y[0]-viewday)<3600*24:
                img.line((10,((y[0]-viewday)/3600-hstart)*vadjust+newh,16,((y[0]-viewday)/3600-hstart)*vadjust+newh),outline = (250,250,100), width = 2)
                img.blit(sound, target=(0,((y[0]-viewday)/3600-hstart)*vadjust+newh))

def drawSignal():
    global img
    #Signal and battery lines, changing every minute
    img.rectangle((0,h-endh,w,h),fill=(0,0,0))
    global unreadsms, missedcalls, phone, sms, currentfont, silence, xprof, viewday, currentday
    img.line((0,0,w,0), outline=(0,0,0), width=1)
    try:
        img.line((w,0,int(w-w*1./2*sysinfo.battery()/100),0),outline=(int(255*(1-float(sysinfo.battery()/100))),int(255.*sysinfo.battery()/100),0),width=1)
        img.line((0,0,int(w*1./2*sysinfo.signal()/7),0),outline=(int(255*(1-float(sysinfo.signal()/7))),int(255.*(sysinfo.signal())/7),0),width=1)
    except:
        pass
        
    all=u""
    img.rectangle((12,1,w,newh),fill=(0,0,0))
    if len(annivs) > 0:
        poss=0
        hehe=0
        for y in annivs:
            img.blit(present, target=(2+hehe,h-endh))
            hehe+=14
            img.text((2+hehe,h), unicode(y[0]), fill = (255,255,255))
            hehe+=len(unicode(y[0]))*6
    watched=int(currentday/(3600*24))
    hourr=str(int(((time.time()-currentday)/3600)))
    minutess=str(int(((time.time()-currentday)%3600)/60))
    hourr=int(hourr)%24
    hourr=str(hourr)
    if len(hourr)==1:
        hourr="0"+hourr
    minutess=int(minutess)%60
    minutess=str(minutess)
    if len(minutess)==1:
        minutess="0"+minutess
    img.text((w-30,h-2), unicode(hourr+":"+minutess), font=currentfont ,fill=(245,245,245))
    
    if missedcalls==1:
        img.blit(phone, target=(w-57,h-endh))
    if unreadsms==1:
        img.blit(sms, target=(w-72,h-endh))
    if xprof:
        img.blit(silence, target=(w-42,h-endh))
    
    all=u" " + unicode(days[weekday])
    if int(-(currentday-viewday)/(3600*24))==0:
        all+=u" (Today)"
    elif int(viewday-3600*24)/(3600*24)==watched:
        all+=u" (Tomorrow)"
    elif int(viewday-7200*24)/(3600*24)==watched:
        all+=u" (After Tomorow)"
    elif int(viewday+3600*24)/(3600*24)==watched:
        all+=u" (Yesterday)"
    elif (watched-int(viewday/(3600*24)))%7==0:
        all+=u" (" + str(-(watched-int(viewday/(3600*24)))/7) + " week)"
    img.text((12,12), unicode(e32db.format_time(viewday)[:10])+all,font=currentfont, fill = (255,255,255))
    img.blit(logo, target=(w-14,0))
    handleRedraw(None)
    
def drawRectangle(list):
    global selected, newh, vadjust, mode, ideacat, inHand, dish, currentfont,logo, currentfont,w
    if (selected < 0):
        selected=len(list)-1
    elif (selected > int(len(list)-1)):
        selected=0
        
    if list!=[[]]:
        try:
            difk=(list[selected][2]+(list[selected][3]*1./60)-list[selected][0]-(list[selected][1]*1./60))*vadjust
        except:
            return 0
        category=list[selected][5]
        try:
            category=ideacat[int(category)][0]
        except:
            category=list[selected][5]
        linecount=int((difk)/dish)
        
        time0=str(list[selected][0])
        time1=str(list[selected][1])
        time2=str(list[selected][2])
        time3=str(list[selected][3])
        if len(time0)==1:
            time0="0"+time0
        if len(time1)==1:
            time1="0"+time1
        if len(time2)==1:
            time2="0"+time2
        if len(time3)==1:
            time3="0"+time3
        
        long_str=unicode(time0 +":" + time1+ "-" + time2 +":" + time3+ " "+ list[selected][4] +" | " + category)
        lines = wrap_text_to_array(long_str, currentfont, w-10)
        if linecount<len(lines):
            difk=(dish+2)*len(lines)
        difk2=difk
        split=2*int(difk/6)
        if split!=0:
            difk=float(difk/split)
        cc=(list[selected][0]+(list[selected][1]*1./60)-hstart)*vadjust
        
        for j in range(0,split/2):
            img.rectangle((13,int(cc+difk*j+newh),w,int(cc+difk*(j+1)+newh)), fill=(255-(j)*(80/split),
                                                                                    255-(j)*(80/split),
                                                                                    255-(j)*(80/split)))
        if split==0:
            split=1
        
        img.rectangle((13,int(cc+difk*split/2+newh),w-1,int(cc+difk*(split)+newh+1)), fill=(220,220,220))
        img.line((12,cc+newh,w,cc+newh), outline=(10,10,10), width=1)
        img.line((12,int(cc+split*difk+newh),w,int(cc+split*difk+newh)), outline=(230,230,230), width=1)
        
        #Draw lines
        img.rectangle((w-4,cc+newh,w,int(cc+difk*(split)+newh+1)),fill=(0,0,0))
        img.rectangle((w-8,cc+newh,w-4,int(cc+difk*(split)+newh+1)),fill=(50,50,50))
        img.rectangle((12,cc+newh,16,int(cc+difk*(split)+newh+1)),fill=(0,0,0))
        img.rectangle((16,cc+newh,20,int(cc+difk*(split)+newh+1)),fill=(50,50,50))
        #When the text should be displayed
        addy=0
        textpos=int(difk2-(len(lines)*dish))/2
        for line in lines:
            img.text((21,cc+10+textpos+newh+addy), line, font=currentfont,fill = (240,240,240))
            img.text((22,cc+11+textpos+newh+addy), line, font=currentfont,fill = (0,0,0))
            addy+= dish
            linecount-=1

    
def drawAdjust():
    global events, selected, start,h,w
    if (selected < 0):
        selected=len(events)-1
    elif (selected > int(len(events)-1)):
        selected=0
    drawSignal()
    img.rectangle((12,h-20,100,h-10),fill=(0,0,0))
    img.text((12,h-10),u"Resize mode on",fill=(255,255,255))
    
    cW=(w-12)/5
    if start:
        for i in range(5):
            img.line((12+cW*i,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ,12+cW*i+cW/2,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ), outline = (230,230,230), width = 2)
            img.line((12+cW*i+cW/2,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ,12+(2*cW*i),(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ), outline = (20,20,20), width = 2)
    else:
        for i in range(5):
            img.line((12+cW*i,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh  ,12+cW*i+cW/2,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh ), outline = (230,230,230), width = 2)
            img.line((12+cW*i+cW/2,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh  ,12+(2*cW*i),(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh ), outline = (20,20,20), width = 2)
    
    
def drawHalf(text=u"Move"):
    global eventCopy, colors, ideacat, hstart, hstop, vadjust, newh,w,h, selected, events
    drawSignal()
    img.rectangle((12,h-20,90,h-10),fill=(0,0,0))
    img.text((12,h-10),text+u" mode on",fill=(255,255,255))
    colisions= checkColisions()
    if len(colisions)==0:
        color=colors[12]
    elif len(colisions)==1 and (eventCopy[2]*60+eventCopy[3]-eventCopy[0]*60-eventCopy[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
        color=colors[13]
    else:
        color=colors[14]
        
    category=eventCopy[5]
    try:
        category=ideacat[int(category)][0]
    except:
        category=eventCopy[5]
    
    #difk=(eventCopy[2]+(eventCopy[3]*1./60)-eventCopy[0]+(eventCopy[1]*1./60))*vadjust
    
    cc=(eventCopy[0]+(eventCopy[1]*1./60)-hstart)*vadjust
    
    #split=difk/3.0 #wsp dobrany eksperymentalnie
    #difk=int(difk/split)
    #split=int(split)
    #else:
    #    split=2
    #try: 
    #    for j in range(0,split-1):
    #        img.rectangle((w/2,int(cc+difk*j+newh),w,int(cc+difk*(j+1)+newh)), fill=tuple([x+((j+1)*(80/split)) for x in color]))
    #except:
    #    idealistappuifw2.note(u"error")
    img.rectangle((w/2,cc+newh,w,(eventCopy[2]+(eventCopy[3]*1./60)-hstart)*vadjust+newh), fill=color)
    img.text((w/2 + 2,cc+10+newh), unicode(str(eventCopy[0]) +":" + str(eventCopy[1])+ "-" + str(eventCopy[2]) +":" + str(eventCopy[3])+ " "+ eventCopy[4] +"| " + category), fill = colors[4])
    
def drawOutline():
    global events, selected,w,h
    if (selected < 0):
        selected=len(events)-1
    elif (selected > int(len(events)-1)):
        selected=0
    drawSignal()
    img.rectangle((12,h-20,140,h-10),fill=(0,0,0))
    img.text((12,h-10),u"Change order mode on",fill=(255,255,255))
    #drawRectangle(events)
    img.line((12,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh,w,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh), outline = (0,0,0), width = 2)
    img.line((12+20,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh,w-20,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh), outline = (240,240,240), width = 2)
    
    img.line((12,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh,w,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh), outline = (0,0,0), width = 2)
    img.line((12+20,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh,w-20,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh), outline = (240,240,240), width = 2)
    
def drawHLine(string):
    global events, selected, hline
    drawSignal()
    img.rectangle((12,h-endh-endh,110,h-endh),fill=(0,0,0))
    img.text((12,h-endh-1),u"Adding " + unicode(string) ,fill=(255,255,255))
    img.line((12,(hline-hstart*60)*vadjust/60+newh ,w,(hline-hstart*60)*vadjust/60+newh), outline = colors[8], width = 2)
    img.rectangle((w-26,(hline-hstart*60)*vadjust/60+newh-12,w,(hline-hstart*60)*vadjust/60+newh),fill=(5,5,5))
    img.text((w-26,(hline-hstart*60)*vadjust/60+newh), unicode(str(int(hline/60))+":"+str(int(hline%60))), fill=colors[8])

def update():
    # define a url where the picture you want to download is located on the net
    url = "http://idealist.googlecode.com/svn/public/update.sis"
    # define the file name and the location of the downloaded file for local storage e.g. on the c drive
    tempfile = "c:\\idealist\\update.sis"

    apid = socket.select_access_point()
    if not apid:
        appuifw2.note(u"Could't find any access point.","error")
    apo = socket.access_point(apid)
    apo.start()
    urllib.urlretrieve(url, tempfile)
    apo.stop()
    appuifw2.note(u"Succesfuly downloaded! Proceed the instalation process", "info")
    envy.set_app_system(0)
    e32.start_exe(tempfile,'',1)
    #e32.ao_sleep(1)
    #quit()
    



#gradient()
#draw(events)
#drawSms()
#drawSignal()
#drawRectangle(events)
watchout()
drawOnStandby()

handleRedraw(None)
app_lock.wait()
