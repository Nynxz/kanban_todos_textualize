from textual import on
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.widgets import Button, Static

from app.models.todo import TodoStatus


class TodoWidget(HorizontalGroup):
    class TodoProgress(Message):
        def __init__(self, todo_id) -> None:
            super().__init__()
            self.todo_id = todo_id

    def __init__(self, description="Todo") -> None:
        super().__init__()
        self.description = description

    def compose(self):
        yield Static(f"{self.description[1]}")
        yield Button(">")

    def on_mount(self):
        btn = self.query_one(Button)
        match self.description[2]:
            case TodoStatus.todo:
                btn.add_class("yellow")
            case TodoStatus.doing:
                btn.label = "✅"
            case TodoStatus.done:
                btn.add_class("red")
                btn.label = "❌"

    @on(Button.Pressed)
    def on_button_pressed(self):
        self.post_message(self.TodoProgress(self.description[0]))
