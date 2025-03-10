import json

class BasicGraph:
    def __init__(self, graph):
        self.graph = graph
    
    def generate(self):
        graph_processed = {
            "data" : {"grad": self.graph.get("grad"),
                      "coeffizienten" : process_coef(self.graph.get("coeffizienten"))},
            "option" : {
                "xAxis": {
                "name": "x",
                "max": self.graph.get("max_x"),
                "min": self.graph.get("min_x")
                },
                "yAxis": {
                "name": "y",
                "max": self.graph.get("max_y"),
                "min": self.graph.get("min_y")
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
    
    split_coef = raw_coef.split(",")
    for coef in split_coef:
        coef = float(coef)
    return split_coef