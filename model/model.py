from itertools import combinations

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.albums = []
        self.nodi = []
        self.best_path = []


    def create_graph(self, durata):
        self.nodi = DAO.get_album(durata)
        diz_playlist_album = DAO.get_playlist_album()


        for nodo in self.nodi:
            self.G.add_node(nodo.id)    # AGGIUNGO COME NODO SOLO L'ID DELL'ALBUM
            self.albums.append(nodo.title)

        for (a1, a2) in combinations(self.nodi, 2):
            id1 = a1.id
            id2 = a2.id

            # se entrambi gli album[i] sono nel dizionario playlist --> album_id[i], allora li collego
            for playlist in diz_playlist_album:
                album_nella_playlist = diz_playlist_album[playlist]  #recupero la lista di album

                if id1 in album_nella_playlist and id2 in album_nella_playlist:
                    self.G.add_edge(id1, id2)
                    break

    def get_graph_details(self):
        componenti_connesse = list(nx.connected_components(self.G))

        dim_componente_connessa = len(componenti_connesse)

        n_nodi = self.G.number_of_nodes()
        n_archi = self.G.number_of_edges()

        return dim_componente_connessa, n_nodi, n_archi

    def get_durata_album(self, a1):
        id_trovato = None

        # self.nodi contiene tutti gli oggetti Album scaricati dal DB
        for album in self.nodi:
            if album.title == a1:
                id_trovato = album.id
                break

        # METODO PER TROVARE LA COMPONENTE CONNESSA DI UN SOLO GRAFO
        componente_connessa_a1 = list(nx.node_connected_component(self.G, id_trovato))

        durata_totale = 0
        for album in self.nodi:
            durata_album = album.duration

            if album.id in componente_connessa_a1:
                durata_totale += durata_album

        return durata_totale

    def get_best_path(self, a1_titolo, durata_max):
        self.best_path = []

        # 1. Recupero l'oggetto album iniziale (ci serve id e durata)
        start_album = None
        for album in self.nodi:
            if album.title == a1_titolo:
                start_album = album
                break

        componente_connessa_ids = list(nx.node_connected_component(self.G, start_album.id))

        parziale = [(start_album.title, start_album.duration)]

        self.ricorsione(parziale, componente_connessa_ids, durata_max, start_album.duration)

        return self.best_path

    def ricorsione(self, parziale, componente_connessa_ids, durata_max, durata_attuale):
        # Ho fatto meglio di prima?
        if len(parziale) > len(self.best_path):
            self.best_path = list(parziale)

        for album in self.nodi:
            titoli_in_parziale = [x[0] for x in parziale]

            if album.title not in titoli_in_parziale:
                # Se fa parte della componente connessa
                if album.id in componente_connessa_ids:

                    if (durata_attuale + album.duration) <= durata_max:
                        parziale.append((album.title, album.duration))

                        # Passo la NUOVA somma alla ricorsione
                        self.ricorsione(parziale, componente_connessa_ids, durata_max, durata_attuale + album.duration)

                        parziale.pop()
