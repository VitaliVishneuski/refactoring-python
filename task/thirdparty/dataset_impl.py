from task.thirdparty.dataset import DataSet


class Data:

    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value

    def get_column_name(self):
        return self.column_name

    def get_value(self):
        return self.value


class DataSetImpl(DataSet):

    def __init__(self):
        self.data = []

    def put(self, column_name, value):
        self.data.append(Data(column_name, value))

    def get_column_names(self) -> list:
        result = []
        for d in self.data:
            result.append(d.get_column_name())
        return result

    def get_values(self) -> list:
        result = []
        for d in self.data:
            result.append(d.get_value())
        return result
