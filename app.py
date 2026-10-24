import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

st.set_page_config(
    page_title="IQRA AI — Your Personal Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------ Styling ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink: #292347;
  --muted: #77738f;
  --purple: #7657e8;
  --pink: #e45bb7;
  --blue: #54a9f5;
  --line: rgba(120, 102, 190, .17);
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 10% 0%, rgba(228,91,183,.13), transparent 33%),
    radial-gradient(ellipse at 95% 8%, rgba(84,169,245,.14), transparent 30%),
    linear-gradient(135deg, #fbfaff 0%, #f6f3ff 48%, #f7fbff 100%);
  color: var(--ink);
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1180px; padding-top: 1.35rem; padding-bottom: 6rem; }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #f1edff 0%, #f8f4ff 52%, #eef7ff 100%);
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
.brand {
  display:flex; align-items:center; gap:12px; margin: 4px 0 26px;
}
.brand-icon {
  display:flex; align-items:center; justify-content:center; width:48px; height:48px;
  border-radius:16px; font-size:25px; color:white;
  background:linear-gradient(135deg,#7757eb,#e15ab6 62%,#68b8fa);
  box-shadow:0 9px 24px rgba(123,83,220,.28);
  animation: floaty 3.2s ease-in-out infinite;
}
.brand-name {font-family:'Space Grotesk',sans-serif;font-size:23px;font-weight:700;letter-spacing:-.7px;color:#30264e;}
.brand-sub {font-size:11px;color:#8880a5;margin-top:1px;letter-spacing:.8px;text-transform:uppercase;}
@keyframes floaty {0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-6px) rotate(4deg)}}
.hero {
  max-width: 760px; margin: 5vh auto 2.4rem; text-align:center; padding: 28px 22px 10px;
}
.orb {
  width:104px;height:104px;border-radius:32px;margin:0 auto 23px;display:flex;
  justify-content:center;align-items:center;font-size:51px;
  background:linear-gradient(140deg,#e8ddff,#ffe1f4 55%,#dff2ff);
  box-shadow:0 18px 50px rgba(126,92,210,.18), inset 0 0 0 1px rgba(255,255,255,.9);
  animation: floaty 3s ease-in-out infinite;
}
.eyebrow {
  display:inline-block;padding:7px 13px;border-radius:999px;
  color:#7354d9;background:#eee8ff;border:1px solid #e1d7ff;
  font-size:12px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;
}
.hero h1 {
  font-family:'Space Grotesk',sans-serif;font-size:clamp(34px,5vw,55px);
  line-height:1.12;letter-spacing:-1.8px;color:#2e254c;margin:17px 0 12px;
}
.gradient-text {
  background:linear-gradient(90deg,#7755e8,#d94eae 52%,#428fe9);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.hero p {font-size:16px;line-height:1.7;color:#77718f;max-width:590px;margin:0 auto;}
.feature-row {display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin:23px 0 10px;}
.feature-pill {border:1px solid #e8e0fa;background:rgba(255,255,255,.75);padding:9px 13px;border-radius:999px;font-size:12px;color:#625879;}
.panel {
  max-width:650px;margin:0 auto;background:rgba(255,255,255,.82);
  border:1px solid rgba(150,126,215,.23);border-radius:26px;padding:25px 27px;
  box-shadow:0 18px 60px rgba(70,47,130,.09);backdrop-filter:blur(14px);
}
.panel-title {font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:21px;color:#30264e;margin-bottom:5px;}
.panel-copy {color:#817b99;font-size:13px;line-height:1.6;margin-bottom:18px;}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
  border-radius:13px !important; border-color:#e2daf5 !important; background:#fff !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {border-color:#9b7bf1 !important;box-shadow:0 0 0 2px #eee7ff !important;}
.stButton > button, .stFormSubmitButton > button {
  border:0 !important;border-radius:13px !important;color:white !important;font-weight:700 !important;
  background:linear-gradient(100deg,#7655e8,#c853c5 58%,#5e9cf0) !important;
  box-shadow:0 8px 20px rgba(122,83,220,.2);padding:.68rem 1rem;transition:transform .18s ease,box-shadow .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {transform:translateY(-2px);box-shadow:0 12px 26px rgba(122,83,220,.27);}
div[data-testid="stChatMessage"] {
  background:rgba(255,255,255,.75);border:1px solid rgba(150,126,215,.14);
  border-radius:19px;padding:15px 18px;margin-bottom:12px;box-shadow:0 5px 18px rgba(70,47,130,.035);
}
div[data-testid="stChatInput"] {
  border:1px solid #ded5f4 !important;border-radius:20px !important;
  background:rgba(255,255,255,.96) !important;box-shadow:0 12px 34px rgba(75,48,130,.11) !important;
}
div[data-testid="stChatInput"] textarea {background:transparent !important;}
.chat-heading {display:flex;align-items:center;gap:12px;margin:4px 0 22px;}
.chat-heading .mini-orb {width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:15px;background:linear-gradient(140deg,#e8ddff,#ffe1f4,#dff2ff);font-size:24px;}
.chat-heading h2 {font-family:'Space Grotesk',sans-serif;font-size:24px;margin:0;color:#30264e;}
.chat-heading p {font-size:12px;color:#8982a1;margin:2px 0 0;}
div[data-testid="stAlert"] {border-radius:14px;}
.small-note {font-size:11px;color:#9690a9;line-height:1.5;text-align:center;margin-top:13px;}
.sidebar-note {font-size:12px;line-height:1.6;color:#807995;background:rgba(255,255,255,.68);border:1px solid #e8e0fa;padding:12px;border-radius:14px;}
@media(max-width:700px){.hero{margin-top:2vh;padding-left:4px;padding-right:4px}.panel{padding:19px 16px}.block-container{padding-left:1rem;padding-right:1rem}.hero p{font-size:14px}}
</style>
""", unsafe_allow_html=True)

# ------------------------------ State ------------------------------
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None
if "system_role" not in st.session_state:
    st.session_state.system_role = "You are a helpful, thoughtful assistant. Answer clearly and adapt to the user's needs."
if "model_name" not in st.session_state:
    st.session_state.model_name = "gpt-5.2"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.5

def new_chat():
    import uuid
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New conversation",
        "messages": [],
    }
    st.session_state.active_chat = chat_id

def reset_to_welcome():
    st.session_state.api_key = ""
    st.rerun()

# ------------------------------ Sidebar ------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">✨</div>
      <div><div class="brand-name">IQRA AI</div><div class="brand-sub">Your personal assistant</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.api_key:
        if st.button("＋  New chat", use_container_width=True):
            new_chat()
            st.rerun()

        st.markdown("##### Your conversations")
        if not st.session_state.chats:
            st.caption("Your chats will appear here.")
        else:
            for cid, chat_data in list(st.session_state.chats.items())[::-1]:
                label = ("● " if cid == st.session_state.active_chat else "○ ") + chat_data["title"][:28]
                if st.button(label, key=f"chat_{cid}", use_container_width=True):
                    st.session_state.active_chat = cid
                    st.rerun()

        st.divider()
        st.markdown("##### Customize")
        st.session_state.model_name = st.selectbox(
            "AI model",
            ["gpt-5.2", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"],
            index=["gpt-5.2", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"].index(st.session_state.model_name)
            if st.session_state.model_name in ["gpt-5.2", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"] else 0,
            help="Choose a model available to your OpenAI API account."
        )
        st.session_state.temperature = st.slider("Creativity", 0.0, 1.0, float(st.session_state.temperature), 0.1)
        with st.expander("Assistant personality"):
            role_text = st.text_area("System instructions", value=st.session_state.system_role, height=120)
            if st.button("Save personality", use_container_width=True):
                st.session_state.system_role = role_text.strip() or "You are a helpful assistant."
                st.success("Personality updated.")
        with st.expander("API key & privacy"):
            st.caption("Your key is held in this active Streamlit session and is not written to a file by this app. Only enter a key on a device and deployment you trust.")
            replacement_key = st.text_input("Replace OpenAI API key", type="password", placeholder="sk-...")
            if st.button("Update API key", use_container_width=True):
                if replacement_key.strip():
                    st.session_state.api_key = replacement_key.strip()
                    st.success("Key updated for this session.")
                    st.rerun()
            if st.button("Forget API key / lock app", use_container_width=True):
                reset_to_welcome()
    else:
        st.markdown('<div class="sidebar-note">🔐 Enter your own OpenAI API key on the welcome screen to start chatting. Your key is not saved to a project file.</div>', unsafe_allow_html=True)

# ------------------------------ Welcome screen ------------------------------
if not st.session_state.api_key:
    st.markdown("""
    <div class="hero">
      <div class="orb">🤖</div>
      <div class="eyebrow">✦ Meet your new AI sidekick</div>
      <h1>Big ideas start with<br><span class="gradient-text">a little conversation.</span></h1>
      <p>A beautiful, colorful AI chat space for brainstorming, learning, writing, coding, and turning your ideas into action.</p>
      <div class="feature-row">
        <span class="feature-pill">✍️ Writing & ideas</span>
        <span class="feature-pill">💻 Coding help</span>
        <span class="feature-pill">🧠 Learn anything</span>
        <span class="feature-pill">🌈 Your own AI space</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">🔑 Connect your OpenAI API key</div><div class="panel-copy">Add your personal API key to unlock the chat. Your key is used to make requests from this app and is kept in session memory only.</div>', unsafe_allow_html=True)
    with st.form("connect_form", clear_on_submit=False):
        api_key_input = st.text_input(
            "OpenAI API key",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="Create or manage your key in the official OpenAI platform. Never share your key publicly."
        )
        show_model = st.selectbox("Starting model", ["gpt-5.2", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"])
        submitted = st.form_submit_button("✨  Unlock my AI chat", use_container_width=True)
        if submitted:
            if not api_key_input.strip():
                st.error("Please paste your OpenAI API key first.")
            else:
                st.session_state.api_key = api_key_input.strip()
                st.session_state.model_name = show_model
                new_chat()
                st.rerun()
    st.markdown('<div class="small-note">🔒 This is an independent app using the OpenAI API — it is not the official ChatGPT website. API usage may incur charges on your OpenAI account.</div></div>', unsafe_allow_html=True)
    st.stop()

# ------------------------------ Chat screen ------------------------------
if st.session_state.active_chat not in st.session_state.chats:
    new_chat()

active = st.session_state.chats[st.session_state.active_chat]
st.markdown("""
<div class="chat-heading">
  <div class="mini-orb">🤖</div>
  <div><h2>IQRA AI</h2><p>Your ideas, with a little more magic ✨</p></div>
</div>
""", unsafe_allow_html=True)

if not active["messages"]:
    st.markdown("""
    <div style="text-align:center;padding:8vh 12px 5vh;">
      <div style="font-size:39px;animation:floaty 3s ease-in-out infinite;">🌷 💫 🌷</div>
      <h2 style="font-family:'Space Grotesk',sans-serif;color:#342950;font-size:30px;margin:16px 0 8px;">What shall we create today?</h2>
      <p style="color:#837c9b;">Ask a question, explore an idea, or start something new.</p>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(3)
    suggestions = [
        ("✍️  Write something", "Help me write a clear, friendly email."),
        ("💻  Build with code", "Explain Python functions with a simple example."),
        ("🧠  Learn a topic", "Teach me an interesting concept step by step."),
    ]
    for col, (label, prompt) in zip(cols, suggestions):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()

for message in active["messages"]:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
        st.markdown(message.content)

prompt = st.chat_input("Message IQRA AI…")
if not prompt and st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    active["messages"].append(HumanMessage(content=prompt))
    if active["title"] == "New conversation":
        active["title"] = prompt.strip().replace("\n", " ")[:30] or "New conversation"

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            with st.spinner("✨ Thinking…"):
                chat_model = ChatOpenAI(
                    model=st.session_state.model_name,
                    temperature=st.session_state.temperature,
                    api_key=st.session_state.api_key,
                    streaming=True,
                )
                messages = [SystemMessage(content=st.session_state.system_role)] + active["messages"]
                answer = st.write_stream(
                    chunk.content for chunk in chat_model.stream(messages)
                    if isinstance(chunk.content, str) and chunk.content
                )
            active["messages"].append(AIMessage(content=answer))
        except Exception as exc:
            error_text = str(exc)
            st.error("I couldn't complete that request. Check your API key, model access, and API billing, then try again.")
            with st.expander("Technical details"):
                st.code(error_text)
    st.rerun()

st.markdown('<div class="small-note">IQRA AI can make mistakes. Check important information. Your API usage is billed by OpenAI according to your account and model.</div>', unsafe_allow_html=True)
