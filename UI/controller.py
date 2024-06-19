import copy

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_team = None
        self.teams = []

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        if len(self.teams) == 0:
            self._view._txt_result.controls.append(ft.Text("Selezionare le squadre!", color='red'))
            self._view.update_page()
            return
        else:
            self._model.createGraph(self.teams, self._view._ddAnno.value)
            self._view._txt_result.controls.append(ft.Text(self._model.getGraphDetails()))
            self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        if len(self.teams) == 0:
            self._view._txt_result.controls.append(ft.Text("Selezionare le squadre!", color='red'))
            self._view.update_page()
            return
        else:
            if self._view._ddSquadra.value is None:
                self._view._txt_result.controls.append(ft.Text("Selezionare la squadra!", color='red'))
                self._view.update_page()
                return
            elif len(self._model.graph.nodes) == 0:
                self._view._txt_result.controls.append(ft.Text("Creare il grafo!", color='red'))
                self._view.update_page()
                return
            else:
                vicini = self._model.getDettagli(self._selected_team)
                for vicino in vicini:
                    self._view._txt_result.controls.append(ft.Text(f"squadra: {vicino[0]}, peso: {vicino[1]}"))
                self._view.update_page()

    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view._txt_result.controls.append(ft.Text("Creare il grafo!", color='red'))
            self._view.update_page()
            return
        if self._view._ddSquadra.value is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare la squadra!", color='red'))
            self._view.update_page()
            return
        path = self._model.getPath(self._selected_team)
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato con {len(self._model._bestPath)} nodi e {self._model.bestObjVal} peso"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p[0]} -- {p[1]}"))
            self._view.update_page()



    def fillDDAnno(self):
        years = self._model.getYears()
        years_options = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = years_options
        self._view.update_page()

    def handleSquadre(self, e):
        squadre = self._model.getSquadre(str(self._view._ddAnno.value))
        self.teams = copy.deepcopy(squadre)
        self._view._txtOutSquadre.controls.clear()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Squadre nell'anno {self._view._ddAnno.value}: {len(squadre)}"))
        i = 0
        for squadra in squadre:
            self._view._txt_result.controls.append(ft.Text(squadra.teamCode))
            self._view._txtOutSquadre.controls.append(ft.Text(f"Squadra {i}"))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data=squadra, text=squadra.teamCode, on_click=self.readDDteams))
            i += 1
        self._view.update_page()

    def readDDteams(self, e):
        if e.control.data is None:
            self._selected_team = None
        else:
            self._selected_team = e.control.data
