from fastapi import FastAPI
from app.routes.amazon_routes import router as amazon_routes
from app.routes.hello_routes import router as hello_routes

app = FastAPI(
    title="Javi app",
    version="1.0.0",
    description=""
)

app.include_router(hello_routes)
app.include_router(amazon_routes)

@app.get("/", tags=["Root"])
def root():
    return {"message": "api works! :)"}
