import re

from flask import Blueprint, jsonify, request, session

from backend.auth.models import create_user, get_user_by_email, verify_password


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "JSON inválido."
        }), 400

    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    if not email or not EMAIL_PATTERN.fullmatch(email):
        return jsonify({
            "error": "E-mail inválido."
        }), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            "error": "A senha deve ter pelo menos 8 caracteres."
        }), 400

    if len(password) > 128:
        return jsonify({
            "error": "A senha deve ter no máximo 128 caracteres."
        }), 400

    if get_user_by_email(email):
        return jsonify({
            "error": "E-mail já cadastrado."
        }), 409

    try:
        user_id = create_user(email, password)
    except Exception:
        return jsonify({
            "error": "Não foi possível criar a conta."
        }), 500

    return jsonify({
        "message": "Conta criada com sucesso.",
        "user": {
            "id": user_id,
            "email": email
        }
    }), 201



@auth_bp.get("/me")
def me():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Não autenticado."
        }), 401

    connection = None

    try:
        from backend.database import get_connection

        connection = get_connection()

        user = connection.execute(
            """
            SELECT
                id,
                email,
                plan,
                subscription_status,
                message_limit,
                messages_used,
                created_at,
                updated_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    finally:
        if connection:
            connection.close()

    if not user:
        session.clear()

        return jsonify({
            "error": "Usuário não encontrado."
        }), 401

    return jsonify({
        "user": dict(user)
    }), 200


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "JSON inválido."
        }), 400

    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    if not email or not isinstance(password, str):
        return jsonify({
            "error": "E-mail e senha são obrigatórios."
        }), 400

    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({
            "error": "E-mail ou senha inválidos."
        }), 401

    session.clear()
    session["user_id"] = user["id"]

    return jsonify({
        "message": "Login realizado com sucesso.",
        "user": {
            "id": user["id"],
            "email": user["email"]
        }
    }), 200
