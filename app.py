import streamlit as st
import time
from datetime import datetime
from zoneinfo import ZoneInfo

EST = ZoneInfo("America/New_York")

st.set_page_config(
    page_title="Snowfall Probability – Zack Hennigan",
    page_icon="❄️",
    layout="centered",
)

# Hide Streamlit default UI for a clean look
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: #0b1628;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0;
        max-width: 700px;
    }
    iframe {
        border: none !important;
    }
    .last-updated {
        text-align: center;
        color: #5a8ec2;
        font-family: sans-serif;
        font-size: 12px;
        margin-top: 8px;
    }
    .on-the-fours {
        text-align: center;
        font-family: sans-serif;
        margin-bottom: 12px;
    }
    .on-the-fours .tagline {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .on-the-fours .tagline span {
        color: #6eaaef;
    }
    .on-the-fours .sub {
        font-size: 12px;
        color: #5a8ec2;
        letter-spacing: 1px;
        margin-top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SNOWFALL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { background: #0b1628; margin: 0; padding: 8px; }
  body {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    font-family: 'Source Sans Pro', sans-serif;
  }
  .card {
    width: 100%;
    max-width: 620px;
    background: linear-gradient(165deg, #0f2044 0%, #162d5a 40%, #1a3568 70%, #0f2044 100%);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 80px rgba(30, 90, 180, 0.15);
    position: relative;
  }
  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
  }
  .snowflakes {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    overflow: hidden;
  }
  .snowflake {
    position: absolute;
    color: rgba(255,255,255,0.08);
    font-size: 18px;
    animation: fall linear infinite;
  }
  .snowflake:nth-child(1) { left: 8%; animation-duration: 12s; animation-delay: 0s; font-size: 14px; }
  .snowflake:nth-child(2) { left: 22%; animation-duration: 15s; animation-delay: 2s; font-size: 20px; }
  .snowflake:nth-child(3) { left: 45%; animation-duration: 10s; animation-delay: 4s; font-size: 12px; }
  .snowflake:nth-child(4) { left: 65%; animation-duration: 14s; animation-delay: 1s; font-size: 16px; }
  .snowflake:nth-child(5) { left: 82%; animation-duration: 11s; animation-delay: 3s; font-size: 22px; }
  .snowflake:nth-child(6) { left: 92%; animation-duration: 13s; animation-delay: 5s; font-size: 10px; }
  @keyframes fall {
    0% { transform: translateY(-30px) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(700px) rotate(360deg); opacity: 0; }
  }
  .header {
    padding: 28px 32px 8px;
    text-align: center;
    position: relative;
    z-index: 1;
  }
  .storm-label {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6eaaef;
    margin-bottom: 6px;
  }
  .title {
    font-family: 'Oswald', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2px;
    line-height: 1.15;
  }
  .subtitle {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 15px;
    color: #8ab4e0;
    margin-top: 6px;
    font-weight: 400;
  }
  .divider {
    height: 3px;
    background: linear-gradient(90deg, transparent, #3b7fdb, transparent);
    margin: 16px 32px;
    border-radius: 2px;
  }
  .bars-container {
    padding: 8px 32px 24px;
    position: relative;
    z-index: 1;
  }
  .bar-row { margin-bottom: 16px; }
  .bar-label-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
  }
  .bar-label {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #d0dff0;
  }
  .bar-label.highlight { color: #ffffff; font-size: 17px; font-weight: 700; }
  .bar-percent {
    font-family: 'Oswald', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #6eaaef;
  }
  .bar-percent.highlight {
    color: #ffffff;
    font-size: 28px;
    text-shadow: 0 0 20px rgba(110, 170, 239, 0.5);
  }
  .bar-track {
    width: 100%;
    height: 14px;
    background: rgba(255,255,255,0.08);
    border-radius: 7px;
    overflow: hidden;
  }
  .bar-track.highlight { height: 18px; border-radius: 9px; }
  .bar-fill {
    height: 100%;
    border-radius: 7px;
    background: linear-gradient(90deg, #2b6cb8, #4a9af5);
    position: relative;
  }
  .bar-fill.highlight {
    background: linear-gradient(90deg, #3b82f6, #60b3ff);
    box-shadow: 0 0 16px rgba(60, 150, 255, 0.4);
    border-radius: 9px;
  }
  .bar-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.2), transparent);
    border-radius: inherit;
  }
  .footer {
    padding: 14px 32px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 1;
    border-top: 1px solid rgba(255,255,255,0.06);
  }
  .credit {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 13px;
    color: #5a8ec2;
    font-weight: 600;
  }
  .credit span { color: #8ab4e0; font-weight: 700; }
  .snowflake-icon { font-size: 20px; opacity: 0.4; }

  @media (max-width: 480px) {
    .header { padding: 20px 18px 6px; }
    .title { font-size: 24px; letter-spacing: 1px; }
    .storm-label { font-size: 11px; }
    .subtitle { font-size: 13px; }
    .divider { margin: 12px 18px; }
    .bars-container { padding: 6px 18px 18px; }
    .bar-label { font-size: 13px; }
    .bar-label.highlight { font-size: 15px; }
    .bar-percent { font-size: 18px; }
    .bar-percent.highlight { font-size: 24px; }
    .footer { padding: 12px 18px 16px; }
  }
</style>
</head>
<body>
<div class="card">
  <div class="snowflakes">
    <div class="snowflake">&#10052;</div>
    <div class="snowflake">&#10052;</div>
    <div class="snowflake">&#10052;</div>
    <div class="snowflake">&#10052;</div>
    <div class="snowflake">&#10052;</div>
    <div class="snowflake">&#10052;</div>
  </div>
  <div class="header">
    <div class="storm-label">Winter Storm Outlook</div>
    <div class="title">Snowfall Amount Probability</div>
    <div class="subtitle">Sunday, Feb 22 &rarr; Early Monday, Feb 23</div>
  </div>
  <div class="divider"></div>
  <div class="bars-container">
    <div class="bar-row">
      <div class="bar-label-row">
        <span class="bar-label">Greater than 10 in</span>
        <span class="bar-percent">4%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:4%;"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label-row">
        <span class="bar-label">6 &ndash; 10 in</span>
        <span class="bar-percent">8%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:8%;"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label-row">
        <span class="bar-label highlight">3 &ndash; 6 in</span>
        <span class="bar-percent highlight">71%</span>
      </div>
      <div class="bar-track highlight"><div class="bar-fill highlight" style="width:71%;"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label-row">
        <span class="bar-label">1 &ndash; 3 in</span>
        <span class="bar-percent">10%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:10%;"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label-row">
        <span class="bar-label">Less than 1 in</span>
        <span class="bar-percent">7%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:7%;"></div></div>
    </div>
  </div>
  <div class="footer">
    <div class="credit">Meteorologist <span>Zack Hennigan</span></div>
    <div class="snowflake-icon">&#10052;</div>
  </div>
</div>
</body>
</html>
"""

# "On The 4's" banner
st.markdown(
    '<div class="on-the-fours">'
    '<div class="tagline">❄️ Weather <span>On The 4\'s</span> ❄️</div>'
    '<div class="sub">Auto-updated every :04 · :14 · :24 · :34 · :44 · :54</div>'
    '</div>',
    unsafe_allow_html=True,
)

# Render the graphic
st.components.v1.html(SNOWFALL_HTML, height=620, scrolling=False)

# Calculate the most recent :X4 time
def most_recent_x4():
    now = datetime.now(EST)
    current_min = now.minute
    targets = [54, 44, 34, 24, 14, 4]
    for t in targets:
        if current_min >= t:
            return now.replace(minute=t, second=0, microsecond=0)
    # Current minute is 0-3, so most recent was :54 of previous hour
    prev_hour = now.replace(second=0, microsecond=0)
    prev_hour = prev_hour.replace(minute=54)
    if now.hour == 0:
        prev_hour = prev_hour.replace(hour=23)
    else:
        prev_hour = prev_hour.replace(hour=now.hour - 1)
    return prev_hour

last_x4 = most_recent_x4()
st.markdown(
    f'<div class="last-updated">Last updated: {last_x4.strftime("%I:%M %p")} EST</div>',
    unsafe_allow_html=True,
)

# --- Auto-refresh logic ---
# Calculate seconds until the next minute ending in :X4
def seconds_until_next_x4():
    now = datetime.now(EST)
    current_min = now.minute
    current_sec = now.second

    # Find next minute ending in 4: 4, 14, 24, 34, 44, 54
    targets = [4, 14, 24, 34, 44, 54]
    for t in targets:
        if t > current_min or (t == current_min and current_sec < 2):
            diff_min = t - current_min
            return max(diff_min * 60 - current_sec, 1)

    # Wrap to next hour's :04
    diff_min = (60 - current_min) + 4
    return max(diff_min * 60 - current_sec, 1)


wait = seconds_until_next_x4()

# Streamlit's st.rerun with a sleep timer to hit the :X4 marks
time.sleep(wait)
st.rerun()
