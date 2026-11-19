#   그림 범례 'Fig. 1' 굵게·끝 구두점 없음, 보충 = 'Online Resource 1', 파일명 ESM_1.pdf·Fig1.tif. 게재료 없음(구독).
import os, re, json, subprocess, sys
from docx.shared import Pt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import content_scrn as C
import build_manuscript_base_scrn as J0
from build_manuscript_base_scrn import TX, put_table, table1, table2, ZENODO, GITHUB, ORCID, AFFIL, ADDRESS, ETHICS
MS = os.path.dirname(HERE); OUT = os.path.join(MS, "out_springer"); os.makedirs(OUT, exist_ok=True)
N = C.N; REFS = json.load(open(os.path.join(HERE, "refs_scrn_full.json"), encoding="utf-8"))
JN = {"suh2017impact": "The American Journal of Cardiology", "kang2017current": "Annals of Occupational and Environmental Medicine", "kim2017first": "Annals of Occupational and Environmental Medicine",
      "eom2017effectiveness": "Annals of Occupational and Environmental Medicine", "lee2026occupational": "Annals of Occupational and Environmental Medicine", "kim2023regional": "Environmental Health and Preventive Medicine",
      "kim2026impact": "Frontiers in Public Health", "hahm2017why": "Cancer Research and Treatment", "kim2016impact": "Cancer Research and Treatment", "kang2014factors": "Asian Pacific Journal of Cancer Prevention",
      "hart1971inverse": "Lancet", "vonelm2007strengthening": "Lancet", "liss2021general": "JAMA", "tabuchi2015determinants": "Cancer Science", "chiou2014changes": "Health Policy", "ko2016unmet": "Health Policy",
      "shim2019employment": "BMC Public Health", "yamaguchi2018sociodemographic": "BMC Public Health", "sedani2025social": "JAMA Network Open", "luu2023socioeconomic": "Epidemiology and Health",
      "park2022impact": "Epidemiology and Health", "igarashi2019nonparticipation": "Geriatrics & Gerontology International", "cheolseong2017data": "International Journal of Epidemiology",
      "inskip1983methods": "Statistics in Medicine", "knorrheld2000bayesian": "Statistics in Medicine", "kang2015korea": "Osong Public Health and Research Perspectives",
      "riebler2016intuitive": "Statistical Methods in Medical Research", "simpson2017penalising": "Statistical Science", "rue2009approximate": "Journal of the Royal Statistical Society: Series B (Statistical Methodology)",
      "steegen2016increasing": "Perspectives on Psychological Science", "dupont2022spatial": "Biometrics", "lipsitch2010negative": "Epidemiology", "bell2015explaining": "Political Science Research and Methods",
      "morgenstern1995ecologic": "Annual Review of Public Health", "besag1991bayesian": "Annals of the Institute of Statistical Mathematics", "ord1995local": "Geographical Analysis"}
FIXN = {"Cheol Seong S": "Seong, S. C.", "Heon Park J": "Park, J. H.", "Hyon Bang J": "Bang, J. H.", "Ae Shin S": "Shin, S. A.", "L Kim EA": "Kim, E. A."}
def apa_name(n):
    n = n.strip()
    if n in FIXN: return FIXN[n]
    m = re.match(r"^(.*?)\s+([A-Z]{1,4})$", n)
    if not m: return n
    return f"{m.group(1)}, " + " ".join(f"{c}." for c in m.group(2))
