import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Survival Word Card Speaking Game",
    page_icon="🃏",
    layout="wide"
)

# =========================================================
# Survival words
# =========================================================
WORD_THEMES = {'🧍 Tôi và mọi người': [{'word': 'I', 'meaning': 'tôi', 'emoji': '🙋'}, {'word': 'you', 'meaning': 'bạn', 'emoji': '👉'}, {'word': 'he', 'meaning': 'anh ấy', 'emoji': '👦'}, {'word': 'she', 'meaning': 'cô ấy', 'emoji': '👧'}, {'word': 'we', 'meaning': 'chúng tôi', 'emoji': '👥'}, {'word': 'they', 'meaning': 'họ', 'emoji': '👥'}, {'word': 'friend', 'meaning': 'bạn bè', 'emoji': '🤝'}, {'word': 'teacher', 'meaning': 'giáo viên', 'emoji': '👩\u200d🏫'}, {'word': 'student', 'meaning': 'học sinh', 'emoji': '🧑\u200d🎓'}, {'word': 'classmate', 'meaning': 'bạn cùng lớp', 'emoji': '👫'}, {'word': 'family', 'meaning': 'gia đình', 'emoji': '👨\u200d👩\u200d👧'}, {'word': 'father', 'meaning': 'bố', 'emoji': '👨'}, {'word': 'mother', 'meaning': 'mẹ', 'emoji': '👩'}, {'word': 'brother', 'meaning': 'anh/em trai', 'emoji': '👦'}, {'word': 'sister', 'meaning': 'chị/em gái', 'emoji': '👧'}, {'word': 'name', 'meaning': 'tên', 'emoji': '🏷️'}, {'word': 'person', 'meaning': 'người', 'emoji': '🧍'}, {'word': 'man', 'meaning': 'đàn ông', 'emoji': '👨'}, {'word': 'woman', 'meaning': 'phụ nữ', 'emoji': '👩'}, {'word': 'child', 'meaning': 'trẻ em', 'emoji': '🧒'}], '🏃 Hành động cơ bản': [{'word': 'go', 'meaning': 'đi', 'emoji': '➡️'}, {'word': 'come', 'meaning': 'đến', 'emoji': '⬅️'}, {'word': 'walk', 'meaning': 'đi bộ', 'emoji': '🚶'}, {'word': 'run', 'meaning': 'chạy', 'emoji': '🏃'}, {'word': 'sit', 'meaning': 'ngồi', 'emoji': '🪑'}, {'word': 'stand', 'meaning': 'đứng', 'emoji': '🧍'}, {'word': 'stop', 'meaning': 'dừng lại', 'emoji': '🛑'}, {'word': 'start', 'meaning': 'bắt đầu', 'emoji': '▶️'}, {'word': 'open', 'meaning': 'mở', 'emoji': '📂'}, {'word': 'close', 'meaning': 'đóng', 'emoji': '📕'}, {'word': 'eat', 'meaning': 'ăn', 'emoji': '🍽️'}, {'word': 'drink', 'meaning': 'uống', 'emoji': '🥤'}, {'word': 'sleep', 'meaning': 'ngủ', 'emoji': '😴'}, {'word': 'study', 'meaning': 'học', 'emoji': '📚'}, {'word': 'read', 'meaning': 'đọc', 'emoji': '📖'}, {'word': 'write', 'meaning': 'viết', 'emoji': '✏️'}, {'word': 'listen', 'meaning': 'nghe', 'emoji': '👂'}, {'word': 'speak', 'meaning': 'nói', 'emoji': '🗣️'}, {'word': 'help', 'meaning': 'giúp đỡ', 'emoji': '🆘'}, {'word': 'wait', 'meaning': 'đợi', 'emoji': '⏳'}], '💖 Cảm xúc và cơ thể': [{'word': 'happy', 'meaning': 'vui vẻ', 'emoji': '😊'}, {'word': 'sad', 'meaning': 'buồn', 'emoji': '😢'}, {'word': 'angry', 'meaning': 'tức giận', 'emoji': '😠'}, {'word': 'tired', 'meaning': 'mệt', 'emoji': '🥱'}, {'word': 'hungry', 'meaning': 'đói', 'emoji': '😋'}, {'word': 'thirsty', 'meaning': 'khát', 'emoji': '🥤'}, {'word': 'sick', 'meaning': 'ốm', 'emoji': '🤒'}, {'word': 'okay', 'meaning': 'ổn', 'emoji': '👌'}, {'word': 'fine', 'meaning': 'khỏe, ổn', 'emoji': '🙂'}, {'word': 'cold', 'meaning': 'lạnh', 'emoji': '🥶'}, {'word': 'hot', 'meaning': 'nóng', 'emoji': '🥵'}, {'word': 'pain', 'meaning': 'đau', 'emoji': '🤕'}, {'word': 'headache', 'meaning': 'đau đầu', 'emoji': '🤯'}, {'word': 'stomachache', 'meaning': 'đau bụng', 'emoji': '🤢'}, {'word': 'fever', 'meaning': 'sốt', 'emoji': '🌡️'}, {'word': 'hurt', 'meaning': 'đau, bị thương', 'emoji': '🩹'}, {'word': 'good', 'meaning': 'tốt', 'emoji': '👍'}, {'word': 'bad', 'meaning': 'xấu, tệ', 'emoji': '👎'}, {'word': 'worried', 'meaning': 'lo lắng', 'emoji': '😟'}, {'word': 'scared', 'meaning': 'sợ', 'emoji': '😨'}], '🍎 Đồ ăn và nước uống': [{'word': 'food', 'meaning': 'thức ăn', 'emoji': '🍽️'}, {'word': 'water', 'meaning': 'nước', 'emoji': '💧'}, {'word': 'rice', 'meaning': 'cơm, gạo', 'emoji': '🍚'}, {'word': 'bread', 'meaning': 'bánh mì', 'emoji': '🍞'}, {'word': 'milk', 'meaning': 'sữa', 'emoji': '🥛'}, {'word': 'juice', 'meaning': 'nước ép', 'emoji': '🧃'}, {'word': 'coffee', 'meaning': 'cà phê', 'emoji': '☕'}, {'word': 'tea', 'meaning': 'trà', 'emoji': '🍵'}, {'word': 'apple', 'meaning': 'táo', 'emoji': '🍎'}, {'word': 'banana', 'meaning': 'chuối', 'emoji': '🍌'}, {'word': 'egg', 'meaning': 'trứng', 'emoji': '🥚'}, {'word': 'meat', 'meaning': 'thịt', 'emoji': '🥩'}, {'word': 'chicken', 'meaning': 'gà, thịt gà', 'emoji': '🍗'}, {'word': 'fish', 'meaning': 'cá', 'emoji': '🐟'}, {'word': 'breakfast', 'meaning': 'bữa sáng', 'emoji': '🍳'}, {'word': 'lunch', 'meaning': 'bữa trưa', 'emoji': '🍱'}, {'word': 'dinner', 'meaning': 'bữa tối', 'emoji': '🍽️'}, {'word': 'snack', 'meaning': 'đồ ăn nhẹ', 'emoji': '🍪'}, {'word': 'medicine', 'meaning': 'thuốc', 'emoji': '💊'}, {'word': 'hospital', 'meaning': 'bệnh viện', 'emoji': '🏥'}], '🚗 Địa điểm và di chuyển': [{'word': 'home', 'meaning': 'nhà', 'emoji': '🏠'}, {'word': 'school', 'meaning': 'trường học', 'emoji': '🏫'}, {'word': 'classroom', 'meaning': 'lớp học', 'emoji': '🧑\u200d🏫'}, {'word': 'bathroom', 'meaning': 'nhà vệ sinh', 'emoji': '🚻'}, {'word': 'hospital', 'meaning': 'bệnh viện', 'emoji': '🏥'}, {'word': 'store', 'meaning': 'cửa hàng', 'emoji': '🏪'}, {'word': 'station', 'meaning': 'nhà ga', 'emoji': '🚉'}, {'word': 'bus', 'meaning': 'xe buýt', 'emoji': '🚌'}, {'word': 'car', 'meaning': 'ô tô', 'emoji': '🚗'}, {'word': 'taxi', 'meaning': 'taxi', 'emoji': '🚕'}, {'word': 'train', 'meaning': 'tàu hỏa', 'emoji': '🚆'}, {'word': 'bike', 'meaning': 'xe đạp', 'emoji': '🚲'}, {'word': 'road', 'meaning': 'đường', 'emoji': '🛣️'}, {'word': 'street', 'meaning': 'phố', 'emoji': '🏙️'}, {'word': 'here', 'meaning': 'ở đây', 'emoji': '📍'}, {'word': 'there', 'meaning': 'ở đó', 'emoji': '📌'}, {'word': 'near', 'meaning': 'gần', 'emoji': '↔️'}, {'word': 'far', 'meaning': 'xa', 'emoji': '🌁'}, {'word': 'left', 'meaning': 'bên trái', 'emoji': '⬅️'}, {'word': 'right', 'meaning': 'bên phải, đúng', 'emoji': '➡️'}], '⏰ Thời gian và số': [{'word': 'time', 'meaning': 'thời gian', 'emoji': '⏰'}, {'word': 'now', 'meaning': 'bây giờ', 'emoji': '🕒'}, {'word': 'today', 'meaning': 'hôm nay', 'emoji': '📅'}, {'word': 'tomorrow', 'meaning': 'ngày mai', 'emoji': '➡️📅'}, {'word': 'yesterday', 'meaning': 'hôm qua', 'emoji': '⬅️📅'}, {'word': 'morning', 'meaning': 'buổi sáng', 'emoji': '🌅'}, {'word': 'afternoon', 'meaning': 'buổi chiều', 'emoji': '☀️'}, {'word': 'evening', 'meaning': 'buổi tối', 'emoji': '🌆'}, {'word': 'night', 'meaning': 'đêm', 'emoji': '🌙'}, {'word': 'early', 'meaning': 'sớm', 'emoji': '🐓'}, {'word': 'late', 'meaning': 'muộn', 'emoji': '🌃'}, {'word': 'one', 'meaning': 'một', 'emoji': '1️⃣'}, {'word': 'two', 'meaning': 'hai', 'emoji': '2️⃣'}, {'word': 'three', 'meaning': 'ba', 'emoji': '3️⃣'}, {'word': 'four', 'meaning': 'bốn', 'emoji': '4️⃣'}, {'word': 'five', 'meaning': 'năm', 'emoji': '5️⃣'}, {'word': 'six', 'meaning': 'sáu', 'emoji': '6️⃣'}, {'word': 'seven', 'meaning': 'bảy', 'emoji': '7️⃣'}, {'word': 'eight', 'meaning': 'tám', 'emoji': '8️⃣'}, {'word': 'ten', 'meaning': 'mười', 'emoji': '🔟'}], '🎒 Đồ vật và tiền': [{'word': 'bag', 'meaning': 'cặp, túi', 'emoji': '🎒'}, {'word': 'phone', 'meaning': 'điện thoại', 'emoji': '📱'}, {'word': 'book', 'meaning': 'sách', 'emoji': '📘'}, {'word': 'notebook', 'meaning': 'vở', 'emoji': '📓'}, {'word': 'pen', 'meaning': 'bút mực', 'emoji': '🖊️'}, {'word': 'pencil', 'meaning': 'bút chì', 'emoji': '✏️'}, {'word': 'desk', 'meaning': 'bàn học', 'emoji': '🪑'}, {'word': 'chair', 'meaning': 'ghế', 'emoji': '🪑'}, {'word': 'door', 'meaning': 'cửa', 'emoji': '🚪'}, {'word': 'window', 'meaning': 'cửa sổ', 'emoji': '🪟'}, {'word': 'key', 'meaning': 'chìa khóa', 'emoji': '🔑'}, {'word': 'money', 'meaning': 'tiền', 'emoji': '💵'}, {'word': 'card', 'meaning': 'thẻ', 'emoji': '💳'}, {'word': 'ticket', 'meaning': 'vé', 'emoji': '🎫'}, {'word': 'clothes', 'meaning': 'quần áo', 'emoji': '👕'}, {'word': 'shoes', 'meaning': 'giày', 'emoji': '👟'}, {'word': 'hat', 'meaning': 'mũ', 'emoji': '🧢'}, {'word': 'watch', 'meaning': 'đồng hồ', 'emoji': '⌚'}, {'word': 'cup', 'meaning': 'cốc', 'emoji': '☕'}, {'word': 'bottle', 'meaning': 'chai', 'emoji': '🍼'}], '🆘 Nhờ giúp đỡ': [{'word': 'help', 'meaning': 'giúp đỡ', 'emoji': '🆘'}, {'word': 'please', 'meaning': 'làm ơn', 'emoji': '🙏'}, {'word': 'sorry', 'meaning': 'xin lỗi', 'emoji': '🙇'}, {'word': 'excuse me', 'meaning': 'xin lỗi / làm phiền', 'emoji': '🙋'}, {'word': 'again', 'meaning': 'lại, lần nữa', 'emoji': '🔁'}, {'word': 'slowly', 'meaning': 'chậm rãi', 'emoji': '🐢'}, {'word': 'understand', 'meaning': 'hiểu', 'emoji': '💡'}, {'word': 'question', 'meaning': 'câu hỏi', 'emoji': '❓'}, {'word': 'problem', 'meaning': 'vấn đề', 'emoji': '⚠️'}, {'word': 'need', 'meaning': 'cần', 'emoji': '📌'}, {'word': 'want', 'meaning': 'muốn', 'emoji': '✨'}, {'word': 'know', 'meaning': 'biết', 'emoji': '🧠'}, {'word': 'say', 'meaning': 'nói', 'emoji': '💬'}, {'word': 'tell', 'meaning': 'nói, kể', 'emoji': '📣'}, {'word': 'ask', 'meaning': 'hỏi', 'emoji': '❔'}, {'word': 'answer', 'meaning': 'câu trả lời', 'emoji': '✅'}, {'word': 'repeat', 'meaning': 'lặp lại', 'emoji': '🔁'}, {'word': 'speak', 'meaning': 'nói', 'emoji': '🗣️'}, {'word': 'look', 'meaning': 'nhìn', 'emoji': '👀'}, {'word': 'listen', 'meaning': 'nghe', 'emoji': '👂'}]}


