import appuifw2, TopWindow, appswitch, keycapture, miso, e32db, contacts, globalui, messaging, math, sysinfo, xprofile
import e32, key_codes, graphics, time, calendar, logs, inbox, sysinfo, urllib, envy, thread
from e32db import format_time
from akntextutils import wrap_text_to_array
import cerealizer as pickle
#Setting system app status
try:
    envy.set_app_system(1)
except:
    appuifw2.note(u"Can't set a system app status!");

class DrawStandby:
    window=None
    app_lock = None
    def __init__(self):
        #self.app_lock = e32.Ao_lock()
        #Create an instance of TopWindow
        self.window = TopWindow.TopWindow()
        #Set its size
        self.window.size = (210, 160)
        #Set the position of it upper left corner
        self.window.position = (50, 60)
         
        #Create a new, red image to display
        img = graphics.Image.new((0, 0))
        img.clear(0x000000)
        #Write text on it
        img.text((25, 25), u"This is a pop-up", font = 'title')
        #Add it to the window specifying coordinates for its upper left corner
        self.window.add_image(img, (10, 10))
        #Make the window's background green
        self.window.background_color = 0x000000
        #Make the corners round
        self.window.corner_type = 'corner5'
        #Key capture
        capturer=keycapture.KeyCapturer(self.cb_capture)
        capturer.keys=(keycapture.EKey1,keycapture.EKey2)
        capturer.start()
        #self.app_lock.wait()
    def hide(self):
        self.window.hide()
    
    def show(self):
        (size, position) = appuifw2.app.layout(appuifw2.EWallpaperPane)
        self.window.size = size
        self.window.position= position
        self.window.show()
 
    def cb_capture(self,key):
        if(key==keycapture.EKey1):
            globalui.global_note(u"Maselko!")
        elif(key==keycapture.EKey2):
            globalui.global_note(u"prawie maslo :)")
    




    

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


    


class Categories:
    def __init__():
        pass

