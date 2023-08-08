from sqlalchemy.orm import declarative_base
from sqlalchemy import UUID, Column, String, Boolean, Enum, ForeignKey
from uuid import uuid4
from sqlalchemy_utils import ChoiceType

Base = declarative_base()

class UserDetails(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable= False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    

class OrderDetails(Base):
    __tablename__ = "order"

    PizzaSizes= (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large")
    )
    PizzaStatus= (
        ("PENDING", "pending"),
        ("IN_TRANSIT", "in_transit"),
        ("DELIVERED", "delivered")
    )    
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    size = Column(ChoiceType(choices=PizzaSizes),default="SMALL")
    status = Column(ChoiceType(choices=PizzaStatus),default="PENDING")

    user_id = Column(UUID(as_uuid=True), ForeignKey(UserDetails.id, ondelete="CASCADE", onupdate="CASCADE"))



