# Threat Model: Fictional Wallet Approval API

**Assets:** authorization permissions, server API secrets, approval records and audit events. **Trust boundary:** a caller supplies untrusted fields to a service that validates authorization and integrity. Nothing connects to a blockchain.

| Threat | Test / control | What remains unresolved |
|---|---|---|
| Cross-wallet operation (BOLA/IDOR) | Check owner or explicitly approved operator | Permission changes and revocation are not modeled |
| Replay of a signed request | Remember nonce after successful approval | In-memory nonces disappear on restart; no atomic concurrent store |
| Altered operation or amount | Canonical HMAC-protected fields | Real secret storage, rotation and client authentication needed |
| Unexpected scope or amount | Only permit one operation and amount bound | No transaction monitoring, risk rules, or multi-person approvals |
| Expired request | Enforce a five-minute validity horizon | Test passes the clock directly; real service requires trusted time |
| Missing investigation records | Record decisions without secret values | No durable tamper-resistant audit trail |

## Separate security concepts

A wallet private key authorizes on-chain asset operations. This exercise's shared HMAC key only authenticates an internal request. API authentication is not sufficient for authorization: an authenticated user still must not act on someone else's wallet. An API approval is **not** a settled blockchain transaction.

## Possible next iteration

Use an actual HTTP API over a localhost test server; centralize user identity; persist permission mappings, used nonces, and audit events in a transactional database; apply rate limiting and key rotation; test simultaneous duplicate submissions.
