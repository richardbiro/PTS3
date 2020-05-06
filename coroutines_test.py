from asyncio import run
import asynctest
from initialize_nodes import do_stuff
from itertools import permutations
from coroutines import Network, NetworkFunction
from unittest.mock import Mock
import unittest
from time import time
import threading


class CoroutinesTest(unittest.TestCase):
    def setUp(self):
        self.g = Network(NetworkFunction())
        self.graph = set()

        self.g.function.add_edge = Mock(side_effect = lambda node1,node2:
                                        self.graph.add( (node1,node2) ))
        
        self.g.function.get_neighbours = Mock(side_effect = lambda node1:
                                              list(node2 for (node,node2)
                                                   in self.graph if node == node1))
        

    def test_complete_neighbourhood(self):
        self.graph = {(0, 1), (0, 2), (0, 3)}

        run(self.g.complete_neighbourhood(0))

        for pair in permutations((1,2,3),2):
            self.assertTrue(pair in self.graph)

        self.assertEqual(self.g.function.add_edge.call_count, 6)
        self.assertEqual(self.g.function.get_neighbours.call_count, 1)
        self.g.function.get_neighbours.assert_called_with(0)
        

    def test_climb_degree(self):
        self.graph = {(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)}

        self.assertEqual(run(self.g.climb_degree(0)), 1)
        self.assertEqual(self.g.function.get_neighbours.call_count, 9)


    def test_distance4(self):
        self.graph = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)}

        self.assertEqual(run(self.g.distance4(0)), {4})
        self.assertEqual(self.g.function.get_neighbours.call_count, 4)
        

if __name__ == '__main__':
    unittest.main()
