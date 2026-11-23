"""楽天GORA 各コースの先頭4プランの説明から海外の方向けの条件を拾う (2026-11-23)。Usage: python scripts/scan_foreign_conditions.py <出力ディレクトリ>"""
import json, re, sys, time, subprocess, os
sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0"
KW = re.compile(r"海外|外国|日本語|渡航|訪日|インバウンド|国外|英語")
def get(url, path):
    if not os.path.exists(path) or os.path.getsize(path) < 2000:
        subprocess.run(["curl", "-sL", "-A", UA, "-o", path, url]); time.sleep(1.0)
    b = open(path, "rb").read()
    return b.decode("euc_jp", "replace")
d = json.load(open("C:/Users/Owner/fukuoka-golf-guide/rakuten_gora_mapping.json", encoding="utf-8"))["courses"]
res = {}
for c in d:
    cid = c.get("c_id")
    if not cid: continue
    t = get(f"https://search.gora.golf.rakuten.co.jp/cal/disp/c_id/{cid}/", f"{OUT}/cal_{cid}.html")
    plans = []
    for pid, body in re.findall(r'<tr id="(\d+)"[^>]*\bfee="\d+"[^>]*>(.*?)</tr>', t, re.S):
        nm = re.search(r'class="planName[^"]*"[^>]*>(.*?)</td>', body, re.S)
        nm = re.sub(r"<[^>]+>|\s+", "", nm.group(1)) if nm else ""
        if nm not in [p[1] for p in plans]: plans.append((pid, nm))
    hits = set()
    for pid, nm in plans[:4]:
        s = get(f"https://search.gora.golf.rakuten.co.jp//?menu=compe&act=detail&plan_id={pid}", f"{OUT}/plan_{pid}.html")
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))
        for m in KW.finditer(txt):
            hits.add(txt[max(0, m.start()-60):m.end()+60])
    res[c["file"]] = dict(cid=cid, nplans=len(plans), hits=sorted(hits))
    print(c["file"], cid, len(plans), len(hits), flush=True)
json.dump(res, open(f"{OUT}/rakuten_foreign.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
