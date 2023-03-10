import pygame
#import psutil

import globals
import menu
import wall
import background
import player
import enemy
import pointer
import drone
import cross
import hud
import regulator

class Sprites():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen):
        self.screen = screen
        self.dict = {}
        self.regulator = regulator.Regulator(self.screen, self.dict)

        self.load_dict()
        self.dict["welcome_menu"][0].toggle_menu()

    def load_dict(self):
        self.dict["welcome_menu"] = []
        self.dict["welcome_menu"].append(menu.Menu(self, "welcome"))

        self.dict["pause_menu"] = []
        self.dict["pause_menu"].append(menu.Menu(self, "pause"))

        self.dict["over_menu"] = []
        self.dict["over_menu"].append(menu.Menu(self, "over"))

        self.dict["victory_menu"] = []
        self.dict["victory_menu"].append(menu.Menu(self, "victory"))

        self.dict["walls"] = []
        self.dict["walls"].append(wall.Wall("top"))
        self.dict["walls"].append(wall.Wall("bottom"))
        self.dict["walls"].append(wall.Wall("left"))
        self.dict["walls"].append(wall.Wall("right"))

        self.dict["background"] = []
        self.dict["background"].append(background.Background(self.screen))

        self.dict["drone"] = []
        self.dict["drone"].append(drone.Drone(self.screen, self.regulator, self.dict))

        self.dict["player"] = []
        self.dict["player"].append(player.Player(self.screen, self.regulator, self.dict))

        self.dict["cross"] = []
        self.dict["cross"].append(cross.Cross(self.screen, self.regulator, self.dict))

        self.dict["enemies"] = []
        self.regulator.spawn_df_num_enemies()

        self.dict["bullets"] = []

        self.dict["hud"] = []
        self.dict["hud"].append(hud.Hud(self.screen, self.dict))

        self.dict["pointer"] = []
        self.dict["pointer"].append(pointer.Pointer(self.screen, self.dict))


    def animate(self):
        #print(f"RAM memory % used: {psutil.virtual_memory()[2]}")
        #print(f"RAM Used (GB): {psutil.virtual_memory()[3]/1000000000}")
        
        eventsQueueArr = pygame.event.get()

        keysArr = list(self.dict.keys())
        for key in keysArr:
            if key.endswith(".paused"): continue
            if key not in self.dict: break # key no longer there, meaning that menu was toggled and all the other keys were changed as well

            for sprite in self.dict[key][:]: # itterate over array and remove items simuntaniously
                if hasattr(sprite, 'user_input'):
                    sprite.user_input(eventsQueueArr)
                if hasattr(sprite, 'update_location'):
                    sprite.update_location()
                if hasattr(sprite, 'shouldDelete') and sprite.shouldDelete:
                    try: self.dict[key].remove(sprite) # this removes its reference in self.dict
                    except: pass # bug fix
                    del sprite # this removes the sprite instance itself
                    continue
                if hasattr(sprite, 'blit'):
                    sprite.blit()
                
        pygame.display.update()
