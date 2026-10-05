import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --bg:#07120d; --panel:#0d1d16; --panel2:#10261c; --line:#1b3b2c; --green:#63f29a; --mint:#b6ffd0; --text:#eefaf2; --muted:#91a99a; }
    html,body,[class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background: radial-gradient(circle at 85% 5%, #123a27 0, transparent 28%), var(--bg); color:var(--text); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#08150f,#06100c); border-right:1px solid var(--line); }
    .block-container { max-width:1500px; padding-top:1.5rem; }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.03em; }
    .brand-mark { width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--green),#24a85d); color:#062011; display:flex;align-items:center;justify-content:center;font-weight:800;font-family:'Space Grotesk'; box-shadow:0 0 30px #63f29a33; }
    .side-footer { color:#526b5c;font-size:10px;line-height:1.7;margin-top:2rem; }
    .topbar { display:flex;align-items:center;justify-content:space-between;margin-bottom:20px; }
    .topbar h1 { margin:.1rem 0 0;font-size:32px; }
    .eyebrow { color:var(--green);font-size:11px;font-weight:700;letter-spacing:.16em; }
    .top-status { color:var(--green);border:1px solid #27583e;background:#0b2418;padding:8px 12px;border-radius:999px;font-size:11px;font-weight:700; }
    .hero-panel { min-height:260px;padding:38px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(135deg,#102a1eaa,#0a1711ee);display:flex;align-items:center;justify-content:space-between;overflow:hidden;position:relative; }
    .hero-panel:before { content:'';position:absolute;inset:-50%;background:radial-gradient(circle,#63f29a12,transparent 35%);animation:pulse 5s infinite alternate; }
    .hero-panel h2 { font-size:44px;margin:8px 0;position:relative; }
    .hero-panel p { max-width:650px;color:var(--muted);font-size:16px;position:relative; }
    .hero-orb { width:160px;height:160px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid #63f29a55;color:var(--green);font-size:70px;box-shadow:0 0 80px #63f29a20;animation:float 4s ease-in-out infinite; }
    @keyframes float {50%{transform:translateY(-10px) scale(1.03)}} @keyframes pulse {to{transform:translate(8%,4%) scale(1.08)}}
    .metric-card,.workflow-card,.result-card { background:linear-gradient(145deg,#102219,#0b1711);border:1px solid var(--line);border-radius:20px;padding:20px;transition:.25s; }
    .metric-card:hover,.workflow-card:hover { transform:translateY(-3px);border-color:#2d6e4a; }
    .metric-label { color:var(--muted);font-size:12px; } .metric-value { font:700 25px 'Space Grotesk';margin:5px 0; } .metric-help{font-size:11px;color:#5f7969}
    .workflow-card { min-height:120px;display:flex;flex-direction:column;gap:8px; } .workflow-card span{color:var(--green);font-size:11px}.workflow-card b{font-family:'Space Grotesk'}.workflow-card small{color:var(--muted)}
    .result-card { display:flex;justify-content:space-between;align-items:center;margin-top:18px;background:linear-gradient(110deg,#10291d,#0a1610); }
    .result-card h2 { margin:5px 0;color:var(--green); }
    .risk-ring { width:100px;height:100px;border:5px solid var(--green);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 40px #63f29a22; } .risk-ring b{font:700 27px 'Space Grotesk'} .risk-ring span{font-size:10px;color:var(--muted)}
    .stButton > button { background:linear-gradient(135deg,#63f29a,#38ca76);color:#062011;border:0;border-radius:12px;font-weight:800;min-height:42px;transition:.2s; }
    .stButton > button:hover { transform:translateY(-2px);box-shadow:0 10px 30px #63f29a25; }
    [data-testid="stFileUploaderDropzone"] { border:1px dashed #2c6547;background:#0b1c13; }
    div[data-baseweb="input"],div[data-baseweb="select"] { background:#0b1912; }
    .stDataFrame { border:1px solid var(--line);border-radius:14px;overflow:hidden; }
    </style>
    """, unsafe_allow_html=True)

def metric_card(label, value, help_text):
    return f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-help">{help_text}</div></div>'

def section_title(title, subtitle=""):
    st.markdown(f"### {title}")
    if subtitle: st.caption(subtitle)

def status_badge(text):
    return f'<span class="top-status">{text}</span>'
