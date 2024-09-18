import click
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from apps.libs.hr_parser.app.routes.parser import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router_prefix = "/parse"
app.include_router(router, prefix=router_prefix)


@click.command()
@click.option("-h", "--host", default="0.0.0.0", type=str)
@click.option("-p", "--port", default=80, type=int)
def run(host: str = "0.0.0.0", port: int = 80) -> None:
    uvicorn.run(app, host=host, port=port)


handler = Mangum(app)

if __name__ == "__main__":
    run()
