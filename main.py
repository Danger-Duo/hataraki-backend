import uvicorn

# helper script for running in development mode only
if __name__ == '__main__':
    uvicorn.run('app.server:app', port=8001, reload=True)
