import uvicorn
from src.core.settings import settings


def main():
    uvicorn.run(
        'server:app',
        reload=True,
        host=settings.host,
        port=settings.port,
    )


if __name__ == '__main__':
    main()
