# Dependency Audit Report
**Date:** 2025-12-21
**Project:** Musicazoo
**Current Version:** 5.2.6
**Branch:** claude/audit-dependencies-MYsuU

## Executive Summary

This audit identifies **critical security vulnerabilities** and **significant outdated dependencies** in the Musicazoo project. All core dependencies are from 2015 or earlier, posing security risks and compatibility issues with modern Python environments.

**Risk Level:** 🔴 **CRITICAL**

**⚠️ See CVE_FINDINGS.md for detailed vulnerability scan results (18 CVEs found)**

### Key Findings:
- **18 known CVEs** affecting Tornado and Werkzeug (confirmed via pip-audit)
- **Python 3 incompatibility:** toro and supervisor 3.1 cannot run on Python 3.11.14
- 6 out of 6 core dependencies are severely outdated (8-10 years old)
- 1 dependency is completely deprecated (toro)
- 1 dependency has an actively maintained replacement (youtube-dl → yt-dlp)

---

## Detailed Dependency Analysis

### Core Dependencies (requirements.txt)

#### 1. tornado==4.3 🔴 CRITICAL
- **Current Pinned Version:** 4.3 (2015)
- **Latest Stable Version:** 6.5+ (2025)
- **Years Outdated:** ~9 years
- **Security Issues:** **6 CVEs identified by pip-audit**
  - CVE-2025-47287 (fix: 6.5)
  - CVE-2024-52804 (fix: 6.4.2)
  - PYSEC-2023-75 (fix: 6.3.2)
  - GHSA-qppv-j76h-2rpx (fix: 6.3.3)
  - GHSA-753j-mpmx-qq6g (fix: 6.4.1)
  - GHSA-w235-7p84-xx57 (fix: 6.4.1)
- **Breaking Changes:** Major API changes from 4.x to 5.x to 6.x
- **Recommendation:** Upgrade to 6.5+ with code migration
- **Effort:** HIGH - requires significant code changes

#### 2. toro==1.0 🔴 DEPRECATED
- **Current Pinned Version:** 1.0 (2014)
- **Status:** DEPRECATED - Package is no longer maintained
- **Latest Version:** 1.0.1 (final release)
- **Python 3 Compatibility:** ❌ **FAILS TO INSTALL** - uses deprecated `use_2to3`
- **Issue:** Functionality has been merged into Tornado itself since Tornado 5.0
- **Recommendation:** Remove dependency and migrate to native Tornado async primitives
- **Effort:** MEDIUM - code refactoring required
- **Migration Path:** Use `tornado.locks`, `tornado.queues` instead of toro equivalents

#### 3. youtube-dl>=2015.11.19 🔴 CRITICAL
- **Current Minimum Version:** 2015.11.19 (2015)
- **Status:** Effectively unmaintained (DMCA takedown in 2020, minimal updates since)
- **Issue:**
  - Many video sites no longer work
  - Missing modern site support
  - Security vulnerabilities not being patched
- **Active Alternative:** yt-dlp (actively maintained fork)
- **Recommendation:** Replace with yt-dlp
- **Effort:** LOW - mostly compatible API
- **Note:** yt-dlp is a drop-in replacement with better site support

#### 4. supervisor==3.1 🔴 CRITICAL
- **Current Pinned Version:** 3.1.x (2013)
- **Latest Stable Version:** 4.2.5 (2023)
- **Years Outdated:** ~10 years
- **Python 3 Compatibility:** ❌ **DOES NOT SUPPORT PYTHON 3** - requires Python 2 only
- **Security Issues:** Various security fixes in 4.x series
- **Breaking Changes:** Minimal between 3.x and 4.x (except Python 3 support)
- **Recommendation:** Upgrade to 4.2.5 (REQUIRED for Python 3)
- **Effort:** LOW - supervisor is relatively stable between versions

#### 5. Werkzeug==0.11 🔴 CRITICAL
- **Current Pinned Version:** 0.11 (2015)
- **Latest Stable Version:** 3.1.4+ (2025)
- **Years Outdated:** ~10 years
- **Security Issues:** **12 CVEs identified by pip-audit**
  - CVE-2025-66221 (fix: 3.1.4) - Latest 2025 vulnerability
  - CVE-2024-49767 (fix: 3.0.6)
  - CVE-2024-49766 (fix: 3.0.6)
  - CVE-2024-34069 (fix: 3.0.3)
  - CVE-2019-14322 (fix: 0.15.5) - Path traversal
  - PYSEC-2023-221 (fix: 2.3.8, 3.0.1)
  - Plus 6 more CVEs (see CVE_FINDINGS.md)
- **Breaking Changes:** Major API changes across versions
- **Recommendation:** Upgrade to 3.1.4+ with thorough testing
- **Effort:** MEDIUM-HIGH - API has evolved significantly
- **Note:** Critical for web security

#### 6. shmooze==1.2.4 🟡 UNKNOWN
- **Current Pinned Version:** 1.2.4
- **Status:** Unable to verify maintenance status
- **Latest Version:** 1.2.4 appears to be latest
- **Recommendation:** Verify if still maintained; consider alternatives if not
- **Effort:** N/A - requires investigation
- **Note:** This appears to be a WSGI framework wrapper

### Optional Dependencies (requirements-optional.txt)

#### 7. pyalsaaudio==0.8.2 🟡 OUTDATED
- **Current Pinned Version:** 0.8.2 (2015)
- **Latest Stable Version:** 0.11.0 (2024)
- **Years Outdated:** ~9 years
- **Security Issues:** None known
- **Breaking Changes:** Minimal
- **Recommendation:** Upgrade to 0.11.0
- **Effort:** LOW

