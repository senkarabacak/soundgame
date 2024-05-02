import random

class Coordinate:
    def __init__(self, x, y, xmin, ymin, xmax, ymax):
        self.x, self.y = x, y
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.xoffset, self.yoffset = 0, 0

    def transform(self, d=None, show_time=None, animate_time=None):
        border_hit = False  # To track if the border was hit

        # Apply offset and check borders
        self.x += self.xoffset
        self.y += self.yoffset
        if self.x < self.xmin:
            self.x = self.xmin
            border_hit = True
        if self.y < self.ymin:
            self.y = self.ymin
            border_hit = True
        if self.x > self.xmax:
            self.x = self.xmax
            border_hit = True
        if self.y > self.ymax:
            self.y = self.ymax
            border_hit = True

        # Reset offsets
        self.xoffset, self.yoffset = 0, 0
        return border_hit

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
        self.rendered = None
        Rectangle.instances.append(self)

    def render(self, screen_width, screen_height):
        top_left_x = self.xalign * screen_width
        top_left_y = self.yalign * screen_height
        self.rendered = (top_left_x, top_left_y, self.x, self.y)
        return self.rendered

def generate_non_overlapping_positions(count, rect_size, screen_width, screen_height):
    max_attempts = 100
    positions = []
    width, height = rect_size

    def overlaps(new_rect, rects):
        nx, ny = new_rect
        nw, nh = width, height
        for x, y, _, _ in rects:
            if not (x + width < nx or nx + nw < x or y + height < ny or ny + nh < y):
                return True
        return False

    while len(positions) < count:
        attempt = 0
        while attempt < max_attempts:
            new_position = (
                random.uniform(0, screen_width - width),
                random.uniform(0, screen_height - height)
            )
            if not overlaps(new_position, positions):
                positions.append(new_position + (width, height))
                break
            attempt += 1
        if attempt == max_attempts:
            raise Exception("Couldn't place all rectangles without overlap.")
    return positions
