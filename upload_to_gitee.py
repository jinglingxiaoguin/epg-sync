#!/usr/bin/env python3
import requests
import base64
import os
from datetime import datetime

def upload_file():
    # Gitee配置
    token = os.environ.get('GITEE_TOKEN')
    owner = 'shiwenhua'
    repo = 'epg-sync'
    file_path = 'swh123_epg.gz'
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    # 获取现有文件SHA
    url = f'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{file_path}'
    params = {'access_token': token}
    
    response = requests.get(url, params=params)
    sha = None
    if response.status_code == 200:
        sha = response.json().get('sha')
        print(f"找到现有文件，SHA: {sha}")
    
    # 准备上传数据
    data = {
        'access_token': token,
        'content': content,
        'message': f'🤖 Auto sync EPG: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}',
        'branch': 'main'
    }
    
    if sha:
        data['sha'] = sha
    
    # 上传文件
    response = requests.post(url, json=data)
    
    if response.status_code in [200, 201]:
        print('✅ 文件上传成功！')
        print(f'文件URL: {response.json().get("content", {}).get("download_url")}')
    else:
        print(f'❌ 上传失败: {response.status_code}')
        print(f'错误信息: {response.text}')

if __name__ == '__main__':
    upload_file()
