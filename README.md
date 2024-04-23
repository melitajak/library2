# Web_Library

## Usage:

To launch:

```git clone --recurse https://github.com/melitajak/library2.git```

```cd library2```

```docker-compose up```

Postman to test HTTP methods:
```https://www.postman.com/```

Program runs on port 5000:
```localhost:5000```

### GET:

Read books:

```curl http://localhost:5000/books```

Read readers:

```curl http://localhost:5000/readers```

Read libraries:

```curl http://localhost:5000/libraries```

Read book by id:

```curl http://localhost:5000/books/1```


### POST:

Create book: 

```curl -X POST -H "Content-Type: application/json" -d '{"title": "New Book Title", "author": "New Book Author"}' http://localhost:5000/books```

Create reader:

```curl -X POST -H "Content-Type: application/json" -d '{"name": "New Name"}' http://localhost:5000/readers```

Create library:

```curl -X POST -H "Content-Type: application/json" -d '{"name": "New Library"}' http://localhost:5000/libraries```

Assigns a reader to a specific book:

```curl -X PUT -H "Content-Type: application/json" -d '{"reader_id": "1"}' http://localhost:5000/books/1/reader```

Assigns a library to a specific book:

```curl -X PUT -H "Content-Type: application/json" -d '{"library_id": "1"}' http://localhost:5000/books/1/library```

### PUT:

Update book:

```curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Book Title", "author": "Updated Book Author"}' http://localhost:5000/books/1```

Update reader:

```curl -X PUT -H "Content-Type: application/json" -d '{"name": "new name"}' http://localhost:5000/readers/1```

Update library:

```curl -X PUT -H "Content-Type: application/json" -d '{"name": "new name library"}' http://localhost:5000/libraries/1```

### DELETE:

Delete book:

```curl -X DELETE http://localhost:5000/books/1```

Unassing reader:

```curl -X DELETE http://localhost:5000/books/1/reader```


















