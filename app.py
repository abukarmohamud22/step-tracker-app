import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Page Configuration & Hiding Branding via layout/config properties
st.set_page_config(
    page_title="Smart Step Tracker",
    page_icon="👟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. LANGUAGE TRANSLATIONS DICTIONARY ---
translations = {
    "Soomaali": {
        "title": "👟 Smart Step Tracker & AI Motivator",
        "subtitle": "Taleefankaaga jeebka geli ama gacanta ku hay — **tallaabo kasta si otomaatig ah ayay u kordhaysaa!**",
        "sidebar_header": "⚙️ Dejinta App-ka",
        "lang_label": "Dooro Luqadda / Language:",
        "day_label": "Maanta waa Maalin Kee:",
        "goal_label": "Hadaafka Maalinlaha ah (Goal):",
        "start_btn": "▶️ Bilow (Start)",
        "stop_btn": "🛑 Jooji (Stop)",
        "today_steps": "Tallaabooyinka Maanta",
        "timer_text": "⏱️ Wakhtiga Socodka:",
        "analytics_box": "📊 Xogta Isbuuceeda (Weekly Analytics)",
        "analytics_desc": "Halkan ka daawo maalmaha aad socodka ugu badnayd iyo maalmaha aad yaraysay:",
        "insights": "💡 **AI Insights:** Maalinta aad **ugu badanayd** socodka waxay ahayd **{max_day}**, halka maalinta aad **ugu yarayd** ay ahayd **{min_day}**. Joogteey dadaalkaaga!",
        "notes_title": "📝 Qoraallada & Dareenka Maanta",
        "note_input": "Tusaale: Maanta waxaan lugeeyay xilli hore...",
        "save_btn": "Kaydi Qoraalka",
        "saved_msg": "Waa la kaydiyay!",
        "days": ["Isniin", "Talaado", "Arbaco", "Khamiis", "Jimco", "Sabti", "Axad"],
        "quotes": [
            "🌟 Guushu waxay ku timaadaa tallaabooyin joogto ah. Horay u soco!",
            "💪 Jir caafimaad qaba wuxuu ku jiraa lugeyn joogto ah. Aad bay kuu taraysaa!",
            "🔥 1,000 tallaabo ayaa dhabarkaaga ka baxay! Joogso ma jiro!",
            "🚀 Waxaad tahay qof hami leh! Hadaafkii waa uu sii dhowaanayaa.",
            "🎯 Nolosha waa l sakin — tallaabo kasta waa guul cusub!"
        ]
    },
    "English": {
        "title": "👟 Smart Step Tracker & AI Motivator",
        "subtitle": "Keep your phone in your pocket or hand — **every step counts automatically!**",
        "sidebar_header": "⚙️ App Settings",
        "lang_label": "Select Language:",
        "day_label": "Select Today's Day:",
        "goal_label": "Daily Step Goal:",
        "start_btn": "▶️ Start",
        "stop_btn": "🛑 Stop",
        "today_steps": "Today's Steps",
        "timer_text": "⏱️ Walking Time:",
        "analytics_box": "📊 Weekly Analytics",
        "analytics_desc": "Check your most active days and low-activity days this week:",
        "insights": "💡 **AI Insights:** Your **most active** day was **{max_day}**, and your **lowest** day was **{min_day}**. Keep up the great work!",
        "notes_title": "📝 Daily Notes & Mood",
        "note_input": "Example: Walked early in the morning today...",
        "save_btn": "Save Note",
        "saved_msg": "Successfully saved!",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "quotes": [
            "🌟 Success comes from consistent steps. Keep moving forward!",
            "💪 A healthy body relies on regular walking. Great job!",
            "🔥 1,000 steps unlocked! There's no stopping you!",
            "🚀 You are ambitious! Your daily goal is getting closer.",
            "🎯 Every single step is a new victory!"
        ]
    }
}

# --- 2. SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Menu")
lang_choice = st.sidebar.selectbox(
    "Language / Luqad:", ["Soomaali", "English"])
t = translations[lang_choice]

st.sidebar.markdown("---")
st.sidebar.subheader(t["sidebar_header"])
selected_day = st.sidebar.selectbox(t["day_label"], t["days"])
daily_goal = st.sidebar.number_input(t["goal_label"], value=1000, step=500)

# --- 3. MAIN INTERFACE ---
st.title(t["title"])
st.markdown(t["subtitle"])

# Session state initialization
if "weekly_data" not in st.session_state:
    st.session_state.weekly_data = {
        t["days"][0]: 1200, t["days"][1]: 3400, t["days"][2]: 800,
        t["days"][3]: 4500, t["days"][4]: 2100, t["days"][5]: 5000, t["days"][6]: 1500
    }

if "notes" not in st.session_state:
    st.session_state.notes = []

# --- 4. HTML + JS SENSOR COMPONENT ---
quotes_js = json.dumps(t["quotes"])

sensor_code = f"""
<div style="font-family: sans-serif; text-align: center; padding: 25px; border: 2px solid #4CAF50; border-radius: 20px; background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%); box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h3 style="color: #2e7d32; margin-top: 0;">{t["today_steps"]} ({selected_day})</h3>
    <div id="stepCount" style="font-size: 72px; font-weight: 800; color: #2e7d32; line-height: 1;">0</div>
    
    <div style="font-size: 18px; color: #555; margin: 15px 0;">
        {t["timer_text"]} <span id="timer" style="font-weight: bold; color: #333;">00:00</span>
    </div>

    <div id="motivationBox" style="display: none; background-color: #e8f5e9; color: #1b5e20; padding: 15px; border-radius: 12px; font-weight: bold; margin: 15px 0; border: 1px solid #4CAF50; font-size: 16px;">
        🤖 <span id="motivationText">Hambalyo!</span>
    </div>

    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px;">
        <button onclick="startTracking()" style="background-color: #4CAF50; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1;">
            {t["start_btn"]}
        </button>
        <button onclick="stopTracking()" style="background-color: #e53935; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1;">
            {t["stop_btn"]}
        </button>
    </div>
</div>

<script>
let steps = 0;
let seconds = 0;
let timerInterval = null;
let isTracking = false;
let lastStepTime = 0;
let lastMilestone = 0;
const quotes = {quotes_js};

function playAlarmSound() {{
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(880, audioCtx.currentTime);
    oscillator.connect(audioCtx.destination);
    oscillator.start();
    setTimeout(() => oscillator.stop(), 800);
}}

function startTracking() {{
    if (isTracking) return;
    isTracking = true;

    timerInterval = setInterval(() => {{
        seconds++;
        let mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        let secs = (seconds % 60).toString().padStart(2, '0');
        document.getElementById("timer").innerText = mins + ":" + secs;
    }}, 1000);

    if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {{
        DeviceMotionEvent.requestPermission().then(response => {{
            if (response == 'granted') {{
                window.addEventListener('devicemotion', detectStep);
            }}
        }});
    }} else {{
        window.addEventListener('devicemotion', detectStep);
    }}
}}

function detectStep(event) {{
    if (!isTracking) return;
    let acc = event.accelerationIncludingGravity;
    if (!acc) return;

    let totalForce = Math.sqrt(acc.x * acc.x + acc.y * acc.y + acc.z * acc.z);
    let now = Date.now();

    if (totalForce > 13.5 && (now - lastStepTime) > 350) {{
        steps++;
        lastStepTime = now;
        document.getElementById("stepCount").innerText = steps;

        let currentMilestone = Math.floor(steps / 1000);
        if (currentMilestone > lastMilestone) {{
            lastMilestone = currentMilestone;
            let randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
            document.getElementById("motivationText").innerText = "Milestone (" + (currentMilestone * 1000) + "): " + randomQuote;
            document.getElementById("motivationBox").style.display = "block";
            playAlarmSound();
        }}
    }}
}}

function stopTracking() {{
    isTracking = false;
    clearInterval(timerInterval);
    window.removeEventListener('devicemotion', detectStep);
}}
</script>
"""

components.html(sensor_code, height=400)

# --- 5. WEEKLY ANALYTICS EXPANDER BOX ---
st.markdown("---")
with st.expander(t["analytics_box"], expanded=False):
    st.write(t["analytics_desc"])

    current_weekly_dict = st.session_state.weekly_data
    df_steps = pd.DataFrame(list(current_weekly_dict.items()), columns=[
                            "Maalinta", "Tallaabooyinka"])
    df_steps.set_index("Maalinta", inplace=True)

    st.bar_chart(df_steps, color="#4CAF50")

    max_day = df_steps["Tallaabooyinka"].idxmax()
    min_day = df_steps["Tallaabooyinka"].idxmin()

    st.info(t["insights"].format(max_day=max_day, min_day=min_day))

# --- 6. DAILY NOTES SECTION ---
st.markdown("---")
st.subheader(t["notes_title"])
note_input = st.text_input(t["note_input"])
if st.button(t["save_btn"]) and note_input:
    st.session_state.notes.append(note_input)
    st.success(t["saved_msg"])

if st.session_state.notes:
    for idx, n in enumerate(st.session_state.notes, 1):
        st.write(f"**{idx}.** {n}")
