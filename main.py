from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

DATABASE_URL = "postgresql+psycopg2://usuarios_db_9x33_user:pajNkphKikCMzRsu7A3Md1rn9UUASFPM@dpg-d82puc4vikkc73ahvrcg-a/usuarios_db_9x33"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

app = FastAPI()


class Movimiento(Base):

    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)


Base.metadata.create_all(bind=engine)


@app.get("/")
def inicio():

    return {
        "mensaje": "API Pokemon funcionando"
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


@app.get("/movimientos/{movimiento_id}")
def obtener_movimiento(movimiento_id: int):

    db = SessionLocal()

    movimiento = db.query(Movimiento).filter(
        Movimiento.id == movimiento_id
    ).first()

    if movimiento is None:

        return {
            "mensaje": "Movimiento no encontrado"
        }

    return {
        "id": movimiento.id,
        "nombre": movimiento.nombre,
        "tipo": movimiento.tipo
    }