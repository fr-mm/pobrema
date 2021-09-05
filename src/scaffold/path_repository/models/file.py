from src.scaffold.path_repository.models import BasicPath


class File(BasicPath):
    def _create(self, content: str = None) -> None:
        if not content:
            content = ''
        with open(self.path, 'w') as file:
            file.write(content)

    @property
    def content(self) -> str:
        with open(self.path, 'r') as file:
            return file.read()