def ref(k):
    r = REFS[k]
    if r["type"] == "web": return f"{r['authors']}. ({r['year']}). {r['title']}. Retrieved {r['accessed']}, from {r['url']}"
    au = [apa_name(a) for a in r.get("authors_all") or r["authors"]]
    if len(au) > 20: au = au[:19] + ["…", au[-1]]
    a = au[0] if len(au) == 1 else (", ".join(au[:-1]) + ", & " + au[-1])
    t = r["title"].rstrip("."); t = t + ("" if t.endswith(("?", "!")) else ".")
    s = f"{a} ({r['year']}). {t} <i>{JN[k]}</i>"
    if r.get("vol"): s += f", <i>{r['vol']}</i>" + (f"({r['issue']})" if r.get("issue") else "")
    pg = r.get("pages") or r.get("elocation", "")
    if pg and not pg.startswith(("10.", "doi")):
        if "-" in pg:
            a1, b1 = pg.split("-")[:2]
            if b1.isdigit() and a1.isdigit() and len(b1) < len(a1): b1 = a1[:len(a1) - len(b1)] + b1
            pg = f"{a1}–{b1}"
        s += f", {pg}"
    s += "."
    if r.get("doi"): s += f" https://doi.org/{r['doi']}"
    return s
def cites(t):
    return re.sub(r"\s*\[(@[^\]]+)\]", lambda m: " {{" + ",".join(k.strip().lstrip("@") for k in m.group(1).split(";")) + "}}", t)
def esm(t):   # 보충 명칭: Springer 'Online Resource'
    t = t.replace("Supplementary Tables S2–S5c", "Online Resource 1 (Tables S2–S5c)").replace("Supplementary Table S1", "Online Resource 1, Table S1")
    return t.replace("with the checklist provided as a supplementary file", "with the checklist provided as Online Resource 2")
ABS = (f"Uptake of national health check-ups among eligible adults varies between areas, but long-term small-area patterns are rarely described. This ecological panel study examined first-stage uptake of the National Health Insurance Service general health screening among eligible persons in all {N['n_districts']} districts of the Republic of Korea from 2011 to 2024 ({N['scr_total_m']:.1f} million attendances among {N['elig_total_m']:.1f} million eligible persons summed over years). "
       f"Expected attendees were standardised for sex, and Bayesian spatio-temporal binomial models related uptake to 12 district characteristics with 5 adjustments, followed by covariate-subset, space-time and spatial-confounding checks. "
       f"National uptake was {C.U['2011']}% in 2011, {C.U['2017']}% in 2017, {C.U['2020']}% in 2020 and {C.U['2024']}% in 2024. District standardised uptake ratios ranged from {N['sur_p10']:.2f} to {N['sur_p90']:.2f} (10th–90th percentile); 10 of {N['gi_cold']} local cold spots were in Seoul, and industrial cities such as Ulsan and Geoje had high ratios. "
       f"Uptake was lower where more older adults lived alone (odds ratio per 1 standard deviation {C.m('alone_elderly', lab=False)}), an association retained in space-time and spatial-confounding models but not with an intrinsic autoregressive district effect alone or in 2019–2024 alone. Physical activity indicators showed no consistent association. "
       "District differences in uptake were small but persistent. The association with older adults living alone was model-dependent and may identify districts for closer study rather than individuals for outreach.")
KEYWORDS = "Mass screening; Preventive health services; Healthcare disparities; Small-area analysis; Spatio-temporal analysis; Republic of Korea"
AI_M = "The author used Claude (Anthropic) and ChatGPT (OpenAI) only for translation and English-language editing of the manuscript, reviewed and edited all output, and takes full responsibility for the content."
def data_statement(): return ("All source data are publicly available aggregate statistics from the National Health Insurance Service, resident registration and the Korea Community Health Survey, accessed through the Korean Statistical Information Service. "
                             "The processed district-year data are available from the author on reasonable request.")
