from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

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

class Movimiento(Base):

    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)

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


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        return {
            "mensaje": "Usuario no encontrado"
        }

    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "edad": usuario.edad
    }

@app.delete("/usuarios")
def eliminar_usuarios():

    db = SessionLocal()

    db.query(Usuario).delete()
    db.commit()

    return {
        "mensaje": "Todos los usuarios eliminados"
    }


@app.post("/importar-csv")
def importar_csv():

    db = SessionLocal()

    with open("usuarios.csv", newline="", encoding="utf-8") as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            nuevo_usuario = Usuario(
                nombre=fila["nombre"],
                edad=int(fila["edad"])
            )

            db.add(nuevo_usuario)

        db.commit()

    return {
        "mensaje": "Usuarios importados correctamente"
    }

@app.post("/importar-movimientos")
def importar_movimientos():

    db = SessionLocal()

    with open(
        "bridge_move_type_MOVES_IS_TYPE.csv",
        newline="",
        encoding="utf-8"
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            nuevo_movimiento = Movimiento(
                nombre=fila["Name"],
                tipo=fila["Type"]
            )

            db.add(nuevo_movimiento)

        db.commit()

    return {
        "mensaje": "Movimientos importados correctamente"
    }

@app.get("/movimientos")
def obtener_movimientos():

    db = SessionLocal()

    movimientos = db.query(Movimiento).all()

    resultado = []

    for movimiento in movimientos:

        resultado.append({
            "id": movimiento.id,
            "nombre": movimiento.nombre,
            "tipo": movimiento.tipo
        })

    return resultado