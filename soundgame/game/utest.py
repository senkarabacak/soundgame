import unittest
from logic import Rectangle, generate_non_overlapping_positions

class TestRectangle(unittest.TestCase):
    def test_rendered_property(self):
        rect = Rectangle(100, 100, 0.5, 0.5, "path/to/sound")
        self.assertIsNotNone(rect.rendered)

    def test_remove_instance_by_position(self):
        rect = Rectangle(100, 100, 0.5, 0.5, "path/to/sound")
        initial_count = len(Rectangle.instances)
        Rectangle.remove_instance_by_position(0.5, 0.5)
        self.assertEqual(len(Rectangle.instances), initial_count - 1)

    # Add more test cases as needed

class TestGenerateNonOverlappingPositions(unittest.TestCase):
    def test_positions_count(self):
        positions = generate_non_overlapping_positions(5, (0.1, 0.1))
        self.assertEqual(len(positions), 5)

    def test_no_overlaps(self):
        positions = generate_non_overlapping_positions(5, (0.1, 0.1))
        for i, pos1 in enumerate(positions):
            for pos2 in positions[i + 1:]:
                self.assertFalse(self.check_overlap(pos1, pos2))

    def check_overlap(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        width, height = 0.1, 0.1
        return not (x1 + width < x2 or x2 + width < x1 or y1 + height < y2 or y2 + height < y1)

    # Add more test cases as needed

if __name__ == "__main__":
    unittest.main()
