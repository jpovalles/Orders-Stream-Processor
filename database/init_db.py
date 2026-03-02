from .conn import engine
from .models import Base

Base.metadata.create_all(bind=engine)

print("---- Base de datos inicializada ----")
