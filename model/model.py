import copy
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.DiGraph()
        self._drivers = []
        self._id_map_drivers = {}

        self._best_team = []
        self._best_score = 0

    def getYears(self):
        return DAO.getAllYear()

    def buildGraph(self, year):
        self._grafo.clear()

        self.fillIDMapDrivers(year)
        self._grafo.add_nodes_from(self._drivers)
        allEdges = DAO.getAllResultsByYear(year, self._id_map_drivers)
        for e in allEdges:
            self._grafo.add_edge(e[0], e[1], weight=e[2])
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def findBestDriver(self, grafo):
        bestScore = 0
        bestDriver = None
        for node in self._grafo.nodes():
            final_score = 0
            for edge_out in self._grafo.out_edges(node, data=True):
                final_score += edge_out[2]["weight"]
            for edge_in in self._grafo.in_edges(node, data=True):
                final_score -= edge_in[2]["weight"]

            if final_score > bestScore:
                bestScore = final_score
                bestDriver = node
        bestDriver = self._id_map_drivers[bestDriver]
        return bestDriver, bestScore


    def fillIDMapDrivers(self, year):
        self._drivers = DAO.getAllDriversByYear(year)
        for driver in self._drivers:
            self._id_map_drivers[driver.driverId] = driver

    def getDreamTeam(self, dimensione):
        self._best_team = []
        self._best_score = 100000 # per inizializzare a un valore molto alto
        temp_team = []
        self.ricorsione(temp_team, dimensione)
        lista_drivers_best_team = []
        for driver in self._best_team:
            lista_drivers_best_team.append(self._id_map_drivers[driver.driverId])
        return self._best_team, self._min_score

    def ricorsione(self, temp_team, dimensione):
        if len(temp_team) == dimensione:
            score = self.getScore(temp_team)
            if score < self._best_score:
                self._min_score = score
                self._best_team = copy.deepcopy(temp_team)
            return

        for driver in self._drivers:
            if driver not in temp_team:
                temp_team.append(driver)
                self.ricorsione(temp_team, dimensione)
                temp_team.pop() # backtracking

    def getScore(self, temp_team):
        score = 0
        for edge in self._grafo.edges(data=True):
            if edge[0] not in temp_team and edge[1] in temp_team: # analizzo gli archi entranti nel team
                score += edge[2]["weight"]
        return score