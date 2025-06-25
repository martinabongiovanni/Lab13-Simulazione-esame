import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.getYears()
        for year in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def handleDDYearSelection(self, e):
        pass

    def handleCreaGrafo(self,e):
        try:
            year = self._view._ddAnno.value
            if year is None:
                self._view.create_alert("Attenzione! Selezionare un anno.")
                return
            nNodes, nEdges = self._model.buildGraph(year)

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
            bestDriver, bestScore = self._model.findBestDriver(year)
            self._view.txt_result.controls.append(ft.Text(f"Best driver: {bestDriver}, with score {bestScore}"))

        finally:
            self._view._ddAnno.disabled = True
            self._view._btnCreaGrafo.disabled = True
            self._view._txtIntK.disabled = False
            self._view._btnCerca.disabled = False
            self._view.update_page()

    def handleCerca(self, e):
        try:
            dimensione = self._view._txtIntK.value
            if dimensione is None:
                self._view.create_alert("Attenzione! Inserire una dimensione.")
                return
            best_team, best_score = self._model.getDreamTeam(int(dimensione))

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Il Dream Team con il minor tasso di sconfitta pari a {best_score} è:"))
            for driver in best_team:
                self._view.txt_result.controls.append(ft.Text(f"{driver}"))

        finally:
            self._view._ddAnno.disabled = True
            self._view._btnCreaGrafo.disabled = True
            self._view._txtIntK.disabled = False
            self._view._btnCerca.disabled = False
            self._view.update_page()