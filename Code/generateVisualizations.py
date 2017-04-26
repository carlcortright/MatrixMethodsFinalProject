################################################################################
# Parse the edges from our edges files to a CSV files
#
# Authors:
# Date: 4/23/2017
#
################################################################################
import csv
from graph_tool.all import *

g = Graph(directed=False)
vpropName = g.new_vertex_property("string")
vertNames = []
vertices = []

print("Creating Graph...")
with open("0Ego.csv", "r") as adjFile:
    adjReader = csv.reader(adjFile)
    vertNames = adjReader.__next__()[1:]
    g.add_vertex(len(vertNames))
    for i in range(len(vertNames)):
        vpropName[g.vertex(i)] = vertNames[i]
    for line in adjReader:
        lineTrimmed = line[1:]
        baseIndex = vertNames.index(lineTrimmed[0])
        for entry in range(len(lineTrimmed)):
            if(lineTrimmed[entry] == "1" and baseIndex != entry):
                g.add_edge(g.vertex(baseIndex), g.vertex(entry))

# Generating Image
print("Generating Image...")
pos = planar_layout(g)
graph_draw(g, pos=pos, output_size=(2000, 2000), output="Images/0Ego.png")


# g = Graph()
# v1 = g.add_vertex()
# v2 = g.add_vertex()
#
# e = g.add_edge(v1, v2)
# graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="two-nodes.png")
