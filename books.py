class Book:
    def __init__(self, id, title, author, reader_id=None, library_id=None):
        self.id = id
        self.title = title
        self.author = author

books = [
    Book(1, "Animal Farm", "George Orwell"),
    Book(2, "The Hobbit", "J.R.R. Tolkien"),
    Book(3, "To Kill a Mockingbird", "Harper Lee"),
]
