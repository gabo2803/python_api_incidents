from app.database import db
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class TipoIncidencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    observacion = db.Column(db.String(250), nullable=False)
    prioridad = db.Column(db.Enum("Baja", "Media", "Alta" , name="incident_prioridad"), nullable=False, default="Media" )   
    fecha_limite = db.Column(db.Date, nullable=True)
    
    # Relación con usuarios
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    asignado_por_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    asignado_a_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    
    # Relaciones con otras tablas
    #equipo_id = db.Column(db.Integer, db.ForeignKey("equipo.id"), nullable=True)
    estado_id = db.Column(db.Integer, db.ForeignKey("estado.id"), nullable=True)
    tipo_incidencia_id = db.Column(db.Integer, db.ForeignKey("tipo_incidencia.id"), nullable=True)
    
    comentario_solucion = db.Column(db.String(500), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Definir relaciones
    user = relationship("User", foreign_keys=[user_id])
    asignado_por = relationship("User", foreign_keys=[asignado_por_id])
    asignado_a = relationship("User", foreign_keys=[asignado_a_id])
    #equipo = relationship("Equipo", foreign_keys=[equipo_id])
    estado = relationship("Estado", foreign_keys=[estado_id])
    tipo_incidencia = relationship("TipoIncidencia", foreign_keys=[tipo_incidencia_id])