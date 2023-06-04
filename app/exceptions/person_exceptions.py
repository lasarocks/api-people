

class PersonNotFound(Exception):
    def __init__(self, name: str = 'PersonNotFound', message: str = ''):
        self.name = name
        self.message = message
        self.status_code = 404