from pydantic import BaseModel, Field
from typing import Optional

class CertificateRequest(BaseModel):
    """证书生成请求的数据模型"""
    studentName: str = Field(..., description="学生姓名")
    ngoSignature: Optional[str] = Field(None, description="NGO签名图片URL或文本")
    ngoName: str = Field(..., description="NGO名称")
    contents: str = Field(..., description="证书内容")
    date: str = Field(..., description="颁发日期") 