---

## Security Risk Assessment

### Critical Vulnerabilities (Immediate Action Required)

1. **Werkzeug 0.11** - Multiple CVEs including DoS and data parsing vulnerabilities
2. **Tornado 4.3** - Open redirect and DoS vulnerabilities
3. **youtube-dl** - Unmaintained, potential security issues in video parsing

### Compatibility Risks

1. **Python Version Compatibility**
   - Current dependencies from Python 2 era
   - System running Python 3.11.14
   - Some packages may have compatibility issues or use deprecated Python features

2. **Dependency Conflicts**
   - Pinned versions may conflict with other system packages
   - Old versions may not install on modern systems without legacy tooling

---

## Recommended Action Plan

### Phase 1: Immediate Security Fixes (Priority: CRITICAL)
1. **Werkzeug:** Upgrade to 3.0.x
   - Test all web endpoints
   - Update code for API changes
2. **Tornado:** Upgrade to 6.4.x
   - Migrate async code patterns
   - Update WebSocket implementations
3. **youtube-dl:** Replace with yt-dlp
   - Update import statements
   - Test video playback functionality

### Phase 2: Deprecation Removal (Priority: HIGH)
1. **toro:** Remove and migrate to native Tornado features
   - Replace toro.Queue with tornado.queues.Queue
   - Replace toro.Lock with tornado.locks.Lock
   - Update all async coordination code

### Phase 3: General Updates (Priority: MEDIUM)
1. **supervisor:** Upgrade to 4.2.5
   - Test supervisord.conf compatibility
   - Update any supervisor-specific code
2. **pyalsaaudio:** Upgrade to 0.11.0
   - Test audio functionality

### Phase 4: Verification (Priority: HIGH)
1. **shmooze:** Investigate maintenance status
   - Check for updates or alternatives
   - Evaluate replacing with modern WSGI server (gunicorn, uvicorn)

---

## Testing Requirements

After any dependency updates, the following must be tested:

- [ ] Web interface loads and functions correctly
- [ ] Queue service starts and manages modules
- [ ] Volume control works
- [ ] NLP interface responds to commands
- [ ] Video playback (youtube-dl/yt-dlp)
- [ ] Audio output (pyalsaaudio if installed)
- [ ] Supervisor configuration and process management
- [ ] All JSON endpoints (/queue, /vol, /nlp)

---

## Version Compatibility Matrix

| Package | Current | Latest | Python 3.11 Compatible | Notes |
|---------|---------|--------|------------------------|-------|
| tornado | 4.3 | 6.4.x | ⚠️ Yes, but outdated | Requires migration |
| toro | 1.0 | N/A (deprecated) | ❌ Use Tornado native | Must remove |
| youtube-dl | 2015.11.19+ | 2021.x | ⚠️ Unmaintained | Replace with yt-dlp |
| supervisor | 3.1 | 4.2.5 | ✅ Yes | Should update |
| Werkzeug | 0.11 | 3.0.x | ⚠️ Yes, but critical CVEs | Must update |
| shmooze | 1.2.4 | 1.2.4 | ❓ Unknown | Needs investigation |
| pyalsaaudio | 0.8.2 | 0.11.0 | ✅ Yes | Optional update |

---

## Estimated Migration Effort

| Phase | Effort | Risk | Timeline Estimate |
|-------|--------|------|-------------------|
| Phase 1 (Security) | High | High | 2-3 weeks |
| Phase 2 (Deprecation) | Medium | Medium | 1-2 weeks |
| Phase 3 (Updates) | Low | Low | 3-5 days |
| Phase 4 (Verification) | Low | Low | 1-2 days |
| **Total** | **High** | **High** | **4-6 weeks** |

---

## Additional Recommendations

1. **Add dependency version ranges** instead of pinning exact versions:
   - Example: `tornado>=6.4,<7.0` instead of `tornado==4.3`
   - This allows security patches while preventing breaking changes

2. **Implement automated dependency scanning:**
   - Use `pip-audit` or `safety` to check for known vulnerabilities
   - Integrate into CI/CD pipeline

3. **Consider modernization:**
   - Evaluate if Tornado is still the best choice vs. FastAPI, Flask, etc.
   - Consider containerization (Docker) for consistent environments

4. **Add testing infrastructure:**
   - Unit tests for core functionality
   - Integration tests for dependency changes
   - This project appears to lack automated tests

5. **Document Python version requirements:**
   - Specify minimum Python version in setup.py
   - Add python_requires='>=3.8' or similar

---

## Conclusion

The current dependency state poses **significant security and maintenance risks**. Immediate action is required to address critical vulnerabilities in Werkzeug and Tornado. The use of deprecated (toro) and unmaintained (youtube-dl) packages further increases technical debt.

**Recommended Next Steps:**
1. Create a test environment to validate changes
2. Begin Phase 1 security updates immediately
3. Plan for systematic migration following the phased approach
4. Establish ongoing dependency monitoring

---

## Appendix: Useful Commands

```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Check outdated packages
pip list --outdated

# Update a specific package
pip install --upgrade <package-name>

# Test installation
pip install -r requirements.txt

# Create updated requirements
pip freeze > requirements-new.txt
```

---

**Audit Completed By:** Claude (AI Assistant)
**Review Status:** Draft - requires human review and validation
