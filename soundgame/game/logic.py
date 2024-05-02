


import random
import pygame

class Coordinate:
        def __init__(self,x,y,xmin,ymin,xmax,ymax):
            self.x,self.y,self.xmin,self.ymin,self.xmax,self.ymax=x,y,xmin,ymin,xmax,ymax
            self.xoffset,self.yoffset=0,0
            self.border_hit = False
            return

        def transform(self, d, show_time, animate_time):
            # To track if the border was hit
            self.border_hit = False

            # Apply offset and check borders
            self.x += self.xoffset
            self.y += self.yoffset
            if self.x < self.xmin:
                self.x = self.xmin
                self.border_hit = True
            if self.y < self.ymin:
                self.y = self.ymin
                self.border_hit = True
            if self.x > self.xmax:
                self.x = self.xmax
                self.border_hit = True
            if self.y > self.ymax:
                self.y = self.ymax
                self.border_hit = True

            # Reset offsets
            self.xoffset, self.yoffset = 0, 0


            d.pos = (self.x, self.y)
            return self.border_hit


def calculate_rendered_rect(xalign, yalign, x, y):


        top_left_x = xalign * 1920
        top_left_y = yalign * 1080
        return pygame.Rect(top_left_x, top_left_y, x, y)


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
            #self.rendered = ""
            self.rendered = calculate_rendered_rect(xalign, yalign, x, y)  # Calculate rendered rectangle

            Rectangle.instances.append(self)
        
        def __del__(self):
            pass
            #print("Destructor called, MyClass deleted.")

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
            # screen_width = renpy.config.screen_width
            # screen_height = renpy.config.screen_height
            # top_left_x = self.xalign * screen_width
            # top_left_y = self.yalign * screen_height
            # self.rendered = pygame.Rect(top_left_x, top_left_y, self.x, self.y)
            # #return #pygame.Rect(top_left_x, top_left_y, self.x, self.y)
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
