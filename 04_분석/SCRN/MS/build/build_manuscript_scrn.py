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
TITLE = C.TITLE; assert TITLE == "Persistent small-area gaps in uptake of Korea's organised health check-up among eligible adults, 2011–2024"
assert ":" not in TITLE and "229" not in TITLE and "standardi" not in TITLE.lower()

# 본문 수정: 빠진 문헌 인용 정리(문장 의미 유지), 익명화, 국제적 의의
SUB = [
 ("[@kim2017first; @kang2017current; @eom2017effectiveness]", "[@kang2017current]"),
 ("[@kang2014factors; @hahm2017why; @luu2023socioeconomic]", "[@kang2014factors; @luu2023socioeconomic]"),
 ("participation in cancer screening [@kim2016impact; @shim2019employment]", "participation in cancer screening [@shim2019employment]"),
 (" [@yamaguchi2018sociodemographic], non-attendance there predicts later loss of independence [@igarashi2019nonparticipation], and", " [@yamaguchi2018sociodemographic], and"),
 ("fell from 2019 to 2020 [@kim2026impact], as did participation in cancer screening [@park2022impact].", "fell from 2019 to 2020 [@kim2026impact]."),
 ("nor ask whether physical activity, which may cluster with other health-seeking behaviours [@tabuchi2015determinants], is associated with attendance.", "nor ask whether district physical activity is associated with attendance."),
 ("[@besag1991bayesian; @riebler2016intuitive]", "[@riebler2016intuitive]"),
 ("and penalised complexity priors [@simpson2017penalising], fitted", "and penalised complexity priors (standard deviations above 0.5 with probability 0.01; mixing parameter below 0.5 with probability 2/3), fitted"),
 (" in R 4.6.0 [@web:rcore2026].", " in R 4.6.0."),
 ("always with the 5 adjustments [@steegen2016increasing].", "always with the 5 adjustments."),
 (" [@sedani2025social], and non-attendance at check-ups has predicted later dependency [@igarashi2019nonparticipation].", " [@sedani2025social]."),
 ("which mixes eligibility and uptake and is not an age standardisation of eligible persons. Fifth,", "which mixes eligibility and uptake and is not an age standardisation of eligible persons; in 2 of 3,206 district-years this expected uptake exceeded 0.98 (maximum 1.02) and was capped at 0.98, the same bound used at both ends, so that its logit was defined. Fifth,"),
 ("The Institutional Review Board of Hongik University approved the study (7002340-202511-HR-012; continuing review 7002340-202611-HR-040) and waived informed consent because only published aggregate statistics were used.",
  "The institutional review board of the author's institution approved the study and its continuing review and waived informed consent because only published aggregate statistics were used (details on the title page)."),
]
def fix(t):
    for a, b in SUB: t = t.replace(a, b)
    return t
INTL = ("The findings bear on health systems that monitor organised check-up or screening programmes by area. Persistent geographical variation in organised screening uptake has also been reported in Taiwan [@chiou2014changes], and the clinical value of general health checks remains debated [@liss2021general]. "
        "In this study, uptake was recorded programme attendance divided by the eligible population. If some eligible adults use private check-ups instead of programme check-ups, programme records alone would not capture all check-up use; this possibility was not tested here. "
        "Data linkage or surveys covering both programme and private check-ups could help to assess unmet preventive need before programme uptake is used to prioritise outreach between areas.")
ABSTRACT = [
 ("Objectives", "Small-area studies of Korea's national general health check-up have covered at most 2 years. This study followed uptake among eligible adults in every district over 14 years to describe where it was persistently lower or higher than expected and which district characteristics were associated with it."),
 ("Methods", f"Ecological panel study of annual district counts of first-stage attendees and eligible persons (270.6 million eligible person-years) in all {N['n_districts']} districts of the Republic of Korea, 2011–2024. Expected numbers of attendees were calculated from sex-specific national uptake. Bayesian spatio-temporal binomial models related uptake to 12 district characteristics and 5 adjustment variables, with covariate-subset, Knorr-Held space-time and spatial-confounding checks."),
 ("Results", f"National uptake was {U['2011']}% in 2011, {U['2017']}% in 2017, {U['2020']}% in 2020 and {U['2024']}% in 2024. The 10th and 90th percentiles of district standardised uptake ratios were {N['sur_p10']:.2f} and {N['sur_p90']:.2f}, and district rankings persisted over time (Kendall's W {N['kendall_w']:.2f}). The lowest ratios were in remote counties such as Ulleung and Wando and in some Seoul districts; 10 of the {N['gi_cold']} local cold spots were in Seoul, whereas industrial areas such as Ulsan and Geoje had high ratios. Uptake was lower where more older adults lived alone (odds ratio per 1 SD increase 0.933, 95% credible interval 0.912–0.954); the association was retained in space-time and spatial-confounding models, but its interval included 1 with an intrinsic autoregressive district effect alone and in 2019–2024 alone. Physical activity associations were not consistent across space-time models."),
 ("Conclusions", "Uptake of the organised check-up differed modestly but persistently between districts, with local clusters of lower uptake in Seoul. Private check-ups were not measured, so lower programme uptake in some districts may reflect use of other check-up services rather than unmet need. The association with older adults living alone was model-dependent, and residual spatial autocorrelation remained."),
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
