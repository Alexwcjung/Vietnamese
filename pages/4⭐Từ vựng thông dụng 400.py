import streamlit as st
from urllib.parse import quote
import requests
import hashlib
import random
import re
import html
import base64
import json
import uuid
import streamlit.components.v1 as components

# =====================================================
# Daily English 400 - 단어 동기화 카세트 버전
# 핵심 구조:
# 1) gTTS 제거
# 2) requests로 Google TTS mp3를 직접 받아오기
# 3) 단어별 mp3가 끝날 때 다음 단어로 이동
# 4) 현재 단어, 뜻, 이모지를 화면에 크게 동기화 표시
# =====================================================

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Daily English 400",
    page_icon="🌱",
    layout="wide"
)

# =========================
# CSS 디자인
# =========================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 44px;
        font-weight: 900;
        color: #1f2937;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 24px;
    }

    .hero-box {
        background: linear-gradient(135deg, #dcfce7 0%, #e0f2fe 50%, #fef3c7 100%);
        border-radius: 26px;
        padding: 28px 30px;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.8);
    }

    .hero-title {
        font-size: 27px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 10px;
    }

    .hero-text {
        font-size: 14px;
        color: #374151;
        line-height: 1.8;
    }

    .theme-header {
        background: linear-gradient(135deg, #22c55e 0%, #0ea5e9 50%, #8b5cf6 100%);
        color: white;
        padding: 22px 26px;
        border-radius: 24px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(34,197,94,0.25);
    }

    .theme-title {
        font-size: 27px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .theme-desc {
        font-size: 15px;
        opacity: 0.95;
    }

    .dialogue-box {
        background: #fefce8;
        border: 1px solid #fde68a;
        border-radius: 24px;
        padding: 20px 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .dialogue-title {
        font-size: 16px;
        font-weight: 900;
        color: #854d0e;
        margin-bottom: 14px;
    }

    .dialogue-line {
        font-size: 18px;
        font-weight: 900;
        color: #111827;
        margin-top: 10px;
    }

    .dialogue-meaning {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 5px;
    }

    .word-card {
        background: white;
        border-radius: 18px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border: 1px solid #dcfce7;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    .word-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .word-number {
        min-width: 38px;
        font-size: 13px;
        font-weight: 900;
        color: #166534;
        background: #dcfce7;
        border-radius: 999px;
        padding: 5px 9px;
        text-align: center;
    }

    .word-text {
        min-width: 170px;
        font-size: 25px;
        font-weight: 900;
        color: #111827;
    }

    .meaning-text {
        font-size: 19px;
        font-weight: 800;
        color: #374151;
        margin-left: 8px;
    }

    .emoji-text {
        font-size: 25px;
        line-height: 1;
        text-align: center;
        padding-top: 2px;
    }

    .quiz-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 22px 24px;
        margin-bottom: 18px;
        border: 1px solid #dbeafe;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }

    .quiz-number {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .quiz-word {
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 8px;
    }

    .score-box {
        background: linear-gradient(135deg, #dcfce7 0%, #dbeafe 50%, #fce7f3 100%);
        border-radius: 24px;
        padding: 24px 26px;
        margin: 20px 0;
        border: 1px solid #bbf7d0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .score-title {
        font-size: 27px;
        font-weight: 900;
        color: #14532d;
    }

    .wrong-box {
        background: #fff7ed;
        border-left: 6px solid #fb923c;
        border-radius: 18px;
        padding: 16px 18px;
        margin: 18px 0;
        color: #7c2d12;
        font-weight: 700;
    }

    .answer-box {
        background: #f8fafc;
        border-radius: 20px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }


    .cassette-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 50%, #fff7ed 100%);
        border: 1px solid #bbf7d0;
        border-radius: 28px;
        padding: 28px 30px;
        margin: 22px 0 22px 0;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    }

    .cassette-title {
        font-size: 36px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 0px;
        line-height: 1.25;
        letter-spacing: -0.5px;
    }

    .cassette-text {
        display: none;
    }

    h2, h3 {
        font-weight: 1000 !important;
    }

    div[data-testid="stRadio"] > label {
        font-weight: 800;
        color: #374151;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 1000;
        border: 1px solid #bbf7d0;
        padding: 1.15rem 1.45rem;
        min-height: 84px;
        font-size: 30px;
        box-shadow: 0 6px 16px rgba(34,197,94,0.16);
    }

    .stButton > button:hover {
        border-color: #22c55e;
        color: #22c55e;
    }


    /* 카테고리 탭 크게 보이게 */
    div[data-testid="stTabs"] button[role="tab"] {
        min-height: 58px !important;
        padding: 10px 16px !important;
        border-radius: 18px 18px 0 0 !important;
    }

    div[data-testid="stTabs"] button[role="tab"] p {
        font-size: 21px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #dcfce7, #dbeafe, #fef3c7) !important;
        border-radius: 18px 18px 0 0 !important;
    }

    .theme-header {
        padding: 30px 34px !important;
        border-radius: 30px !important;
    }

    .theme-title {
        font-size: 38px !important;
        line-height: 1.2 !important;
    }

    .theme-desc {
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    @media (max-width: 520px) {
        div[data-testid="stTabs"] button[role="tab"] {
            min-height: 50px !important;
            padding: 8px 11px !important;
        }
        div[data-testid="stTabs"] button[role="tab"] p {
            font-size: 17px !important;
        }
        .theme-title {
            font-size: 30px !important;
        }
        .theme-desc {
            font-size: 15px !important;
        }
        .cassette-title {
            font-size: 29px !important;
        }
        .stButton > button {
            min-height: 72px;
            font-size: 27px;
            padding: 0.95rem 1.15rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 상단 제목
# =========================
st.markdown("<div class='main-title'>🌱 Daily English 400</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>기초 일상대화에 필요한 단어와 문장을 듣고 읽어 봅시다.</div>",
    unsafe_allow_html=True
)

# =========================
# 뜻 언어 선택
# =========================
meaning_language = st.radio(
    "뜻 언어 선택",
    ["한국어 Korean", "베트남어 Vietnamese"],
    horizontal=True,
    key="daily400_meaning_language"
)

st.caption("영어 단어와 영어 듣기는 그대로 두고, 뜻만 선택한 언어로 보여줍니다.")

# =========================
# TTS 함수 - gTTS 대신 requests 사용
# =========================
def make_google_tts_url(text, lang="en"):
    clean_text = str(text).strip()
    if not clean_text:
        clean_text = "Hello"
    encoded = quote(clean_text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded}"


@st.cache_data(show_spinner=False)
def get_tts_mp3_bytes(text, lang="en"):
    """Google TTS mp3를 requests로 직접 받아와 st.audio에서 재생합니다."""
    clean_text = str(text).strip()
    if not clean_text:
        clean_text = "Hello"

    url = make_google_tts_url(clean_text, lang=lang)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://translate.google.com/",
    }
    response = requests.get(url, headers=headers, timeout=12)
    response.raise_for_status()

    audio_bytes = response.content
    if not audio_bytes or len(audio_bytes) < 500:
        raise ValueError("음성 파일이 비어 있습니다.")
    return audio_bytes


def make_tts_audio(text, lang="en", tld="com"):
    """기존 코드 호환용 함수입니다."""
    return get_tts_mp3_bytes(text, lang=lang)


def remove_speaker_label(sentence):
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(dialogue):
    return " ".join([remove_speaker_label(item["en"]) for item in dialogue])


def play_audio_block(text, label="🔊 듣기", show_link=True, key=None):
    text = str(text).strip()
    if not text:
        return

    if key is None:
        key = "audio_" + hashlib.md5((label + "::" + text).encode("utf-8")).hexdigest()

    if st.button(label, key=key, use_container_width=True):
        try:
            audio_bytes = get_tts_mp3_bytes(text, lang="en")
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error("음성 파일을 만들지 못했습니다. requirements.txt에 requests가 있는지 확인해 주세요.")
            st.caption(f"오류 내용: {e}")
            if show_link:
                st.link_button("🔊 새 창에서 듣기", make_google_tts_url(text, lang="en"), use_container_width=True)


def direct_audio_player(text, show_link=True):
    """단어 카드용: 오디오 플레이어를 바로 보여줍니다."""
    text = str(text).strip()
    if not text:
        return

    try:
        audio_bytes = get_tts_mp3_bytes(text, lang="en")
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("음성 파일을 만들지 못했습니다.")
        st.caption(f"오류 내용: {e}")
        if show_link:
            st.link_button("🔊 새 창에서 듣기", make_google_tts_url(text, lang="en"), use_container_width=True)


def get_word_emoji(word):
    """단어별로 최대한 어울리는 이모지를 붙입니다."""
    emoji_map = {
        # 학교생활
        "subject": "📚", "math": "➗", "science": "🔬", "history": "🏛️", "music": "🎵",
        "art": "🎨", "P.E.": "🏃", "club": "👥", "schedule": "🗓️", "semester": "🏫",
        "assignment": "📝", "project": "📁", "presentation": "🗣️", "report": "📄", "textbook": "📘",
        "workbook": "📗", "library": "📚", "cafeteria": "🍽️", "hallway": "🚶", "attendance": "✅",

        # 교실 활동
        "copy": "✍️", "repeat": "🔁", "underline": "〽️", "circle": "⭕", "choose": "☝️",
        "check": "✅", "match": "🧩", "complete": "🏁", "fill": "🖊️", "spell": "🔤",
        "pronounce": "🗣️", "review": "🔎", "explain": "💬", "describe": "🖼️", "compare": "⚖️",
        "discuss": "🗨️", "present": "📢", "take notes": "📝", "turn in": "📥", "hand out": "📤",

        # 집과 생활
        "living room": "🛋️", "bedroom": "🛏️", "kitchen": "🍳", "balcony": "🌇", "floor": "🧱",
        "wall": "🧱", "roof": "🏠", "garden": "🌷", "yard": "🌳", "sofa": "🛋️",
        "television": "📺", "refrigerator": "🧊", "microwave": "♨️", "blanket": "🛌", "pillow": "🛏️",
        "towel": "🧺", "soap": "🧼", "mirror": "🪞", "closet": "🚪", "trash": "🗑️",

        # 하루 일과
        "routine": "🔄", "wake up": "⏰", "get up": "🌅", "brush": "🪥", "shower": "🚿",
        "dress": "👕", "leave": "🚪", "arrive": "📍", "return": "↩️", "finish": "🏁",
        "relax": "😌", "weekday": "📅", "weekend": "🎉", "usually": "🔁", "often": "🔂",
        "sometimes": "🤔", "always": "♾️", "never": "🚫", "habit": "🔁", "lifestyle": "🌿",

        # 취미와 여가
        "hobby": "🎯", "movie": "🎬", "drama": "📺", "song": "🎵", "concert": "🎤",
        "dance": "💃", "drawing": "✏️", "painting": "🖌️", "comic": "💬", "novel": "📖",
        "photography": "📷", "cooking": "🍳", "baking": "🍞", "camping": "⛺", "hiking": "🥾",
        "fishing": "🎣", "free time": "🕒", "favorite": "⭐", "popular": "🔥", "relaxing": "😌",

        # 운동과 활동
        "soccer": "⚽", "baseball": "⚾", "basketball": "🏀", "volleyball": "🏐", "tennis": "🎾",
        "badminton": "🏸", "swimming": "🏊", "cycling": "🚴", "skating": "⛸️", "boxing": "🥊",
        "taekwondo": "🥋", "yoga": "🧘", "fitness": "💪", "field": "🏟️", "court": "🎾",
        "stadium": "🏟️", "coach": "📣", "match": "🏆", "competition": "🏁", "medal": "🏅",

        # 날씨와 계절
        "season": "🍂", "spring": "🌸", "summer": "☀️", "fall": "🍁", "winter": "❄️",
        "cloudy": "☁️", "rainy": "🌧️", "snowy": "🌨️", "windy": "🌬️", "stormy": "⛈️",
        "foggy": "🌫️", "dry": "🏜️", "wet": "💦", "humid": "💧", "temperature": "🌡️",
        "degree": "🌡️", "forecast": "📡", "umbrella": "☂️", "raincoat": "🧥", "rainbow": "🌈",

        # 자연과 환경
        "nature": "🌿", "environment": "🌎", "plant": "🌱", "forest": "🌲", "lake": "🏞️",
        "ocean": "🌊", "island": "🏝️", "desert": "🏜️", "farm": "🚜", "village": "🏘️",
        "leaf": "🍃", "root": "🌱", "stone": "🪨", "sand": "🏖️", "soil": "🌱",
        "plastic": "🥤", "recycle": "♻️", "protect": "🛡️", "pollution": "🏭",

        # 식당과 주문
        "restaurant": "🍽️", "menu": "📋", "seat": "💺", "waiter": "🤵", "waitress": "🤵‍♀️",
        "order": "🛎️", "dish": "🍛", "meal": "🍽️", "soup": "🍲", "salad": "🥗",
        "steak": "🥩", "pizza": "🍕", "pasta": "🍝", "burger": "🍔", "sandwich": "🥪",
        "dessert": "🍰", "spicy": "🌶️", "sweet": "🍬", "bill": "🧾", "receipt": "🧾",

        # 쇼핑과 가격
        "shop": "🏪", "market": "🛒", "mall": "🏬", "supermarket": "🛒", "cashier": "💁",
        "customer": "🧑", "price": "💰", "sale": "🏷️", "discount": "🔻", "coupon": "🎟️",
        "change": "💵", "coin": "🪙", "expensive": "💸", "cheap": "👍", "size": "📏",
        "color": "🎨", "brand": "🏷️", "exchange": "🔄", "refund": "↩️",

        # 옷과 외모
        "T-shirt": "👕", "pants": "👖", "jeans": "👖", "shorts": "🩳", "skirt": "👗",
        "dress": "👗", "jacket": "🧥", "coat": "🧥", "sweater": "🧶", "hoodie": "🧥",
        "uniform": "🎽", "socks": "🧦", "sneakers": "👟", "boots": "🥾", "sandals": "🩴",
        "scarf": "🧣", "gloves": "🧤", "belt": "👖", "glasses": "👓", "comfortable": "😌",

        # 교통과 길 찾기
        "bus stop": "🚏", "subway": "🚇", "airport": "✈️", "terminal": "🚌", "platform": "🚉",
        "route": "🗺️", "direction": "➡️", "straight": "⬆️", "corner": "↪️", "block": "🏙️",
        "traffic": "🚦", "crosswalk": "🚸", "sidewalk": "🚶", "bridge": "🌉", "tunnel": "🚇",
        "entrance": "🚪", "exit": "🚪", "transfer": "🔁", "lost": "😵", "guide": "🧭",

        # 여행과 숙박
        "travel": "✈️", "trip": "🧳", "vacation": "🏖️", "tourist": "📸", "passport": "🛂",
        "flight": "🛫", "hotel": "🏨", "motel": "🏩", "hostel": "🛏️", "reservation": "📅",
        "check in": "🔑", "check out": "👋", "luggage": "🧳", "suitcase": "🧳", "backpack": "🎒",
        "souvenir": "🎁", "museum": "🏛️", "famous": "⭐", "local": "📍",

        # 친구 관계
        "friendship": "🤝", "best friend": "👯", "teammate": "👥", "partner": "🤝", "message": "💬",
        "call": "📞", "chat": "💬", "invite": "✉️", "visit": "🏠", "meet": "🤝",
        "hang out": "🎉", "laugh": "😂", "share": "🤲", "trust": "🤝", "promise": "🤞",
        "secret": "🤫", "joke": "😄", "together": "👥", "alone": "🚶", "forgive": "🫶",

        # 감정 표현 확장
        "excited": "🤩", "nervous": "😬", "bored": "🥱", "surprised": "😲", "confused": "😕",
        "embarrassed": "😳", "proud": "😊", "disappointed": "😞", "lonely": "🥲", "relaxed": "😌",
        "calm": "🧘", "upset": "😟", "interested": "🧐", "satisfied": "😌", "thankful": "🙏",
        "hopeful": "🌟", "mood": "🙂", "stress": "😣", "confidence": "💪", "courage": "🦁",

        # 생각과 의견
        "think": "💭", "believe": "🙏", "guess": "🤔", "remember": "🧠", "forget": "💨",
        "mean": "💡", "agree": "👍", "disagree": "👎", "opinion": "💬", "idea": "💡",
        "reason": "❓", "example": "🔎", "fact": "✅", "choice": "☝️", "decision": "✅",
        "advice": "💡", "suggestion": "💬", "possible": "✅", "impossible": "🚫", "confusing": "😵",

        # 계획과 약속
        "plan": "📝", "appointment": "📅", "meeting": "👥", "date": "📆", "event": "🎪",
        "party": "🎉", "festival": "🎊", "deadline": "⏳", "calendar": "📅", "next week": "➡️",
        "join": "🙋", "prepare": "🎒", "decide": "✅", "cancel": "❌", "on time": "⏰",
        "available": "🟢", "reminder": "🔔",

        # 건강한 생활
        "health": "🩺", "body": "🧍", "eye": "👁️", "ear": "👂", "nose": "👃",
        "mouth": "👄", "tooth": "🦷", "hand": "✋", "arm": "💪", "leg": "🦵",
        "foot": "🦶", "stomach": "🤰", "back": "🔙", "heart": "❤️", "clinic": "🏥",
        "vitamin": "💊", "diet": "🥗", "cough": "😷", "flu": "🤒", "breathe": "🌬️",

        # 미디어와 스마트폰
        "smartphone": "📱", "screen": "🖥️", "app": "📲", "website": "🌐", "internet": "🌐",
        "Wi-Fi": "📶", "password": "🔐", "text": "💬", "video call": "📹", "gallery": "🖼️",
        "news": "📰", "channel": "📺", "post": "📝", "comment": "💬", "upload": "⬆️",
        "download": "⬇️", "search": "🔎", "click": "🖱️", "battery": "🔋", "notification": "🔔",

        # 직업과 미래
        "job": "💼", "work": "💼", "company": "🏢", "office": "🏢", "factory": "🏭",
        "engineer": "🛠️", "mechanic": "🔧", "chef": "👨‍🍳", "firefighter": "🚒", "farmer": "🚜",
        "designer": "🎨", "singer": "🎤", "actor": "🎭", "athlete": "🏃", "dream": "🌈",
        "future": "🔮", "goal": "🎯", "skill": "🛠️", "interview": "🎙️", "experience": "🌱",
    }
    return emoji_map.get(word, "🌱")



# =========================
# 복습 희망 저장 기능
# =========================
if "unknown_words" not in st.session_state:
    st.session_state.unknown_words = []

if "unknown_word_info" not in st.session_state:
    st.session_state.unknown_word_info = {}


def make_review_id(theme_name, word):
    """
    Daily English 400에는 같은 단어가 여러 테마에 나올 수 있으므로
    내부 저장은 '테마||단어' 기준으로 구분합니다.
    """
    return f"{theme_name}||{word}"


def add_unknown_word(word, meaning, theme_name):
    review_id = make_review_id(theme_name, word)

    if review_id not in st.session_state.unknown_words:
        st.session_state.unknown_words.append(review_id)

    st.session_state.unknown_word_info[review_id] = {
        "word": word,
        "meaning": meaning,
        "theme": theme_name,
    }


def remove_unknown_word(review_id):
    if review_id in st.session_state.unknown_words:
        st.session_state.unknown_words.remove(review_id)

    if review_id in st.session_state.unknown_word_info:
        del st.session_state.unknown_word_info[review_id]


def clear_review_checkbox_keys():
    keys_to_delete = [
        key for key in list(st.session_state.keys())
        if "_unknown_" in str(key)
    ]

    for key in keys_to_delete:
        del st.session_state[key]


# =========================
# 단어·대화 오디오
# =========================
def audio_button(label, text, key=None):
    # 버튼을 한 번 더 거치지 않고 오디오 플레이어를 바로 보여줍니다.
    direct_audio_player(text)


def html_dialogue_audio_player(label, dialogue_lines, line_pause_ms=1400, height=105):
    # 기존 함수 이름은 유지하되, 내부는 안정적인 st.audio 방식으로 바꿉니다.
    dialogue_text = make_dialogue_tts_text(dialogue_lines)
    play_audio_block(dialogue_text, label=label, key="dialogue_" + hashlib.md5(dialogue_text.encode("utf-8")).hexdigest())


# =========================
# Daily English 400 통합 카테고리별 단어
# =========================
word_themes = {
    "🏫 학교생활": [
        {"word": "subject", "meaning": "과목"},
        {"word": "math", "meaning": "수학"},
        {"word": "science", "meaning": "과학"},
        {"word": "history", "meaning": "역사"},
        {"word": "music", "meaning": "음악"},
        {"word": "art", "meaning": "미술"},
        {"word": "P.E.", "meaning": "체육"},
        {"word": "club", "meaning": "동아리"},
        {"word": "schedule", "meaning": "일정표"},
        {"word": "semester", "meaning": "학기"},
        {"word": "assignment", "meaning": "과제"},
        {"word": "project", "meaning": "프로젝트"},
        {"word": "presentation", "meaning": "발표"},
        {"word": "report", "meaning": "보고서"},
        {"word": "textbook", "meaning": "교과서"},
        {"word": "workbook", "meaning": "문제집"},
        {"word": "library", "meaning": "도서관"},
        {"word": "cafeteria", "meaning": "급식소, 식당"},
        {"word": "hallway", "meaning": "복도"},
        {"word": "attendance", "meaning": "출석"}],

    "✏️ 교실 활동": [
        {"word": "copy", "meaning": "베껴 쓰다"},
        {"word": "repeat", "meaning": "반복하다"},
        {"word": "underline", "meaning": "밑줄 치다"},
        {"word": "circle", "meaning": "동그라미 치다"},
        {"word": "choose", "meaning": "고르다"},
        {"word": "check", "meaning": "확인하다"},
        {"word": "match", "meaning": "연결하다, 맞추다"},
        {"word": "complete", "meaning": "완성하다"},
        {"word": "fill", "meaning": "채우다"},
        {"word": "spell", "meaning": "철자를 말하다"},
        {"word": "pronounce", "meaning": "발음하다"},
        {"word": "review", "meaning": "복습하다"},
        {"word": "explain", "meaning": "설명하다"},
        {"word": "describe", "meaning": "묘사하다"},
        {"word": "compare", "meaning": "비교하다"},
        {"word": "discuss", "meaning": "토론하다"},
        {"word": "present", "meaning": "발표하다"},
        {"word": "take notes", "meaning": "필기하다"},
        {"word": "turn in", "meaning": "제출하다"},
        {"word": "hand out", "meaning": "나누어 주다"}],

    "🏠 집과 생활": [
        {"word": "living room", "meaning": "거실"},
        {"word": "bedroom", "meaning": "침실"},
        {"word": "kitchen", "meaning": "부엌"},
        {"word": "balcony", "meaning": "발코니"},
        {"word": "floor", "meaning": "바닥, 층"},
        {"word": "wall", "meaning": "벽"},
        {"word": "roof", "meaning": "지붕"},
        {"word": "garden", "meaning": "정원"},
        {"word": "yard", "meaning": "마당"},
        {"word": "sofa", "meaning": "소파"},
        {"word": "television", "meaning": "텔레비전"},
        {"word": "refrigerator", "meaning": "냉장고"},
        {"word": "microwave", "meaning": "전자레인지"},
        {"word": "blanket", "meaning": "담요"},
        {"word": "pillow", "meaning": "베개"},
        {"word": "towel", "meaning": "수건"},
        {"word": "soap", "meaning": "비누"},
        {"word": "mirror", "meaning": "거울"},
        {"word": "closet", "meaning": "옷장"},
        {"word": "trash", "meaning": "쓰레기"}],

    "🌅 하루 일과": [
        {"word": "routine", "meaning": "일과"},
        {"word": "wake up", "meaning": "잠에서 깨다"},
        {"word": "get up", "meaning": "일어나다"},
        {"word": "brush", "meaning": "닦다"},
        {"word": "shower", "meaning": "샤워하다"},
        {"word": "dress", "meaning": "옷을 입다"},
        {"word": "leave", "meaning": "떠나다"},
        {"word": "arrive", "meaning": "도착하다"},
        {"word": "return", "meaning": "돌아오다"},
        {"word": "finish", "meaning": "끝내다"},
        {"word": "relax", "meaning": "쉬다"},
        {"word": "weekday", "meaning": "평일"},
        {"word": "weekend", "meaning": "주말"},
        {"word": "usually", "meaning": "보통"},
        {"word": "often", "meaning": "자주"},
        {"word": "sometimes", "meaning": "가끔"},
        {"word": "always", "meaning": "항상"},
        {"word": "never", "meaning": "절대 ~않다"},
        {"word": "habit", "meaning": "습관"},
        {"word": "lifestyle", "meaning": "생활 방식"}],

    "🎮 취미와 여가": [
        {"word": "hobby", "meaning": "취미"},
        {"word": "movie", "meaning": "영화"},
        {"word": "drama", "meaning": "드라마"},
        {"word": "song", "meaning": "노래"},
        {"word": "concert", "meaning": "콘서트"},
        {"word": "dance", "meaning": "춤"},
        {"word": "drawing", "meaning": "그림 그리기"},
        {"word": "painting", "meaning": "그림, 회화"},
        {"word": "comic", "meaning": "만화"},
        {"word": "novel", "meaning": "소설"},
        {"word": "photography", "meaning": "사진 촬영"},
        {"word": "cooking", "meaning": "요리"},
        {"word": "baking", "meaning": "빵 굽기"},
        {"word": "camping", "meaning": "캠핑"},
        {"word": "hiking", "meaning": "하이킹"},
        {"word": "fishing", "meaning": "낚시"},
        {"word": "free time", "meaning": "여가 시간"},
        {"word": "favorite", "meaning": "가장 좋아하는"},
        {"word": "popular", "meaning": "인기 있는"},
        {"word": "relaxing", "meaning": "편안한"}],

    "⚽ 운동과 활동": [
        {"word": "soccer", "meaning": "축구"},
        {"word": "baseball", "meaning": "야구"},
        {"word": "basketball", "meaning": "농구"},
        {"word": "volleyball", "meaning": "배구"},
        {"word": "tennis", "meaning": "테니스"},
        {"word": "badminton", "meaning": "배드민턴"},
        {"word": "swimming", "meaning": "수영"},
        {"word": "cycling", "meaning": "자전거 타기"},
        {"word": "skating", "meaning": "스케이트 타기"},
        {"word": "boxing", "meaning": "복싱"},
        {"word": "taekwondo", "meaning": "태권도"},
        {"word": "yoga", "meaning": "요가"},
        {"word": "fitness", "meaning": "체력 운동"},
        {"word": "field", "meaning": "경기장, 들판"},
        {"word": "court", "meaning": "코트"},
        {"word": "stadium", "meaning": "경기장"},
        {"word": "coach", "meaning": "코치"},
        {"word": "match", "meaning": "경기"},
        {"word": "competition", "meaning": "대회"},
        {"word": "medal", "meaning": "메달"}],

    "🌦️ 날씨와 계절": [
        {"word": "season", "meaning": "계절"},
        {"word": "spring", "meaning": "봄"},
        {"word": "summer", "meaning": "여름"},
        {"word": "fall", "meaning": "가을"},
        {"word": "winter", "meaning": "겨울"},
        {"word": "cloudy", "meaning": "흐린"},
        {"word": "rainy", "meaning": "비 오는"},
        {"word": "snowy", "meaning": "눈 오는"},
        {"word": "windy", "meaning": "바람 부는"},
        {"word": "stormy", "meaning": "폭풍우 치는"},
        {"word": "foggy", "meaning": "안개 낀"},
        {"word": "dry", "meaning": "건조한"},
        {"word": "wet", "meaning": "젖은"},
        {"word": "humid", "meaning": "습한"},
        {"word": "temperature", "meaning": "온도"},
        {"word": "degree", "meaning": "도"},
        {"word": "forecast", "meaning": "일기예보"},
        {"word": "umbrella", "meaning": "우산"},
        {"word": "raincoat", "meaning": "비옷"},
        {"word": "rainbow", "meaning": "무지개"}],

    "🌳 자연과 환경": [
        {"word": "nature", "meaning": "자연"},
        {"word": "environment", "meaning": "환경"},
        {"word": "plant", "meaning": "식물"},
        {"word": "forest", "meaning": "숲"},
        {"word": "lake", "meaning": "호수"},
        {"word": "ocean", "meaning": "대양"},
        {"word": "island", "meaning": "섬"},
        {"word": "desert", "meaning": "사막"},
        {"word": "field", "meaning": "들판"},
        {"word": "farm", "meaning": "농장"},
        {"word": "village", "meaning": "마을"},
        {"word": "leaf", "meaning": "잎"},
        {"word": "root", "meaning": "뿌리"},
        {"word": "stone", "meaning": "돌"},
        {"word": "sand", "meaning": "모래"},
        {"word": "soil", "meaning": "흙"},
        {"word": "plastic", "meaning": "플라스틱"},
        {"word": "recycle", "meaning": "재활용하다"},
        {"word": "protect", "meaning": "보호하다"},
        {"word": "pollution", "meaning": "오염"}],

    "🍽️ 식당과 주문": [
        {"word": "restaurant", "meaning": "식당"},
        {"word": "menu", "meaning": "메뉴"},
        {"word": "seat", "meaning": "자리"},
        {"word": "waiter", "meaning": "남자 종업원"},
        {"word": "waitress", "meaning": "여자 종업원"},
        {"word": "order", "meaning": "주문하다"},
        {"word": "dish", "meaning": "요리, 접시"},
        {"word": "meal", "meaning": "식사"},
        {"word": "soup", "meaning": "수프"},
        {"word": "salad", "meaning": "샐러드"},
        {"word": "steak", "meaning": "스테이크"},
        {"word": "pizza", "meaning": "피자"},
        {"word": "pasta", "meaning": "파스타"},
        {"word": "burger", "meaning": "버거"},
        {"word": "sandwich", "meaning": "샌드위치"},
        {"word": "dessert", "meaning": "디저트"},
        {"word": "spicy", "meaning": "매운"},
        {"word": "sweet", "meaning": "단"},
        {"word": "bill", "meaning": "계산서"},
        {"word": "receipt", "meaning": "영수증"}],

    "🛍️ 쇼핑과 가격": [
        {"word": "shop", "meaning": "가게"},
        {"word": "market", "meaning": "시장"},
        {"word": "mall", "meaning": "쇼핑몰"},
        {"word": "supermarket", "meaning": "슈퍼마켓"},
        {"word": "cashier", "meaning": "계산원"},
        {"word": "customer", "meaning": "손님"},
        {"word": "price", "meaning": "가격"},
        {"word": "sale", "meaning": "할인 판매"},
        {"word": "discount", "meaning": "할인"},
        {"word": "coupon", "meaning": "쿠폰"},
        {"word": "change", "meaning": "거스름돈"},
        {"word": "coin", "meaning": "동전"},
        {"word": "bill", "meaning": "지폐, 계산서"},
        {"word": "expensive", "meaning": "비싼"},
        {"word": "cheap", "meaning": "싼"},
        {"word": "size", "meaning": "크기"},
        {"word": "color", "meaning": "색깔"},
        {"word": "brand", "meaning": "상표"},
        {"word": "exchange", "meaning": "교환하다"},
        {"word": "refund", "meaning": "환불"}],

    "👕 옷과 외모": [
        {"word": "T-shirt", "meaning": "티셔츠"},
        {"word": "pants", "meaning": "바지"},
        {"word": "jeans", "meaning": "청바지"},
        {"word": "shorts", "meaning": "반바지"},
        {"word": "skirt", "meaning": "치마"},
        {"word": "dress", "meaning": "드레스, 원피스"},
        {"word": "jacket", "meaning": "재킷"},
        {"word": "coat", "meaning": "코트"},
        {"word": "sweater", "meaning": "스웨터"},
        {"word": "hoodie", "meaning": "후드티"},
        {"word": "uniform", "meaning": "교복, 제복"},
        {"word": "socks", "meaning": "양말"},
        {"word": "sneakers", "meaning": "운동화"},
        {"word": "boots", "meaning": "부츠"},
        {"word": "sandals", "meaning": "샌들"},
        {"word": "scarf", "meaning": "목도리"},
        {"word": "gloves", "meaning": "장갑"},
        {"word": "belt", "meaning": "벨트"},
        {"word": "glasses", "meaning": "안경"},
        {"word": "comfortable", "meaning": "편안한"}],

    "🚇 교통과 길 찾기": [
        {"word": "bus stop", "meaning": "버스 정류장"},
        {"word": "subway", "meaning": "지하철"},
        {"word": "airport", "meaning": "공항"},
        {"word": "terminal", "meaning": "터미널"},
        {"word": "platform", "meaning": "승강장"},
        {"word": "route", "meaning": "경로"},
        {"word": "direction", "meaning": "방향"},
        {"word": "straight", "meaning": "똑바로"},
        {"word": "corner", "meaning": "모퉁이"},
        {"word": "block", "meaning": "구역, 블록"},
        {"word": "traffic", "meaning": "교통"},
        {"word": "crosswalk", "meaning": "횡단보도"},
        {"word": "sidewalk", "meaning": "인도"},
        {"word": "bridge", "meaning": "다리"},
        {"word": "tunnel", "meaning": "터널"},
        {"word": "entrance", "meaning": "입구"},
        {"word": "exit", "meaning": "출구"},
        {"word": "transfer", "meaning": "갈아타다"},
        {"word": "lost", "meaning": "길을 잃은"},
        {"word": "guide", "meaning": "안내하다, 안내자"}],

    "🧳 여행과 숙박": [
        {"word": "travel", "meaning": "여행하다"},
        {"word": "trip", "meaning": "여행"},
        {"word": "vacation", "meaning": "방학, 휴가"},
        {"word": "tourist", "meaning": "관광객"},
        {"word": "guide", "meaning": "안내자"},
        {"word": "passport", "meaning": "여권"},
        {"word": "flight", "meaning": "항공편"},
        {"word": "hotel", "meaning": "호텔"},
        {"word": "motel", "meaning": "모텔"},
        {"word": "hostel", "meaning": "호스텔"},
        {"word": "reservation", "meaning": "예약"},
        {"word": "check in", "meaning": "체크인하다"},
        {"word": "check out", "meaning": "체크아웃하다"},
        {"word": "luggage", "meaning": "짐"},
        {"word": "suitcase", "meaning": "여행 가방"},
        {"word": "backpack", "meaning": "배낭"},
        {"word": "souvenir", "meaning": "기념품"},
        {"word": "museum", "meaning": "박물관"},
        {"word": "famous", "meaning": "유명한"},
        {"word": "local", "meaning": "현지의"}],

    "👥 친구 관계": [
        {"word": "friendship", "meaning": "우정"},
        {"word": "best friend", "meaning": "가장 친한 친구"},
        {"word": "teammate", "meaning": "팀 동료"},
        {"word": "partner", "meaning": "짝, 파트너"},
        {"word": "message", "meaning": "메시지"},
        {"word": "call", "meaning": "전화하다"},
        {"word": "chat", "meaning": "채팅하다"},
        {"word": "invite", "meaning": "초대하다"},
        {"word": "visit", "meaning": "방문하다"},
        {"word": "meet", "meaning": "만나다"},
        {"word": "hang out", "meaning": "어울려 놀다"},
        {"word": "laugh", "meaning": "웃다"},
        {"word": "share", "meaning": "나누다, 공유하다"},
        {"word": "trust", "meaning": "믿다"},
        {"word": "promise", "meaning": "약속"},
        {"word": "secret", "meaning": "비밀"},
        {"word": "joke", "meaning": "농담"},
        {"word": "together", "meaning": "함께"},
        {"word": "alone", "meaning": "혼자"},
        {"word": "forgive", "meaning": "용서하다"}],

    "😊 감정 표현 확장": [
        {"word": "excited", "meaning": "신난"},
        {"word": "nervous", "meaning": "긴장한"},
        {"word": "bored", "meaning": "지루한"},
        {"word": "surprised", "meaning": "놀란"},
        {"word": "confused", "meaning": "혼란스러운"},
        {"word": "embarrassed", "meaning": "당황한"},
        {"word": "proud", "meaning": "자랑스러운"},
        {"word": "disappointed", "meaning": "실망한"},
        {"word": "lonely", "meaning": "외로운"},
        {"word": "relaxed", "meaning": "편안한"},
        {"word": "calm", "meaning": "차분한"},
        {"word": "upset", "meaning": "속상한"},
        {"word": "interested", "meaning": "관심 있는"},
        {"word": "satisfied", "meaning": "만족한"},
        {"word": "thankful", "meaning": "감사하는"},
        {"word": "hopeful", "meaning": "희망적인"},
        {"word": "mood", "meaning": "기분"},
        {"word": "stress", "meaning": "스트레스"},
        {"word": "confidence", "meaning": "자신감"},
        {"word": "courage", "meaning": "용기"}],

    "💭 생각과 의견": [
        {"word": "think", "meaning": "생각하다"},
        {"word": "believe", "meaning": "믿다"},
        {"word": "guess", "meaning": "추측하다"},
        {"word": "remember", "meaning": "기억하다"},
        {"word": "forget", "meaning": "잊다"},
        {"word": "mean", "meaning": "의미하다"},
        {"word": "agree", "meaning": "동의하다"},
        {"word": "disagree", "meaning": "동의하지 않다"},
        {"word": "opinion", "meaning": "의견"},
        {"word": "idea", "meaning": "생각, 아이디어"},
        {"word": "reason", "meaning": "이유"},
        {"word": "example", "meaning": "예시"},
        {"word": "fact", "meaning": "사실"},
        {"word": "choice", "meaning": "선택"},
        {"word": "decision", "meaning": "결정"},
        {"word": "advice", "meaning": "조언"},
        {"word": "suggestion", "meaning": "제안"},
        {"word": "possible", "meaning": "가능한"},
        {"word": "impossible", "meaning": "불가능한"},
        {"word": "confusing", "meaning": "혼란스러운"}],

    "📅 계획과 약속": [
        {"word": "plan", "meaning": "계획"},
        {"word": "appointment", "meaning": "약속, 예약"},
        {"word": "promise", "meaning": "약속"},
        {"word": "meeting", "meaning": "모임, 회의"},
        {"word": "date", "meaning": "날짜, 데이트"},
        {"word": "event", "meaning": "행사"},
        {"word": "party", "meaning": "파티"},
        {"word": "festival", "meaning": "축제"},
        {"word": "deadline", "meaning": "마감일"},
        {"word": "calendar", "meaning": "달력"},
        {"word": "next week", "meaning": "다음 주"},
        {"word": "message", "meaning": "메시지"},
        {"word": "join", "meaning": "참여하다"},
        {"word": "prepare", "meaning": "준비하다"},
        {"word": "decide", "meaning": "결정하다"},
        {"word": "change", "meaning": "바꾸다"},
        {"word": "cancel", "meaning": "취소하다"},
        {"word": "on time", "meaning": "시간 맞춰"},
        {"word": "available", "meaning": "시간이 되는, 이용 가능한"},
        {"word": "reminder", "meaning": "알림"}],

    "🩺 건강한 생활": [
        {"word": "health", "meaning": "건강"},
        {"word": "body", "meaning": "몸"},
        {"word": "eye", "meaning": "눈"},
        {"word": "ear", "meaning": "귀"},
        {"word": "nose", "meaning": "코"},
        {"word": "mouth", "meaning": "입"},
        {"word": "tooth", "meaning": "이"},
        {"word": "hand", "meaning": "손"},
        {"word": "arm", "meaning": "팔"},
        {"word": "leg", "meaning": "다리"},
        {"word": "foot", "meaning": "발"},
        {"word": "stomach", "meaning": "배, 위"},
        {"word": "back", "meaning": "등, 허리"},
        {"word": "heart", "meaning": "심장"},
        {"word": "clinic", "meaning": "의원, 진료소"},
        {"word": "vitamin", "meaning": "비타민"},
        {"word": "diet", "meaning": "식단"},
        {"word": "cough", "meaning": "기침"},
        {"word": "flu", "meaning": "독감"},
        {"word": "breathe", "meaning": "숨 쉬다"}],

    "📱 미디어와 스마트폰": [
        {"word": "smartphone", "meaning": "스마트폰"},
        {"word": "screen", "meaning": "화면"},
        {"word": "app", "meaning": "앱"},
        {"word": "website", "meaning": "웹사이트"},
        {"word": "internet", "meaning": "인터넷"},
        {"word": "Wi-Fi", "meaning": "와이파이"},
        {"word": "password", "meaning": "비밀번호"},
        {"word": "text", "meaning": "문자 메시지"},
        {"word": "video call", "meaning": "영상 통화"},
        {"word": "gallery", "meaning": "사진첩"},
        {"word": "news", "meaning": "뉴스"},
        {"word": "channel", "meaning": "채널"},
        {"word": "post", "meaning": "게시물"},
        {"word": "comment", "meaning": "댓글"},
        {"word": "upload", "meaning": "업로드하다"},
        {"word": "download", "meaning": "다운로드하다"},
        {"word": "search", "meaning": "검색하다"},
        {"word": "click", "meaning": "클릭하다"},
        {"word": "battery", "meaning": "배터리"},
        {"word": "notification", "meaning": "알림"}],

    "🌈 직업과 미래": [
        {"word": "job", "meaning": "직업"},
        {"word": "work", "meaning": "일하다"},
        {"word": "company", "meaning": "회사"},
        {"word": "office", "meaning": "사무실"},
        {"word": "factory", "meaning": "공장"},
        {"word": "engineer", "meaning": "기술자, 엔지니어"},
        {"word": "mechanic", "meaning": "정비사"},
        {"word": "chef", "meaning": "요리사"},
        {"word": "firefighter", "meaning": "소방관"},
        {"word": "farmer", "meaning": "농부"},
        {"word": "designer", "meaning": "디자이너"},
        {"word": "singer", "meaning": "가수"},
        {"word": "actor", "meaning": "배우"},
        {"word": "athlete", "meaning": "운동선수"},
        {"word": "dream", "meaning": "꿈"},
        {"word": "future", "meaning": "미래"},
        {"word": "goal", "meaning": "목표"},
        {"word": "skill", "meaning": "기술, 능력"},
        {"word": "interview", "meaning": "면접"},
        {"word": "experience", "meaning": "경험"}],
}

# =========================
# 오늘의 일상 대화
# =========================
theme_dialogues = {
    "🏫 학교생활": [
        {"en": "A: What is your favorite subject?", "ko": "A: 네가 가장 좋아하는 과목은 뭐니?"},
        {"en": "B: My favorite subject is science.", "ko": "B: 내가 가장 좋아하는 과목은 과학이야."},
        {"en": "A: Do you have homework today?", "ko": "A: 오늘 숙제 있니?"},
        {"en": "B: Yes, I have a report.", "ko": "B: 응, 보고서가 있어."},
        {"en": "A: When is the presentation?", "ko": "A: 발표는 언제니?"},
        {"en": "B: It is next week.", "ko": "B: 다음 주야."}],

    "✏️ 교실 활동": [
        {"en": "A: Please underline this word.", "ko": "A: 이 단어에 밑줄을 그어 주세요."},
        {"en": "B: Okay. I will underline it.", "ko": "B: 좋아요. 밑줄 칠게요."},
        {"en": "A: Can you repeat the sentence?", "ko": "A: 문장을 반복해 줄 수 있니?"},
        {"en": "B: Yes, I can repeat it.", "ko": "B: 네, 반복할 수 있어요."},
        {"en": "A: Please turn in your paper.", "ko": "A: 종이를 제출해 주세요."},
        {"en": "B: Sure. Here it is.", "ko": "B: 네. 여기 있어요."}],

    "🏠 집과 생활": [
        {"en": "A: Where is your room?", "ko": "A: 네 방은 어디에 있니?"},
        {"en": "B: It is next to the living room.", "ko": "B: 거실 옆에 있어."},
        {"en": "A: Is your room clean?", "ko": "A: 네 방은 깨끗하니?"},
        {"en": "B: No, it is a little messy.", "ko": "B: 아니, 조금 지저분해."},
        {"en": "A: Can you clean it?", "ko": "A: 청소할 수 있니?"},
        {"en": "B: Yes, I can clean it today.", "ko": "B: 응, 오늘 청소할 수 있어."}],

    "🌅 하루 일과": [
        {"en": "A: What time do you get up?", "ko": "A: 너는 몇 시에 일어나니?"},
        {"en": "B: I usually get up at seven.", "ko": "B: 나는 보통 7시에 일어나."},
        {"en": "A: What do you do after school?", "ko": "A: 방과 후에 무엇을 하니?"},
        {"en": "B: I relax and watch videos.", "ko": "B: 쉬면서 영상을 봐."},
        {"en": "A: Do you sleep early?", "ko": "A: 너는 일찍 자니?"},
        {"en": "B: No, I sometimes sleep late.", "ko": "B: 아니, 가끔 늦게 자."}],

    "🎮 취미와 여가": [
        {"en": "A: What is your hobby?", "ko": "A: 네 취미는 뭐니?"},
        {"en": "B: My hobby is watching movies.", "ko": "B: 내 취미는 영화 보기야."},
        {"en": "A: Do you like music?", "ko": "A: 음악 좋아하니?"},
        {"en": "B: Yes, I like pop songs.", "ko": "B: 응, 나는 팝송을 좋아해."},
        {"en": "A: What do you do in your free time?", "ko": "A: 여가 시간에 무엇을 하니?"},
        {"en": "B: I play games and read comics.", "ko": "B: 게임하고 만화를 읽어."}],

    "⚽ 운동과 활동": [
        {"en": "A: What sport do you like?", "ko": "A: 어떤 운동을 좋아하니?"},
        {"en": "B: I like tennis.", "ko": "B: 나는 테니스를 좋아해."},
        {"en": "A: Do you practice often?", "ko": "A: 자주 연습하니?"},
        {"en": "B: Yes, I practice after school.", "ko": "B: 응, 방과 후에 연습해."},
        {"en": "A: Did your team win?", "ko": "A: 너희 팀이 이겼니?"},
        {"en": "B: Yes, we won the match.", "ko": "B: 응, 우리는 경기에서 이겼어."}],

    "🌦️ 날씨와 계절": [
        {"en": "A: How is the weather today?", "ko": "A: 오늘 날씨가 어때?"},
        {"en": "B: It is cloudy and windy.", "ko": "B: 흐리고 바람이 불어."},
        {"en": "A: Do you like winter?", "ko": "A: 겨울을 좋아하니?"},
        {"en": "B: No, I like spring.", "ko": "B: 아니, 나는 봄을 좋아해."},
        {"en": "A: Do you need an umbrella?", "ko": "A: 우산이 필요하니?"},
        {"en": "B: Yes, it may rain.", "ko": "B: 응, 비가 올지도 몰라."}],

    "🌳 자연과 환경": [
        {"en": "A: Do you like nature?", "ko": "A: 자연을 좋아하니?"},
        {"en": "B: Yes, I like forests and lakes.", "ko": "B: 응, 나는 숲과 호수를 좋아해."},
        {"en": "A: What can we do for the environment?", "ko": "A: 환경을 위해 무엇을 할 수 있을까?"},
        {"en": "B: We can recycle plastic.", "ko": "B: 플라스틱을 재활용할 수 있어."},
        {"en": "A: Is pollution a problem?", "ko": "A: 오염은 문제니?"},
        {"en": "B: Yes, it is a big problem.", "ko": "B: 응, 큰 문제야."}],

    "🍽️ 식당과 주문": [
        {"en": "A: Are you ready to order?", "ko": "A: 주문할 준비가 되셨나요?"},
        {"en": "B: Yes, I want pasta.", "ko": "B: 네, 파스타 주세요."},
        {"en": "A: Do you want a drink?", "ko": "A: 음료도 원하시나요?"},
        {"en": "B: Yes, I want juice.", "ko": "B: 네, 주스 주세요."},
        {"en": "A: How is the food?", "ko": "A: 음식은 어때요?"},
        {"en": "B: It is delicious.", "ko": "B: 맛있어요."}],

    "🛍️ 쇼핑과 가격": [
        {"en": "A: Can I help you?", "ko": "A: 도와드릴까요?"},
        {"en": "B: Yes, I am looking for a bag.", "ko": "B: 네, 가방을 찾고 있어요."},
        {"en": "A: What color do you want?", "ko": "A: 어떤 색을 원하세요?"},
        {"en": "B: I want a black one.", "ko": "B: 검은색을 원해요."},
        {"en": "A: It is on sale today.", "ko": "A: 오늘 할인 중이에요."},
        {"en": "B: Great. I will buy it.", "ko": "B: 좋아요. 살게요."}],

    "👕 옷과 외모": [
        {"en": "A: Do you like this jacket?", "ko": "A: 이 재킷 마음에 드니?"},
        {"en": "B: Yes, it looks comfortable.", "ko": "B: 응, 편해 보여."},
        {"en": "A: What size do you need?", "ko": "A: 어떤 사이즈가 필요하니?"},
        {"en": "B: I need a medium size.", "ko": "B: 중간 사이즈가 필요해."},
        {"en": "A: Are these sneakers new?", "ko": "A: 이 운동화는 새거니?"},
        {"en": "B: Yes, they are new.", "ko": "B: 응, 새거야."}],

    "🚇 교통과 길 찾기": [
        {"en": "A: Where is the bus stop?", "ko": "A: 버스 정류장이 어디에 있나요?"},
        {"en": "B: Go straight and turn left.", "ko": "B: 똑바로 가서 왼쪽으로 도세요."},
        {"en": "A: Is the subway station far?", "ko": "A: 지하철역은 먼가요?"},
        {"en": "B: No, it is near here.", "ko": "B: 아니요, 여기 근처에 있어요."},
        {"en": "A: I think I am lost.", "ko": "A: 길을 잃은 것 같아요."},
        {"en": "B: I can help you.", "ko": "B: 제가 도와드릴 수 있어요."}],

    "🧳 여행과 숙박": [
        {"en": "A: Do you have a reservation?", "ko": "A: 예약하셨나요?"},
        {"en": "B: Yes, I have a hotel reservation.", "ko": "B: 네, 호텔 예약이 있어요."},
        {"en": "A: May I see your passport?", "ko": "A: 여권을 볼 수 있을까요?"},
        {"en": "B: Sure. Here it is.", "ko": "B: 물론이죠. 여기 있어요."},
        {"en": "A: What time is check out?", "ko": "A: 체크아웃은 몇 시인가요?"},
        {"en": "B: It is at eleven.", "ko": "B: 11시입니다."}],

    "👥 친구 관계": [
        {"en": "A: Do you want to hang out this weekend?", "ko": "A: 이번 주말에 같이 놀래?"},
        {"en": "B: Yes, that sounds fun.", "ko": "B: 응, 재미있겠다."},
        {"en": "A: Can I invite my friend?", "ko": "A: 내 친구도 초대해도 돼?"},
        {"en": "B: Sure. We can meet together.", "ko": "B: 물론이지. 같이 만날 수 있어."},
        {"en": "A: Thank you for helping me.", "ko": "A: 도와줘서 고마워."},
        {"en": "B: No problem. We are friends.", "ko": "B: 괜찮아. 우리는 친구잖아."}],

    "😊 감정 표현 확장": [
        {"en": "A: You look nervous.", "ko": "A: 너 긴장해 보여."},
        {"en": "B: Yes, I have a presentation.", "ko": "B: 응, 발표가 있어."},
        {"en": "A: Don't worry. You can do it.", "ko": "A: 걱정하지 마. 너는 할 수 있어."},
        {"en": "B: Thank you. I feel better.", "ko": "B: 고마워. 기분이 나아졌어."},
        {"en": "A: Are you proud of yourself?", "ko": "A: 너 자신이 자랑스럽니?"},
        {"en": "B: Yes, I am proud.", "ko": "B: 응, 자랑스러워."}],

    "💭 생각과 의견": [
        {"en": "A: What do you think about this idea?", "ko": "A: 이 생각에 대해 어떻게 생각하니?"},
        {"en": "B: I think it is useful.", "ko": "B: 유용하다고 생각해."},
        {"en": "A: Do you agree with me?", "ko": "A: 내 말에 동의하니?"},
        {"en": "B: Yes, I agree.", "ko": "B: 응, 동의해."},
        {"en": "A: Can you give me a reason?", "ko": "A: 이유를 말해 줄 수 있니?"},
        {"en": "B: Sure. It is simple and clear.", "ko": "B: 물론이지. 간단하고 명확해."}],

    "📅 계획과 약속": [
        {"en": "A: Do you have plans this weekend?", "ko": "A: 이번 주말에 계획 있니?"},
        {"en": "B: Yes, I have a meeting.", "ko": "B: 응, 모임이 있어."},
        {"en": "A: Are you available tomorrow?", "ko": "A: 내일 시간 돼?"},
        {"en": "B: Yes, I am free in the afternoon.", "ko": "B: 응, 오후에 시간이 있어."},
        {"en": "A: Can we change the time?", "ko": "A: 시간을 바꿀 수 있을까?"},
        {"en": "B: Sure. No problem.", "ko": "B: 물론이지. 문제없어."}],

    "🩺 건강한 생활": [
        {"en": "A: You look tired.", "ko": "A: 너 피곤해 보여."},
        {"en": "B: Yes, I did not sleep well.", "ko": "B: 응, 잠을 잘 못 잤어."},
        {"en": "A: You should rest.", "ko": "A: 쉬는 게 좋겠어."},
        {"en": "B: I know. I need more sleep.", "ko": "B: 알아. 잠이 더 필요해."},
        {"en": "A: Do you exercise often?", "ko": "A: 자주 운동하니?"},
        {"en": "B: Sometimes. I want to be healthy.", "ko": "B: 가끔. 건강해지고 싶어."}],

    "📱 미디어와 스마트폰": [
        {"en": "A: What app do you use often?", "ko": "A: 어떤 앱을 자주 사용하니?"},
        {"en": "B: I often use a video app.", "ko": "B: 나는 영상 앱을 자주 사용해."},
        {"en": "A: Can you send me the link?", "ko": "A: 링크를 보내줄 수 있니?"},
        {"en": "B: Sure. I will send it now.", "ko": "B: 물론이지. 지금 보낼게."},
        {"en": "A: Is your battery low?", "ko": "A: 배터리가 부족하니?"},
        {"en": "B: Yes, I need to charge my phone.", "ko": "B: 응, 휴대폰을 충전해야 해."}],

    "🌈 직업과 미래": [
        {"en": "A: What is your dream job?", "ko": "A: 네 꿈의 직업은 뭐니?"},
        {"en": "B: I want to be an engineer.", "ko": "B: 나는 엔지니어가 되고 싶어."},
        {"en": "A: What skill do you need?", "ko": "A: 어떤 기술이 필요하니?"},
        {"en": "B: I need computer skills.", "ko": "B: 컴퓨터 기술이 필요해."},
        {"en": "A: Do you have a goal?", "ko": "A: 목표가 있니?"},
        {"en": "B: Yes, I want to get a good job.", "ko": "B: 응, 좋은 직업을 얻고 싶어."}],
}


# =========================
# 카테고리 통합
# - 단어 400개와 대화 내용은 삭제하지 않습니다.
# - 카테고리만 크게 묶습니다.
# - 이 통합 결과가 단어 목록, 카테고리별 카세트, 전체 카세트에 모두 적용됩니다.
# =========================
CATEGORY_MERGE_MAP = {
    # 1. 학교
    "🏫 학교생활": "🏫 학교생활",
    "✏️ 교실 활동": "🏫 학교생활",

    # 2. 생활
    "🏠 집과 생활": "🏠 생활",
    "🌅 하루 일과": "🏠 생활",
    "🩺 건강한 생활": "🏠 생활",

    # 3. 여가
    "🎮 취미와 여가": "🎮 여가",
    "⚽ 운동과 활동": "🎮 여가",
    "🌦️ 날씨와 계절": "🎮 여가",
    "🌳 자연과 환경": "🎮 여가",

    # 4. 음식·쇼핑
    "🍽️ 식당과 주문": "🍽️ 음식·쇼핑",
    "🛍️ 쇼핑과 가격": "🍽️ 음식·쇼핑",
    "👕 옷과 외모": "🍽️ 음식·쇼핑",

    # 5. 이동·여행
    "🚇 교통과 길 찾기": "🚇 이동·여행",
    "🧳 여행과 숙박": "🚇 이동·여행",

    # 6. 사람·감정
    "👥 친구 관계": "👥 사람·감정",
    "😊 감정 표현 확장": "👥 사람·감정",
    "💭 생각과 의견": "👥 사람·감정",
    "📅 계획과 약속": "👥 사람·감정",

    # 7. 미디어·미래
    "📱 미디어와 스마트폰": "📱 미디어·미래",
    "🌈 직업과 미래": "📱 미디어·미래",
}


def merge_categories(original_dict):
    merged = {}

    for old_cat, items in original_dict.items():
        new_cat = CATEGORY_MERGE_MAP.get(old_cat, old_cat)

        if new_cat not in merged:
            merged[new_cat] = []

        # 단어/대화 내용은 그대로 유지하고, 카테고리만 합칩니다.
        merged[new_cat].extend(items)

    return merged


# 여기에서 먼저 통합해야 아래의 단어 목록, 카세트가 모두 통합 카테고리 기준으로 작동합니다.
word_themes = merge_categories(word_themes)
theme_dialogues = merge_categories(theme_dialogues)


VI_MEANINGS = {'subject': 'môn học', 'math': 'toán', 'science': 'khoa học', 'history': 'lịch sử', 'music': 'âm nhạc', 'art': 'mỹ thuật', 'P.E.': 'thể dục', 'club': 'câu lạc bộ', 'schedule': 'thời khóa biểu', 'semester': 'học kỳ', 'assignment': 'bài tập', 'project': 'dự án', 'presentation': 'bài thuyết trình', 'report': 'báo cáo', 'textbook': 'sách giáo khoa', 'workbook': 'sách bài tập', 'library': 'thư viện', 'cafeteria': 'nhà ăn', 'hallway': 'hành lang', 'attendance': 'điểm danh', 'copy': 'chép lại', 'repeat': 'lặp lại', 'underline': 'gạch chân', 'circle': 'khoanh tròn', 'choose': 'chọn', 'check': 'kiểm tra', 'match': 'nối, ghép', 'complete': 'hoàn thành', 'fill': 'điền vào', 'spell': 'đánh vần', 'pronounce': 'phát âm', 'review': 'ôn tập', 'explain': 'giải thích', 'describe': 'miêu tả', 'compare': 'so sánh', 'discuss': 'thảo luận', 'present': 'thuyết trình', 'take notes': 'ghi chép', 'turn in': 'nộp', 'hand out': 'phát cho', 'living room': 'phòng khách', 'bedroom': 'phòng ngủ', 'kitchen': 'nhà bếp', 'balcony': 'ban công', 'floor': 'sàn nhà, tầng', 'wall': 'bức tường', 'roof': 'mái nhà', 'garden': 'khu vườn', 'yard': 'sân', 'sofa': 'ghế sofa', 'television': 'tivi', 'refrigerator': 'tủ lạnh', 'microwave': 'lò vi sóng', 'blanket': 'chăn', 'pillow': 'gối', 'towel': 'khăn', 'soap': 'xà phòng', 'mirror': 'gương', 'closet': 'tủ quần áo', 'trash': 'rác', 'routine': 'thói quen hằng ngày', 'wake up': 'thức dậy', 'get up': 'ngủ dậy', 'brush': 'chải, đánh', 'shower': 'tắm vòi sen', 'dress': 'váy liền, đầm', 'leave': 'rời đi', 'arrive': 'đến nơi', 'return': 'trở về', 'finish': 'kết thúc', 'relax': 'thư giãn', 'weekday': 'ngày trong tuần', 'weekend': 'cuối tuần', 'usually': 'thường thường', 'often': 'thường xuyên', 'sometimes': 'thỉnh thoảng', 'always': 'luôn luôn', 'never': 'không bao giờ', 'habit': 'thói quen', 'lifestyle': 'lối sống', 'hobby': 'sở thích', 'movie': 'phim', 'drama': 'phim truyền hình', 'song': 'bài hát', 'concert': 'buổi hòa nhạc', 'dance': 'nhảy, múa', 'drawing': 'vẽ tranh', 'painting': 'bức tranh, hội họa', 'comic': 'truyện tranh', 'novel': 'tiểu thuyết', 'photography': 'chụp ảnh', 'cooking': 'nấu ăn', 'baking': 'làm bánh', 'camping': 'cắm trại', 'hiking': 'đi bộ đường dài', 'fishing': 'câu cá', 'free time': 'thời gian rảnh', 'favorite': 'yêu thích nhất', 'popular': 'phổ biến', 'relaxing': 'thư giãn', 'soccer': 'bóng đá', 'baseball': 'bóng chày', 'basketball': 'bóng rổ', 'volleyball': 'bóng chuyền', 'tennis': 'quần vợt', 'badminton': 'cầu lông', 'swimming': 'bơi lội', 'cycling': 'đạp xe', 'skating': 'trượt băng', 'boxing': 'quyền anh', 'taekwondo': 'taekwondo', 'yoga': 'yoga', 'fitness': 'thể dục thể hình', 'field': 'sân, cánh đồng', 'court': 'sân thi đấu', 'stadium': 'sân vận động', 'coach': 'huấn luyện viên', 'competition': 'cuộc thi, giải đấu', 'medal': 'huy chương', 'season': 'mùa', 'spring': 'mùa xuân', 'summer': 'mùa hè', 'fall': 'mùa thu', 'winter': 'mùa đông', 'cloudy': 'nhiều mây', 'rainy': 'có mưa', 'snowy': 'có tuyết', 'windy': 'có gió', 'stormy': 'có bão', 'foggy': 'có sương mù', 'dry': 'khô', 'wet': 'ướt', 'humid': 'ẩm', 'temperature': 'nhiệt độ', 'degree': 'độ', 'forecast': 'dự báo thời tiết', 'umbrella': 'ô, dù', 'raincoat': 'áo mưa', 'rainbow': 'cầu vồng', 'nature': 'thiên nhiên', 'environment': 'môi trường', 'plant': 'cây, thực vật', 'forest': 'rừng', 'lake': 'hồ', 'ocean': 'đại dương', 'island': 'hòn đảo', 'desert': 'sa mạc', 'farm': 'nông trại', 'village': 'ngôi làng', 'leaf': 'lá', 'root': 'rễ', 'stone': 'đá', 'sand': 'cát', 'soil': 'đất', 'plastic': 'nhựa', 'recycle': 'tái chế', 'protect': 'bảo vệ', 'pollution': 'ô nhiễm', 'restaurant': 'nhà hàng', 'menu': 'thực đơn', 'seat': 'chỗ ngồi', 'waiter': 'nam phục vụ', 'waitress': 'nữ phục vụ', 'order': 'gọi món, đặt hàng', 'dish': 'món ăn, cái đĩa', 'meal': 'bữa ăn', 'soup': 'súp', 'salad': 'sa lát', 'steak': 'bít tết', 'pizza': 'pizza', 'pasta': 'mì Ý', 'burger': 'bánh burger', 'sandwich': 'bánh sandwich', 'dessert': 'món tráng miệng', 'spicy': 'cay', 'sweet': 'ngọt', 'bill': 'hóa đơn', 'receipt': 'biên lai', 'shop': 'cửa hàng', 'market': 'chợ', 'mall': 'trung tâm mua sắm', 'supermarket': 'siêu thị', 'cashier': 'thu ngân', 'customer': 'khách hàng', 'price': 'giá', 'sale': 'giảm giá', 'discount': 'giảm giá', 'coupon': 'phiếu giảm giá', 'change': 'tiền thối lại', 'coin': 'đồng xu', 'expensive': 'đắt', 'cheap': 'rẻ', 'size': 'kích cỡ', 'color': 'màu sắc', 'brand': 'thương hiệu', 'exchange': 'đổi hàng', 'refund': 'hoàn tiền', 'T-shirt': 'áo thun', 'pants': 'quần dài', 'jeans': 'quần jean', 'shorts': 'quần ngắn', 'skirt': 'váy', 'jacket': 'áo khoác', 'coat': 'áo khoác dài', 'sweater': 'áo len', 'hoodie': 'áo hoodie', 'uniform': 'đồng phục', 'socks': 'tất, vớ', 'sneakers': 'giày thể thao', 'boots': 'ủng', 'sandals': 'dép xăng đan', 'scarf': 'khăn quàng cổ', 'gloves': 'găng tay', 'belt': 'thắt lưng', 'glasses': 'kính', 'comfortable': 'thoải mái', 'bus stop': 'trạm xe buýt', 'subway': 'tàu điện ngầm', 'airport': 'sân bay', 'terminal': 'bến, nhà ga', 'platform': 'sân ga', 'route': 'tuyến đường', 'direction': 'hướng', 'straight': 'đi thẳng', 'corner': 'góc đường', 'block': 'khu, dãy nhà', 'traffic': 'giao thông', 'crosswalk': 'vạch qua đường', 'sidewalk': 'vỉa hè', 'bridge': 'cây cầu', 'tunnel': 'đường hầm', 'entrance': 'lối vào', 'exit': 'lối ra', 'transfer': 'chuyển tuyến', 'lost': 'bị lạc', 'guide': 'hướng dẫn, hướng dẫn viên', 'travel': 'du lịch', 'trip': 'chuyến đi', 'vacation': 'kỳ nghỉ', 'tourist': 'khách du lịch', 'passport': 'hộ chiếu', 'flight': 'chuyến bay', 'hotel': 'khách sạn', 'motel': 'nhà nghỉ ven đường', 'hostel': 'nhà trọ', 'reservation': 'đặt chỗ', 'check in': 'nhận phòng', 'check out': 'trả phòng', 'luggage': 'hành lý', 'suitcase': 'vali', 'backpack': 'ba lô', 'souvenir': 'quà lưu niệm', 'museum': 'bảo tàng', 'famous': 'nổi tiếng', 'local': 'địa phương', 'friendship': 'tình bạn', 'best friend': 'bạn thân nhất', 'teammate': 'đồng đội', 'partner': 'bạn cùng nhóm, đối tác', 'message': 'tin nhắn', 'call': 'gọi điện', 'chat': 'trò chuyện', 'invite': 'mời', 'visit': 'thăm', 'meet': 'gặp', 'hang out': 'đi chơi', 'laugh': 'cười', 'share': 'chia sẻ', 'trust': 'tin tưởng', 'promise': 'lời hứa, hứa', 'secret': 'bí mật', 'joke': 'trò đùa', 'together': 'cùng nhau', 'alone': 'một mình', 'forgive': 'tha thứ', 'excited': 'hào hứng', 'nervous': 'lo lắng, hồi hộp', 'bored': 'chán', 'surprised': 'ngạc nhiên', 'confused': 'bối rối', 'embarrassed': 'xấu hổ, ngượng', 'proud': 'tự hào', 'disappointed': 'thất vọng', 'lonely': 'cô đơn', 'relaxed': 'thư thái', 'calm': 'bình tĩnh', 'upset': 'buồn bực', 'interested': 'quan tâm, thích thú', 'satisfied': 'hài lòng', 'thankful': 'biết ơn', 'hopeful': 'đầy hy vọng', 'mood': 'tâm trạng', 'stress': 'căng thẳng', 'confidence': 'sự tự tin', 'courage': 'lòng can đảm', 'think': 'nghĩ', 'believe': 'tin', 'guess': 'đoán', 'remember': 'nhớ', 'forget': 'quên', 'mean': 'có nghĩa là', 'agree': 'đồng ý', 'disagree': 'không đồng ý', 'opinion': 'ý kiến', 'idea': 'ý tưởng', 'reason': 'lý do', 'example': 'ví dụ', 'fact': 'sự thật', 'choice': 'sự lựa chọn', 'decision': 'quyết định', 'advice': 'lời khuyên', 'suggestion': 'gợi ý, đề xuất', 'possible': 'có thể', 'impossible': 'không thể', 'confusing': 'khó hiểu', 'plan': 'kế hoạch', 'appointment': 'cuộc hẹn', 'meeting': 'cuộc họp, buổi gặp', 'date': 'ngày, cuộc hẹn', 'event': 'sự kiện', 'party': 'bữa tiệc', 'festival': 'lễ hội', 'deadline': 'hạn chót', 'calendar': 'lịch', 'next week': 'tuần sau', 'join': 'tham gia', 'prepare': 'chuẩn bị', 'decide': 'quyết định', 'cancel': 'hủy', 'on time': 'đúng giờ', 'available': 'có sẵn, rảnh', 'reminder': 'lời nhắc', 'health': 'sức khỏe', 'body': 'cơ thể', 'eye': 'mắt', 'ear': 'tai', 'nose': 'mũi', 'mouth': 'miệng', 'tooth': 'răng', 'hand': 'bàn tay', 'arm': 'cánh tay', 'leg': 'chân', 'foot': 'bàn chân', 'stomach': 'bụng, dạ dày', 'back': 'lưng', 'heart': 'tim', 'clinic': 'phòng khám', 'vitamin': 'vitamin', 'diet': 'chế độ ăn', 'cough': 'ho', 'flu': 'cúm', 'breathe': 'thở', 'smartphone': 'điện thoại thông minh', 'screen': 'màn hình', 'app': 'ứng dụng', 'website': 'trang web', 'internet': 'internet', 'Wi-Fi': 'Wi-Fi', 'password': 'mật khẩu', 'text': 'tin nhắn văn bản', 'video call': 'cuộc gọi video', 'gallery': 'thư viện ảnh', 'news': 'tin tức', 'channel': 'kênh', 'post': 'bài đăng', 'comment': 'bình luận', 'upload': 'tải lên', 'download': 'tải xuống', 'search': 'tìm kiếm', 'click': 'nhấp chuột', 'battery': 'pin', 'notification': 'thông báo', 'job': 'nghề nghiệp', 'work': 'làm việc', 'company': 'công ty', 'office': 'văn phòng', 'factory': 'nhà máy', 'engineer': 'kỹ sư', 'mechanic': 'thợ máy', 'chef': 'đầu bếp', 'firefighter': 'lính cứu hỏa', 'farmer': 'nông dân', 'designer': 'nhà thiết kế', 'singer': 'ca sĩ', 'actor': 'diễn viên', 'athlete': 'vận động viên', 'dream': 'ước mơ', 'future': 'tương lai', 'goal': 'mục tiêu', 'skill': 'kỹ năng', 'interview': 'phỏng vấn', 'experience': 'kinh nghiệm'}

def get_display_meaning(word, ko_meaning):
    """선택한 뜻 언어에 따라 한국어 또는 베트남어 뜻을 반환합니다."""
    selected_language = st.session_state.get("daily400_meaning_language", "한국어 Korean")
    if selected_language == "베트남어 Vietnamese":
        return VI_MEANINGS.get(str(word).strip(), ko_meaning)
    return ko_meaning


# =========================
# 카세트 듣기 - 단어별 mp3 순차 재생 + 현재 단어 동기화 표시
# =========================
def flatten_all_words():
    all_items = []
    number = 1
    for theme_name, theme_words in word_themes.items():
        for item in theme_words:
            word = item["word"]
            all_items.append({
                "number": number,
                "theme": theme_name,
                "word": word,
                "meaning": get_display_meaning(word, item["meaning"]),
                "emoji": get_word_emoji(word),
            })
            number += 1
    return all_items


def make_theme_cassette_items(theme_words, theme_name):
    theme_items = []
    for idx, item in enumerate(theme_words, start=1):
        word = item["word"]
        theme_items.append({
            "number": idx,
            "theme": theme_name,
            "word": word,
            "meaning": item["meaning"],
            "emoji": get_word_emoji(word),
        })
    return theme_items


def make_cassette_text(items, repeat_word=2):
    parts = []
    for item in items:
        word = item["word"]
        parts.append(". ".join([word] * repeat_word) + ".")
    return " ".join(parts)


def js_cassette_visual_player(items, audio_payloads, title="📼 단어 카세트", height=470):
    """
    단어별 mp3를 순서대로 재생합니다.
    각 mp3가 끝나면 다음 단어로 넘어가므로 화면의 단어·뜻·이모지가 발음과 잘 맞습니다.
    """
    player_id = "daily_cassette_" + uuid.uuid4().hex

    visual_items = []
    for idx, (item, audio_b64) in enumerate(zip(items, audio_payloads), start=1):
        visual_items.append({
            "number": item.get("number", idx),
            "theme": str(item.get("theme", "")),
            "word": str(item.get("word", "")),
            "meaning": str(item.get("meaning", "")),
            "emoji": get_word_emoji(item.get("word", "")),
            "src": "data:audio/mp3;base64," + audio_b64,
        })

    items_json = json.dumps(visual_items, ensure_ascii=False)
    safe_title = html.escape(title)
    safe_player_id = json.dumps(player_id)

    components.html(
        f"""
        <div id="{player_id}" style="
            font-family: Arial, sans-serif;
            width:100%;
            box-sizing:border-box;
            border-radius:28px;
            padding:14px;
            background:linear-gradient(135deg,#f0fdf4 0%,#eff6ff 48%,#fff7ed 100%);
            border:1px solid #bbf7d0;
            box-shadow:0 8px 22px rgba(15,23,42,0.10);
            overflow:hidden;
        ">
            <div style="display:flex; justify-content:flex-end; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
                <div id="count_{player_id}" style="font-size:13px; font-weight:900; color:#475569; background:rgba(255,255,255,.8); border:1px solid #dcfce7; border-radius:999px; padding:7px 12px;">1 / {len(visual_items)}</div>
            </div>

            <audio id="audio_{player_id}" preload="auto" style="width:100%; margin:6px 0 14px 0;"></audio>

            <div style="display:grid; grid-template-columns:1fr; gap:12px;">
                <div style="
                    background:rgba(255,255,255,0.88);
                    border:1px solid #dcfce7;
                    border-radius:26px;
                    padding:16px 14px;
                    text-align:center;
                ">
                    <div id="theme_{player_id}" style="display:inline-block; font-size:13px; font-weight:900; color:#15803d; background:#dcfce7; border-radius:999px; padding:6px 12px; margin-bottom:10px;">Theme</div>
                    <div id="emoji_{player_id}" style="font-size:46px; line-height:1.05; margin:2px 0;">🌱</div>
                    <div id="word_{player_id}" style="font-size:clamp(36px,7.8vw,62px); font-weight:1000; color:#111827; line-height:1.05; word-break:break-word; letter-spacing:-1px;">Ready</div>
                    <div id="meaning_{player_id}" style="font-size:clamp(20px,4.4vw,30px); font-weight:900; color:#334155; margin-top:10px; word-break:keep-all;">재생 버튼을 눌러 주세요.</div>
                    <div style="width:100%; height:14px; background:#e2e8f0; border-radius:999px; overflow:hidden; margin-top:12px;">
                        <div id="bar_{player_id}" style="height:100%; width:0%; background:linear-gradient(90deg,#22c55e,#0ea5e9,#8b5cf6); border-radius:999px;"></div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns:1fr; gap:8px;">
                    <button id="play_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #86efac; background:linear-gradient(135deg,#dcfce7,#dbeafe); font-size:13px; font-weight:900; cursor:pointer; box-shadow:0 3px 9px rgba(15,23,42,0.08);">▶️ 재생</button>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <button id="prev_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">⏮ 이전</button>
                    <button id="next_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">다음 ⏭</button>
                </div>

                <div id="status_{player_id}" style="font-size:14px; font-weight:900; color:#075985; min-height:22px;">준비 완료</div>

            </div>
        </div>

        <script>
        const items_{player_id} = {items_json};
        const audio_{player_id} = document.getElementById("audio_{player_id}");
        const wordEl_{player_id} = document.getElementById("word_{player_id}");
        const meaningEl_{player_id} = document.getElementById("meaning_{player_id}");
        const emojiEl_{player_id} = document.getElementById("emoji_{player_id}");
        const themeEl_{player_id} = document.getElementById("theme_{player_id}");
        const countEl_{player_id} = document.getElementById("count_{player_id}");
        const barEl_{player_id} = document.getElementById("bar_{player_id}");
        const statusEl_{player_id} = document.getElementById("status_{player_id}");
        const playBtn_{player_id} = document.getElementById("play_{player_id}");
        const prevBtn_{player_id} = document.getElementById("prev_{player_id}");
        const nextBtn_{player_id} = document.getElementById("next_{player_id}");
        const playerId_{player_id} = {safe_player_id};

        let currentIndex_{player_id} = 0;
        let isPlayingList_{player_id} = false;
        let isFinished_{player_id} = false;


        function setCurrent_{player_id}(idx) {{
            if (!items_{player_id}.length) return;
            idx = Math.max(0, Math.min(idx, items_{player_id}.length - 1));
            currentIndex_{player_id} = idx;
            const it = items_{player_id}[idx];

            wordEl_{player_id}.textContent = it.word;
            meaningEl_{player_id}.textContent = it.meaning;
            emojiEl_{player_id}.textContent = it.emoji;
            themeEl_{player_id}.textContent = it.theme || "Daily English";
            countEl_{player_id}.textContent = (idx + 1) + " / " + items_{player_id}.length;

            const percent = items_{player_id}.length <= 1 ? 100 : (idx / (items_{player_id}.length - 1)) * 100;
            barEl_{player_id}.style.width = percent + "%";
        }}

        function loadCurrent_{player_id}() {{
            const it = items_{player_id}[currentIndex_{player_id}];
            setCurrent_{player_id}(currentIndex_{player_id});
            if (audio_{player_id}.src !== it.src) {{
                audio_{player_id}.src = it.src;
                audio_{player_id}.load();
            }}
        }}

        function playCurrent_{player_id}() {{
            if (!items_{player_id}.length) return;
            isPlayingList_{player_id} = true;
            isFinished_{player_id} = false;
            loadCurrent_{player_id}();
            playBtn_{player_id}.textContent = "⏸ 멈춤";
            statusEl_{player_id}.textContent = "현재 단어: " + items_{player_id}[currentIndex_{player_id}].word;
            audio_{player_id}.play().catch(() => {{
                statusEl_{player_id}.textContent = "브라우저가 자동 재생을 막았습니다. 재생 버튼을 한 번 더 눌러 주세요.";
                playBtn_{player_id}.textContent = "▶️ 재생";
            }});
        }}

        function pauseCurrent_{player_id}() {{
            isPlayingList_{player_id} = false;
            audio_{player_id}.pause();
            playBtn_{player_id}.textContent = "▶️ 이어 듣기";
            statusEl_{player_id}.textContent = "일시정지";
        }}

        function moveTo_{player_id}(idx, autoPlay=false) {{
            isPlayingList_{player_id} = autoPlay;
            isFinished_{player_id} = false;
            audio_{player_id}.pause();
            currentIndex_{player_id} = Math.max(0, Math.min(idx, items_{player_id}.length - 1));
            loadCurrent_{player_id}();
            if (autoPlay) {{
                playCurrent_{player_id}();
            }} else {{
                playBtn_{player_id}.textContent = "▶️ 재생";
                statusEl_{player_id}.textContent = "선택된 단어: " + items_{player_id}[currentIndex_{player_id}].word;
            }}
        }}

        loadCurrent_{player_id}();

        playBtn_{player_id}.addEventListener("click", function() {{
            if (isPlayingList_{player_id}) {{
                pauseCurrent_{player_id}();
            }} else {{
                if (isFinished_{player_id}) {{
                    currentIndex_{player_id} = 0;
                    isFinished_{player_id} = false;
                }}
                playCurrent_{player_id}();
            }}
        }});

        prevBtn_{player_id}.addEventListener("click", function() {{
            moveTo_{player_id}(currentIndex_{player_id} - 1, false);
        }});

        nextBtn_{player_id}.addEventListener("click", function() {{
            moveTo_{player_id}(currentIndex_{player_id} + 1, false);
        }});

        audio_{player_id}.addEventListener("ended", function() {{
            if (!isPlayingList_{player_id}) return;
            if (currentIndex_{player_id} < items_{player_id}.length - 1) {{
                currentIndex_{player_id} += 1;
                playCurrent_{player_id}();
            }} else {{
                isPlayingList_{player_id} = false;
                isFinished_{player_id} = true;
                playBtn_{player_id}.textContent = "▶️ 처음부터 다시";
                statusEl_{player_id}.textContent = "✅ 카세트 재생 완료";
                barEl_{player_id}.style.width = "100%";
            }}
        }});
        </script>
        """,
        height=height,
        scrolling=False
    )


def show_cassette_audio(items, title):
    repeat_word = st.selectbox(
        "단어 반복 횟수",
        [1, 2, 3],
        index=1,
        key=f"repeat_{title}"
    )

    if title == "전체 단어":
        button_label = "🎧 전체 단어 듣기"
    elif title == "복습 희망":
        button_label = "🎧 복습 희망 단어 듣기"
    else:
        button_label = "🎧 테마별 전체 단어 듣기"

    if st.button(button_label, key=f"visual_cassette_{title}", use_container_width=True):
        try:
            with st.spinner("단어별 카세트 음성을 만드는 중입니다. 처음 한 번은 조금 걸릴 수 있습니다."):
                audio_payloads = []
                for item in items:
                    word = str(item["word"]).strip()
                    tts_text = ". ".join([word] * repeat_word) + "."
                    audio_bytes = get_tts_mp3_bytes(tts_text, lang="en")
                    audio_payloads.append(base64.b64encode(audio_bytes).decode("utf-8"))

            js_cassette_visual_player(
                items=items,
                audio_payloads=audio_payloads,
                title="🎧 전체 단어 듣기" if title == "전체 단어" else "🎧 단어 듣기",
                height=470
            )
        except Exception as e:
            st.error("카세트 음성을 만들지 못했습니다. requirements.txt에 requests가 있는지 확인해 주세요.")
            st.caption(f"오류 내용: {e}")




def show_all_cassette_tab():
    all_items = flatten_all_words()
    show_cassette_audio(all_items, "전체 단어")


def show_cassette_player(theme_words, theme_name):
    theme_items = make_theme_cassette_items(theme_words, theme_name)
    show_cassette_audio(theme_items, theme_name)


# =========================
# 오늘의 일상 대화 보여주기
# =========================
def show_dialogue(theme_name):
    dialogue = theme_dialogues.get(theme_name, [])

    if not dialogue:
        return

    st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
    st.markdown('<div class="dialogue-title">💬 오늘의 일상 대화</div>', unsafe_allow_html=True)

    for line in dialogue:
        st.markdown(
            f"<div class='dialogue-line'>{line['en']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='dialogue-meaning'>{line['ko']}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    html_dialogue_audio_player(
        label="🔊 대화 듣기",
        dialogue_lines=dialogue,
        line_pause_ms=1400,
        height=105
    )

    dialogue_text = make_dialogue_tts_text(dialogue)
    dialogue_audio_bytes = make_tts_audio(dialogue_text)

    safe_file_name = re.sub(r"[^a-zA-Z0-9가-힣_]+", "_", theme_name)

    st.download_button(
        label="⬇️ 대화 듣기 파일 다운로드",
        data=dialogue_audio_bytes,
        file_name=f"{safe_file_name}_dialogue.mp3",
        mime="audio/mp3",
        key=f"{theme_name}_dialogue_download"
    )


# =========================
# 단어 익히기
# =========================
def show_word_cards(theme_words, theme_name):
    for idx, item in enumerate(theme_words):
        word = item["word"]
        meaning = item["meaning"]
        display_meaning = get_display_meaning(word, meaning)
        review_id = make_review_id(theme_name, word)
        checked = review_id in st.session_state.unknown_words
        checkbox_key = f"{theme_name}_unknown_{idx}_{word}"

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.25, 1.05, 0.35, 1.65, 1.25])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{word}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='meaning-text'>{display_meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            audio_button(
                "🔊 듣기",
                word,
                key=f"{theme_name}_learn_audio_{idx}"
            )

        with col5:
            review_checked = st.checkbox(
                "복습 희망",
                value=checked,
                key=checkbox_key
            )

            # 체크박스 화면 상태와 실제 복습 희망 목록을 매번 동기화합니다.
            # 이렇게 해야 전체 삭제 후 다시 체크해도 바로 목록에 들어갑니다.
            if review_checked and review_id not in st.session_state.unknown_words:
                add_unknown_word(word, meaning, theme_name)
            elif not review_checked and review_id in st.session_state.unknown_words:
                remove_unknown_word(review_id)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 
# =========================



# =========================
# 복습 희망 단어 모음 탭
# =========================
def show_unknown_words_tab():
    st.markdown(
        """
        <div class="theme-header">
            <div class="theme-title">⭐ 복습 희망</div>
            <div class="theme-desc">각 탭에서 복습하고 싶은 단어만 모아서 다시 들을 수 있습니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    unknown_ids = st.session_state.unknown_words
    unknown_info = st.session_state.unknown_word_info

    if not unknown_ids:
        st.info("아직 체크한 단어가 없습니다. 각 단어 옆의 '복습 희망'을 체크해 보세요.")
        return

    st.success(f"총 {len(unknown_ids)}개의 단어를 체크했습니다.")

    unknown_items = []
    for idx, review_id in enumerate(unknown_ids, start=1):
        info = unknown_info.get(review_id, {})
        word = info.get("word", review_id.split("||")[-1])
        ko_meaning = info.get("meaning", "")
        unknown_items.append({
            "number": idx,
            "theme": info.get("theme", "복습 희망"),
            "word": word,
            "meaning": get_display_meaning(word, ko_meaning),
            "emoji": get_word_emoji(word),
        })

    show_cassette_audio(unknown_items, "복습 희망")

    st.markdown("### 📌 체크한 단어 목록")

    for idx, review_id in enumerate(unknown_ids):
        info = unknown_info.get(review_id, {})
        word = info.get("word", review_id.split("||")[-1])
        meaning = get_display_meaning(word, info.get("meaning", ""))
        theme_name = info.get("theme", "")

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.25, 1.05, 0.35, 1.65, 1.25])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{word}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='meaning-text'>{display_meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            audio_button(
                "🔊 듣기",
                word,
                key=f"unknown_word_audio_{idx}_{review_id}"
            )

        with col5:
            if st.button("삭제", key=f"delete_unknown_{idx}_{review_id}", use_container_width=True):
                remove_unknown_word(review_id)

                keys_to_delete = [
                    key for key in list(st.session_state.keys())
                    if "_unknown_" in str(key) and str(key).endswith(f"_{word}")
                ]
                for key in keys_to_delete:
                    del st.session_state[key]

                st.rerun()

        st.caption(f"분류: {theme_name}")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ 복습 희망 전체 삭제", key="clear_all_unknown_words", use_container_width=True):
        st.session_state.unknown_words = []
        st.session_state.unknown_word_info = {}
        clear_review_checkbox_keys()
        st.rerun()


# =========================
# 탭 구성
# =========================
tab_names = list(word_themes.keys()) + ["🎧 전체 단어 듣기", "⭐ 복습 희망"]
tabs = st.tabs(tab_names)

for tab, theme_name in zip(tabs[:-2], word_themes.keys()):
    with tab:
        theme_words = word_themes[theme_name]

        st.markdown(
            f"""
            <div class="theme-header">
                <div class="theme-title">{theme_name}</div>
                <div class="theme-desc">{len(theme_words)}개의 일상 단어를 듣고 익혀 봅시다.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        show_cassette_player(theme_words, theme_name)
        show_word_cards(theme_words, theme_name)

with tabs[-2]:
    show_all_cassette_tab()

with tabs[-1]:
    show_unknown_words_tab()
