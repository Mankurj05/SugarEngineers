from demo_app.models.domain import app

__all__ = ['app']

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('demo_app.main:app', host='127.0.0.1', port=8000, reload=False)
