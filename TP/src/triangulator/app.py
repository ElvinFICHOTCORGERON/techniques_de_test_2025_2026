""" 
Module App 
Description : Ce module gère l'app avec Flask.
"""
import uuid

from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException

from .execption import PointSetManagerUnavailable, PointSetNotFound, TriangulatorError
from .service import process_triangulation_request


def create_app():
    """Créer et configurer l'instance de l'application Flask."""
    app = Flask(__name__)
    
    
    @app.errorhandler(Exception)
    @app.errorhandler(PointSetNotFound)
    def handle_not_found(error):
        """Gérer les erreurs de ressource non trouvée (404)."""
        return jsonify(
            {"code": "NOT_FOUND", "message": str(error)}
        ), 404

    @app.errorhandler(PointSetManagerUnavailable)
    def handle_service_unavailable(error):
        """Gérer les erreurs de service externe indisponible (503)."""
        return jsonify(
            {"code": "SERVICE_UNAVAILABLE", "message": str(error)}
        ), 503

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Gérer toutes les autres exceptions et les convertir en erreur 500.

        Cette fonction intercepte les erreurs HTTP de Flask pour les laisser
        passer et traite les erreurs métier ainsi que les bugs inattendus.
        """
        if isinstance(error, HTTPException):
            return error

        if isinstance(error, TriangulatorError):
            return jsonify(
                {"code": "INTERNAL_ERROR", "message": str(error)}
            ), 500

        app.logger.error(f"Erreur non gérée: {error}")
        return jsonify(
            {"code": "INTERNAL_ERROR", "message": str(error)}
        ), 500


    @app.route("/triangulation/<pointSetId>", methods=["GET"])
    def get_triangulation(pointSetId):
        """Traiter une demande de triangulation pour un identifiant donné.

        Vérifie d'abord si l'identifiant est un UUID valide, puis délègue
        le traitement à la couche service avant de renvoyer le binaire.
        """
        try:
            uuid.UUID(pointSetId)
        except ValueError:
            return jsonify(
                {"code": "INVALID_ID_FORMAT", "message": 
                "PointSetID must be a valid UUID."}
            ), 400

        triangles_bin = process_triangulation_request(pointSetId)
        
        return Response(
            triangles_bin,
            mimetype='application/octet-stream',
            status=200
        )

    return app