from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

#book model
class Book(BaseModel):
    id: int
    book_name: str
    author: str
    publisher: str

#database
books: List[Book] = []

#create book
@app.post("/books", response_model=Book)
def create_book(book: Book):
    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books.append(book)
    return book

#read all books
@app.get("/books", response_model=List[Book])
def get_books():
    return books


#read a single book by id
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for b in books:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


#update book by id
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, b in enumerate(books):
        if b.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


#delete book by id
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b.id == book_id:
            del books[i]
            return {"detail": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

