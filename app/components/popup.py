from textual import on
from textual import events
from textual.events import Key
from textual.screen import ModalScreen

from textual.containers import Grid
from textual.message import Message
from textual.widgets import Button, Input, Label


class PopupModal(ModalScreen):
    class NewTodo(Message):
        def __init__(self, description) -> None:
            super().__init__()
            self.description = description

    def compose(self):
        yield Grid(
            Label("New Todo", id="popuptitle"),
            Input(id="descriptioninput", placeholder="Description"),
            Button("Add", variant="success", id="button_confirm"),
            Button("Cancel", variant="error", id="button_cancel"),
            id="popupscreen",
        )

    @on(Key)
    def on_keypress(self, event: events.Key):
        if event.key == "escape":
            self.app.pop_screen()

    @on(Button.Pressed, "#button_confirm")
    def add(self):
        i_description = self.query_one("#descriptioninput", Input)
        self.app.pop_screen()
        self.post_message(self.NewTodo(str(i_description.value)))

    @on(Button.Pressed, "#button_cancel")
    def cancel(self):
        self.app.pop_screen()
