# Web_Library

## Usage:

To launch:

```git clone --recurse https://github.com/melitajak/library2.git```

```cd library2```

```docker-compose up```

Postman to test HTTP methods:

```https://www.postman.com/```

Program runs on port 80:

```localhost:80```

### GET:
get book

```curl http://localhost:80/books```


### POST:
Create book: 

```curl -X POST -H "Content-Type: application/json" -d '{"title": "New Book Title", "author": "New Book Author"}' http://localhost:80/books```

Create reader:

```curl -X POST -H "Content-Type: application/json" -d '{"name": "New Name"}' http://localhost:80/readers```

Assigns a reader to a specific book:

```curl -X PUT -H "Content-Type: application/json" -d '{"reader_id": "1"}' http://localhost:80/books/1/reader```

Assigns a library to a specific book:

```curl -X PUT -H "Content-Type: application/json" -d '{"library_id": "1"}' http://localhost:80/books/1/library```

### PUT:
Update book:

```curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Book Title", "author": "Updated Book Author"}' http://localhost:80/books/1```


### DELETE:
Unassing reader:

```curl -X DELETE http://localhost:80/books/1/reader```


















