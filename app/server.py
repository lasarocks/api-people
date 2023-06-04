from fastapi import(
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status
)
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse


from app.core.database import(
    SessionLocal,
    engine,
    Base
)

from app.exceptions.person_exceptions import(
    PersonNotFound
)


from app.exceptions.garimpa_exceptions import(
    ItemNotFound
)

from app.api.base import api_router

#Base.metadata.create_all(engine, Base.metadata.tables.values(),checkfirst=True)

Base.metadata.create_all(bind=engine, checkfirst=True)
#Base.metadata.tables['ContactTypes'].create(bind=engine, checkfirst=True, create_table=True)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)



app.include_router(api_router)


@app.exception_handler(ItemNotFound)
async def notfound_exception_handler(request, exc: ItemNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "data": None,
            "error_code": exc.name,
            "message": exc.message
        }
    )


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     print('porra')
#     return {
#         "error": True,
#         "data": None,
#         "message": exc.detail
#     }



