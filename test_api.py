"""
API测试脚本
用于测试证书生成服务的API
"""
import requests
import json
import os
import time
import webbrowser
from datetime import datetime

# API地址
API_URL = "http://localhost:8000"  # 本地测试地址

def test_api():
    """测试证书生成API"""
    print("=== 开始测试证书生成API ===")
    
    # 构建请求数据
    data = {
        "studentName": "张三",
        "ngoSignature": "OpenLab创新实验室",  # 这里使用文本作为签名，也可以使用图片URL
        "ngoName": "OpenLab创新实验室",
        "contents": "兹证明该学生在我们组织完成了Python高级编程课程的学习，表现优异。",
        "date": datetime.now().strftime("%Y年%m月%d日")
    }
    
    print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送POST请求
        response = requests.post(
            f"{API_URL}/generate-certificate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        # 检查响应状态
        if response.status_code == 200:
            # 保存返回的PDF文件
            filename = f"test_certificate_{int(time.time())}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"证书生成成功，保存为: {filename}")
            
            # 尝试打开文件
            try:
                webbrowser.open(f"file://{os.path.abspath(filename)}")
                print("已尝试打开生成的证书文件")
            except Exception as e:
                print(f"无法自动打开文件: {e}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
    
    except Exception as e:
        print(f"测试过程中出错: {e}")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_api() 