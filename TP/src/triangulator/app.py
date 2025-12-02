# Fichier: src/triangulator/api.py
from flask import Flask, jsonify, Response
from .exceptions import *
from .service import process_triangulation_request
import uuid

def create_app():
    app = Flask(__name__)
    
    
    @app.errorhandler(PointSetNotFound)
    def handle_not_found(error):
        return jsonify({"code": "NOT_FOUND", "message": str(error)}), 404

    @app.errorhandler(PointSetManagerUnavailable)
    def handle_service_unavailable(error):
        return jsonify({"code": "SERVICE_UNAVAILABLE", "message": str(error)}), 503

    @app.errorhandler(TriangulatorError) 
    @app.errorhandler(Exception) 
    def handle_internal_error(error):
        app.logger.error(f"Erreur interne: {error}")
        return jsonify({"code": "INTERNAL_ERROR", "message": "Triangulation failed due to an unexpected server issue."}), 500

    # --- Routes ---

    @app.route("/triangulation/<pointSetId>", methods=["GET"])
    def get_triangulation(pointSetId):
        try:
            uuid.UUID(pointSetId)
        except ValueError:
            return jsonify({"code": "INVALID_ID_FORMAT", "message": "PointSetID must be a valid UUID."}), 400

        triangles_bin = process_triangulation_request(pointSetId)
        
        return Response(
            triangles_bin,
            mimetype='application/octet-stream',
            status=200
        )

    return app