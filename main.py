import uvicorn

if __name__ == '__main__':
    uvicorn.run('app:app', port=8001, reload=True)
