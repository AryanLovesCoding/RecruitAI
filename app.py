import streamlit as st
import pdfplumber
import json
import re
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

st.set_page_config(
    page_title="RecruitAI — Smart Resume Screening",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body { background: #0a0a0a !important; color: #e8e8e8; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* NUCLEAR: nuke every Streamlit wrapper background — root cause of all black boxes */
.stApp, .main, .appview-container,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stColumn"],
.element-container,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stFileUploaderFileList"],
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] > section,
[data-testid="stFileUploaderDropzoneInstructions"] > div,
[data-testid="stFileUploaderFile"] > div,
[data-testid="stFileUploaderDeleteBtn"],
[data-testid="stFileUploaderDeleteBtn"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Button wrapper black box fix */
.stButton, .stButton > div, .stButton > div > div,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondaryFormSubmit"],
div:has(> [data-testid="stBaseButton-secondary"]),
div:has(> [data-testid="stBaseButton-primary"]) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── NAVBAR ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 6rem;
    border-bottom: 1px solid #1a1a1a;
    background: #0a0a0a !important;
    position: sticky; top: 0; z-index: 100;
}
.nav-logo { display: flex; align-items: center; gap: 0.75rem; }
.nav-logo-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; color: white; flex-shrink: 0;
}
.nav-logo-name { font-size: 1rem; font-weight: 700; line-height: 1.1; }
.nav-logo-name .plain { color: #fff; }
.nav-logo-name .grad {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.nav-logo-sub { font-size: 0.6rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #666; }
.nav-badge {
    display: flex; align-items: center; gap: 0.45rem;
    background: #111 !important; border: 1px solid #2a2a2a !important;
    border-radius: 99px; padding: 0.35rem 0.9rem;
    font-size: 0.75rem; font-weight: 500; color: #999;
}
.nav-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 6px #22c55e; flex-shrink:0; }

/* ── HERO ── */
.hero { text-align: center; padding: 4.5rem 2rem 3.5rem; max-width: 900px; margin: 0 auto; }
.hero-chip {
    display: inline-flex; align-items: center; gap: 0.55rem;
    background: #111 !important; border: 1px solid #2a2a2a !important;
    border-radius: 99px; padding: 0.45rem 1.2rem;
    font-size: 0.8rem; font-weight: 500; color: #999;
    margin-bottom: 2rem; transition: all 0.3s ease; cursor: default;
}
.hero-chip:hover { border-color: rgba(168,85,247,0.5) !important; color: #c084fc; box-shadow: 0 0 20px rgba(168,85,247,0.12); }
.hero-chip-icon {
    background: linear-gradient(135deg, #a855f7, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    font-size: 1rem;
}
.hero-title { font-size: clamp(2.8rem, 6vw, 4.4rem); font-weight: 800; line-height: 1.08; letter-spacing: -0.03em; color: #fff; margin-bottom: 1.4rem; }
.hero-title .grad { background: linear-gradient(90deg, #a855f7 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { font-size: 1rem; color: #999; line-height: 1.7; max-width: 560px; margin: 0 auto; }

/* ── MAIN WRAP ── */
.main-wrap { max-width: 1280px; margin: 0 auto; padding: 0 6rem 2rem; }

/* ── Input headers ── */
.input-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.75rem; }
.input-title { font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.15rem; }
.input-sub { font-size: 0.75rem; color: #999; }
.count-pill { background: #161616 !important; border: 1px solid #2a2a2a !important; border-radius: 99px; padding: 0.2rem 0.75rem; font-size: 0.72rem; font-weight: 500; color: #999; white-space: nowrap; flex-shrink: 0; }

/* ── Textarea ── */
.stTextArea textarea {
    background: #111 !important; border: 1px solid #2a2a2a !important;
    border-radius: 12px !important; color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
    line-height: 1.7 !important; padding: 1rem !important;
    min-height: 280px !important; box-shadow: none !important; resize: vertical !important;
}
.stTextArea textarea:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 2px rgba(124,58,237,0.12) !important; outline: none !important; }
.stTextArea textarea::placeholder { color: #444 !important; }
.stTextArea label { display: none !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] { background: #111 !important; border: 2px dashed #7c3aed !important; border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; padding: 2rem 1rem !important; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.6rem; }
[data-testid="stFileUploaderDropzone"] svg { display: none !important; }
[data-testid="stFileUploaderDropzone"]::before {
    content: "↑";
    display: flex; align-items: center; justify-content: center;
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    font-size: 1.4rem; color: white; font-weight: 700;
    margin-bottom: 0.4rem; box-shadow: 0 4px 20px rgba(124,58,237,0.4);
}
[data-testid="stFileUploaderDropzoneInstructions"] p { color: #bbb !important; font-size: 0.85rem !important; text-align: center; }
[data-testid="stFileUploaderDropzoneInstructions"] small { color: #999 !important; font-size: 0.75rem !important; }
[data-testid="stFileUploaderFileList"] { background: transparent !important; padding: 0 0.75rem 0.75rem !important; }
[data-testid="stFileUploaderFile"] { background: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 10px !important; padding: 0.65rem 1rem !important; margin-top: 0.5rem !important; box-shadow: none !important; }
[data-testid="stFileUploaderFileName"] { color: #e0e0e0 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
[data-testid="stFileUploaderFileData"] { color: #999 !important; font-size: 0.72rem !important; }
[data-testid="stFileUploaderDeleteBtn"] button { background: transparent !important; border: none !important; box-shadow: none !important; color: #666 !important; }
[data-testid="stFileUploaderDeleteBtn"] button:hover { color: #bbb !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%) !important;
    color: #fff !important; font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    border: none !important; border-radius: 99px !important;
    padding: 0.85rem 2.8rem !important; transition: all 0.2s ease !important;
    box-shadow: 0 4px 30px rgba(168,85,247,0.4) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 40px rgba(168,85,247,0.6) !important; filter: brightness(1.08) !important; }

/* ── RESULTS ── */
.results-badge { display: inline-flex; align-items: center; gap: 0.5rem; background: #161616 !important; border: 1px solid #2a2a2a !important; border-radius: 99px; padding: 0.3rem 0.85rem; font-size: 0.72rem; font-weight: 500; color: #aaa; margin-bottom: 0.8rem; }
.results-title { font-size: 1.9rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; margin-bottom: 0.25rem; }
.results-sub { font-size: 0.85rem; color: #999; margin-bottom: 1.8rem; }

/* ── CANDIDATE CARD ── */
.ccard { background: #111 !important; border: 1px solid #1e1e1e !important; border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; transition: border-color 0.2s, box-shadow 0.2s; animation: slideUp 0.4s ease both; }
.ccard:hover { border-color: #2a2a2a !important; box-shadow: 0 0 30px rgba(124,58,237,0.08); }
@keyframes slideUp { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }
.ccard-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; gap: 1rem; }
.ccard-left { display: flex; align-items: center; gap: 0.9rem; }
.rank-badge { width: 42px; height: 42px; background: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.82rem; font-weight: 700; color: #bbb; flex-shrink: 0; }
.rank-badge.top { background: rgba(124,58,237,0.15) !important; border-color: rgba(124,58,237,0.3) !important; color: #a855f7; }
.ccard-name { font-size: 1.15rem; font-weight: 700; color: #fff; }
.ccard-sub { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #777; margin-top: 0.15rem; }
.match-pill { display: inline-flex; align-items: center; gap: 0.35rem; border-radius: 99px; padding: 0.3rem 0.85rem; font-size: 0.78rem; font-weight: 600; white-space: nowrap; flex-shrink: 0; }
.match-high { background: rgba(34,197,94,0.1) !important; border: 1px solid rgba(34,197,94,0.3) !important; color: #4ade80; }
.match-mid  { background: rgba(234,179,8,0.1) !important; border: 1px solid rgba(234,179,8,0.3) !important; color: #facc15; }
.match-low  { background: rgba(239,68,68,0.1) !important; border: 1px solid rgba(239,68,68,0.3) !important; color: #f87171; }
.score-bar-bg { width:100%; height:4px; background:#1e1e1e; border-radius:99px; overflow:hidden; margin-bottom:1rem; }
.score-bar-fill { height:100%; border-radius:99px; }
.bar-high { background: linear-gradient(90deg,#16a34a,#4ade80); }
.bar-mid  { background: linear-gradient(90deg,#ca8a04,#facc15); }
.bar-low  { background: linear-gradient(90deg,#dc2626,#f87171); }
.ccard-summary { font-size: 0.88rem; color: #aaa; line-height: 1.7; margin-bottom: 1.2rem; }
.skills-grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.skills-label { font-size:0.62rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.6rem; }
.skills-label.str { color: #4ade80; }
.skills-label.gap { color: #fb923c; }
.skills-tags { display:flex; flex-wrap:wrap; gap:0.4rem; }
.skill-tag { display:inline-block; border-radius:6px; padding:0.28rem 0.75rem; font-size:0.76rem; font-weight:500; }
.skill-tag.str { background:rgba(74,222,128,0.1) !important; border:1px solid rgba(74,222,128,0.25) !important; color:#86efac; }
.skill-tag.gap { background:rgba(251,146,60,0.1) !important; border:1px solid rgba(251,146,60,0.25) !important; color:#fdba74; }

/* ── FOOTER ── */
.site-footer { text-align: center; padding: 2.5rem 2rem 3rem; border-top: 1px solid #1a1a1a; margin-top: 3rem; }
.footer-credit { font-size: 0.88rem; color: #999; margin-bottom: 1.6rem; }
.footer-credit span { background: linear-gradient(90deg, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; }
.footer-links-wrap { display: flex; justify-content: center; gap: 0.8rem; }
.footer-btn { display: inline-flex; align-items: center; gap: 0.55rem; border-radius: 10px; padding: 0.6rem 1.3rem; font-size: 0.82rem; font-weight: 600; text-decoration: none; transition: all 0.25s ease; cursor: pointer; }
.footer-btn-li { background: rgba(10,102,194,0.12) !important; border: 1px solid rgba(10,102,194,0.35) !important; color: #60a5fa; }
.footer-btn-li:hover { background: rgba(10,102,194,0.22) !important; border-color: rgba(10,102,194,0.6) !important; transform: translateY(-2px); box-shadow: 0 4px 20px rgba(10,102,194,0.2); color: #93c5fd; }
.footer-btn-web { background: linear-gradient(135deg, #7c3aed, #a855f7, #ec4899) !important; border: none !important; color: #fff; box-shadow: 0 4px 20px rgba(168,85,247,0.35); }
.footer-btn-web:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(168,85,247,0.55); filter: brightness(1.08); }

/* ── MISC ── */
.stSpinner > div { border-top-color: #a855f7 !important; }
.stAlert { border-radius: 10px !important; }
.btn-center { display: flex; justify-content: center; margin: 1.5rem 0 2rem; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────
def extract_pdf_text(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text.strip()


def score_class(score: int) -> str:
    if score >= 70: return "high"
    if score >= 40: return "mid"
    return "low"


def analyse_resumes(jd: str, resumes: list) -> list:
    client = Groq(api_key=GROQ_API_KEY)
    resume_block = ""
    for i, r in enumerate(resumes):
        resume_block += f"\n--- RESUME {i+1} (filename: {r['name']}) ---\n{r['text']}\n"

    prompt = f"""You are an expert technical recruiter. Analyse each resume against the job description and return a JSON array.

JOB DESCRIPTION:
{jd}

RESUMES:
{resume_block}

Return ONLY a valid JSON array, no markdown, no explanation. Each element:
{{
  "rank": <integer starting at 1, 1 = best fit>,
  "filename": "<exact filename>",
  "candidate_name": "<full name from resume or Unknown>",
  "score": <integer 0-100>,
  "strengths": ["<skill 1>", "<skill 2>", "<skill 3>"],
  "gaps": ["<gap 1>", "<gap 2>", "<gap 3>"],
  "summary": "<2-3 sentence honest assessment for this role>"
}}

Rules: rank 1 has highest score. Scores must be unique. Strengths and gaps must be SHORT skill/keyword labels (2-3 words max), not full sentences.
Return exactly {len(resumes)} objects."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```(?:json)?", "", raw).strip("`").strip()
    results = json.loads(raw)
    return sorted(results, key=lambda x: x["rank"])


# ── NAVBAR ───────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">
    <div class="nav-logo-icon">✦</div>
    <div>
      <div class="nav-logo-name"><span class="plain">Recruit</span><span class="grad">AI</span></div>
      <div class="nav-logo-sub">Smart Resume Screening</div>
    </div>
  </div>
  <div class="nav-badge">
    <span class="nav-dot"></span>
    Powered by Groq · Llama 3.3
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-chip">
    <span class="hero-chip-icon">✦</span>
    AI-powered candidate analysis
  </div>
  <div class="hero-title">
    Screen resumes at the <span class="grad">speed</span><br><span class="grad">of thought.</span>
  </div>
  <div class="hero-sub">
    Drop a job description, upload candidate PDFs, and get a ranked shortlist with<br>strengths, gaps, and a match score — in seconds.
  </div>
</div>
""", unsafe_allow_html=True)

if not GROQ_API_KEY:
    st.error("⚠️ No API key found. Add GROQ_API_KEY to your .env file and restart.")
    st.stop()

# ── INPUTS ───────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    char_placeholder = st.empty()
    jd_text = st.text_area(
        "jd", placeholder="We are looking for a Senior Software Engineer with experience in…",
        height=300, label_visibility="collapsed", key="jd_input",
    )
    char_placeholder.markdown(f"""
    <div class="input-header">
      <div>
        <div class="input-title">Job description</div>
        <div class="input-sub">Paste the full role description for best results.</div>
      </div>
      <div class="count-pill">{len(jd_text)} chars</div>
    </div>""", unsafe_allow_html=True)

with col2:
    file_placeholder = st.empty()
    uploaded_files = st.file_uploader(
        "resumes", type=["pdf"], accept_multiple_files=True,
        label_visibility="collapsed", key="resume_upload",
    )
    file_count = len(uploaded_files) if uploaded_files else 0
    file_placeholder.markdown(f"""
    <div class="input-header">
      <div>
        <div class="input-title">Resumes</div>
        <div class="input-sub">Drop PDF files or click to browse.</div>
      </div>
      <div class="count-pill">{file_count} file{"s" if file_count != 1 else ""}</div>
    </div>""", unsafe_allow_html=True)

# ── BUTTON (centred via a middle column) ─────────────────
_, mid, _ = st.columns([2, 1, 2])
with mid:
    run = st.button("✈  Start screening", key="btn_screen")

# ── RESULTS ──────────────────────────────────────────────
if run:
    if not jd_text.strip():
        st.error("Please paste a job description first.")
    elif not uploaded_files:
        st.error("Please upload at least one resume PDF.")
    else:
        with st.spinner("Analysing candidates…"):
            try:
                resumes = []
                for f in uploaded_files:
                    text = extract_pdf_text(f)
                    if text:
                        resumes.append({"name": f.name, "text": text})
                    else:
                        st.warning(f"Could not extract text from {f.name} — skipping.")

                if not resumes:
                    st.error("No readable text found in the uploaded PDFs.")
                else:
                    results = analyse_resumes(jd_text, resumes)
                    n = len(results)

                    st.markdown(f"""
                    <div style="margin-top:1rem;">
                      <div class="results-badge">🏆 &nbsp;Ranked shortlist</div>
                      <div class="results-title">Screening results</div>
                      <div class="results-sub">{n} candidate{"s" if n != 1 else ""} analysed, ranked by match score.</div>
                    </div>""", unsafe_allow_html=True)

                    for r in results:
                        sc        = r.get("score", 0)
                        sc_cls    = score_class(sc)
                        rank      = r.get("rank", 0)
                        name      = r.get("candidate_name", "Unknown")
                        summary   = r.get("summary", "")
                        strengths = r.get("strengths", [])
                        gaps      = r.get("gaps", [])

                        rank_cls  = "top" if rank == 1 else ""
                        s_tags    = "".join(f'<span class="skill-tag str">{s}</span>' for s in strengths)
                        g_tags    = "".join(f'<span class="skill-tag gap">{g}</span>' for g in gaps)

                        st.markdown(f"""
                        <div class="ccard">
                          <div class="ccard-top">
                            <div class="ccard-left">
                              <div class="rank-badge {rank_cls}">#{rank}</div>
                              <div>
                                <div class="ccard-name">{name}</div>
                                <div class="ccard-sub">Match Analysis</div>
                              </div>
                            </div>
                            <div class="match-pill match-{sc_cls}">↗ &nbsp;{sc}% match</div>
                          </div>
                          <div class="score-bar-bg">
                            <div class="score-bar-fill bar-{sc_cls}" style="width:{sc}%"></div>
                          </div>
                          <div class="ccard-summary">{summary}</div>
                          <div class="skills-grid">
                            <div>
                              <div class="skills-label str">Top Strengths</div>
                              <div class="skills-tags">{s_tags}</div>
                            </div>
                            <div>
                              <div class="skills-label gap">Skill Gaps</div>
                              <div class="skills-tags">{g_tags}</div>
                            </div>
                          </div>
                        </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  <div class="footer-credit">
    Developed by <span>Aryan Ajmera</span>
  </div>
  <div class="footer-links-wrap">
    <a class="footer-btn footer-btn-li"
       href="https://www.linkedin.com/in/aryan-ajmera7" target="_blank">
      <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
      </svg>
      LinkedIn
    </a>
    <a class="footer-btn footer-btn-web"
       href="https://aryanlovescoding.github.io/AryanWebsite/" target="_blank">
      <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
      Portfolio
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
