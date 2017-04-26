################################################################################
# Parse the edges from our edges files to a CSV files
#
# Authors:
# Date: 4/23/2017
#
################################################################################
import glob
import csv
import re
import progressbar
import copy

EGO_REGEX = re.compile('\d+')

#
# Parses an edges file and returns a 2D list of edges
#
def parseEgoFile(path, edges):
    # Open the ego file and get the ego node
    egofile = open(path, "r")
    egoNode = int(EGO_REGEX.findall(path)[0])
    # Loop through the file creating all of the edges
    for line in egofile:
        nodes = EGO_REGEX.findall(line.rstrip())
        n1 = nodes[0]
        n2 = nodes[1]
        if(egoNode in edges.keys()):
            edges[egoNode].append(n1)
            edges[egoNode].append(n2)
        else:
            edges[egoNode] = []
            edges[egoNode].append(n1)
            edges[egoNode].append(n2)
        if(n1 in edges.keys()):
            edges[n1].append(n2)
            edges[n1].append(egoNode)
        else:
            edges[n1] = []
            edges[n1].append(n2)
            edges[n1].append(egoNode)
        if(n2 in edges.keys()):
            edges[n2].append(n1)
            edges[n2].append(egoNode)
        else:
            edges[n2] = []
            edges[n2].append(n1)
            edges[n2].append(egoNode)
    return edges

################################################################################
# Get all of the edges from ego files
################################################################################
egoPaths = glob.glob("Edges/0.edges")
# Parse each file to one big edges dictionary
edges = {}
for path in egoPaths:
    edges = parseEgoFile(path, edges)

################################################################################
# Export the adjacency matrix to a csv
################################################################################
print("Writing matrix to CSV...")
nodes = list(set(edges.keys()))
# Create the diagonal
for node in nodes:
    edges[node].append(node)

with open("0Ego.csv", "r+") as adjMatrixFile:
    adjwriter = csv.writer(adjMatrixFile)
    header = copy.copy(nodes)
    header.insert(0, "")
    adjwriter.writerow(header)
    bar = progressbar.ProgressBar()
    for node in bar(nodes):
        adjList = edges[node]
        row = [node]
        for testNode in nodes:
            if(testNode in adjList):
                row.append(1)
            else:
                row.append(0)
        adjwriter.writerow(row)
