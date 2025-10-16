#!/usr/bin/env python3
import requests
import os
import hashlib
from datetime import datetime

# 定义需要同步的文件列表
# 格式: (本地文件名, 远程URL)
SYNC_FILES = [
    ("swh123_epg.xml.gz", "https://epgcloud.swh123.top/epg.php?ch=xml&v=e2all&gz=1"),
    ("tel-epg.xml", "https://epg.deny.vip/sh/tel-epg.xml"),
    ("dm2.xml.gz", "https://epg.swh123.link:4443/live.php?ch=xml&v=dm2&gz=1"),
]

def sync_file(filename, url):
    """同步单个文件，检查哈希后保存。"""
    
    file_changed = False
    
    try:
        print(f"--- 🚀 开始同步文件: {filename} ---")
        
        # 1. 下载文件
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        new_content = response.content
        new_hash = hashlib.md5(new_content).hexdigest()
        
        # 2. 检查文件是否发生变化
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                existing_content = f.read()
                existing_hash = hashlib.md5(existing_content).hexdigest()
            
            if existing_hash == new_hash:
                print(f"    🔄 文件内容未变化，跳过更新: {filename}")
                return False
            else:
                print(f"    🔄 文件内容已变化 (Hash: {existing_hash[:8]}->{new_hash[:8]})，准备更新")
                file_changed = True
        else:
            print(f"    ✨ 文件不存在，首次创建")
            file_changed = True
            
        # 3. 如果文件有变化，保存文件
        if file_changed:
            with open(filename, 'wb') as f:
                f.write(new_content)
            
            print(f"    ✅ 文件已更新/创建: {filename}")
            print(f"    📦 文件大小: {len(new_content)} 字节")
            print(f"    🕒 同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        return file_changed
        
    except Exception as e:
        print(f"    ❌ 同步失败: {filename} - {e}")
        return False

def run_all_syncs():
    """遍历所有文件并执行同步，同时将文件名列表写入文件。"""
    
    overall_changed = False
    
    for filename, url in SYNC_FILES:
        if sync_file(filename, url):
            overall_changed = True
            
    # 【核心逻辑】将文件名列表（用空格分隔）写入 epg_files.txt
    filename_list = [f[0] for f in SYNC_FILES]
    try:
        with open('epg_files.txt', 'w') as f:
            file_content = ' '.join(filename_list)
            f.write(file_content + '\n')
            print(f"    📄 已创建 epg_files.txt，内容: {file_content}")
    except Exception as e:
        print(f"    ❌ 写入 epg_files.txt 失败: {e}")
            
    return overall_changed

if __name__ == "__main__":
    print(f"--- 全局同步任务开始于: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    run_all_syncs() 
    print("--- 磁盘文件更新完成，准备检查Git状态。 ---")
