from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import addMemories, getMemories, updateMemory, deleteMemory, getMetadataFields
from app.memory_client import get_memory_client

# 加载 .env 文件
load_dotenv()

app = FastAPI(title="Memory Management API")

# 启动时初始化 memory 客户端
@app.on_event("startup")
async def startup_event():
    """启动时自动初始化 memory 客户端"""
    print("🚀 Initializing memory client...")
    get_memory_client()
    print("✅ Memory client initialized successfully")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(addMemories.router, prefix="/api", tags=["Memories"])
app.include_router(getMemories.router, prefix="/api", tags=["Memories"])
app.include_router(getMetadataFields.router, prefix="/api", tags=["Memories"])
app.include_router(updateMemory.router, prefix="/api", tags=["Memories"])
app.include_router(deleteMemory.router, prefix="/api", tags=["Memories"])

@app.get("/")
def root():
    return {"message": "Memory Management API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
