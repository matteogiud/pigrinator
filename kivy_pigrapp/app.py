from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import json


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Label per visualizzare il risultato JSON
        self.result_label = Label(text="", size_hint=(1, None), size=(100, 44))
        self.retry_button = Button(
            text="Riprova", size_hint=(None, None), size=(100, 44)
        )
        self.retry_button.bind(on_press=self.send_get_request)

        # Spinner per selezionare il valore
        self.spinner = Spinner(
            text="Dove deve andare?",
            values=[],
            size_hint=(None, None),
            size=(150, 44),
        )

        self.spinner_lable = Label(
            text="Dove deve andare?", size_hint=(None, None), size=(150, 44)
        )

        # Bottone per inviare la richiesta POST
        self.button = Button(text="Vieni!", size_hint=(None, None), size=(100, 44))
        self.button.bind(on_press=self.send_post_request)
        self.bottom_layout = BoxLayout(orientation="horizontal", size_hint=(1, None))
        self.bottom_layout.add_widget(self.button)
        self.add_widget(self.result_label)
        self.add_widget(self.bottom_layout)

        # Effettua la richiesta GET quando l'app viene aperta
        self.send_get_request()

    def send_get_request(self, *args):
        url = "http://pigrinatorstand.local/searchAllPaths"  # Sostituisci con l'URL corretto per la richiesta GET
        self.disabled = True

        def on_success(request, result):
            # Parsing del risultato JSON

            values = [key for key in result.keys()]

            # Aggiorna il valore dello spinner con i valori ottenuti dal JSON
            self.spinner.values = [str(value) for value in values]
            self.result_label.text = "Pigrinator connesso!"
            # Visualizza il risultato JSON
            if self.retry_button in self.bottom_layout.children:
                self.bottom_layout.remove_widget(self.retry_button)
            if not self.spinner in self.bottom_layout.children:
                self.bottom_layout.add_widget(self.spinner)
            self.disabled = False

        def on_failure(request, result):
            self.result_label.text = "Errore, controllare che pigrinator sia connesso"
            if not self.retry_button in self.bottom_layout.children:
                self.bottom_layout.add_widget(self.retry_button)
            self.disabled = False

        headers = {"Content-Type": "application/json"}

        UrlRequest(
            url, on_success=on_success, on_failure=on_failure, req_headers=headers
        )

    def send_post_request(self, *args):
        selected_value = self.spinner.text
        if selected_value == "Dove deve andare?":
            self.result_label.text = "Selezionare un valore!!"
            return

        data = {"path_id": selected_value}

        url = "http://pigrinatorstand.local/goTo"  # Sostituisci con l'URL corretto per la richiesta POST

        def on_success(request, result):
            self.result_label.text = "Sto arrivando!"

        def on_failure(request, result):
            self.result_label.text = "Errore nella richiesta POST"

        UrlRequest(
            url, req_body=json.dumps(data), on_success=on_success, on_failure=on_failure
        )


class MyApp(App):
    def build(self):
        Window.size = (360, 640)
        return MyBoxLayout()


if __name__ == "__main__":
    MyApp().run()
