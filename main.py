from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import re
import requests
from bs4 import BeautifulSoup

# 创建一个FastAPI应用实例
app = FastAPI()


class WebhookData(BaseModel):
    url: str
    activityType: str
    creatorId: int
    createdTs: int
    memo: dict

class Memo(BaseModel):
    id: int
    creatorId: int
    createdTs: int
    updatedTs: int
    content: str
    visibility: str
    pinned: bool
    resourceList: list
    relationList: list

class WebhookPayload(BaseModel):
    url: str
    activityType: str
    creatorId: int
    createdTs: int
    memo: Memo


def update_memo(id, content):
    conn = sqlite3.connect('/root/data/docker_data/memos/.memos/memos_prod.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行UPDATE SQL语句
    update_sql = f"UPDATE memo SET content = ? WHERE id = ?"
    cursor.execute(update_sql, (content, id))
    conn.commit()
    conn.close()


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        encoding = response.apparent_encoding
        response.encoding = encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else None
        # 可以在这里添加其他需要的信息的提取逻辑

        return {'title': title}
    except Exception as e:
        print(f"Failed to retrieve text from URL: {url}. Error: {str(e)}")
        return {'title': None}

# 定义一个路由，使用GET请求处理根路径
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/webhook")
async def webhook_handler(payload: WebhookPayload):
    # print(payload)
    memo_id = payload.memo.id
    content = payload.memo.content
    regexp = r"\[.*?\]\(.*?\)"
    content_clean = re.sub(regexp,"", content)
    print(content_clean)
    url_regexp = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    urls = re.findall(url_regexp, content_clean)
    content_new = content
    for url in urls:
        print(url)
        text = get_text(url)
        if text['title']:
            content_new = content_new.replace(url, f'[{text["title"]}]({url})')
    if content_new != content:
        print(memo_id, content_new)
        print(type(memo_id), type(content_new))

        update_memo(memo_id, content_new)
    update_memo(id, content)


# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
