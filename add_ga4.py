import glob, re

MEASUREMENT_ID = "G-PENH0Z4VT7"

GA_SNIPPET = """  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={mid}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{mid}');
  </script>""".format(mid=MEASUREMENT_ID)

files = glob.glob("*.html")
ok, skip, already = 0, 0, 0

for f in files:
    with open(f, encoding="utf-8") as fh:
        content = fh.read()

    if MEASUREMENT_ID in content:
        already += 1
        continue

    if not re.search(r'<html', content, re.IGNORECASE):
        skip += 1
        continue

    if "</head>" not in content:
        skip += 1
        continue

    new_content = content.replace("</head>", GA_SNIPPET + "\n</head>", 1)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(new_content)
    ok += 1
    print(f"OK: {f}")

print(f"\n追加: {ok}件 / スキップ: {skip}件 / 既存: {already}件")
