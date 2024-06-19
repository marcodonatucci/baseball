import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.bestObjVal = None
        self._bestPath = None
        self.graph = nx.Graph()
        self.all_squadre = []
        self.idMap = {}

    def getYears(self):
        return DAO.get_all_years()

    def getSquadre(self, year):
        self.all_squadre = DAO.get_all_teams(year)
        self.idMap = {t.ID: t for t in self.all_squadre}
        return self.all_squadre

    def createGraph(self, teams, year):
        self.graph.clear()
        self.graph.add_nodes_from(teams)
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if node1 != node2:
                    self.graph.add_edge(node1, node2)
        salari = DAO.get_all_weights(year, self.idMap)
        for e in self.graph.edges:
            self.graph[e[0]][e[1]]['weight'] = salari[e[0]] + salari[e[1]]

    def getGraphDetails(self):
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."

    def getDettagli(self, team):
        vicini = self.graph.neighbors(team)
        result = []
        for vicino in vicini:
            result.append((vicino.name, self.graph[team][vicino]['weight']))
        return result

    # metodo che gestisce la ricorsione, inizializza le variabili, gestisce il caching e le condizioni
    def getPath(self, v0):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestPath = []
        self.bestObjVal = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [v0]
        listaVicini = []
        # per ogni vicino del nodo iniziale
        for v in self.graph.neighbors(v0):
            edgeV = self.graph[v0][v]["weight"]  # peso arco che mando in ricorsione: arco dall'ultimo nodo della soluzione parziale a quello corrente
            listaVicini.append((v, edgeV))  # metto nella lista dei vicini una tupla con il nodo e il peso per arrivarci
        listaVicini.sort(key=lambda x: x[1],
                         reverse=True)  # sort sulla base del peso in modo da mandare in ricorsione solo quello più pesante (greedy)
        parziale.append(listaVicini[0][0])  # aggiungo al parziale il nodo che ho selezionato e inizio la ricorsione
        self._ricorsionev2(parziale)
        parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self.getWeightsOfPath(self._bestPath)
        # for v in self._grafo.neighbors(v0):
        #     parziale.append(v)
        #     self._ricorsione(parziale)
        #     parziale.pop()

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di best
        if self._getScore(parziale) > self.bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self.bestObjVal = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        for v in self.graph.neighbors(parziale[-1]):
            edgeW = self.graph[parziale[-1]][v]["weight"]  # peso arco che mando in ricorsione
            if (v not in parziale and
                    self.graph[parziale[-2]][parziale[-1]]["weight"] > edgeW):
                parziale.append(v)
                # si itera di nuovo tutti i nodi, non efficiente
                self._ricorsione(parziale)
                parziale.pop()
        # aggiungo e faccio ricorsione
        pass

    def _ricorsionev2(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if self._getScore(parziale) > self.bestObjVal:
            # se lo è aggiorno i valori migliori
            self._bestPath = copy.deepcopy(parziale)
            self.bestObjVal = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        listaVicini = []
        # per ogni vicino dell'ultimo nodo del percorso:
        for v in self.graph.neighbors(parziale[-1]):

            edgeV = self.graph[parziale[-1]][v]["weight"]  # peso arco che mando in ricorsione
            listaVicini.append((v, edgeV))
            # solito sort
        listaVicini.sort(key=lambda x: x[1], reverse=True)
        for v1 in listaVicini:
            # per ogni vicino trovato, se il nodo non è nella soluzione parziale, e il peso del suo predecessore è maggiore del suo
            if (v1[0] not in parziale and
                    self.graph[parziale[-2]][parziale[-1]]["weight"] > v1[1]):
                parziale.append(v1[0]) # aggiungo il nodo, faccio la ricorsione e poi la return, perchè gli altri sono sicuro peggiori ( lista ordinata )
                self._ricorsionev2(parziale)
                parziale.pop()
                return
        pass
        # aggiungo e faccio ricorsione

    def _getScore(self, listOfNodes):
        # funzione per calcolare il peso totale di un cammino
        if len(listOfNodes) == 1:
            return 0
        score = 0
        for i in range(0, len(listOfNodes) - 1):
            score += self.graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return score

    def getSortedNeighbors(self, v0):
        # funzione per ottenere una lista di vicini ordinata per peso
        vicini = self.graph.neighbors(v0)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self.graph.edges[v0][v]["weight"]))
        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return viciniTuples

    def getWeightsOfPath(self, path):
        listTuples = [(path[0], 0)]
        for i in range(0, len(path)-1):
            listTuples.append((path[i+1], self.graph[path[i]][path[i+1]]['weight']))
        return listTuples

