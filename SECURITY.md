# Security Policy

## Supported Versions

We are committed to ensuring the security of our users. We currently support security updates for the following versions:

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 2.0.x   | :white_check_mark: | Active Development |
| 1.0.x   | :x:                | End of Life |

## Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please report it to us immediately.

### **Do NOT report security vulnerabilities via public GitHub issues.**

### How to Report

Please email your report to: `security@example.com` (Replace with actual email)

### What to Include

*   **Type of Issue**: (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
*   **Full paths** of source file(s) related to the manifestation of the issue.
*   **Location** of the affected source code (tag/branch/commit or direct URL).
*   **Step-by-step instructions** to reproduce the issue.
*   **Proof-of-concept** or exploit code (if possible).
*   **Impact** of the issue, including how an attacker might exploit it.

### Our Response Policy

1.  **Acknowledgement**: We will acknowledge receipt of your report within 48 hours.
2.  **Assessment**: We will assess the issue and determine its severity.
3.  **Resolution**: We will work to resolve the issue and release a patch as soon as possible.
4.  **Disclosure**: We will coordinate with you on the public disclosure of the vulnerability.

## Security Measures

This project employs the following security measures:
*   **CodeQL Analysis**: Automated vulnerability scanning on every push.
*   **Dependency Auditing**: Automated checks for known vulnerabilities in dependencies (`pip-audit`).
*   **Secret Scanning**: Prevention of accidental secret commits.
*   **Least Privilege**: CI/CD workflows run with restricted permissions.

## License

This project is licensed under the MIT License.
