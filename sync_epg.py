#!/usr/bin/env python3
import requests
import os
import hashlib
from datetime import datetime
import subprocess

def sync_epg_file():
    url = "https://epgcloud.swh123.top/epg.php?ch=xml&v=e2all&gz=1"
    
    try:
        print("🚀 开始同步EPG数据...")
        
        # 下载文件
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 使用固定文件名
        filename = "swh123_epg.gz"
        
        # 检查文件是否发生变化
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                existing_content = f.read()
                existing_hash = hashlib.md5(existing_content).hexdigest()
            
            new_hash = hashlib.md5(response.content).hexdigest()
            
            if existing_hash == new_hash:
                print("🔄 文件内容未变化，跳过更新")
                return None
        
        # 保存文件（覆盖）
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ 文件下载成功: {filename}")
        print(f"📦 文件大小: {len(response.content)} 字节")
        print(f"🕒 同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return filename
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return None

if __name__ == "__main__":
    result = sync_epg_file()
    if result:
        print(f"🎉 同步完成，文件已保存为: {result}")
    else:
        print("ℹ️  无需更新")
