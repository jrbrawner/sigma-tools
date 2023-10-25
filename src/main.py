from fastapi import FastAPI
from src.db import Base, engine
from src.sigma.router import router as sigma_router
from src.arcsight_rules_xml.router import router as rules_router
from src.arcsight_rules_json.router import router as json_rules_router


app = FastAPI()

app.include_router(sigma_router)
app.include_router(rules_router)
app.include_router(json_rules_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
