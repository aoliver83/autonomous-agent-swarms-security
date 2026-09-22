"""
HackerDummy Benchmark Catalog (AAS-Sec Integration)
Indexes deliberately vulnerable labs from borbollanetwork/HackerDummy.
Categorizes challenges by MITRE ATT&CK / OWASP, difficulty, flags, and expected finding keys.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HackerDummyLab(BaseModel):
    id: str
    lab_dir: str
    title: str
    category: str
    difficulty: str  # beginner, intermediate, advanced, expert
    owasp_tag: str
    mitre_atlas_tag: str
    description: str
    expected_vulnerabilities: List[str]
    target_flags: List[str] = Field(default_factory=list)
    simulated_ports: List[int] = Field(default_factory=lambda: [80, 8080])
    recommended_squad: List[str] = Field(default_factory=lambda: ["RED-ARGOS-02", "RED-VEKTOR-03", "RED-AEGIS-04"])


HACKERDUMMY_LABS: List[HackerDummyLab] = [
    HackerDummyLab(
        id="HD-01",
        lab_dir="01-vulnshop",
        title="VulnShop - E-Commerce SQLi & Broken Auth",
        category="Web Application / Injection",
        difficulty="beginner",
        owasp_tag="A03:2021-Injection",
        mitre_atlas_tag="AML.T0054",
        description="Classic vulnerable store containing union-based SQL injection, unauthenticated order manipulation, and admin password disclosure.",
        expected_vulnerabilities=["SQL Injection (Union-based)", "Broken Authentication", "IDOR in Orders"],
        target_flags=["FLAG{HD_SQLI_ADMIN_BYPASS_8392}"],
        simulated_ports=[3000, 80]
    ),
    HackerDummyLab(
        id="HD-02",
        lab_dir="02-vaultauth",
        title="VaultAuth - JWT Secret & Token Forgery",
        category="Identity & Access Management",
        difficulty="intermediate",
        owasp_tag="A07:2021-Identification & Auth Failures",
        mitre_atlas_tag="AML.T0057",
        description="Authentication service with weak HMAC-SHA256 secret keys, 'none' algorithm bypass, and privilege escalation to tenant admin.",
        expected_vulnerabilities=["JWT None Algorithm Vulnerability", "Weak HMAC Secret Brute-force", "Privilege Escalation"],
        target_flags=["FLAG{HD_JWT_TAMPER_ROOT_ACCESS_1948}"],
        simulated_ports=[8000]
    ),
    HackerDummyLab(
        id="HD-03",
        lab_dir="03-relaykit",
        title="RelayKit - SSRF to Cloud Metadata",
        category="Network & Cloud Infrastructure",
        difficulty="intermediate",
        owasp_tag="A10:2021-Server-Side Request Forgery",
        mitre_atlas_tag="AML.T0054",
        description="Webhook relay endpoint allowing internal IP traversal (169.254.169.254) and extraction of temporary IAM instance credentials.",
        expected_vulnerabilities=["Blind SSRF", "Cloud Metadata Extraction", "Internal Port Pivoting"],
        target_flags=["FLAG{HD_SSRF_AWS_METADATA_IAM_4021}"],
        simulated_ports=[8080]
    ),
    HackerDummyLab(
        id="HD-04",
        lab_dir="04-shopapi",
        title="ShopAPI - Mass Assignment & BOLA/IDOR",
        category="API Security",
        difficulty="beginner",
        owasp_tag="API1:2023-Broken Object Level Authorization",
        mitre_atlas_tag="AML.T0054",
        description="REST API exhibiting Mass Assignment allowing users to set 'is_admin=true' and direct ID access to private user records.",
        expected_vulnerabilities=["Mass Assignment", "BOLA / IDOR", "Information Disclosure"],
        target_flags=["FLAG{HD_API_MASS_ASSIGN_ESCALATION}"],
        simulated_ports=[5000]
    ),
    HackerDummyLab(
        id="HD-05",
        lab_dir="05-springvault",
        title="SpringVault - Spring Boot RCE / SpEL",
        category="Binary & Runtime Exploit",
        difficulty="advanced",
        owasp_tag="A03:2021-Injection",
        mitre_atlas_tag="AML.T0054",
        description="Spring Boot application vulnerable to SpEL (Spring Expression Language) injection leading to remote code execution and shell escape.",
        expected_vulnerabilities=["SpEL Remote Code Execution", "JVM Sandbox Escape", "Environment Variable Dumping"],
        target_flags=["FLAG{HD_SPEL_RCE_CONTAINER_POP_7721}"],
        simulated_ports=[8080]
    ),
    HackerDummyLab(
        id="HD-06",
        lab_dir="06-openservices",
        title="OpenServices - Insecure CORS & CSRF Chain",
        category="Client-Side & Cross-Origin",
        difficulty="intermediate",
        owasp_tag="A05:2021-Security Misconfiguration",
        mitre_atlas_tag="AML.T0057",
        description="Misconfigured CORS wildcard with credentials enabled allowing authenticated cross-origin data exfiltration.",
        expected_vulnerabilities=["CORS Misconfiguration", "Account Takeover via CSRF", "Token Leakage in Referrer"],
        target_flags=["FLAG{HD_CORS_EXFIL_AUTHENTICATED_3321}"],
        simulated_ports=[4000]
    ),
    HackerDummyLab(
        id="HD-07",
        lab_dir="07-graphvault",
        title="GraphVault - GraphQL Introspection & Batching",
        category="API Security",
        difficulty="intermediate",
        owasp_tag="API7:2023-Server Side Request Forgery & Misconfig",
        mitre_atlas_tag="AML.T0054",
        description="GraphQL endpoint with introspection enabled, nested query DoS vulnerability, and hidden mutation for credential dumping.",
        expected_vulnerabilities=["GraphQL Introspection Enabled", "Authorization Bypass in Mutations", "Batching Brute Force"],
        target_flags=["FLAG{HD_GQL_INTROSPECT_ADMIN_SECRET}"],
        simulated_ports=[4000]
    ),
    HackerDummyLab(
        id="HD-08",
        lab_dir="08-trustedge",
        title="TrustEdge - Hardcoded Certificates & Secrets",
        category="Secrets & Cryptography",
        difficulty="beginner",
        owasp_tag="A02:2021-Cryptographic Failures",
        mitre_atlas_tag="AML.T0057",
        description="TLS endpoint using hardcoded private keys in source and exposed `.env` files in git commit history.",
        expected_vulnerabilities=["Hardcoded Private RSA Keys", "Leaked Database Secrets", "Git Repository Exposure"],
        target_flags=["FLAG{HD_TRUFFLEHOG_HARDCODED_KEY_9921}"],
        simulated_ports=[8443, 80]
    ),
    HackerDummyLab(
        id="HD-09",
        lab_dir="09-injectarena",
        title="InjectArena - Multi-vector Command & SSTI",
        category="Web Application / Injection",
        difficulty="advanced",
        owasp_tag="A03:2021-Injection",
        mitre_atlas_tag="AML.T0054",
        description="Template rendering pipeline vulnerable to Jinja2/Mako SSTI and chained OS command execution via pipe filters.",
        expected_vulnerabilities=["Server-Side Template Injection (SSTI)", "OS Command Injection", "Filter Bypass"],
        target_flags=["FLAG{HD_SSTI_JINJA_REMOTE_EXEC_6631}"],
        simulated_ports=[5000]
    ),
    HackerDummyLab(
        id="HD-10",
        lab_dir="10-uploadforge",
        title="UploadForge - Unrestricted File Upload to RCE",
        category="File Handling & Execution",
        difficulty="intermediate",
        owasp_tag="A04:2021-Insecure Design",
        mitre_atlas_tag="AML.T0054",
        description="Profile picture upload vulnerable to extension blacklist bypass (.phar/.phtml), null-byte truncation, and web shell execution.",
        expected_vulnerabilities=["Unrestricted File Upload", "Web Shell RCE", "Directory Traversal in Filename"],
        target_flags=["FLAG{HD_UPLOAD_WEBSHELL_POPPED_5129}"],
        simulated_ports=[80]
    ),
    HackerDummyLab(
        id="HD-12",
        lab_dir="12-cloudpivot",
        title="CloudPivot - S3 Bucket Takeover & IAM Pivoting",
        category="Network & Cloud Infrastructure",
        difficulty="expert",
        owasp_tag="A05:2021-Security Misconfiguration",
        mitre_atlas_tag="AML.T0054",
        description="Exposed cloud storage bucket with write permissions, allowing lambda backdoor injection and lateral movement into the VPC.",
        expected_vulnerabilities=["Public S3 Bucket Write", "Lambda Function Poisoning", "Privilege Escalation via IAM Policy"],
        target_flags=["FLAG{HD_AWS_S3_LAMBDA_PIVOT_EXPERT_881}"],
        simulated_ports=[443, 9000]
    ),
    HackerDummyLab(
        id="HD-15",
        lab_dir="15-racevault",
        title="RaceVault - Concurrency & TOCTOU Race Condition",
        category="Business Logic & Concurrency",
        difficulty="advanced",
        owasp_tag="A04:2021-Insecure Design",
        mitre_atlas_tag="AML.T0054",
        description="Coupon redemption and wallet withdrawal flow vulnerable to async HTTP race conditions, allowing infinite balance duplication.",
        expected_vulnerabilities=["TOCTOU Race Condition", "Negative Balance Exploitation", "Double-spend in Transaction Bus"],
        target_flags=["FLAG{HD_RACE_CONDITION_DOUBLE_SPEND_1209}"],
        simulated_ports=[8000]
    ),
    HackerDummyLab(
        id="HD-18",
        lab_dir="18-javaforge",
        title="JavaForge - Java Object Insecure Deserialization",
        category="Binary & Runtime Exploit",
        difficulty="expert",
        owasp_tag="A08:2021-Software & Data Integrity Failures",
        mitre_atlas_tag="AML.T0054",
        description="Java RMI and serialized cookie endpoint vulnerable to Apache Commons-Collections gadget chains leading to blind RCE.",
        expected_vulnerabilities=["Insecure Deserialization (ysoserial)", "Gadget Chain RCE", "Out-of-band DNS Exfiltration"],
        target_flags=["FLAG{HD_JAVA_DESER_YSOSERIAL_GADGET_99}"],
        simulated_ports=[1099, 8080]
    ),
    HackerDummyLab(
        id="HD-20",
        lab_dir="20-graphforge",
        title="GraphForge - Neo4j Cypher Injection & Traversal",
        category="Web Application / Injection",
        difficulty="advanced",
        owasp_tag="A03:2021-Injection",
        mitre_atlas_tag="AML.T0054",
        description="Graph-backed social network engine vulnerable to Cypher injection (`LOAD CSV`, `CALL dbms.components()`), dumping internal graph edges.",
        expected_vulnerabilities=["Cypher Query Injection", "Neo4j Schema Dumping", "File Read via Cypher"],
        target_flags=["FLAG{HD_NEO4J_CYPHER_INJECT_MAP_771}"],
        simulated_ports=[7474, 7687]
    ),
    HackerDummyLab(
        id="HD-MOB-01",
        lab_dir="mobile/01-insecure-apk",
        title="MobileForge - Insecure Storage & SSL Pinning Bypass",
        category="Mobile Security",
        difficulty="intermediate",
        owasp_tag="M01:2024-Improper Credential Usage",
        mitre_atlas_tag="AML.T0057",
        description="Android APK with hardcoded API keys in SharedPreferences, disabled network security config, and bypassable Frida SSL pinning.",
        expected_vulnerabilities=["Hardcoded Secret in Dex", "Insecure SQLite Storage", "SSL Pinning Weakness"],
        target_flags=["FLAG{HD_ANDROID_DEX_EXTRACTED_KEY_44}"],
        simulated_ports=[]
    )
]


def get_lab_by_id(lab_id: str) -> Optional[HackerDummyLab]:
    for lab in HACKERDUMMY_LABS:
        if lab.id.lower() == lab_id.lower() or lab.lab_dir.lower() == lab_id.lower():
            return lab
    return None
