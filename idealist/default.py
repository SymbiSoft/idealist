import appuifw2

import e32, key_codes, graphics, time, calendar, miso, e32db, contacts, globalui, messaging, math, sysinfo, xprofile, logs, inbox, sysinfo, urllib

from e32db import format_time
from akntextutils import wrap_text_to_array

import cerealizer as pickle

xprof=0

polish={"yes":u"Tak","no":u"Nie","months":[u"Styczeń",u"Luty",u"Marzec",u"Kwiecień",u"Maj",u"Czerwiec",u"Lipiec",u"Sierpień",u"Wrzesień",u"Październik",u"Listopad",u"Grudzień"],"days":[u"Poniedziałek",u"Wtorek",u"Środa",u"Czwartek",u"Piątek",u"Sobota",u"Niedziela"]}
english={"yes":u"Yes","no":u"No","months":[u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December"],"days":[u"Monday",u"Tuesday",u"Wednesday",u"Thursday",u"Friday",u"Saturday",u"Sunday"]}

#Importing all images needed for the application
logo = graphics.Image.open('C:\\idealist\\logo.png')
present = graphics.Image.open('C:\\idealist\\present.png')
bell = graphics.Image.open('C:\\idealist\\bell.png')
message = graphics.Image.open('C:\\idealist\\message.png')
phone = graphics.Image.open('C:\\idealist\\phone.png')
sms = graphics.Image.open('C:\\idealist\\sms.png')
silence = graphics.Image.open('C:\\idealist\\silence.png')
messageinfo=u""
remindinfo=u""
annivsinfo=u""
#Lists of data
days=[u"Monday",u"Tuesday",u"Wednesday",u"Thursday",u"Friday",u"Saturday",u"Sunday"]
months=[u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December"]
#Initializing time
tempek=list(time.localtime())
tempek[3]=tempek[4]=tempek[5]=0
tempek=tuple(tempek)
viewday=time.mktime(tempek)
currentday=float(viewday)
weekday=time.localtime().tm_wday
#All the variables used in app
annivs=[]
remind=[]
#variables which specify if the Ideas menu should be visible
selected=0
start = 0
#The beginning of the day
dhstart=hstart=7
dhstop=hstop=23
newh=14
endh=10
m=0
currentfont='dense'
missedcalls=0
unreadsms=0
atext=""
#0-select mode (multiple), 1-move mode (multiple), 2-adjust mode (single)
smslist=[]
projects=[]
mode=0
exploremode=1
whichnew=3
zoom=0
ideacat=[[u'Temp',(220,220,220)],[u'School',(200,200,70)],[u'Work',(200,200,70)],[u'Science',(220,70,200)],[u'Physical Exercise',(100,70,100)],[u'Meeting',(70,100,100)],[u'Relax',(100,70,70)],[u'Meal',(80,80,80)],[u'Cleanings',(90,90,90)]]
cati=len(ideacat)
path='C:\\idealist\\ideas.txt'
#Initialize the reading ideas from file
ideas=[]
anychange=0
#Define if alarms should be enabled
alarm = 1
#A variable for mode=2 event
eventl=0
otherday=0
savelist=[]
hline=0
c1=0
dish=11
#It's 1 if menu is opened
menu=0


inboxx=inbox.Inbox()
def saveconfig():
    global ideacat, dhstart, dhstop, hstart, hstop, currentfont, alarm
    tosave=[ideacat,dhstart,dhstop,currentfont, alarm]
    try:
        pickle.dump(tosave,open('C:\\idealist\\config.txt','w'))
    except:
        pass
        #appuifw2.note(u"Can't save the config file")
    
def loadconfig():
    global ideacat, dhstart, dhstop, hstart, hstop, currentfont, alarm
    try:
        toload=pickle.load(open('C:\\idealist\\config.txt'))
        ideacat=toload[0]
        dhstart=hstart=toload[1]
        dhstop=hstop=toload[2]
        currentfont=toload[3]
        alarm = toload[4]
    except:
        #appuifw2.note(u"[First run warnings]")
        #appuifw2.note(u"Can't load the config file")
        pass
        
loadconfig()
try:
    ideas=pickle.load(open('C:\\idealist\\ideas.txt'))
except:
    #appuifw2.note("Can't load the ideas db")
    pass
try:
    smslist=pickle.load(open('C:\\idealist\\smses.txt'))
except:
    #appuifw2.note("Can't load the planned sms db")
    pass

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

colors =[(0,200,220),(0,220,240), (0,0,0), (0,0,0),(255,255,255),(200,200,200),(0,0,0),(0,0,0),(255,255,255),(100,100,100),(220,220,220),(240,240,240),(255,0,0), (0,150,0), (150, 90, 0), (0,0,150)]

ideabox=[]
def loadbase():
    global base
    try:
        cyk=pickle.load(open('C:\\idealist\\ideabox.txt'))
        base=[]
        for i in range(0,len(cyk)):
            base+=[[]]
            for j in range(0,len(cyk[i])):
                if j==0:
                    base[i]+=[cyk[i][j]]
                else:
                    base[i]+=[[]]
                    base[i][j]=appuifw2.Item(cyk[i][j][0])
                    base[i][j].marked=cyk[i][j][1]
    except:
        #appuifw2.note(u"Cannot load IdeaBox file!")
        base=[[[]]]
        pass
    
loadbase()

def savebase():
    global base
    tosave=[]
    for i in range(0,len(base)):
        tosave += [[]]
        for j in range(0,len(base[i])):
            if j==0:
                tosave[i]+=[base[i][j]]
            else:
                try:
                    tosave[i]+=[[base[i][j].title,base[i][j].marked]]
                except:
                    tosave[i]+=[[base[i][j].title,False]]
    try:
        pickle.dump(tosave,open('C:\\idealist\\ideabox.txt','w'))
    except:
        appuifw2.note(u"Cannot save the Ideabox file")
    

class Ideabox:
    global base
    
    inside=0
    def __init__(self,index=0,theid=0):
        loadbase()
        self.prepare(index)
        if theid!=0:
            self.newbox(theid)
    def left(self):
        if self.inside:
            self.inside=0
            self.prepare()
    def select(self):
        if base[self.inside]!=[]:
            if self.inside:
                #Kurwa, I wasn't that pissed off since they change Family Guy aerial time
                base[self.inside][self.nana.current()+1].marked=not base[self.inside][self.nana.current()+1].marked
            else:
                self.inside=self.nana.current()+1
                self.prepare(self.inside)
    def newbox(self,id=0):
        if self.inside:
            a=appuifw2.query(u"Element name:", 'text', u"")
            if a!=u"" and a!=None:
                b=appuifw2.Item(a)
                b.marked=False
                base[self.inside].extend([b])
                self.prepare(self.inside)
        else:
            a=appuifw2.query(u"Box name:", 'text', u"")
            if a!=u"" and a!=None:
                b=appuifw2.Item(a)
                b.marked=False
                base[0].extend([b])
                if id!=0:
                    base.extend([[[id]]])
                else:
                    base.extend([[[]]])
                self.inside=-1
                self.prepare(self.inside)

    def delbox(self):
        if base[self.inside]!=[]:
            if self.inside:
                del base[self.inside][self.nana.current()+1]
            else:
                del base[self.nana.current()+1]
                del base[0][self.nana.current()+1]
            self.prepare(self.inside)
    
    def edit(self):
        if base[self.inside]!=[]:
            if self.inside:
                a=appuifw2.query(u"Edit","text",base[self.inside][self.nana.current()+1].title)
                if a!=None and a!="":
                    z=appuifw2.Item(a)
                    z.marked=base[self.inside][self.nana.current()+1].marked
                    base[self.inside][self.nana.current()+1]=z
                else:
                    return 0
            else:
                a=appuifw2.query(u"Edit","text",base[0][self.nana.current()+1].title)
                if a!=None and a!="":
                    z=appuifw2.Item(a)
                    base[0][self.nana.current()+1] = z
                else:
                    return 0
            self.prepare(self.inside)

    def prepare(self,selec=0):
        try:
            curr=self.nana.current()
            del self.nana
        except:
            curr=None
        
        if selec==0:
            mark=False
            appuifw2.app.navi_text=u'Boxes'
            texxt=u"box"
        else:
            appuifw2.app.navi_text=base[0][selec].title
            mark=True
            texxt=u"element"
        self.nana=appuifw2.Listbox2(base[selec][1:], markable=mark)
        self.nana.set_empty_list_text=u"Empty list"
        appuifw2.app.body=self.nana
        appuifw2.app.screen='normal'
        if curr!=None:
            self.nana.set_current=curr
        self.nana.bind(key_codes.EKeyBackspace,self.delbox)
        self.nana.bind(key_codes.EKeySelect,self.select)
        self.nana.bind(key_codes.EKeyLeftArrow,self.left)
        self.nana.bind(key_codes.EKeyRightArrow,self.select)
        self.nana.bind(key_codes.EKeyYes,self.edit)
        appuifw2.app.menu_key_text=u"Add " + texxt
        appuifw2.app.menu_key_handler=self.newbox
        self.inside=selec
        appuifw2.app.menu=[]
        #appuifw2.app.menu=[(u"Add to box", self.add2box),(u"Remove from box", self.rembox),(u"Box", ((u"Add box", self.newbox),(u"Edit box name", self.edit),(u"Remove box", self.editbox)))]

def putit():
    global ideacat, ideas, cati, exploremode, c1, dlist
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
        draw(input)
        draw_sms()
        difflist(input)
        if dlist==[]:
            appuifw2.note(u"It's a past day, can't insert it here")
        exploremode=2
    if c2==1:
        difflist(input)
        for i in dlist:
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
        
def buildrepeat(start, edit=0):
    global days, months
    posibles=['daily','weekly','monthly_by_days','monthly_by_dates','yearly_by_date','yearly_by_day']
    a=appuifw2.popup_menu([u'daily',u'weekly',u'monthly by days',u'monthly by days',u'yearly by date',u'yearly by day'], u"Repeat it")
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

def make_event(idea,space, ok=0):
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
            c.priority=3
            c.alarm=viewday+int(space[0])*3600+int(space[1])*60
        else:
            c.priority=2
    else:
        c.priority=3
        c.alarm=viewday+int(space[0])*3600+int(space[1])*60
    c.commit()
    forwatch()
    prepare(viewday)
    gradient()
    draw(input)
    draw_sms()
    return c.id
    
def check_add():
    global dlist, selected,exploremode, input, viewday, mode, c1
    timeleft=(dlist[selected][-1]-ideas[c1][1]/60)
    if ideas[c1][1] == 0:
        if int(dlist[selected][0]*60+dlist[selected][1]-dlist[selected][2]*60-dlist[selected][3]>60):
            dlist[selected][2]=dlist[selected][0]+1
            dlist[selected][3]=dlist[selected][1]
        eventid = make_event(ideas[c1],dlist[selected])
        notyes=appuifw2.query( u"The idea has no required time. Put it also back to IdeaList?","query")
        if not notyes:
            del ideas[c1]
            pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        prepare(viewday)
        draw(input)
        appuifw2.note(u"Event added. Adjust its duration")
        exploremode=1
        mode=3
        #okresl ktory powinien byc zaznaczony
        sme=0
        for i in input:
            if i[-1]==eventid:
                selected=sme
                break
            sme+=1
        draw_adjust()
    elif ideas[c1][1] >= 0 and timeleft>=0:
        make_event(ideas[c1],dlist[selected],1)
        exploremode=1
        del ideas[c1]
        pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        prepare(viewday)
        draw(input)
    else:
        notyes=appuifw2.query( u"The idea requires more time. Put the rest back to IdeaList?","query")
        make_event(ideas[c1],dlist[selected])
        if not notyes:
            del ideas[c1]
            pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
            exploremode=1
            return 0
        ideas[c1][1]=int(ideas[c1][1]+timeleft)
        pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        exploremode=1
        
#Function which prepares names of ideas for a selectable list
def ideasnames():
    global ideas, ideacat, cati
    rlist=[]
    
    for i in ideas:
        category=i[4]
        if int(category)==cati or cati==len(ideacat):
                
            try:
                category=ideacat[int(category)][0]
            except:
                category=i[4]
            if i[1]==0:
                rlist.extend([(category,i[3])])
            else:
                rlist.extend([(category+unicode(": "+str(int(i[1]/60))+" min"),i[3])])
    if rlist==[]:
        rlist=[(u"Empty",u"Empty list")]
    return rlist

def event2idea(eventk, much=0):
    global ideas
    newone=[]
    newone.extend([0])
    newone.extend([eventk[2]*3600+eventk[3]*60-eventk[0]*3600-eventk[1]*60-much*60])
    newone.extend([2])
    newone.extend([eventk[4]])
    newone.extend([eventk[5]])
    ideas += [newone]
    pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
    
def saveundone(undone):
    global ideas
    newone=[]
    newone.extend([0])
    newone.extend([int(undone[1]-undone[0])])
    newone.extend([2])
    newone.extend([undone[2]])
    newone.extend([undone[3]])
    ideas += [newone]
    pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))

def newidea():
    global ideacat, ideas, cati
    if cati==len(ideacat):
        which=0
    else:
        which=cati
    a=[]
    for i in ideacat:
        a.extend([i[0]])
    data=[(u'Idea','text',u""),(u'Category','combo', (a,which)),(u'Duration','time',0.)]
    #flags = appuifw2.FFormEditModeOnly
    f=appuifw2.Form(data)
    f.execute()
    if f[0][2]!=u"":
        newone=[]
        #[0 extra data, 1 timeneeded, 2 priority, 3 name, 4 category]
        newone.extend([0])
        
        newone.extend([f[2][2]])
        newone.extend([0])
        newone.extend([f[0][2]])
        newone.extend([int(f[1][2][1])])
        ideas += [newone]
        pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        ideas=pickle.load(open('C:\\idealist\\ideas.txt'))
        appuifw2.app.body.set_list(ideasnames(), -1)
        
def editidea():
    global ideacat, ideas, cati
    which2=appuifw2.app.body.current()
    if cati==len(ideacat):
        which=appuifw2.app.body.current()
    else:
        which=-1
        for i in ideas:
            if int(i[4])==int(cati):
                which2-=1
            which+=1
            if which2==-1:
                break
        if which2!=-1:
            return 0
            
    b=appuifw2.popup_menu([u"Name",u"Category",u"Time needed",u"Expire date"], u"Edit " + ideas[which][3])
    if b==0:
        if ideas[which][3]==None:
            ideas[which][3]=0
        a=appuifw2.query(u'Nazwa','text', ideas[appuifw2.app.body.current()][3])
        if a!=ideas[which][3] and a!=None:
            ideas[which][3]=a
    elif b==1:
        if ideas[which][4]==None:
            ideas[which][4]=0
        z=[]
        for i in ideacat:
            z.extend([i[0]])
        a=appuifw2.popup_menu(z, u"Change category")
        if a!=ideas[which][4] and a!=None:
            ideas[which][4]=a
    elif b==2:
        if ideas[which][1]==None:
            ideas[which][1]=0.
        a=appuifw2.query(u'Change duration','time',ideas[which][1])
        if a!=ideas[which][1] and a!=None:
            ideas[which][1]=float(a)
    elif b==3:
        if ideas[which][0]==None:
            ideas[which][0]=0.
        a=appuifw2.query(u'Change expire date','date',ideas[which][0])
        if a!=ideas[which][0] and a!=None:
            ideas[which][0]=float(a)
    if b!=None:
        pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        ideas=pickle.load(open('C:\\idealist\\ideas.txt'))
        appuifw2.app.body.set_list(ideasnames(), which)
    

def delevent():
    global selected, input
    b=calendar.open()
    b.__delitem__(input[selected][-1])
    del input[selected]
    gradient()
    draw(input)
    


def editevent():
    global selected, input, viewday
    a=[]
    for i in ideacat:
        a.extend([i[0]])

    data=[(u'Idea','text',input[selected][4]),(u'Category','combo', (a,int(input[selected][5]))),(u'Silent','combo', ([u"No",u"Yes"],int(input[selected][6]%2))),(u'Event start','time',float(input[selected][0]*3600+input[selected][1]*60)),(u'Event end','time',float(input[selected][2]*3600+input[selected][3]*60)),(u'Event date','date',viewday)]
    flags = appuifw2.FFormEditModeOnly
    f=appuifw2.Form(data,flags)
    f.execute()
    input[selected][4]=f[0][2]
    input[selected][5]=f[1][2][1]
    input[selected][0]=int((f[3][2])/3600)
    input[selected][1]=int((f[3][2])%3600/60)
    input[selected][2]=int((f[4][2])/3600)
    input[selected][3]=int((f[4][2])%3600/60)
    input[selected][6]=int(f[2][2][1])
    if f[5][2] != viewday:
        event=input[selected]
        viewday=f[5][2]
        prepare(viewday)
        if input==[[]]:
            input=[]
        input.extend([event])
        overwrite(-1)
        forwatch()
        input.sort()
        draw(input)
        draw_rectangle(input)
        return 0
    
    overwrite(selected)
    forwatch()
    draw(input)
    draw_rectangle(input)

def newevent():
    global ideacat, ideas, input, exploremode, c1, eventl, hstop, hstart, mode, dlist, selected
    appuifw2.app.screen='normal'
    a=[]
    for i in ideacat:
        a.extend([i[0]])
    data=[(u'Name','text',u""),(u'Category','combo', (a,0)),(u'Duration','time',0.)]
    flags = appuifw2.FFormEditModeOnly
    f=appuifw2.Form(data,flags)
    f.execute()
    if f[0][2]!=u"":
        newone=[]
        #[0 expires, 1 timeneeded, 2 priority, 3 name, 4 category]
        newone.extend([0])
        newone.extend([f[2][2]])
        newone.extend([0])
        newone.extend([f[0][2]])
        newone.extend([int(f[1][2][1])])
        ideas += [newone]
        c1=-1
        pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
        appuifw2.app.screen='full'
        difflist(input)
        selected=0
        exploremode=2
        draw(input)
        draw_rectangle(dlist)
    else:
        appuifw2.app.screen='full'
def newbirthday():
    pass

def newreminder():
    global exploremode, input, viewday, hline, remindinfo
    a=appuifw2.query(u"Reminder name:",'text',remindinfo)
    if a!='' and a!=None:
        c=calendar.open()
        b=c.add_event()
        b.content=unicode(a)
        b.set_time(viewday+hline*60)
        b.alarm=viewday+hline*60
        b.commit()
        appuifw2.note(u"New reminder succesfuly added")
        prepare(viewday)
        exploremode = 1
        draw(input)
        draw_rectangle(input)
    else:
        exploremode=1
        appuifw2.note(u"Adding canceled")
    draw_sms()
    remindinfo=u""


def newmessage():
    global exploremode, input, viewday, hline, smslist, messageinfo, atext
    message=appuifw2.query(u"Message text:", 'text', messageinfo)
    
    if message != None and message!= u"":
        showpeople=[]
        db = contacts.open()
        allo=[]
        for i in db.keys():
            showpeople+=[db.__getitem__(i).title]
            allo+=[i]
        appuifw2.app.screen='normal'
        b=appuifw2.selection_list(showpeople,1)
        if b!=None:
            c=db.__getitem__(allo[b])
            d=c.find(type='mobile_number')
            try:
                d=d[0].value
                smslist.extend([[viewday+hline*60,d,message,allo[b]]])
                exploremode = 1
                for i in range(0,len(smslist)):
                    if smslist[i][0]<time.time():
                        del smslist[i]
                smslist.sort()
                pickle.dump(smslist,open('C:\\idealist\\smses.txt','w'))
            except:
                appuifw2.note(u"The contact doesn't contain a mobile phone number!")
        appuifw2.app.screen='full'
        predraw()
        buildcanvas('Landscape')
        draw_sms()
        handle_redraw(None)
    messageinfo=u""



def newaniv(str=0):
    global viewday, input, exploremode, annivsinfo
    if str==0:
        c=appuifw2.query(u"Anniversary of...?", 'text',annivsinfo)
    else:
        c=str
    if c != "":
        a=calendar.open()
        b=a.add_anniversary()
        b.content=unicode(c)
        b.set_time(viewday+24*3600)
        b.alarm=viewday+hstart*3600
        b.commit()
        appuifw2.note(u"New anniversary succesfuly added")
        prepare(viewday)
        exploremode = 1
        draw(input)
        draw_rectangle(input)
        return 0
    exploremode=1
    appuifw2.note(u"Adding canceled")
        
def delidea():
    global ideacat, ideas, cati
    which2=appuifw2.app.body.current()
    if cati==len(ideacat):
        which=appuifw2.app.body.current()
    else:
        which=-1
        for i in ideas:
            if int(i[4])==int(cati):
                which2-=1
            which+=1
            if which2==-1:
                break
        if which2!=-1:
            return 0
    del ideas[which]
    pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
    appuifw2.app.body.set_list(ideasnames(),which-1)

def overwrite(michal=-2):
    global input, selected, start, viewday
    changed=0
    if michal==-2:
        michal=selected
        changed=1
    b=calendar.open()    
    c=b.__getitem__(input[michal][-1])
    c.begin()
    alarminfo=c.alarm
    if c.get_repeat()!=None:
        choices = [u"This only", u"Future", u"All"]
        index = appuifw2.popup_menu(choices, u"Save "+input[michal][4])
        if index==0:
            #Make the old event end at the start day of the new one
            zz=c.get_repeat()
            zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
            c.set_repeat(zz)
            c.commit()
            #Make a new shit
            d=b.add_appointment()
            d.content=input[michal][4]
            d.location=input[michal][5]
            d.priority=input[michal][6]
            d.set_time(viewday+input[michal][0]*3600+input[michal][1]*60,viewday+input[michal][2]*3600+input[michal][3]*60)
            if alarminfo!=None:
                d.alarm=viewday+input[michal][0]*3600+input[michal][1]*60
            else:
                d.alarm=None
            d.commit()
            forwatch()
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
                b.__delitem__(input[michal][-1])
            c.commit()
            #Make a new shit
            c=b.add_appointment()
            c.content=input[michal][4]
            c.location=input[michal][5]
            c.priority=input[michal][6]
            c.set_time(viewday+input[michal][0]*3600+input[michal][1]*60,viewday+input[michal][2]*3600+input[michal][3]*60)
            if alarminfo!=None:
                c.alarm=viewday+input[michal][0]*3600+input[michal][1]*60
            else:
                c.alarm=None
            zzz['start']=viewday
            c.set_repeat(zzz)
            c.commit()
            forwatch()
        elif index==2:
            #Make the old event end at the start day of the new one
            c.content=input[michal][4]
            c.location=input[michal][5]
            c.priority=input[michal][6]
            c.set_time(viewday+input[michal][0]*3600+input[michal][1]*60,viewday+input[michal][2]*3600+input[michal][3]*60)
            if alarminfo!=None:
                c.alarm=viewday+input[michal][0]*3600+input[michal][1]*60
            else:
                c.alarm=None
            c.commit()
            forwatch()
    else:
        c.content=input[michal][4]
        c.location=input[michal][5]
        c.priority=input[michal][6]
        c.set_time(viewday+input[michal][0]*3600+input[michal][1]*60,viewday+input[michal][2]*3600+input[michal][3]*60)
        if alarminfo!=None:
            c.alarm=viewday+input[michal][0]*3600+input[michal][1]*60
        else:
            c.alarm=None
        c.commit()
        forwatch()
def delevent(sel):
    global input
    #DELETE EVENT INTELI GENTLY
    b=calendar.open()
    c=b.__getitem__(input[sel][-1])
    zz=c.get_repeat()
    if zz!=None:
        choices=[u"Remove this only", u"Remove this & future", u"Remove all"]
        index = appuifw2.popup_menu(choices, u""+ input[sel][4])
        notyes1=appuifw2.query( u"Put it also back to IdeaList?","query")
        if notyes1:
            event2idea(input[sel])
        if index==2:
            b.__delitem__(input[sel][-1])
            del input[sel]
        elif index==1:
            c.begin()
            zz['end']=viewday-2*(24*3600)
            c.set_repeat(zz)
            c.commit()
            del input[sel]
        elif index==0:
            b=calendar.open()
            c.begin()
            zz=c.get_repeat()
            zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
            c.set_repeat(zz)
            c.commit()
            del input[sel]
    else:
        yesno=appuifw2.query(u"Do you want to remove event "+ input[sel][4],"query")
        if yesno:
            notyes1=appuifw2.query( u"Put it also back to IdeaList?","query")
            if notyes1:
                event2idea(input[sel])
            b.__delitem__(input[sel][-1])
            del input[sel]
            #END DELETE EVENT INTELIGENTLY


def move_hline(time):
    global hline, hstart, hstop
    if hline+time<hstart*60:
        hline=hstart*60
    elif hline+time>hstop*60:
        hline=hstop*60
    else:
        hline+=time

def adjust(sel, start, time):
    global hstart, hstop, selected, input, anychange, mode, savelist
    anychange=1
    if selected not in savelist:
        savelist+=[selected]
    if start:
        if (time > 0):
            if (hstop*60<=input[sel][2]*60+input[sel][3]+time):
                time=hstop*60-input[sel][2]*60-input[sel][3]
            if sel==len(input)-1:
                if input[sel][3]+time>=60:
                    input[sel][2]+=1
                    input[sel][3]=input[sel][3]+time-60
                    return 0
                input[sel][3]+=time
                return 0
            elif (input[sel + 1][0]*60+input[sel+1][1]-input[sel][2]*60-input[sel][3]<time):
                #Co jesli nastepne zdarzenie stanie sie zbyt krotkie?
                if selected+1 not in savelist:
                    savelist+=[(selected+1)]
                if (input[sel+1][2]*60+input[sel+1][3]-input[sel+1][0]*60-input[sel+1][1]<=time):
                    delevent(sel+1)
                    return 0
                if input[sel+1][1]+time>=60:
                    input[sel+1][0]+=1
                    input[sel+1][1]=input[sel+1][1]+time-60
                    input[sel][2]=input[sel+1][0]
                    input[sel][3]=input[sel+1][1]
                else:
                    input[sel+1][1]+=time
                    input[sel][2]=input[sel+1][0]
                    input[sel][3]=input[sel+1][1]
                return 0
            if input[sel][3]+time>=60:
                input[sel][2]+=1
                input[sel][3]=input[sel][3]+time-60
                return 0
        #input[sel][2]+=time
        elif (time < 0):
            if ((input[sel][2]*60+input[sel][3]-input[sel][0]*60-input[sel][1])<=-time):
                delevent(sel)
                if input==[]:
                    input=[[]]
                    selection=0
                    mode=0
                    draw_rectangle(selection)
                return 0
            elif input[sel][3]+time<0:
                input[sel][3]=60+time+input[sel][3]
                input[sel][2]-=1
                return 0
        input[sel][3]+=time
    elif (not start):
        if (time < 0):
            if (hstart*60>=input[sel][0]*60+input[sel][1]+time):
                time=hstart*60-input[sel][0]*60-input[sel][1]
            if sel==0:
                if (input[sel][1]+time<0):
                    input[sel][0]-=1
                    input[sel][1]=60+time+input[sel][1]
                    return 0
                input[sel][1]+=time
                return 0
            
            if (input[sel][0]*60+input[sel][1]-input[sel-1][2]*60-input[sel-1][3]<-time):
                if (selected-1) not in savelist:
                    savelist+=[(selected-1)]
                if (input[sel-1][2]*60+input[sel-1][3]-input[sel-1][0]*60-input[sel-1][1]<=-time):
                    delevent(sel-1)
                    selected-=1
                    draw(input)
                    draw_adjust()
                    return 0
                elif input[sel-1][3]+time<0:
                    input[sel-1][2]-=1
                    input[sel-1][3]=60+time+input[sel-1][3]
                    input[sel][0]=input[sel-1][2]
                    input[sel][1]=input[sel-1][3]
                    return 0
                input[sel-1][3]+=time
                input[sel][0]=input[sel-1][2]
                input[sel][1]=input[sel-1][3]
                return 0
            else:
                if input[sel][1]+time<0:
                    input[sel][0]-=1
                    input[sel][1]=60+time+input[sel][1]
                    return 0
        elif (time>0):
            if (input[sel][2]*60+input[sel][3]-input[sel][0]*60-input[sel][1]-time<=0):
                delevent(sel)
                if input==[]:
                    input=[[]]
                    selection=0
                    mode=0
                    draw_rectangle(selection)
                return 0
            elif input[sel][1]+time>=60:
                input[sel][1]=input[sel][1]+time-60
                input[sel][0]+=1
                return 0
        input[sel][1]+=time
def move(sel, time):
    global input, selected, hstop, hstart, anychange, savelist
    anychange=1
    if sel not in savelist:
        savelist+=[sel]
    if (time>0):
        if sel==len(input)-1:
            if (hstop*60<=input[sel][2]*60+input[sel][3]+time):
                time=hstop*60-input[sel][2]*60-input[sel][3]
            if input[sel][1]+time>=60:
                input[sel][1]=input[sel][1]+time-60
                input[sel][0]+=1
                if input[sel][3]+time>=60:
                    input[sel][3]=input[sel][3]+time-60
                    input[sel][2]+=1
                    return 0
                input[sel][3]+=time
                return 0
            if input[sel][3]+time>=60:
                input[sel][3]=input[sel][3]+time-60
                input[sel][2]+=1
                input[sel][1]+=time
                return 0
            input[sel][1]+=time
            input[sel][3]+=time
            return 0
        elif (input[sel+1][0]*60+input[sel+1][1]-input[sel][2]*60-input[sel][3]<time):
            if sel+1 not in savelist:
                savelist+=[sel+1]
            copysel = list(input[sel])
            copysel1= list(input[sel+1])
            input[sel]=list(input[sel+1])
            input[sel+1]=list(copysel)
            #setting hour for the missed event
            input[sel][0]=input[sel+1][0]
            input[sel][1]=input[sel+1][1]
            input[sel][2]=copysel1[2]-copysel1[0]+input[sel+1][0]
            input[sel][3]=copysel1[3]-copysel1[1]+input[sel+1][1]
            if input[sel][3]>60:
                input[sel][2]+=1
                input[sel][3]= input[sel][3] % 60
            input[sel+1][0]=input[sel][2]
            input[sel+1][1]=input[sel][3]
            input[sel+1][2]=copysel[2]-copysel[0]+input[sel+1][0]
            input[sel+1][3]=copysel[3]-copysel[1]+input[sel+1][1]
            if input[sel+1][3]>60:
                input[sel+1][2]+=1
                input[sel+1][3]= input[sel+1][3] % 60
            selected+=1
        else:
            if input[sel][1]+time>=60:
                input[sel][1]=input[sel][1]+time-60
                input[sel][0]+=1
                if input[sel][3]+time>=60:
                    input[sel][3]=input[sel][3]+time-60
                    input[sel][2]+=1
                    return 0
                input[sel][3]+=time
                return 0
            if input[sel][3]+time>=60:
                input[sel][3]=input[sel][3]+time-60
                input[sel][2]+=1
                input[sel][1]+=time
                return 0
            input[sel][1]+=time
            input[sel][3]+=time
            return 0
    if (time<0):
        if sel==0:
            if (hstart*60>=input[sel][0]*60+input[sel][1]+time):
                time=hstart*60-input[sel][0]*60-input[sel][1]
            if input[sel][1]+time<0:
                input[sel][1]=60+time+input[sel][1]
                input[sel][0]-=1
                if input[sel][3]+time<0:
                    input[sel][3]=60+time+input[sel][3]
                    input[sel][2]-=1
                    return 0
                input[sel][3]+=time
                return 0
            if input[sel][3]+time<0:
                input[sel][3]=60+time+input[sel][3]
                input[sel][2]-=1
                input[sel][1]+=time
                return 0
            input[sel][1]+=time
            input[sel][3]+=time
            return 0
        elif (input[sel][0]*60+input[sel][1]-input[sel-1][2]*60-input[sel-1][3]<-time):
            if sel-1 not in savelist:
                savelist+=[sel-1]
            copysel = list(input[sel])
            copysel1= list(input[sel-1])
            input[sel]=list(input[sel-1])
            input[sel-1]=list(copysel)
            input[sel-1][0]=copysel1[0]
            input[sel-1][1]=copysel1[1]
            input[sel-1][2]=copysel[2]-copysel[0]+input[sel-1][0]
            input[sel-1][3]=copysel[3]-copysel[1]+input[sel-1][1]
            if input[sel-1][3]<0:
                input[sel-1][2]-=1
                input[sel-1][3]= input[sel-1][3] % 60
            #setting hour for the missed event
            input[sel][0]=input[sel-1][2]
            input[sel][1]=input[sel-1][3]
            input[sel][2]=copysel1[2]-copysel1[0]+input[sel][0]
            input[sel][3]=copysel1[3]-copysel1[1]+input[sel][1]
            if input[sel][3]<0:
                input[sel][2]-=1
                input[sel][3]= input[sel][3] % 60
            selected-=1
        else:
            if input[sel][1]+time<=0:
                input[sel][1]=60+time+input[sel][1]
                input[sel][0]-=1
                if input[sel][3]+time<0:
                    input[sel][3]=60+time+input[sel][3]
                    input[sel][2]-=1
                    return 0
                input[sel][3]+=time
                return 0
            if input[sel][3]+time<0:
                input[sel][3]=60+time+input[sel][3]
                input[sel][2]-=1
                input[sel][1]+=time
                return 0
            input[sel][1]+=time
            input[sel][3]+=time
            return 0

def move2(time):
    global eventl, hstart, hstop, anychange, viewday
    anychange = 1
    if time>0:
        if (hstop*60<=eventl[2]*60+eventl[3]+time):
            time=hstop*60-eventl[2]*60-eventl[3]
        if eventl[1]+time>=60:
            if eventl[3]+time>=60:
                eventl[1]=eventl[1]+time-60
                eventl[3]=eventl[3]+time-60
                eventl[0]+=1
                eventl[2]+=1
                return 0
            eventl[0]+=1
            eventl[1]=eventl[1]+time-60
            eventl[3]+=time
            return 0
        elif eventl[3]+time>=60:
            eventl[2]+=1
            eventl[3]=eventl[3]+time-60
            eventl[1]+=time
            return 0
        eventl[1]+=time
        eventl[3]+=time
    elif time<0:
        if (hstart*60>=eventl[0]*60+eventl[1]+time):
            time=hstart*60-eventl[0]*60-eventl[1]
        elif eventl[1]+time<0:
            if eventl[3]+time<0:
                eventl[1]=60+time+eventl[1]
                eventl[3]=60+time+eventl[3]
                eventl[0]-=1
                eventl[2]-=1
                return 0
            eventl[3]+=time
            eventl[1]=60+time+eventl[1]
            eventl[0]-=1
            return 0
        elif eventl[3]+time<0:
            eventl[3]=60+time+eventl[3]
            eventl[1]+=time
            eventl[2]-=1
            return 0
        eventl[1]+=time
        eventl[3]+=time

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
            c.priority=3
            c.alarm=vviewday+int(i[0])*3600+int(i[1])*60
        else:
            c.priority=2
    else:
        c.priority=3
        c.alarm=viewday+int(i[0])*3600+int(i[1])*60
    c.commit()
    forwatch()
    return c.id
    



def checkcolisions():
    global eventl, input
    freespace=[]
    var=[eventl[0],eventl[1]]
    begining=eventl[0]*60 + eventl[1]
    end=eventl[2]*60 + eventl[3]
    if input==[[]]:
        freespace=[[hstart,0,hstop,0]]
        return freespace
    for i in input:
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
        freespace.extend([[var[0],var[1],eventl[2],eventl[3]]])
    return freespace
        
def handle_redraw(rect):
    if img: canvas.blit(img)

def quick_edit():
    global selected, whichnew, ideas,exploremode, viewday, input, mode, start, colors, anychange, ideacat, dhstop, dhstart, zoom, hstart, hstop, eventl, otherday, savelist, hline, cati, m, dlist, remind, smslist, messageinfo, remindinfo, annivs, annivsinfo, base, ideabox, missedcalls, unreadsms,weekday, menu, alarm
    b=calendar.open()
    alarminfo=None
    try:
        d=b.__getitem__(input[selected][-1])
        d.begin()
        alarminfo=d.alarm
    except:
        appuifw2.note(u"Error building menu")
    if alarminfo==None:
        label=u"Turn Alarm ON"
    else:
        label=u"Turn Alarm OFF"
    
    b=appuifw2.popup_menu([u"Name",u"Category",u"Repeat rules",u"Color",label,u"More"], u"Edit " + input[selected][4])
    if b==0:
        c=appuifw2.query(u"Name", 'text',unicode(input[selected][4]))
        if c != input[selected][4] and c!=None:
            input[selected][4]=c
            b=calendar.open()
            d=b.__getitem__(input[selected][-1])
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
                    d.content=input[selected][4]
                    d.location=input[selected][5]
                    d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    d.priority=input[selected][6]
                    if alarminfo!=None:
                        d.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        d.alarm=None
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
                    d.content=input[selected][4]
                    d.location=input[selected][5]
                    d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    d.priority=input[selected][6]
                    if alarminfo!=None:
                        d.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        d.alarm=None
                    zzz['start']=viewday
                    d.set_repeat(zzz)
                    d.commit()
                elif index==2:
                    #Make the old event end at the start day of the new one
                    d.content=input[selected][4]
                    d.commit()
            d.content=input[selected][4]
            d.commit()
            draw(input)
            draw_rectangle(input)
    elif b==1:
        a=[]
        for i in ideacat:
            a.extend([i[0]])
        d=appuifw2.popup_menu(a, input[selected][4] + u" category")
        if d!= input[selected][5] and d!=None:
            input[selected][5]=d
            b=calendar.open()
            d=b.__getitem__(input[selected][-1])
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
                    d.content=input[selected][4]
                    d.location=input[selected][5]
                    d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    d.priority=input[selected][6]
                    if alarminfo!=None:
                        d.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        d.alarm=None
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
                    d.content=input[selected][4]
                    d.location=input[selected][5]
                    d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    d.priority=input[selected][6]
                    if alarminfo!=None:
                        d.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        d.alarm=None
                    zzz['start']=viewday
                    d.set_repeat(zzz)
                    d.commit()
                elif index==2:
                    #Make the old event end at the start day of the new one
                    
                    d.location=input[selected][5]
                    d.commit()
            d.location=input[selected][5]
            d.commit()
            draw(input)
            draw_rectangle(input)
    elif b==2:
        builded=buildrepeat(viewday+input[selected][0]*3600+input[selected][1]*60, 1)
        if builded != None:
            b=calendar.open()
            c=b.__getitem__(input[selected][-1])
            if c.get_repeat()!=None:
                choices = [u"Future", u"All",u"This only"]
                index = appuifw2.popup_menu(choices, u"Save on:")
                if index==0:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=input[selected][6]
                    if alarminfo!=None:
                        c.alarm=c.start_time
                    else:
                        c.alarm=None
                    zz=c.get_repeat()
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['end']=viewday-2*(24*3600)
                    c.set_repeat(zz)
                    c.commit()
                    #Make a new shit
                    c=b.add_appointment()
                    c.content=input[selected][4]
                    c.location=input[selected][5]
                    c.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    
                    c.priority=input[selected][6]
                    if alarminfo!=None:
                        c.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        c.alarm=None
                    c.set_repeat(builded)
                    c.commit()
                    return 0
                elif index==1:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=input[selected][6]
                    if alarminfo!=None:
                        c.alarm=c.start_time
                    else:
                        c.alarm=None
                    c.set_repeat(builded)
                    c.commit()
                    return 0
                elif index==2:
                    #Make the old event end at the start day of the new one
                    c.begin()
                    c.set_time(c.start_time,c.end_time)
                    c.priority=input[selected][6]
                    if alarminfo!=None:
                        c.alarm=c.start_time
                    else:
                        c.alarm=None
                    zz=c.get_repeat()
                    #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                    zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                    c.set_repeat(zz)
                    c.commit()
                    #Make a new shit
                    c=b.add_appointment()
                    c.content=input[selected][4]
                    c.location=input[selected][5]
                    c.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                    c.priority=input[selected][6]
                    if alarminfo!=None:
                        c.alarm=viewday+input[selected][0]*3600+input[selected][1]*60
                    else:
                        c.alarm=None
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
                ideacat[int(input[selected][5])][1]=acolors[d]
            except:
                appuifw2.note(u"Can't change color. Event doesn't belong to any category!")
    elif b==4:
        if alarminfo == None:
            alarminfo=viewday+input[selected][0]*3600+input[selected][1]*60
        else:
            alarminfo=None
            
        b=calendar.open()
        d=b.__getitem__(input[selected][-1])
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
                d.content=input[selected][4]
                d.location=input[selected][5]
                d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                d.priority=input[selected][6]
                d.alarm=alarminfo
                d.commit()
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
                d.content=input[selected][4]
                d.location=input[selected][5]
                d.set_time(viewday+input[selected][0]*3600+input[selected][1]*60,viewday+input[selected][2]*3600+input[selected][3]*60)
                d.priority=input[selected][6]
                d.alarm=alarminfo
                zzz['start']=viewday
                d.set_repeat(zzz)
                d.commit()
                return 0
            elif index==2:
                #Make the old event end at the start day of the new one
                d.priority=input[selected][6]
                d.alarm=alarminfo
                d.commit()
                draw(input)
                draw_rectangle(input)
                return 0
        d.alarm=alarminfo
        d.commit()
        draw(input)
        draw_rectangle(input)
    elif b==5:
        editevent()

    
#This thing handles buttons which are being clicked
def handle_event(event):
    global selected, whichnew, ideas,exploremode, viewday, input, mode, start, colors, anychange, ideacat, dhstop, dhstart, zoom, hstart, hstop, eventl, otherday, savelist, hline, cati, m, dlist, remind, smslist, messageinfo, remindinfo, annivs, annivsinfo, base, ideabox, missedcalls, unreadsms,weekday, menu, alarm
    ev = event['keycode']
    pi = event['scancode']
#This part in part used to be a redraw triggerer in past - not needed anymore
#    if event['type'] == appuifw2.EEventKeyDown: 
#        gradient()
#        draw(input)
    if pi == key_codes.EScancodeEdit:
        if exploremode==1:
            if mode==0:
                try:
                    if input[selected]==[]:
                        appuifw2.note(u"Nothing to edit!")
                        return 0
                except:
                    pass
                gradient()
                mode=1
                eventl=list(input[selected])
                del input[selected]
                otherday=viewday
                draw(input)
                draw_half()
    elif ev == key_codes.EKey3:
        if exploremode==1 and mode==0:
            a=appuifw2.query(u"Idea description:", 'text', "")
            if ""!=a and a!=None:
                z=[]
                for i in ideacat:
                    z.extend([i[0]])
                b=appuifw2.popup_menu(z,u"Choose category")
                if b!=None:
                    #[0 expires, 1 timeneeded, 2 priority, 3 name, 4 category]
                    newone=[]
                    newone.extend([0.])
                    newone.extend([0.])
                    newone.extend([0])
                    newone.extend([a])
                    newone.extend([b])
                    ideas += [newone]
                    pickle.dump(ideas,open('C:\\idealist\\ideas.txt','w'))
                    ideas=pickle.load(open('C:\\idealist\\ideas.txt'))
                    
    elif ev== key_codes.EKey4:
        appuifw2.app.screen='normal'
        nana=appuifw2.Listbox(ideasnames(),putit)
        nana.bind(key_codes.EKeyBackspace,delidea)
        nana.bind(key_codes.EKeyYes,editidea)
        nana.bind(key_codes.EKeyLeftArrow,cleft)
        nana.bind(key_codes.EKeyRightArrow,cright)
        appuifw2.app.body=nana
        appuifw2.app.menu_key_text=u"Add Idea"
        appuifw2.app.left_navi_arrow=True
        appuifw2.app.right_navi_arrow=True
        if cati==len(ideacat):
            appuifw2.app.navi_text=u'All categories'
        else:
            appuifw2.app.navi_text=ideacat[cati][0]
        appuifw2.app.menu=[]
        appuifw2.app.menu_key_handler=newidea
        return 0
    
    elif ev==key_codes.EKey6:
        try:
            del ideabox
        except:
            pass
        ideabox = Ideabox()
    
    elif ev == key_codes.EKey1 and mode!=3:
        if mode==0 or mode==1 or exploremode==0 or exploremode==2 or exploremode==-1:
            a=appuifw2.query(u"Go to:", 'date', viewday)
            if viewday!=a and a!=None:
                if zoom>0:
                    zoom=0
                    hstart=dhstart
                    hstop=dhstop
                weekday+=int((a-viewday)/86400)
                weekday=weekday%7
                viewday=a
                prepare(viewday)
                gradient()
                draw(input)
                draw_sms()
                if exploremode==2:
                    difflist(input)
                elif mode==1:
                    anychange = 1
                    draw_half()
                elif exploremode==-1:
                    draw_hline()
                elif mode==0:
                    draw_rectangle(input)
                
    
    elif ev == key_codes.EKeyUpArrow:
        if menu:
            menu=0
            choices = [u"Custom Event", u"Reminder", u"Anniversary", u"Message"]
            gradient()
            draw(input)
            draw_rectangle(input)
            draw_sms()
            draw_signal()
            handle_redraw(None)
            index = appuifw2.popup_menu(choices, u"Select:") 
            if index == 0 : 
                newevent()
            elif index == 1 :
                appuifw2.note(u"Choose time for the reminder")
                selected=0
                
                exploremode=-1
                if viewday<=time.time() and time.time()<=viewday+3600*24:
                    hline=(time.time()-viewday)/60+30
                else:
                    hline=((hstop-hstart)/2+hstart)*60
                draw(input)
                draw_hline()
                draw_sms()
                handle_redraw(None)
            elif index == 2: 
                appuifw2.note(u"Choose a day for which the anniversary should be added")
                selected=0
                draw(input)
                exploremode=0
            elif index == 3:
                selected=0
                exploremode=-1
                m=1
                if viewday<=time.time() and time.time()<=viewday+3600*24:
                    hline=(time.time()-viewday)/60+30
                else:
                    hline=((hstop-hstart)/2+hstart)*60
                draw(input)
                draw_hline()
                handle_redraw(None)
            return 0
        if exploremode==-1 and mode==0:
            move_hline(-5)
            gradient()
            draw(input)
            draw_hline()
        elif mode == 0:
            gradient()
            if selected!=0:
                selected-=1
                draw(input)
            else:
                draw(input)
                selected-=1
            if exploremode==2:
                draw_rectangle(dlist)
            else:
                draw_rectangle(input)
        elif exploremode==0:
            selected=0
            return 0
        elif mode==1:
            gradient()
            move2(-5)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, -5)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, - 5)
            draw(input)
            draw_adjust()
        if zoom>0:
            #middle=(1.0*int(input[selected][0])/60+int(input[selected][1])-1.0*int(input[selected][2])/60+int(input[selected][3]))
            dif=(hstop-hstart)/2

            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)

    elif ev == key_codes.EKeyDownArrow:
        if menu:
            if alarm:
                label=u"Turn Auto add alarm OFF"
            else:
                label=u"Turn Auto add alarm ON"
            menu=0
            menua=[u"Wake-sleep hours", u"Categories colors", u"Font", label, u"App info", u"Update",u"Exit"]
            gradient()
            draw(input)
            draw_rectangle(input)
            draw_sms()
            draw_signal()
            handle_redraw(None)
            cc=appuifw2.popup_menu(menua,u"")
            if cc==0:
                hourset()
            elif cc==1:
                catconfig()
            elif cc==2:
                changefont()
            elif cc==3:
                alarm = not alarm
            elif cc==4:
                menub=[u"Authors blog",u"Shortcut keys",u"Version info"]
                cd=appuifw2.popup_menu(menub,u"Info")
                if cd==0:
                    website()
                elif cd==1:
                    shortcuts()
                elif cd==2:
                    version()
            elif cc==5:
                update()
            elif cc==6:
                quit()
            return 0
        if exploremode==-1 and mode==0:
            move_hline(5)
            gradient()
            draw(input)
            draw_hline()
        elif mode == 0:
            gradient()
            if selected!=(len(input)-1):
                selected+=1
                draw(input)
            else:
                draw(input)
                selected+=1
            if exploremode==2:
                draw_rectangle(dlist)
            else:
                draw_rectangle(input)
        elif exploremode==0:
            selected=0
            return 0
        elif mode==1:
            gradient()
            move2(5)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, +5)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, +5)
            draw(input)
            draw_adjust()
        if zoom>0:
            dif=(hstop-hstart)/2
            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
    
    
    #SUPER SCROLL UP
    elif ev == key_codes.EKey2:
        if exploremode==0:
            return 0
        elif exploremode==-1 and mode==0:
            move_hline(-30)
            gradient()
            draw(input)
            draw_hline()
        elif mode == 0:
            if exploremode==1:
                newevent()
        elif mode==1:
            gradient()
            move2(-30)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, -30)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, -30)
            draw(input)
            draw_adjust()
        if zoom>0:
            dif=(hstop-hstart)/2
            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
    #SUPER SCROLL DOWN
    elif ev == key_codes.EKey0:
        if exploremode==0:
            return 0
        elif exploremode==-1 and mode==0:
            move_hline(30)
            gradient()
            draw(input)
            draw_hline()
        elif mode == 0:
            return 0
        elif mode==1:
            gradient()
            move2(30)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, 30)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, 30)
            draw(input)
            draw_adjust()
        if zoom>0:
            dif=(hstop-hstart)/2
            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
            
    #GENTLE SCROLL UP
    elif ev == key_codes.EKey5:
        if exploremode==0:
            return 0
        elif exploremode==-1 and mode==0:
            move_hline(-1)
            gradient()
            draw(input)
            draw_hline()
        elif mode == 0:
            exploremode=-1
            selected=0
            appuifw2.note(u"Creates new reminder")
            hline=(hstop-hstart)*30+hstart*60
            m=0
            draw_hline()
        elif mode==1:
            gradient()
            move2(-1)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, -1)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, -1)
            draw(input)
            draw_adjust()
        if zoom>0:
            dif=(hstop-hstart)/2
            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
    
    #GENTLE SCROLL DOWN
    elif ev == key_codes.EKey8:
        if exploremode==0:
            return 0
        elif exploremode==-1 and mode==0:
            move_hline(1)
            gradient()
            draw(input)
            draw_hline()
            
        elif mode == 0:
            return 0
        elif mode==1:
            gradient()
            move2(1)
            draw(input)
            draw_half()
        elif mode==2:
            gradient()
            move(selected, 1)
            draw(input)
            draw_outline()
        elif mode==3:
            gradient()
            adjust(selected, start, 1)
            draw(input)
            draw_adjust()
        if zoom>0:
            dif=(hstop-hstart)/2
            hstart=input[selected][0]-dif
            hstop=input[selected][0]+dif
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==2:
                draw_outline()
            elif mode==1:
                draw_half()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
    #Middle Button
    elif ev == key_codes.EKeySelect:
        if menu:
            menu=0
            choices = [u"This Event",u"Reminder",u"Anniversary", u"Message"]
            gradient()
            draw(input)
            draw_rectangle(input)
            draw_sms()
            draw_signal()
            handle_redraw(None)
            index = appuifw2.popup_menu(choices, u"Select:")
            if index == 0:
                quick_edit()
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
                        selected=-1
                        remindinfo=unicode(remind[c1][2])
                        del remind[c1]
                        draw_sms()
                        selected=0
                        exploremode=-1
                        draw_sms()
                        draw_hline()
                        handle_redraw(None)
            elif index == 3:
                sms=[]
                if smslist!=[]:
                    db=contacts.open()
                    for i in smslist:
                        if (0<=(int(i[0])-viewday)) and (3600*24 >(int(i[0])-viewday)):
                            sms.extend([unicode(int(i[0]-viewday)/3600)+":"+str(int((i[0]-viewday)%3600/60))+" "+db.__getitem__(int(i[3])).title+"-" +i[2]])
                    c1 = appuifw2.popup_menu(sms,u"Sms list:")
                    if c1!=None:
                        hline=(smslist[c1][0]-viewday)/60
                        m=1
                        selected=0
                        messageinfo=unicode(smslist[c1][2])
                        del smslist[c1]
                        smslist.sort()
                        pickle.dump(smslist,open('C:\\idealist\\smses.txt','w'))
                        selected=0
                        exploremode=-1
                        draw_sms()
                        draw_hline()
                        handle_redraw(None)
            elif index == 2: 
                if annivs!=[]:
                    names=[]
                    for i in annivs:
                        names.extend([i[0]])
                    c1 = appuifw2.popup_menu(names,u"Anniversary:")
                    if c1!=None:
                        exploremode=0
                        appuifw2.note(u"Choose the day")
                        annivsinfo=unicode(annivs[c1][0])
                        a=calendar.open()
                        a.__delitem__(int(annivs[c1][1]))
                        del annivs[c1]
                        draw(input)
                        draw_sms()
                        handle_redraw(None)
            return 0
        if exploremode==2:
            if dlist==[]:
                appuifw2.note(u"There's nothing to choose from at this day")
                exploremode=1
            else:
                check_add()
        elif exploremode==0:
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
                    c=db.__getitem__(allo[b])
                    c.begin()
                    c.add_field('date',viewday)
                    c.commit()
                    newaniv(u"" + showpeople[b])
                annivsinfo=u""
            elif a==1:
                newaniv()
            return 0
        elif exploremode==-1:
            if m:
                newmessage()
                m=0
            else:
                newreminder()
        elif exploremode==1:
            #Pretty much awesome function!
            if mode==0 and input[selected]!=[]:
                try:
                    del ideabox
                except:
                    pass
                theid=input[selected][-1]
                for i in range(1,len(base)):
                    if theid in base[i][0]:
                        ideabox=Ideabox(index=i)
                        return 0
                b=appuifw2.popup_menu([u"Connect with IdeaBox",u"New Ideabox"],u"Choose")
                if len(base[0][1:])<1:
                    b=1
                if b==0:
                    args=[]
                    for i in base[0][1:]:
                        args+=[i.title]
                    c=appuifw2.popup_menu(args,u"")
                    if c!=None:
                        base[c+1][0].extend([theid])
                        savebase()
                    ideabox=Ideabox(index=(c+1))
                    
                elif b==1:
                    ideabox=Ideabox(theid=theid)
                    savebase()
                loadbase()
            elif mode==1:
                if anychange:
                    colisions = checkcolisions()
                    if len(colisions)==1 and (eventl[2]*60+eventl[3]-eventl[0]*60-eventl[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
                        input.extend([eventl])
                        overwrite(-1)
                    elif len(colisions)==0:
                        #IN FUTURE MAKE IT POSIBLE TO ADD IT HERE AFTER A WARNING BY SPLITING UP OTHERS AND ADDING THEM TO IDEABOX
                        appuifw2.note(u"You can't add it here!")
                    else:
                        choices = [u"Use biggest",u"Use all ava. space"]
                        index = appuifw2.popup_menu(choices, u"What to do?:")
                        if index == 0:
                            much=0
                            record=0
                            for i in colisions:
                                if (i[2]*60+i[3]-i[0]*60-i[1])>much:
                                    record=i
                                    much=i[2]*60+i[3]-i[0]*60-i[1]
                            idea2event(record,eventl)
                            a= appuifw2.query(u"Add the rest to the IdeaList?", "query")
                            if a:
                                event2idea(eventl,much)
                        elif index == 1:
                            a=calendar.open()
                            a.__delitem__(eventl[-1])
                            much=0
                            for i in colisions:
                               idea2event(i,eventl)
                               much+=i[2]*60+i[3]-i[0]*60-i[1]
                            if much<(eventl[2]*60+eventl[3]-eventl[0]*60-eventl[1]):
                                b= appuifw2.query(u"Add the rest to the IdeaList?", "query")
                                if b:
                                    event2idea(eventl,much)
                    anychange=0
                    if otherday == viewday:
                        del input[selected]
                    prepare(viewday)
                    mode=0
                    gradient()
                    draw_signal()
                    draw(input)
                    draw_rectangle(input)
                    handle_redraw(None)
                    return 0
                if otherday==viewday:
                    prepare(viewday)
                gradient()
                mode=2
                draw(input)
                draw_outline()
                handle_redraw(None)
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
                    draw_signal()
                    draw(input)
                    draw_rectangle(input)
                    handle_redraw(None)
                    return 0
                gradient()
                mode =3
                draw_signal()
                draw(input)
                draw_adjust()
                handle_redraw(None)
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
                    draw_signal()
                    draw(input)
                    draw_rectangle(input)
                    handle_redraw(None)
                    return 0
                mode=0
                gradient()
                draw_signal()
                draw(input)
                draw_rectangle(input)
                handle_redraw(None)
            else:
                try:
                    if input[selected]==[] and mode!=1:
                        appuifw2.note(u"Nothing to edit!")
                        return 0
                except:
                    pass

    #Left arrow handler
    elif ev == key_codes.EKeyLeftArrow:
        if menu:
            menu=0
            appuifw2.app.screen='normal'
            nana=appuifw2.Listbox(ideasnames(),putit)
            nana.bind(key_codes.EKeyBackspace,delidea)
            nana.bind(key_codes.EKeyYes,editidea)
            nana.bind(key_codes.EKeyLeftArrow,cleft)
            nana.bind(key_codes.EKeyRightArrow,cright)
            appuifw2.app.body=nana
            appuifw2.app.menu_key_text=u"Add Idea"
            appuifw2.app.left_navi_arrow=True
            appuifw2.app.right_navi_arrow=True
            if cati==len(ideacat):
                appuifw2.app.navi_text=u'All categories'
            else:
                appuifw2.app.navi_text=ideacat[cati][0]
            appuifw2.app.menu=[]
            appuifw2.app.menu_key_handler=newidea
            return 0
        if zoom!=0:
            zoom=0
            hstart=dhstart
            hstop=dhstop
        if exploremode==2 and mode==0:
            viewday-=3600*24
            weekday-=1
            if weekday<0:
                weekday=weekday%7
            prepare(viewday)
            difflist(input)
            selected=0
            gradient()
            draw(input)
            draw_sms()
            draw_signal()
            draw_rectangle(dlist)
            if dlist==[]:
                img.rectangle((12,h-12,w,h),fill=(0,0,0))
                img.text((12,h),u"Can't insert here! It's a past day!",fill=(255,255,255))
        elif exploremode==0:
            viewday-=3600*24
            weekday-=1
            if weekday<0:
                weekday=weekday%7
            prepare(viewday)
            selected=0
            gradient()
            draw(input)
            draw_sms()
            draw_signal()
            
        elif exploremode==-1:
            viewday-=3600*24
            weekday-=1
            if weekday<0:
                weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(input)
            draw_hline()
            draw_sms()
            draw_signal()
        elif mode==0 and exploremode!=2:
            if selected==-1:
                draw(input)
                whichnew-=1
            else:
                viewday-=3600*24
                weekday-=1
                if weekday<0:
                    weekday=weekday%7
                prepare(viewday)
                selected=0
                gradient()
                draw(input)
                draw_signal()
                if exploremode ==2:
                    difflist(input)
            if whichnew==0:
                whichnew=4
            draw_rectangle(input)
            draw_sms()
            draw_signal()
        elif mode==1:
            viewday-=3600*24
            weekday-=1
            if weekday<0:
                weekday=weekday%7
            prepare(viewday)
            if input==[[]]:
                input=[[]]
            elif otherday==viewday:
                del input[selected]
            anychange = 1
            gradient()
            draw(input)
            draw_sms()
            draw_signal()
            draw_half()
        elif mode==2:
            selected-=1
            gradient()
            draw(input)
            draw_signal()
            draw_outline()
        elif mode==3:
            if start == 0:
                selected -= 1
            gradient()
            start = not start
            draw(input)
            draw_signal()
            draw_adjust()
            
    #Right arrow handler
    elif ev == key_codes.EKeyRightArrow:
        if menu:
            menu=0
            try:
                del ideabox
            except:
                pass
            ideabox = Ideabox()
            return 0
        if zoom!=0:
            zoom=0
            hstart=dhstart
            hstop=dhstop
        if exploremode==2:
            viewday+=3600*24
            weekday+=1
            if weekday>6:
                weekday=weekday%7
            prepare(viewday)
            difflist(input)
            selected=0
            gradient()
            draw(input)
            draw_rectangle(dlist)
            draw_sms()
            draw_signal()
            if dlist==[]:
                img.rectangle((12,h-12,w,h),fill=(0,0,0))
                img.text((12,h),u"Can't insert here! It's a past day!",fill=(255,255,255))
        elif exploremode==0:
            viewday+=3600*24
            weekday+=1
            if weekday>6:
                weekday=weekday%7
            prepare(viewday)
            selected=0
            gradient()
            draw(input)
            draw_sms()
            draw_signal()
        elif exploremode==-1:
            viewday+=3600*24
            weekday+=1
            if weekday>6:
                weekday=weekday%7
            prepare(viewday)
            gradient()
            draw(input)
            draw_hline()
            draw_sms()
            draw_signal()
        elif mode==0 and exploremode!=2:
            if selected==-1:
                draw(input)
                whichnew+=1
            else:
                viewday+=3600*24
                weekday+=1
                if weekday>6:
                    weekday=weekday%7
                prepare(viewday)
                selected=0
                gradient()
                draw(input)
                draw_signal()
                if exploremode ==2:
                    difflist(input)
            if whichnew==5:
                whichnew=1
            draw_rectangle(input)
            draw_sms()
            draw_signal()
        elif mode==1:
            viewday+=3600*24
            weekday+=1
            if weekday>6:
                weekday=weekday%7
            prepare(viewday)
            if input==[[]]:
                input=[[]]
            elif otherday==viewday:
                del input[selected]
            anychange = 1
            gradient()
            draw(input)
            draw_sms()
            draw_signal()
            draw_half()
            
        elif mode==2:
            selected+=1
            gradient()
            draw(input)
            draw_signal()
            draw_outline()
            
        elif mode==3:
            if start == 1:
                selected += 1
            gradient()
            start = not start
            draw(input)
            draw_signal()
            draw_adjust()
            
    elif ev== key_codes.EKeyStar:
        zoom+=1
        hstart = (input[selected][0]-hstart)/2+hstart
        hstop = hstop-(hstop-input[selected][0])/2
        gradient()
        vadjustrefresh()
        draw(input)
        draw_sms()
        if mode==1:
            draw_half()
        elif mode==2:
            draw_outline()
        elif mode==3:
            draw_adjust()
        else:
            draw_rectangle(input)
        
    elif ev== key_codes.EKeyHash:
        if zoom != 0:
            zoom-=1
            hstart=2*hstart-input[selected][0]
            hstop=2*hstop-input[selected][0]
            if hstart<dhstart:
                hstart=dhstart
            if hstop>dhstop:
                hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==1:
                draw_half()
            elif mode==2:
                draw_outline()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
        elif zoom ==0:
            hstart=dhstart
            hstop=dhstop
            vadjustrefresh()
            gradient()
            draw(input)
            if mode==1:
                draw_half()
            elif mode==2:
                draw_outline()
            elif mode==3:
                draw_adjust()
            else:
                draw_rectangle(input)
        draw_sms()
    elif ev== key_codes.EKeyYes and exploremode==1 and selected !=-1:
        quick_edit()

    #Deletes an event from the calendar
    elif ev == key_codes.EKeyBackspace and selected != -1:
        delevent(selected)
        if input==[]:
            input=[[]]
            selected=0
        gradient()
        draw(input)
        draw_rectangle(input)
    handle_redraw(None)


def cleft():
    global cati, ideacat, ideas
    cati-=1
    if cati<0:
        cati=len(ideacat)
    appuifw2.app.body.set_list(ideasnames(),0)
    if cati<len(ideacat):
        appuifw2.app.navi_text=ideacat[cati][0]
    else:
        appuifw2.app.navi_text=u"All categories"                

def cright():
    global cati, ideacat, ideas
    cati+=1
    if cati>len(ideacat):
        cati=0
    appuifw2.app.body.set_list(ideasnames(),0)
    if cati<len(ideacat):
        appuifw2.app.navi_text=ideacat[cati][0]
    else:
        appuifw2.app.navi_text=u"All categories"
    


#Function preparing events db [From internal calendar -> inside the app]
def prepare(datetime):
    global input, annivs, format_time, remind
    try:
        b=calendar.open()
    except():
        exit()
    c=b.daily_instances(datetime, appointments=1, events=0, anniversaries=0,todos=0)
    d=[]
    input=[]
    for i in c:
        if i.values()[1]<=datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=b.__getitem__(k)
        input.extend([[int(format_time(z.start_time)[11:13]),int(format_time(z.start_time)[14:16]),int(format_time(z.end_time)[11:13]),int(format_time(z.end_time)[14:16]),z.content,z.location,z.priority,z.id]])
    if input==[]:
        input=[[]]
    
    annivs=[]
    c=b.daily_instances(datetime, appointments=0, events=0, anniversaries=1,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <= datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=b.__getitem__(k)
        annivs.extend([[z.content,z.id]])
    remind=[]
    c=b.daily_instances(datetime, appointments=0, events=1, anniversaries=0,todos=0)
    d=[]
    for i in c:
        if i.values()[1] <= datetime+24*3600:
            d.append(i.values()[0])
    for k in d:
        z=b.__getitem__(k)
        remind.extend([[int(format_time(z.start_time)[11:13]),int(format_time(z.start_time)[14:16]),z.content,z.id]])
    return input
    

#Prepare a list of empty spaces [From input list creates dlist]
def difflist(input):
    global dlist, hstart, hstop, viewday
    #Checking if day is totaly free
    if input==[[]]:
        #If time now is below the time schedule
        if time.time()-hstart*3600<viewday:
            dlist=[[hstart,0,hstop,0,unicode(str((hstop-hstart)*60)), u" minutes", 0, (hstop-hstart)*60]]
        #When time is somewhere in the middle
        else:
            dlist=[[int((time.time()-viewday)/3600),int(((time.time()-viewday)%3600)/60),hstop,0,unicode(int((hstop*3600-time.time()+viewday)/60+((time.time()-viewday)%3600)/60)), u" minutes", 0, int((hstop*3600-time.time()+viewday)/60+((time.time()-viewday)%3600)/60)]]
    else:
        dlist=[]
        varr=[hstart,0]
        #Usual, unempty day
        #A loop over all events in the prepare() day
        for i in input:
            #If time is below the timetable current loop event
            if (time.time()<=(viewday+ i[0]*3600 + i[1]*60)):
                #If it's below the previous event end
                if (time.time() <= (viewday+ varr[0]*3600 + varr[1]*60)):
                    dif=i[1]+(i[0]*60)-varr[0]*60-varr[1]
                    if (dif>0):
                        dlist.extend([[varr[0],varr[1],i[0],i[1],unicode(str(dif)),u" minutes",i[-1],dif]])
                #And if it's not
                else:
                    dlist=[[int((time.time()-viewday)/3600),int(((time.time()-viewday)%3600)/60),i[0],i[1],unicode(int((viewday+i[0]*3600+i[1]*60-time.time())/60)), u" minutes", i[-1], int((viewday+i[0]*3600+i[1]*60-time.time())/60)]]
            varr=[i[2],i[3]]
        #If time is smaller than last event end time (the absence of = makes it imposible to insert something on hstop hour)
        if (time.time()<viewday+varr[0]*3600+varr[1]*60):
           dlist.extend([[varr[0],varr[1],hstop,0, unicode(hstop*60-varr[0]*60-varr[1]),u" minutes",0,hstop*60-varr[0]*60-varr[1]]])
        #If it's between the last event ending and the hstop hour
        elif (time.time()<viewday+hstop*3600):
            dlist.extend([[int((time.time()-viewday)/3600),int(((time.time()-viewday)%3600))/60,hstop,0, unicode(int(hstop*3600-time.time()+viewday)/60),u" minutes",0,int(hstop*3600-time.time()+viewday)/60]])

def orientation():
    if appuifw2.app.orientation=='automatic':
        appuifw2.app.orientation='landscape'
        buildcanvas('Portrait')
    elif appuifw2.app.orientation=='landscape':
        appuifw2.app.orientation='portrait'
        buildcanvas('Automatic')
    elif appuifw2.app.orientation=='portrait':
        appuifw2.app.orientation='automatic'
        buildcanvas('Landscape')
    vadjustrefresh()

timer=e32.Ao_timer()
wlist = []
def forwatch():
    global wlist, currentday
    try:
        b=calendar.open()
    except():
        exit()
    c=b.daily_instances(currentday, appointments=1, events=0, anniversaries=0,todos=0)
    d=[]
    wlist=[]
    for i in c:
        d.append(i.values()[0])
    for k in d:
        z=b.__getitem__(k)
        if z.end_time>time.time():
            wlist.extend([[z.start_time,z.end_time,z.content,z.location,z.priority,z.id]])
forwatch()

def watchout():
    #Timer function
    global input, wlist, img, currentday, smslist,w, h,missedcalls, inboxx,currentfont, unreadsms, phone, message, xprof, menu, timer, mode
    #gradient()
    
    if currentday+24*3600<=time.time():
        currentday+=24*3600*math.floor((time.time()-currentday)/(24*3600))
        forwatch()    
    elif currentday>=time.time():
        currentday+=24*3600*math.floor((time.time()-currentday)/(24*3600))
        forwatch()
    
    
    if smslist!=[]:
        if int(smslist[0][0]/60)==int(time.time()/60):
            messaging.sms_send(smslist[0][1],smslist[0][2])
            del smslist[0]
            smslist.sort()
            pickle.dump(smslist,open('C:\\idealist\\smses.txt','w'))
        if smslist[0][0]<time.time():
            del smslist[0]
            smslist.sort()
            pickle.dump(smslist,open('C:\\idealist\\smses.txt','w'))
    try:
        if wlist!=[] and int(wlist[0][1]/60)==int(time.time()/60) and (int(wlist[0][4])==1):
            xprofile.set_ap(0)
            del wlist[0]
        if wlist!=[] and int(wlist[0][0]/60)==int(time.time()/60) and (int(wlist[0][4])==1):
            xprofile.set_ap(1)
        
    except:
        pass
    
    #This lines display a new message when it comes
    unreadsms=0
    if inboxx.unread(inboxx.sms_messages()[0])<>0:
        unreadsms=1
    #Displays missed calls
    l=logs.calls(mode='missed')  #The dictionary for the latest missed call
    missedcalls=0
    if len(l)>0 and l[0]["flags"]==0:
        missedcalls=1
    else:
        missedcalls=0
    del l
    xprof=xprofile.get_ap()[0]
    
    draw(input)
    draw_signal()
    if menu:
        mmenu()
    elif mode==1:
        draw_half()
    elif mode==2:
        draw_outline()
    elif mode==3:
        draw_adjust()
    elif exploremode==-1:
        draw_hline()
    else:
        draw_rectangle(input)
    
    
    
    handle_redraw(None)
    timer.after(30, watchout)
    
def gradient():
    global img, h, w, currentday, newh
    z=(h-newh-endh)*1./100
    anglehour=(2*math.pi*((time.time()-currentday)/3600)/24)
    coshour=math.cos(anglehour)
    for i in range(0,100):
        img.rectangle((12,int(i*z+newh),w,int((i+1)*z+newh)), fill=(20,int(-25*coshour+(160-i)),int(-25*coshour+(175-i))))

def quit():
    global exploremode, mode, viewday,anychange, running, input, img, selected, menu, timer, inboxx

    if menu:
        menu=0
        gradient()
        draw(input)
        draw_rectangle(input)
        draw_sms()
        draw_signal()
        handle_redraw(None)
        return 0
    savebase()
    
    if appuifw2.app.screen=='normal':
        appuifw2.app.left_navi_arrow=False
        appuifw2.app.right_navi_arrow=False
        appuifw2.app.menu_key_handler=None
        appuifw2.app.navi_text=u''
        appuifw2.app.menu_key_text=u'Options'
        #appuifw2.app.screen = 'full'
        buildcanvas('Landscape')
        appuifw2.app.body = canvas
        #gradient()
        
        #draw(input)
        #draw_sms()
        #draw_signal()
        draw_rectangle(input)
        handle_redraw(None)
    elif exploremode == 2 or exploremode==-1:
        exploremode =1
        prepare(viewday)
        gradient()
        draw(input)
        draw_rectangle(input)
        draw_sms()
        draw_signal()
        handle_redraw(None)
    elif exploremode==0:
        exploremode =1
        appuifw2.note(u"Anniversery deleted.")
        prepare(viewday)
        gradient()
        draw(input)
        draw_rectangle(input)
        draw_sms()
        draw_signal()
        handle_redraw(None)
    elif (mode==1 or mode == 2 or mode==3):
        mode=0
        prepare(viewday)
        gradient()
        draw(input)
        draw_rectangle(input)
        draw_sms()
        draw_signal()
        handle_redraw(None)
        anychange=0
    else:
        try:
            saveconfig()
        except:
            appuifw2.note(u"Error saving config file")
        try:
            timer.cancel()
        except:
            appuifw2.note(u"Error while stopping the main loop")
        del timer
        del inboxx
        appuifw2.app.menu_key_handler=None
        app_lock.signal()
        appuifw2.app.set_exit()


canvas=0
img=0
w=0
h=0
#THE DRAWING PART
vadjust=(h-newh-endh)/(hstop-hstart)
def vadjustrefresh():
    global newh, h, hstop, hstart, vadjust, hline, dish, endh
    vadjust=(h-newh-endh)/(hstop-hstart)



def resize_canvas(rect):
    global canvas, img, w,h, input
    if not canvas: return

    # Initialize drawing coordinate
    if img: del img
    img = graphics.Image.new(canvas.size, mode='RGB')
    w, h = canvas.size
    try:
        vadjustrefresh()
        gradient()
        draw(input)
        draw_sms()
        draw_signal()
    except:
        pass
    

def predraw():
    global w,h, img, canvas
    img = None
    canvas = appuifw2.Canvas(\
                  redraw_callback = handle_redraw,\
                  event_callback = handle_event,
                  resize_callback= resize_canvas)
    appuifw2.app.body = canvas
    appuifw2.app.title = u"IdeaList"
    appuifw2.app.screen = 'full'

predraw()


def changefont():
    global currentfont, input
    fonty=appuifw2.available_fonts()
    del fonty[-1]
    a=appuifw2.popup_menu(fonty,u"Choose a font")
    if a!=None:
        currentfont=fonty[a]
        draw(input)
        draw_rectangle(input)
        
def hourset():
    global hstart, hstop, dhstart, dhstop, input
    a=appuifw2.query(u"Wake-up hour","time",float(dhstart*3600))
    b=appuifw2.query(u"Go to sleep hour", "time", float(dhstop*3600))
    if a!=None and b!=None:
        hstart=dhstart=int(a/3600)
        hstop=dhstop=int(b/3600)
        vadjustrefresh()
        gradient()
        draw(input)
        draw_sms()

def website():
    e32.start_exe('BrowserNG.exe', ' "4 http://www.masteranza.wordpress.com/ 1"', 1)

def catconfig():
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
        catconfig()
    appuifw2.app.screen='full'
    
def mmenu():
    global currentfont, w, h, menu
    img.polygon((40,h/2,w/2,h/2-w/2+40,w-40,h/2,w/2,h/2+w/2-40),fill=(0,0,0), outline=(200,200,200), width=4)
    img.rectangle((20+w/4,h/2-w/4+20,w-20-w/4,h/2+w/4-20),outline=(200,200,200), width=4)
    img.text((w/2-12,h/2+5),u"Edit",fill=(255,255,255), font=currentfont)
    img.text((w/2-10,h/2-w/4+10),u"New",fill=(255,255,255), font=currentfont)
    img.text((w/4-4,h/2+5),u"List",fill=(255,255,255), font=currentfont)
    img.text((w-10-w/4,h/2+5),u"Box",fill=(255,255,255), font=currentfont)
    img.text((w/2-20,h/2+w/4-5),u"Settings",fill=(255,255,255), font=currentfont)
    menu=1
    handle_redraw(None)

def version():
    appuifw2.note(u"Idealist 1.0\nby Ranza's Research",'info')
def shortcuts():
    shortk=appuifw2.Text(text=u"Green Key - Quick Edit\nPencil Key - Enter Edit mode\nStar Key - Zoom in\nHash key - Zoom out\n1 - Jump to date\n2 - New Event\n3 - New Idea\n4 - Opens IdeaList\n5 - New Reminder\n6 - Opens Ideabox\n\nHowever if you're in edit mode the keys:\n2 & 0 - move selection quickly [30 min]\n5 & 8 - move selection slowly [1 min]")
    appuifw2.app.screen='normal'
    appuifw2.app.body=shortk

def buildcanvas(strs):
    global w,h, img, canvas, selected
    appuifw2.app.screen = 'full'
    appuifw2.app.menu_key_handler = mmenu
    appuifw2.app.menu = None
    appuifw2.app.exit_key_handler = quit
    w, h = canvas.size
    img = graphics.Image.new((canvas.size[0], canvas.size[1]), mode='RGB')
    try:
        gradient()
        selected=0
        draw(input)
        draw_sms()
        draw_signal()
        draw_rectangle(input)
        #watchout()
        handle_redraw(None)
    except:
        pass
buildcanvas('Landscape')

input=[[]]
input=prepare(viewday)

    
def draw(list):
    global vadjust, newh, currentask, viewday, ideacat, hstart, hstop, annivs, w, h, currentday, logo, present, smslist, exploremode, currentfont, weekday, days
    if input!=[[]]:
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
            img.rectangle((12,int(cc+hsize+difk+newh),w,int(cc+2*(hsize)+difk+newh)), fill=clor)
            img.line((12,cc+newh,w,cc+newh), outline=(30,30,30), width=1)
            img.line((12,cc+newh+2*(hsize)+difk,w,cc+newh+2*(hsize)+difk), outline=(30,30,30), width=1)
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
    if exploremode==0:
        img.rectangle((12,h-12,w,h),fill=(0,0,0))
        img.text((11,h),u"Choose day by pressing select",fill=(255,255,255))    
    
        
def draw_sms():
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
    if len(smslist) > 0:
        for y in smslist:
            if (y[0]-viewday)>0 and (y[0]-viewday)<3600*24:
                img.line((10,((y[0]-viewday)/3600-hstart)*vadjust+newh,16,((y[0]-viewday)/3600-hstart)*vadjust+newh),outline = (250,250,100), width = 2)
                img.blit(message, target=(0,((y[0]-viewday)/3600-hstart)*vadjust+newh))

def draw_signal():
    
    #Signal and battery lines, changing every minute
    img.rectangle((0,h-endh,w,h),fill=(0,0,0))
    global unreadsms, missedcalls, phone, sms, currentfont, silence, xprof
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
    img.text((w-30,h), unicode(hourr+":"+minutess), font=currentfont ,fill=(245,245,245))
    if missedcalls==1:
        img.blit(phone, target=(w-57,h-11))
    if unreadsms==1:
        img.blit(sms, target=(w-72,h-11))
    if xprof:
        img.blit(silence, target=(w-42,h-11))
    
    all=u" " + unicode(days[weekday])
    if int(-(currentday-viewday)/(3600*24))==0:
        all+=u" (Today)"
    elif int(viewday-3600*24)/(3600*24)==watched:
        all+=u" (Tomorow)"
    elif int(viewday-7200*24)/(3600*24)==watched:
        all+=u" (After Tomorow)"
    elif int(viewday+3600*24)/(3600*24)==watched:
        all+=u" (Yesterday)"
    elif (watched-int(viewday/(3600*24)))%7==0:
        all+=u" (" + str(-(watched-int(viewday/(3600*24)))/7) + " week)"
    img.text((12,12), unicode(format_time(viewday)[:10])+all,font=currentfont, fill = (255,255,255))
    img.blit(logo, target=(w-14,0))

def draw_rectangle(list):
    global selected, newh, vadjust,whichnew, mode, ideacat, exploremode, dish, currentfont,logo, currentfont,w
    
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
    #draw_signal()
    
def draw_adjust():
    global input, selected, start,h,w
    if (selected < 0):
        selected=len(input)-1
    elif (selected > int(len(input)-1)):
        selected=0
    draw_signal()
    img.rectangle((12,h-10,100,h),fill=(0,0,0))
    img.text((12,h),u"Resize mode on",fill=(255,255,255))
    #draw_rectangle(input)
    if start:
        img.line((12,(input[selected][2]+(input[selected][3]*1./60)-hstart)*vadjust+newh ,w,(input[selected][2]+(input[selected][3]*1./60)-hstart)*vadjust+newh ), outline = (0,150,0), width = 3)
    else:
        img.line((12,(input[selected][0]+(input[selected][1]*1./60)-hstart)*vadjust+newh  ,w,(input[selected][0]+(input[selected][1]*1./60)-hstart)*vadjust+newh ), outline = (0,150,0), width = 3)
    
    
def draw_half():
    global eventl, colors, ideacat, hstart, hstop, vadjust, newh,w,h, selected, input
    draw_signal()
    img.rectangle((12,h-10,90,h),fill=(0,0,0))
    img.text((12,h),u"Move mode on",fill=(255,255,255))
    colisions= checkcolisions()
    if len(colisions)==0:
        color=colors[12]
    elif len(colisions)==1 and (eventl[2]*60+eventl[3]-eventl[0]*60-eventl[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
        color=colors[13]
    else:
        color=colors[14]
        
    category=eventl[5]
    try:
        category=ideacat[int(category)][0]
    except:
        category=eventl[5]
    img.rectangle((w/2,(eventl[0]+(eventl[1]*1./60)-hstart)*vadjust+newh,w,(eventl[2]+ (eventl[3]*1./60)-hstart)*vadjust+newh), fill=color)
    img.text((w/2 + 2,(eventl[0]+(eventl[1]*1./60)-hstart)*vadjust+10+newh), unicode(str(eventl[0]) +":" + str(eventl[1])+ "-" + str(eventl[2]) +":" + str(eventl[3])+ " "+ eventl[4] +"| " + category), fill = colors[4])
    
def draw_outline():
    global input, selected,w,h
    if (selected < 0):
        selected=len(input)-1
    elif (selected > int(len(input)-1)):
        selected=0
    draw_signal()
    img.rectangle((12,h-10,140,h),fill=(0,0,0))
    img.text((12,h),u"Change order mode on",fill=(255,255,255))
    #draw_rectangle(input)
    img.line((12,(input[selected][2]+(input[selected][3]*1./60)-hstart)*vadjust+newh,w,(input[selected][2]+(input[selected][3]*1./60)-hstart)*vadjust+newh), outline = colors[13], width = 3)
    img.line((12,(input[selected][0]+(input[selected][1]*1./60)-hstart)*vadjust+newh,w,(input[selected][0]+(input[selected][1]*1./60)-hstart)*vadjust+newh), outline = colors[13], width = 3)
    
    
def draw_hline():
    global input, selected, hline
    draw_signal()
    img.rectangle((12,h-10,100,h),fill=(0,0,0))
    img.text((12,h),u"Insert mode on",fill=(255,255,255))
    img.line((12,(hline-hstart*60)*vadjust/60+newh ,w,(hline-hstart*60)*vadjust/60+newh), outline = colors[8], width = 2)
    img.rectangle((w-26,(hline-hstart*60)*vadjust/60+newh-12,w,(hline-hstart*60)*vadjust/60+newh),fill=(5,5,5))
    img.text((w-26,(hline-hstart*60)*vadjust/60+newh), unicode(str(int(hline/60))+":"+str(int(hline%60))), fill=colors[8])

def update():
    global timer
    # define a url where the picture you want to download is located on the net
    url = "http://idealist.googlecode.com/files/idealist.py"
    # define the file name and the location of the downloaded file for local storage e.g. on the c drive
    tempfile = "c:\\Private\\"+ str(appuifw2.app.uid()) + "\\default.py"
    try:
        urllib.urlretrieve(url, tempfile)
        appuifw2.note(u"Succesfuly updated! The app will exit now", "info")
        e32.ao_sleep(1)
        quit()
    except:
        appuifw2.note(u"Could not communicate with the server.")

gradient()
draw(input)
draw_sms()
draw_signal()
draw_rectangle(input)
app_lock = e32.Ao_lock()
watchout()
handle_redraw(None)
app_lock.wait()