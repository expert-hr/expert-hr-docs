import click
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from libs.hr_comparator.app.routes.comparator import router as compare_router


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

compare_router_prefix = "/compare"
app.include_router(compare_router, prefix=compare_router_prefix)


@click.command()
@click.option("-h", "--host", default="0.0.0.0", type=str)
@click.option("-p", "--port", default=80, type=int)
def run(host: str, port: int) -> None:
    uvicorn.run(app, host=host)


handler = Mangum(app)

if __name__ == "__main__":
    run()
