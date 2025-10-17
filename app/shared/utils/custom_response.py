from typing import Any, Dict, List, Tuple

ApiResponse = Tuple[Dict[str, Any], int]


class CustomResponse:
    @staticmethod
    def ok(
        data: Dict[str, Any] | List[Dict[str, Any]] | None = None, message: str = "OK"
    ) -> ApiResponse:
        return {"status": "success", "message": message, "data": data or {}}, 200

    @staticmethod
    def bad_request(message: str = "Error Request") -> ApiResponse:
        return {"status": "error", "message": message}, 400

    @staticmethod
    def unauthorized(message: str = "Access Unauthorized") -> ApiResponse:
        return {"status": "error", "message": message}, 401

    @staticmethod
    def not_found(message: str = "Resource Not found") -> ApiResponse:
        return {"status": "error", "message": message}, 404

    @staticmethod
    def server_error(message: str = "Internal Error Server") -> ApiResponse:
        return {"status": "error", "message": message}, 500
