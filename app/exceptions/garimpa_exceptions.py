

class ItemNotFound(Exception):
    def __init__(self, name: str = 'ItemNotFound', message: str = ''):
        self.name = name
        self.message = message
        self.status_code = 404