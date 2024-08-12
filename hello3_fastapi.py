from fastapi import FastAPI

# fastapi 앱 실행 방법
# python -m uvicorn 파일명:app --reload
# python -m uvicorn hello2_fastapi:app --reload
app = FastAPI()

@app.get('/')
def sayhello():
    return 'Hello, World!!'
@app.get('/sayHello')
def sayhello(msg: str):
    return f'Hello, {msg}!!'

@app.get('/sayAgain/{msg}')
def sayagain(msg: str):
    return f'Hello, {msg}!!'

# __name__: 실행중인 모듈 이름을 의미하는 매직키워드
# 만일, 파일을 직접 실행하면 __name__의 이름은 __main__으로 자동지정
if __name__ == "__main__":   # 파일을 직접 실행하면 아래 코드를 불러와라
    import uvicorn
    uvicorn.run('hello3_fastapi:app', reload=True)