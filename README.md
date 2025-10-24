
# Prueba tecnica Python Playwright



## Instrucciones de compilación

Para compilar el proyecto se recomienda el uso de un entorno virtual de Python (venv).

Comandos:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
## Peticiones al API

Petición para comprar un producto en amazon:

URL: http://127.0.0.1:8000/amazon/shopping-flow

METHOD: POST

BODY:

{

    "headless": true,
    "user_email": "user@email.com",
    "user_pwd": "123Password!"
}