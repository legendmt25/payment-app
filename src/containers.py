from dependency_injector import containers, providers
from dotenv import load_dotenv
from src.database import Database

load_dotenv('.env.local')

class Container(containers.DeclarativeContainer): 
    config = providers.Configuration()
    config.DB_CONNECTION.from_env("DB_CONNECTION")
    config.PORT.from_env("PORT", as_=int, default=5000)
    wiring_config = containers.WiringConfiguration(modules=["src.endpoints"])    
    db = providers.Singleton(Database, config.DB_CONNECTION)