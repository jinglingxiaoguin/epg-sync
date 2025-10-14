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
        
        # 计算文件hash用于去重
        file_hash = hashlib.md5(response.content).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"epg_{timestamp}_{file_hash}.xml.gz"
        
        # 保存文件
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ 文件下载成功: {filename}")
        print(f"📦 文件大小: {len(response.content)} 字节")
        
        # 检查是否与最近文件内容相同（去重）
        existing_files = [f for f in os.listdir('.') if f.startswith('epg_') and f.endswith('.xml.gz')]
        if existing_files:
            existing_files.sort(reverse=True)
            with open(existing_files[0], 'rb') as f:
                existing_hash = hashlib.md5(f.read()).hexdigest()[:8]
            
            if existing_hash == file_hash:
                print("🔄 文件内容未变化，删除重复文件")
                os.remove(filename)
                return None
        
        return filename
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return None

if __name__ == "__main__":
    result = sync_epg_file()
    if result:
        print(f"🎉 同步完成，新文件: {result}")
    else:
        print("ℹ️  无需更新")