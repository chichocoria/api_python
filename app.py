from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos iniciales
tareas = [
    {"id": 1, "titulo": "Aprender Flask", "completado": False},
    {"id": 2, "titulo": "Hacer una API", "completado": False},
]

# Obtener todas las tareas
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas)

# Obtener una tarea por ID
@app.route("/tareas/<int:id>", methods=["GET"])
def obtener_tarea(id):
    tarea = next((t for t in tareas if t["id"] == id), None)
    if tarea is None:
        return jsonify({"mensaje": "Tarea no encontrada"}), 404
    return jsonify(tarea)

# Crear una nueva tarea
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    nueva_tarea = request.get_json()
    nueva_tarea["id"] = len(tareas) + 1
    tareas.append(nueva_tarea)
    return jsonify(nueva_tarea), 201

# Actualizar una tarea
@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    tarea = next((t for t in tareas if t["id"] == id), None)
    if tarea is None:
        return jsonify({"mensaje": "Tarea no encontrada"}), 404

    datos = request.get_json()
    tarea.update(datos)
    return jsonify(tarea)

# Eliminar una tarea
@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    global tareas
    tareas = [t for t in tareas if t["id"] != id]
    return jsonify({"mensaje": "Tarea eliminada"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
