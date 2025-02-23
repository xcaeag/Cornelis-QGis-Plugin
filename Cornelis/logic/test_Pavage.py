import unittest
from pavage import Node


class TestNodeMethods(unittest.TestCase):

    def test_projectionPerpendiculaire(self):
        # Test case 1: Point lies directly on the segment
        p = Node(1, 1)
        p1 = Node(0, 0)
        p2 = Node(2, 2)
        projected = p.projectionPerpendiculaire(p1, p2)
        self.assertAlmostEqual(projected.x, 1)
        self.assertAlmostEqual(projected.y, 1)

        # Test case 2: Point lies outside the segment
        p = Node(3, 1)
        p1 = Node(0, 0)
        p2 = Node(2, 2)
        projected = p.projectionPerpendiculaire(p1, p2)
        self.assertAlmostEqual(projected.x, 2)
        self.assertAlmostEqual(projected.y, 2)

        # Test case 3: Vertical segment
        p = Node(0, 2)
        p1 = Node(1, 0)
        p2 = Node(1, 4)
        projected = p.projectionPerpendiculaire(p1, p2)
        self.assertAlmostEqual(projected.x, 1)
        self.assertAlmostEqual(projected.y, 2)

        # Test case 4: Horizontal segment
        p = Node(2, 2)
        p1 = Node(4, 1)
        p2 = Node(8, 1)
        projected = p.projectionPerpendiculaire(p1, p2)
        self.assertAlmostEqual(projected.x, 2)
        self.assertAlmostEqual(projected.y, 1)


if __name__ == "__main__":
    unittest.main()
