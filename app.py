import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(page_title="Smart Step Tracker & AI Motivator",
                   page_icon="👟", layout="centered")

st.title("👟 Smart Step Tracker & AI Motivator")
st.write("Taleefankaaga jeebka geli ama gacanta ku hay — **tallaabo kasta si otomaatig ah ayay u kordhaysaa!**")

# --- 1. SESSION STATE INITIALIZATION ---
if "weekly_data" not in st.session_state:
    # Keydinta xogta isbuuca (Tusaale ahaan maalmaha isbuuca iyo tallaabooyinkoodii)
    st.session_state.weekly_data = {
        "Isniin": 1200,
        "Talaado": 3400,
        "Arbaco": 800,
        "Khamiis": 4500,
        "Jimco": 2100,
        "Sabti": 5000,
        "Axad": 1500
    }

if "notes" not in st.session_state:
    st.session_state.notes = []

# Sidebar for Settings & Weekly Overview
st.sidebar.header("⚙️ Dejinta Isbuuca")
selected_day = st.sidebar.selectbox("Dooro Maanta waa Maalin Kee:", [
                                    "Isniin", "Talaado", "Arbaco", "Khamiis", "Jimco", "Sabti", "Axad"])
daily_goal = st.sidebar.number_input(
    "Hadaafka Maalinlaha ah:", value=1000, step=500)

# --- 2. HTML + JS SENSOR COMPONENT WITH DYNAMIC MOTIVATION ---
sensor_code = f"""
<div style="font-family: sans-serif; text-align: center; padding: 25px; border: 2px solid #4CAF50; border-radius: 20px; background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%); box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h3 style="color: #2e7d32; margin-top: 0;">Tallaabooyinka Maanta ({selected_day})</h3>
    <div id="stepCount" style="font-size: 72px; font-weight: 800; color: #2e7d32; line-height: 1;">0</div>
    
    <div style="font-size: 18px; color: #555; margin: 15px 0;">
        ⏱️ Wakhtiga Socodka: <span id="timer" style="font-weight: bold; color: #333;">00:00</span>
    </div>

    <!-- AI Motivational Box oo soo boodaya mar kasta oo 1000 la gaaro -->
    <div id="motivationBox" style="display: none; background-color: #e8f5e9; color: #1b5e20; padding: 15px; border-radius: 12px; font-weight: bold; margin: 15px 0; border: 1px solid #4CAF50; font-size: 16px;">
        🤖 <span id="motivationText">Hambalyo! Waa tallaabo weyn!</span>
    </div>

    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px;">
        <button onclick="startTracking()" style="background-color: #4CAF50; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1;">
            ▶️ Bilow (Start)
        </button>
        <button onclick="stopTracking()" style="background-color: #e53935; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1;">
            🛑 Jooji (Stop)
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

// Hadalada Dhiirrigelinta ah ee AI-ga
const quotes = [
    "🌟 Guushu waxay ku timaadaa tallaabooyin joogto ah. Horay u soco!",
    "💪 Jir caafimaad qaba wuxuu ku jiraa lugeyn joogto ah. Aad bay kuu taraysaa!",
    "🔥 1,000 tallaabo ayaa dhabarkaaga ka baxay! Joogso ma jiro!",
    "🚀 Waxaad tahay qof hami leh! Hadaafkii waa uu sii dhowaanayaa.",
    "🎯 Nolosha waa l sakin — tallaabo kasta waa guul cusub!"
];

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

        // Hubi markasta oo 1,000 tallaabo la dhaafo
        let currentMilestone = Math.floor(steps / 1000);
        if (currentMilestone > lastMilestone) {{
            lastMilestone = currentMilestone;
            let randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
            document.getElementById("motivationText").innerText = "Milestone (" + (currentMilestone * 1000) + " steps): " + randomQuote;
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

# --- 3. WEEKLY ANALYTICS & CHARTS SECTION ---
st.markdown("---")
st.subheader("📊 Xogta Isbuuceeda (Weekly Analytics)")
st.write("Halkan ka daawo maalmaha aad socodka ugu badnayd iyo maalmaha aad yaraysay:")

# Beddelista xogta isbuuca si Streamlit u sawiro Bar Chart
df_steps = pd.DataFrame(list(st.session_state.weekly_data.items()), columns=[
                        "Maalinta", "Tallaabooyinka"])
df_steps.set_index("Maalinta", inplace=True)

# Muujinta Bar Chart-ka xogta isbuuca
st.bar_chart(df_steps, color="#4CAF50")

# Falanqeyn yar oo AI ah oo ku saabsan isbuuca
max_day = df_steps["Tallaabooyinka"].idxmax()
min_day = df_steps["Tallaabooyinka"].idxmin()

st.info(
    f"💡 **AI Insights:** Maalinta aad **ugu badanayd** socodka waxay ahayd **{max_day}**, halka maalinta aad **ugu yarayd** ay ahayd **{min_day}**. Joogteey dadaalkaaga!")

# --- 4. DAILY NOTES SECTION ---
st.markdown("---")
st.subheader("📝 Qoraallada & Dareenka Maanta")
note_input = st.text_input(
    "Tusaale: Maanta waxaan lugeeyay xilli hore oo subax ah...")
if st.button("Kaydi Qoraalka") and note_input:
    st.session_state.notes.append(note_input)
    st.success("Waa la kaydiyay!")

if st.session_state.notes:
    for idx, n in enumerate(st.session_state.notes, 1):
        st.write(f"**{idx}.** {n}")
