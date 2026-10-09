from fastapi.responses import FileResponse
from pathlib import Path
from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

DB = Path(__file__).with_name('cafe.db')

class Product(BaseModel):
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)

def connect():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection

def setup():
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL CHECK(price > 0))')
        if db.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
            db.executemany('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', [('Latte', 'Coffee', 3.50), ('Chicken Sandwich', 'Food', 4.75), ('Chocolate Cake', 'Cake', 3.95)])

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup()
    yield

app = FastAPI(title='Café Products API', description='A simple REST API for a classroom demonstration', lifespan=lifespan)

@app.get('/products')
def get_products():
    with connect() as db:
        return [dict(row) for row in db.execute('SELECT * FROM products ORDER BY id')]

@app.get('/products/{product_id}')
def get_product(product_id: int):
    with connect() as db:
        row = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return dict(row)

@app.post('/products', status_code=201)
def create_product(product: Product):
    with connect() as db:
        cursor = db.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', (product.name, product.category, product.price))
        row = db.execute('SELECT * FROM products WHERE id = ?', (cursor.lastrowid,)).fetchone()
    return dict(row)

@app.put('/products/{product_id}')
def update_product(product_id: int, product: Product):
    with connect() as db:
        cursor = db.execute('UPDATE products SET name = ?, category = ?, price = ? WHERE id = ?', (product.name, product.category, product.price, product_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail='Product not found')
        row = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    return dict(row)

@app.delete('/products/{product_id}', status_code=204)
def delete_product(product_id: int):
    with connect() as db:
        cursor = db.execute('DELETE FROM products WHERE id = ?', (product_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail='Product not found')
    return Response(status_code=204)

@app.get("/", include_in_schema=False)
def homepage():
    html_file = Path(__file__).resolve().parent / "index.html"
    return FileResponse(html_file)