class Main:
    
    def __init__(self):
        
        #Loading all images needed for the application
        self.logo = graphics.Image.open('C:\\idealist\\logo.png')
        self.present = graphics.Image.open('C:\\idealist\\present.png')
        self.bell = graphics.Image.open('C:\\idealist\\bell.png')
        self.message = graphics.Image.open('C:\\idealist\\message.png')
        self.phone = graphics.Image.open('C:\\idealist\\phone.png')
        self.sms = graphics.Image.open('C:\\idealist\\sms.png')
        self.silence = graphics.Image.open('C:\\idealist\\silence.png')
        self.messageinfo=u""
        self.remindersinfo=u""
        self.anniversariesinfo=u""
        
        
        
        
        #Lists of data
        self.days=[u"Monday",u"Tuesday",u"Wednesday",u"Thursday",u"Friday",u"Saturday",u"Sunday"]
        self.months=[u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December"]
        #Initializing time
        tempek=list(time.localtime())
        tempek[3]=tempek[4]=tempek[5]=0
        tempek=tuple(tempek)
        self.viewday=time.mktime(tempek)
        self.currentday=float(self.viewday)
        self.weekday=time.localtime().tm_wday
        #All the variables used in app
        self.anniversaries=[]
        self.reminders=[]
        #variables which specify if the Ideas menu should be visible
        self.selected=0
        self.start = 0
        #The beginning of the day
        self.dhstart=self.hstart=7
        self.dhstop=self.hstop=23
        self.newh=14
        self.endh=10
        self.m=0
        self.currentfont='dense'
        self.missedcalls=0
        self.unreadsms=0
        self.atext=""
        #0-select mode (multiple), 1-move mode (multiple), 2-adjust mode (single)
        self.smslist=[]
        self.projects=[]
        self.mode=0
        self.inHand=0
        self.whichnew=3
        self.ideacat=[[u'Temp',(220,220,220)],[u'School',(200,200,70)],[u'Work',(200,200,70)],[u'Science',(220,70,200)],[u'Physical Exercise',(100,70,100)],[u'Meeting',(70,100,100)],[u'Relax',(100,70,70)],[u'Shoping',(80,80,80)],[u'Cleanings',(90,90,90)]]
        self.cati=len(self.ideacat)
        self.path='C:\\idealist\\ideas.txt'
        #Initialize the reading ideas from file
        self.ideas=[]
        self.anychange=0
        #Define if alarms should be enabled
        self.alarm = 1
        #A variable for mode=2 event
        self.eventCopy=0
        self.otherday=0
        self.savelist=[]
        self.hline=0
        self.c1=0
        self.dish=11
        #It's 1 if menu is opened
        self.menu=0
        self.screenObj=None
        self.onstandby=False
        self.xprof=0
        self.img=0
        self.w=0
        self.h=0
        self.lastPress=0
        #THE DRAWING PART
        self.vadjust=(self.h-self.newh-self.endh)/(self.hstop-self.hstart)
        self.events=self.prepare(self.viewday)
        self.canvas=0
        
        
        self.loadConfig()
        self.predraw()
        self.buildCanvas()
        self.forwatch()
        self.watchout()
        
        
        
    polish={"yes":u"Tak","no":u"Nie","months":[u"Styczeń",u"Luty",u"Marzec",u"Kwiecień",u"Maj",u"Czerwiec",u"Lipiec",u"Sierpień",u"Wrzesień",u"Październik",u"Listopad",u"Grudzień"],"days":[u"Poniedziałek",u"Wtorek",u"Środa",u"Czwartek",u"Piątek",u"Sobota",u"Niedziela"]}
    english={"yes":u"Yes","no":u"No","months":[u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December"],"days":[u"Monday",u"Tuesday",u"Wednesday",u"Thursday",u"Friday",u"Saturday",u"Sunday"]}
    
    
    
    
    
    inboxx=inbox.Inbox()
    def saveConfig(self):
        
        tosave=[self.ideacat,self.dhstart,self.dhstop,self.currentfont,self.alarm]
        try:
            pickle.dump(self.tosave,open('C:\\idealist\\config.txt','w'))
        except:
            pass
            #appuifw2.note(u"Can't save the config file")
        
    def loadConfig(self):
        
        try:
            toload=pickle.load(open('C:\\idealist\\config.txt'))
            self.ideacat=toload[0]
            self.dhstart=self.hstart=toload[1]
            self.dhstop=self.hstop=toload[2]
            self.currentfont=toload[3]
            self.alarm = toload[4]
        except:
            #appuifw2.note(u"[First run warnings]")
            #appuifw2.note(u"Can't load the config file")
            pass
            
    
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
    def loadbase(self):
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
    
    def savebase(self):
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
    
    
    
    
    
    
    
    
    
    
    
    
    #Function preparing events database
    #optimazed
    def prepare(self, datetime):
        try:
            b=calendar.open()
        except():
            appuifw2.note("Can't open the nokia calendar db")
            
            
        #Prepare events list
        d=[]
        self.events=[]
        c=b.daily_instances(datetime, appointments=1, events=0, anniversaries=0,todos=0)
        for i in c:
            if i.values()[1]<=datetime+24*3600:
                d.append(i.values()[0])
        for k in d:
            z=b.__getitem__(k)
            start=time.gmtime(z.start_time)
            end=time.gmtime(z.end_time)
            self.events.extend([[start[3]-start[-1],start[4],end[3]-end[-1],end[4],z.content,z.location,z.priority,z.id]])
        if self.events==[]:
            self.events=[[]]
        
        #Prepare anniversaries list
        self.anniversaries=[]
        c=b.daily_instances(datetime, appointments=0, events=0, anniversaries=1,todos=0)
        d=[]
        for i in c:
            if i.values()[1] <= datetime+24*3600:
                d.append(i.values()[0])
        for k in d:
            z=b.__getitem__(k)
            self.anniversaries.extend([[z.content,z.id]])
            
        #Prepare reminders list
        self.reminders=[]
        c=b.daily_instances(datetime, appointments=0, events=1, anniversaries=0,todos=0)
        d=[]
        for i in c:
            if i.values()[1] <= datetime+24*3600:
                d.append(i.values()[0])
        for k in d:
            z=b.__getitem__(k)
            start=time.gmtime(z.start_time)
            self.reminders.extend([[start[3]-start[-1],start[4],z.content,z.id]])
        return self.events
    
    def buildRepeat(self, start, edit=0):
        posibles=['daily','weekly','monthly_by_days','monthly_by_dates','yearly_by_date','yearly_by_day']
        a=appuifw2.popup_menu([u'Daily',u'Weekly',u'Monthly by days',u'Monthly by days',u'Yearly by date',u'Yearly by day',u'Never'], u"Repeat:")
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
        elif a==6:
            return None
        else:
            return None
        repeat={"type":posibles[a],"exceptions":exclist,"start":start,"end":d,"interval":b}
        if a in [1,2,3,5]:
            repeat={"type":posibles[a],"days":replist,"exceptions":exclist,"start":start,"end":d,"interval":b}
        return repeat
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def putit(self):
        
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
            buildCanvas('Landscape')
            gradient()
            draw(self.events)
            drawSms()
            eventsSpace(events)
            if eventsSpace==[]:
                appuifw2.note(u"It's a past day, can't insert it here")
            inHand=2
        if c2==1:
            eventsSpace(events)
            for i in eventsSpace:
                if viewday+i[2]*3600+i[3]*60>time.time():
                    if viewday+i[0]*3600+i[1]*60<time.time():
                        if viewday+i[2]*3600+i[3]*60-time.time()>=ideas[c1][1]:
                            i[0]=int((time.time()-viewday)/3600)
                            i[1]=int(((time.time()-viewday)/60)%60)
                            makeEvent(ideas[c1],i,1)
                            del ideas[c1]
                            return 0
                        continue
                    elif i[2]*3600+i[3]*60-i[0]*3600+i[1]*60>=ideas[c1][1]:
                        makeEvent(ideas[c1],i,1)
                        del ideas[c1]
                        return 0
                continue
            appuifw2.note(u"Sorry, no free space available on this day")
            
    
    
    def makeEvent(self,idea,space, ok=0):
        #This function creates an event in standard calendar using given idea and space
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
        draw(self.events)
        drawSms()
        return c.id
            
    def delEvent():
        global selected, events
        b=calendar.open()
        b.__delitem__(events[selected][-1])
        del events[selected]
        gradient()
        draw(self.events)
        
    def editEvent():
        global selected, events, viewday
        a=[]
        for i in ideacat:
            a.extend([i[0]])
    
        data=[(u'Idea','text',events[selected][4]),(u'Category','combo', (a,int(events[selected][5]))),(u'Silent','combo', ([u"No",u"Yes"],int(events[selected][6]%2))),(u'Event start','time',float(events[selected][0]*3600+events[selected][1]*60)),(u'Event end','time',float(events[selected][2]*3600+events[selected][3]*60)),(u'Event date','date',viewday)]
        flags = appuifw2.FFormEditModeOnly
        f=appuifw2.Form(data,flags)
        f.execute()
        events[selected][4]=f[0][2]
        events[selected][5]=f[1][2][1]
        events[selected][0]=int((f[3][2])/3600)
        events[selected][1]=int((f[3][2])%3600/60)
        events[selected][2]=int((f[4][2])/3600)
        events[selected][3]=int((f[4][2])%3600/60)
        events[selected][6]=int(f[2][2][1])
        if f[5][2] != viewday:
            event=events[selected]
            viewday=f[5][2]
            prepare(viewday)
            if events==[[]]:
                events=[]
            events.extend([event])
            overwrite(-1)
            forwatch()
            events.sort()
            draw(self.events)
            drawRectangle(events)
            return 0
        
        overwrite(selected)
        forwatch()
        draw(self.events)
        drawRectangle(events)
    
    def newEvent():
        a=appuifw2.query(u"Event name:",'text')
        if (a!="" and a!=None):
            selected=0
            inHand=2
            draw(self.events)
            drawRectangle(eventsSpace)
    
    def newReminder():
        global inHand, events, viewday, hline, remindersinfo
        a=appuifw2.query(u"Reminder name:",'text',remindersinfo)
        if a!='' and a!=None:
            c=calendar.open()
            b=c.add_event()
            b.content=unicode(a)
            b.set_time(viewday+hline*60)
            b.alarm=viewday+hline*60
            b.commit()
            appuifw2.note(u"New reminderser succesfuly added")
            prepare(viewday)
            inHand = 1
            draw(self.events)
            drawRectangle(events)
        else:
            inHand=1
            appuifw2.note(u"Adding canceled")
        drawSms()
        remindersinfo=u""
    
    
    def newMessage():
        global inHand, events, viewday, hline, smslist, messageinfo, atext
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
                    inHand = 1
                    for i in range(0,len(smslist)):
                        if smslist[i][0]<time.time():
                            del smslist[i]
                    smslist.sort()
                    pickle.dump(smslist,open('C:\\idealist\\smses.txt','w'))
                except:
                    appuifw2.note(u"The contact doesn't contain a mobile phone number!")
            appuifw2.app.screen='full'
            predraw()
            buildCanvas('Landscape')
            drawSms()
            handleRedraw(None)
        messageinfo=u""
    
    
    
    def newAnniversary(self,str=0):
        if str==0:
            c=appuifw2.query(u"Anniversary of...?", 'text',anniversariesinfo)
        else:
            c=str
        if c != "":
            a=calendar.open()
            b=a.add_anniversary()
            b.content=unicode(c)
            b.set_time(viewday)
            b.alarm=viewday+hstart*3600
            b.commit()
            appuifw2.note(u"New anniversary succesfuly added")
            prepare(viewday)
            inHand = 1
            draw(self.events)
            drawRectangle(events)
            return 0
        inHand=1
        appuifw2.note(u"Adding canceled")
            
    
    def overwrite(self, which=-2):
        
        changed=0
        if which==-2:
            which=self.selected
            changed=1
        b=calendar.open()    
        c=b.__getitem__(self.events[which][-1])
        c.begin()
        alarminfo=c.alarm
        if c.get_repeat()!=None:
            choices = [u"This only", u"Future", u"All"]
            index = appuifw2.popup_menu(choices, u"Save "+self.events[which][4])
            if index==0:
                #Make the old event end at the start day of the new one
                zz=c.get_repeat()
                zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                c.set_repeat(zz)
                c.commit()
                #Make a new shit
                d=b.add_appointment()
                d.content=self.events[which][4]
                d.location=self.events[which][5]
                d.priority=self.events[which][6]
                d.set_time(self.viewday+self.events[which][0]*3600+self.events[which][1]*60,self.viewday+self.events[which][2]*3600+self.events[which][3]*60)
                if alarminfo!=None:
                    d.alarm=self.viewday+self.events[which][0]*3600+self.events[which][1]*60
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
                zz['end']=self.viewday-2*(24*3600)
                try:
                    c.set_repeat(zz)
                except:
                    b.__delitem__(self.events[which][-1])
                c.commit()
                #Make a new shit
                c=b.add_appointment()
                c.content=self.events[which][4]
                c.location=self.events[which][5]
                c.priority=self.events[which][6]
                c.set_time(self.viewday+self.events[which][0]*3600+self.events[which][1]*60,self.viewday+self.events[which][2]*3600+self.events[which][3]*60)
                if alarminfo!=None:
                    c.alarm=self.viewday+self.events[which][0]*3600+self.events[which][1]*60
                else:
                    c.alarm=None
                zzz['start']=self.viewday
                c.set_repeat(zzz)
                c.commit()
                self.forwatch()
            elif index==2:
                #Make the old event end at the start day of the new one
                c.content=self.events[which][4]
                c.location=self.events[which][5]
                c.priority=self.events[which][6]
                c.set_time(self.viewday+self.events[which][0]*3600+self.events[which][1]*60,self.viewday+self.events[which][2]*3600+self.events[which][3]*60)
                if alarminfo!=None:
                    c.alarm=self.viewday+self.events[which][0]*3600+self.events[which][1]*60
                else:
                    c.alarm=None
                c.commit()
                self.forwatch()
        else:
            c.content=self.events[which][4]
            c.location=self.events[which][5]
            c.priority=self.events[which][6]
            c.set_time(self.viewday+self.events[which][0]*3600+self.events[which][1]*60,self.viewday+self.events[which][2]*3600+self.events[which][3]*60)
            if alarminfo!=None:
                c.alarm=self.viewday+self.events[which][0]*3600+self.events[which][1]*60
            else:
                c.alarm=None
            c.commit()
            self.forwatch()
    def delEvent(sel):
        global events
        #DELETE EVENT INTELI GENTLY
        b=calendar.open()
        c=b.__getitem__(events[sel][-1])
        zz=c.get_repeat()
        if zz!=None:
            choices=[u"Remove this only", u"Remove this & future", u"Remove all"]
            index = appuifw2.popup_menu(choices, u""+ events[sel][4])
            notyes1=appuifw2.query( u"Put it also back to IdeaList?","query")
            if notyes1:
                event2idea(events[sel])
            if index==2:
                b.__delitem__(events[sel][-1])
                del events[sel]
            elif index==1:
                c.begin()
                zz['end']=viewday-2*(24*3600)
                c.set_repeat(zz)
                c.commit()
                del events[sel]
            elif index==0:
                b=calendar.open()
                c.begin()
                zz=c.get_repeat()
                zz['exceptions']=list(zz['exceptions']) + [viewday+3600]
                c.set_repeat(zz)
                c.commit()
                del events[sel]
        else:
            yesno=appuifw2.query(u"Do you want to remove event "+ events[sel][4],"query")
            if yesno:
                notyes1=appuifw2.query( u"Put it also back to IdeaList?","query")
                if notyes1:
                    event2idea(events[sel])
                b.__delitem__(events[sel][-1])
                del events[sel]
                #END DELETE EVENT INTELIGENTLY
    

    def move(self, time, sel=0, start=0):
        self.redrawGUI()
        if self.inHand==0:
            #default movement over events
            if self.mode==0:
                if time<0:
                    self.selected-=1
                else:
                    self.selected+=1
                self.drawRectangle(self.events)
            #for drawHalf()
            elif self.mode==1:
                self.anychange = 1
                if (self.hstop*60<=self.eventCopy[2]*60+self.eventCopy[3]+time):
                    time=self.hstop*60-self.eventCopy[2]*60-self.eventCopy[3]
                elif (self.hstart*60>=self.eventCopy[0]*60+self.eventCopy[1]+time):
                    time=self.hstart*60-self.eventCopy[0]*60-self.eventCopy[1]
                self.eventCopy[0]+=((self.eventCopy[1]+time)/60)
                self.eventCopy[1]=((self.eventCopy[1]+time)%60)
                self.eventCopy[2]+=((self.eventCopy[3]+time)/60)
                self.eventCopy[3]=((self.eventCopy[3]+time)%60)
            #for drawOutline()
            elif self.mode==2:
                self.anychange=1
                if sel not in self.savelist:
                    self.savelist+=[sel]
                if (time>0):
                    if sel==len(self.events)-1:
                        if (self.hstop*60<=self.events[sel][2]*60+self.events[sel][3]+time):
                            time=self.hstop*60-self.events[sel][2]*60-self.events[sel][3]
                        if self.events[sel][1]+time>=60:
                            self.events[sel][1]=self.events[sel][1]+time-60
                            self.events[sel][0]+=1
                            if self.events[sel][3]+time>=60:
                                self.events[sel][3]=self.events[sel][3]+time-60
                                self.events[sel][2]+=1
                                return 0
                            self.events[sel][3]+=time
                            return 0
                        if self.events[sel][3]+time>=60:
                            self.events[sel][3]=self.events[sel][3]+time-60
                            self.events[sel][2]+=1
                            self.events[sel][1]+=time
                            return 0
                        self.events[sel][1]+=time
                        self.events[sel][3]+=time
                        return 0
                    elif (self.events[sel+1][0]*60+self.events[sel+1][1]-self.events[sel][2]*60-self.events[sel][3]<time):
                        if sel+1 not in self.savelist:
                            self.savelist+=[sel+1]
                        copysel = list(self.events[sel])
                        copysel1= list(self.events[sel+1])
                        self.events[sel]=list(self.events[sel+1])
                        self.events[sel+1]=list(copysel)
                        #setting hour for the missed event
                        self.events[sel][0]=self.events[sel+1][0]
                        self.events[sel][1]=self.events[sel+1][1]
                        self.events[sel][2]=copysel1[2]-copysel1[0]+self.events[sel+1][0]
                        self.events[sel][3]=copysel1[3]-copysel1[1]+self.events[sel+1][1]
                        if self.events[sel][3]>60:
                            self.events[sel][2]+=1
                            self.events[sel][3]= self.events[sel][3] % 60
                        self.events[sel+1][0]=self.events[sel][2]
                        self.events[sel+1][1]=self.events[sel][3]
                        self.events[sel+1][2]=copysel[2]-copysel[0]+self.events[sel+1][0]
                        self.events[sel+1][3]=copysel[3]-copysel[1]+self.events[sel+1][1]
                        if self.events[sel+1][3]>60:
                            self.events[sel+1][2]+=1
                            self.events[sel+1][3]= self.events[sel+1][3] % 60
                        self.selected+=1
                    else:
                        if self.events[sel][1]+time>=60:
                            self.events[sel][1]=self.events[sel][1]+time-60
                            self.events[sel][0]+=1
                            if self.events[sel][3]+time>=60:
                                self.events[sel][3]=self.events[sel][3]+time-60
                                self.events[sel][2]+=1
                                return 0
                            self.events[sel][3]+=time
                            return 0
                        if self.events[sel][3]+time>=60:
                            self.events[sel][3]=self.events[sel][3]+time-60
                            self.events[sel][2]+=1
                            self.events[sel][1]+=time
                            return 0
                        self.events[sel][1]+=time
                        self.events[sel][3]+=time
                        return 0
                if (time<0):
                    if sel==0:
                        if (self.hstart*60>=self.events[sel][0]*60+self.events[sel][1]+time):
                            time=self.hstart*60-self.events[sel][0]*60-self.events[sel][1]
                        if self.events[sel][1]+time<0:
                            self.events[sel][1]=60+time+self.events[sel][1]
                            self.events[sel][0]-=1
                            if self.events[sel][3]+time<0:
                                self.events[sel][3]=60+time+self.events[sel][3]
                                self.events[sel][2]-=1
                                return 0
                            self.events[sel][3]+=time
                            return 0
                        if self.events[sel][3]+time<0:
                            self.events[sel][3]=60+time+self.events[sel][3]
                            self.events[sel][2]-=1
                            self.events[sel][1]+=time
                            return 0
                        self.events[sel][1]+=time
                        self.events[sel][3]+=time
                        return 0
                    elif (self.events[sel][0]*60+self.events[sel][1]-self.events[sel-1][2]*60-self.events[sel-1][3]<-time):
                        if sel-1 not in self.savelist:
                            self.savelist+=[sel-1]
                        copysel = list(self.events[sel])
                        copysel1= list(self.events[sel-1])
                        self.events[sel]=list(self.events[sel-1])
                        self.events[sel-1]=list(copysel)
                        self.events[sel-1][0]=copysel1[0]
                        self.events[sel-1][1]=copysel1[1]
                        self.events[sel-1][2]=copysel[2]-copysel[0]+self.events[sel-1][0]
                        self.events[sel-1][3]=copysel[3]-copysel[1]+self.events[sel-1][1]
                        if self.events[sel-1][3]<0:
                            self.events[sel-1][2]-=1
                            self.events[sel-1][3]= self.events[sel-1][3] % 60
                        #setting hour for the missed event
                        self.events[sel][0]=self.events[sel-1][2]
                        self.events[sel][1]=self.events[sel-1][3]
                        self.events[sel][2]=copysel1[2]-copysel1[0]+self.events[sel][0]
                        self.events[sel][3]=copysel1[3]-copysel1[1]+self.events[sel][1]
                        if self.events[sel][3]<0:
                            self.events[sel][2]-=1
                            self.events[sel][3]= self.events[sel][3] % 60
                        selected-=1
                    else:
                        if self.events[sel][1]+time<=0:
                            self.events[sel][1]=60+time+self.events[sel][1]
                            self.events[sel][0]-=1
                            if self.events[sel][3]+time<0:
                                self.events[sel][3]=60+time+self.events[sel][3]
                                self.events[sel][2]-=1
                                return 0
                            self.events[sel][3]+=time
                            return 0
                        if self.events[sel][3]+time<0:
                            self.events[sel][3]=60+time+self.events[sel][3]
                            self.events[sel][2]-=1
                            self.events[sel][1]+=time
                            return 0
                        self.events[sel][1]+=time
                        self.events[sel][3]+=time
                        return 0

            
            #for drawAdjust()
            elif self.mode==3:
                self.anychange=1
                if self.selected not in self.savelist:
                    self.savelist+=[self.selected]
                if self.start:
                    if (time > 0):
                        if (self.hstop*60<=self.events[sel][2]*60+self.events[sel][3]+time):
                            time=self.hstop*60-self.events[sel][2]*60-self.events[sel][3]
                        if sel==len(self.events)-1:
                            if self.events[sel][3]+time>=60:
                                self.events[sel][2]+=1
                                self.events[sel][3]=self.events[sel][3]+time-60
                                return 0
                            self.events[sel][3]+=time
                            return 0
                        elif (self.events[sel + 1][0]*60+self.events[sel+1][1]-self.events[sel][2]*60-self.events[sel][3]<time):
                            #Co jesli nastepne zdarzenie stanie sie zbyt krotkie?
                            if self.selected+1 not in self.savelist:
                                self.savelist+=[(self.selected+1)]
                            if (self.events[sel+1][2]*60+self.events[sel+1][3]-self.events[sel+1][0]*60-self.events[sel+1][1]<=time):
                                self.delEvent(sel+1)
                                return 0
                            if self.events[sel+1][1]+time>=60:
                                self.events[sel+1][0]+=1
                                self.events[sel+1][1]=self.events[sel+1][1]+time-60
                                self.events[sel][2]=self.events[sel+1][0]
                                self.events[sel][3]=self.events[sel+1][1]
                            else:
                                self.events[sel+1][1]+=time
                                self.events[sel][2]=self.events[sel+1][0]
                                self.events[sel][3]=self.events[sel+1][1]
                            return 0
                        if self.events[sel][3]+time>=60:
                            self.events[sel][2]+=1
                            self.events[sel][3]=self.events[sel][3]+time-60
                            return 0
                    #events[sel][2]+=time
                    elif (time < 0):
                        if ((self.events[sel][2]*60+self.events[sel][3]-self.events[sel][0]*60-self.events[sel][1])<=-time):
                            self.delEvent(sel)
                            if self.events==[]:
                                self.events=[[]]
                                self.selection=0
                                self.mode=0
                                self.drawRectangle(self.selection)
                            return 0
                        elif self.events[sel][3]+time<0:
                            self.events[sel][3]=60+time+self.events[sel][3]
                            self.events[sel][2]-=1
                            return 0
                    self.events[sel][3]+=time
                else:
                    if (time < 0):
                        if (self.hstart*60>=self.events[sel][0]*60+self.events[sel][1]+time):
                            time=self.hstart*60-self.events[sel][0]*60-self.events[sel][1]
                        if sel==0:
                            if (self.events[sel][1]+time<0):
                                self.events[sel][0]-=1
                                self.events[sel][1]=60+time+self.events[sel][1]
                                return 0
                            self.events[sel][1]+=time
                            return 0
                        
                        if (self.events[sel][0]*60+self.events[sel][1]-self.events[sel-1][2]*60-self.events[sel-1][3]<-time):
                            if (self.selected-1) not in self.savelist:
                                self.savelist+=[(self.selected-1)]
                            if (self.events[sel-1][2]*60+self.events[sel-1][3]-self.events[sel-1][0]*60-self.events[sel-1][1]<=-time):
                                self.delEvent(sel-1)
                                self.selected-=1
                                self.draw(self.events)
                                self.drawAdjust()
                                return 0
                            elif self.events[sel-1][3]+time<0:
                                self.events[sel-1][2]-=1
                                self.events[sel-1][3]=60+time+self.events[sel-1][3]
                                self.events[sel][0]=self.events[sel-1][2]
                                self.events[sel][1]=self.events[sel-1][3]
                                return 0
                            self.events[sel-1][3]+=time
                            self.events[sel][0]=self.events[sel-1][2]
                            self.events[sel][1]=self.events[sel-1][3]
                            return 0
                        else:
                            if self.events[sel][1]+time<0:
                                self.events[sel][0]-=1
                                self.events[sel][1]=60+time+self.events[sel][1]
                                return 0
                    elif (time>0):
                        if (self.events[sel][2]*60+self.events[sel][3]-self.events[sel][0]*60-self.events[sel][1]-time<=0):
                            self.delEvent(sel)
                            if self.events==[]:
                                self.events=[[]]
                                self.selection=0
                                self.mode=0
                                self.drawRectangle(self.selection)
                            return 0
                        elif self.events[sel][1]+time>=60:
                            self.events[sel][1]=self.events[sel][1]+time-60
                            self.events[sel][0]+=1
                            return 0
                    self.events[sel][1]+=time

        elif self.inHand==1:
            return 0
        #for drawHline()
        elif self.inHand==2:
            if self.hline+time<vhstart*60:
                self.hline=self.hstart*60
            elif self.hline+time>self.hstop*60:
                self.hline=self.hstop*60
            else:
                self.hline+=time
        #self.Highlight()
    
    
    def checkColisions(self):
        freespace=[]
        var=[self.eventCopy[0],self.eventCopy[1]]
        begining=self.eventCopy[0]*60 + self.eventCopy[1]
        end=self.eventCopy[2]*60 + self.eventCopy[3]
        if self.events==[[]]:
            freespace=[[self.hstart,0,self.hstop,0]]
            return freespace
        for i in self.events:
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
            freespace.extend([[var[0],var[1],self.eventCopy[2],self.eventCopy[3]]])
        return freespace
            
    def handleRedraw(self,rect):
        if self.img: self.canvas.blit(self.img)
    
    def menuUp(self):
        self.menu=0
        self.redrawGUI() 
        choices = [u"Custom Event", u"Reminder", u"Anniversary", u"Message"]
        index = appuifw2.popup_menu(choices, u"Select:") 
        if index == 0 : 
            self.newEvent()
        elif index == 1 :
            appuifw2.note(u"Choose time for the reminder")
            self.selected=0
            
            self.inHand=-1
            if self.viewday<=time.time() and time.time()<=self.viewday+3600*24:
                hline=(time.time()-self.viewday)/60+30
            else:
                hline=((self.hstop-self.hstart)/2+self.hstart)*60
            self.draw(self.events)
            self.drawHLine()
            self.drawSms()
            self.handleRedraw(None)
        elif index == 2: 
            appuifw2.note(u"Choose a day for which the anniversary should be added")
            self.selected=0
            self.draw(self.events)
            self.inHand=0
        elif index == 3:
            self.selected=0
            self.inHand=-1
            m=1
            if self.viewday<=time.time() and time.time()<=self.viewday+3600*24:
                hline=(time.time()-self.viewday)/60+30
            else:
                hline=((self.hstop-self.hstart)/2+self.hstart)*60
            self.draw(self.events)
            self.drawHLine()
            self.handleRedraw(None)
        return 0
    def menuLeft(self):
        pass
    def menuRight(self):
        pass
    def menuMiddle(self):
        self.menu=0
        choices = [u"This Event",u"reminderser",u"Anniversary", u"Message"]
        self.gradient()
        self.draw(self.events)
        self.drawRectangle(self.events)
        self.drawSms()
        self.drawSignal()
        self.handleRedraw(None)
        index = appuifw2.popup_menu(choices, u"Select:")
        if index == 0:
            self.quickEdit()
        if index == 1:
            rnames=[]
            if self.reminders!=[]:
                for i in self.reminders:
                    rnames.extend([unicode(str(i[0])+ ":" + str(i[1]) +" "+ i[2])])
                c1 = appuifw2.popup_menu(rnames,u"reminderser:")
                if c1!=None:
                    a=calendar.open()
                    a.__delitem__(self.reminders[c1][-1])
                    hline=self.reminders[c1][0]*60+self.reminders[c1][1]
                    self.selected=-1
                    self.remindersinfo=unicode(self.reminders[c1][2])
                    del self.reminders[c1]
                    self.drawSms()
                    self.selected=0
                    self.inHand=-1
                    self.drawSms()
                    self.drawHLine()
                    self.handleRedraw(None)
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
                    inHand=-1
                    drawSms()
                    drawHLine()
                    handleRedraw(None)
        elif index == 2: 
            if anniversaries!=[]:
                names=[]
                for i in anniversaries:
                    names.extend([i[0]])
                c1 = appuifw2.popup_menu(names,u"Anniversary:")
                if c1!=None:
                    inHand=0
                    appuifw2.note(u"Choose the day")
                    anniversariesinfo=unicode(anniversaries[c1][0])
                    a=calendar.open()
                    a.__delitem__(int(anniversaries[c1][1]))
                    del anniversaries[c1]
                    draw(self.events)
                    drawSms()
                    handleRedraw(None)
        return 0
    def menuDown(self):
        self.menu=0
        self.redrawGUI()   
        if self.alarm:
            label=u"Turn Auto add alarm OFF"
        else:
            label=u"Turn Auto add alarm ON"
        
        menua=[u"Wake-sleep hours", u"Categories colors", u"Font", label, u"App info",u"Standby screen", u"Update",u"Exit"]
        
        cc=appuifw2.popup_menu(menua,u"")
        if cc==0:
            self.setHours()
        elif cc==1:
            self.catconfig()
        elif cc==2:
            self.changeFont()
        elif cc==3:
            self.alarm = not self.alarm
        elif cc==4:
            menub=[u"Authors blog",u"Shortcut keys",u"Version info"]
            cd=appuifw2.popup_menu(menub,u"Info")
            if cd==0:
                self.website()
            elif cd==1:
                self.shortcuts()
            elif cd==2:
                self.version()
        elif cc==5:
            self.screenObj=DrawStandby()
            self.onstandby=True
            self.drawOnStandby()
            
        elif cc==6:
            self.update()
        elif cc==7:
            self.quit()
        return 0
    def quickEdit(self):
        b=calendar.open()
        alarminfo=None
        try:
            d=b.__getitem__(events[selected][-1])
            d.begin()
            alarminfo=d.alarm
        except:
            appuifw2.note(u"Error building menu")
        if alarminfo==None:
            label=u"Turn Alarm ON"
        else:
            label=u"Turn Alarm OFF"
        
        b=appuifw2.popup_menu([u"Name",u"Category",u"Repeat rules",u"Color",label,u"More"], u"Edit " + self.events[self.selected][4])
        if b==0:
            c=appuifw2.query(u"Name", 'text',unicode(self.events[self.selected][4]))
            if c != self.events[self.selected][4] and c!=None:
                self.events[self.selected][4]=c
                b=calendar.open()
                d=b.__getitem__(self.events[self.selected][-1])
                d.begin()
                if d.get_repeat()!=None:
                    choices = [u"This only",u"Future", u"All"]
                    index = appuifw2.popup_menu(choices, u"Save on:")
                    if index==0:
                        #Make the old event end at the start day of the new one
                        zz=d.get_repeat()
                        if zz!=None:
                            zz['exceptions']=list(zz['exceptions']) + [self.viewday+3600]
                        d.set_repeat(zz)
                        d.commit()
                        #Make a new shit
                        d=b.add_appointment()
                        d.content=events[selected][4]
                        d.location=events[selected][5]
                        d.set_time(self.viewday+self.events[self.selected][0]*3600+self.events[self.selected][1]*60,self.viewday+self.events[self.selected][2]*3600+self.events[self.selected][3]*60)
                        d.priority=self.events[self.selected][6]
                        if alarminfo!=None:
                            d.alarm=self.viewday+self.events[self.selected][0]*3600+self.events[self.selected][1]*60
                        else:
                            d.alarm=None
                        d.commit()
                    elif index==1:
                        #Make the old event end at the start day of the new one
                        zz=d.get_repeat()
                        zzz=dict(zz)
                        #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                        zz['end']=self.viewday-2*(24*3600)
                        d.set_repeat(zz)
                        d.commit()
                        #Make a new shit
                        d=b.add_appointment()
                        d.content=self.events[self.selected][4]
                        d.location=self.events[self.selected][5]
                        d.set_time(self.viewday+self.events[self.selected][0]*3600+self.events[self.selected][1]*60,self.viewday+self.events[self.selected][2]*3600+self.events[self.selected][3]*60)
                        d.priority=self.events[self.selected][6]
                        if alarminfo!=None:
                            d.alarm=self.viewday+self.events[self.selected][0]*3600+self.events[self.selected][1]*60
                        else:
                            d.alarm=None
                        zzz['start']=viewday
                        d.set_repeat(zzz)
                        d.commit()
                    elif index==2:
                        #Make the old event end at the start day of the new one
                        d.content=self.events[self.selected][4]
                        d.commit()
                d.content=self.events[self.selected][4]
                d.commit()
                self.draw(self.events)
                self.drawRectangle(self.events)
        elif b==1:
            a=[]
            for i in ideacat:
                a.extend([i[0]])
            d=appuifw2.popup_menu(a, events[selected][4] + u" category")
            if d!= self.events[self.selected][5] and d!=None:
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
                        d.set_time(self.viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                        d.priority=events[selected][6]
                        if alarminfo!=None:
                            d.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            d.alarm=None
                        d.commit()
                    elif index==1:
                        #Make the old event end at the start day of the new one
                        
                        zz=d.get_repeat()
                        zzz=dict(zz)
                        #Huj ze dwa dni do tylu zamiast jednego ale to DZIALA!
                        zz['end']=self.viewday-2*(24*3600)
                        d.set_repeat(zz)
                        d.commit()
                        #Make a new shit
                        d=b.add_appointment()
                        d.content=self.events[self.selected][4]
                        d.location=events[selected][5]
                        d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                        d.priority=events[selected][6]
                        if alarminfo!=None:
                            d.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            d.alarm=None
                        zzz['start']=viewday
                        d.set_repeat(zzz)
                        d.commit()
                    elif index==2:
                        #Make the old event end at the start day of the new one
                        
                        d.location=events[selected][5]
                        d.commit()
                d.location=events[selected][5]
                d.commit()
                draw(self.events)
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
                        c.content=events[selected][4]
                        c.location=events[selected][5]
                        c.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                        
                        c.priority=events[selected][6]
                        if alarminfo!=None:
                            c.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
                        else:
                            c.alarm=None
                        c.set_repeat(builded)
                        c.commit()
                        return 0
                    elif index==1:
                        #Make the old event end at the start day of the new one
                        c.begin()
                        c.set_time(c.start_time,c.end_time)
                        c.priority=events[selected][6]
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
                        c.priority=events[selected][6]
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
                        c.content=events[selected][4]
                        c.location=events[selected][5]
                        c.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                        c.priority=events[selected][6]
                        if alarminfo!=None:
                            c.alarm=viewday+events[selected][0]*3600+events[selected][1]*60
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
                    ideacat[int(events[selected][5])][1]=acolors[d]
                except:
                    appuifw2.note(u"Can't change color. Event doesn't belong to any category!")
        elif b==4:
            if alarminfo == None:
                alarminfo=viewday+events[selected][0]*3600+events[selected][1]*60
            else:
                alarminfo=None
                
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
                    d.priority=events[selected][6]
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
                    d.content=events[selected][4]
                    d.location=events[selected][5]
                    d.set_time(viewday+events[selected][0]*3600+events[selected][1]*60,viewday+events[selected][2]*3600+events[selected][3]*60)
                    d.priority=events[selected][6]
                    d.alarm=alarminfo
                    zzz['start']=viewday
                    d.set_repeat(zzz)
                    d.commit()
                    return 0
                elif index==2:
                    #Make the old event end at the start day of the new one
                    d.priority=events[selected][6]
                    d.alarm=alarminfo
                    d.commit()
                    draw(self.events)
                    drawRectangle(events)
                    return 0
            d.alarm=alarminfo
            d.commit()
            draw(self.events)
            drawRectangle(events)
        elif b==5:
            editEvent()
    
    def redrawGUI(self):
        self.gradient()
        self.draw(self.events)
        self.drawSms()
        self.drawSignal()
        self.handleRedraw(None)
    
    def saveEvent(self,where,event):
        b=calendar.open()
        c=b.add_appointment()
        c.content=event[4]
        c.location=event[5]
        c.set_time(self.viewday+where[0]*3600+where[1]*60,self.viewday+where[2]*3600+where[3]*60)
        if not alarm:
            noyes=appuifw2.query( u"Set Alarm ?","query")
            if noyes:
                c.priority=3
                c.alarm=self.viewday+int(where[0])*3600+int(where[1])*60
            else:
                c.priority=2
        else:
            c.priority=3
            c.alarm=self.viewday+int(where[0])*3600+int(where[1])*60
        c.commit()
        forwatch()
        return c.id
    
    #Highlight the proper
    def Highlight(self):
        if self.inHand==0:
            if self.mode==0:
                self.drawRectangle(self.events)
            elif self.mode==1:
                self.drawHalf()
            elif self.mode==2:
                self.drawOutline()
            elif self.mode==3:
                self.drawAdjust()
        elif self.inHand==1:
            pass
        elif self.inHand==2:
            self.drawHLine()
            
    def handleEvent(self,event):
        ev = event['keycode']
        pi = event['scancode']
        
        #If someone pressed pencil button
        if pi == key_codes.EScancodeEdit:
            if self.inHand==0:
                if self.mode==0:
                    try:
                        if self.events[self.selected]==[]:
                            appuifw2.note(u"Nothing to edit!")
                            return 0
                    except:
                        pass
                    self.mode=1
                    #Copy current event
                    self.eventCopy=list(self.events[self.selected])
                    del self.events[self.selected]
                    self.otherday=self.viewday
                    self.gradient()
                    self.draw(self.events)
                    self.drawHalf()
        
        #Jump to date
        elif ev == key_codes.EKey1:
            if (self.mode==0 or self.mode==1):
                a=appuifw2.query(u"Go to:", 'date', self.viewday)
                if self.viewday!=a and a!=None:
                    self.weekday+=int((a-self.viewday)/86400)
                    self.weekday=self.weekday%7
                    self.viewday=a
                    self.prepare(self.viewday)
                    self.gradient()
                    self.draw(self.events)
                    self.drawSms()
                    if self.inHand==0:
                        if self.mode==0:
                            self.drawRectangle(events)
                        elif self.mode==1:
                            self.anychange = 1
                            self.drawHalf()
                    elif self.inHand==1:
                        pass
                    elif self.inHand==2:
                        self.drawHLine()
                    
                    
        #Up arrow was pressed
        elif ev == key_codes.EKeyUpArrow:
            if self.menu:
                self.menuUp()
            self.move(-30, self.selected, self.start)
    
        elif ev == key_codes.EKeyDownArrow:
            if self.menu:
                self.menuDown()
            self.move(30, self.selected, self.start)

        #SUPER SCROLL UP
        elif ev == key_codes.EKey2:
            if self.menu:
                self.menuUp()
            self.move(-60, self.selected, self.start)

        #SUPER SCROLL DOWN
        elif ev == key_codes.EKey0:
            if self.menu:
                self.menuUp()
            self.move(60, self.selected, self.start)
            
        #GENTLE SCROLL UP
        elif ev == key_codes.EKey5:
            if self.menu:
                self.menuUp()
            self.move(-5, self.selected, self.start)
        
        #GENTLE SCROLL DOWN
        elif ev == key_codes.EKey8:
            if self.menu:
                self.menuUp()
            self.move(5, self.selected, self.start)

        #Middle Button
        elif ev == key_codes.EKeySelect:
            if self.menu:
                self.menuMiddle()

            elif self.inHand==0:
                if self.mode==0 and self.events[self.selected]!=[]:
                    try:
                        del ideabox
                    except:
                        pass
                    theid=self.events[self.selected][-1]
                    for i in range(1,len(base)):
                        if theid in base[i][0]:
                            ideabox=Ideabox(index=i)
                            return 0
                    b=appuifw2.popup_menu([u"Connect with Idealist",u"New Idealist"],u"Choose")
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
                        self.savebase()
                    self.loadbase()
                
                elif self.mode==1:
                    if self.anychange:
                        colisions = self.checkColisions()
                        if len(colisions)==1 and (self.eventCopy[2]*60+self.eventCopy[3]-self.eventCopy[0]*60-self.eventCopy[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
                            self.events.extend([self.eventCopy])
                            self.overwrite(-1)
                        elif len(colisions)==0:
                            #IN FUTURE MAKE IT POSIBLE TO ADD IT HERE AFTER A WARNING BY SPLITING UP OTHERS AND ADDING THEM TO IDEABOX
                            appuifw2.note(u"You can't add it here!")
                        else:
                            choices = [u"Use biggest",u"Use all ava. space"]
                            index = appuifw2.popup_menu(choices, u"What to do?:")
                            if index == 0:
                                much=0
                                where=0
                                for i in colisions:
                                    if (i[2]*60+i[3]-i[0]*60-i[1])>much:
                                        where=i
                                        much=i[2]*60+i[3]-i[0]*60-i[1]
                                self.saveEvent(where,self.eventCopy)
                                
                            elif index == 1:
                                a=calendar.open()
                                a.__delitem__(self.eventCopy[-1])
                                much=0
                                for i in colisions:
                                   self.saveEvent(i,self.eventCopy)
                                   much+=i[2]*60+i[3]-i[0]*60-i[1]
                                if much<(self.eventCopy[2]*60+self.eventCopy[3]-self.eventCopy[0]*60-self.eventCopy[1]):
                                    pass
                        self.anychange=0
                        if self.otherday == self.viewday:
                            del self.events[self.selected]
                        self.prepare(self.viewday)
                        self.mode=0
                        self.redrawGUI()
                    
                    elif self.otherday==self.viewday:                      
                        self.prepare(self.viewday)
                        self.mode=2
                        self.gradient()
                        self.draw(self.events)
                        self.drawOutline()
                        self.handleRedraw(None)
                elif self.mode==2:
                    self.mode=3
                    self.gradient()
                    self.draw(self.events)
                    self.drawAdjust()
                    self.handleRedraw(None)
                    

                    
                    
            elif self.inHand==2:
                if self.eventsSpace==[]:
                    appuifw2.note(u"There's nothing to choose from at this day")
                    self.inHand=1
                else:
                    self.checkAdd()
            elif self.inHand==1:
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
                        newAnniversary(u"" + showpeople[b])
                    anniversariesinfo=u""
                elif a==1:
                    newAnniversary()
                return 0
            elif self.inHand==-1:
                if m:
                    self.newMessage()
                    m=0
                else:
                    self.newReminder()
                    
            elif self.mode ==2:
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
                    draw(self.events)
                    drawRectangle(events)
                    handleRedraw(None)
                    return 0
                gradient()
                mode =3
                drawSignal()
                draw(self.events)
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
                    draw(self.events)
                    drawRectangle(events)
                    handleRedraw(None)
                    return 0
                mode=0
                gradient()
                drawSignal()
                draw(self.events)
                drawRectangle(events)
                handleRedraw(None)
            else:
                try:
                    if events[selected]==[] and mode!=1:
                        appuifw2.note(u"Nothing to edit!")
                        return 0
                except:
                    pass
    
        
        
        #Left arrow handler
        elif ev == key_codes.EKeyLeftArrow:
            
            if self.menu:
                self.menu=0
                #Menu left (idealist)
                return 0

            elif self.inHand==0 or self.inHand==1 or self.inHand==2:
                if self.mode==0 or self.mode==1:
                    self.viewday-=3600*24
                    self.weekday-=1
                    self.weekday=self.weekday%7
                    self.prepare(self.viewday)
                    self.selected=0
                    self.redrawGUI()
                    self.Highlight()

                
        #Right arrow handler
        elif ev == key_codes.EKeyRightArrow:
            
            if self.menu:
                self.menu=0
                #Menu right
                return 0
            
            elif self.inHand==0 or self.inHand==1 or self.inHand==2:
                if self.mode==0 or self.mode==1:
                    self.viewday+=3600*24
                    self.weekday+=1
                    self.weekday=self.weekday%7
                    self.prepare(self.viewday)
                    self.selected=0
                    self.redrawGUI()
                    self.Highlight()
                
        
        elif ev== key_codes.EKeyYes and self.inHand==0 and self.mode==0:
            self.quickEdit()
        
        #Deletes an event from the calendar
        elif ev == key_codes.EKeyBackspace and self.inHand==0 and self.mode==0:
            self.delEvent(self.selected)
            if self.events==[]:
                self.events=[[]]
                self.selected=0
            self.redrawGUI()
            self.Highlight()
        
        
    def eventsSpace(events):
        #Checking if day is totaly free
        if self.events==[[]]:
            #If time now is below the time schedule
            if time.time()-self.hstart*3600<self.viewday:
                self.eventsSpace=[[self.hstart,0,self.hstop,0,unicode(str((self.hstop-self.hstart)*60)), u" minutes", 0, (self.hstop-self.hstart)*60]]
            #When time is somewhere in the middle
            else:
                self.eventsSpace=[[int((time.time()-self.viewday)/3600),int(((time.time()-self.viewday)%3600)/60),self.hstop,0,unicode(int((self.hstop*3600-time.time()+self.viewday)/60+((time.time()-self.viewday)%3600)/60)), u" minutes", 0, int((self.hstop*3600-time.time()+self.viewday)/60+((time.time()-self.viewday)%3600)/60)]]
        else:
            self.eventsSpace=[]
            varr=[self.hstart,0]
            #Usual, unempty day
            #A loop over all events in the prepare() day
            for i in self.events:
                #If time is below the timetable current loop event
                if (time.time()<=(self.viewday+ i[0]*3600 + i[1]*60)):
                    #If it's below the previous event end
                    if (time.time() <= (self.viewday+ varr[0]*3600 + varr[1]*60)):
                        dif=i[1]+(i[0]*60)-varr[0]*60-varr[1]
                        if (dif>0):
                            self.eventsSpace.extend([[varr[0],varr[1],i[0],i[1],unicode(str(dif)),u" minutes",i[-1],dif]])
                    #And if it's not
                    else:
                        self.eventsSpace=[[int((time.time()-self.viewday)/3600),int(((time.time()-self.viewday)%3600)/60),i[0],i[1],unicode(int((self.viewday+i[0]*3600+i[1]*60-time.time())/60)), u" minutes", i[-1], int((self.viewday+i[0]*3600+i[1]*60-time.time())/60)]]
                varr=[i[2],i[3]]
            #If time is smaller than last event end time (the absence of = makes it imposible to insert something on hstop hour)
            if (time.time()<self.viewday+varr[0]*3600+varr[1]*60):
                self.eventsSpace.extend([[varr[0],varr[1],self.hstop,0, unicode(self.hstop*60-varr[0]*60-varr[1]),u" minutes",0,self.hstop*60-varr[0]*60-varr[1]]])
            #If it's between the last event ending and the hstop hour
            elif (time.time()<self.viewday+self.hstop*3600):
                self.eventsSpace.extend([[int((time.time()-self.viewday)/3600),int(((time.time()-self.viewday)%3600))/60,self.hstop,0, unicode(int(self.hstop*3600-time.time()+self.viewday)/60),u" minutes",0,int(self.hstop*3600-time.time()+self.viewday)/60]])
    
    
    def forwatch(self):
        #check this
        try:
            b=calendar.open()
        except():
            exit()
        c=b.daily_instances(self.currentday, appointments=1, events=0, anniversaries=0,todos=0)
        d=[]
        self.wlist=[]
        for i in c:
            d.append(i.values()[0])
        for k in d:
            z=b.__getitem__(k)
            if z.end_time>time.time():
                self.wlist.extend([[z.start_time,z.end_time,z.content,z.location,z.priority,z.id]])
    

    def drawOnStandby():
        global screenObj, onstandby
        #t = e32.Ao_timer()
        while(onstandby):
            e32.ao_sleep(0.1)
            e32.ao_yield()
            current=appswitch.application_list(1)[0]
            if (current=="Standby mode"):
                screenObj.show()
            else:
                screenObj.hide()
                
    def watchout(self):
        while(0):
            e32.ao_sleep(30)
            e32.ao_yield()
            if self.currentday+24*3600<=time.time():
                self.currentday+=24*3600*math.floor((time.time()-self.currentday)/(24*3600))
                self.forwatch()
                
            elif self.currentday>=time.time():
                self.currentday+=24*3600*math.floor((time.time()-self.currentday)/(24*3600))
                self.forwatch()
            
            
            if self.smslist!=[]:
                if int(self.smslist[0][0]/60)==int(time.time()/60):
                    messaging.sms_send(self.smslist[0][1],self.smslist[0][2])
                    del self.smslist[0]
                    self.smslist.sort()
                    pickle.dump(self.smslist,open('C:\\idealist\\smses.txt','w'))
                if self.smslist[0][0]<time.time():
                    del self.smslist[0]
                    self.smslist.sort()
                    pickle.dump(self.smslist,open('C:\\idealist\\smses.txt','w'))
            try:
                #globalui.global_note(unicode(str(wlist[0])))
                if self.wlist!=[] and int(self.wlist[0][1]/60)==int(time.time()/60) and (int(self.wlist[0][4])%2==1):
                    xprofile.set_ap(0)
                    del self.wlist[0]
                if self.wlist!=[] and int(self.wlist[0][0]/60)==int(time.time()/60) and (int(self.wlist[0][4])%2==1):
                    xprofile.set_ap(1)
                
            except:
                pass
            
            #This lines display a new message when it comes
            unreadsms=0
            if self.inboxx.unread(self.inboxx.sms_messages()[0])<>0:
                unreadsms=1
            #Displays missed calls
            l=logs.calls(mode='missed')  #The dictionary for the latest missed call
            self.missedcalls=0
            if len(l)>0 and l[0]["flags"]==0:
                self.missedcalls=1
            else:
                self.missedcalls=0
            del l
            self.xprof=xprofile.get_ap()[0]
            
            self.draw(self.events)
            self.drawSignal()
            if self.menu:
                self.mainMenu()
            elif self.mode==1:
                self.drawHalf()
            elif self.mode==2:
                self.drawOutline()
            elif self.mode==3:
                self.drawAdjust()
            elif self.inHand==-1:
                self.drawHLine()
            else:
                self.drawRectangle(self.events)
            
            
            
            self.handleRedraw(None)
            
        
    def gradient(self):
        z=(self.h-self.newh-self.endh)*1./100
        anglehour=(2*math.pi*((time.time()-self.currentday)/3600)/24)
        coshour=math.cos(anglehour)
        for i in range(0,100):
            self.img.rectangle((12,int(i*z+self.newh),self.w,int((i+1)*z+self.newh)), fill=(20,int(-25*coshour+(160-i)),int(-25*coshour+(175-i))))
    
    def quit(self):

        if self.menu:
            self.menu=0
            self.gradient()
            self.draw(self.events)
            self.drawRectangle(events)
            self.drawSms()
            self.drawSignal()
            self.handleRedraw(None)
            return 0
        self.savebase()
        
        if appuifw2.app.screen=='normal':
            appuifw2.app.left_navi_arrow=False
            appuifw2.app.right_navi_arrow=False
            appuifw2.app.menu_key_handler=None
            appuifw2.app.navi_text=u''
            appuifw2.app.menu_key_text=u'Options'
            #appuifw2.app.screen = 'full'
            self.buildCanvas()
            appuifw2.app.body = canvas
            #gradient()
            
            #draw(self.events)
            #drawSms()
            #drawSignal()
            self.drawRectangle(events)
            self.handleRedraw(None)
        elif eself.xploremode == 2 or self.inHand==-1:
            self.inHand =1
            self.prepare(viewday)
            self.gradient()
            self.draw(self.events)
            self.drawRectangle(events)
            self.drawSms()
            self.drawSignal()
            self.handleRedraw(None)
        elif self.inHand==0:
            self.inHand =1
            appuifw2.note(u"Anniversery deleted.")
            self.prepare(viewday)
            self.gradient()
            self.draw(self.events)
            self.drawRectangle(events)
            self.drawSms()
            self.drawSignal()
            self.handleRedraw(None)
        elif (self.mode==1 or self.mode == 2 or self.mode==3):
            self.mode=0
            self.prepare(viewday)
            self.gradient()
            self.draw(self.events)
            self.drawRectangle(events)
            self.drawSms()
            self.drawSignal()
            self.handleRedraw(None)
            self.anychange=0
        else:
            try:
                self.saveConfig()
            except:
                appuifw2.note(u"Error saving config file")
            del inboxx
            
    
    
    
    def vadjustrefresh(self):
        
        self.vadjust=(self.h-self.newh-self.endh)/(self.hstop-self.hstart)
    
    
    
    def resizeCanvas(self,rect):
        
        if not self.canvas: return
    
        # Initialize drawing coordinate
        if self.img: del self.img
        self.img = graphics.Image.new(self.canvas.size, mode='RGB')
        self.w, self.h = self.canvas.size
        try:
            self.vadjustrefresh()
            self.gradient()
            self.draw(self.events)
            self.drawSms()
            self.drawSignal()
        except:
            pass
        
    
    def predraw(self):
        #optimazed 8.2.2009
        self.canvas = appuifw2.Canvas(\
                      redraw_callback = self.handleRedraw,\
                      event_callback = self.handleEvent,
                      resize_callback= self.resizeCanvas)
        appuifw2.app.body = self.canvas
        appuifw2.app.screen = 'full'
        appuifw2.app.title = u"IdeaList"
    
    
    
    def changeFont():
        global currentfont, events
        fonty=appuifw2.available_fonts()
        del fonty[-1]
        a=appuifw2.popup_menu(fonty,u"Choose a font")
        if a!=None:
            currentfont=fonty[a]
            draw(self.events)
            drawRectangle(events)
            
    def setHours(self):
        
        a=appuifw2.query(u"Wake-up hour","time",float(self.dhstart*3600))
        b=appuifw2.query(u"Go to sleep hour", "time", float(self.dhstop*3600))
        if a!=None and b!=None:
            self.hstart=self.dhstart=int(a/3600)
            self.hstop=self.dhstop=int(b/3600)
            self.vadjustrefresh()
            self.gradient()
            self.draw(self.events)
            self.drawSms()
    
    def website(self):
        e32.start_exe('BrowserNG.exe', ' "4 http://www.masteranza.wordpress.com/ 1"', 1)
    
    def catconfig(self):
        appuifw2.app.screen='normal'
        b=[]
        for i in self.ideacat:
            b.extend([unicode(i[0]+": "+str(i[1]))])
        a=appuifw2.selection_list(b)
        if a!=None:
            colors=[(200,70,70),(70,200,70),(70,70,200),(200,200,70),(70,200,200),(200,70,200),(70,70,70)]
            d = appuifw2.popup_menu([u"Red",u"Green",u"Blue",u"Yellow",u"Sea",u"Violet",u"Black"], u"Choose:")
            if d!=None:
                self.ideacat[a][1]=colors[d]
            self.catconfig()
        appuifw2.app.screen='full'
        
    def mainMenu(self):
        self.img.polygon((40,self.h/2,self.w/2,self.h/2-self.w/2+40,self.w-40,self.h/2,self.w/2,self.h/2+self.w/2-40),fill=(0,0,0), outline=(200,200,200), width=4)
        self.img.rectangle((20+self.w/4,self.h/2-self.w/4+20,self.w-20-self.w/4,self.h/2+self.w/4-20),outline=(200,200,200), width=4)
        self.img.text((self.w/2-12,self.h/2+5),u"Edit",fill=(255,255,255), font=self.currentfont)
        self.img.text((self.w/2-10,self.h/2-self.w/4+10),u"New",fill=(255,255,255), font=self.currentfont)
        self.img.text((self.w/4-4,self.h/2+5),u"List",fill=(255,255,255), font=self.currentfont)
        self.img.text((self.w-10-self.w/4,self.h/2+5),u"Box",fill=(255,255,255), font=self.currentfont)
        self.img.text((self.w/2-20,self.h/2+self.w/4-5),u"Settings",fill=(255,255,255), font=self.currentfont)
        self.menu=1
        self.handleRedraw(None)
    
    def version(self):
        appuifw2.note(u"Idealist 1.0\nby Ranza's Research",'info')
    def shortcuts(self):
        shortk=appuifw2.Text(text=u"Green Key - Quick Edit\nPencil Key - Enter Edit mode\nStar Key - Zoom in\nHash key - Zoom out\n1 - Jump to date\n2 - New Event\n3 - New Idea\n4 - Opens IdeaList\n5 - New reminderser\n6 - Opens Ideabox\n\nHowever if you're in edit mode the keys:\n2 & 0 - move selection quickly [30 min]\n5 & 8 - move selection slowly [1 min]")
        appuifw2.app.screen='normal'
        appuifw2.app.body=shortk
    
    def buildCanvas(self):
        appuifw2.app.menu_key_handler = self.mainMenu
        appuifw2.app.menu = None
        #appuifw2.app.exit_key_handler = self.quit
        self.w, self.h = self.canvas.size
        self.img = graphics.Image.new((self.canvas.size[0], self.canvas.size[1]), mode='RGB')
        try:
            self.selected=0
            self.redrawGUI()
        except:
            pass
        
    def draw(self,list):
        if self.events!=[[]]:
            for i in range(0,len(list)):
                #The height in pixels of an event
                #hsize=int((list[i][2]+(list[i][3]*1./60)-list[i][0]-(list[i][1]*1./60))*self.vadjust)/2
                #a rectangle height
                #difk=int(hsize/12)
                #how many blocks
                #if difk==0:
                #    difk=1
                #split=int(hsize/difk)+2
                #if split==0:
                #    split=2
                #color jump
                #cjump=int(70/split)
                #the start position
                cc=(list[i][0]+(list[i][1]*1./60)-self.hstart)*self.vadjust
                try:
                    clor=self.ideacat[int(list[i][5])][1]
                except:
                    clor=(70,70,70)
                #for j in range(0,split):
                #    clor=tuple(map(lambda x: x-cjump,clor))
                #    self.img.rectangle((12,int(cc+difk*j+self.newh),self.w+100,int(cc+difk*(j+1)+self.newh)),fill=clor)
                #if split==0:
                #    split=1
                self.img.rectangle((12,int(cc+self.newh),self.w,int((list[i][2]+(list[i][3]*1./60)-self.hstart)*self.vadjust+self.newh)),fill=clor)
                #self.img.rectangle((12,int(cc+hsize+difk+self.newh),self.w,int(cc+2*(hsize)+difk+self.newh)), fill=clor)
                #self.img.line((12,cc+self.newh,self.w,cc+self.newh), outline=(30,30,30), width=1)
                #self.img.line((12,cc+self.newh+2*(hsize)+difk,self.w,cc+self.newh+2*(hsize)+difk), outline=(30,30,30), width=1)
                #img.line((12,int(cc+split*difk+newh),w,int(cc+split*difk+newh)), outline=(100,100,100), width=1)
                category=list[i][5]
                
                try:
                    category=self.ideacat[int(category)][0]
                except:
                    category=str(list[i][5])
                
                #When the text should be displayed
                linecount=int((list[i][2]+list[i][3]*1./60-list[i][1]*1/60.-list[i][0])*self.vadjust/self.dish)
                zzz=1
                if linecount>=2:
                    zzz=0
                long_str=unicode(list[i][4] +" | " + category)
                lines = wrap_text_to_array(long_str, self.currentfont, self.w-41-zzz*29)
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
                    textpos=int((list[i][2]+list[i][3]*1./60-list[i][1]*1/60.-list[i][0])*self.vadjust-(len(lines)*self.dish))/2
                    if len(lines)>linecount:
                        textpos=1
                    if linecount>=2:
                        self.img.text((self.w-26,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(240,230,230))
                        self.img.text((self.w-26,cc+10+self.dish+self.newh+addy),unicode(time2 +":" + time3), font=self.currentfont , fill=(240,230,230))
                    else:
                        self.img.text((self.w-58,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(240,230,230))
                    for line in lines:
                        if linecount==0:
                            break
                        self.img.text((13,cc+10+textpos+self.newh+addy), line, font=self.currentfont,fill = (240,240,240))
                        addy+= self.dish
                        linecount-=1
                else:
                    try:
                        if int((list[i+1][0]+list[i+1][1]*1./60-list[i][3]*1/60.-list[i][2])*self.vadjust/self.dish)>0:
                            self.img.text((13,cc+10+self.newh), lines[0], font=self.currentfont,fill = (10,10,10))
                            self.img.text((15,cc+12+self.newh), lines[0], font=self.currentfont,fill = (10,10,10))
                            self.img.text((14,cc+11+self.newh), lines[0], font=self.currentfont,fill = (240,240,240))
                            
                            self.img.text((w-58,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(10,10,10))
                            self.img.text((w-58,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(240,230,230))
                    except:
                        self.img.text((13,cc+10+self.newh), lines[0], font=self.currentfont,fill = (10,10,10))
                        self.img.text((15,cc+12+self.newh), lines[0], font=self.currentfont,fill = (10,10,10))
                        self.img.text((14,cc+11+self.newh), lines[0], font=self.currentfont,fill = (240,240,240))
                        self.img.text((self.w-58,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(10,10,10))
                        self.img.text((self.w-58,cc+10+self.newh+addy),unicode(time0 +":" + time1+ "-" + time2 +":" + time3), font=self.currentfont , fill=(240,230,230))
        #current hour line
        self.img.line((11,self.newh+((time.time()-self.viewday)/3600-self.hstart)*self.vadjust,self.w,self.newh+((time.time()-self.viewday)/3600-self.hstart)*self.vadjust), (250,50,0),width=2)
        if self.inHand==1:
            self.img.rectangle((12,self.h-12,self.w,self.h),fill=(0,0,0))
            self.img.text((11,self.h),u"Choose day by pressing select",fill=(255,255,255))    
        
            
    def drawSms(self):
        #draws the hours line
        self.img.rectangle((0,1,12,self.h),fill=(0,0,0))
        for i in range(0,self.hstop-self.hstart+1):
            self.img.line((8,self.newh+i*self.vadjust,12,self.newh+i*self.vadjust),(250,250,250), width = 1)
            self.img.text((0,self.newh+i*self.vadjust), unicode(i+self.hstart),(200,200,200))
        #Draws remindersers icons
        if len(self.reminders) > 0:
            for y in self.reminders:
                self.img.line((10,(int(y[0])+(int(y[1])*1./60)-self.hstart)*self.vadjust+self.newh,13,(int(y[0])+(int(y[1])*1./60)-self.hstart)*self.vadjust+self.newh),outline = (250,250,250), width = 2)
                self.img.blit(self.bell, target=(0,(int(y[0])+(int(y[1])*1./60)-self.hstart)*self.vadjust+self.newh))
        #Draws Sms icons
        if len(self.smslist) > 0:
            for y in self.smslist:
                if (y[0]-self.viewday)>0 and (y[0]-self.viewday)<3600*24:
                    self.img.line((10,((y[0]-self.viewday)/3600-self.hstart)*self.vadjust+self.newh,16,((y[0]-self.viewday)/3600-self.hstart)*self.vadjust+self.newh),outline = (250,250,100), width = 2)
                    self.img.blit(self.message, target=(0,((y[0]-self.viewday)/3600-self.hstart)*self.vadjust+self.newh))
    
    def drawSignal(self):
        
        #Signal and battery lines, changing every minute
        self.img.rectangle((0,self.h-self.endh,self.w,self.h),fill=(0,0,0))
        self.img.line((0,0,self.w,0), outline=(0,0,0), width=1)
        try:
            self.img.line((self.w,0,int(self.w-self.w*1./2*sysinfo.battery()/100),0),outline=(int(255*(1-float(sysinfo.battery()/100))),int(255.*sysinfo.battery()/100),0),width=1)
            self.img.line((0,0,int(self.w*1./2*sysinfo.signal()/7),0),outline=(int(255*(1-float(sysinfo.signal()/7))),int(255.*(sysinfo.signal())/7),0),width=1)
        except:
            appuifw2.note(u"Can't draw the batery or signal status")
            
        all=u""
        self.img.rectangle((12,1,self.w,self.newh),fill=(0,0,0))
        if len(self.anniversaries) > 0:
            poss=0
            hehe=0
            for y in self.anniversaries:
                self.img.blit(self.present, target=(2+hehe,self.h-self.endh))
                hehe+=14
                self.img.text((2+hehe,self.h), unicode(y[0]), fill = (255,255,255))
                hehe+=len(unicode(y[0]))*6
        watched=int(self.currentday/(3600*24))
        hourr=str(int(((time.time()-self.currentday)/3600)))
        minutess=str(int(((time.time()-self.currentday)%3600)/60))
        hourr=int(hourr)%24
        hourr=str(hourr)
        if len(hourr)==1:
            hourr="0"+hourr
        minutess=int(minutess)%60
        minutess=str(minutess)
        if len(minutess)==1:
            minutess="0"+minutess
        self.img.text((self.w-30,self.h), unicode(hourr+":"+minutess), font=self.currentfont ,fill=(245,245,245))
        if self.missedcalls==1:
            self.img.blit(self.phone, target=(self.w-57,self.h-11))
        if self.unreadsms==1:
            self.img.blit(self.sms, target=(self.w-72,self.h-11))
        if self.xprof:
            self.img.blit(self.silence, target=(self.w-42,self.h-11))
        
        all=u" " + unicode(self.days[self.weekday])
        if int(-(self.currentday-self.viewday)/(3600*24))==0:
            all+=u" (Today)"
        elif int(self.viewday-3600*24)/(3600*24)==watched:
            all+=u" (Tomorow)"
        elif int(self.viewday-7200*24)/(3600*24)==watched:
            all+=u" (After Tomorow)"
        elif int(self.viewday+3600*24)/(3600*24)==watched:
            all+=u" (Yesterday)"
        elif (watched-int(self.viewday/(3600*24)))%7==0:
            all+=u" (" + str(-(watched-int(self.viewday/(3600*24)))/7) + " week)"
        self.img.text((12,12), unicode(format_time(self.viewday)[:10])+all,font=self.currentfont, fill = (255,255,255))
        self.img.blit(self.logo, target=(self.w-14,0))
    
    def drawRectangle(self,list):
        #Loop the event list
        if (self.selected < 0):
            self.selected=len(list)-1
        elif (self.selected > int(len(list)-1)):
            self.selected=0
            
        if list!=[[]]:
            try:
                difk=(list[self.selected][2]+(list[self.selected][3]*1./60)-list[self.selected][0]-(list[self.selected][1]*1./60))*self.vadjust
            except:
                return 0
            category=list[self.selected][5]
            try:
                category=self.ideacat[int(category)][0]
            except:
                category=list[self.selected][5]
            linecount=int((difk)/self.dish)
            
            time0=str(list[self.selected][0])
            time1=str(list[self.selected][1])
            time2=str(list[self.selected][2])
            time3=str(list[self.selected][3])
            if len(time0)==1:
                time0="0"+time0
            if len(time1)==1:
                time1="0"+time1
            if len(time2)==1:
                time2="0"+time2
            if len(time3)==1:
                time3="0"+time3
            
            long_str=unicode(time0 +":" + time1+ "-" + time2 +":" + time3+ " "+ list[self.selected][4] +" | " + category)
            lines = wrap_text_to_array(long_str, self.currentfont, self.w-10)
            if linecount<len(lines):
                difk=(self.dish+2)*len(lines)
            difk2=difk
            split=2*int(difk/6)
            if split!=0:
                difk=float(difk/split)
            cc=(list[self.selected][0]+(list[self.selected][1]*1./60)-self.hstart)*self.vadjust
            
            for j in range(0,split/2):
                self.img.rectangle((13,int(cc+difk*j+self.newh),self.w,int(cc+difk*(j+1)+self.newh)), fill=(255-(j)*(80/split),
                                                                                        255-(j)*(80/split),
                                                                                        255-(j)*(80/split)))
            if split==0:
                split=1
            
            self.img.rectangle((13,int(cc+difk*split/2+self.newh),self.w-1,int(cc+difk*(split)+self.newh+1)), fill=(220,220,220))
            self.img.line((12,cc+self.newh,self.w,cc+self.newh), outline=(10,10,10), width=1)
            self.img.line((12,int(cc+split*difk+self.newh),self.w,int(cc+split*difk+self.newh)), outline=(230,230,230), width=1)
            
            #Draw lines
            self.img.rectangle((self.w-4,cc+self.newh,self.w,int(cc+difk*(split)+self.newh+1)),fill=(0,0,0))
            self.img.rectangle((self.w-8,cc+self.newh,self.w-4,int(cc+difk*(split)+self.newh+1)),fill=(50,50,50))
            self.img.rectangle((12,cc+self.newh,16,int(cc+difk*(split)+self.newh+1)),fill=(0,0,0))
            self.img.rectangle((16,cc+self.newh,20,int(cc+difk*(split)+self.newh+1)),fill=(50,50,50))
            #When the text should be displayed
            addy=0
            textpos=int(difk2-(len(lines)*self.dish))/2
            for line in lines:
                self.img.text((21,cc+10+textpos+self.newh+addy), line, font=self.currentfont,fill = (240,240,240))
                self.img.text((22,cc+11+textpos+self.newh+addy), line, font=self.currentfont,fill = (0,0,0))
                addy+= self.dish
                linecount-=1
        #drawSignal()
        
    def drawAdjust():

        if (selected < 0):
            selected=len(events)-1
        elif (selected > int(len(events)-1)):
            selected=0
        drawSignal()
        img.rectangle((12,h-10,100,h),fill=(0,0,0))
        img.text((12,h),u"Resize mode on",fill=(255,255,255))
        #drawRectangle(events)
        if start:
            img.line((12,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ,w,(events[selected][2]+(events[selected][3]*1./60)-hstart)*vadjust+newh ), outline = (0,150,0), width = 3)
        else:
            img.line((12,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh  ,w,(events[selected][0]+(events[selected][1]*1./60)-hstart)*vadjust+newh ), outline = (0,150,0), width = 3)
        
        
    def drawHalf(self):
        
        self.drawSignal()
        self.img.rectangle((12,self.h-10,90,self.h),fill=(0,0,0))
        self.img.text((12,self.h),u"Move mode on",fill=(255,255,255))
        colisions= self.checkColisions()
        if len(colisions)==0:
            color=self.colors[12]
        elif len(colisions)==1 and (self.eventCopy[2]*60+self.eventCopy[3]-self.eventCopy[0]*60-self.eventCopy[1]<=colisions[0][2]*60+colisions[0][3]-colisions[0][0]*60-colisions[0][1]):
            color=self.colors[13]
        else:
            color=self.colors[14]
            
        category=self.eventCopy[5]
        try:
            category=self.ideacat[int(category)][0]
        except:
            category=self.eventCopy[5]
        self.img.rectangle((self.w/2,(self.eventCopy[0]+(self.eventCopy[1]*1./60)-self.hstart)*self.vadjust+self.newh,self.w,(self.eventCopy[2]+ (self.eventCopy[3]*1./60)-self.hstart)*self.vadjust+self.newh), fill=color)
        self.img.text((self.w/2 + 2,(self.eventCopy[0]+(self.eventCopy[1]*1./60)-self.hstart)*self.vadjust+10+self.newh), unicode(str(self.eventCopy[0]) +":" + str(self.eventCopy[1])+ "-" + str(self.eventCopy[2]) +":" + str(self.eventCopy[3])+ " "+ self.eventCopy[4] +"| " + category), fill = self.colors[4])
        
    def drawOutline(self):
        if (self.selected < 0):
            self.selected=len(self.events)-1
        elif (self.selected > int(len(self.events)-1)):
            self.selected=0
        self.drawSignal()
        self.img.rectangle((12,self.h-10,140,self.h),fill=(0,0,0))
        self.img.text((12,self.h),u"Change order mode on",fill=(255,255,255))
        #drawRectangle(events)
        self.img.line((12,(self.events[self.selected][2]+(self.events[self.selected][3]*1./60)-self.hstart)*self.vadjust+self.newh,self.w,(self.events[self.selected][2]+(self.events[self.selected][3]*1./60)-self.hstart)*self.vadjust+self.newh), outline = self.colors[13], width = 3)
        self.img.line((12,(self.events[self.selected][0]+(self.events[self.selected][1]*1./60)-self.hstart)*self.vadjust+self.newh,self.w,(self.events[self.selected][0]+(self.events[self.selected][1]*1./60)-self.hstart)*self.vadjust+self.newh), outline = self.colors[13], width = 3)
        
        
    def drawHLine(self):
        
        self.drawSignal()
        self.img.rectangle((12,self.h-10,100,self.h),fill=(0,0,0))
        self.img.text((12,self.h),u"Insert mode on",fill=(255,255,255))
        self.img.line((12,(self.hline-self.hstart*60)*self.vadjust/60+self.newh ,self.w,(self.hline-self.hstart*60)*self.vadjust/60+self.newh), outline = self.colors[8], width = 2)
        self.img.rectangle((self.w-26,(self.hline-self.hstart*60)*self.vadjust/60+self.newh-12,self.w,(self.hline-self.hstart*60)*self.vadjust/60+self.newh),fill=(5,5,5))
        self.img.text((self.w-26,(self.hline-self.hstart*60)*self.vadjust/60+self.newh), unicode(str(int(self.hline/60))+":"+str(int(self.hline%60))), fill=self.colors[8])
    
    def update(self):
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
    

app_lock = e32.Ao_lock()

def exit():
    app_lock.signal()
    
    
appuifw2.app.exit_key_handler=exit
main=Main()
app_lock.wait()
