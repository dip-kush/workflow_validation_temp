from DomComparator import htmlCompare
from logger import LoggerHandler
import GetClickables
import networkx as nx

logger = LoggerHandler(__name__)


class NodeData:
    ''' Initializing the Each State of StateMachine'''

    def __init__(self):
        self.link = ""
        self.domString = ""
        self.title = ""
        self.index = -1
        self.visited = 0
        self.clickables = []
        # print self.domString


class StateMachine:
    '''Initializing the State Machine with A Multi Directed Graph'''

    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def addNode(self, number, data):
        '''
        Adding the State in the FSM assigning the nodenumber and 
        data to the node self.graph.node[number]['nodedata'] = data
         '''

        self.graph.add_node(number, nodedata=data)

    def addEdges(self, n1, n2, et):
        ''' Adding a edge from node n1 to n2 '''

        self.graph.add_edge(n1, n2, event=et)

    def checkNodeExists(self, dom):
        ''' 
        Checks if a State already exists by 
        checking the DomString of all the StateNodes 
        '''

        for n in self.graph.nodes():
            # print self.graph.node[n]['nodedata']
            if htmlCompare(dom, None, self.graph.node[
                           n]['nodedata'].domString):
                ''' Comparing the Dom String of the two State Nodes '''
                return n
        return -1

    def numberOfNodes(self):
        ''' Returns the number of Nodes in a graph '''

        return self.graph.number_of_nodes()


class MyGraph(nx.MultiGraph):
    ''' Temporary Graph Class'''

    def __init__(self):
        pass


'''

n1=NodeData()
n2=NodeData()
n1.domString="abc"
n1.domAddressPath="xyz"
n2.domString="abc"
n2.domAddressPath="abc";
s=StateMachine()
s.addNode(n1)
s.addNode(n2)
print s.graph.node[0]
s.addEdges(0,1)
'''
