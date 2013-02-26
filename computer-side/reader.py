# -*- coding: utf-8 -*-
from sys import stdout
import os.path
import textwrap
import pygame
pygame.font.init()

class Reader(pygame.Rect,object):
    
    class ln(object):
        def __init__(self,string,nl,sp):
            self.string = string
            self.nl = nl
            self.sp = sp

    def __init__(self,text,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),split=True):
        self._original = text.expandtabs(4).split('\n')
        self.BG = bg
        self.FGCOLOR = fgcolor
        self._line = 0
        self._index = 0
        if not font:
            self._fontname = pygame.font.match_font('mono',1)
            self._font = pygame.font.Font(self._fontname,fontsize)
        elif type(font) == str:
            self._fontname = font
            self._font = pygame.font.Font(font,fontsize)
        self._w,self._h = self._font.size(' ')
        self._fontsize = fontsize
        if not height: pygame.Rect.__init__(self,pos,(width,self._font.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self.split = split
        self._splitted = self.splittext()
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self._hlc = hlcolor
        self.HLCOLOR = hlcolor

    def splittext(self):
        nc = self.width // self._w
        out = []
        for e,i in enumerate(self._original):
            a = Reader.ln('',e,0)
            if not i:
                out.append(a)
                continue
            for j in textwrap.wrap(i,nc,drop_whitespace=True) if self.split else [i]:
                out.append(Reader.ln(j,e,a.sp+len(a.string)))
                a = out[-1]
        return out
    
    @property
    def TEXT(self):
        return '\n'.join(self._original)
    @TEXT.setter
    def TEXT(self,text):
        self._original = text.expandtabs(4).split('\n')
        self._splitted = self.splittext()
    
    @property
    def LEN(self):
        return len(self._splitted)
    
    @property
    def HLCOLOR(self):
        return self._hlc
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)

    @property
    def POS(self):
        return self._line,self._index

    @property
    def NLINE(self):
        return self._splitted[self._line].nl

    @property
    def LINE(self):
        return self._original[self.NLINE]
        
    @property
    def WORD(self):
        try:
            s = self._splitted[self._line].sp+self.wrd
            p1 = self.LINE[:s].split(' ')[-1]
            p2 = self.LINE[s:].split(' ')[0]
            if p2: return p1+p2
        except: return None
    
    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i.string) for i in self._splitted[:p2[0]]]
            return '\n'.join(self._original)[sum(selection[:p1[0]]) + self._splitted[p1[0]].nl + p1[1]:sum(selection) + self._splitted[p2[0]].nl + p2[1]]
        return ''
                
    @property
    def FONTSIZE(self):
        return self._fontsize
    @FONTSIZE.setter
    def FONTSIZE(self,size):
        self._font = pygame.font.Font(self._fontname,size)
        self._fontsize = size
        self._w,self._h = self._font.size(' ')
        self._splitted = self.splittext()
        y = self._y
        h = len(self._splitted) * self._h
        if h > self.height:
            if self._y - self._h < self.bottom - h: self._y = self.bottom - h
        self._y += (self.top - self._y)%self._h
        self.HLCOLOR = self._hlc
    
    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)
        
        start = (self.top - self._y) // self._h
        end = (self.bottom - self._y) // self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i.string):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x,y))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                x += self._w
            y += self._h
        self._src.set_clip(clip)
        
    def show(self):
        self.screen()
        pygame.display.update(self)
      
    def scrolldown(self,n):
        y = self._y
        if self._y + self._h * n > self.top: self._y = self.top
        else: self._y += self._h * n
    
    def scrollup(self,n):
        y = self._y
        h = len(self._splitted) * self._h
        if h > self.height:
            if self._y - self._h * n < self.bottom - h: self._y = self.bottom - h
            else: self._y -= self._h * n
                
    def update(self,ev):

        line,index = self._line,self._index
        ctrl = pygame.key.get_pressed()
        ctrl = ctrl[pygame.K_RCTRL]|ctrl[pygame.K_LCTRL]
      
        if ev.type == pygame.KEYDOWN:            
            if ev.key == pygame.K_UP:
                self.scrolldown(1)
                return True
                
            elif ev.key == pygame.K_DOWN:
                self.scrollup(1)   
                return True        
            
            elif ctrl and ev.key == pygame.K_KP_PLUS:
                self.FONTSIZE += 1  
                return True       
            
            elif ctrl and ev.key == pygame.K_KP_MINUS and self._fontsize:
                self.FONTSIZE -= 1
                return True

        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button == 1:
                ret = True if self._select != (self._line,self._index) else None
                self._line = (ev.pos[1] - self._y) // self._h
                self._index = (ev.pos[0] - self._x) // self._w
                self.wrd = self._index
                if ((ev.pos[0] - self._x) % self._w) > (self._w // 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line].string)
                if self._index > len(self._splitted[self._line].string): self._index = len(self._splitted[self._line].string)
                self._select = self._line,self._index
                return ret
                
        elif ev.type == pygame.MOUSEBUTTONUP and self.collidepoint(ev.pos):
            try:
                if ev.click[4]:
                    self.scrolldown(sum(range(1,ev.click[4]+1))//10+1)
                    return True
                elif ev.click[5]:
                    self.scrollup(sum(range(1,ev.click[5]+1))//10+1)
                    return True
            except:
                if ev.button == 4:
                    self.scrolldown(3)
                    return True
                
                elif ev.button == 5:
                    self.scrollup(3)
                    return True
        
        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) // self._h
            self._index = (ev.pos[0] - self._x) // self._w
            if ((ev.pos[0] - self._x) % self._w) > (self._w // 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line].string)
            if self._index > len(self._splitted[self._line].string): self._index = len(self._splitted[self._line].string)
            return True

class Lister(Reader):
    
    def __init__(self,liste,pos,size,fontsize,font=None,fgcolor=(0,0,0),hlcolor=(120,18,250)):
        self.font = font
        self.text = ' %s\n'%'\n '.join(liste)
        self.fontsize = fontsize
        self.fgcolor = fgcolor
        self.hlcolor = hlcolor
        self.foo = -1
        self.pack(pos,size)
        self.scr = pygame.display.get_surface()
    
    def pack(self,pos,size):
        width,height = size
        Reader.__init__(self,self.text,pos,width,self.fontsize,None,self.font,fgcolor=self.fgcolor,hlcolor=self.hlcolor,split=False)
        self._line = self.foo
        h = self.height
        self.height = height//self.height*self.height
        self.BG = pygame.Surface(self.size)
        for i in range(self.height//h): self.BG.fill(0xffffff if i&1 else 0xf0f0f0,(0,i*h,width,h))
    
    def update(self,ev):
        nline = self.NLINE
        ret = super(Lister,self).update(ev)
        if nline == self.NLINE: ret = False
        if ev.type == pygame.MOUSEBUTTONUP and self.collidepoint(ev.pos):
            self.foo = self.NLINE
            return True
        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and not self.collidepoint(ev.pos):
            self._line = self.foo
            return False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self.collidepoint(ev.pos):
            return True
        return ret
            
    
    @property
    def OUTPUT(self): return None
    @OUTPUT.setter
    def OUTPUT(self,liste):
        self.text = ' %s\n'%'\n '.join(liste)
        Reader.__init__(self,self.text,self.topleft,self.width,self.fontsize,self.height,self.font,bg=self.BG,fgcolor=self.fgcolor,split=False,hlcolor=self.hlcolor)
        self._line = self.foo = -1
        
        
    def screen(self):
        #super(Lister,self).screen()
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)
        
        start = (self.top - self._y) // self._h
        end = (self.bottom - self._y) // self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i.string):
                if py != self.NLINE:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._font.set_italic(1)
                    self._src.blit(self._font.render(j,1,self.HLCOLOR),(x,y))
                    self._font.set_italic(0)
                x += self._w
            y += self._h
        self._src.set_clip(clip)

if __name__ == '__main__':
    import os.path
    pygame.display.set_mode((700,400))
    text = """"Reader" allows you to render text and scroll it by using mouse wheel or arrow keys.
The constraint being that it only supports monospaced fonts and use unicode string.
ctrl+, ctrl- : increase and decrease font.
all tab characters in text will be expanded to spaces(4).

Reader(text,pos,width,height=None,font=None,fontsize=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200))

pos      = position of the box
width    = width in pix
height   = height in pix
fontsize = size of the font
bg       = backgroud: color triplet or surface object
fgcolor  = foreground: color triplet
hlcolor  = highlight: rgb or rgba color

Reader.show()
display the box.

Reader.update(pygame.event)
Update the box by sending event.

property:
LINE      = get the clicked line
NLINE     = get the clicked line number
WORD      = get the clicked word
SELECTION = get the selected text

with NLINE and WORD you can make some simplist menus, ex:
choose a colour, click on following items:

\t\tRED
\t\tBLUE
\t\tWHITE

QUIT"""
    
    try: import GetEvent
    except : GetEvent = pygame.event
    txt = Reader(text.expandtabs(4),(20,20),660,15,height=360,bg=(20,20,20),fgcolor=(255,255,255),hlcolor=(255,10,150,100),split=True)
    txt.show()
    pygame.key.set_repeat(100,25)
    while True:
        evs = GetEvent.get()
        if evs:
            for ev in evs:
                txt.update(ev)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if txt.WORD: stdout.write(txt.WORD+'\n')
                    if txt.WORD == 'QUIT': exit()
                    if txt.WORD == 'RED': txt.FGCOLOR = 255,200,180
                    if txt.WORD == 'BLUE': txt.FGCOLOR = 180,200,255
                    if txt.WORD == 'WHITE': txt.FGCOLOR = 255,255,255
            txt.show()
