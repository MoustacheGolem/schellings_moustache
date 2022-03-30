from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Schelling


class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)




def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal


happy_element = HappyElement()
canvas_element = CanvasGrid(schelling_draw, 30, 30, 500, 500)
happy_chart = ChartModule([{"Label": "happy", "Color": "Green"}])
cluster_chart = ChartModule([{"Label": "cluster_count", "Color": "Blue"},{"Label": "cluster_size_avarage", "Color": "Purple"}])

model_params = {
    "height": 30,
    "width": 30,
    "density": UserSettableParameter("slider", "Agent density", 0.7, 0.1, 1.0, 0.1),
    "minority_pc": UserSettableParameter(
        "slider", "Fraction minority", 0.2, 0.00, 0.5, 0.05
    ),
    "homophily": UserSettableParameter("slider", "Homophily", 3, 1, 8, 1),
    #"adversity": UserSettableParameter("slider", "Adversity", 0, 0.0, 0.2, 0.01), ## adiciona slider de advercity.
    "distaste": UserSettableParameter("slider", "Distaste",1,0,2,0.25),          ## adiciona checkbos de distaste.
}

server = ModularServer(
    Schelling, [canvas_element, happy_element, cluster_chart, happy_chart], "Schelling", model_params
)
