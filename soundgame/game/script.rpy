
image hamster = Solid(color="#ffffff",  xsize=50, ysize=50)
# image rectone = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.4, yalign=0.3)
# image recttwo = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.2, yalign=0.2)
# image rectthree = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.5, yalign=0.8)
# image rectfour = Solid(color="#672c2c",  xsize=50, ysize=50, xalign=0.6, yalign=0.6)

#define sound_collision = "sounds/sinister.mp3"
default change_rectone_visibility = False
default rectangle_selected = False
define level_one_start = False
define level_two_start = False

define config.log = "mylogs.txt"

default g_time = 0

default rect_positions = []

screen timerFame(max, endup):
    frame:
        xalign 0.9
        yalign 0.1
        hbox:
            timer 0.1 action If(g_time > max, false = SetVariable("g_time", g_time + 0.1), true = [Hide("timerFame"), SetVariable("g_time", 0), Jump("%s"%endup) ]) repeat True
            bar: #an animated bar top center screen
                value AnimatedValue(value=g_time, range=max, delay= 0.5)
                xalign 0.0
                yalign 0.0
                xmaximum 200



init  python:
    import pygame
    import random
    import weakref

    k_pressed = False
    n_pressed = False
    selected_rects = []
    list
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


    class Rectangle:
        instances = []

        def __init__(self, x, y, xalign, yalign, path):
            self.x = x
            self.y = y
            self.xalign = xalign
            self.yalign = yalign
            self.path = path
            self.music_started = False
            self.is_found = False
            self.rendered = ""
            Rectangle.instances.append(self)
        def __del__(self):
            print("Destructor called, MyClass deleted.")

        @classmethod
        def remove_all_instances(cls):
            while cls.instances:
                cls.instances.pop()  # Each pop should eventually trigger __del__()
        @classmethod
        def remove_instance(cls, instance):
            if instance in cls.instances:
                cls.instances.remove(instance)
                del instance  # Optionally delete the object; __del__ will be called

        @classmethod
        def remove_instance_by_position(cls, xalign, yalign):
            for instance in list(cls.instances):
                if instance.xalign == xalign and instance.yalign == yalign:
                    cls.remove_instance(instance)
                    break  # Break after removing to avoid modifying list during iteration if only one is to be removed

        def render(self):
        # Calculate the top-left corner based on alignment and size
            screen_width = renpy.config.screen_width
            screen_height = renpy.config.screen_height
            top_left_x = self.xalign * screen_width
            top_left_y = self.yalign * screen_height
            self.rendered = pygame.Rect(top_left_x, top_left_y, self.x, self.y)
            #return #pygame.Rect(top_left_x, top_left_y, self.x, self.y)
            pass
   

    def generate_non_overlapping_positions(count, rect_size):
        max_attempts = 100
        positions = []
        width, height = rect_size

        def overlaps(new_rect, rects):
            nx, ny = new_rect
            nw, nh = width, height
            for x, y in rects:
                if not (x + width < nx or nx + nw < x or y + height < ny or ny + nh < y):
                    return True
            return False

        while len(positions) < count:
            attempt = 0
            while attempt < max_attempts:
                new_position = (random.uniform(0, 1 - width), random.uniform(0, 1 - height))
                if not overlaps(new_position, positions):
                    positions.append(new_position)
                    break
                attempt += 1
            if attempt == max_attempts:
                raise Exception("Couldn't place all rectangles without overlap.")

        return positions

    hamster_coordinate=Coordinate(0.5,0.5,0.05,0.05,0.95,0.95)

    renpy.music.register_channel("collision_channel", mixer="sfx", loop=False)

# screen level_display():
#     $ rect_positions = generate_non_overlapping_positions(4, (0.1, 0.1))  # assuming each rect is about 10% of screen size

#     # Dynamically create rectangles with positions
#     for i, pos in enumerate(rect_positions):
#         x, y, width, height = pos
#         add Solid(
#             color="#672c2c",
#             xsize=width * 800,  # Assuming screen width is 800
#             ysize=height * 600,  # Assuming screen height is 600
#             xpos=x * 800,
#             ypos=y * 600
#         )








