from flask import request


def get_ip() -> str:
    """Retorna o IP real do cliente, considerando proxy reverso."""
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        # Usa o primeiro IP da cadeia (cliente original).
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP", "").strip()
    if real_ip:
        return real_ip

    return (request.remote_addr or "unknown").strip()
