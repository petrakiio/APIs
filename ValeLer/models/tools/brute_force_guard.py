import os
import time
from datetime import datetime
from collections import defaultdict, deque
from threading import Lock
from connection.notification_conn import send_bruteforce_notification


def _to_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


class BruteForceGuard:
    def __init__(self):
        # Configurável por ambiente para facilitar ajuste entre dev/prod.
        self.max_attempts = _to_int(os.getenv("LOGIN_MAX_ATTEMPTS"), 5)
        self.window_seconds = _to_int(os.getenv("LOGIN_WINDOW_SECONDS"), 300)
        self.lockout_seconds = _to_int(os.getenv("LOGIN_LOCKOUT_SECONDS"), 900)
        self._lock = Lock()
        # Histórico de tentativas dentro da janela (IP e conta).
        self._attempts_ip = defaultdict(deque)
        self._attempts_account = defaultdict(deque)
        # Momento (timestamp) até quando a origem/conta fica bloqueada.
        self._blocked_ip_until = {}
        self._blocked_account_until = {}
        # Armazena IPs em lockout e a duração aplicada.
        self.atq = {}

    @staticmethod
    def _normalize_account(account: str | None) -> str:
        return (account or "").strip().lower()

    def _prune(self, attempts: deque, now: float) -> None:
        # Remove tentativas antigas para manter apenas a janela ativa.
        while attempts and now - attempts[0] > self.window_seconds:
            attempts.popleft()

    @staticmethod
    def _format_datetime(ts: float | None = None) -> str:
        base = ts if ts is not None else time.time()
        return datetime.fromtimestamp(base).strftime("%Y-%m-%d %H:%M:%S")

    def _seconds_left(self, blocked_until: float | None, now: float) -> int:
        if not blocked_until:
            return 0
        remaining = int(blocked_until - now)
        return remaining if remaining > 0 else 0

    def check_block(self, ip: str, account: str | None) -> tuple[bool, int]:
        normalized_account = self._normalize_account(account)
        now = time.time()
        with self._lock:
            # Bloqueia se IP OU conta ainda estiverem em lockout.
            left_ip = self._seconds_left(self._blocked_ip_until.get(ip), now)
            left_account = self._seconds_left(
                self._blocked_account_until.get(normalized_account), now
            )
            wait_seconds = max(left_ip, left_account)
            if wait_seconds > 0:
                print(
                    "[BRUTE_FORCE] Tentativa bloqueada:",
                    f"data_hora={self._format_datetime(now)}",
                    f"ip={ip}",
                    f"conta={normalized_account or 'N/A'}",
                    f"aguarde={wait_seconds}s",
                )
                return True, wait_seconds
            return False, 0

    def register_failure(self, ip: str, account: str | None) -> None:
        normalized_account = self._normalize_account(account)
        now = time.time()
        notification_payload = None
        with self._lock:
            # Registra a tentativa falha nas duas dimensões.
            ip_attempts = self._attempts_ip[ip]
            account_attempts = self._attempts_account[normalized_account]
            ip_attempts.append(now)
            account_attempts.append(now)
            self._prune(ip_attempts, now)
            self._prune(account_attempts, now)
            print(
                "[BRUTE_FORCE] Falha de login:",
                f"data_hora={self._format_datetime(now)}",
                f"ip={ip}",
                f"conta={normalized_account or 'N/A'}",
                f"tentativas_ip={len(ip_attempts)}/{self.max_attempts}",
                f"tentativas_conta={len(account_attempts)}/{self.max_attempts}",
            )

            # Ao atingir o limite, aplica lockout e zera o contador local.
            ip_locked = False
            account_locked = False
            if len(ip_attempts) >= self.max_attempts:
                ip_locked = True
                self._blocked_ip_until[ip] = now + self.lockout_seconds
                self.atq[ip] = {
                    "duracao_segundos": self.lockout_seconds,
                    "data_hora": self._format_datetime(now),
                    "ate": self._format_datetime(now + self.lockout_seconds),
                }
                ip_attempts.clear()
                print(
                    "[BRUTE_FORCE] Lockout por IP:",
                    f"data_hora={self._format_datetime(now)}",
                    f"ip={ip}",
                    f"duracao={self.lockout_seconds}s",
                    f"atq={self.atq}",
                )

            if normalized_account and len(account_attempts) >= self.max_attempts:
                account_locked = True
                self._blocked_account_until[normalized_account] = (
                    now + self.lockout_seconds
                )
                account_attempts.clear()
                print(
                    "[BRUTE_FORCE] Lockout por conta:",
                    f"data_hora={self._format_datetime(now)}",
                    f"conta={normalized_account}",
                    f"duracao={self.lockout_seconds}s",
                )

            if ip_locked or account_locked:
                if ip_locked and account_locked:
                    tipo_bloqueio = "IP + Conta"
                elif ip_locked:
                    tipo_bloqueio = "IP"
                else:
                    tipo_bloqueio = "Conta"

                notification_payload = {
                    "ip": ip,
                    "conta": normalized_account or "N/A",
                    "duracao_segundos": self.lockout_seconds,
                    "data_hora": self._format_datetime(now),
                    "ate": self._format_datetime(now + self.lockout_seconds),
                    "tipo_bloqueio": tipo_bloqueio,
                }

        if notification_payload:
            send_bruteforce_notification(notification_payload)

    def register_success(self, ip: str, account: str | None) -> None:
        normalized_account = self._normalize_account(account)
        with self._lock:
            # Login válido limpa estado para não manter bloqueios indevidos.
            self._attempts_ip.pop(ip, None)
            self._blocked_ip_until.pop(ip, None)
            if normalized_account:
                self._attempts_account.pop(normalized_account, None)
                self._blocked_account_until.pop(normalized_account, None)


brute_force_guard = BruteForceGuard()
