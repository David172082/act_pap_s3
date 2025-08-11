from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ✅ Modelo base para productos
class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str  # alimento, juguetes, accesorios
    stock: int

# ✅ Modelo para actualización parcial
class ProductoParcial(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None

# ✅ Base de datos simulada
productos = [
    {"id": 1, "nombre": "Croquetas Premium", "precio": 25.0, "categoria": "alimento", "stock": 50},
    {"id": 2, "nombre": "Pelota de Goma", "precio": 5.5, "categoria": "juguetes", "stock": 100},
    {"id": 3, "nombre": "Correa para perro", "precio": 15.0, "categoria": "accesorios", "stock": 30},
    {"id": 4, "nombre": "Arena para gatos", "precio": 12.0, "categoria": "accesorios", "stock": 40},
    {"id": 5, "nombre": "Comida húmeda para gato", "precio": 2.5, "categoria": "alimento", "stock": 60},
    {"id": 6, "nombre": "Hueso de juguete", "precio": 4.0, "categoria": "juguetes", "stock": 75},
    {"id": 7, "nombre": "Dispensador de agua", "precio": 18.0, "categoria": "accesorios", "stock": 25},
    {"id": 8, "nombre": "Snacks para perro", "precio": 3.5, "categoria": "alimento", "stock": 80},
    {"id": 9, "nombre": "Ratón de peluche", "precio": 3.0, "categoria": "juguetes", "stock": 90},
    {"id": 10, "nombre": "Cepillo para mascotas", "precio": 9.0, "categoria": "accesorios", "stock": 35},
    {"id": 11, "nombre": "Pienso natural", "precio": 22.5, "categoria": "alimento", "stock": 45},
    {"id": 12, "nombre": "Cuerda para morder", "precio": 6.0, "categoria": "juguetes", "stock": 50},
    {"id": 13, "nombre": "Transportín pequeño", "precio": 29.0, "categoria": "accesorios", "stock": 20},
    {"id": 14, "nombre": "Galletas para gato", "precio": 3.8, "categoria": "alimento", "stock": 70},
    {"id": 15, "nombre": "Pelota con sonido", "precio": 7.5, "categoria": "juguetes", "stock": 60},
    {"id": 16, "nombre": "Collar reflectante", "precio": 8.0, "categoria": "accesorios", "stock": 55},
    {"id": 17, "nombre": "Comida seca para perro", "precio": 20.0, "categoria": "alimento", "stock": 65},
    {"id": 18, "nombre": "Juguete interactivo", "precio": 15.0, "categoria": "juguetes", "stock": 40},
    {"id": 19, "nombre": "Cama para mascotas", "precio": 35.0, "categoria": "accesorios", "stock": 30},
    {"id": 20, "nombre": "Snacks naturales para gato", "precio": 4.5, "categoria": "alimento", "stock": 85}
]

# 🔹 GET: Listar todos los productos + filtros opcionales por nombre y categoría
@app.get("/productos/")
def obtener_productos(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría")
):
    resultado = productos
    if nombre:
        resultado = [p for p in resultado if nombre.lower() in p["nombre"].lower()]
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    return {"productos": resultado}

# 🔹 GET: Obtener un producto por ID
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return {"error": "Producto no encontrado"}

# 🔷 POST: Crear un nuevo producto (JSON)
@app.post("/productos/")
def crear_producto(producto: Producto):
    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    nuevo_producto = producto.dict()
    nuevo_producto["id"] = nuevo_id
    productos.append(nuevo_producto)
    return {"mensaje": "Producto creado", "producto": nuevo_producto}

# 🔶 PUT: Actualizar un producto completo (JSON)
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    for p in productos:
        if p["id"] == producto_id:
            p["nombre"] = producto.nombre
            p["precio"] = producto.precio
            p["categoria"] = producto.categoria
            p["stock"] = producto.stock
            return {"mensaje": "Producto actualizado", "producto": p}
    return {"error": "Producto no encontrado"}

# 🟡 PATCH: Actualizar parcialmente un producto (JSON)
@app.patch("/productos/{producto_id}")
def actualizar_parcial_producto(producto_id: int, producto: ProductoParcial):
    for p in productos:
        if p["id"] == producto_id:
            if producto.nombre is not None:
                p["nombre"] = producto.nombre
            if producto.precio is not None:
                p["precio"] = producto.precio
            if producto.categoria is not None:
                p["categoria"] = producto.categoria
            if producto.stock is not None:
                p["stock"] = producto.stock
            return {"mensaje": "Producto actualizado parcialmente", "producto": p}
    return {"error": "Producto no encontrado"}

# 🔻 DELETE: Eliminar un producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {"mensaje": "Producto eliminado"}
    return {"error": "Producto no encontrado"}