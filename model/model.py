import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMap={}

        self._bestPath=[]
        self._bestScore=999

    def getAllYears(self):
        return DAO.getAllYears()

    def createGraph(self, anno1, anno2):
        self._graph.clear()
        self._idMap={}

        nodes=DAO.getNodes(anno1,anno2)
        for node in nodes:
            self._idMap[node.constructorId]=node
        self._graph.add_nodes_from(nodes)

        self._addEdges(anno1,anno2)

    def _addEdges(self, anno1, anno2):
        edges=DAO.getEdges(anno1,anno2)
        for edge in edges:
            n1=self._idMap[edge[0]]
            n2=self._idMap[edge[1]]
            self._graph.add_edge(n1,n2, weight=edge[2])

    def getInfoGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getDetails(self):
        edges=list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'], reverse=True)

        compo=list(nx.connected_components(self._graph))
        biggest=max(compo,key=len)
        nodi_con_grado = [(n, self._graph.degree(n)) for n in biggest]
        nodi_con_grado.sort(key=lambda x: x[1], reverse=True)

        return edges[:3], len(compo), nodi_con_grado

    def searchPath(self, anno1, anno2, k):
        self._bestPath = []
        self._bestScore = float('inf')

        eta = DAO.getAllOld(anno1, anno2)
        for nodeId, old in eta.items():
            if nodeId in self._idMap:
                self._idMap[nodeId].oldest_driver_dob = old
        compo = [list(c) for c in nx.connected_components(self._graph)]
        if k > len(compo):
            return [], -1
        print("inizio")
        self._ricorsione([], 0, compo, k)
        print("final")

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, livello, compo, k):
        if len(parziale) == k:
            date_veterani = [c.oldest_driver_dob for c in parziale if c.oldest_driver_dob is not None]
            if len(date_veterani) == k:
                score = (max(date_veterani) - min(date_veterani)).days
                if score < self._bestScore:
                    self._bestScore = score
                    self._bestPath = copy.deepcopy(parziale)
            return

        if livello == len(compo):
            return

        for costruttore in compo[livello]:
            parziale.append(costruttore)
            self._ricorsione(parziale, livello + 1, compo, k)
            parziale.pop()

        componenti_rimaste = len(compo) - livello - 1
        nodi_mancanti = k - len(parziale)

        if componenti_rimaste >= nodi_mancanti:
            self._ricorsione(parziale, livello + 1, compo, k)
