from sqlalchemy import Column, Enum, ForeignKey, Integer, Date, Numeric, String
from sqlalchemy.orm import declared_attr, relationship
from src.database import Base
from src.enums import TransactionStatus

class HasPetId:
    @declared_attr
    def petId(cls):
        return cls.__table__.c.get('petId', Column(Integer))

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column("id", Integer, primary_key = True, index = True)
    type = Column(String(50))
    userId = Column(String(50))
    createdAt = Column(Date)
    price = Column(Numeric)
    status = Column(Enum(TransactionStatus))

    __mapper_args__ = {
        'polymorphic_identity': 'base',
        'polymorphic_on': type
    }

class MarketTransaction(Transaction):
    __tablename__ = "market_transactions"
    
    transaction_market_id = Column("id", Integer, ForeignKey("transactions.id"), primary_key = True)
    shoppingCartId = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'market'
    }

class ServiceTransaction(HasPetId, Transaction):
    __tablename__ = "service_transactions"

    transaction_service_id = Column("id", Integer, ForeignKey("transactions.id"), primary_key = True)
    serviceIds = relationship("Transactions_Resources_Services", back_populates = "services")

    __mapper_args__ = {
        'polymorphic_identity': 'service'
    }

class ResourceTransaction(HasPetId, Transaction):
    __tablename__ = "resource_transactions"

    transaction_resource_id = Column("id", Integer, ForeignKey("transactions.id"), primary_key = True)
    resourceIds = relationship("Transactions_Resources_Services", back_populates = "resources")

    __mapper_args__ = {
        'polymorphic_identity': 'resource'
    }

class Transactions_Resources_Services(Base):
    __tablename__ = "transactions_services_resources"
    
    id = Column("id", Integer, ForeignKey("transactions.id"), primary_key = True)
    data_id = Column(Integer, primary_key = True)
    services = relationship("ServiceTransaction", back_populates = "serviceIds")
    resources = relationship("ResourceTransaction", back_populates = "resourceIds")
