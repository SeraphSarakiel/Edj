import json

class BasicGraph:
    def __init__(self, graph):
        self.graph = graph
    
    def generate(self):
        graph_processed = {
            "data" : {"grad": self.graph["grad"],
                      "coeffizienten" : process_coef(self.graph["coeffizienten"])},
            "option" : {
                "xAxis": {
                "name": "x",
                "max": self.graph["max_x"],
                "min": self.graph["min_x"]
                },
                "yAxis": {
                "name": "y",
                "max": self.graph["max_y"],
                "min": self.graph["min_y"]
                },
                "series": [
                {
                    "showSymbol": False,
                    "type": "line"
                }
                ]
            }
        }
        return json.dumps(graph_processed)
    
def process_coef(raw_coef):
    result_coef = []
    split_coef = raw_coef.split(",")
    for coef in split_coef:
        result_coef.append(int(coef))        
    return result_coef