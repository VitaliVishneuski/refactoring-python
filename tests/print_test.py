import unittest

import mockito
import pytest

from task.print import Print
from task.thirdparty.dataset_impl import DataSetImpl
from task.thirdparty.database_manager import DatabaseManager
from task.thirdparty.illegal_argument_exception import IllegalArgumentException
from tests.view_stub import ViewStub


class PrintTest(unittest.TestCase):

    view = ViewStub()
    manager = mockito.mock(DatabaseManager())
    command = Print(view, manager)

    def test_should_trow_exception_when_command_is_wrong(self):
        with pytest.raises(IllegalArgumentException):
            self.command.process("print")

    def test_shouldProcessValidCommand(self):
        assert self.command.can_process("print test")

    def test_should_not_process_invalid_command(self):
        assert not self.command.can_process("qwe")

    def test_should_print_table_with_multi_data_sets(self):
        # given
        self.create_user_datasets()
        # when
        self.command.process("print users")
        # then
        self.assert_printed(
            "╔════════════════╦════════════════╦════════════════╗\n"
            "║       id       ║      name      ║    password    ║\n"
            "╠════════════════╬════════════════╬════════════════╣\n"
            "║       1        ║ Steven Seagal  ║     123456     ║\n"
            "╠════════════════╬════════════════╬════════════════╣\n"
            "║       2        ║    Eva Song    ║     789456     ║\n"
            "╚════════════════╩════════════════╩════════════════╝\n"
        )

    def create_user_datasets(self):
        user1 = self.create_user(1, "Steven Seagal", "123456")
        user2 = self.create_user(2, "Eva Song", "789456")
        data_sets = [user1, user2]
        mockito.when(self.manager).get_table_data("users").thenReturn(data_sets)

    def create_user(self, id, name, password):
        user = DataSetImpl()
        user.put("id", id)
        user.put("name", name)
        user.put("password", password)
        return user

    def prepare_single_result(self):
        mockito.when(self.manager).get_table_data("test").thenReturn([self.dataSet])

    def assert_printed(self, expected):
        assert expected == self.view.read(), print(self.view.read())


if __name__ == "__main__":
    unittest.main()
