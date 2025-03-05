from fastapi import FastAPI
import uvicorn
from integration.integration_endpoint import integration_app


app = FastAPI()
app.include_router(integration_app)


@app.get('/')
async def root():
    return {"message": "Welcome to Profile Search"}


@app.get('/health')
async def health_check():
    return {"status": "UP"}





if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8101)