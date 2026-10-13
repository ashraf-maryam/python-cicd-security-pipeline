# Python CI/CD & Security Verification

An educational Python project demonstrating automated testing and security scanning in **GitHub Actions** and **Jenkins**. The sample application generates and validates time-limited tokens; the pipelines run unit tests, examine the source for potential security issues, and check Python dependencies.

> **Learning project — not production authentication software.** The token implementation intentionally uses an insecure hardcoded demonstration secret and MD5-based signing so security scanning and review can identify weaknesses. Do not deploy it or use it to protect real accounts.

## What this project demonstrates

- A Python token service with generation, expiration checks, and signature validation
- **Nine pytest test cases** covering expected behavior, empty or malformed input, expiration, and tampering
- CI automation on pushes and pull requests with GitHub Actions
- A Jenkins pipeline with checkout, virtual-environment setup, tests, security scans, and report archiving
- **Bandit** static application security testing (SAST)
- **pip-audit** dependency vulnerability checking (SCA)

## Repository structure

```text
.github/workflows/ci.yml  # GitHub Actions workflow
Jenkinsfile               # Jenkins declarative pipeline
token_service.py          # Demonstration token generator and validator
test_token_service.py     # Nine pytest tests
requirements.txt          # Development and scanning tools
.gitignore
```

## Run the tests locally

Requires Python 3.11 or a compatible Python 3 version.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

To run the scanners manually:

```bash
bandit -r token_service.py
pip-audit -r requirements.txt
```

## How the CI/CD pipelines work

**GitHub Actions** (`.github/workflows/ci.yml`) runs on pushes and pull requests targeting `main` and `develop`:

1. Check out the source code.
2. Set up Python 3.11 and install dependencies.
3. Run pytest (a failing test fails this job).
4. Run Bandit and write an HTML report to `reports/bandit-report.html`.
5. Run pip-audit against `requirements.txt`.
6. Upload the `reports/` directory as a workflow artifact.

**Jenkins** (`Jenkinsfile`) performs a comparable sequence using a Python virtual environment and archives report files.

**Important scan behavior:** In both configurations, the Bandit and pip-audit commands end with `|| true`. This lets the pipeline collect and display findings without failing the build because of scan results. These are **informational security scans, not enforced security gates**. The intentionally insecure demo code remains in the project for analysis.

## What I tested and learned

The test suite includes nine cases: successful token creation and validation; rejected empty user IDs, null or empty tokens, malformed tokens, invalid Base64, expired tokens, and tampered tokens. Building and troubleshooting the GitHub Actions and Jenkins workflows provided practice with CI configuration, dependencies, logs, repeatable automated testing, and interpreting security tool findings.

## Limitations and potential improvements

- Replace MD5-based signing with an appropriate cryptographic mechanism and manage secrets securely if adapting these ideas for production.
- Decide on enforceable security-scan policies instead of `|| true` when moving beyond the demonstration.
- Pin and maintain dependency versions, expand edge-case testing, and publish test/scan summaries.

**Purpose:** This repository documents hands-on CI/CD and software security verification coursework, not a production deployment.
