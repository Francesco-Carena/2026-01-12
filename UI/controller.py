import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddyear(self):
        anni=self._model.getAllYears()
        for a in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(a))
            self._view._ddAnno2.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def handleCreaGrafo(self,e):
        anno1=self._view._ddAnno1.value
        anno2=self._view._ddAnno2.value
        if anno1 is None or anno2 is None:
            self._view.create_alert("Selezionare un valore dai dd")
            self._view.update_page()
            return
        self._model.createGraph(int(anno1), int(anno2))

        nodi, archi=self._model.getInfoGraph()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nodi} nodi e {archi} archi"))
        self._view.update_page()


    def handleDettagli(self, e):
        if self._model._graph.nodes is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        edges, ncompo, bigcompo=self._model.getDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"I 3 archi più grandi del grafo:"))
        for e in edges:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} - {e[1]} : {e[2]["weight"]}"))
        self._view.txt_result.controls.append(ft.Text(f"\nCi sono {ncompo} compo"))
        self._view.txt_result.controls.append(ft.Text(f"\nComponente connessa maggiore ha dimensione {len(bigcompo)} ed è formata da:"))
        for e in bigcompo:
            self._view.txt_result.controls.append(ft.Text(f"{e}"))

        self._view.update_page()

    def handleCerca(self, e):
        if self._model._graph.nodes is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        k=self._view._txtInK.value
        if k is None:
            self._view.create_alert("Inserire valore numerico")
            self._view.update_page()
            return
        try:
            k=int(k)
        except ValueError:
            self._view.create_alert("Inserire valore numerico")
            self._view.update_page()
            return
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value
        path, score=self._model.searchPath(int(anno1), int(anno2), k)
        if score==-1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Trovato nessun cammino o impossibile"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino trovato con {len(path)} nodi e punteggio di {score}"))
        for e in path:
            self._view.txt_result.controls.append(ft.Text(f"{e}"))

        self._view.update_page()

