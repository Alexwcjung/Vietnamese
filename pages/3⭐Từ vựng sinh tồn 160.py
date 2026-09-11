
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

# =========================
# =========================
st.set_page_config(
    page_title="Survival English 160 - Vietnamese",
    page_icon="🛟",
    layout="wide"
)

# =========================
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
        background: linear-gradient(135deg, #ecfeff 0%, #fef3c7 50%, #fce7f3 100%);
        border-radius: 22px;
        padding: 18px 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        border: 1px solid rgba(255,255,255,0.8);
    }

    .hero-title {
        font-size: 27px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 10px;
    }

    .hero-text {
        font-size: 16px;
        color: #374151;
        line-height: 1.8;
    }

    .theme-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 50%, #ec4899 100%);
        color: white;
        padding: 30px 32px;
        border-radius: 28px;
        margin-bottom: 26px;
        box-shadow: 0 10px 24px rgba(14,165,233,0.28);
    }

    .theme-title {
        font-size: 40px;
        font-weight: 1000;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }

    .theme-desc {
        font-size: 19px;
        font-weight: 800;
        opacity: 0.98;
        line-height: 1.55;
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
        font-size: 24px;
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
        border: 1px solid #e0f2fe;
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
        color: #0369a1;
        background: #e0f2fe;
        border-radius: 999px;
        padding: 5px 9px;
        text-align: center;
    }

    .word-text {
        min-width: 170px;
        font-size: 25px;
        font-weight: 900;
        color: #111827;
        white-space: nowrap;
    }

    .meaning-text {
        font-size: 19px;
        font-weight: 800;
        color: #374151;
        margin-left: 8px;
        white-space: nowrap;
        line-height: 42px;
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
        border: 1px solid #e9d5ff;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }

    .quiz-number {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
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

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: 1px solid #d1d5db;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        border-color: #0ea5e9;
        color: #0ea5e9;
    }


    
    div[data-baseweb="tab-list"] {
        gap: 10px;
        flex-wrap: wrap;
    }

    button[data-baseweb="tab"] {
        min-height: 58px;
        padding: 12px 18px;
        border-radius: 18px 18px 0 0;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        margin-right: 4px;
    }

    button[data-baseweb="tab"] p {
        font-size: 21px !important;
        font-weight: 1000 !important;
        color: #111827 !important;
        line-height: 1.25 !important;
        white-space: nowrap;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #dbeafe, #fce7f3);
        border-bottom: 4px solid #8b5cf6;
    }

    
    div[role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 900 !important;
    }

    @media (max-width: 600px) {
        .main-title {
            font-size: 34px;
        }

        .theme-header {
            padding: 24px 22px;
            border-radius: 24px;
        }

        .theme-title {
            font-size: 33px;
        }

        .theme-desc {
            font-size: 16px;
        }

        button[data-baseweb="tab"] {
            min-height: 52px;
            padding: 10px 14px;
        }

        button[data-baseweb="tab"] p {
            font-size: 18px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# =========================
st.markdown("<div class='main-title'>🛟 Survival English 160</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>Listen, repeat, and practice essential survival English words and sentences.</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-text" style="font-size:18px; font-weight:900; color:#374151;">
            Memorize these 160 words to survive basic communication in English.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# Meaning language: Vietnamese only
# =========================
meaning_language = "Vietnamese"

# =========================
# =========================
def make_google_tts_url(text, lang="en"):
    clean_text = str(text).strip()
    if not clean_text:
        clean_text = "Hello"
    encoded = quote(clean_text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded}"


@st.cache_data(show_spinner=False)
def get_tts_mp3_bytes(text, lang="en"):
    """Fetch Google TTS mp3 with requests and play it with st.audio."""
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
        raise ValueError("   .")
    return audio_bytes


def make_tts_audio(text, lang="en", tld="com"):
    """Compatibility wrapper."""
    return get_tts_mp3_bytes(text, lang=lang)


def remove_speaker_label(sentence):
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(dialogue):
    return " ".join([remove_speaker_label(item["en"]) for item in dialogue])


def play_audio_block(text, label="🔊 Listen", show_link=True, key=None):
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
            st.error("Could not create audio. Please check that requests is in requirements.txt.")
            st.caption(f"Error: {e}")
            if show_link:
                st.link_button("🔊 Listen in new window", make_google_tts_url(text, lang="en"), use_container_width=True)


def direct_audio_player(text, show_link=True, lang="en"):
    """Word-card audio player. Supports English and Vietnamese TTS."""
    text = str(text).strip()
    if not text:
        return

    try:
        audio_bytes = get_tts_mp3_bytes(text, lang=lang)
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("Could not create audio.")
        st.caption(f"Error: {e}")
        if show_link:
            st.link_button("🔊 Listen in new window", make_google_tts_url(text, lang=lang), use_container_width=True)


# =========================
# =========================
word_themes = {
    "🧍 Tôi và con người": [
        {"word": "I", "meaning": "tôi"},
        {"word": "you", "meaning": "bạn"},
        {"word": "he", "meaning": "anh ấy"},
        {"word": "she", "meaning": "cô ấy"},
        {"word": "we", "meaning": "chúng tôi"},
        {"word": "they", "meaning": "họ"},
        {"word": "friend", "meaning": "bạn bè"},
        {"word": "teacher", "meaning": "giáo viên"},
        {"word": "student", "meaning": "học sinh"},
        {"word": "classmate", "meaning": "bạn cùng lớp"},
        {"word": "family", "meaning": "gia đình"},
        {"word": "father", "meaning": "bố"},
        {"word": "mother", "meaning": "mẹ"},
        {"word": "brother", "meaning": "anh/em trai"},
        {"word": "sister", "meaning": "chị/em gái"},
        {"word": "name", "meaning": "tên"},
        {"word": "person", "meaning": "người"},
        {"word": "man", "meaning": "đàn ông"},
        {"word": "woman", "meaning": "phụ nữ"},
        {"word": "child", "meaning": "trẻ em"},
    ],
    "🏃 Hành động cơ bản": [
        {"word": "go", "meaning": "đi"},
        {"word": "come", "meaning": "đến"},
        {"word": "walk", "meaning": "đi bộ"},
        {"word": "run", "meaning": "chạy"},
        {"word": "sit", "meaning": "ngồi"},
        {"word": "stand", "meaning": "đứng"},
        {"word": "stop", "meaning": "dừng lại"},
        {"word": "start", "meaning": "bắt đầu"},
        {"word": "open", "meaning": "mở"},
        {"word": "close", "meaning": "đóng"},
        {"word": "eat", "meaning": "ăn"},
        {"word": "drink", "meaning": "uống"},
        {"word": "sleep", "meaning": "ngủ"},
        {"word": "study", "meaning": "học"},
        {"word": "read", "meaning": "đọc"},
        {"word": "write", "meaning": "viết"},
        {"word": "listen", "meaning": "nghe"},
        {"word": "speak", "meaning": "nói"},
        {"word": "help", "meaning": "giúp đỡ"},
        {"word": "wait", "meaning": "chờ"},
    ],
    "💖 Cảm xúc và cơ thể": [
        {"word": "happy", "meaning": "vui vẻ"},
        {"word": "sad", "meaning": "buồn"},
        {"word": "angry", "meaning": "tức giận"},
        {"word": "tired", "meaning": "mệt"},
        {"word": "hungry", "meaning": "đói"},
        {"word": "thirsty", "meaning": "khát"},
        {"word": "sick", "meaning": "ốm"},
        {"word": "okay", "meaning": "ổn"},
        {"word": "fine", "meaning": "khỏe / ổn"},
        {"word": "cold", "meaning": "lạnh"},
        {"word": "hot", "meaning": "nóng"},
        {"word": "pain", "meaning": "đau"},
        {"word": "headache", "meaning": "đau đầu"},
        {"word": "stomachache", "meaning": "đau bụng"},
        {"word": "fever", "meaning": "sốt"},
        {"word": "hurt", "meaning": "đau / bị thương"},
        {"word": "good", "meaning": "tốt"},
        {"word": "bad", "meaning": "xấu / tệ"},
        {"word": "worried", "meaning": "lo lắng"},
        {"word": "scared", "meaning": "sợ"},
    ],
    "🍎 Đồ ăn và nước": [
        {"word": "food", "meaning": "đồ ăn"},
        {"word": "water", "meaning": "nước"},
        {"word": "rice", "meaning": "cơm / gạo"},
        {"word": "bread", "meaning": "bánh mì"},
        {"word": "milk", "meaning": "sữa"},
        {"word": "juice", "meaning": "nước ép"},
        {"word": "coffee", "meaning": "cà phê"},
        {"word": "tea", "meaning": "trà"},
        {"word": "apple", "meaning": "quả táo"},
        {"word": "banana", "meaning": "quả chuối"},
        {"word": "egg", "meaning": "trứng"},
        {"word": "meat", "meaning": "thịt"},
        {"word": "chicken", "meaning": "gà / thịt gà"},
        {"word": "fish", "meaning": "cá"},
        {"word": "breakfast", "meaning": "bữa sáng"},
        {"word": "lunch", "meaning": "bữa trưa"},
        {"word": "dinner", "meaning": "bữa tối"},
        {"word": "snack", "meaning": "đồ ăn nhẹ"},
        {"word": "medicine", "meaning": "thuốc"},
        {"word": "hospital", "meaning": "bệnh viện"},
    ],
    "🚗 Địa điểm và di chuyển": [
        {"word": "home", "meaning": "nhà"},
        {"word": "school", "meaning": "trường học"},
        {"word": "classroom", "meaning": "lớp học"},
        {"word": "bathroom", "meaning": "nhà vệ sinh"},
        {"word": "hospital", "meaning": "bệnh viện"},
        {"word": "store", "meaning": "cửa hàng"},
        {"word": "station", "meaning": "nhà ga"},
        {"word": "bus", "meaning": "xe buýt"},
        {"word": "car", "meaning": "ô tô"},
        {"word": "taxi", "meaning": "taxi"},
        {"word": "train", "meaning": "tàu hỏa"},
        {"word": "bike", "meaning": "xe đạp"},
        {"word": "road", "meaning": "đường"},
        {"word": "street", "meaning": "đường phố"},
        {"word": "here", "meaning": "ở đây"},
        {"word": "there", "meaning": "ở đó"},
        {"word": "near", "meaning": "gần"},
        {"word": "far", "meaning": "xa"},
        {"word": "left", "meaning": "bên trái"},
        {"word": "right", "meaning": "bên phải / đúng"},
    ],
    "⏰ Thời gian và số": [
        {"word": "time", "meaning": "thời gian"},
        {"word": "now", "meaning": "bây giờ"},
        {"word": "today", "meaning": "hôm nay"},
        {"word": "tomorrow", "meaning": "ngày mai"},
        {"word": "yesterday", "meaning": "hôm qua"},
        {"word": "morning", "meaning": "buổi sáng"},
        {"word": "afternoon", "meaning": "buổi chiều"},
        {"word": "evening", "meaning": "buổi tối"},
        {"word": "night", "meaning": "ban đêm"},
        {"word": "nine", "meaning": "chín"},
        {"word": "late", "meaning": "muộn"},
        {"word": "one", "meaning": "một"},
        {"word": "two", "meaning": "hai"},
        {"word": "three", "meaning": "ba"},
        {"word": "four", "meaning": "bốn"},
        {"word": "five", "meaning": "năm"},
        {"word": "six", "meaning": "sáu"},
        {"word": "seven", "meaning": "bảy"},
        {"word": "eight", "meaning": "tám"},
        {"word": "ten", "meaning": "mười"},
    ],
    "🎒 Đồ vật và tiền": [
        {"word": "bag", "meaning": "cặp / túi"},
        {"word": "phone", "meaning": "điện thoại"},
        {"word": "book", "meaning": "sách"},
        {"word": "notebook", "meaning": "vở"},
        {"word": "pen", "meaning": "bút mực"},
        {"word": "pencil", "meaning": "bút chì"},
        {"word": "desk", "meaning": "bàn học"},
        {"word": "chair", "meaning": "ghế"},
        {"word": "door", "meaning": "cửa"},
        {"word": "window", "meaning": "cửa sổ"},
        {"word": "key", "meaning": "chìa khóa"},
        {"word": "money", "meaning": "tiền"},
        {"word": "card", "meaning": "thẻ"},
        {"word": "ticket", "meaning": "vé"},
        {"word": "clothes", "meaning": "quần áo"},
        {"word": "shoes", "meaning": "giày"},
        {"word": "hat", "meaning": "mũ"},
        {"word": "watch", "meaning": "đồng hồ"},
        {"word": "cup", "meaning": "cốc"},
        {"word": "bottle", "meaning": "chai"},
    ],
    "🆘 Yêu cầu giúp đỡ": [
        {"word": "help", "meaning": "giúp đỡ"},
        {"word": "please", "meaning": "làm ơn"},
        {"word": "sorry", "meaning": "xin lỗi"},
        {"word": "excuse me", "meaning": "xin lỗi / làm ơn cho hỏi"},
        {"word": "again", "meaning": "lại / một lần nữa"},
        {"word": "slowly", "meaning": "chậm rãi"},
        {"word": "understand", "meaning": "hiểu"},
        {"word": "question", "meaning": "câu hỏi"},
        {"word": "problem", "meaning": "vấn đề"},
        {"word": "need", "meaning": "cần"},
        {"word": "want", "meaning": "muốn"},
        {"word": "know", "meaning": "biết"},
        {"word": "say", "meaning": "nói"},
        {"word": "tell", "meaning": "nói / kể"},
        {"word": "ask", "meaning": "hỏi"},
        {"word": "answer", "meaning": "câu trả lời"},
        {"word": "repeat", "meaning": "lặp lại"},
        {"word": "speak", "meaning": "nói"},
        {"word": "look", "meaning": "nhìn"},
        {"word": "listen", "meaning": "nghe"},
    ],
}


# =========================
# =========================
VI_MEANINGS = {
    "I": "tôi",
    "you": "bạn",
    "he": "anh ấy",
    "she": "cô ấy",
    "we": "chúng tôi",
    "they": "họ",
    "friend": "bạn bè",
    "teacher": "giáo viên",
    "student": "học sinh",
    "classmate": "bạn cùng lớp",
    "family": "gia đình",
    "father": "bố",
    "mother": "mẹ",
    "brother": "anh/em trai",
    "sister": "chị/em gái",
    "name": "tên",
    "person": "người",
    "man": "đàn ông",
    "woman": "phụ nữ",
    "child": "trẻ em",

    "go": "đi",
    "come": "đến",
    "walk": "đi bộ",
    "run": "chạy",
    "sit": "ngồi",
    "stand": "đứng",
    "stop": "dừng lại",
    "start": "bắt đầu",
    "open": "mở",
    "close": "đóng",
    "eat": "ăn",
    "drink": "uống",
    "sleep": "ngủ",
    "study": "học",
    "read": "đọc",
    "write": "viết",
    "listen": "nghe",
    "speak": "nói",
    "help": "giúp đỡ",
    "wait": "chờ",

    "happy": "vui vẻ",
    "sad": "buồn",
    "angry": "tức giận",
    "tired": "mệt",
    "hungry": "đói",
    "thirsty": "khát",
    "sick": "ốm",
    "okay": "ổn",
    "fine": "khỏe / ổn",
    "cold": "lạnh",
    "hot": "nóng",
    "pain": "đau",
    "headache": "đau đầu",
    "stomachache": "đau bụng",
    "fever": "sốt",
    "hurt": "đau / bị thương",
    "good": "tốt",
    "bad": "xấu / tệ",
    "worried": "lo lắng",
    "scared": "sợ",

    "food": "đồ ăn",
    "water": "nước",
    "rice": "cơm / gạo",
    "bread": "bánh mì",
    "milk": "sữa",
    "juice": "nước ép",
    "coffee": "cà phê",
    "tea": "trà",
    "apple": "quả táo",
    "banana": "quả chuối",
    "egg": "trứng",
    "meat": "thịt",
    "chicken": "gà / thịt gà",
    "fish": "cá",
    "breakfast": "bữa sáng",
    "lunch": "bữa trưa",
    "dinner": "bữa tối",
    "snack": "đồ ăn nhẹ",
    "medicine": "thuốc",
    "hospital": "bệnh viện",

    "home": "nhà",
    "school": "trường học",
    "classroom": "lớp học",
    "bathroom": "nhà vệ sinh",
    "store": "cửa hàng",
    "station": "nhà ga",
    "bus": "xe buýt",
    "car": "ô tô",
    "taxi": "taxi",
    "train": "tàu hỏa",
    "bike": "xe đạp",
    "road": "đường",
    "street": "đường phố",
    "here": "ở đây",
    "there": "ở đó",
    "near": "gần",
    "far": "xa",
    "left": "bên trái",
    "right": "bên phải / đúng",

    "time": "thời gian",
    "now": "bây giờ",
    "today": "hôm nay",
    "tomorrow": "ngày mai",
    "yesterday": "hôm qua",
    "morning": "buổi sáng",
    "afternoon": "buổi chiều",
    "evening": "buổi tối",
    "night": "ban đêm",
    "early": "sớm",
    "late": "muộn",
    "one": "một",
    "two": "hai",
    "three": "ba",
    "four": "bốn",
    "five": "năm",
    "six": "sáu",
    "seven": "bảy",
    "eight": "tám",
    "nine": "chín",
    "ten": "mười",

    "bag": "cặp / túi",
    "phone": "điện thoại",
    "book": "sách",
    "notebook": "vở",
    "pen": "bút mực",
    "pencil": "bút chì",
    "desk": "bàn học",
    "chair": "ghế",
    "door": "cửa",
    "window": "cửa sổ",
    "key": "chìa khóa",
    "money": "tiền",
    "card": "thẻ",
    "ticket": "vé",
    "clothes": "quần áo",
    "shoes": "giày",
    "hat": "mũ",
    "watch": "đồng hồ",
    "cup": "cốc",
    "bottle": "chai",

    "please": "làm ơn",
    "sorry": "xin lỗi",
    "excuse me": "xin lỗi / làm ơn cho hỏi",
    "again": "lại / một lần nữa",
    "slowly": "chậm rãi",
    "understand": "hiểu",
    "question": "câu hỏi",
    "problem": "vấn đề",
    "need": "cần",
    "want": "muốn",
    "know": "biết",
    "say": "nói",
    "tell": "nói / kể",
    "ask": "hỏi",
    "answer": "câu trả lời",
    "repeat": "lặp lại",
    "look": "nhìn",
}

def get_display_meaning(word, default_meaning):
    """Always show Vietnamese meaning for English learning."""
    return VI_MEANINGS.get(str(word).strip(), default_meaning)


# =========================
# =========================
CASSETTE_EXAMPLES = {
    "I": "I am a student.", "you": "You are my friend.", "he": "He is my friend.", "she": "She is a student.",
    "we": "We are happy.", "they": "They are students.", "friend": "He is my friend.", "teacher": "She is my teacher.",
    "student": "I am a student.", "classmate": "He is my classmate.", "family": "This is my family.",
    "father": "He is my father.", "mother": "She is my mother.", "brother": "He is my brother.",
    "sister": "She is my sister.", "name": "My name is Alex.", "person": "He is a good person.",
    "man": "He is a man.", "woman": "She is a woman.", "child": "He is a child.",

    "go": "I go to school.", "come": "Please come here.", "walk": "I walk to school.", "run": "I can run.",
    "sit": "Please sit down.", "stand": "Please stand up.", "stop": "Please stop.", "start": "Let's start.",
    "open": "Open the door.", "close": "Close the door.", "eat": "I eat lunch.", "drink": "I drink water.",
    "sleep": "I sleep at night.", "study": "I study English.", "read": "I read a book.", "write": "I write my name.",
    "listen": "Listen carefully.", "speak": "Please speak slowly.", "help": "Can you help me?", "wait": "Please wait.",

    "happy": "I am happy.", "sad": "I am sad.", "angry": "I am angry.", "tired": "I am tired.",
    "hungry": "I am hungry.", "thirsty": "I am thirsty.", "sick": "I am sick.", "okay": "I am okay.",
    "fine": "I am fine.", "cold": "I am cold.", "hot": "It is hot.", "pain": "I have pain.",
    "headache": "I have a headache.", "stomachache": "I have a stomachache.", "fever": "I have a fever.",
    "hurt": "My leg hurts.", "good": "It is good.", "bad": "It is bad.", "worried": "I am worried.",
    "scared": "I am scared.",

    "food": "I need food.", "water": "I need water.", "rice": "I eat rice.", "bread": "I eat bread.",
    "milk": "I drink milk.", "juice": "I drink juice.", "coffee": "I drink coffee.", "tea": "I drink tea.",
    "apple": "I like apples.", "banana": "I like bananas.", "egg": "I eat an egg.", "meat": "I eat meat.",
    "chicken": "I like chicken.", "fish": "I eat fish.", "breakfast": "I eat breakfast.", "lunch": "I eat lunch.",
    "dinner": "I eat dinner.", "snack": "I want a snack.", "medicine": "I need medicine.", "hospital": "I need a hospital.",

    "home": "I go home.", "school": "I go to school.", "classroom": "This is my classroom.",
    "bathroom": "Where is the bathroom?", "store": "I go to the store.", "station": "Where is the station?",
    "bus": "I take a bus.", "car": "This is my car.", "taxi": "I need a taxi.", "train": "I take a train.",
    "bike": "I ride a bike.", "road": "This road is long.", "street": "This street is busy.",
    "here": "Come here.", "there": "Go there.", "near": "It is near here.", "far": "It is far.",
    "left": "Turn left.", "right": "Turn right.",

    "time": "What time is it?", "now": "I am here now.", "today": "Today is Monday.",
    "tomorrow": "See you tomorrow.", "yesterday": "I studied yesterday.", "morning": "Good morning.",
    "afternoon": "Good afternoon.", "evening": "Good evening.", "night": "Good night.",
    "early": "It is early.", "late": "It is late.", "one": "I have one book.", "two": "I have two books.",
    "three": "I have three books.", "four": "I have four books.", "five": "I have five books.",
    "six": "I have six books.", "seven": "I have seven books.", "eight": "I have eight books.",
    "nine": "I have nine books.", "ten": "I have ten books.",

    "bag": "This is my bag.", "phone": "This is my phone.", "book": "This is my book.",
    "notebook": "This is my notebook.", "pen": "I have a pen.", "pencil": "I have a pencil.",
    "desk": "This is my desk.", "chair": "This is my chair.", "door": "Open the door.",
    "window": "Close the window.", "key": "I need a key.", "money": "I need money.",
    "card": "I have a card.", "ticket": "I need a ticket.", "clothes": "These are my clothes.",
    "shoes": "These are my shoes.", "hat": "This is my hat.", "watch": "This is my watch.",
    "cup": "This is my cup.", "bottle": "This is my bottle.",

    "please": "Please help me.", "sorry": "I am sorry.", "excuse me": "Excuse me.",
    "again": "Please say it again.", "slowly": "Please speak slowly.", "understand": "I understand.",
    "question": "I have a question.", "problem": "I have a problem.", "need": "I need help.",
    "want": "I want water.", "know": "I know.", "say": "Please say it again.",
    "tell": "Please tell me.", "ask": "Can I ask you?", "answer": "This is the answer.",
    "repeat": "Please repeat.", "look": "Look at this.",
}

CASSETTE_EXAMPLES_KO = {}

# =========================
# Word emojis
# =========================
WORD_EMOJIS = {
    "I": "🙋", "you": "👉", "he": "👦", "she": "👧", "we": "👥", "they": "👥",
    "friend": "🤝", "teacher": "👩‍🏫", "student": "🧑‍🎓", "classmate": "👫", "family": "👨‍👩‍👧",
    "father": "👨", "mother": "👩", "brother": "👦", "sister": "👧", "name": "🏷️",
    "person": "🧍", "man": "👨", "woman": "👩", "child": "🧒",
    "go": "➡️", "come": "⬅️", "walk": "🚶", "run": "🏃", "sit": "🪑", "stand": "🧍",
    "stop": "🛑", "start": "▶️", "open": "📂", "close": "📕", "eat": "🍽️", "drink": "🥤",
    "sleep": "😴", "study": "📚", "read": "📖", "write": "✏️", "listen": "👂", "speak": "🗣️",
    "help": "🆘", "wait": "⏳",
    "happy": "😊", "sad": "😢", "angry": "😠", "tired": "🥱", "hungry": "😋", "thirsty": "🥤",
    "sick": "🤒", "okay": "👌", "fine": "🙂", "cold": "🥶", "hot": "🥵", "pain": "🤕",
    "headache": "🤯", "stomachache": "🤢", "fever": "🌡️", "hurt": "🩹", "good": "👍", "bad": "👎",
    "worried": "😟", "scared": "😨",
    "food": "🍽️", "water": "💧", "rice": "🍚", "bread": "🍞", "milk": "🥛", "juice": "🧃",
    "coffee": "☕", "tea": "🍵", "apple": "🍎", "banana": "🍌", "egg": "🥚", "meat": "🥩",
    "chicken": "🍗", "fish": "🐟", "breakfast": "🍳", "lunch": "🍱", "dinner": "🍽️", "snack": "🍪",
    "medicine": "💊", "hospital": "🏥",
    "home": "🏠", "school": "🏫", "classroom": "🧑‍🏫", "bathroom": "🚻", "store": "🏪", "station": "🚉",
    "bus": "🚌", "car": "🚗", "taxi": "🚕", "train": "🚆", "bike": "🚲", "road": "🛣️",
    "street": "🏙️", "here": "📍", "there": "📌", "near": "↔️", "far": "🌁", "left": "⬅️", "right": "➡️",
    "time": "⏰", "now": "🕒", "today": "📅", "tomorrow": "➡️📅", "yesterday": "⬅️📅",
    "morning": "🌅", "afternoon": "☀️", "evening": "🌆", "night": "🌙", "early": "🐓", "late": "🌃",
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣",
    "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣", "ten": "🔟",
    "bag": "🎒", "phone": "📱", "book": "📘", "notebook": "📓", "pen": "🖊️", "pencil": "✏️",
    "desk": "🪑", "chair": "🪑", "door": "🚪", "window": "🪟", "key": "🔑", "money": "💵",
    "card": "💳", "ticket": "🎫", "clothes": "👕", "shoes": "👟", "hat": "🧢", "watch": "⌚",
    "cup": "☕", "bottle": "🍼",
    "please": "🙏", "sorry": "🙇", "excuse me": "🙋", "again": "🔁", "slowly": "🐢",
    "understand": "💡", "question": "❓", "problem": "⚠️", "need": "📌", "want": "✨",
    "know": "🧠", "say": "💬", "tell": "📣", "ask": "❔", "answer": "✅",
    "repeat": "🔁", "look": "👀",
}


def get_word_emoji(word):
    return WORD_EMOJIS.get(word, "🌱")


# =========================
# =========================
def audio_button(label, text, key=None, lang="en"):
    direct_audio_player(text, lang=lang)


def html_dialogue_audio_player(label, dialogue_lines, line_pause_ms=1400, height=105):
    dialogue_text = make_dialogue_tts_text(dialogue_lines)
    play_audio_block(
        dialogue_text,
        label=label,
        key="dialogue_" + hashlib.md5(dialogue_text.encode("utf-8")).hexdigest()
    )


# =========================
# Survival Dialogue
# =========================
theme_dialogues = {
    "🧍 Tôi và con người": [
        {"en": "A: Hello. What is your name?", "ko": "A: Xin chào. Tên của bạn là gì?"},
        {"en": "B: My name is Alex.", "ko": "B: Tên tôi là Alex."},
        {"en": "A: Are you a student?", "ko": "A: Bạn có phải là học sinh không?"},
        {"en": "B: Yes, I am a student.", "ko": "B: Vâng, tôi là học sinh."},
        {"en": "A: Is he your friend?", "ko": "A: Anh ấy có phải là bạn của bạn không?"},
        {"en": "B: Yes, he is my friend.", "ko": "B: Vâng, anh ấy là bạn của tôi."},
    ],
    "🏃 Hành động cơ bản": [
        {"en": "A: Can you come here?", "ko": "A: Bạn có thể đến đây không?"},
        {"en": "B: Yes, I can come.", "ko": "B: Vâng, tôi có thể đến."},
        {"en": "A: Please sit down.", "ko": "A: Làm ơn ngồi xuống."},
        {"en": "B: Okay. I will sit down.", "ko": "B: Được rồi. Tôi sẽ ngồi xuống."},
        {"en": "A: Can you help me?", "ko": "A: Bạn có thể giúp tôi không?"},
        {"en": "B: Yes, I can help you.", "ko": "B: Vâng, tôi có thể giúp bạn."},
    ],
    "💖 Cảm xúc và cơ thể": [
        {"en": "A: Are you okay?", "ko": "A: Bạn ổn không?"},
        {"en": "B: No, I am tired.", "ko": "B: Không, tôi mệt."},
        {"en": "A: Are you hungry?", "ko": "A: Bạn có đói không?"},
        {"en": "B: Yes, I am hungry.", "ko": "B: Vâng, tôi đói."},
        {"en": "A: Are you sick?", "ko": "A: Bạn bị ốm à?"},
        {"en": "B: Yes, I am sick.", "ko": "B: Vâng, tôi bị ốm."},
    ],
    "🍎 Đồ ăn và nước": [
        {"en": "A: Are you thirsty?", "ko": "A: Bạn có khát không?"},
        {"en": "B: Yes, I need water.", "ko": "B: Vâng, tôi cần nước."},
        {"en": "A: Do you want food?", "ko": "A: Bạn có cần đồ ăn không?"},
        {"en": "B: Yes, I want food.", "ko": "B: Vâng, tôi cần đồ ăn."},
        {"en": "A: Do you like apples?", "ko": "A: Bạn có thích táo không?"},
        {"en": "B: Yes, I like apples.", "ko": "B: Vâng, tôi thích táo."},
    ],
    "🚗 Địa điểm và di chuyển": [
        {"en": "A: Where is the bathroom?", "ko": "A: Nhà vệ sinh ở đâu?"},
        {"en": "B: It is near here.", "ko": "B: Nó ở gần đây."},
        {"en": "A: I want to go home.", "ko": "A: Tôi muốn về nhà."},
        {"en": "B: You can go by bus.", "ko": "B: Bạn có thể đi bằng xe buýt."},
        {"en": "A: Where is the station?", "ko": "A: Nhà ga ở đâu?"},
        {"en": "B: It is not far.", "ko": "B: Nó không xa."},
    ],
    "⏰ Thời gian và số": [
        {"en": "A: What time is it?", "ko": "A: Bây giờ là mấy giờ?"},
        {"en": "B: It is three.", "ko": "B: Bây giờ là ba giờ."},
        {"en": "A: Is it morning?", "ko": "A: Bây giờ là buổi sáng à?"},
        {"en": "B: No, it is afternoon.", "ko": "B: Không, bây giờ là buổi chiều."},
        {"en": "A: Do you study today?", "ko": "A: Hôm nay bạn có học không?"},
        {"en": "B: Yes, I study today.", "ko": "B: Vâng, hôm nay tôi học."},
    ],
    "🎒 Đồ vật và tiền": [
        {"en": "A: Where is my phone?", "ko": "A: Điện thoại của tôi ở đâu?"},
        {"en": "B: It is in your bag.", "ko": "B: Nó ở trong túi của bạn."},
        {"en": "A: Do you have money?", "ko": "A: Bạn có tiền không?"},
        {"en": "B: No, I do not have money.", "ko": "B: Không, tôi không có tiền."},
        {"en": "A: Is this your book?", "ko": "A: Đây có phải là sách của bạn không?"},
        {"en": "B: Yes, it is my book.", "ko": "B: Vâng, đó là sách của tôi."},
    ],
    "🆘 Yêu cầu giúp đỡ": [
        {"en": "A: Excuse me.", "ko": "A: Xin lỗi."},
        {"en": "B: Yes?", "ko": "B: Vâng?"},
        {"en": "A: I don't understand.", "ko": "A: Tôi không hiểu."},
        {"en": "B: Okay. I will say it again.", "ko": "B: Được rồi. Tôi sẽ nói lại."},
        {"en": "A: Please speak slowly.", "ko": "A: Làm ơn nói chậm lại."},
        {"en": "B: Sure. I can help you.", "ko": "B: Tất nhiên. Tôi có thể giúp bạn."},
    ],
}



# =========================
# =========================
if "unknown_words" not in st.session_state:
    st.session_state.unknown_words = []

if "unknown_word_info" not in st.session_state:
    st.session_state.unknown_word_info = {}


def add_unknown_word(word, meaning, theme_name):
    if word not in st.session_state.unknown_words:
        st.session_state.unknown_words.append(word)

    st.session_state.unknown_word_info[word] = {
        "meaning": meaning,
        "theme": theme_name,
    }


def remove_unknown_word(word):
    if word in st.session_state.unknown_words:
        st.session_state.unknown_words.remove(word)

    if word in st.session_state.unknown_word_info:
        del st.session_state.unknown_word_info[word]



def clear_review_checkbox_keys():
    """
    Remove checkbox keys when clearing the review list.
    """
    keys_to_delete = [
        key for key in list(st.session_state.keys())
        if "_unknown_" in str(key)
    ]

    for key in keys_to_delete:
        del st.session_state[key]


def toggle_unknown_word(word, meaning, theme_name):
    if word in st.session_state.unknown_words:
        remove_unknown_word(word)
    else:
        add_unknown_word(word, meaning, theme_name)


# =========================
# =========================
def get_example_sentence(word):
    return CASSETTE_EXAMPLES.get(word, f"This is {word}.")


def get_example_sentence_ko(word):
    return CASSETTE_EXAMPLES_KO.get(word, "This is a survival English sentence using the word.")


def flatten_survival_words():
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


def js_cassette_visual_player(items, audio_payloads, title="📼 Word Cassette", height=560):
    """
    Cassette player with play, previous, next, speed, and repeat controls.
    """
    player_id = "survival_cassette_" + uuid.uuid4().hex

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
                    <div id="emoji_{player_id}" style="font-size:46px; line-height:1.05; margin:2px 0;">🛟</div>
                    <div id="word_{player_id}" style="font-size:clamp(36px,7.8vw,62px); font-weight:1000; color:#111827; line-height:1.05; word-break:break-word; letter-spacing:-1px;">Ready</div>
                    <div id="meaning_{player_id}" style="font-size:clamp(20px,4.4vw,30px); font-weight:900; color:#334155; margin-top:10px; word-break:keep-all;">Press play to start.</div>
                    <div style="width:100%; height:14px; background:#e2e8f0; border-radius:999px; overflow:hidden; margin-top:12px;">
                        <div id="bar_{player_id}" style="height:100%; width:0%; background:linear-gradient(90deg,#22c55e,#0ea5e9,#8b5cf6); border-radius:999px;"></div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns:1fr; gap:8px;">
                    <button id="play_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #86efac; background:linear-gradient(135deg,#dcfce7,#dbeafe); font-size:13px; font-weight:900; cursor:pointer; box-shadow:0 3px 9px rgba(15,23,42,0.08);">▶️ Play</button>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <button id="prev_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">⏮ Previous</button>
                    <button id="next_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">Next ⏭</button>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <div style="background:rgba(255,255,255,0.88); border:1px solid #dcfce7; border-radius:16px; padding:9px 11px;">
                        <div style="font-size:12px; font-weight:900; color:#64748b; margin-bottom:4px;">Speed</div>
                        <select id="speed_{player_id}" style="width:100%; border:0; background:transparent; font-size:14px; font-weight:900; color:#0f172a; outline:none;">
                            <option value="0.75">Slow</option>
                            <option value="1" selected>Normal</option>
                            <option value="1.15">A little faster</option>
                            <option value="1.3">Fast</option>
                        </select>
                    </div>
                    <div style="background:rgba(255,255,255,0.88); border:1px solid #dcfce7; border-radius:16px; padding:9px 11px;">
                        <div style="font-size:12px; font-weight:900; color:#64748b; margin-bottom:4px;">Repeat all</div>
                        <select id="loop_{player_id}" style="width:100%; border:0; background:transparent; font-size:14px; font-weight:900; color:#0f172a; outline:none;">
                            <option value="1" selected>1 time</option>
                            <option value="2">2 times</option>
                            <option value="3">3 times</option>
                        </select>
                    </div>
                </div>

                <div id="status_{player_id}" style="font-size:14px; font-weight:900; color:#075985; min-height:22px;">Ready</div>
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
        const speedSelect_{player_id} = document.getElementById("speed_{player_id}");
        const loopSelect_{player_id} = document.getElementById("loop_{player_id}");

        let currentIndex_{player_id} = 0;
        let currentLoop_{player_id} = 1;
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
            themeEl_{player_id}.textContent = it.theme || "Survival English";
            countEl_{player_id}.textContent = (idx + 1) + " / " + items_{player_id}.length + " · " + currentLoop_{player_id} + "round";

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
            audio_{player_id}.playbackRate = parseFloat(speedSelect_{player_id}.value || "1");
        }}

        function playCurrent_{player_id}() {{
            if (!items_{player_id}.length) return;
            isPlayingList_{player_id} = true;
            isFinished_{player_id} = false;
            loadCurrent_{player_id}();
            playBtn_{player_id}.textContent = "⏸ Pause";
            statusEl_{player_id}.textContent = "Current word: " + items_{player_id}[currentIndex_{player_id}].word;
            audio_{player_id}.play().catch(() => {{
                statusEl_{player_id}.textContent = "  Play . Play      .";
                playBtn_{player_id}.textContent = "▶️ Play";
            }});
        }}

        function pauseCurrent_{player_id}() {{
            isPlayingList_{player_id} = false;
            audio_{player_id}.pause();
            playBtn_{player_id}.textContent = "▶️  Listen";
            statusEl_{player_id}.textContent = "Paused";
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
                playBtn_{player_id}.textContent = "▶️ Play";
                statusEl_{player_id}.textContent = "Selected word: " + items_{player_id}[currentIndex_{player_id}].word;
            }}
        }}

        loadCurrent_{player_id}();

        speedSelect_{player_id}.addEventListener("change", function() {{
            audio_{player_id}.playbackRate = parseFloat(speedSelect_{player_id}.value || "1");
        }});

        playBtn_{player_id}.addEventListener("click", function() {{
            if (isPlayingList_{player_id}) {{
                pauseCurrent_{player_id}();
            }} else {{
                if (isFinished_{player_id}) {{
                    currentIndex_{player_id} = 0;
                    currentLoop_{player_id} = 1;
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
            const maxLoop = parseInt(loopSelect_{player_id}.value || "1");
            if (currentIndex_{player_id} < items_{player_id}.length - 1) {{
                currentIndex_{player_id} += 1;
                playCurrent_{player_id}();
            }} else if (currentLoop_{player_id} < maxLoop) {{
                currentLoop_{player_id} += 1;
                currentIndex_{player_id} = 0;
                playCurrent_{player_id}();
            }} else {{
                isPlayingList_{player_id} = false;
                isFinished_{player_id} = true;
                playBtn_{player_id}.textContent = "▶️  again";
                statusEl_{player_id}.textContent = "✅  Play ";
                barEl_{player_id}.style.width = "100%";
            }}
        }});
        </script>
        """,
        height=height,
        scrolling=True
    )


def show_cassette_audio(items, title):
    repeat_word = st.selectbox(
        "Word repeat count",
        [1, 2, 3],
        index=1,
        key=f"repeat_{title}"
    )

    button_label = "🎧 All words Listen" if title == "All words" else "🎧 Theme All words Listen"

    if st.button(button_label, key=f"visual_cassette_{title}", use_container_width=True):
        try:
            with st.spinner("Creating word audio. The first time may take a moment."):
                audio_payloads = []
                for item in items:
                    word = str(item["word"]).strip()
                    tts_text = ". ".join([word] * repeat_word) + "."
                    audio_bytes = get_tts_mp3_bytes(tts_text, lang="en")
                    audio_payloads.append(base64.b64encode(audio_bytes).decode("utf-8"))

            js_cassette_visual_player(
                items=items,
                audio_payloads=audio_payloads,
                title="🎧 All words Listen" if title == "All words" else "🎧 word Listen",
                height=560
            )
        except Exception as e:
            st.error("Could not create cassette audio. Please check that requests is in requirements.txt.")
            st.caption(f"Error: {e}")


def show_all_cassette_tab():
    all_items = flatten_survival_words()
    show_cassette_audio(all_items, "All words")


def show_cassette_player(theme_words, theme_name):
    theme_items = make_theme_cassette_items(theme_words, theme_name)
    show_cassette_audio(theme_items, theme_name)


# =========================
# =========================
all_words = []
for theme_words in word_themes.values():
    all_words.extend(theme_words)


def get_all_display_meanings():
    return [
        get_display_meaning(item["word"], item["meaning"])
        for item in all_words
    ]


# =========================
# =========================
def get_shuffled_options(theme_name, index, options):
    key = f"{theme_name}_options_{index}"

    if key not in st.session_state:
        shuffled = options[:]
        random.seed(f"{theme_name}_{index}")
        random.shuffle(shuffled)
        st.session_state[key] = shuffled

    return st.session_state[key]


# =========================
# =========================
def make_quiz_items(theme_words, theme_name):
    quiz_items = []
    display_meanings = get_all_display_meanings()

    for idx, item in enumerate(theme_words):
        word = item["word"]
        correct = get_display_meaning(word, item["meaning"])
        distractors = [m for m in display_meanings if m != correct]
        random.seed(f"{theme_name}_{word}_{idx}_vi")
        wrong_options = random.sample(distractors, 3)

        options = [correct] + wrong_options

        quiz_items.append({
            "word": word,
            "answer": correct,
            "options": options
        })

    return quiz_items


# =========================
# =========================
def init_state(theme_name):
    if f"{theme_name}_submitted1" not in st.session_state:
        st.session_state[f"{theme_name}_submitted1"] = False

    if f"{theme_name}_submitted2" not in st.session_state:
        st.session_state[f"{theme_name}_submitted2"] = False

    if f"{theme_name}_wrong" not in st.session_state:
        st.session_state[f"{theme_name}_wrong"] = []


def reset_theme(theme_name):
    keys_to_delete = []

    for key in st.session_state.keys():
        if key.startswith(theme_name):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del st.session_state[key]


# =========================
# =========================
def show_dialogue(theme_name):
    dialogue = theme_dialogues.get(theme_name, [])

    if not dialogue:
        return

    st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
    st.markdown('<div class="dialogue-title">💬 Survival Dialogue</div>', unsafe_allow_html=True)

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
        label="🔊 Listen to dialogue",
        dialogue_lines=dialogue,
        line_pause_ms=1400,
        height=105
    )



# =========================
# =========================
def show_word_cards(theme_words, theme_name):
    for idx, item in enumerate(theme_words):
        word = item["word"]
        meaning = get_display_meaning(word, item["meaning"])
        checked = word in st.session_state.unknown_words
        checkbox_key = f"{theme_name}_unknown_{idx}_{word}"

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5, col6 = st.columns([1.20, 1.05, 0.32, 1.30, 1.30, 1.10])

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
                f"<div class='meaning-text'>{meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            st.caption("🇺🇸 English")
            audio_button(
                "🔊 Listen",
                word,
                key=f"{theme_name}_learn_audio_{idx}",
                lang="en"
            )

        with col5:
            st.caption("🇻🇳 Tiếng Việt")
            audio_button(
                "🔊 Nghe",
                meaning,
                key=f"{theme_name}_vi_audio_{idx}",
                lang="vi"
            )

        with col6:
            review_checked = st.checkbox(
                "Review List",
                value=checked,
                key=checkbox_key
            )

            if review_checked and word not in st.session_state.unknown_words:
                add_unknown_word(word, meaning, theme_name)
            elif not review_checked and word in st.session_state.unknown_words:
                remove_unknown_word(word)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# =========================
def show_quiz(theme_words, theme_name):
    init_state(theme_name)

    quiz_items = make_quiz_items(theme_words, theme_name)

    submitted1_key = f"{theme_name}_submitted1"
    submitted2_key = f"{theme_name}_submitted2"
    wrong_key = f"{theme_name}_wrong"

    if not st.session_state[submitted1_key]:
        st.markdown("### 🧸 Quiz 1")
        st.write("Look at the English word and choose the correct Vietnamese meaning.")

        for i, q in enumerate(quiz_items):
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

            st.markdown(f"<div class='quiz-number'>🌟 Question {i + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='quiz-word'>{q['word']}</div>", unsafe_allow_html=True)

            audio_button(
                "🔊  Listen",
                q["word"],
                key=f"{theme_name}_quiz_audio1_{i}"
            )

            options = get_shuffled_options(theme_name, i, q["options"])

            st.radio(
                "Choose the meaning.",
                options,
                key=f"{theme_name}_q1_{i}"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("✅ Submit Quiz 1", key=f"{theme_name}_submit1"):
            wrong = []

            for i, q in enumerate(quiz_items):
                user_answer = st.session_state.get(f"{theme_name}_q1_{i}")

                if user_answer != q["answer"]:
                    wrong.append(i)

            st.session_state[wrong_key] = wrong
            st.session_state[submitted1_key] = True
            st.rerun()

    elif st.session_state[submitted1_key] and not st.session_state[submitted2_key]:
        wrong = st.session_state[wrong_key]
        score = len(quiz_items) - len(wrong)

        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-title">🎉 Quiz 1 result: {score} / {len(quiz_items)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(wrong) == 0:
            st.balloons()
            st.success("🌈 Perfect! You remember all words in this theme.")

            if st.button("🔄 Try again", key=f"{theme_name}_reset_all_correct"):
                reset_theme(theme_name)
                st.rerun()

        else:
            st.markdown(
                f"""
                <div class="wrong-box">
                    🍊 Wrong words {len(wrong)}words. Try them again.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### 🔁 2 : Wrong words Try again")

            for i in wrong:
                q = quiz_items[i]

                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

                st.markdown(f"<div class='quiz-number'>🌟 Retry {i + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='quiz-word'>{q['word']}</div>", unsafe_allow_html=True)

                audio_button(
                    "🔊  again Listen",
                    q["word"],
                    key=f"{theme_name}_quiz_audio2_{i}"
                )

                options = get_shuffled_options(theme_name, i, q["options"])

                st.radio(
                    "Choose the meaning again.",
                    options,
                    key=f"{theme_name}_q2_{i}"
                )

                st.markdown('</div>', unsafe_allow_html=True)

            if st.button("✅ Submit Quiz 2", key=f"{theme_name}_submit2"):
                st.session_state[submitted2_key] = True
                st.rerun()

    else:
        wrong = st.session_state[wrong_key]
        second_wrong = []

        for i in wrong:
            q = quiz_items[i]
            user_answer = st.session_state.get(f"{theme_name}_q2_{i}")

            if user_answer != q["answer"]:
                second_wrong.append(i)

        final_score = len(quiz_items) - len(second_wrong)

        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-title">🏆 Final result: {final_score} / {len(quiz_items)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(second_wrong) == 0:
            st.balloons()
            st.success("💖 Great! You reviewed all missed words.")
        else:
            st.warning("🍊 Review the words below again.")

        st.markdown("### ✅ Check answers")

        if len(wrong) == 0:
            st.info("No wrong answers.")
        else:
            for i in wrong:
                q = quiz_items[i]
                user1 = st.session_state.get(f"{theme_name}_q1_{i}")
                user2 = st.session_state.get(f"{theme_name}_q2_{i}")

                st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                st.markdown(f"### 🌱 {q['word']}")

                audio_button(
                    "🔊  again Listen",
                    q["word"],
                    key=f"{theme_name}_answer_audio_{i}"
                )

                st.write(f"First choice: {user1}")
                st.write(f"Second choice: {user2}")
                st.success(f"Answer: {q['answer']}")
                st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔄 Try again", key=f"{theme_name}_reset"):
            reset_theme(theme_name)
            st.rerun()



# =========================
# =========================
def show_unknown_words_tab():
    st.markdown(
        """
        <div class="theme-header">
            <div class="theme-title">⭐ Review List</div>
            <div class="theme-desc">Collect words you want to review and listen to them again.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    unknown_words = st.session_state.unknown_words
    unknown_info = st.session_state.unknown_word_info

    if not unknown_words:
        st.info(" check word .  word  'Review List' check .")
        return

    st.success(f"Total {len(unknown_words)} words checked.")

    unknown_items = []
    for idx, word in enumerate(unknown_words, start=1):
        info = unknown_info.get(word, {})
        unknown_items.append({
            "number": idx,
            "theme": info.get("theme", "Review List"),
            "word": word,
            "meaning": get_display_meaning(word, info.get("meaning", "")),
            "emoji": get_word_emoji(word),
        })

    show_cassette_audio(unknown_items, "Review List")

    st.markdown("### 📌 Checked word list")

    for idx, word in enumerate(unknown_words):
        info = unknown_info.get(word, {})
        meaning = get_display_meaning(word, info.get("meaning", ""))
        theme_name = info.get("theme", "")

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5, col6 = st.columns([1.20, 1.05, 0.32, 1.30, 1.30, 1.10])

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
                f"<div class='meaning-text'>{meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            st.caption("🇺🇸 English")
            audio_button(
                "🔊 Listen",
                word,
                key=f"unknown_word_audio_{idx}_{word}",
                lang="en"
            )

        with col5:
            st.caption("🇻🇳 Tiếng Việt")
            audio_button(
                "🔊 Nghe",
                meaning,
                key=f"unknown_word_vi_audio_{idx}_{word}",
                lang="vi"
            )

        with col6:
            if st.button("Delete", key=f"delete_unknown_{idx}_{word}", use_container_width=True):
                remove_unknown_word(word)

                # Remove the checkbox state for this word too.
                keys_to_delete = [
                    key for key in list(st.session_state.keys())
                    if "_unknown_" in str(key) and str(key).endswith(f"_{word}")
                ]
                for key in keys_to_delete:
                    del st.session_state[key]

                st.rerun()

        st.caption(f"Category: {theme_name}")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ Review List All Delete", key="clear_all_unknown_words", use_container_width=True):
        st.session_state.unknown_words = []
        st.session_state.unknown_word_info = {}
        st.rerun()


# =========================
# =========================
tab_names = list(word_themes.keys()) + ["🎧 All words Listen", "⭐ Review List"]
tabs = st.tabs(tab_names)

for tab, theme_name in zip(tabs[:-2], word_themes.keys()):
    with tab:
        theme_words = word_themes[theme_name]

        st.markdown(
            f"""
            <div class="theme-header">
                <div class="theme-title">{theme_name}</div>
                <div class="theme-desc">{len(theme_words)} survival words   .</div>
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
