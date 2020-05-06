from asyncio import run
from asynctest import main, TestCase
from coroutines import Network, NetworkFunction
from initialize_nodes import do_stuff
from threading import Condition, Thread
from unittest.mock import Mock


class SystemTest(TestCase):

    #testovanie siete trva cca minutu
    def setUp(self):
        HOST = "localhost"
        self.g = Network(NetworkFunction())

        self.g.function.add_edge = Mock(side_effect = lambda node1,node2:
                                        self.graph.add( (node1,node2) ))
        
        self.g.function.get_neighbours = Mock(side_effect = lambda node1:
                                              list(node2 for (node,node2)
                                                   in self.graph if node == node1))
        graph_base = 8030
        
        self.graph = {(0, 1),
                      (1, 2), (1, 3), (1, 4),
                      (4, 5), (4, 7),
                      (5, 6)}
                      
        self.graph = {(graph_base + x, graph_base + y) for x, y in self.graph}
        nodes = {x for y in self.graph for x in y}
        
        self.condition_ready = Condition()
        self.condition_done = Condition()
        
        self.server = Thread(target = do_stuff,
                             args = (HOST, nodes, self.graph,
                                     self.condition_ready, self.condition_done))
        self.server.start()
        
        with self.condition_ready:
            self.condition_ready.wait()
            
            
    def test_all_system(self):
        self.assertEqual(run(self.g.climb_degree(8030)), 8031)
        self.assertEqual(run(self.g.distance4(8030)), {8036})
        
        run(self.g.complete_neighbourhood(8031))
        print(self.graph)
        
        self.assertEqual(run(self.g.climb_degree(8030)), 8034)
        self.assertEqual(run(self.g.distance4(8030)), {8036})
        
        with self.condition_done:
            self.condition_done.notify()
            
        self.server.join()
        

if __name__ == '__main__':
    main()
