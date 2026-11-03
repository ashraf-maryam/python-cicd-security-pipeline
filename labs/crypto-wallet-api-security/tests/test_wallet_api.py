import unittest
from src.wallet_api import RequestDenied, WalletApprovalService, sign_request

SECRETS = {"alice": b"fixed-demo-secret-alice-not-real",
           "bob": b"fixed-demo-secret-bob-not-real",
           "ops": b"fixed-demo-secret-ops-not-real"}
NOW = 10000

class WalletSecurityTests(unittest.TestCase):
    def setUp(self):
        self.service = WalletApprovalService(
            SECRETS, {"wallet-a": "alice", "wallet-b": "bob"},
            {"wallet-a": {"ops"}})

    def request(self, actor="alice", wallet="wallet-a", operation="withdraw",
                amount=50, nonce="unique-001", expires_at=NOW+60, now=NOW):
        sig = sign_request(SECRETS[actor], actor=actor, wallet=wallet,
                           operation=operation, amount=amount,
                           nonce=nonce, expires_at=expires_at)
        return dict(actor=actor, wallet=wallet, operation=operation,
                    amount=amount, nonce=nonce, expires_at=expires_at,
                    now=now, signature=sig)

    def test_valid_owner_request(self):
        self.assertTrue(self.service.approve(**self.request())["approved"])

    def test_cross_wallet_access_denied(self):
        with self.assertRaisesRegex(RequestDenied, "lacks wallet permission"):
            self.service.approve(**self.request(wallet="wallet-b"))

    def test_delegated_operator_allowed(self):
        self.assertTrue(self.service.approve(**self.request(actor="ops"))["approved"])

    def test_replay_denied(self):
        req = self.request()
        self.service.approve(**req)
        with self.assertRaisesRegex(RequestDenied, "replayed nonce"):
            self.service.approve(**req)

    def test_changed_amount_breaks_signature(self):
        req = self.request()
        req["amount"] = 999
        with self.assertRaisesRegex(RequestDenied, "integrity"):
            self.service.approve(**req)

    def test_expired_request_denied(self):
        with self.assertRaisesRegex(RequestDenied, "expired"):
            self.service.approve(**self.request(expires_at=NOW-1))

    def test_unreasonably_far_expiry_denied(self):
        with self.assertRaisesRegex(RequestDenied, "expired"):
            self.service.approve(**self.request(expires_at=NOW+10000))

    def test_over_limit_denied(self):
        with self.assertRaisesRegex(RequestDenied, "amount"):
            self.service.approve(**self.request(amount=1001))

    def test_boolean_amount_denied(self):
        with self.assertRaisesRegex(RequestDenied, "amount"):
            self.service.approve(**self.request(amount=True))

    def test_unapproved_operation_denied(self):
        with self.assertRaisesRegex(RequestDenied, "operation"):
            self.service.approve(**self.request(operation="grant_admin"))

    def test_wrong_actor_secret_rejected(self):
        req = self.request()
        req["signature"] = sign_request(SECRETS["bob"], actor="alice",
                                         wallet="wallet-a", operation="withdraw",
                                         amount=50, nonce="unique-001",
                                         expires_at=NOW+60)
        with self.assertRaisesRegex(RequestDenied, "integrity"):
            self.service.approve(**req)

    def test_denial_audited(self):
        with self.assertRaises(RequestDenied):
            self.service.approve(**self.request(wallet="wallet-b"))
        self.assertEqual(self.service.audit_events[0]["result"], "DENIED")

    def test_rejected_attempt_does_not_consume_nonce(self):
        req = self.request()
        req["signature"] = "f"*64
        with self.assertRaises(RequestDenied):
            self.service.approve(**req)
        self.assertTrue(self.service.approve(**self.request())["approved"])

if __name__ == "__main__":
    unittest.main()
