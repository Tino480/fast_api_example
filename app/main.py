from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, likes
from starlette.responses import RedirectResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
