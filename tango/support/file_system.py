import os
from abc import ABCMeta, abstractmethod


class ContentsInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, source): pass

    @abstractmethod
    def get_contents(self): pass


class FileContents(ContentsInterface):
    def __init__(self, source):
        super().__init__(source)
        self.source = source

    def get_contents(self):
        with open(self.source, 'r') as fp:
            contents = fp.read()
        fp.close()
        return contents


class StringContents(ContentsInterface):
    def __init__(self, source):
        super().__init__(source)
        self.source = source

    def get_contents(self):
        return self.source


class FileSystem:
    def create_from_stub(self, source: ContentsInterface, destination=None, replace=None):
        if destination:
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            with open(destination, 'w') as fp_destination:
                contents = source.get_contents()
                contents = self.replace_placeholders(contents, replace) if isinstance(replace, dict) else contents
                fp_destination.write(contents)
            fp_destination.close()
        else:
            raise ValueError('File destination can not be None.')

    def replace_placeholders(self, contents, replace):
        contents_updated = contents
        for key, value in replace.items():
            contents_updated = contents_updated.replace(key, value)
        return contents_updated
