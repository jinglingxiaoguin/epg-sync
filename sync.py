#!/usr/bin/env python3
import requests
import os
import hashlib
from datetime import datetime

# 定义需要同步的文件列表
SYNC_FILES = [
    ("swh123_epg.xml.gz", "https://epgcloud.swh123.top/epg.php?ch=xml&v=e2all&gz=1"),
    ("tel-epg.xml", "https://epg.deny.vip/sh/tel-epg.xml"),
    ("dm2.xml.gz", "https://epg.swh123.link:4443/live.php?ch=xml&v=dm2&gz=1"),
]


def download_and_check(filename, url):
    """
    下载文件并检测是否变化，返回 (changed, message)
    """
    try:
        print(f"\n🚀 开始同步: {filename}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.content

        # 检查文件是否有变化
        file_changed = True
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                old_hash = hashlib.md5(f.read()).hexdigest()
            new_hash = hashlib.md5(content).hexdigest()
            if old_hash == new_hash:
                print("🔄 内容未变化，跳过更新")
                file_changed = False
            else:
                print("🔄 检测到更新，准备写入文件")

        if file_changed:
            with open(filename, 'wb') as f:
                f.write(content)
            print(f"✅ 已更新文件: {filename} ({len(content)} 字节)")
            print(f"🕒 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return file_changed

    except Exception as e:
        print(f"❌ {filename} 同步失败: {e}")
        return False


def main():
    any_changed = False
    for filename, url in SYNC_FILES:
        changed = download_and_check(filename, url)
        if changed:
            any_changed = True

    if any_changed:
        print("\n🎉 有文件更新，准备提交到仓库")
    else:
        print("\nℹ️ 所有文件均无变化，无需提交")

    return any_changed


if __name__ == "__main__":
    result = main()
    # 输出环境变量以供 GitHub Actions 读取
    if result:
        print("::set-output name=changed::true")
    else:
        print("::set-output name=changed::false")
