import click
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from apps.libs.questionnaire_disc.app.routes.disc import disc_router

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


generation_routes_prefix = "/disc"
app.include_router(disc_router, prefix=generation_routes_prefix)


@click.command()
@click.option("-h", "--host", default="0.0.0.0", type=str)
@click.option("-p", "--port", default=88, type=int)
def run(host: str = "0.0.0.0", port: int = 88) -> None:
    uvicorn.run(app, host=host, port=port)


handler = Mangum(app)

if __name__ == "__main__":
    run()
