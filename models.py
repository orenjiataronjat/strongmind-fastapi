from sqlalchemy import Boolean, Column, Integer, String, ARRAY

from database import Base


class Topping(Base):
    __tablename__ = "toppings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    toppings = Column(String)

# schemas

