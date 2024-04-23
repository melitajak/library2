from flask import Flask, request, jsonify
from books import Book, books
from readers import Reader, readers
from libraries import Library, libraries
from contacts import get_contacts, create_contact

app = Flask(__name__)

#get contacts from the second service
@app.get('/contacts/<int:cont_id>')
def get_contact_route(cont_id):
    contact = get_contacts(cont_id)
    if 'error' in contact:
        return jsonify({'error': contact['error']}), 500
    return jsonify(contact)
    
@app.post('/contacts')
def create_contact_route():
    data = request.json
    # Ensure required fields are present in the request data
    required_fields = ['id', 'surname', 'name', 'number', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Forward the request to the Java service
    response = create_contact(data)
    if 'error' in response:
        return jsonify({'error': response['error']}), 500
    
    return jsonify(response), 201

@app.get('/')
def index():
    return jsonify({
        'books': [book.__dict__ for book in books],
        'readers': [reader.__dict__ for reader in readers],
        'libraries': [library.__dict__ for library in libraries]
    })
    

#GET requests
@app.get('/books')
def get_all_books():
    return jsonify([book.__dict__ for book in books])

@app.get('/readers')
def get_all_readers():
    return jsonify([reader.__dict__ for reader in readers])

@app.get('/libraries')
def get_all_libraries():
    return jsonify([library.__dict__ for library in libraries])

# Get a specific book by ID
@app.get('/books/<int:book_id>')
def get_book_by_id(book_id):
    for book in books:
        if book.id == book_id:
            return jsonify(book.__dict__)
    return jsonify({'error': 'Book not found'}), 404
   

# Get a specific reader by ID, additional info from contacts
@app.get('/contacts/readers/<int:reader_id>')
def get_reader_contacts(reader_id):
    reader = next((reader for reader in readers if reader.id == reader_id), None)
    if reader:
        reader_info = get_contacts(reader_id)
        if 'error' in reader_info:
            return jsonify({'error': reader_info['error']}), 500
        return jsonify({'id': reader_id, 'contacts': reader_info})
    return jsonify({'error: No contacts found for reader ID {reader_id}'}), 404
   

# Get a specific library by ID
@app.get('/libraries/<int:library_id>')
def get_library_by_id(library_id):
    for library in libraries:
        if library.id == library_id:
            return jsonify(library.__dict__)
    return jsonify({'error': 'Library not found'}), 404

#create book
@app.post('/books')
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    if title and author:
        new_book = Book(len(books) + 1, title, author)
        books.append(new_book)
        return jsonify(new_book.__dict__), 201, {"location": f"/books/{new_book.id}"}
    return jsonify({'error': 'Invalid data supplied'}), 400

#delete book
@app.delete('/books/<int:book_id>')
def delete_book(book_id):
    global books
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return jsonify([book.__dict__ for book in books]), 204
    return jsonify({'error': 'Book not found'}), 404

#update book
@app.put('/books/<int:book_id>')
def update_book(book_id):
    data = request.json
    title = data.get('title')
    author = data.get('author')
    reader_id = data.get('reader_id')
    library_id = data.get('library_id')
    
    for book in books:
        if book.id == book_id:
            book.title = title 
            book.author = author
            if reader_id:
                for reader in readers:
                    if reader.id == reader_id:
                        book.reader_id = reader_id
                        book.reader_name = reader.name
                        break
            if library_id:
                for library in libraries:
                    if library.id == library_id:
                        book.library_id = library_id
                        book.library_name = library.name
                        break
            return jsonify(book.__dict__)
    
    return jsonify({'error': 'Book not found'}), 404


#create reader
@app.post('/readers')
def add_reader():
    data = request.json
    reader_id = data.get('id')
    if reader_id:
        new_reader = Reader(reader_id) 
        readers.append(new_reader)
        return jsonify(new_reader.__dict__), 201, {"location": f"/readers/{new_reader.id}"}
    return jsonify({'error': 'Invalid data supplied'}), 400

#delete reader
@app.delete('/readers/<int:reader_id>')
def delete_reader(reader_id):
    global readers
    for reader in readers:
        if reader.id == reader_id:
            readers.remove(reader)
            return jsonify([reader.__dict__ for reader in readers]), 204
    return jsonify({'error': 'Reader not found'}), 404

#update reader
@app.put('/readers/<int:reader_id>')
def update_reader(reader_id):
    data = request.json
    new_reader_id = data.get('id')
    if new_reader_id:
        for reader in readers:
            if reader.id == reader_id:
                reader.id = new_reader_id
                return jsonify(reader.__dict__)
        return jsonify({'error': 'Reader not found'}), 404
    return jsonify({'error': 'Invalid data supplied'}), 400

#create library
@app.post('/libraries')
def add_library():
    data = request.json
    name = data.get('name')
    if name:
        new_library = Library(len(libraries) + 1, name)
        libraries.append(new_library)
        return jsonify(new_library.__dict__), 201, {"location": f"/libraries/{new_library.id}"}
    return jsonify({'error': 'Invalid data supplied'}), 400

#delete library
@app.delete('/libraries/<int:library_id>')
def delete_library(library_id):
    global libraries
    for library in libraries:
        if library.id == library_id:
            libraries.remove(library)
            return jsonify([library.__dict__ for library in libraries]), 204
    return jsonify({'error': 'Library not found'}), 404

#update library
@app.put('/libraries/<int:library_id>')
def update_library(library_id):
    data = request.json
    name = data.get('name')
    for library in libraries:
        if library.id == library_id:
            library.name = name
            return jsonify(library.__dict__)
    return jsonify({'error': 'Library not found'}), 404

# Update book with reader
@app.put('/books/<int:book_id>/reader')
def update_book_reader(book_id):
    data = request.json
    reader_id = data.get('reader_id')
    if reader_id:
        reader_id = int(reader_id)
        for book in books:
            if book.id == book_id:
                for reader in readers:
                    if reader.id == reader_id:
                        book.reader_id = reader_id
                        return jsonify(book.__dict__)
                return jsonify({'error': 'Reader not found'}), 404
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'error': 'Invalid data supplied'}), 400 

# Update book with library
@app.put('/books/<int:book_id>/library')
def update_book_library(book_id):
    data = request.json
    library_id = data.get('library_id')
    if library_id:
        library_id = int(library_id)
        for book in books:
            if book.id == book_id:
                for library in libraries:
                    if library.id == library_id:
                        book.library_id = library_id
                        book.library_name = library.name
                        return jsonify(book.__dict__)
                return jsonify({'error': 'Library not found'}), 404 
        return jsonify({'error': 'Book not found'}), 404 
    return jsonify({'error': 'Invalid data supplied'}), 400


# Unassign the reader from the book
@app.delete('/books/<int:book_id>/reader')
def unassign_reader(book_id):
    for book in books:
        if book.id == book_id:
            if hasattr(book, 'reader_id'):
                del book.reader_id
                return jsonify(book.__dict__), 204
            return jsonify({'error': 'Reader is not assigned to this book'}), 400
    return jsonify({'error': 'Book not found'}), 404


# Unassign the library from the book
@app.delete('/books/<int:book_id>/library')
def unassign_library(book_id):
    for book in books:
        if book.id == book_id:
            if hasattr(book, 'library_id'): 
                del book.library_id
                del book.library_name
                return jsonify(book.__dict__), 204
            return jsonify({'error': 'Library is not assigned to this book'}), 400
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
