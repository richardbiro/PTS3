from asyncio import create_task, gather, sleep
from requests import get

class Network:
    def __init__(self, function):
        self.function = function

    async def complete_neighbourhood(self, start):
        neighbours = self.function.get_neighbours(start)
        
        async def connect(node):
            for neighbour in neighbours:
                if node != neighbour:
                    self.function.add_edge(node,neighbour)
                await sleep(0.66)
                    
        await gather(*[create_task(connect(neighbour))
                       for neighbour in neighbours])

        

    async def climb_degree(self, start):
        def get_degree(node):
            return len(self.function.get_neighbours(node))

        def get_next(node):
            neighbours = self.function.get_neighbours(node)
            if len(neighbours) == 0:
                return None

            degrees = [[-get_degree(neighbour),neighbour]
                       for neighbour in neighbours]
            
            degrees.sort()
            return degrees[0][1]

        current_node = start
        next_node = get_next(current_node)
        
        while next_node != None and get_degree(next_node) > get_degree(current_node):
            current_node = next_node
            next_node = get_next(current_node)

        return current_node

    

    async def distance4(self, start):
        answer = set()

        async def calculate(node, distance=0, visited=set()):
            if node not in visited:
                visited.add(node)
                if distance == 4:
                    answer.add(node)
                else:
                    await gather(*[calculate(neighbour, distance+1, visited)
                                   for neighbour in self.function.get_neighbours(node)])

        await calculate(start)
        return answer



class NetworkFunction:
    header = F"http://localhost:"

    def add_edge(self,node1,node2):
        get(header + F"{node1}/new?port={node2}")
    
    def get_neighbours(self,node):
        try:
            return list(map(int,get(header + str(node)).text.split(',')))
        except:
            return []

    
