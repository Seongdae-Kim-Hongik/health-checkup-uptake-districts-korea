# build_manuscript_scrn.py — 65호 SCRN 원고 조립(익명 본문 + 제목면): 본문 ≤3,500단어, 참고문헌 ≤30, 구조 초록 ≤300, 키워드 3개, Vancouver 번호 인용.
import os, re, json, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import content_scrn as C
import build_manuscript_base_scrn as J0
from build_manuscript_base_scrn import TX, put_table, table1, table2, ORCID, AFFIL, ADDRESS, PHONE, ETHICS, AI_USE, CREDIT, COI, FUNDING, FIGCAP
MS = os.path.dirname(HERE); OUT = os.environ.get("MS_OUT", os.path.join(MS, "out_ms")); os.makedirs(OUT, exist_ok=True)
N = C.N; U = C.U; m = C.m
ZENODO = os.environ.get("ZENODO_DOI", "[ZENODO DOI]"); GITHUB = os.environ.get("GITHUB_URL", "[GITHUB URL]")
REFS = json.load(open(os.path.join(HERE, "refs_scrn.json"), encoding="utf-8"))
DROP = ["kim2017first", "eom2017effectiveness", "kim2016impact", "hahm2017why", "park2022impact", "tabuchi2015determinants", "igarashi2019nonparticipation",
        "web:rcore2026", "besag1991bayesian", "simpson2017penalising", "steegen2016increasing"]   # 참고문헌 ≤30 규정
REFS = {k: v for k, v in REFS.items() if k not in DROP}
TITLE = C.TITLE; assert TITLE == "Does organised health screening reach affluent districts? Fourteen years of eligible-population uptake of Korea's national health check-up"
assert ":" not in TITLE and "229" not in TITLE and "standardi" not in TITLE.lower()

# 본문 수정: 빠진 문헌 인용 정리(문장 의미 유지), 익명화, 국제적 의의
SUB = [
 ("[@kim2017first; @kang2017current; @eom2017effectiveness]", "[@kang2017current]"),
 ("[@kang2014factors; @hahm2017why; @luu2023socioeconomic]", "[@kang2014factors; @luu2023socioeconomic]"),
 ("participation in cancer screening [@kim2016impact; @shim2019employment]", "participation in cancer screening [@shim2019employment]"),
 (" [@yamaguchi2018sociodemographic], non-attendance there predicts later loss of independence [@igarashi2019nonparticipation], and", " [@yamaguchi2018sociodemographic], and"),
 ("fell from 2019 to 2020 [@kim2026impact], as did participation in cancer screening [@park2022impact].", "fell from 2019 to 2020 [@kim2026impact]."),
 ("nor ask whether physical activity, which may cluster with other health-seeking behaviours [@tabuchi2015determinants], is associated with attendance.", "nor ask whether physical activity, which may cluster with other health-seeking behaviours, is associated with attendance."),
 ("[@besag1991bayesian; @riebler2016intuitive]", "[@riebler2016intuitive]"),
 ("and penalised complexity priors [@simpson2017penalising], fitted", "and penalised complexity priors, fitted"),
 (" in R 4.6.0 [@web:rcore2026].", " in R 4.6.0."),
 ("always with the 5 adjustments [@steegen2016increasing].", "always with the 5 adjustments, as a multiverse analysis."),
 (" [@sedani2025social], and non-attendance at check-ups has predicted later dependency [@igarashi2019nonparticipation].", " [@sedani2025social]."),
 ("which mixes eligibility and uptake and is not an age standardisation of eligible persons. Fifth,", "which mixes eligibility and uptake and is not an age standardisation of eligible persons; its expected uptake was truncated at 0.98 in 2 of 3,206 district-years, where it reached 1.02, so that the logit was defined. Fifth,"),
 ("The Institutional Review Board of Hongik University approved the study (7002340-202511-HR-012; continuing review 7002340-202611-HR-040) and waived informed consent because only published aggregate statistics were used.",
  "The institutional review board of the author's institution approved the study and its continuing review and waived informed consent because only published aggregate statistics were used (details on the title page)."),
]
def fix(t):
    for a, b in SUB: t = t.replace(a, b)
    return t
