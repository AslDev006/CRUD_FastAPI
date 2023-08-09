from fastapi import FastAPI, Body, Depends, HTTPException, status
import schemes
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
Base.metadata.create_all(engine)
import uvicorn
from hash import hash_password, verify_password
from user_token import create_access_token

def get_session():
    session = SessionLocal()
    try:
        yield session

    finally:
        session.close()



app = FastAPI()

fakeDataBase = {
    1: {'task': 'Clean Car'},
    2: {'task': 'Clean Car'},
    3: {'task': 'Clean Car'},
}

@app.get('/')
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

#create #1
# @app.post('/')
# def addItem(task: str):
#     newID = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newID] = {'task': task}
#     return fakeDataBase



#create #2
@app.post("/")
def addItem(item: schemes.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item





#create #3
# @app.post('/')
# def addItem(body=Body()):
#     newID = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newID] = {'task': body['task']}
#     return fakeDataBase

#update  #1
# @app.put('/{id}')


@app.put("/{id}")
def updateItem(id: int, item: schemes.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted...'
