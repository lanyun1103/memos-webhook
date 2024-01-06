from fastapi import FastAPI
from pydantic import BaseModel

# 创建一个FastAPI应用实例
app = FastAPI()


class WebhookPayload(BaseModel):
    event: str
    data: dict


# 定义一个路由，使用GET请求处理根路径
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/webhook")
async def webhook_handler(payload: WebhookPayload):
    event = payload.event
    data = payload.data

    # 在这里处理Webhook请求，根据事件类型执行相应的操作
    # 这只是一个示例，您可以根据实际需求编写处理逻辑

    return {"message": f"Received event: {event}", "data": data}


# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
