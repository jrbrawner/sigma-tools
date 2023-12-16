from fastapi import FastAPI
from src.db import Base, engine
from src.arcsight_rules_xml.resources import router as rules_router
from src.publish.router import router as publish_router
from src.elastic_sigma.router import router as elastic_sigma_router


app = FastAPI()

app.include_router(rules_router)
app.include_router(elastic_sigma_router)
app.include_router(publish_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
