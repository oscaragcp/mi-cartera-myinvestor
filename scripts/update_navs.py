"""Descarga los valores liquidativos diarios (EUR) de Morningstar para los fondos de data/funds.json
y regenera data/navs.json. Lo ejecuta la acción de GitHub cada día laborable."""
import datetime as dt, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EPOCH = dt.date(2021, 1, 1)
URL = ("https://lt.morningstar.com/api/rest.svc/timeseries_price/9vehuxllxs?id={sec}%5D2%5D0%5DFOESP%24%24ALL"
       "&currencyId=EUR&idtype=Morningstar&frequency=daily&startDate={a}&endDate={b}&outputType=COMPACTJSON")

funds = json.loads((ROOT / "data/funds.json").read_text(encoding="utf-8"))
old = json.loads((ROOT / "data/navs.json").read_text(encoding="utf-8"))
today = dt.date.today().isoformat()
out = {"epoch": str(EPOCH), "generated": today, "funds": {}}
for isin, f in funds.items():
    req = urllib.request.Request(URL.format(sec=f["secid"], a=f["from"], b=f["to"] or today), headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=60))
    except Exception as e:  # si falla un fondo se conserva su histórico anterior
        print(f"{isin}: error {e}; se mantiene el histórico anterior")
        out["funds"][isin] = {**old["funds"].get(isin, {"secid": f["secid"], "nav": []}), "name": f["name"], "block": f["block"], "category": f.get("category", "")}
        continue
    pts = [[(dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).date() - EPOCH).days, v] for t, v in data]
    prev = old["funds"].get(isin, {}).get("nav", [])
    if len(pts) < len(prev):  # respuesta incompleta: no perder datos
        print(f"{isin}: respuesta más corta que la guardada; se mantiene la anterior")
        pts = prev
    out["funds"][isin] = {"name": f["name"], "block": f["block"], "category": f.get("category", ""), "secid": f["secid"], "nav": pts}
    print(isin, len(pts), pts[-1] if pts else None)
(ROOT / "data/navs.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
