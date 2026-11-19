import csv
import io
import urllib.request
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import os
host = os.environ.get("PUBLIC_HOST", "localhost")
app = FastMCP("Koudou", host="0.0.0.0", port=int(os.environ.get("PORT","8000")), stateless_http=True, json_response=True, transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=[host,host+":*"],allowed_origins=["https://"+host]))
url="https://docs.google.com/spreadsheets/d/1ZdjnZB2ftEtazU4DUm_jtW0DiqTKJ-tqE_Jy2nkgFcE/export?format=csv"
@app.tool()
def rechercher_terme_scout(terme: str, langue_source: str = "fr") -> list[dict]:
    """Cherche un terme scout FR ou NL dans le lexique de la Route."""
    term=terme.strip().casefold()
    if not term or len(term)>100 or langue_source not in ("fr","nl"):
        raise ValueError("Fournir un terme de 1 à 100 caractères et la langue fr ou nl.")
    with urllib.request.urlopen(url,timeout=10) as response:
        if "html" in response.headers.get("Content-Type",""):
            raise ValueError("Lexique Google indisponible.")
        rows=csv.reader(io.StringIO(response.read().decode("utf-8-sig")))
        matches=[]
        for row in rows:
            if len(row)==1: row=row[0].split(":",1)
            if len(row)<2: continue
            fr,nl=(s.strip() for s in row[:2])
            if fr and nl and term in (fr if langue_source=="fr" else nl).casefold():
                matches.append({"fr":fr,"nl":nl})
        return matches[:30]
if __name__=="__main__":
    app.run(transport="streamable-http")