def code_statement(): return f"The analysis code that generates every number, table and figure is openly available on GitHub ({GITHUB}) and archived on Zenodo (https://doi.org/{ZENODO})."
FIGCAP = {1: J0.FIGCAP[1].rstrip("."), 2: J0.FIGCAP[2].rstrip(".")}
def build(counts=None):
    J = TX(cite="bracket"); c = counts or {}
    J.para(f"<b>{C.TITLE}</b>")
    J.para("Seongdae Kim", before=6); J.para(AFFIL)
    J.para(f"<b>Corresponding author:</b> Seongdae Kim, {ADDRESS}. Email: kimsd@hongik.ac.kr. ORCID: {ORCID}", before=6)
    J.para("<b>Acknowledgments:</b> None.", before=6)
    J.para(f"<b>Word count:</b> abstract, {c.get('abstract', '[A]')} words; main text, {c.get('main', '[M]')} words; tables, 2; figures, 2; references, {c.get('refs', '[R]')}.", before=6)
    J.page_break(); J.head("Abstract", 1); J.para(ABS)
    J.para(f"<b>Keywords:</b> {KEYWORDS}", before=6)
    J.page_break(); J.counting = True
    J.head("Introduction", 1)
    for p in C.INTRO: J.para(cites(esm(p)), indent=True)
    J.head("Methods", 1)
    for i, x in enumerate(C.METHODS):
        J.head(x[0], 2)
        for p in x[1:]:
            if p.startswith("The Institutional Review Board"): p = p + " " + AI_M
            J.para(cites(esm(p)), indent=True)
    J.head("Results", 1)
    for x in C.RESULTS:
        J.head(x[0], 2)
        for p in x[1:]: J.para(cites(esm(p)), indent=True)
    J.head("Discussion", 1)
    for p in C.DISCUSSION:
        if p.startswith("### "): h = p[4:].strip(); J.head(h, 1 if h == "Conclusions" else 2); continue
        J.para(cites(esm(p)), indent=True)
    J.counting = False
    J.head("Statements and Declarations", 1)
    for h, t in [("Funding", "No funding was received for conducting this study."), ("Competing interests", "The author has no relevant financial or non-financial interests to disclose."),
                 ("Ethics approval", ETHICS), ("Consent to participate", "Not applicable. Only published aggregate statistics were used, and the Institutional Review Board waived informed consent."),
                 ("Consent for publication", "Not applicable."), ("Data availability", data_statement()), ("Code availability", code_statement()),
                 ("Author contributions", "Seongdae Kim: conceptualization, data curation, formal analysis, methodology, software, visualization, writing – original draft, and writing – review and editing.")]:
        J.head(h, 2); J.para(t)
    unused = set(REFS) - set(J.cites); assert not unused, unused
    J.page_break(); J.head("References", 1); rl = []
    for i, k in enumerate(J.cites, 1): s = f"{i}. " + ref(k); rl.append(s); J.raw = True; J.para(s); J.raw = False
    J.page_break(); put_table(J, table1())
    J.new_page("landscape"); put_table(J, table2(), fs=8)
    J.new_page("portrait"); J.head("Figure captions", 1)
    for k in sorted(FIGCAP): J.para(f"<b>Fig. {k}</b> {FIGCAP[k]}", after=6)
    return J, rl
def main_words(path):
    t = J0.docx_text(path); i = t.find("\nIntroduction\n"); j = t.find("\nStatements and Declarations\n"); return len(t[i:j].split())
if __name__ == "__main__":
    p = os.path.join(OUT, "Manuscript.docx"); aw = len(ABS.split()); assert 150 <= aw <= 250, aw
    J, rl = build(); J.doc_title = "Manuscript"; J.save(p)
    for _ in range(2):
        mw = main_words(p); J, rl = build({"main": f"{mw:,}", "abstract": aw, "refs": len(rl)}); J.doc_title = "Manuscript"; J.save(p)
    subprocess.run(["/opt/homebrew/bin/soffice", "--headless", "-env:UserInstallation=file:///tmp/lo_scrn_springer", "--convert-to", "pdf", "--outdir", OUT, p], check=True, capture_output=True)
    npg = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", p.replace(".docx", ".pdf")], capture_output=True, text=True).stdout).group(1))
    open(os.path.join(OUT, "reference_list.txt"), "w", encoding="utf-8").write("\n".join(rl))
    open(os.path.join(OUT, "wordcount.txt"), "w").write(f"main={main_words(p)}\nabstract={aw}\nrefs={len(rl)}\npages={npg}\n")
    print(f"[build JCH] main {main_words(p)} · abstract {aw} (150–250) · keywords {len(KEYWORDS.split(';'))} · refs {len(rl)} · pages {npg}")