label start:

    "this is soundgame"

    "Once you add a story, pictures, and music, you can release it to the world!"
    #show screen level_display


label level_one:
    "level one"
    #show screen timerFame(10, "level_two")

    

   
    python:
        
            rect_positions = generate_non_overlapping_positions(4, (0.05, 0.05))
            
            print(rect_positions)
  
            for i, pos in enumerate(rect_positions):
                    Rectangle(100, 100, pos[0], pos[1], "sounds/sinister.mp3" if i < 2 else "sounds/biolife.mp3").render()
 
    call screen hamster_cage   


label level_two:
    "level two"   
    python:
        
            rect_positions = generate_non_overlapping_positions(6, (0.05, 0.05))            
            print(rect_positions)
            rectangles = [
                Rectangle(100, 100, pos[0], pos[1], "sounds/sinister.mp3" if i < 2 else "sounds/biolife.mp3").render()
                for i, pos in enumerate(rect_positions)
            ]

    call screen hamster_cage   

label level_three:
    "level three"    
    python:        
            rect_positions = generate_non_overlapping_positions(8, (0.05, 0.05))            
            print(rect_positions)
            rectangles = [
                Rectangle(100, 100, pos[0], pos[1], "sounds/sinister.mp3" if i < 2 else "sounds/biolife.mp3").render()
                for i, pos in enumerate(rect_positions)
            ]
          
    call screen hamster_cage   

label after: 
    "not finished level "      


screen hamster_cage:    
    frame:
        add "hamster" anchor (0.5,0.5) at Transform(function=hamster_coordinate.transform)  
        key "g" action ToggleVariable("change_rectone_visibility")    
        key "n" action SetLocalVariable("n_pressed",  True)
        key "focus_left" action SetField(hamster_coordinate,"xoffset",-0.005)
        key "focus_right" action SetField(hamster_coordinate,"xoffset",+0.005)
        key "focus_up" action SetField(hamster_coordinate,"yoffset",-0.005)
        key "focus_down" action SetField(hamster_coordinate,"yoffset",+0.005)
        key "dismiss" action Return("hamster")
        
        if change_rectone_visibility == True:
            for xalign, yalign in rect_positions:
                add Solid(color="#672c2c", xsize=50, ysize=50, xalign=xalign, yalign=yalign)

        python:        
        
            hamster_rect = pygame.Rect(hamster_coordinate.x * renpy.config.screen_width, hamster_coordinate.y * renpy.config.screen_height, 100, 100)       
            collision_channel = 'collision_channel'

            # for position in rect_positions:
            #     xalign, yalign = position  # Unpack the position list into xalign and yalign
            #     renpy.add(renpy.Solid(color="#672c2c", xsize=50, ysize=50, xalign=xalign, yalign=yalign))
                


            for rect in Rectangle.instances:
                print(rect)
                rect = rect
                music_started = rect.music_started

                if hamster_rect.colliderect(rect.rendered):
                    if not music_started:
                        renpy.music.play(rect.path, channel=collision_channel, loop=True)
                        rect.music_started = True

                    if n_pressed:
                        renpy.log("The 'n' key was pressed!")
                        selected_rects.append(rect)
                        renpy.log(selected_rects)
                        renpy.notify(selected_rects)
                        n_pressed = False
                else:                
                    
                    if music_started:
                        renpy.music.stop(channel=collision_channel)
                        rect.music_started = False
            n_pressed = False


            if len(selected_rects) == 2:
                if selected_rects[0].path == selected_rects[1].path:
                    renpy.notify("you found same sounds")
                    for selected_rect in selected_rects:
                        if selected_rect in Rectangle.instances:
                            selected_rect.remove_instance_by_position(selected_rect.xalign,selected_rect.yalign )
                            renpy.music.stop(channel=collision_channel)
                    selected_rects.clear()
            



    # Continue with your Ren'Py story script here.
