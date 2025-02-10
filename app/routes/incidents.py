from flask import request, jsonify, Blueprint
from app.database import db
from app.models import Incident

# Definir el Blueprint
incidents_bp = Blueprint("incidents", __name__)

# ✅ Ruta para crear un incidente
@incidents_bp.route("/incidents", methods=["POST"])
def create_incident():
    data = request.json
    new_incident = Incident(
        title=data["title"],
        description=data["description"],
        observacion=data["observacion"],
        prioridad=data["prioridad"],
        fecha_limite =data["fecha_limite"],
        user_id=data["user_id"],
        asignado_por_id=data["asignado_por_id"],
        asignado_a_id=data["asigna_a_id"],        
        estado_id=data["estado_id"],
        tipo_incidencia_id=data["tipo_incidencia_id"],
        comentario_solucion=data["comentario_solucion"]      
    )
    db.session.add(new_incident)
    db.session.commit()
    return jsonify({"message": "Incident created successfully"}), 201

# ✅ Ruta para obtener todos los incidentes
@incidents_bp.route("/incidents", methods=["GET"])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([{"id": inc.id, "title": inc.title, "description": inc.description , "observacion":inc.observacion,  "prioridad":inc.prioridad, "fecha_limite":inc.fecha_limite, "estado_id": inc.estado_id,
                      "tipo_incidencia_id": inc.tipo_incidencia_id, "comentario_solucion": inc.comentario_solucion} for inc in incidents])


# ✅ Ruta para obtener un incidentes
@incidents_bp.route("/incidents/<int:id>", methods=["GET"])
def get_incident(id):
    incident= Incident.query.get(id)
    if not incident:
        return jsonify({"error": "incidente no encontrado"}),404
    return jsonify({"id": incident.id, "title": incident.title, "description": incident.description , "observacion":incident.observacion,  "prioridad":incident.prioridad, "fecha_limite":incident.fecha_limite, "estado_id": incident.estado_id,
                      "tipo_incidencia_id": incident.tipo_incidencia_id, "comentario_solucion": incident.comentario_solucion} )

# ✅ Ruta para editar un incidente
@incidents_bp.route("/incidents/<int:id>", methods=["PUT"])
def update_incident(id):
    data = request.json
    # Buscar el incidente por su ID
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({"message": "Incidente no encontrado"}), 404

    # Actualizar los campos del incidente
    incident.title = data.get("title", incident.title)
    incident.description = data.get("description", incident.description)
    incident.observacion = data.get("observacion", incident.observacion)
    incident.prioridad = data.get("prioridad", incident.prioridad)
    incident.fecha_limite = data.get("fecha_limite", incident.fecha_limite)
    incident.user_id = data.get("user_id", incident.user_id)
    incident.asignado_por_id = data.get("asignado_por_id", incident.asignado_por_id)
    incident.asignado_a_id = data.get("asigna_a_id", incident.asignado_a_id)
    incident.estado_id = data.get("estado_id", incident.estado_id)
    incident.tipo_incidencia_id = data.get("tipo_incidencia_id", incident.tipo_incidencia_id)
    incident.comentario_solucion = data.get("comentario_solucion", incident.comentario_solucion)
    
    db.session.commit()
    return jsonify({"message": "Incidente actualizado correctamente"}), 200

# ✅ Ruta para eliminar un incidente
@incidents_bp.route("/incidents/<int:id>", methods=["DELETE"])
def delete_incident(id):
    incident = Incident.query.get(id)    
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    db.session.delete(incident)
    db.session.commit()    
    return jsonify({"message": "Incident deleted successfully"}), 200