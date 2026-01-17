import flet as ft
import networkx as nx

from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def get_durata(self, e):
        return self._view.txt_durata.value

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        durata = int(self.get_durata(e))
        self._model.create_graph(durata)

        albums = self._model.albums

        dim_componente_connessa, n_nodi, n_archi = self._model.get_graph_details()

        self._view.dd_album.options.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {n_nodi} album, {n_archi} archi"))
        for a in albums:
            self._view.dd_album.options.append(ft.dropdown.Option(a))

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        album_selezionato = self._view.dd_album.value
        print("Album salvato con successo!")

        return album_selezionato

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        dim_componente_connessa, n_nodi, n_archi = self._model.get_graph_details()

        a1 = self._view.dd_album.value
        durata_comp_connessa_a1 = self._model.get_durata_album(a1)

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {dim_componente_connessa}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Durata totale: {durata_comp_connessa_a1}."))

        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        a1_titolo = self._view.dd_album.value
        durata_max = int(self._view.txt_durata_totale.value)

        album_set = self._model.get_best_path(a1_titolo, durata_max)

        self._view.lista_visualizzazione_3.controls.clear()
        for album, durata in album_set:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{album} ({durata} minuti)"))

        self._view.update()