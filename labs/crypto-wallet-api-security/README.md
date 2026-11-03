# Crypto Wallet API Security Review — Local Simulation

This exercise asks: **what should an application check before approving a wallet-related operation?** The code models an internal API approval step using fictional actors and wallets; it never connects to a blockchain or transfers cryptocurrency.

I used Python's standard library to model six controls:

| Control | Behavior |
|---|---|
| API request integrity | HMAC-SHA256 protects canonical request fields |
| Wallet authorization | Owner or explicitly delegated operator required |
| Replay check | Accepted nonces recorded per API actor |
| Request expiry | Reject past or excessively future-dated requests |
| Scope and limits | Only one demo operation and bounded positive amounts |
| Audit history | Minimal approval/denial record; no secret values |

HMAC authentication here is **not an on-chain transaction signature**. Actual asset custody, blockchain signing, smart contracts, API permissions, and consensus are separate concerns.

## Run the tests

From this folder, with Python 3.10+:

```bash
python -m unittest discover -s tests -v
```

The 13 tests check owner access, cross-wallet denial, delegated access, replay attempts, edited signed fields, expiry, amount boundaries, operation permissions, invalid credentials, and audit recording.

Read [the threat model](docs/threat-model.md) and [test observations](reports/test-observations.md).

## Limits

- No HTTP server, crypto exchange integration, blockchain signing, real wallets, or real funds.
- The fixed secret values in the tests are made-up demonstration bytes, never production credentials.
- Used nonces and audit events exist only in memory and disappear after restart.
- A trusted clock, persistent nonce store, key vault, real identity controls, and step-up authentication would be required in a real product.
- The service's clock is passed as a parameter to make tests deterministic. Real authorization must use trusted server-side time.

This is a security-design and unit-testing lab, **not a deployed cryptocurrency product**.
