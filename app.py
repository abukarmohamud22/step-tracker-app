import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Auto Step Tracker", page_icon="👟")

st.title("👟 Auto Step Counter (Sensor Mode)")
st.write("Ku rid taleefanka jeebka ama gacanta ku hay — **tallaabo kasta isagaa 1 u tirinaya!**")

# --- HTML + JavaScript Component for Real Phone Accelerometer & Live Timer ---
sensor_code = """
<div style="font-family: sans-serif; text-align: center; padding: 20px; border: 2px solid #4CAF50; border-radius: 15px; background-color: #f9f9f9;">
    <h2 style="color: #333; margin-bottom: 5px;">Tallaabooyinka (Steps)</h2>
    <div id="stepCount" style="font-size: 64px; font-weight: bold; color: #4CAF50;">0</div>
    
    <div style="font-size: 20px; color: #555; margin: 10px 0;">
        ⏱️ Wakhtiga: <span id="timer">00:00</span>
    </div>

    <div id="alarmBox" style="display: none; background-color: #ffeb3b; color: #000; padding: 15px; border-radius: 10px; font-weight: bold; margin: 15px 0;">
        🔔 ALARM: Hambalyo! Waxaad gaartay 1,000 tallaabo!
    </div>

    <button id="startBtn" onclick="startTracking()" style="background-color: #4CAF50; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; margin: 5px;">
        ▶️ Bilow Socodka (Start)
    </button>
    
    <button onclick="stopTracking()" style="background-color: #f44336; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; margin: 5px;">
        🛑 Jooji & Ka Bax (Exit)
    </button>

    <div id="exitMessage" style="display: none; margin-top: 20px; padding: 15px; background-color: #e8f5e9; border-left: 5px solid #4CAF50; font-size: 18px; color: #2e7d32;">
        🎉 <strong>Good job! Maanta shaqo fiican ayaad qabatay!</strong>
    </div>
</div>

<script>
let steps = 0;
let seconds = 0;
let timerInterval = null;
let isTracking = false;
let lastStepTime = 0;

// Codka Alarm-ka (Beep Sound)
function playAlarmSound() {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(880, audioCtx.currentTime); // Dhawaaq sare
    oscillator.connect(audioCtx.destination);
    oscillator.start();
    setTimeout(() => oscillator.stop(), 800); // Wuxuu dhacayaa 0.8 ilbiriqsi
}

function startTracking() {
    if (isTracking) return;
    isTracking = true;
    document.getElementById("exitMessage").style.display = "none";

    // Bilow Saacadda (Timer)
    timerInterval = setInterval(() => {
        seconds++;
        let mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        let secs = (seconds % 60).toString().padStart(2, '0');
        document.getElementById("timer").innerText = mins + ":" + secs;
    }, 1000);

    // Weydiiso oggolaanshaha Sensor-ka (iPhone/Android)
    if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {
        DeviceMotionEvent.requestPermission().then(response => {
            if (response == 'granted') {
                window.addEventListener('devicemotion', detectStep);
            }
        });
    } else {
        window.addEventListener('devicemotion', detectStep);
    }
}

function detectStep(event) {
    if (!isTracking) return;
    let acc = event.accelerationIncludingGravity;
    if (!acc) return;

    // Xisaabi xoogga dhaqdhaqaaqa (Magnitude)
    let totalForce = Math.sqrt(acc.x * acc.x + acc.y * acc.y + acc.z * acc.z);
    let now = Date.now();

    // Haddii xooggu dhaafo 13.5 isla markaana 350ms ka soo wareegtay tallaabadii hore -> +1 Tallaabo!
    if (totalForce > 13.5 && (now - lastStepTime) > 350) {
        steps++;
        lastStepTime = now;
        document.getElementById("stepCount").innerText = steps;

        // Hubi 1,000-ka tallaabo
        if (steps % 1000 === 0) {
            document.getElementById("alarmBox").style.display = "block";
            playAlarmSound();
        }
    }
}

function stopTracking() {
    isTracking = false;
    clearInterval(timerInterval);
    window.removeEventListener('devicemotion', detectStep);
    document.getElementById("exitMessage").style.display = "block";
}
</script>
"""

components.html(sensor_code, height=450)

# --- Qaybta Qoraallada (Notes) ---
st.subheader("📝 Daily Walk Notes")
if "notes" not in st.session_state:
    st.session_state.notes = []

note = st.text_input("Qor dareenkaaga ama meesha aad maanta ku lugeysay:")
if st.button("Save Note") and note:
    st.session_state.notes.append(note)

for i, n in enumerate(st.session_state.notes, 1):
    st.write(f"**{i}.** {n}")
