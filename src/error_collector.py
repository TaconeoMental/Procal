from src.token import Token


class Error:
    def __init__(self, token, descrip):
        self.error_description = descrip

        self.start = token.start
        self.end = token.end
        self.length = self.end - self.start + 1

    # TODO
    def __str__(self):
        return self.error_description


class ErrorCollector:
    def __init__(self, prop):
        self.proposition = prop

        self.errors = list()

    # TODO
    def add_error(self, err: Error):
        self.errors.append(err)

    def has_errors(self) -> bool:
        if not self.errors:
            return False
        return True

    def show_errors(self):
        for err in self.errors:
            print("Error:", err)
            print(self.proposition)
            print(' ' * err.start + '^' * err.length)
