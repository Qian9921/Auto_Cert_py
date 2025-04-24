import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from certificate.models import CertificateRequest
from certificate.generator import generate_certificate

app = FastAPI(
    title="证书生成服务",
    description="生成自定义证书的API服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "证书生成服务已启动"}

@app.post("/generate-certificate")
async def create_certificate(request: CertificateRequest):
    try:
        # 生成证书并获取文件路径
        certificate_path = generate_certificate(
            student_name=request.studentName,
            ngo_signature=request.ngoSignature,
            ngo_name=request.ngoName,
            contents=request.contents,
            date=request.date
        )
        
        # 返回生成的证书文件
        return FileResponse(
            path=certificate_path,
            filename="certificate.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 获取PORT环境变量，用于Cloud Run部署
    port = int(os.environ.get("PORT", 8080))
    
    # 启动服务器
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False) 