INTL = ("Beyond Korea, the findings bear on any health system that offers population health checks alongside private ones, as in Japan and Taiwan [@chiou2014changes], or that debates their value [@liss2021general]. "
        "Programme uptake measured against the eligible population is the usual indicator for national targets and for comparing areas, yet where adults with more resources substitute privately arranged checks, low recorded uptake may mark substitution rather than unmet need, "
        "and area targets based on programme records alone could direct outreach to the wrong places. Linking private and programme check-ups, or surveying both, would make small-area monitoring of preventive service use more useful for planning.")
ABSTRACT = [
 ("Objectives", "Small-area studies of Korea's national general health check-up have covered at most 2 years. This study followed uptake among eligible adults in every district over 14 years to describe where it was persistently lower than expected, including affluent districts where privately arranged check-ups are common, and which district characteristics were associated with it."),
 ("Methods", f"Ecological panel of first-stage attendees among {N['elig_total_m']:.1f} million eligible persons summed over years in all {N['n_districts']} districts of the Republic of Korea, 2011–2024. Expected attendees were standardised for sex. Bayesian spatio-temporal binomial models related uptake to 12 district characteristics and 5 adjustments, with covariate-subset, Knorr-Held space-time and spatial-confounding checks."),
 ("Results", f"National uptake was {U['2011']}% in 2011, {U['2017']}% in 2017, {U['2020']}% in 2020 and {U['2024']}% in 2024. District standardised uptake ratios ranged from {N['sur_p10']:.2f} to {N['sur_p90']:.2f} (10th–90th percentile), and rankings persisted over time. Ten of {N['gi_cold']} local cold spots were in Seoul, including the affluent Gangnam and central Jongno, whereas industrial cities such as Ulsan and Geoje had high ratios. Uptake was lower where more older adults lived alone (odds ratio per 1 SD {m('alone_elderly', lab=False)}, 95% credible interval), an association retained in space-time and spatial-confounding models but not with an intrinsic autoregressive district effect alone or in 2019–2024 alone. Physical activity indicators showed no consistent association."),
 ("Conclusions", "Organised check-up uptake differed modestly but persistently between districts, with clusters of lower uptake in affluent Seoul districts, where unrecorded private check-ups may substitute for the programme. Monitoring that counts only programme attendance may misdirect outreach; the association with older adults living alone was model-dependent."),
]
KEYWORDS = "Preventive health services; Health check-up uptake; Small-area variation"
def para_set():
    intro = [fix(p) for p in C.INTRO]
    meth = [(x[0],) + tuple(fix(p) for p in x[1:]) for x in C.METHODS]
    res = [(x[0],) + tuple(fix(p) for p in x[1:]) for x in C.RESULTS]
    disc = []
    for p in C.DISCUSSION:
        if p == "### Strengths and limitations": disc += ["### Implications for health services and policy", INTL]
        disc.append(fix(p))
    return intro, meth, res, disc
def build(counts=None):
    J = TX(cite="sup"); c = counts or {}
    intro, meth, res, disc = para_set()
    J.para(f"<b>{TITLE}</b>")
    J.page_break(); J.head("Abstract", 1)
    for h, t in ABSTRACT: J.para(f"<b>{h}:</b> {t}")
    J.para(f"<b>Keywords:</b> {KEYWORDS}", before=6)
    J.page_break(); J.counting = True
    J.head("Introduction", 1)
    for p in intro: J.para(J0.pandoc_cites(p), indent=True)
    J.head("Methods", 1)
    for x in meth:
        J.head(x[0], 2)
        for p in x[1:]: J.para(J0.pandoc_cites(p), indent=True)
    J.head("Results", 1)
    for x in res:
        J.head(x[0], 2)
        for p in x[1:]: J.para(J0.pandoc_cites(p), indent=True)
    J.head("Discussion", 1)
    for p in disc:
        if p.startswith("### "): h = p[4:].strip(); J.head(h, 1 if h == "Conclusions" else 2); continue
        J.para(J0.pandoc_cites(p), indent=True)
    J.counting = False
    J.head("Use of artificial intelligence", 1); J.para(AI_USE)
    unused = set(REFS) - set(J.cites); assert not unused, unused
    miss = set(J.cites) - set(REFS); assert not miss, miss
    J.page_break(); J.head("References", 1); J.raw = True; rl = []
    for i, k in enumerate(J.cites, 1):
        J0.REFS = REFS; s = f"{i}. " + J0.ref(k); rl.append(s); J.para(s)
    J.raw = False
    J.page_break(); put_table(J, table1())
    J.new_page("landscape"); put_table(J, table2(), fs=8)
    J.new_page("portrait"); J.head("Figure legends", 1)
    for k in sorted(FIGCAP): J.para(f"<b>Figure {k}.</b> {FIGCAP[k]}", after=6)
    return J, rl
