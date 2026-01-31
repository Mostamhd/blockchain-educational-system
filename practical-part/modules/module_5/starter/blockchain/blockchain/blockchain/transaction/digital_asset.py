import json

class Book:
    def __init__(self, isbn, title, author, owner_public_key):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.owner_public_key = owner_public_key

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return Book(data['isbn'], data['title'], data['author'], data['owner_public_key'])
