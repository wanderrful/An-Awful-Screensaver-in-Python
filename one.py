#internet connection required!

import pygame.display, pygame.event, pygame.image, pygame.time, pygame.mouse
import urllib2, StringIO, re, os, shlex
from random import choice

class App:
    def __init__(self):
        self._running = True

    def onInit(self):
        pygame.init()
        pygame.display.init()

        #set the program's trivial settings
        pygame.display.set_caption('r/EarthPorn Screensaver!')

        pygame.mouse.set_visible(False)

        #set the resolution and bit depth
        info = pygame.display.Info()
        BITDEPTH = info.bitsize
        self.RESOLUTION = (info.current_w,info.current_h)

        pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN, BITDEPTH)

        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.USEREVENT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])

        self._screen = pygame.display.get_surface()
        self._screen.fill((0,0,0))

        f = open('proj\subreddits.txt')
        subredditList = shlex.split(f.read())
        redditUrlList = []
        self.imgurlList = []

        for i in subredditList:
            redditUrlList.append('http://reddit.com/r/'+i)

        print redditUrlList
            
        for x in range(0,len(redditUrlList)):
            webPage = urllib2.urlopen(redditUrlList[x])
            self.imgurlList = re.findall(r'http\:\/\/i.imgur.com\/.........',webPage.read())

        print self.imgurlList
        
        self._running = True

    def onEvent(self, event):
        if not event.type == pygame.USEREVENT: 
            self._running = False
        else:
            self._screen.fill((0,0,0))
            self.selectImage()

    def selectImage(self):
        self.imgURL = choice(self.imgurlList)

    def onLoop(self):
        try:
            imgFile = urllib2.urlopen(self.imgURL)
            buffer = StringIO.StringIO(imgFile.read())
            self.img = pygame.image.load(buffer).convert()
        except pygame.error, message:
            print 'Error: Cannot load image!'
            raise SystemExit, message
    
    def onRender(self):
        if self.img.get_width() >= self.RESOLUTION[0]:
            self.img = pygame.transform.scale(self.img,(self.RESOLUTION[0],self.img.get_height()))
        if self.img.get_height() >= self.RESOLUTION[1]:
            self.img = pygame.transform.scale(self.img,(self.img.get_width(),self.RESOLUTION[1]))

        self._screen.blit(self.img, (0,0))
        
        pygame.display.flip() #update screen
    
    def onCleanup(self):
        pygame.quit()
        exit()

    def onExecute(self):
        self.onInit()
        self.selectImage()

        pygame.time.set_timer(pygame.USEREVENT,5000)
        
        while self._running:
            for e in pygame.event.get():
                self.onEvent(e)
            self.onLoop()
            self.onRender()            
            
        self.onCleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.onExecute()
    
#made by github.com/wanderrful
#with a little help here and there from r/programming
