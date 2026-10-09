# Café API classroom demo

## Run in VS Code

1. Open this folder in VS Code.
2. Open the integrated terminal.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Start the server: `python -m uvicorn main:app --reload`
7. Open **http://127.0.0.1:8000/docs** in a browser.

The SQLite file `cafe.db` is created automatically on first run, with three example products. It stays on your computer after the server stops. To reset the demo, stop the server, delete `cafe.db` and restart.

## Suggested classroom sequence

1. GET `/products` — see all products and the JSON response.
2. GET `/products/2` — retrieve a specific product.
3. GET `/products/999` — show a 404 error.
4. POST `/products` — add `{"name":"Espresso","category":"Coffee","price":2.75}`.
5. GET `/products` again — see the new product.
6. PUT `/products/{product_id}` — change the price of the newly created product.
7. DELETE `/products/{product_id}` — remove it.
8. GET `/products` again — confirm the deletion.

Open `cafe.db` in a VS Code SQLite viewer extension to show the underlying table. Alternatively use Python's sqlite3 module. This is a local teaching demo, not a production API; it has no authentication and should not be exposed to the public internet.
