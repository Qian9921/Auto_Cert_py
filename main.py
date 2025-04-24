import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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

@app.post("/generate-certificate/debug")
async def create_certificate_debug(
    request: CertificateRequest, 
    enable_debug: bool = Query(True, description="启用调试模式")
):
    """调试模式生成证书，会记录详细的字体渲染信息"""
    
    # 设置环境变量启用调试模式
    if enable_debug:
        os.environ["DEBUG_FONT"] = "1"
    
    debug_info = []
    
    # 自定义处理器捕获调试信息
    class DebugInfoHandler:
        def write(self, message):
            debug_info.append(message)
        def flush(self):
            pass
    
    # 保存原始错误输出
    original_stderr = os.sys.stderr
    
    try:
        # 替换为我们的处理器来捕获调试输出
        if enable_debug:
            os.sys.stderr = DebugInfoHandler()
        
        # 生成证书并获取文件路径
        certificate_path = generate_certificate(
            student_name=request.studentName,
            ngo_signature=request.ngoSignature,
            ngo_name=request.ngoName,
            contents=request.contents,
            date=request.date
        )
        
        # 返回生成的证书文件和调试信息
        response_data = {
            "message": "证书生成成功",
            "certificate_path": certificate_path,
            "debug_info": debug_info if enable_debug else []
        }
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 恢复原始错误输出
        if enable_debug:
            os.sys.stderr = original_stderr
        
        # 重置环境变量
        if "DEBUG_FONT" in os.environ:
            del os.environ["DEBUG_FONT"]

@app.get("/font-info")
async def get_font_info():
    """返回关于可用字体的信息"""
    import config
    from certificate.generator import get_font
    
    # 测试字体大小为40
    test_size = 40
    
    # 设置调试模式
    os.environ["DEBUG_FONT"] = "1"
    
    debug_info = []
    
    # 自定义处理器捕获调试信息
    class DebugInfoHandler:
        def write(self, message):
            debug_info.append(message)
        def flush(self):
            pass
    
    # 保存原始错误输出
    original_stderr = os.sys.stderr
    
    try:
        # 替换为我们的处理器来捕获调试输出
        os.sys.stderr = DebugInfoHandler()
        
        # 获取字体
        font = get_font(config.DEFAULT_FONT, test_size)
        
        # 收集系统字体信息
        font_info = {
            "default_font": config.DEFAULT_FONT,
            "font_dir": config.FONT_DIR,
            "available_fonts": []
        }
        
        # 检查系统字体
        system_fonts = [
            "arial.ttf", "simsun.ttc", "simhei.ttf", "msyh.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
        ]
        
        for font_name in system_fonts:
            try:
                test_font = get_font(font_name, test_size)
                if test_font:
                    font_info["available_fonts"].append(font_name)
            except Exception:
                pass
        
        # 返回字体信息和调试信息
        return {
            "font_info": font_info,
            "debug_info": debug_info
        }
    
    finally:
        # 恢复原始错误输出
        os.sys.stderr = original_stderr
        
        # 重置环境变量
        if "DEBUG_FONT" in os.environ:
            del os.environ["DEBUG_FONT"]

if __name__ == "__main__":
    # 获取PORT环境变量，用于Cloud Run部署
    port = int(os.environ.get("PORT", 8080))
    
    # 启动服务器
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False) 