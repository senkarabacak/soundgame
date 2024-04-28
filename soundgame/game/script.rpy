
image hamster = Solid(color="#ffffff",  xsize=50, ysize=50)
image rectone = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.4, yalign=0.3)
image recttwo = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.2, yalign=0.2)
image rectthree = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.5, yalign=0.8)
image rectfour = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.6, yalign=0.6)

define sound_collision = "sounds/sinister.mp3"
default change_rectone_visibility = False
default rectangle_selected = False


define config.log = "mylogs.txt"

default g_time = 0


screen timerFame(max, endup):
    frame:
        xalign 0.5
        yalign 0.0
        hbox:
            timer 0.1 action If(g_time > max, false = SetVariable("g_time", g_time + 0.1), true = [Hide("timerFame"), SetVariable("g_time", 0), Jump("%s"%endup) ]) repeat True
            bar: #an animated bar top center screen
                value AnimatedValue(value=g_time, range=max, delay= 0.5)
                xalign 0.0
                yalign 0.0
                xmaximum 200



init  python:
    import pygame
    n_pressed = False
    selected_rects = []

    class Coordinate:
        def __init__(self,x,y,xmin,ymin,xmax,ymax):

            self.x,self.y,self.xmin,self.ymin,self.xmax,self.ymax=x,y,xmin,ymin,xmax,ymax

            self.xoffset,self.yoffset=0,0
            return

        def transform(self,d,show_time,animate_time):

            self.x+=self.xoffset
            self.y+=self.yoffset
            self.xoffset,self.yoffset=0,0

            if self.x<self.xmin:
                self.x=self.xmin
            if self.y<self.ymin:
                self.y=self.ymin
            if self.x>self.xmax:
                self.x=self.xmax
            if self.y>self.ymax:
                self.y=self.ymax

            d.pos=(self.x,self.y)

            return 0

    hamster_coordinate=Coordinate(0.5,0.5,0.05,0.05,0.95,0.95)

    renpy.music.register_channel("collision_channel", mixer="sfx", loop=False)

    rectangles = [
        {"rect": pygame.Rect(0.4 * renpy.config.screen_width, 0.3 * renpy.config.screen_height, 100, 100), "music_started": False, "path": "sounds/sinister.mp3"},
        {"rect": pygame.Rect(0.2 * renpy.config.screen_width, 0.2 * renpy.config.screen_height, 100, 100), "music_started": False, "path": "sounds/sinister.mp3"}
    ]

    
    class Rectangle:
        def __init__(self, x, y, xalign, yalign, path):
            self.x = x
            self.y = y
            self.xalign = xalign
            self.yalign = yalign
            self.path = path
            self.music_started = False
            self.is_found = False

        # def __init__(self,x,y,xalign,yalign,path):

        #     self.x,self.y,self.xalign,self.yalign,self.path            
        #     self.path=path
        #     self.music_started = False
        #     self.is_found=False
        #     return

        def render(self):
        # Calculate the top-left corner based on alignment and size
            screen_width = renpy.config.screen_width
            screen_height = renpy.config.screen_height
            top_left_x = self.xalign * screen_width
            top_left_y = self.yalign * screen_height
            return pygame.Rect(top_left_x, top_left_y, self.x, self.y)

        # def render_rect():
        #     return pygame.Rect(xalign * renpy.config.screen_width, yalign * renpy.config.screen_height, x, y)

    rectOnePy = Rectangle(100,100,0.4,0.3,"sounds/sinister.mp3")
    rectOnePyRender = rectOnePy.render()
    rectTwoPy = Rectangle(100,100,0.2,0.2,"sounds/sinister.mp3")
    rectTwoPyRender = rectTwoPy.render()
    rectThreePy = Rectangle(100,100,0.5,0.8,"sounds/biolife.mp3")
    rectThreePyRender = rectThreePy.render()
    rectFourPy = Rectangle(100,100,0.6,0.6,"sounds/biolife.mp3")
    rectFourPyRender = rectFourPy.render()

screen hamster_cage:


    add "hamster" anchor (0.5,0.5) at Transform(function=hamster_coordinate.transform)
    

    key "g" action ToggleVariable("change_rectone_visibility")
    

    key "n" action SetLocalVariable("n_pressed",  True)
    $ renpy.log(n_pressed)

    
   

    key "focus_left" action SetField(hamster_coordinate,"xoffset",-0.005)
    key "focus_right" action SetField(hamster_coordinate,"xoffset",+0.005)
    key "focus_up" action SetField(hamster_coordinate,"yoffset",-0.005)
    key "focus_down" action SetField(hamster_coordinate,"yoffset",+0.005)



    key "dismiss" action Return("hamster")

    if change_rectone_visibility == True:
        
        if len(rectangles):
                add "rectone"
                add "recttwo"
                add "rectthree"
                add "rectfour"
        $ if change_rectone_visibility: renpy.log("The 'g' key was pressed!")


   



    python:

        

        
      
        hamster_rect = pygame.Rect(hamster_coordinate.x * renpy.config.screen_width, hamster_coordinate.y * renpy.config.screen_height, 100, 100)
       
        collision_channel = 'collision_channel'

        for rect_info in rectangles:
            rect = rect_info["rect"]
            music_started = rect_info["music_started"]

            if hamster_rect.colliderect(rect):
                if not music_started:
                    renpy.music.play(sound_collision, channel=collision_channel, loop=True)
                    rect_info["music_started"] = True

                if n_pressed:
                    renpy.log("The 'n' key was pressed!")
                    selected_rects.append(rect_info)
                    renpy.log(selected_rects)
                    renpy.notify(selected_rects)
                    n_pressed = False
            else:                
                
                if music_started:
                    renpy.music.stop(channel=collision_channel)
                    rect_info["music_started"] = False
        n_pressed = False


        if len(selected_rects) == 2:
            if selected_rects[0]["path"] == selected_rects[1]["path"]:
                renpy.notify("you found same sounds")
                for selected_rect in selected_rects:
                    if selected_rect in rectangles:
                        rectangles.remove(selected_rect)
                selected_rects.clear()


label start:

    "this is soundgame"

    "Once you add a story, pictures, and music, you can release it to the world!"
    show screen timerFame(60, "after")
    call screen hamster_cage   
    # Run the Python script inside Ren'Py
label after: 
    "not finished level "      
# Continue with your Ren'Py story script here.
