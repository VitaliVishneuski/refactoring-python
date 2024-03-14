from task.thirdparty.command import Command
from task.thirdparty.database_manager import DatabaseManager
from task.thirdparty.illegal_argument_exception import IllegalArgumentException
from task.thirdparty.view import View


class Print(Command):

    view = View()
    manager = DatabaseManager()
    table_name = ""

    def __init__(self, view, manager):
        self.view = view
        self.manager = manager

    def can_process(self, command: str) -> bool:
        return command.startswith("print ")

    def process(self, input: str):
        command = input.split(" ")
        if not len(command) == 2:
            raise IllegalArgumentException(
                "incorrect number of parameters. Expected 1, but is {}".format(
                    len(command) - 1
                )
            )
        self.table_name = command[1]
        data = self.manager.get_table_data(self.table_name)
        self.view.write(self.get_table_string(data))

    def get_table_string(self, data):
        max_column_size = self.get_max_column_size(data)
        if max_column_size == 0:
            return self.get_empty_table(self.table_name)
        else:
            return self.get_header_of_the_table(data) + self.get_string_table_data(data)

    def get_empty_table(self, table_name):
        text_empty_table = "║ Table '" + table_name + "' is empty or does not exist ║"
        result = "╔"
        for _ in range(len(text_empty_table) - 2):
            result += "═"
        result += "╗\n"
        result += text_empty_table + "\n"
        result += "╚"
        for i in range(len(text_empty_table) - 2):
            result += "═"
        result += "╝\n"
        return result

    def get_max_column_size(self, datasets):
        max_length = 0
        if len(datasets) > 0:
            column_names = datasets[0].get_column_names()
            for column_name in column_names:
                if len(column_name) > max_length:
                    max_length = len(column_name)
            for dataset in datasets:
                values = dataset.get_values()
                for value in values:
                    # if value is str:
                    if len(str(value)) > max_length:
                        max_length = len(str(value))
        return max_length

    def get_string_table_data(self, datasets):
        rows_count = len(datasets)
        max_column_size = self.get_max_column_size(datasets)
        result = ""
        if max_column_size % 2 == 0:
            max_column_size += 2
        else:
            max_column_size += 3
        column_count = self.get_column_count(datasets)
        for row in range(rows_count):
            values = datasets[row].get_values()
            result += "║"
            for column in range(column_count):
                values_length = len(str(values[column]))
                if values_length % 2 == 0:
                    for _ in range((max_column_size - values_length) // 2):
                        result += " "
                    result += str(values[column])
                    for _ in range((max_column_size - values_length) // 2):
                        result += " "
                    result += "║"
                else:
                    for j in range((max_column_size - values_length) // 2):
                        result += " "
                    result += str(values[column])
                    for j in range(((max_column_size - values_length) // 2) + 1):
                        result += " "
                    result += "║"
            result += "\n"
            if row < rows_count - 1:
                result += "╠"
                for _ in range(1, column_count):
                    for _ in range(max_column_size):
                        result += "═"
                    result += "╬"
                for i in range(max_column_size):
                    result += "═"
                result += "╣\n"
        result += "╚"
        for j in range(1, column_count):
            for _ in range(max_column_size):
                result += "═"
            result += "╩"
        for _ in range(max_column_size):
            result += "═"
        result += "╝\n"
        return result

    def get_column_count(self, datasets):
        result = 0
        if len(datasets) > 0:
            return len(datasets[0].get_column_names())
        return result

    def get_header_of_the_table(self, datasets):
        max_column_size = self.get_max_column_size(datasets)
        result = ""
        column_count = self.get_column_count(datasets)
        if max_column_size % 2 == 0:
            max_column_size += 2
        else:
            max_column_size += 3
        result += "╔"
        for _ in range(1, column_count):
            for _ in range(max_column_size):
                result += "═"
            result += "╦"
        for _ in range(max_column_size):
            result += "═"
        result += "╗\n"
        column_names = datasets[0].get_column_names()
        for column in range(column_count):
            result += "║"
            column_names_length = len(column_names[column])
            if column_names_length % 2 == 0:
                for _ in range((max_column_size - column_names_length) // 2):
                    result += " "
                result += column_names[column]
                for _ in range((max_column_size - column_names_length) // 2):
                    result += " "
            else:
                for j in range((max_column_size - column_names_length) // 2):
                    result += " "
                result += column_names[column]
                for j in range(((max_column_size - column_names_length) // 2) + 1):
                    result += " "
        result += "║\n"

        # last string of the header
        if len(datasets) > 0:
            result += "╠"
            for _ in range(1, column_count):
                for i in range(max_column_size):
                    result += "═"
                result += "╬"
            for i in range(max_column_size):
                result += "═"
            result += "╣\n"
        else:
            result += "╚"
            for _ in range(1, column_count):
                for i in range(max_column_size):
                    result += "═"
            result += "╩"
            for i in range(max_column_size):
                result += "═"
            result += "╝\n"
        return result
