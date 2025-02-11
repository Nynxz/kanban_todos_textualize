from datetime import datetime

from textual import on
from app.components.kanban import Kanban
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header

from app.components.popup import PopupModal
from app.components.todo_widget import TodoWidget
from app.models.db import db
from app.models.todo import Todo, TodoStatus


def initialize_db():
    db.connect()
    db.create_tables([Todo])


def fetch_data_from_db():
    return [
        (
            target.id,
            target.description,
            target.status,
            target.date_added,
            target.date_completed,
        )
        for target in Todo.select()
    ]


class TestApp(App):
    CSS_PATH = "styles/main.tcss"

    BINDINGS = [("n", "new_todo", "New Todo")]

    todos = reactive([])

    def compose(self) -> ComposeResult:
        self.theme = "catppuccin-mocha"
        self.title = "Todos"
        yield Header()
        yield Footer()
        self.kanban = Kanban()
        yield self.kanban

    def on_mount(self):
        self.todos = fetch_data_from_db()

    def watch_todos(self, value):
        self.kanban.update_todos(value)

    def action_new_todo(self):
        self.push_screen(PopupModal())
        return

    @on(TodoWidget.TodoProgress)
    def todowidget_progress(self, event: TodoWidget.TodoProgress):
        todo = Todo.get_by_id(event.todo_id)
        match todo.status:
            case TodoStatus.todo:
                todo.status = TodoStatus.doing
                pass
            case TodoStatus.doing:
                todo.status = TodoStatus.done
                pass
            case TodoStatus.done:
                Todo.delete_by_id(event.todo_id)
                pass

        todo.save()
        self.todos = fetch_data_from_db()

    @on(PopupModal.NewTodo)
    def popup_new_todo(self, event: PopupModal.NewTodo):
        new_todo = Todo(
            status=TodoStatus.todo,
            description=event.description,
            date_added=datetime.now().strftime("%c"),
        )
        new_todo.save()
        self.todos = fetch_data_from_db()


def main():
    initialize_db()
    app = TestApp()
    app.run()


if __name__ == "__main__":
    main()
