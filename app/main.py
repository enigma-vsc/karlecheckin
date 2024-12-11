from fastapi import FastAPI
from .routers import admin, customer
import uvicorn

app = FastAPI()

app.include_router(admin.router)
app.include_router(customer.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Hotel Management System"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
