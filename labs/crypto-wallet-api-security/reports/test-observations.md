# Test observations

Command: `python -m unittest discover -s tests -v`

The local 13-test suite passed when developed. The cases include successful owner and delegated-operator requests, unauthorized cross-wallet access, replay attempts, tampered requests, expiry, value restrictions, unknown operations, incorrect signing keys, and audit records.

These are local unit tests of a simplified Python authorization model, **not** evidence of securing a real wallet, exchange, smart contract or blockchain network. The threat model documents missing production controls.
