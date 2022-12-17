import pygame
import globals

class Player():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.nextImgNum = 0
        self.image = pygame.image.load(f"./media/images/player/{self.nextImgNum}.gif")
        self.rect = self.image.get_rect()
        
        self.dfLeftXCoord = 100 # where the player will spawn
        self.dfTopYCoord = globals.DISPLAY_HEIGHT - self.image.get_height() - 40 # also used with jumping

        self.rect.move_ip(self.dfLeftXCoord, self.dfTopYCoord)

        self.set_image()

        self.nextImageTimerDfDelay = 0.05
        self.nextImageTimer = globals.RepeatTimer(self.nextImageTimerDfDelay, self.set_image)
        self.nextImageTimer.start()

        self.speedX = 5
        self.speedY = 15 # jump duration

        self.curSpeedX = 0
        self.curSpeedY = 0

        self.jumpInProg = False
        self.jumpMaxHeight = self.spritesDict["helicopter"][0].rect.bottom


    ######################################################################
    # OPTIONAL
        
    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.curSpeedX = self.speedX
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay / 1.5 # make the animation faster
                if event.key == pygame.K_LEFT:
                    self.curSpeedX = self.speedX * -1
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay * 1.5 # make the animation slower
                if event.key == pygame.K_UP:
                    self.init_jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.curSpeedX = 0
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay


    def update_location(self):
        newRect = self.rect.move(self.curSpeedX, self.curSpeedY)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect

        if self.jumpInProg: self.manage_jump()

    
    def blit(self):
        self.screen.blit(self.image, self.rect)


    ######################################################################
    # SPECIAL

    def init_jump(self):
        if self.jumpInProg: return
        self.jumpInProg = True
        self.curSpeedY = self.speedY * -1 # needs to go up at first
        self.nextImageTimer.cancel() # no good way to pause/resume the timer, so I just quit it

    def manage_jump(self):
        if self.rect.top <= self.jumpMaxHeight: # jump has reached max height, time to go down
            self.curSpeedY = self.curSpeedY * -1
        elif self.rect.top >= self.dfTopYCoord: # has landed
            self.jumpInProg = False
            self.curSpeedY = 0
            self.nextImageTimer = globals.RepeatTimer(self.nextImageTimerDfDelay, self.set_image)
            self.nextImageTimer.start()
        
    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/player/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1
