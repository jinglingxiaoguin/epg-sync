#!/usr/bin/env python3
import requests
import os
import hashlib
from datetime import datetime

def sync_epg_file():
    url = "https://epgcloud.swh123.top/epg.php?ch=xml&v=e2all&gz=1"
    
    try:
        print("🚀 开始同步EPG数据...")
        
        # 下载文件
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 使用固定文件名
        filename = "swh123_epg.xml.gz"
        
        # 检查文件是否发生变化
        file_changed = True
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                existing_content = f.read()
                existing_hash = hashlib.md5(existing_content).hexdigest()
            
            new_hash = hashlib.md5(response.content).hexdigest()
            
            if existing_hash == new_hash:
                print("🔄 文件内容未变化，跳过更新")
                file_changed = False
            else:
                print("🔄 文件内容已变化，准备更新")
        
        # 如果文件有变化，保存文件
        if file_changed:
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 文件已更新: {filename}")
            print(f"📦 文件大小: {len(response.content)} 字节")
            print(f"🕒 同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("ℹ️ 文件内容相同，无需更新")
        
        return file_changed
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

if __name__ == "__main__":
    result = sync_epg_file()
    if result:
        print(f"🎉 同步完成，文件已保存为: swh123_epg.gz")
    else:
        print("ℹ️ 无需更新")

