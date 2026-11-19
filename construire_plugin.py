import sys,json,zipfile
from pathlib import Path
from urllib.parse import urlsplit
site,mcp=sys.argv[1:]
assert all(urlsplit(u).scheme=="https" and urlsplit(u).hostname for u in [site,mcp])
site=site.rstrip("/")
root=Path(__file__).resolve().parent/"plugin"
manifest=json.loads((root/".codex-plugin/plugin.json").read_text())
manifest["version"]="0.4.0"
manifest["mcpServers"]="./.mcp.json"
manifest["interface"].update(websiteURL=site+"/",supportURL=site+"/support.html",privacyPolicyURL=site+"/confidentialite.html",termsOfServiceURL=site+"/conditions.html")
with zipfile.ZipFile("Koudou-0.4.0.zip","w",zipfile.ZIP_DEFLATED) as z:
    for f in root.rglob("*"):
        if not f.is_file():continue
        name=f.relative_to(root).as_posix()
        if name==".codex-plugin/plugin.json":z.writestr(name,json.dumps(manifest,ensure_ascii=False))
        elif name.endswith("SKILL.md"):z.writestr(name,f.read_text()+"\nPour vérifier une équivalence, appelle rechercher_terme_scout avec le terme seul et sa langue source.\n")
        else:z.write(f,name)
    z.writestr(".mcp.json",json.dumps({"mcpServers":{"koudou":{"url":mcp}}}))
