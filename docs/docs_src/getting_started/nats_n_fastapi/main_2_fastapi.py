from os import environ

from fastapi import FastAPI

from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.adapters.nats import NatsAdapter

nats_url = environ.get("NATS_URL", "nats://localhost:4222")
nats_user: str = "fastagency"
nats_password: str = environ.get("FASTAGENCY_NATS_PASSWORD", "fastagency_nats_password")  # type: ignore[assignment]

provider = NatsAdapter.create_provider(
    nats_url=environ.get("NATS_URL", None), user=nats_user, password=nats_password
)

adapter = FastAPIAdapter(
    provider=provider,
)

# app = FastAPI(lifespan=provider.lifespan)
app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {
        "Workflows": {name: provider.get_description(name) for name in provider.names}
    }


# start the provider with the following command
# uvicorn main_2_fastapi:app --host 0.0.0.0 --port 8008 --reload
