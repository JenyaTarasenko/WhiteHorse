

import ssl
import socket
from urllib.parse import urlparse, urljoin
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend

HEADERS = {"User-Agent": "QuickScanner/1.0 (https://example.com/)"}
COMMON_PATHS = [".env", ".git/HEAD", ".git/config", "backup.zip", "db.sql",
                "admin/", "robots.txt", "sitemap.xml", ".htpasswd", "config.php"]
XSS_PAYLOAD = "<sCrIpT>qXssCheck()</sCrIpT>"

def norm_url(u):
    if not u.startswith("http://") and not u.startswith("https://"):
        u = "https://" + u
    return u.rstrip("/")

def safe_get(u, timeout=10):
    try:
        r = requests.get(u, headers=HEADERS, timeout=timeout, allow_redirects=True, verify=True)
        return r
    except Exception as e:
        return None

def check_headers(base):
    r = safe_get(base)
    wanted = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options",
              "X-Content-Type-Options","Referrer-Policy","Permissions-Policy"]
    headers = {}
    if not r:
        return {"error": "no_response"}
    for h in wanted:
        headers[h] = r.headers.get(h)
    return {"headers": headers, "status_code": r.status_code}

def check_common_paths(base):
    results = []
    for p in COMMON_PATHS:
        u = urljoin(base + "/", p)
        r = safe_get(u)
        if r:
            size = len(r.content or b"")
            snippet = (r.text[:200].replace("\n"," ") + "...") if r.text and len(r.text) > 200 else (r.text or "")
            results.append({
                "path": p,
                "url": u,
                "status_code": r.status_code,
                "size": size,
                "snippet": snippet
            })
        else:
            results.append({"path": p, "url": u, "status_code": None})
    return {"common_paths": results}

def simple_xss_check(base):
    if "?" in base:
        u = base + "&q=" + XSS_PAYLOAD
    else:
        u = base + "/?q=" + XSS_PAYLOAD
    r = safe_get(u)
    found = False
    if r and r.text and XSS_PAYLOAD in r.text:
        found = True
    return {"xss": {"tested_url": u, "payload_found": found}}

def check_robots_sitemap(base):
    found = {}
    for p in ["robots.txt","sitemap.xml"]:
        u = urljoin(base + "/", p)
        r = safe_get(u)
        if r and r.status_code == 200:
            found[p] = {"ok": True, "size": len(r.text)}
        else:
            found[p] = {"ok": False, "status_code": (r.status_code if r else None)}
    return {"robots_sitemap": found}

def get_cert_info(hostname):
    try:
        port = 443
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, port))
            cert_der = s.getpeercert(True)
        cert = x509.load_der_x509_certificate(cert_der, default_backend())
        subj = cert.subject.rfc4514_string()
        issuer = cert.issuer.rfc4514_string()
        not_before = cert.not_valid_before.isoformat()
        not_after = cert.not_valid_after.isoformat()
        san = []
        try:
            ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            san = ext.value.get_values_for_type(x509.DNSName)
        except Exception:
            san = []
        return {"subject": subj, "issuer": issuer, "valid_from": not_before, "valid_to": not_after, "san": san}
    except Exception as e:
        return {"error": str(e)}

def quick_scan(raw_url):
    """
    Главная функция — принимает URL, возвращает dict с результатами.
    """
    base = norm_url(raw_url)
    parsed = urlparse(base)
    host = parsed.hostname
    data = {"url": base}

    # Заголовки
    data.update(check_headers(base))

    # Общие пути
    data.update(check_common_paths(base))

    # XSS
    data.update(simple_xss_check(base))

    # robots & sitemap
    data.update(check_robots_sitemap(base))

    # TLS cert
    data["cert"] = get_cert_info(host) if host else {"error": "no_hostname"}

    return data