def title_page(c):
    J = TX(cite="sup")
    J.para(f"<b>{TITLE}</b>")
    J.para("Seongdae Kim, PhD", before=6); J.para(AFFIL)
    J.para(f"<b>Corresponding author:</b> Seongdae Kim, PhD, {ADDRESS}. Telephone: {PHONE}. Email: kimsd@hongik.ac.kr. ORCID: {ORCID}", before=6)
    J.para(f"<b>Word count:</b> main text, {c['main']} words; abstract, {c['abstract']} words; tables, 2; figures, 2; references, {c['refs']}.", before=6)
    for h, t in [("Acknowledgements", "None."), ("Author contributions", CREDIT), ("Declaration of conflicting interests", COI), ("Funding", FUNDING),
                 ("Ethical approval and informed consent", ETHICS), ("Data availability", "All source data are publicly available aggregate statistics from the National Health Insurance Service, resident registration and the Korea Community Health Survey, accessed through the Korean Statistical Information Service. The processed district-year data are available from the author on reasonable request."),
                 ("Code availability", f"The analysis code that generates every number, table and figure is openly available on GitHub ({GITHUB}) and archived on Zenodo (https://doi.org/{ZENODO})."),
                 ("Use of artificial intelligence", AI_USE)]:
        J.head(h, 2); J.para(t)
    return J
def main_words(path):
    t = J0.docx_text(path); i = t.find("\nIntroduction\n"); j = t.find("\nUse of artificial intelligence\n"); return len(t[i:j].split())
def pdf(p, tag):
    subprocess.run(["/opt/homebrew/bin/soffice", "--headless", f"-env:UserInstallation=file:///tmp/lo_scrn_{tag}", "--convert-to", "pdf", "--outdir", OUT, p], check=True, capture_output=True)
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", p.replace(".docx", ".pdf")], capture_output=True, text=True).stdout).group(1))
if __name__ == "__main__":
    _all = "\n".join(C.INTRO + [q for x in C.METHODS for q in x[1:]] + [q for x in C.RESULTS for q in x[1:]] + C.DISCUSSION); assert all(a in _all for a, _ in SUB), "SUB 불일치"
    p = os.path.join(OUT, "Manuscript_anonymised.docx"); aw = sum(len(t.split()) + 1 for _, t in ABSTRACT)   # 소제목 포함
    J, rl = build(); J.doc_title = "Manuscript"; J.save(p)
    mw = main_words(p); nref = len(rl)
    T = title_page({"main": f"{mw:,}", "abstract": aw, "refs": nref}); T.doc_title = "Title page"; pt = os.path.join(OUT, "Title_page.docx"); T.save(pt)
    npg = pdf(p, "ms"); pdf(pt, "tp")
    txt = J0.docx_text(p)
    assert not re.search(r"(?i)hongik|seongdae|kimsd|7002340|orcid|github|zenodo|0000-0002", txt), "익명화 실패"
    assert mw <= 3500 and aw <= 300 and nref <= 30 and len(KEYWORDS.split(";")) == 3, (mw, aw, nref)
    open(os.path.join(OUT, "reference_list.txt"), "w", encoding="utf-8").write("\n".join(rl))
    open(os.path.join(OUT, "wordcount.txt"), "w").write(f"main={mw}\nabstract={aw}\nrefs={nref}\npages={npg}\n")
    print(f"[build] main {mw} (≤3500) · abstract {aw} (≤300) · keywords 3 · refs {nref} (≤30) · pages {npg}")
