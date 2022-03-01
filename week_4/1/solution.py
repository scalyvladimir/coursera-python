from os.path import isfile, join
from tempfile import gettempdir


class File:
    def __init__(self, path):
        self.path = path
        self.file_tail = 0

        if not isfile(self.path):
            open(self.path, 'w').close()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, content):
        with open(self.path, 'w') as f:
            return f.write(content)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.file_tail)

            line = f.readline()
            if not line:
                self.file_tail = 0
                raise StopIteration

            self.file_tail = f.tell()
            return line

    def __add__(self, other):
        new_path = join(
            gettempdir(),
            hash(self.path).__str__()
        )

        file_obj = File(new_path)
        file_obj.write(self.read() + other.read())

        return file_obj

    def __str__(self):
        return self.path
