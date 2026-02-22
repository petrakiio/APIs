from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os
import json

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

def _get_webhook_url() -> str:

    url = os.getenv("WEBHOOK") or os.getenv("WEBhOOK")
    if not url:
        raise RuntimeError(
            "Variável WEBHOOK não definida no .env (ou WEBhOOK para legado)."
        )
    return url


def _normalize_message(message: object) -> str:
    if isinstance(message, str):
        return message
    return json.dumps(message, ensure_ascii=False)


def send_test_notification(message: object) -> None:
    webhook = DiscordWebhook(url=_get_webhook_url())
    webhook.content = _normalize_message(message)
    response = webhook.execute()
    if response.status_code not in (200, 204):
        raise RuntimeError(
            f"Falha ao enviar notificação. status={response.status_code}, body={response.text}"
        )
    print(f"Notificação enviada com sucesso. status={response.status_code}")


def send_bruteforce_notification(data: dict[str, object]) -> None:
    """Envia alerta de lockout por brute force em formato embed."""
    try:
        webhook = DiscordWebhook(url=_get_webhook_url(), rate_limit_retry=True)
        embed = DiscordEmbed(
            title="🚨 Alerta de Brute Force",
            description="Um bloqueio de segurança foi acionado no login.",
            color="e74c3c",
        )
        embed.set_timestamp()

        embed.add_embed_field(name="📍 IP", value=str(data.get("ip", "N/A")), inline=True)
        embed.add_embed_field(
            name="👤 Conta",
            value=str(data.get("conta", "N/A")),
            inline=True,
        )
        embed.add_embed_field(
            name="⏱️ Duração do lockout",
            value=f"{data.get('duracao_segundos', 'N/A')}s",
            inline=True,
        )
        embed.add_embed_field(
            name="🗓️ Data/Hora",
            value=str(data.get("data_hora", "N/A")),
            inline=True,
        )
        embed.add_embed_field(
            name="🔓 Bloqueado até",
            value=str(data.get("ate", "N/A")),
            inline=True,
        )
        embed.add_embed_field(
            name="🧱 Tipo de bloqueio",
            value=str(data.get("tipo_bloqueio", "N/A")),
            inline=True,
        )
        webhook.add_embed(embed)

        response = webhook.execute()
        if response.status_code not in (200, 204):
            print(
                "[DISCORD] Falha ao enviar alerta brute force:",
                f"status={response.status_code}",
                f"body={response.text}",
            )
            return
        print(f"[DISCORD] Alerta brute force enviado. status={response.status_code}")
    except Exception as err:
        # Não derruba autenticação por falha externa de notificação.
        print(f"[DISCORD] Erro ao enviar alerta brute force: {err}")
