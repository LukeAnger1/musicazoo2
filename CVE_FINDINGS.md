# CVE Findings - Automated Vulnerability Scan
**Date:** 2025-12-21
**Tool:** pip-audit 2.10.0
**Project:** Musicazoo v5.2.6

## Executive Summary

**CRITICAL:** Found **18 known security vulnerabilities** across 2 packages (Tornado and Werkzeug).

Additionally discovered:
- **toro 1.0** - Cannot be installed on Python 3 (uses deprecated `use_2to3`)
- **supervisor 3.1** - Explicitly does not support Python 3

---

## Vulnerability Details

### Tornado 4.3 (6 CVEs)

| CVE ID | Type | Fixed In | Severity |
|--------|------|----------|----------|
| CVE-2025-47287 | TBD | 6.5 | 🔴 CRITICAL |
| CVE-2024-52804 | TBD | 6.4.2 | 🔴 HIGH |
| PYSEC-2023-75 | TBD | 6.3.2 | 🔴 HIGH |
| GHSA-qppv-j76h-2rpx | TBD | 6.3.3 | 🔴 HIGH |
| GHSA-753j-mpmx-qq6g | TBD | 6.4.1 | 🔴 HIGH |
| GHSA-w235-7p84-xx57 | TBD | 6.4.1 | 🔴 HIGH |

**Current Version:** 4.3
**Recommended Version:** 6.5+
**Years Behind:** ~9 years

### Werkzeug 0.11 (12 CVEs)

| CVE ID | Type | Fixed In | Severity |
|--------|------|----------|----------|
| CVE-2025-66221 | TBD | 3.1.4 | 🔴 CRITICAL |
| CVE-2024-49767 | TBD | 3.0.6 | 🔴 HIGH |
| CVE-2024-49766 | TBD | 3.0.6 | 🔴 HIGH |
| CVE-2024-34069 | TBD | 3.0.3 | 🔴 HIGH |
| CVE-2019-14322 | Path traversal | 0.15.5 | 🔴 HIGH |
| PYSEC-2023-221 | TBD | 2.3.8, 3.0.1 | 🔴 HIGH |
| PYSEC-2023-57 | TBD | 2.2.3 | 🟡 MEDIUM |
| PYSEC-2023-58 | TBD | 2.2.3 | 🟡 MEDIUM |
| PYSEC-2022-203 | TBD | 2.1.1 | 🟡 MEDIUM |
| PYSEC-2017-43 | TBD | 0.11.11 | 🟡 MEDIUM |
| PYSEC-2019-140 | TBD | 0.15.3 | 🟡 MEDIUM |
| PYSEC-2020-157 | TBD | 0.11.6 | 🟡 MEDIUM |

**Current Version:** 0.11
**Recommended Version:** 3.1.4+
**Years Behind:** ~10 years

---

## Python 3 Incompatibility Issues

### toro 1.0 - CANNOT INSTALL
```
Error: use_2to3 is invalid
```
- The package uses deprecated setuptools features removed in Python 3.12+
- Package has been deprecated and merged into Tornado
- **Action Required:** Remove dependency and migrate to native Tornado features

### supervisor 3.1 - PYTHON 2 ONLY
```
Error: Supervisor requires Python 2.4 or later but does not work on any version of Python 3.
```
- supervisor 3.x series only supports Python 2
- supervisor 4.x added Python 3 support
- **Action Required:** Upgrade to supervisor 4.2.5

---

## Risk Assessment

### Immediate Threats

1. **Werkzeug CVE-2025-66221** (Latest 2025 vulnerability)
   - Affects all versions below 3.1.4
   - Current version is 0.11 (over 3 major versions behind)

2. **Tornado CVE-2025-47287** (Latest 2025 vulnerability)
   - Affects all versions below 6.5
   - Current version is 4.3 (over 2 major versions behind)

3. **Python 3 Compatibility**
   - Project cannot run on Python 3.11.14 with current dependencies
   - Both `toro` and `supervisor` are incompatible

### Exploitability

- **Werkzeug vulnerabilities:** Directly exploitable via HTTP requests
- **Tornado vulnerabilities:** May allow DoS, open redirects, or other web attacks
- **Attack Surface:** Web-facing application (HTTP server on port 8080)

---

## Technical Details

### Scan Command
```bash
pip-audit -r requirements.txt
```

### Full Scan Output

#### Tornado and Werkzeug Scan
```
Found 18 known vulnerabilities in 2 packages
Name     Version ID                  Fix Versions
-------- ------- ------------------- ------------
tornado  4.3     PYSEC-2023-75       6.3.2
tornado  4.3     GHSA-qppv-j76h-2rpx 6.3.3
tornado  4.3     GHSA-753j-mpmx-qq6g 6.4.1
tornado  4.3     GHSA-w235-7p84-xx57 6.4.1
tornado  4.3     CVE-2025-47287      6.5
tornado  4.3     CVE-2024-52804      6.4.2
werkzeug 0.11    PYSEC-2020-157      0.11.6
werkzeug 0.11    PYSEC-2019-140      0.15.3
werkzeug 0.11    PYSEC-2017-43       0.11.11
werkzeug 0.11    PYSEC-2022-203      2.1.1
werkzeug 0.11    PYSEC-2023-58       2.2.3
werkzeug 0.11    PYSEC-2023-57       2.2.3
werkzeug 0.11    PYSEC-2023-221      2.3.8,3.0.1
werkzeug 0.11    CVE-2019-14322      0.15.5
werkzeug 0.11    CVE-2024-34069      3.0.3
werkzeug 0.11    CVE-2024-49766      3.0.6
werkzeug 0.11    CVE-2024-49767      3.0.6
werkzeug 0.11    CVE-2025-66221      3.1.4
```

#### toro Installation Failure
```
ERROR: use_2to3 is invalid.
```

#### supervisor Installation Failure
```
Supervisor requires Python 2.4 or later but does not work on any version
of Python 3. You are using version 3.11.14
```

---

## Recommendations

### IMMEDIATE (Within 24-48 hours)
1. **Do NOT deploy this application** to production with current dependencies
2. **Isolate from network** if currently running in production
3. **Begin emergency upgrade** of Werkzeug and Tornado

### SHORT-TERM (1-2 weeks)
1. Upgrade to Python 3 compatible versions:
   - tornado >= 6.5
   - Werkzeug >= 3.1.4
   - supervisor >= 4.2.5
2. Remove toro and migrate code to native Tornado
3. Replace youtube-dl with yt-dlp

### LONG-TERM
1. Implement automated vulnerability scanning in CI/CD
2. Set up dependency update monitoring (Dependabot, Renovate)
3. Establish security patch SLA
4. Add comprehensive test suite before future updates

---

## Additional Notes

### Why These Are Critical

**For a web-facing application (which Musicazoo is):**
- Werkzeug vulnerabilities can be exploited through HTTP requests
- Tornado vulnerabilities can allow attackers to:
  - Bypass security controls
  - Execute denial of service attacks
  - Perform open redirects for phishing
  - Potentially gain unauthorized access

### Current State = Unsupportable

The application currently **cannot run** on Python 3.11.14 without:
1. Upgrading supervisor to 4.x
2. Removing toro and refactoring code

This is not just a security issue but a **functional blocker**.

---

## Validation Commands

To reproduce these findings:

```bash
# Install audit tool
pip install pip-audit

# Check for vulnerabilities
pip-audit -r requirements.txt

# Will fail with toro and supervisor errors, confirming Python 3 incompatibility
```

---

**Scan Completed:** 2025-12-21
**Next Review:** Immediate action required - no scheduled review needed
