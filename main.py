from fastapi import FastAPI

app = FastAPI()

usuarios = []

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }

@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

@app.post("/usuarios")
def crear_usuario(usuario: dict):

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }