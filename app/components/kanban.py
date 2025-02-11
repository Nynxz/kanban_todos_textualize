from textual.containers import Horizontal, VerticalScroll

from app.components.todo_widget import TodoWidget
from app.models.todo import TodoStatus


class Kanban(Horizontal):
    def __init__(self, todos=[], **kwargs):
        super().__init__(**kwargs)
        self.todos = todos

    def compose(self):
        self.k_todos = VerticalScroll(
            *[TodoWidget() for _ in self.todos],
            id="kanban_todo",
            classes="kanban_panel",
        )

        self.k_doing = VerticalScroll(
            TodoWidget(), id="kanban_doing", classes="kanban_panel"
        )

        self.k_done = VerticalScroll(
            TodoWidget(), id="kanban_done", classes="kanban_panel"
        )

        yield self.k_todos
        yield self.k_doing
        yield self.k_done

    def render_kanban(self):
        # Clear existing widgets
        self.k_todos.remove_children()
        self.k_doing.remove_children()
        self.k_done.remove_children()

        # Filter todos by status
        todos = [todo for todo in self.todos if todo[2] == TodoStatus.todo]
        doing = [todo for todo in self.todos if todo[2] == TodoStatus.doing]
        done = [todo for todo in self.todos if todo[2] == TodoStatus.done]

        # Add widgets for each todo
        self.k_todos.mount_all([TodoWidget(todo) for todo in todos])
        self.k_doing.mount_all([TodoWidget(todo) for todo in doing])
        self.k_done.mount_all([TodoWidget(todo) for todo in done])

        # Update panel titles and subtitles
        self.k_todos.border_title = "Todos"
        self.k_todos.border_subtitle = f"{len(todos)} Todo"
        self.k_doing.border_title = "Doing"
        self.k_doing.border_subtitle = f"{len(doing)} In Progress"
        self.k_done.border_title = "Done"
        self.k_done.border_subtitle = f"{len(done)} Completed"

    def update_todos(self, todos):
        self.todos = todos
        self.render_kanban()

    def on_mount(self):
        self.render_kanban()