# =========================================================
# Header design
# =========================================================
st.markdown(
    """
    <style>
    .main-title-box {
        background: linear-gradient(135deg, #eff6ff 0%, #fff7ed 50%, #fdf2f8 100%);
        border: 1.5px solid #dbeafe;
        border-radius: 30px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.07);
    }
    .main-title-box h1 {
        margin: 0 0 10px 0;
        color: #0f172a;
        font-size: 38px;
        font-weight: 900;
    }
    .main-title-box p {
        margin: 0;
        color: #475569;
        font-size: 18px;
        line-height: 1.7;
        font-weight: 700;
    }
    @media (max-width: 768px) {
        .main-title-box {
            padding: 20px 18px;
            border-radius: 22px;
        }
        .main-title-box h1 {
            font-size: 27px;
        }
        .main-title-box p {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title-box">
        <h1>🃏 Survival Word Card Speaking Game</h1>
        <p>Nhìn nghĩa tiếng Việt và nói từ tiếng Anh. Đây không phải là bài kiểm tra phát âm, mà là hoạt động kiểm tra xem bạn có biết từ tiếng Anh hay không.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# Speaking card game component
# =========================================================
def word_card_speaking_game(word_themes):
    items = []
    for cat, words in word_themes.items():
        for item in words:
            new_item = dict(item)
            new_item["cat"] = cat
            items.append(new_item)

    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="word-card-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #fdf2f8 100%);
        border: 1.5px solid #dbeafe;
        border-radius: 30px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        max-width: 100%;
        overflow-x: hidden;
        box-sizing: border-box;
    ">
        <style>
            #word-card-app * { box-sizing: border-box; }
            #word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }
            #word-card-app select { max-width: 100%; }

            #cardBox {
                position: relative;
                overflow: hidden;
                transform-origin: center center;
                will-change: transform, opacity, filter;
            }

            #cardBox::before {
                content: "Từ tiếp theo";
                position: absolute;
                top: 18px;
                left: 50%;
                transform: translateX(-50%) translateY(-16px) scale(0.88);
                background: linear-gradient(135deg, #2563eb, #7c3aed);
                color: white;
                border: 3px solid rgba(255,255,255,0.92);
                border-radius: 999px;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: 900;
                letter-spacing: -0.2px;
                box-shadow: 0 12px 26px rgba(37,99,235,0.24);
                opacity: 0;
                z-index: 8;
                pointer-events: none;
                white-space: nowrap;
            }

            #cardBox::after {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background: linear-gradient(90deg,
                    rgba(219,234,254,0) 0%,
                    rgba(219,234,254,0.88) 34%,
                    rgba(237,233,254,0.92) 50%,
                    rgba(254,243,199,0.88) 66%,
                    rgba(219,234,254,0) 100%);
                transform: translateX(-115%);
                opacity: 0;
                z-index: 7;
            }

            .next-card-animate {
                animation: nextCardSlide 0.58s cubic-bezier(.2,.8,.2,1);
            }
            .next-card-animate::before {
                animation: nextBadgePop 0.58s cubic-bezier(.2,.8,.2,1);
            }
            .next-card-animate::after {
                animation: nextLightSweep 0.58s ease-out;
            }

            @keyframes nextCardSlide {
                0% { opacity: 0; transform: translateX(46px) scale(0.965); filter: blur(3px) brightness(1.05); }
                55% { opacity: 1; transform: translateX(-7px) scale(1.012); filter: blur(0) brightness(1.03); }
                100% { opacity: 1; transform: translateX(0) scale(1); filter: blur(0) brightness(1); }
            }

            @keyframes nextBadgePop {
                0% { opacity: 0; transform: translateX(-50%) translateY(-18px) scale(0.86); }
                20% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1.04); }
                62% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                100% { opacity: 0; transform: translateX(-50%) translateY(-8px) scale(0.96); }
            }

            @keyframes nextLightSweep {
                0% { opacity: 0; transform: translateX(-115%); }
                20% { opacity: 1; }
                100% { opacity: 0; transform: translateX(115%); }
            }

            @media (max-width: 768px) {
                #word-card-app {
                    padding: 14px !important;
                    border-radius: 22px !important;
                }
                #categorySelect, #languageSelect {
                    width: 100%;
                    font-size: 14px !important;
                }
                #topControlBox {
                    gap: 8px !important;
                }
                #topControlBox button {
                    flex: 1 1 45%;
                    font-size: 14px !important;
                    padding: 10px 10px !important;
                }
                #cardBox {
                    padding: 18px 14px !important;
                    border-radius: 24px !important;
                }
                #emojiBox { font-size: 72px !important; }
                #meaningBox {
                    font-size: 32px !important;
                    line-height: 1.25 !important;
                }
                #answerBox {
                    font-size: 27px !important;
                    padding: 14px 12px !important;
                    word-break: break-word;
                }
                #micBtn {
                    min-height: 54px !important;
                    font-size: 17px !important;
                    padding: 13px 12px !important;
                    border-radius: 999px !important;
                }
                #transcriptMiniBox {
                    min-height: 62px !important;
                    padding: 10px 12px !important;
                    border-radius: 18px !important;
                }
                #transcriptMiniLabel {
                    font-size: 12px !important;
                    margin-bottom: 4px !important;
                }
                #transcriptBox {
                    font-size: 19px !important;
                    line-height: 1.25 !important;
                }
                #smallButtonRow {
                    gap: 6px !important;
                }
                #smallButtonRow button {
                    min-height: 42px !important;
                    font-size: 12px !important;
                    padding: 8px 4px !important;
                    border-radius: 15px !important;
                    letter-spacing: -0.5px;
                }
                #resultBox { font-size: 17px !important; }
            }
        </style>

        <div id="topControlBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">Chọn phạm vi từ</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bae6fd;
                font-size: 15px;
                font-weight: 800;
                color: #0f172a;
                background: white;
            "></select>

            <button id="randomBtn" style="
                border: 1.5px solid #c7d2fe;
                background: white;
                color: #3730a3;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🎲 Xáo trộn phạm vi này</button>

            <button id="resetBtn" style="
                border: 1.5px solid #fed7aa;
                background: #fff7ed;
                color: #9a3412;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🔄 Bắt đầu lại</button>
        </div>

        <div id="gameArea">
            <div style="display:flex; justify-content:flex-end; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="scoreLabel" style="
                    display:inline-block;
                    background:#f0fdf4;
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bbf7d0;
                ">Đúng 0 / 0 · Từ cần luyện 0</div>
            </div>

            <div id="cardBox" style="
                background:white;
                border-radius:32px;
                padding:30px 24px;
                border:1.5px solid #e0f2fe;
                box-shadow:0 8px 24px rgba(0,0,0,0.07);
                text-align:center;
                margin-bottom:18px;
            ">
                <div id="emojiBox" style="font-size: 96px; line-height: 1.1; margin-bottom: 14px;">🃏</div>

                <div style="
                    display:inline-block;
                    background:#fef3c7;
                    color:#92400e;
                    border:1.5px solid #fde68a;
                    border-radius:999px;
                    padding:7px 14px;
                    font-size:14px;
                    font-weight:900;
                    margin-bottom:14px;
                "><span id="meaningLangLabel">Nghĩa tiếng Việt</span></div>

                <div id="meaningBox" style="
                    font-size: 44px;
                    font-weight: 900;
                    color: #111827;
                    line-height: 1.35;
                    margin-bottom: 16px;
                ">Nghĩa</div>

                <div id="answerBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:16px 18px;
                    font-size:34px;
                    font-weight:900;
                    margin-top:18px;
                ">answer</div>

                <div id="hintBox" style="
                    display:none;
                    background:#fff7ed;
                    border:1.5px solid #fed7aa;
                    color:#9a3412;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:30px;
                    font-weight:900;
                    margin-top:14px;
                ">hint</div>
            </div>

            <div id="buttonBox" style="
                display:flex;
                flex-direction:column;
                gap:10px;
                align-items:stretch;
                margin-bottom:16px;
                width:100%;
            ">
                <button id="micBtn" style="
                    width:100%;
                    border:1.5px solid #fecaca;
                    background:#fff1f2;
                    color:#be123c;
                    border-radius:999px;
                    padding:14px 18px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:19px;
                    min-height:58px;
                    white-space:nowrap;
                    box-shadow:0 3px 9px rgba(0,0,0,0.05);
                ">🎙️ Nói tiếng Anh</button>

                <div id="transcriptMiniBox" style="
                    width:100%;
                    background:#f8fafc;
                    border:1.5px solid #e2e8f0;
                    border-radius:20px;
                    padding:12px 14px;
                    min-height:68px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    overflow:hidden;
                ">
                    <div id="transcriptMiniLabel" style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px; white-space:nowrap;">Từ được nhận diện</div>
                    <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"></div>
                </div>

                <div id="smallButtonRow" style="
                    display:grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap:8px;
                    width:100%;
                ">
                    <button id="hintBtn" style="
                        border:1.5px solid #fed7aa;
                        background:#fff7ed;
                        color:#9a3412;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">💡 Gợi ý</button>

                    <button id="answerBtn" style="
                        border:1.5px solid #bfdbfe;
                        background:#eff6ff;
                        color:#1d4ed8;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">👀 Đáp án+🔊</button>

                    <button id="skipBtn" style="
                        border:1.5px solid #c7d2fe;
                        background:#eef2ff;
                        color:#3730a3;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">➡️ Tiếp theo</button>
                </div>
            </div>

            <div id="resultBox" style="
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                font-size:20px;
                font-weight:900;
                color:#334155;
            "></div>
        </div>

        <div id="finishBox" style="
            display:none;
            background:white;
            border-radius:30px;
            padding:30px 24px;
            border:1.5px solid #bbf7d0;
            box-shadow:0 8px 24px rgba(0,0,0,0.07);
            text-align:center;
            margin-top:16px;
        ">
            <div style="font-size:64px; margin-bottom:10px;">🎉</div>
            <div style="
                font-size:34px;
                font-weight:900;
                color:#14532d;
                margin-bottom:10px;
            ">Hoàn thành phạm vi!</div>
            <div id="finishScore" style="
                font-size:24px;
                font-weight:900;
                color:#166534;
                margin-bottom:18px;
            ">Đúng 0 / 0 · Từ cần luyện 0</div>
            <button id="finishRetryBtn" style="
                border:1.5px solid #a7f3d0;
                background:#ecfdf5;
                color:#047857;
                border-radius:999px;
                padding:13px 22px;
                font-weight:900;
                cursor:pointer;
                font-size:17px;
            ">🔁 Làm lại</button>
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let correctMap = {};
    let missedMap = {};
    let finished = false;

    const categorySelect = document.getElementById("categorySelect");
    const meaningLangLabel = document.getElementById("meaningLangLabel");
    const randomBtn = document.getElementById("randomBtn");
    const resetBtn = document.getElementById("resetBtn");

    const gameArea = document.getElementById("gameArea");
    const finishBox = document.getElementById("finishBox");
    const finishScore = document.getElementById("finishScore");
    const finishRetryBtn = document.getElementById("finishRetryBtn");

    const scoreLabel = document.getElementById("scoreLabel");
    const cardBox = document.getElementById("cardBox");
    const emojiBox = document.getElementById("emojiBox");
    const meaningBox = document.getElementById("meaningBox");
    const answerBox = document.getElementById("answerBox");
    const hintBox = document.getElementById("hintBox");

    const micBtn = document.getElementById("micBtn");
    const answerBtn = document.getElementById("answerBtn");
    const hintBtn = document.getElementById("hintBtn");
    const skipBtn = document.getElementById("skipBtn");

    const transcriptBox = document.getElementById("transcriptBox");
    const resultBox = document.getElementById("resultBox");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;
    let micSafetyTimer = null;
    let recognitionRunId = 0;

    function resetMicButton() {
        isListening = false;
        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        micBtn.style.cursor = "pointer";
        micBtn.innerText = "🎙️ Nói tiếng Anh";
    }

    function cleanupRecognition() {
        recognitionRunId += 1;
        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }
        if (recognition) {
            try { recognition.onresult = null; } catch (e) {}
            try { recognition.onerror = null; } catch (e) {}
            try { recognition.onend = null; } catch (e) {}
            try { recognition.abort(); } catch (e) {}
            try { recognition.stop(); } catch (e) {}
            recognition = null;
        }
        resetMicButton();
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function uniqueCategories() {
        return ["1~50", "51~100", "101~160"];
    }

    function initCategories() {
        const cats = uniqueCategories();
        categorySelect.innerHTML = "";
        cats.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat;
            option.innerText = cat;
            categorySelect.appendChild(option);
        });
    }

    function getFilteredItems() {
        const selected = categorySelect.value || "1~50";
        if (selected === "1~50") return ITEMS.slice(0, 50);
        if (selected === "51~100") return ITEMS.slice(50, 100);
        if (selected === "101~160") return ITEMS.slice(100, 160);
        return ITEMS.slice(0, 50);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
    }

    function hasEnglishLetters(text) {
        return /[a-zA-Z]/.test(String(text || ""));
    }

    function normalizeText(text) {
        return String(text || "")
            .toLowerCase()
            .replace(/\bi'm\b/g, "i am")
            .replace(/\bim\b/g, "i am")
            .replace(/\byou're\b/g, "you are")
            .replace(/\bhe's\b/g, "he is")
            .replace(/\bshe's\b/g, "she is")
            .replace(/\bit's\b/g, "it is")
            .replace(/\bwe're\b/g, "we are")
            .replace(/\bthey're\b/g, "they are")
            .replace(/\bdon't\b/g, "do not")
            .replace(/\bdoesn't\b/g, "do not")
            .replace(/\bdidn't\b/g, "do not")
            .replace(/\bcan't\b/g, "cannot")
            .replace(/\bcant\b/g, "cannot")
            .replace(/\bi'll\b/g, "i will")
            .replace(/\byou'll\b/g, "you will")
            .replace(/\bhe'll\b/g, "he will")
            .replace(/\bshe'll\b/g, "she will")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
            .replace(/\bt shirt\b/g, "tshirt")
            .replace(/\btee shirt\b/g, "tshirt")
            .replace(/\bwi fi\b/g, "wifi")
            .replace(/\bwi-fi\b/g, "wifi")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
            .replace(/\s+/g, " ")
            .trim();
    }

    const KNOWN_ANSWER_WORDS = ITEMS.map(item =>
        normalizeText(item.word).replace(/\s+/g, "")
    );

    function wordsOnly(text) {
        return normalizeText(text)
            .split(" ")
            .filter(function(w) {
                return w.length > 0;
            });
    }

    function editDistance(a, b) {
        a = String(a || "");
        b = String(b || "");
        const dp = [];
        for (let i = 0; i <= a.length; i++) {
            dp[i] = [];
            for (let j = 0; j <= b.length; j++) dp[i][j] = 0;
        }
        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                const cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                );
            }
        }
        return dp[a.length][b.length];
    }

    function wordSimilarity(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (!a || !b) return 0;
        if (a === b) return 1;
        const dist = editDistance(a, b);
        const maxLen = Math.max(a.length, b.length);
        return 1 - (dist / maxLen);
    }

    function soundKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/tion/g, "shun")
            .replace(/sion/g, "shun")
            .replace(/ch/g, "j")
            .replace(/sh/g, "s")
            .replace(/th/g, "d")
            .replace(/ph/g, "f")
            .replace(/gh/g, "g")
            .replace(/ck/g, "k")
            .replace(/qu/g, "kw")
            .replace(/x/g, "ks")
            .replace(/c/g, "k")
            .replace(/q/g, "k")
            .replace(/z/g, "s")
            .replace(/v/g, "b")
            .replace(/f/g, "p")
            .replace(/r/g, "l")
            .replace(/j/g, "g")
            .replace(/w/g, "u")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]/g, "")
            .replace(/(.)\1+/g, "$1");
    }

    function vowelLooseKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]+/g, "v")
            .replace(/(.)\1+/g, "$1");
    }

    function aliasMatch(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        const aliases = {
            "i": ["i", "eye", "hi", "ai", "a"],
            "you": ["you", "u", "yew", "yo", "ya", "your", "yu"],
            "he": ["he", "hi", "hey", "hee"],
            "she": ["she", "see", "sea", "shi", "seat", "sheet"],
            "we": ["we", "wee", "wi", "me", "be"],
            "they": ["they", "day", "dey", "the", "there", "their", "that"],
            "one": ["one", "won", "wan"],
            "two": ["two", "to", "too", "tu"],
            "three": ["three", "tree", "free", "sree"],
            "four": ["four", "for", "fore"],
            "five": ["five", "fife", "pipe"],
            "six": ["six", "sex", "sick", "sicks"],
            "seven": ["seven", "seben", "sevn"],
            "eight": ["eight", "ate", "eit"],
            "ten": ["ten", "tin"],
            "here": ["here", "hear", "hir"],
            "there": ["there", "their", "der", "dare"],
            "right": ["right", "write", "light", "rite"],
            "wait": ["wait", "weight", "wet"],
            "know": ["know", "no", "now"],
            "night": ["night", "knight", "nite"],
            "okay": ["okay", "ok", "kay", "okey"],
            "phone": ["phone", "fone", "pon"],
            "coffee": ["coffee", "coffe", "copy"],
            "please": ["please", "plz", "plis", "place"],
            "go": ["go", "goal"],
            "come": ["come", "com", "gum"],
            "run": ["run", "ran", "learn"],
            "sit": ["sit", "seat", "set"],
            "stand": ["stand", "stan", "stend"],
            "stop": ["stop", "stap", "stub"],
            "start": ["start", "stard", "stut"],
            "open": ["open", "opin", "oben"],
            "close": ["close", "clothes", "cloze", "closed"],
            "eat": ["eat", "it", "e"],
            "drink": ["drink", "dring", "drank"],
            "sleep": ["sleep", "slip", "sleap"],
            "read": ["read", "reed", "rid"],
            "write": ["write", "right", "light"],
            "help": ["help", "hell", "halp"],
            "friend": ["friend", "freind", "frend"],
            "teacher": ["teacher", "techer", "ticher"],
            "student": ["student", "studen", "studant"],
            "classmate": ["classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "class mate"],
            "family": ["family", "famly", "femily"],
            "father": ["father", "fader", "pader"],
            "mother": ["mother", "mader", "moder"],
            "brother": ["brother", "brader", "broder"],
            "sister": ["sister", "seester", "sistar"],
            "person": ["person", "parson"],
            "woman": ["woman", "women", "wuman"],
            "walk": ["walk", "work", "wok"],
            "study": ["study", "stady", "steady"],
            "listen": ["listen", "lisen", "lesson"],
            "speak": ["speak", "speek", "spik"],
            "happy": ["happy", "happi"],
            "sad": ["sad", "set"],
            "angry": ["angry", "angri", "hungry"],
            "tired": ["tired", "tyred", "tire"],
            "hungry": ["hungry", "hangry", "angry"],
            "thirsty": ["thirsty", "thirsti", "firsty"],
            "stomachache": ["stomachache", "stomach ache", "stomachegg"],
            "headache": ["headache", "head ache", "hedache"],
            "breakfast": ["breakfast", "brekfast", "break first"],
            "medicine": ["medicine", "medisin", "medicen"],
            "hospital": ["hospital", "hospitel", "hostpital"],
            "bathroom": ["bathroom", "bath room", "batroom"],
            "station": ["station", "stashion", "staytion"],
            "bottle": ["bottle", "bottel", "battle"],
            "question": ["question", "kwestion", "queshon"],
            "understand": ["understand", "understend", "understanded"],
            "answer": ["answer", "anser", "andser"],
            "again": ["again", "agen", "agein"],
            "slowly": ["slowly", "slowli", "slowy"],
            "water": ["water", "wader"],
            "school": ["school", "skool"],
            "home": ["home", "holm"],
            "food": ["food", "fud", "put"],
            "rice": ["rice", "rise", "lice"],
            "bread": ["bread", "bred"],
            "milk": ["milk", "melk"],
            "juice": ["juice", "juse"],
            "apple": ["apple", "appel"],
            "banana": ["banana", "bananna"],
            "chicken": ["chicken", "chiken"],
            "classroom": ["classroom", "class room"],
            "store": ["store", "stole"],
            "train": ["train", "trane"],
            "bike": ["bike", "back", "baik"],
            "road": ["road", "load"],
            "street": ["street", "strit"],
            "left": ["left", "lift"],
            "morning": ["morning", "mornin"],
            "afternoon": ["afternoon", "after noon"],
            "evening": ["evening", "evning"],
            "money": ["money", "moni"],
            "ticket": ["ticket", "tiket"],
            "clothes": ["clothes", "close", "cloths"],
            "shoes": ["shoes", "shoe"],
            "repeat": ["repeat", "repeet"],
            "look": ["look", "luk"],
            "ask": ["ask", "axe"],
            "tell": ["tell", "tel"],
            "say": ["say", "sei"],
            "want": ["want", "wanna", "won"],
            "need": ["need", "nid"],
            "problem": ["problem", "problum"],
            "sorry": ["sorry", "sori"],
            "child": ["child", "chaild"],
            "man": ["man", "men"],
            "hot": ["hot", "hut"],
            "cold": ["cold", "called"],
            "good": ["good", "gud"],
            "bad": ["bad", "bed"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function clearlyWrongPronoun(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");
        const pronouns = ["i", "you", "he", "she", "we", "they"];
        if (!pronouns.includes(aw)) return false;
        if (!pronouns.includes(sw)) return false;
        return sw !== aw;
    }

    function prefixOverlap(a, b) {
        a = String(a || "");
        b = String(b || "");
        let n = Math.min(a.length, b.length);
        let count = 0;
        for (let i = 0; i < n; i++) {
            if (a.charAt(i) === b.charAt(i)) count += 1;
            else break;
        }
        return count;
    }

    function hasSharedBigram(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (a.length < 2 || b.length < 2) return false;
        for (let i = 0; i < a.length - 1; i++) {
            if (b.includes(a.slice(i, i + 2))) return true;
        }
        return false;
    }

    function isClearlyDifferentKnownWord(sw, aw) {
        if (!KNOWN_ANSWER_WORDS.includes(sw)) return false;
        if (sw === aw) return false;
        if (aliasMatch(sw, aw)) return false;

        const sim = wordSimilarity(sw, aw);
        const soundSim = wordSimilarity(soundKey(sw), soundKey(aw));
        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);

        // Allow possible ASR misrecognitions such as bike/back, but reject clearly different known words.
        return !(sameFirst || sameLast || sim >= 0.45 || soundSim >= 0.36 || hasSharedBigram(sw, aw));
    }

    function isUnderstandableWord(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        // Pronouns change meaning significantly, so different pronouns are incorrect.
        if (clearlyWrongPronoun(sw, aw)) return false;

        // Clearly different known words are incorrect.
        if (isClearlyDifferentKnownWord(sw, aw)) return false;

        const dist = editDistance(sw, aw);
        const sim = wordSimilarity(sw, aw);

        const soundSw = soundKey(sw);
        const soundAw = soundKey(aw);
        const soundDist = editDistance(soundSw, soundAw);
        const soundSim = wordSimilarity(soundSw, soundAw);

        const vowelSw = vowelLooseKey(sw);
        const vowelAw = vowelLooseKey(aw);
        const vowelSim = wordSimilarity(vowelSw, vowelAw);

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameFirstThree = sw.slice(0, 3) === aw.slice(0, 3);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const soundSameFirst = soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);
        const soundSameLast = soundSw && soundAw && soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);
        const overlap = prefixOverlap(sw, aw);

        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            overlap >= 1 ||
            hasSharedBigram(sw, aw) ||
            soundSim >= 0.25 ||
            vowelSim >= 0.30 ||
            sim >= 0.30;

        if (!hasAnyClue) return false;

        // Allow partial or extra recognition around one-word answers.
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) return true;

        // Accept if the consonant-like sound pattern is the same or nearly the same.
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.25) return true;

        // 1-2 letter words: alias-based, but not too strict.
        if (aw.length <= 2) {
            return sim >= 0.55 || soundSim >= 0.35 || sameFirst || sameLast;
        }

        // 3-4 letter words: lenient because this checks word recognition, not pronunciation.
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.32 ||
                soundSim >= 0.24 ||
                vowelSim >= 0.28 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast ||
                hasSharedBigram(sw, aw)
            );
        }

        // 5-6 letter words
        if (aw.length <= 6) {
            return (
                dist <= 4 ||
                sim >= 0.34 ||
                soundSim >= 0.25 ||
                vowelSim >= 0.30 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // 7+ letter words
        return (
            dist <= 6 ||
            sim >= 0.30 ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25 ||
            sameFirst ||
            sameFirstTwo ||
            sameFirstThree ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function isCorrectSpeech(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        if (answerWords.length === 1) {
            const target = answerWords[0];

            // If the whole recognized phrase is similar, accept it.
            if (isUnderstandableWord(s, target)) return true;

            // If any recognized candidate word is similar to the answer, accept it.
            for (const sw of spokenWords) {
                if (isUnderstandableWord(sw, target)) return true;
            }

            // Handle split or joined forms such as "bath room" and "class room".
            const joinedSpoken = spokenWords.join("");
            if (isUnderstandableWord(joinedSpoken, target)) return true;

            // Accept if the key word is correct even with fillers like please, uh, a, the.
            const fillerRemoved = spokenWords.filter(w =>
                !["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(w)
            );
            if (fillerRemoved.length > 0) {
                const joinedClean = fillerRemoved.join("");
                if (isUnderstandableWord(joinedClean, target)) return true;
                for (const w of fillerRemoved) {
                    if (isUnderstandableWord(w, target)) return true;
                }
            }

            return false;
        }

        if (s.includes(a)) return true;

        // For multi-word expressions, accept if key words are recognized in order.
        let pos = 0;
        for (const sw of spokenWords) {
            const target = answerWords[pos];
            if (!target) break;

            if (isUnderstandableWord(sw, target)) {
                pos += 1;
            }
            if (pos >= answerWords.length) break;
        }

        // Allow short expressions like excuse me to be recognized as joined words.
        if (pos < answerWords.length) {
            const joinedSpoken = spokenWords.join("");
            const joinedAnswer = answerWords.join("");
            if (isUnderstandableWord(joinedSpoken, joinedAnswer)) return true;
        }

        return pos >= answerWords.length;
    }

    function transcriptScore(transcript, answer) {
        const spokenWords = wordsOnly(transcript);
        const answerWords = wordsOnly(answer);
        if (spokenWords.length === 0 || answerWords.length === 0) return 0;

        let best = 0;

        for (const sw of spokenWords) {
            for (const aw of answerWords) {
                const swNorm = normalizeText(sw).replace(/\s+/g, "");
                const awNorm = normalizeText(aw).replace(/\s+/g, "");
                const soundSw = soundKey(swNorm);
                const soundAw = soundKey(awNorm);
                const vowelSw = vowelLooseKey(swNorm);
                const vowelAw = vowelLooseKey(awNorm);

                if (isUnderstandableWord(sw, aw)) {
                    best = Math.max(best, 1);
                } else {
                    best = Math.max(
                        best,
                        wordSimilarity(swNorm, awNorm),
                        wordSimilarity(soundSw, soundAw) * 0.95,
                        wordSimilarity(vowelSw, vowelAw) * 0.88
                    );
                }
            }
        }

        const s = normalizeText(transcript);
        const a = normalizeText(answer);
        if (s.includes(a) || a.includes(s)) best += 0.2;

        return best;
    }

    function pickBestTranscriptFromEvent(event, answer) {
        let bestTranscript = "";
        let bestScore = -1;
        let anyFinal = false;

        for (let i = 0; i < event.results.length; i++) {
            if (event.results[i].isFinal) anyFinal = true;

            for (let j = 0; j < event.results[i].length; j++) {
                const candidate = event.results[i][j].transcript.trim();
                if (!candidate) continue;

                if (!bestTranscript) bestTranscript = candidate;

                // If a correct candidate appears, choose it immediately without waiting for final.
                if (isCorrectSpeech(candidate, answer)) {
                    return {
                        transcript: candidate,
                        hasFinal: anyFinal,
                        isCorrectCandidate: true
                    };
                }

                const score = transcriptScore(candidate, answer);
                if (score > bestScore) {
                    bestScore = score;
                    bestTranscript = candidate;
                }
            }
        }

        return {
            transcript: bestTranscript,
            hasFinal: anyFinal,
            isCorrectCandidate: false
        };
    }

    function countCorrectInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;
        list.forEach(item => {
            if (correctMap[getItemKey(item)]) count += 1;
        });
        return count;
    }

    function countMissedInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;
        list.forEach(item => {
            if (missedMap[getItemKey(item)]) count += 1;
        });
        return count;
    }

    function updateScore() {
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();
        scoreLabel.innerText = "Đúng " + correctCount + " / " + list.length + " · Từ cần luyện " + missedCount;
    }

    function speak(text) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 0.82;
        utterance.pitch = 1.05;

        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v =>
            v.lang && v.lang.toLowerCase().startsWith("en") &&
            /(samantha|jenny|aria|zira|google us english|karen|victoria|female)/i.test(v.name)
        );
        if (preferred) utterance.voice = preferred;
        window.speechSynthesis.speak(utterance);
    }

    function showGameArea() {
        gameArea.style.display = "block";
        finishBox.style.display = "none";
        finished = false;
    }

    function showFinishScreen() {
        cleanupRecognition();
        finished = true;
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();

        finishScore.innerText = "Đúng " + correctCount + " / " + list.length + " · Từ cần luyện " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }


    function getDisplayMeaning(item) {
        if (!item) return "";
        return item.meaning || "";
    }

    function updateMeaningLanguageLabel() {
        if (!meaningLangLabel) return;
        meaningLangLabel.innerText = "Nghĩa tiếng Việt";
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) currentList = getFilteredItems();

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();
        cleanupRecognition();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        emojiBox.innerText = currentItem.emoji || "🃏";
        updateMeaningLanguageLabel();
        meaningBox.innerText = getDisplayMeaning(currentItem);

        answerBox.style.display = "none";
        answerBox.style.background = "#ecfdf5";
        answerBox.style.borderColor = "#bbf7d0";
        answerBox.style.color = "#166534";
        answerBox.innerText = "Đáp án: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        transcriptBox.innerText = "";
        resultBox.innerText = "";
        resultBox.style.display = "none";
        resultBox.style.background = "#fff7ed";
        resultBox.style.borderColor = "#fed7aa";
        resultBox.style.color = "#92400e";

        cardBox.classList.remove("next-card-animate");
        void cardBox.offsetWidth;
        cardBox.classList.add("next-card-animate");

        updateScore();
    }

    function goNextCard() {
        if (currentIndex + 1 >= currentList.length) {
            showFinishScreen();
        } else {
            loadQuestion(currentIndex + 1);
        }
    }

    function checkSpeech(spokenText) {
        if (!currentItem) return;

        if (isCorrectSpeech(spokenText, currentItem.word)) {
            correctMap[getItemKey(currentItem)] = true;
            delete missedMap[getItemKey(currentItem)];
            updateScore();

            answerBox.style.display = "none";
            transcriptBox.innerHTML =
                "<span style='color:#334155;'>" + escapeHtml(currentItem.word) + "</span>" +
                " <span style='display:inline-block; margin-left:8px; padding:4px 9px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-size:0.82em; font-weight:900; vertical-align:middle;'>✅ Đúng rồi</span>";
            transcriptBox.style.color = "#334155";

            resultBox.innerText = "";
            resultBox.style.display = "none";

            speak(currentItem.word);
            cleanupRecognition();
        } else {
            answerBox.style.display = "none";
            transcriptBox.style.color = "#334155";
            resultBox.style.display = "block";
            resultBox.innerText = "Nếu không phải là từ hoàn toàn khác, phát âm gần đúng cũng được chấp nhận. Hãy nói lại một lần nữa.";
            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#92400e";
        }
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "Trình duyệt này không hỗ trợ nhận diện giọng nói. Hãy thử dùng Chrome.";
            resultBox.style.display = "block";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            resetMicButton();
            return;
        }

        if (finished || !currentItem) {
            resetMicButton();
            return;
        }

        if (correctMap[getItemKey(currentItem)]) {
            resultBox.innerText = "";
            resultBox.style.display = "none";
            resetMicButton();
            return;
        }

        cleanupRecognition();

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(function(track) { track.stop(); });
            } catch (err) {
                resultBox.innerText = "Cho phép quyền micro rồi bấm lại.";
                resultBox.style.display = "block";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
                resetMicButton();
                return;
            }
        }

        window.speechSynthesis.cancel();

        recognitionRunId += 1;
        const thisRunId = recognitionRunId;

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = true;
        recognition.continuous = false;
        recognition.maxAlternatives = 30;

        isListening = true;
        micBtn.disabled = true;
        micBtn.style.opacity = "0.72";
        micBtn.style.cursor = "wait";
        micBtn.innerText = "🎙️ Đang nghe...";

        resultBox.innerText = "";
        resultBox.style.display = "none";
        resultBox.style.background = "#fff7ed";
        resultBox.style.borderColor = "#fed7aa";
        resultBox.style.color = "#92400e";

        recognition.onresult = function(event) {
            if (thisRunId !== recognitionRunId) return;

            if (!event.results || !event.results[0]) {
                resetMicButton();
                return;
            }

            const picked = pickBestTranscriptFromEvent(event, currentItem.word);
            const bestTranscript = picked.transcript || "";

            transcriptBox.style.color = "#334155";
            transcriptBox.innerText = bestTranscript;

            // Check immediately when a correct candidate appears; also check when final arrives.
            if (picked.isCorrectCandidate || picked.hasFinal) {
                checkSpeech(bestTranscript);
            }
        };

        recognition.onerror = function(event) {
            if (thisRunId !== recognitionRunId) return;

            if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                resultBox.innerText = "Vui lòng cho phép dùng micro.";
                resultBox.style.display = "block";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
            } else if (event.error === "no-speech") {
                resultBox.innerText = "Không nhận diện được âm thanh. Hãy bấm lại.";
                resultBox.style.display = "block";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            } else {
                resultBox.innerText = "Hãy bấm lại.";
                resultBox.style.display = "block";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            }

            resetMicButton();
        };

        recognition.onend = function() {
            if (thisRunId !== recognitionRunId) return;
            recognition = null;
            resetMicButton();
        };

        micSafetyTimer = setTimeout(function() {
            if (thisRunId !== recognitionRunId) return;
            if (isListening) {
                try { recognition.stop(); } catch (e) {}
                try { recognition.abort(); } catch (e) {}
                recognition = null;
                resetMicButton();
            }
        }, 11000);

        try {
            recognition.start();
        } catch (err) {
            resultBox.innerText = "Hãy bấm lại.";
            resultBox.style.display = "block";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";
            cleanupRecognition();
        }
    }

    function resetCurrentRange() {
        cleanupRecognition();
        const list = getFilteredItems();

        list.forEach(item => {
            delete correctMap[getItemKey(item)];
            delete missedMap[getItemKey(item)];
        });

        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    }

    categorySelect.addEventListener("change", function() {
        cleanupRecognition();
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    randomBtn.addEventListener("click", function() {
        cleanupRecognition();
        currentList = shuffleArray(getFilteredItems());
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    resetBtn.addEventListener("click", resetCurrentRange);
    finishRetryBtn.addEventListener("click", resetCurrentRange);
    micBtn.addEventListener("click", startRecognition);

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        answerBox.style.display = "block";
        answerBox.style.background = "#ecfdf5";
        answerBox.style.borderColor = "#bbf7d0";
        answerBox.style.color = "#166534";
        answerBox.innerText = "Đáp án: " + currentItem.word;
        speak(currentItem.word);

        resultBox.style.display = "block";
        resultBox.innerText = "Nghe và nói lại.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";
    });

    hintBtn.addEventListener("click", function() {
        if (!currentItem) return;
        const cleanWord = String(currentItem.word || "").trim();
        const noSpaceWord = cleanWord.replace(/\s+/g, "");
        const firstTwo = noSpaceWord.length <= 2 ? noSpaceWord : noSpaceWord.slice(0, 2);

        hintBox.style.display = "block";
        hintBox.innerText = "Gợi ý: " + firstTwo + "...";
    });

    skipBtn.addEventListener("click", function() {
        if (currentItem && !correctMap[getItemKey(currentItem)]) {
            missedMap[getItemKey(currentItem)] = true;
            updateScore();
        }
        cleanupRecognition();
        goNextCard();
    });

    initCategories();
    currentList = getFilteredItems();
    loadQuestion(0);
    updateScore();
    </script>
    """

    html = html.replace("__ITEMS_JSON__", items_json)

    components.html(html, height=800, scrolling=True)


word_card_speaking_game(WORD_THEMES)
