

default hamster_color = "#000000"  
default change_visibility = False
default change_hasmter_visibility = False
default rectangle_selected = False
define level_one_start = False
define level_two_start = False
default g_time = 0
default rect_positions = []
default level_counter = 0
define config.has_autosave = False
define config.has_quicksave = False


# characters setting are embedded in the renpy, using directly as variable
define senior_hamster = Character("Master", who_color="#ceffc8")
define junior_hamster = Character("Junior", who_color="#c8e6ff")
define tutorial = Character("Tutorial", who_color="#ffc8c8")

# python code can be used in renpy but not directly in framework, instead initializing as codeblocks
init  python:
    
    import pygame
    import random
    import weakref

    ############################################################################################################################
    #####                                                                                                                  #####
    #####   Please check into logic.py for game logic and utest.py for unit tests, it will be run by pipeline at github    #####
    #####                                                                                                                  #####
    ############################################################################################################################


    from logic import Coordinate, Rectangle, generate_non_overlapping_positions, calculate_rendered_rect, render_rectangles


    #activating text-to-Speech using native Speech API of OS
    if renpy.windows:
        config.tts_voice = "Mark"
    elif renpy.macintosh:
        config.tts_voice = "Alex"
    elif renpy.linux:
        config.tts_voice = "english_rp"

    k_pressed = False
    n_pressed = False
    selected_rects = []
    bird_sounds = [
    "sounds/bird001.mp3",
    "sounds/bird002.mp3",
    "sounds/bird003.mp3",
    "sounds/bird004.mp3"
    ]
    list
 

    hamster_coordinate=Coordinate(0.5,0.5,0.05,0.05,0.95,0.95)

    renpy.music.register_channel("collision_channel", mixer="sfx", loop=False)



label start:
    #scene foresthamsters
    scene bg foresthamsters

    "Deep within the forest..."

    senior_hamster "Greetings, my apprentice!"
    senior_hamster "You've completed your training, and now it's time to restore peace to our beloved forest."
    senior_hamster "Our forest was once serene, filled with the delightful sounds of birds."
    senior_hamster "But now, unpleasant bird calls disrupt our tranquil existence."
    senior_hamster "Your task is to capture them and rid our forest of their disturbance."
    senior_hamster "Are you prepared?"

    junior_hamster "YES!"

    jump tutorial
    #show screen level_display


label tutorial:
    "As always, we'll embark on this mission under the cover of night."

    tutorial "Use the arrow keys to navigate – up, down, left, and right."
    tutorial "Should you collide with the forest's borders, you'll hear a bump."
    tutorial "Upon encountering a bird, you'll recognize its call."
    tutorial "Press 'n' to capture a bird when you hear it."
    tutorial "But remember, you must find its mate."
    tutorial "Capture both matching bird sounds by pressing 'n'."
    tutorial "Successful matches result in their expulsion from the forest."
    tutorial "Failed attempts return them to their original spots."
    tutorial "You also have a 60-minute time limit, shown in the top left corner."
    tutorial "Press 'h' to reveal your hamster's position, and 'g' to locate the birds."

    tutorial "Are you ready to embark on this quest?"

    menu:
        "Yes, i am ready":
            jump tutorial_play
        "No, explain again":
            "Take your time. Let me know when you're ready."
            jump tutorial  
# tutorial play
label tutorial_play:
    play music "sounds/jungle.mp3" loop
  
    python:        
            rect_positions = generate_non_overlapping_positions(2, (0.1, 0.1))
            render_rectangles(2, rect_positions, bird_sounds) 
    call screen hamster_cage(100, "tutorial_play")  
# level 1
label level_one:
    "level one"       
    python:        
            rect_positions = generate_non_overlapping_positions(4, (0.1, 0.1))   
            render_rectangles(2, rect_positions, bird_sounds)   
    call screen hamster_cage(100, "level_one")  
# level 2  
label level_two:
    "level two"   
    python:        
            rect_positions = generate_non_overlapping_positions(6, (0.1, 0.1))            
            render_rectangles(2, rect_positions, bird_sounds)     
    call screen hamster_cage(100, "level_two")   
