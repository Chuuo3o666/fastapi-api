from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://usuarios_db_9x33_user:pajNkphKikCMzRsu7A3Md1rn9UUASFPM@dpg-d82puc4vikkc73ahvrcg-a/usuarios_db_9x33"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

app = FastAPI()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)


Base.metadata.create_all(bind=engine)


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando con PostgreSQL"
    }


@app.post("/usuarios")
def crear_usuario(usuario: dict):

    db = SessionLocal()

    nuevo_usuario = Usuario(
        nombre=usuario["nombre"],
        edad=usuario["edad"]
    )

    db.add(nuevo_usuario)
    db.commit()

    return {
        "mensaje": "Usuario agregado"
    }


@app.get("/usuarios")
def obtener_usuarios():

    db = SessionLocal()

    usuarios = db.query(Usuario).all()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        })

    return resultado

@app.delete("/usuarios")
def eliminar_usuarios():

    db = SessionLocal()

    db.query(Usuario).delete()
    db.commit()

    return {
        "mensaje": "Todos los usuarios eliminados"
    }