from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from datetime import datetime
from collections import deque


class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

            ##elif adicional, simula agentes que n somente querem estar proximos a agentes similares mas tambem querem distancia de agentes diferentes.
            elif(self.model.distaste == True):
                if neighbor.type != self.type:
                    similar -= 1
            
            
        #similar = similar/self.model.homophily
        # If unhappy, move:
        ## tambem foi adicionado uso da variavel adversity, que simula a possibilidade de agentes terem que se mudar mesmo estando proximos a similares
        if similar < self.model.homophily or self.model.adversity > self.random.random():
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """
    ## adicionado variavel distate e adversity.
    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3, adversity=0, distaste = True):
        """ """

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.adversity = adversity  ## quanto maior mais chance de agentes terem que se mudar mesmo estando felizes.
        self.distaste = distaste    ## quando True agentes discostam de estar proximos a agentes diferentes.

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0

        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},    
        )


        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False

## As funcoes isSafe BFS e minority_cluster calculam os clusters formados por agentes da minoria
## Foram feitas com referencia a https://www.geeksforgeeks.org/islands-in-a-graph-using-bfs/
def isSafe(mat, i, j, vis):   

    return  mat[i][j] == 2 and (not vis[i][j])

def BFS(mat, vis, si, sj):
     
    # These arrays are used to get row and
    # column numbers of 8 neighbours of
    # a given cell
    row = [-1, -1, -1, 0, 0, 1, 1, 1]
    col = [-1, 0, 1, -1, 1, -1, 0, 1]
 
    # Simple BFS first step, we enqueue
    # source and mark it as visited
    q = deque()
    q.append([si, sj])
    vis[si][sj] = True
 
    # Next step of BFS. We take out
    # items one by one from queue and
    # enqueue their univisited adjacent
    while (len(q) > 0):
        temp = q.popleft()
 
        i = temp[0]
        j = temp[1]
 
        # Go through all 8 adjacent
        for k in range(8):
            ik = (i + row[k])%20
            jk = (j + col[k])%20

            if (isSafe(mat, ik, jk, vis)):
                
                vis[ik][jk] = True
                q.append([ik, jk])
 

def minority_clusters(model):
    vis = [[False for i in range(model.height)]
                  for i in range(model.width)]

    n_minclusters = 0
   

    mat = [[ 0 for i in range(model.height)]
                  for i in range(model.width)]

    for cell in model.grid.coord_iter():
        pos = cell[1],cell[2]
        if not model.grid.is_cell_empty(pos):
            mat[cell[1]][cell[2]] = cell[0].type + 1


    for i in range(model.height):
        for j in range(model.width):
            if (mat[i][j] == 2 and not vis[i][j]):        
                BFS(mat, vis, i, j)      
                n_minclusters += 1    
    ##print()
    ##for i in range(20):
    ##    print(mat[i])
    ##print("clusters = " + str(n_minclusters))
    return n_minclusters

## calcula a media vizinhos do mesmo tipo que cada agente tem
## Feita com referencia a uma funcao do meu colega Alec
def neighborhood_mean(model):
    ret = sum([sum(1 for y in model.grid.neighbor_iter(x.pos) if y.type == x.type) for x in model.schedule.agents if not model.grid.is_cell_empty(x.pos)])/len([x for x in model.schedule.agents if not model.grid.is_cell_empty(x.pos)])
    ##print(ret)
    return  round(ret, 2)

## calcula quantidade de agentes felizes
def happy(model):
    return model.happy


def batch_run():
    fix_params = {
        
        "height": 20,
        "width": 20,
        "distaste" : [True]
        
       
    }
    variable_params = {

        "density" : [0.5,0.7,0.9],
        "minority_pc":[0.2,0.4],
        "homophily": [2,3,4],
        "adversity": [0,0.01,0.02]
        
    }
    #540 total
    experiments_per_parameter_configuration = 10
    max_steps_per_simulation = 400
    # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
    batch_run = BatchRunner(
        Schelling,
        variable_params,
        fix_params,   
        iterations = experiments_per_parameter_configuration,
        max_steps = max_steps_per_simulation,
        model_reporters = {        
            "happy" : happy,
            "Minority_clusters" : minority_clusters,
            "neighborhood_mean" : neighborhood_mean
        },  
        
    )
    
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    #run_agent_data = batch_run.get_agent_vars_dataframe() 

    now = datetime.now().strftime("%Y-%m-%d")
    file_name_suffix =  ("_iter_"+str(experiments_per_parameter_configuration)+
                        "_steps_"+str(max_steps_per_simulation)+"_distaste_true_"+now
                        )
    run_model_data.to_csv("model_data"+file_name_suffix+".csv")
    #run_agent_data.to_csv("agent_data"+file_name_suffix+".csv")