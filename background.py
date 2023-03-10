import pygame
import globals

class Background():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen):
        self.screen = screen

        self.imagesArr = []
        self.rectsArr = []

        for xLeftCoord in [0, globals.DISPLAY_WIDTH]:
            image = pygame.image.load("./media/images/background.png")
            self.imagesArr.append(image)
            rect = pygame.Rect(xLeftCoord, 0, image.get_width(), image.get_height())
            self.rectsArr.append(rect)

        self.speedX = -3
        self.speedY = 0

    ######################################################################
    # OPTIONAL

    def update_location(self):
        for i in range(len(self.rectsArr)):
            self.rectsArr[i] = self.rectsArr[i].move(self.speedX, self.speedY)
            if (self.speedX < 0 and self.rectsArr[i].right <= 0) or (self.speedX > 0 and self.rectsArr[i].left >= globals.DISPLAY_WIDTH):
                leftXCoord = globals.DISPLAY_WIDTH
                if self.speedX > 0: leftXCoord *= -1
                self.rectsArr[i].update(leftXCoord, 0, self.imagesArr[i].get_width(), self.imagesArr[i].get_height())


    def blit(self):
        for i in range(len(self.rectsArr)):
            self.screen.blit(self.imagesArr[i], self.rectsArr[i])
