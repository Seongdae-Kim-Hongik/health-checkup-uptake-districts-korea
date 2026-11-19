import os, re, sys, datetime, subprocess
from docx import Document
from docx.shared import Pt, Cm
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import content_scrn as C
from build_manuscript_base_scrn import ZENODO, GITHUB, ADDRESS
OUT = os.path.join(os.path.dirname(HERE), "out"); N = C.N
W = dict(l.split("=") for l in open(os.path.join(OUT, "wordcount.txt")).read().split())
assert ZENODO.startswith("10.5281/zenodo.")
_d = datetime.date.today(); cl = [f"{_d.day} {_d:%B} {_d.year}", "Professor Nicholas Wald", "Editor-in-Chief, Journal of Medical Screening", "",
      "Dear Professor Wald,",
      f"Please find enclosed the manuscript entitled \"{C.TITLE}\" by Seongdae Kim, for consideration as an Original Article in the Journal of Medical Screening.",
      f"Korea's general health check-up invites tens of millions of eligible adults each year, and who attends shapes both its equity and the interpretation of its results. This study follows first-stage uptake among eligible persons in all {N['n_districts']} districts of the Republic of Korea over 2011–2024 ({N['scr_total_m']:.1f} million attendances among {N['elig_total_m']:.1f} million eligible persons summed over years), using the eligible population as the denominator, sex-standardised expected uptake and Bayesian spatio-temporal binomial models. "
      "District differences were small but persistent, with clusters of lower uptake in Seoul and higher uptake in industrial cities. Districts with more older adults living alone had lower uptake in most, but not all, models, and physical activity indicators showed no consistent association.",
      "The paper suits the journal because it examines where an organised national screening programme reaches fewer of its eligible population, separates persistent district differences from changes in eligibility and the pandemic, and reports all space-time and spatial-confounding checks regardless of their results. "
      "The study used only published aggregate statistics; the Institutional Review Board of Hongik University approved it (7002340-202511-HR-012) and its continuing review (7002340-202611-HR-040). The manuscript is original, has not been published, is not under consideration elsewhere, and the sole author has seen and approved it. Fast-track publication is not requested.",
      f"The main text contains {int(W['main']):,} words (limit 4,000), with a structured abstract of {int(W['abstract'])} words, 2 tables, 2 figures and {W['refs']} references. Supplementary material and the completed STROBE checklist are provided. The analysis code is openly available on GitHub ({GITHUB}) and archived on Zenodo (https://doi.org/{ZENODO}).",
      "No third-party writing assistance was received. The author used Claude (Anthropic) and ChatGPT (OpenAI) only for translation and English-language editing of the manuscript, reviewed and edited all output, and takes full responsibility for the content.",
      "Thank you for considering this manuscript.", "", "Yours sincerely,", "",
      "Seongdae Kim, PhD (corresponding author)", ADDRESS, "Email: kimsd@hongik.ac.kr"]
d = Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11); st.paragraph_format.space_after = Pt(4); st.paragraph_format.line_spacing = 1.0
for s in d.sections: s.page_width, s.page_height = Cm(21), Cm(29.7); s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.54)
gap = False
for t in cl:
    if t == "": gap = True; continue
    p = d.add_paragraph(t)
    if gap: p.paragraph_format.space_before = Pt(10); gap = False
d.core_properties.author = "Seongdae Kim"; d.core_properties.last_modified_by = "Seongdae Kim"; d.core_properties.title = "Cover Letter"; d.core_properties.comments = ""
fp = os.path.join(OUT, "Cover_letter.docx"); d.save(fp)
subprocess.run(["/opt/homebrew/bin/soffice", "--headless", "-env:UserInstallation=file:///tmp/lo_scrn_cl", "--convert-to", "pdf", "--outdir", OUT, fp], capture_output=True)
txt = subprocess.run(["pdftotext", fp.replace(".docx", ".pdf"), "-"], capture_output=True, text=True).stdout
assert not re.search(r"\b(we|our|us|I)\b", txt) and "—" not in txt and re.search(r"7002340-?\s*202611-?\s*HR-040", txt) and not re.search(r"(?i)funding|competing|overlap|previously submitted|token|private link", txt), "문체·IRB·금지 항목"
pages = subprocess.run(["pdfinfo", fp.replace(".docx", ".pdf")], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0]
assert pages == "1", pages; print("cover pages", pages)
