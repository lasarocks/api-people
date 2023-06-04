from fastapi import APIRouter
#from app.api.routes import route_serasa
#from app.api.routes import route_garimpo
from app.api.routes.garimpo import(
    route_source,
    route_documenttype,
    route_person,
    route_garimpa2000,
    route_address,
    route_contact,
    route_document,
    route_workhistory,
    route_financial
)


api_router = APIRouter()
#api_router.include_router(route_serasa.router, prefix="/JustBR", tags=["serasa[justBR] - Name Research"])
# api_router.include_router(route_garimpo.router, prefix="/prato-feito", tags=["PF"])
api_router.include_router(route_garimpa2000.router, prefix="/garimpo", tags=["PF", "PF - garimpo analyses"])


#PESSOA FISICA
api_router.include_router(route_source.router, prefix="/prato-feito", tags=["PF", "source"])
api_router.include_router(route_documenttype.router, prefix="/prato-feito", tags=["PF", "document-type"])
api_router.include_router(route_person.router, prefix="/prato-feito", tags=["PF", "person"])

api_router.include_router(route_address.router, prefix="/prato-feito/person", tags=["PF", "person", "address"])
api_router.include_router(route_contact.router, prefix="/prato-feito/person", tags=["PF", "person", "contact"])
api_router.include_router(route_document.router, prefix="/prato-feito/person", tags=["PF", "person", "document"])
api_router.include_router(route_workhistory.router, prefix="/prato-feito/person", tags=["PF", "person", "work-history"])
api_router.include_router(route_financial.router, prefix="/prato-feito/person", tags=["PF", "person", "financial"])
