from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.likes.routes import router as likes_router
from app.posts.routes import router as posts_router
from app.users.routes import router as users_router
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


app.include_router(auth_router)
app.include_router(likes_router)
app.include_router(posts_router)
app.include_router(users_router)
