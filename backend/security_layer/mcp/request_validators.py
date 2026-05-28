from __future__ import annotations
import re
from urllib.parse import urlparse

SECRET_PAT=re.compile(r"(api[_-]?key|token|password|secret|-----BEGIN PRIVATE KEY-----)",re.I)

def detect_mcp_path_traversal(value:str)->bool: return ".." in value or value.startswith("/")
def detect_mcp_ssrf_url(value:str)->bool:
    h=(urlparse(value).hostname or "").lower()
    return h in {"localhost","169.254.169.254"} or h.startswith("127.") or h.startswith("10.") or h.startswith("192.168.")
def detect_mcp_command_injection(value:str)->bool: return any(x in value for x in [";","&&","||","`","$("])
def detect_mcp_secret_pattern(value:str)->bool: return bool(SECRET_PAT.search(value))
def detect_mcp_prompt_injection_marker(value:str)->bool: return "ignore previous" in value.lower() or "system prompt" in value.lower()

def validate_mcp_argument_types(arguments:dict[str,object]):
    bad=[k for k,v in arguments.items() if not isinstance(v,(str,int,float,bool,list,dict,type(None)))]
    return (not bad,bad)
def validate_mcp_argument_lengths(arguments):
    bad=[k for k,v in arguments.items() if isinstance(v,str) and len(v)>2000]
    return (not bad,bad)
def validate_forbidden_mcp_argument_names(arguments):
    bad=[k for k in arguments if k.lower() in {"password","token","api_key","secret"}]
    return (not bad,bad)
def validate_no_secret_mcp_argument_values(arguments):
    bad=[k for k,v in arguments.items() if isinstance(v,str) and detect_mcp_secret_pattern(v)]
    return (not bad,bad)
def validate_mcp_file_path_argument(value:str): return (not detect_mcp_path_traversal(value),"unsafe_path" if detect_mcp_path_traversal(value) else "ok")
def validate_mcp_url_argument(value:str): return (not detect_mcp_ssrf_url(value),"unsafe_url" if detect_mcp_ssrf_url(value) else "ok")
def validate_mcp_domain_argument(value:str,allowed_domains=None,denied_domains=None):
    d=value.lower();
    if denied_domains and d in denied_domains: return False,"denied_domain"
    if allowed_domains and d not in allowed_domains: return False,"not_allowed_domain"
    return True,"ok"
def validate_mcp_command_argument(value:str): return (not detect_mcp_command_injection(value),"unsafe_command" if detect_mcp_command_injection(value) else "ok")
def validate_mcp_sql_like_argument(value:str): return (not re.search(r"(drop|truncate|delete\s+from)",value,re.I),"unsafe_sql" if re.search(r"(drop|truncate|delete\s+from)",value,re.I) else "ok")
def validate_mcp_prompt_derived_argument(value:str): return (not detect_mcp_prompt_injection_marker(value),"prompt_injection_marker" if detect_mcp_prompt_injection_marker(value) else "ok")
def validate_mcp_resource_identifier(value:str): return (bool(re.match(r"^[a-zA-Z0-9_.:-]{3,128}$",value)),"invalid_resource_id")
def validate_mcp_prompt_identifier(value:str): return (bool(re.match(r"^[a-zA-Z0-9_.:-]{3,128}$",value)),"invalid_prompt_id")
def sanitize_mcp_request_arguments(arguments):
    o={}
    for k,v in arguments.items():
        if isinstance(v,str) and detect_mcp_secret_pattern(v): o[k]="[redacted]"
        else: o[k]=v
    return o

def validate_mcp_request_arguments(arguments):
    checks=[validate_mcp_argument_types(arguments),validate_mcp_argument_lengths(arguments),validate_forbidden_mcp_argument_names(arguments),validate_no_secret_mcp_argument_values(arguments)]
    unsafe=[]
    for k,v in arguments.items():
        if isinstance(v,str) and (detect_mcp_path_traversal(v) or detect_mcp_ssrf_url(v) or detect_mcp_command_injection(v)): unsafe.append(k)
    ok=all(c[0] for c in checks) and not unsafe
    return {"allowed":ok,"unsafe_keys":unsafe,"errors":[c[1] for c in checks if not c[0]],"sanitized":sanitize_mcp_request_arguments(arguments)}
