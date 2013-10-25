from abc import abstractmethod
from abc import ABCMeta 
''' This script implements A* searches, as inspired by the Artificial Intelligence, a modern approach'''

class AGameState(object):
        '''provide an interface to define a problem. Each problem must provide 
        following methods:
            
            is_solved(self)   : returns true if the problem has been solved
            next_states(self) : returns an array of game states that can follow
            after this state
            n_moves(self)     : the number of moves that lead to this position
        
        it must also provide the following members:
            parent: the GameState that this state follows from (None if this is the initial state)
        '''
        
        __meta_class__ = ABCMeta
        
        @abstractmethod
        def is_solved(self):
            pass
        
        
        @abstractmethod
        def next_states(self):
            pass
        
        
        @abstractmethod
        def n_moves(self):
            pass

class AHashableGameState(AGameState):
    ''' in order to perform a search without repeats, it must be possible to obtain
    a unique hash value for a game. Hence a hashable game state must implement the 
    method:
        __hash__(self) : return an integer that uniquely defines the game'''
        
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __hash__():
        pass

class AGameStateWithHeuristics(AGameState):
    ''' a game state that allows heuristics must implement a comparison method. 
    The comparison function will return the comparison between the fitness function 
    of each state. '''
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def heuristic_distance(self):
        pass
        
    def __cmp__(self, other):
        selfV = self.n_moves() + self.heuristic_distance() 
        otherV=other.n_moves() + other.heuristic_distance() 
        return cmp(selfV, otherV)

class NoRepeatSearchForSolution:
    ''' Search through the solution space untill a solution is found.
    
    constructor(problem, container) : the initial problem state and a container 
    to hold the search stack is injected to the solver. Note that problem must 
    implement AHashableGameState to qualify for inclusion.
    
    NoRepeataSearchForSolution.search(self) : returns the solution state (note that by 
    looking at its parents you can get the path to the solution). If the solution cannot 
    be found, return None after the tree is exhaustively searched'''
    
    def __init__(self,problem, container):
        self.problem = problem
        # store a container with the next states to visit and a visited hashed map
        # to ensure that states are only visited once at most
        self.container = container
        self.container.put(self.problem)
        self.visited = set()
        self.iterations = 0;
        
    def search(self):
        self.iterations = 0;
        while not self.container.empty():
            self.iterations +=1;

            current_state = self.container.get()
                
            if current_state.is_solved():
                return current_state
                
            new_states = current_state.next_states();
            for next_state in new_states:
                # if the state is not already in the search path, add it in.
                if not next_state in self.visited:
                    self.container.put(next_state)
                    self.visited.add(next_state)
        return None

class AStarSearchForSolution(NoRepeatSearchForSolution):
    ''' AStarSearchForSolution performs an A* search for a solution. '''
    def __init__(self, problem):
        import Queue
        container = Queue.PriorityQueue()
        NoRepeatSearchForSolution.__init__(self, problem, container)


class EightPuzzle(AHashableGameState,AGameStateWithHeuristics):
    ''' Describe an eight puzzle - see http://en.wikipedia.org/wiki/15_puzzle
    for details'''
    
    def __init__(self, state):
        self.state = state
        self.parent = None
        
    def heuristic_distance(self):
        '''returns a heuristic distance from the solution'''
        expected_coord = [ [i%3, i/3] for i in range(9)]
        actual_coord   = [ [i%3, i/3] for i in self.state]
        distances      = [ abs(actual_coord[i][0] - expected_coord[i][0]) + \
                           abs(actual_coord[i][1] - expected_coord[i][1]) \
                           for i in range(9)]
        return sum (distances)
    
    def is_solved(self):
        '''returns true or false depending on whether the problem is solved'''
        return self.state == range(9)
        
    def next_states(self):
        '''returns the next moves'''
        empty_index = self.state.index(0)
        neighbors = [-1,+1,+3,-3]
        poss_index = [ empty_index + n 
                        for n in neighbors 
                        if empty_index + n >= 0 and empty_index+n < 9]
        future_states = []
        for idx in poss_index:
            newstate = self.state[:]
            newstate[empty_index] , newstate[idx] =newstate[idx],newstate[empty_index]   
            newProblem = EightPuzzle(newstate)
            newProblem.parent =self
            future_states.append(newProblem)
        return future_states  
        
    def n_moves(self):
        if self.parent is not None:
            return 1 + self.parent.n_moves()
        else:
            return 1
    def __hash__(self):
        return sum([9**i *self.state[i] for i in range(9)])
        
    def __repr__(self):
        out = ''
        count =0
        for s in self.state:
            count += 1
            if s==0:
                out = out+' '
            else:
                out = out + '{0}'.format(s)
            if count  == 3:
                out = out +'\n'
                count = 0;
            
        return out+'\n'
    
    def represent_history(self):
        
        if self.parent is not None:
            return self.__repr__() + '\n\n'+ self.parent.represent_history()
        else:
            return self.__repr__()

# worst case is (apparently) the worst case scenario for solution.
worstcase = EightPuzzle([8,0,6,5,4,7,2,3,1])

def report_a_solution(searcher, solution):
    
    if solution is not None:
        print "Found a solution using: {0} iterations".format(searcher.iterations)
        print "The full set of moves to solve the puzzle are (in reverse order):"
        print solution.represent_history()
    else:
        print "Solution NOT found!"
        
def solve_using_AStar():
    searcher = AStarSearchForSolution(worstcase)
    solution = searcher.search()
    report_a_solution(searcher, solution)
    
def solve_using_BreadthFirstSearch():
    import Queue
    searcher = NoRepeatSearchForSolution(worstcase, Queue.Queue())
    solution = searcher.search()
    report_a_solution(searcher, solution)
    
    
    

        
        
        