# level 3
label level_three:
    "level three"    
    python:        
            rect_positions = generate_non_overlapping_positions(8, (0.1, 0.1))            
            render_rectangles(2, rect_positions, bird_sounds)
    call screen hamster_cage(100, "level_three") 
# Finish the game
label finish:
    "Congrulations! you have fullfilled"  

   

# this screen will be loaded as the game.
# it conteins renpy for GUI and pygame for Logic
# The UI elements are component of renpy but they are not able to make dynamic collision and movements
# because of this inability  for the same xy values the pygame elements will be used as backend logic 
screen hamster_cage(max, endup):  

    frame:
        # Setting Timer
        xalign 0.9
        yalign 0.1
        hbox:
            timer 0.1 action If(g_time > max, false=SetVariable("g_time", g_time + 0.1), true=[Hide("timerFame"), SetVariable("g_time", 0), Jump("%s" % endup)]) repeat True
            bar:  # Animated bar top center screen
                value AnimatedValue(value=g_time, range=max, delay=0.5)
                xalign 0.0
                yalign 0.0
                xmaximum 200
        if not Rectangle.instances: 
            text "press space button to continue" 
            $ g_time = 0
        # Showing Hamster
        add Solid(color=hamster_color, xsize=100, ysize=100, xalign=0.5, yalign=0.5) anchor (0.5,0.5) at Transform(function=hamster_coordinate.transform)
       
        $ if hamster_coordinate.border_hit: renpy.music.play("sounds/walk_bump.mp3", channel="collision_channel")
        # Key Toggle show/hide
        key "h" action SetVariable("hamster_color", "#000000" if hamster_color == "#ffffff" else "#ffffff")
        key "g" action ToggleVariable("change_visibility")
        key "n" action SetLocalVariable("n_pressed",  True)
        
        # Key action mappings
        key "focus_left" action [Play("sound", "sounds/walk.mp3"), SetField(hamster_coordinate,"xoffset",-0.040)]
        key "focus_right" action [Play("sound", "sounds/walk.mp3"), SetField(hamster_coordinate,"xoffset",+0.040)]
        key "focus_up" action [Play("sound", "sounds/walk.mp3"), SetField(hamster_coordinate,"yoffset",-0.040)]
        key "focus_down" action [Play("sound", "sounds/walk.mp3"), SetField(hamster_coordinate,"yoffset",+0.040)]
        key "dismiss" action Return("hamster")
        
        if change_visibility == True:
            for xalign, yalign in rect_positions:
                add Solid(color="#672c2c", xsize=100, ysize=100, xalign=xalign, yalign=yalign)

        python:    
            # initialize hamster as pygame      
            hamster_rect = pygame.Rect(hamster_coordinate.x * renpy.config.screen_width, hamster_coordinate.y * renpy.config.screen_height, 100, 100)       
            
            collision_channel = 'collision_channel'
            
            for rect in Rectangle.instances:
                rect = rect
                music_started = rect.music_started
                
                # collision logic
                if hamster_rect.colliderect(rect.rendered):
                    if not music_started:
                        renpy.music.play(rect.path, channel=collision_channel, loop=True)
                        rect.music_started = True

                    if n_pressed:
                        if len(selected_rects) == 0:
                            selected_rects.append(rect)
                            renpy.notify("catch bird")
                        elif len(selected_rects) == 1 and rect != selected_rects[0]:
                            selected_rects.append(rect)
                            renpy.notify("catch bird")
                        elif len(selected_rects) == 1 and rect == selected_rects[0]:
                            renpy.notify("cannot catch the same bird")
                        else:
                            renpy.notify("already selected two birds")
                        n_pressed = False

                        
                else:                     
                    if music_started:
                        renpy.music.stop(channel=collision_channel)
                        rect.music_started = False
            
            n_pressed = False

            # checking matches of pair
            if len(selected_rects) == 2 :
                if selected_rects[0].path == selected_rects[1].path:
                    renpy.notify("found pair")
                    for selected_rect in selected_rects:
                        if selected_rect in Rectangle.instances:
                            selected_rect.remove_instance_by_position(selected_rect.xalign,selected_rect.yalign )
                            renpy.music.stop(channel=collision_channel)
                    selected_rects.clear()
                else:
                    selected_rects.clear()
                    renpy.notify("not the pair, miss the other too.")


