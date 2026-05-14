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
def crear_usuarios(lista_usuarios: list):

    usuarios.extend(lista_usuarios)

    return {
        "mensaje": "Usuarios agregados",
        "usuarios": lista_usuarios
    }