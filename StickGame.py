''' some crude code to minmax a NIM game'''

class StickGameState:
    def __init__(self,state, turn):
        self.state = state[:]
        self.turn = turn
        
    def try_removing_nsticks_from(self,sticks, idx):
        if idx >= len(self.state) or sticks > self.state:
            return False
        self.state[idx] -= sticks
        return self
        
    def next_states(self):
        moves = [];
        
        for idx in range(0,len(self.state)):
            currentsticks = self.state[idx]
            newmoves = [StickGameState(self.state, not self.turn).try_removing_nsticks_from(i, idx)\
                        for i in range(1, currentsticks+1)]
            
            
            moves  = moves + newmoves
        return moves
    
    def is_terminal_state(self):
        return sum(self.state) == 0
    
    def get_value_terminal_state(self):
        if self.turn:
            return 1
        else:
            return -1
        
    def __repr__(self):
        if self.turn:
            out = 'my turn:\n';
        else:
            out = 'your turn\n'
            
        for sticks in self.state:
            out = out + '|' * sticks + '\n'
        return out
        
def create_n_stick_game(n):
    return StickGameState(range(1,n+1), True)     
    
    
import Queue
    
class Node:
    
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
        self.score = None
    
    def add_child(self, node):
        self.children.append(node);
        node.parent = self
    
    def get_all_leafs(self, sofar):
        if len(self.children) == 0:
            sofar.add(self)
            return sofar
        else:
            accumulated = sofar
            for child in self.children:
                accumulated = child.get_all_leafs(accumulated)
            return accumulated


def construct_entire_game_tree(game):
    tree= Node(game)
    container = Queue.LifoQueue()
    container.put(tree)
    while not container.empty():
        print container.qsize()
        this_node = container.get();
        this_game = this_node.data
        next_games = this_game.next_states()
        for nextg in next_games:
            next_node = Node(nextg)
            this_node.add_child(next_node)
            container.put(next_node)
    return tree
    
class MinMaxAgent:
    def __init__(self):
        pass
    
    def initialise(self, game):
        
        print "constructing entire game tree"
        self.tree = construct_entire_game_tree(game)
        self.score_tree()
    
    def score_tree(self):
        def score_nodes(nodes):
            def score_parent_node(node):
                child_scores = []
                for child in node.children:
                    if child.score == None:
                        return False
                    child_scores.append(child.score)
            
                if game.turn:
                    node.score = min(child_scores)
                else:
                    node.score = max(child_scores)
                return True
            
            toscore = Queue.Queue()
            
            for node in nodes:
                toscore.put(node)
            while not toscore.empty():
                node = toscore.get()
                game = node.data
                if not node.parent == None:
                    toscore.put(node.parent)
                if game.is_terminal_state():
                    node.score = game.get_value_terminal_state()
                else:
                    scored = score_parent_node(node)
                    if not scored:
                        toscore.put(node)
                                              
        tree = self.tree
        leaf_nodes = tree.get_all_leafs(set())
        score_nodes(leaf_nodes)
        
        
