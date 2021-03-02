from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import uvicorn
import pymysql
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')

app = FastAPI()

# CORSを回避
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'memo_user'
                ,"passwd": 'memo_pass_db'
                ,"db": 'memo_db'
                ,"charset": 'utf8'
                }

# リクエストbodyを定義(初期値を設定しないと必須項目になってしまうため注意)
class Memo(BaseModel):
    id: int = 0
    title: str = ''
    content: str = ''
    create_day: int = 0
    create_time: int = 0


@app.get("/api/v1/users")
def api_users():
    users = [
        {"id": 1, "name": "1111111"},
        {"id": 2, "name": "sfafasf"},
        {"id": 3, "name": "aaaa"},
        {"id": 4, "name": "fsgdgdffdfdaf"},
        {"id": 5, "name": "c"},
        {"id": 6, "name": "aaaa"}
    ]
    return users

@app.get("/api/v1/memo")
def api_memo():
    return get_memo_data()

@app.post("/api/v1/memo/insert")
def api_insert_memo(memo: Memo):
    now = datetime.now(JST)
    memo.create_day = now.year * 10000 + now.month * 100 + now.day
    memo.create_time = now.hour * 10000 + now.minute * 100 + now.second
    try:
        insert_memo(memo)
    except:
        return {"res": "ng"}
    return {"res": "ok"}

@app.post("/api/v1/memo/modify")
def api_modify_memo(memo: Memo):
    try:
        modify_memo(memo)
    except:
        return {"res": "ng"}
    return {"res": "ok"}

@app.post("/api/v1/memo/delete")
def api_delete_memo(memo: Memo):
    try:
        delete_memo(memo)
    except:
        return {"res": "ng"}
    return {"res": "ok"}

# メモ情報取得
def get_memo_data():
    conn = getConnection()
    datas = None
    results = list()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT *
                    FROM TBL_MEMO
                  ;
                  """
            cursor.execute(sql)
            datas = cursor.fetchall()
    finally:
        conn.close()
    for data in datas:
        results.append({"id":data["ID"],
                        "title":data["TITLE"],
                        "content":data["CONTENT"],
                        "create_day":data["CREATE_DAY"],
                        "create_time":data["CREATE_TIME"],
                       })
    return results

# メモ追加
def insert_memo(memo: Memo):
    conn = getConnection()
    # Insert処理
    with conn.cursor() as cursor:
        # idはAUTO_INCREMENTのため、指定しない
        sql = """
              INSERT INTO TBL_MEMO (ID, TITLE, CONTENT, CREATE_DAY, CREATE_TIME) 
              VALUES (null, %s, %s, %s, %s)
              """
        r = cursor.execute(sql, (memo.title, memo.content, memo.create_day, memo.create_time))
        print(r) # -> 1
        # autocommitではないので、明示的にコミットする
        conn.commit()

# メモ修正
def modify_memo(memo: Memo):
    conn = getConnection()
    # Update処理
    with conn.cursor() as cursor:
        sql = """
              UPDATE TBL_MEMO 
                 SET TITLE = %s,
                     CONTENT = %s
               WHERE ID = %s 
              """
        r = cursor.execute(sql, (memo.title, memo.content, memo.id))
        print(r) # -> 1
        # autocommitではないので、明示的にコミットする
        conn.commit()

# メモ削除
def delete_memo(memo: Memo):
    conn = getConnection()
    # Delete処理
    with conn.cursor() as cursor:
        sql = """
              DELETE FROM TBL_MEMO 
               WHERE ID = %s 
              """
        r = cursor.execute(sql, (memo.id))
        print(r) # -> 1
        # autocommitではないので、明示的にコミットする
        conn.commit()


# データベースコネクション生成
def getConnection():
    conn = pymysql.connect(host=MYSQL_OPTIONS['host']
                          ,port=MYSQL_OPTIONS['port']
                          ,user=MYSQL_OPTIONS['user']
                          ,passwd=MYSQL_OPTIONS['passwd']
                          ,db=MYSQL_OPTIONS['db']
                          ,charset=MYSQL_OPTIONS['charset']
                          ,cursorclass=pymysql.cursors.DictCursor
                          )
    return conn