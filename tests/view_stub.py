from task.thirdparty.view import View


class ViewStub(View):

    message = ""

    def write(self, message):
        self.message = message

    def read(self):
        return self.message
