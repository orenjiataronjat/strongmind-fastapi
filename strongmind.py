from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

from pydantic import BaseModel
from typing import Annotated
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Topping(BaseModel):
    id: int
    title: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    toppings = db.query(models.Topping).all()
    pizzas = db.query(models.Pizza).all()
    return {"toppings": toppings, "pizzas": pizzas}

@app.get("/toppings")
def getToppings(db: Session = Depends(get_db)):
    return {"toppings": db.query(models.Topping).all()}

@app.get("/pizzas")
def getToppings(db: Session = Depends(get_db)):
    return {"pizzas": db.query(models.Pizza).all()}

@app.post("/addTopping/{title}")
def addTopping( title: str, db: Session = Depends(get_db)):
    if db.query(models.Topping.title).filter_by(title=title).first() is None:
        new_topping = models.Topping(title=title)
        db.add(new_topping)
        db.commit()
        return jsonable_encoder(db.query(models.Topping).filter_by(title=title).first()) 
    else:
        return {"Topping not added."}

@app.post("/updateTopping/{id}/{title}")
def updateTopping(id: int, title: str, db: Session = Depends(get_db)):
    if db.query(models.Topping.id).filter_by(id=id).first() is None:
        return {"Topping id does not exist in database"}
    elif db.query(models.Topping.id).filter_by(title=title).first() is not None:
        return {"Topping already in database. No changes made"}
    else:
        db_topping = db.query(models.Topping).filter(models.Topping.id==id).first()
        db_topping.title = title
        db.commit()
        return jsonable_encoder(db.query(models.Topping).filter_by(title=title).first()) 
        

@app.post("/deleteTopping/{id}")
def deleteTopping(id: int, db: Session = Depends(get_db)):
    if db.query(models.Topping.id).filter_by(id=id).first() is None:
        return {"Topping id does not exist in database"}
    else:
        topping = db.query(models.Topping).filter(models.Topping.id == id).first()
        db.delete(topping)
        db.commit()
        return {"Topping deleted"}
    
@app.post("/addPizza/{title}/{toppings}")
def addPizza( title: str,toppings:  str,db: Session = Depends(get_db)):
    if db.query(models.Pizza.title).filter_by(title=title).first() is None:
        new_pizza = models.Pizza(title=title, toppings=toppings)
        db.add(new_pizza)
        db.commit()
        return jsonable_encoder(db.query(models.Pizza).filter_by(toppings=toppings).first())
    else:
        return {"Pizza not added."}

@app.post("/updatePizza/{id}/{title}")
def updatePizza(id: int, title: str, db: Session = Depends(get_db)):
    if db.query(models.Pizza.id).filter_by(id=id).first() is None:
        return {"Pizza id does not exist in database"}
    elif db.query(models.Pizza.id).filter_by(title=title).first() is not None:
        return {"Pizza already in database. No changes made"}
    else:
        db_pizza = db.query(models.Pizza).filter(models.Pizza.id == id).first()
        db_pizza.title = title
        db.commit()
        return jsonable_encoder(db.query(models.Pizza).filter_by(id=id).first())

@app.post("/updatePizzaToppings/{id}/{toppings}")
def updatePizzaToppings(id: int, toppings: str, db: Session = Depends(get_db)):
    if db.query(models.Pizza.id).filter_by(id=id).first() is None:
        return {"Pizza id does not exist in database"}
    elif db.query(models.Pizza.id).filter_by(toppings=toppings).first() is not None:
        return {"Those are already the toppings for that pizza. No changes made"}
    else:
        db_pizza_topping = db.query(models.Pizza).filter(models.Pizza.id == id).first()
        db_pizza_topping.toppings = toppings
        db.commit()
        return jsonable_encoder(db.query(models.Pizza).filter_by(id=id).first())
        
@app.post("/deletePizza/{id}")
def deletePizza( id: int, db: Session = Depends(get_db)):
    if db.query(models.Pizza.id).filter_by(id=id).first() is not None:
        pizza = db.query(models.Pizza).filter(models.Pizza.id == id).first()
        db.delete(pizza)
        db.commit()
        return {"Pizza deleted"}
    else:
        return {"Pizza id does not exist in database"}
    