import unittest
from script import Coordinate, Rectangle, generate_non_overlapping_positions

class TestGameComponents(unittest.TestCase):
    def test_coordinate_transformations(self):
        coord = Coordinate(0.5, 0.5, 0.05, 0.05, 0.95, 0.95)
        coord.xoffset = 0.1  # Move right
        coord.yoffset = -0.1  # Move up
        coord.transform(None, None, None)  # Assume d, show_time, animate_time are None for now
        self.assertEqual(coord.x, 0.6)
        self.assertEqual(coord.y, 0.4)
        # Test border constraints
        coord.xoffset = -0.6
        coord.transform(None, None, None)
        self.assertEqual(coord.x, 0.05)  # Should hit the minimum x border

    def test_rectangle_initialization(self):
        rect = Rectangle(100, 100, 0.1, 0.1, "path/to/sound.mp3")
        self.assertEqual(rect.x, 100)
        self.assertEqual(rect.y, 100)
        self.assertEqual(rect.xalign, 0.1)
        self.assertEqual(rect.yalign, 0.1)
        self.assertEqual(rect.path, "path/to/sound.mp3")

    def test_non_overlapping_positions(self):
        positions = generate_non_overlapping_positions(3, (0.1, 0.1))
        self.assertEqual(len(positions), 3)
        # Ensure no overlaps
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                self.assertFalse(self.rect_overlap(positions[i], positions[j], (0.1, 0.1)))

    def rect_overlap(self, pos1, pos2, size):
        x1, y1 = pos1
        x2, y2 = pos2
        w, h = size
        return not (x1 + w < x2 or x2 + w < x1 or y1 + h < y2 or y2 + h < y1)

if __name__ == "__main__":
    unittest.main()
