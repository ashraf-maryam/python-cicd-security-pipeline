"""Offline wallet-operation authorization simulation. No cryptocurrency is moved."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping
import hashlib
import hmac
import json

class RequestDenied(Exception):
    """Request failed a security check."""

def canonical_message(*, actor: str, wallet: str, operation: str, amount: int,
                      nonce: str, expires_at: int) -> bytes:
    fields = dict(actor=actor, wallet=wallet, operation=operation,
                  amount=amount, nonce=nonce, expires_at=expires_at)
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()

def sign_request(secret: bytes, *, actor: str, wallet: str, operation: str,
                 amount: int, nonce: str, expires_at: int) -> str:
    """Demo request HMAC; NOT a blockchain transaction signature."""
    payload = canonical_message(actor=actor, wallet=wallet, operation=operation,
                                amount=amount, nonce=nonce, expires_at=expires_at)
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()

@dataclass
class WalletApprovalService:
    api_secrets: Mapping[str, bytes]
    wallet_owners: Mapping[str, str]
    allowed_operators: Mapping[str, set[str]] = field(default_factory=dict)
    max_amount: int = 1000
    used_nonces: set[tuple[str, str]] = field(default_factory=set)
    audit_events: list[dict] = field(default_factory=list)

    def approve(self, *, actor: str, wallet: str, operation: str, amount: int,
                nonce: str, expires_at: int, signature: str, now: int) -> dict:
        try:
            self._validate(actor, wallet, operation, amount, nonce,
                           expires_at, signature, now)
        except RequestDenied as exc:
            self.audit_events.append(dict(actor=actor, wallet=wallet,
                                          operation=operation, result="DENIED",
                                          reason=str(exc)))
            raise
        self.used_nonces.add((actor, nonce))
        result = dict(approved=True, actor=actor, wallet=wallet,
                      operation=operation, amount=amount,
                      note="Simulation only: no on-chain transaction")
        self.audit_events.append(dict(actor=actor, wallet=wallet,
                                      operation=operation, result="APPROVED"))
        return result

    def _validate(self, actor, wallet, operation, amount, nonce,
                  expires_at, signature, now):
        if not isinstance(actor, str) or actor not in self.api_secrets:
            raise RequestDenied("unknown actor")
        if not isinstance(wallet, str) or wallet not in self.wallet_owners:
            raise RequestDenied("unknown wallet")
        if operation != "withdraw":
            raise RequestDenied("operation not allowed")
        if type(amount) is not int or not 0 < amount <= self.max_amount:
            raise RequestDenied("amount outside allowed range")
        if (type(now) is not int or type(expires_at) is not int
                or expires_at < now or expires_at > now + 300):
            raise RequestDenied("invalid or expired request")
        if not isinstance(nonce, str) or not 8 <= len(nonce) <= 128:
            raise RequestDenied("invalid nonce")
        if (actor, nonce) in self.used_nonces:
            raise RequestDenied("replayed nonce")
        if (actor != self.wallet_owners[wallet]
                and actor not in self.allowed_operators.get(wallet, set())):
            raise RequestDenied("actor lacks wallet permission")
        if not isinstance(signature, str):
            raise RequestDenied("signature format invalid")
        expected = sign_request(self.api_secrets[actor], actor=actor,
                                wallet=wallet, operation=operation, amount=amount,
                                nonce=nonce, expires_at=expires_at)
        if not hmac.compare_digest(expected, signature):
            raise RequestDenied("request integrity check failed")
