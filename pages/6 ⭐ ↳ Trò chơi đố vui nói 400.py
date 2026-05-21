import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Daily English 400 Word Speaking Game",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# Daily English 400 word data
# =========================================================
WORD_THEMES = {'🏫 Đời sống học đường': [{'word': 'subject', 'meaning': 'môn học'},
                          {'word': 'math', 'meaning': 'toán'},
                          {'word': 'science', 'meaning': 'khoa học'},
                          {'word': 'history', 'meaning': 'lịch sử'},
                          {'word': 'music', 'meaning': 'âm nhạc'},
                          {'word': 'art', 'meaning': 'mỹ thuật'},
                          {'word': 'P.E.', 'meaning': 'thể dục'},
                          {'word': 'club', 'meaning': 'câu lạc bộ'},
                          {'word': 'schedule', 'meaning': 'thời khóa biểu'},
                          {'word': 'semester', 'meaning': 'học kỳ'},
                          {'word': 'assignment', 'meaning': 'bài tập'},
                          {'word': 'project', 'meaning': 'dự án'},
                          {'word': 'presentation', 'meaning': 'bài thuyết trình'},
                          {'word': 'report', 'meaning': 'báo cáo'},
                          {'word': 'textbook', 'meaning': 'sách giáo khoa'},
                          {'word': 'workbook', 'meaning': 'sách bài tập'},
                          {'word': 'library', 'meaning': 'thư viện'},
                          {'word': 'cafeteria', 'meaning': 'nhà ăn'},
                          {'word': 'hallway', 'meaning': 'hành lang'},
                          {'word': 'attendance', 'meaning': 'điểm danh'}],
 '✏️ Hoạt động lớp học': [{'word': 'copy', 'meaning': 'chép lại'},
                          {'word': 'repeat', 'meaning': 'lặp lại'},
                          {'word': 'underline', 'meaning': 'gạch chân'},
                          {'word': 'circle', 'meaning': 'khoanh tròn'},
                          {'word': 'choose', 'meaning': 'chọn'},
                          {'word': 'check', 'meaning': 'kiểm tra'},
                          {'word': 'match', 'meaning': 'nối, ghép'},
                          {'word': 'complete', 'meaning': 'hoàn thành'},
                          {'word': 'fill', 'meaning': 'điền vào'},
                          {'word': 'spell', 'meaning': 'đánh vần'},
                          {'word': 'pronounce', 'meaning': 'phát âm'},
                          {'word': 'review', 'meaning': 'ôn tập'},
                          {'word': 'explain', 'meaning': 'giải thích'},
                          {'word': 'describe', 'meaning': 'miêu tả'},
                          {'word': 'compare', 'meaning': 'so sánh'},
                          {'word': 'discuss', 'meaning': 'thảo luận'},
                          {'word': 'present', 'meaning': 'thuyết trình'},
                          {'word': 'take notes', 'meaning': 'ghi chép'},
                          {'word': 'turn in', 'meaning': 'nộp'},
                          {'word': 'hand out', 'meaning': 'phát cho'}],
 '🏠 Nhà cửa và cuộc sống': [{'word': 'living room', 'meaning': 'phòng khách'},
                            {'word': 'bedroom', 'meaning': 'phòng ngủ'},
                            {'word': 'kitchen', 'meaning': 'nhà bếp'},
                            {'word': 'balcony', 'meaning': 'ban công'},
                            {'word': 'floor', 'meaning': 'sàn nhà, tầng'},
                            {'word': 'wall', 'meaning': 'bức tường'},
                            {'word': 'roof', 'meaning': 'mái nhà'},
                            {'word': 'garden', 'meaning': 'khu vườn'},
                            {'word': 'yard', 'meaning': 'sân'},
                            {'word': 'sofa', 'meaning': 'ghế sofa'},
                            {'word': 'television', 'meaning': 'tivi'},
                            {'word': 'refrigerator', 'meaning': 'tủ lạnh'},
                            {'word': 'microwave', 'meaning': 'lò vi sóng'},
                            {'word': 'blanket', 'meaning': 'chăn'},
                            {'word': 'pillow', 'meaning': 'gối'},
                            {'word': 'towel', 'meaning': 'khăn'},
                            {'word': 'soap', 'meaning': 'xà phòng'},
                            {'word': 'mirror', 'meaning': 'gương'},
                            {'word': 'closet', 'meaning': 'tủ quần áo'},
                            {'word': 'trash', 'meaning': 'rác'}],
 '🌅 Thói quen hằng ngày': [{'word': 'routine', 'meaning': 'thói quen hằng ngày'},
                           {'word': 'wake up', 'meaning': 'thức dậy'},
                           {'word': 'get up', 'meaning': 'ngủ dậy'},
                           {'word': 'brush', 'meaning': 'chải, đánh'},
                           {'word': 'shower', 'meaning': 'tắm vòi sen'},
                           {'word': 'dress', 'meaning': 'váy liền, đầm'},
                           {'word': 'leave', 'meaning': 'rời đi'},
                           {'word': 'arrive', 'meaning': 'đến nơi'},
                           {'word': 'return', 'meaning': 'trở về'},
                           {'word': 'finish', 'meaning': 'kết thúc'},
                           {'word': 'relax', 'meaning': 'thư giãn'},
                           {'word': 'weekday', 'meaning': 'ngày trong tuần'},
                           {'word': 'weekend', 'meaning': 'cuối tuần'},
                           {'word': 'usually', 'meaning': 'thường thường'},
                           {'word': 'often', 'meaning': 'thường xuyên'},
                           {'word': 'sometimes', 'meaning': 'thỉnh thoảng'},
                           {'word': 'always', 'meaning': 'luôn luôn'},
                           {'word': 'never', 'meaning': 'không bao giờ'},
                           {'word': 'habit', 'meaning': 'thói quen'},
                           {'word': 'lifestyle', 'meaning': 'lối sống'}],
 '🎮 Sở thích và thời gian rảnh': [{'word': 'hobby', 'meaning': 'sở thích'},
                                  {'word': 'movie', 'meaning': 'phim'},
                                  {'word': 'drama', 'meaning': 'phim truyền hình'},
                                  {'word': 'song', 'meaning': 'bài hát'},
                                  {'word': 'concert', 'meaning': 'buổi hòa nhạc'},
                                  {'word': 'dance', 'meaning': 'nhảy, múa'},
                                  {'word': 'drawing', 'meaning': 'vẽ tranh'},
                                  {'word': 'painting', 'meaning': 'bức tranh, hội họa'},
                                  {'word': 'comic', 'meaning': 'truyện tranh'},
                                  {'word': 'novel', 'meaning': 'tiểu thuyết'},
                                  {'word': 'photography', 'meaning': 'chụp ảnh'},
                                  {'word': 'cooking', 'meaning': 'nấu ăn'},
                                  {'word': 'baking', 'meaning': 'làm bánh'},
                                  {'word': 'camping', 'meaning': 'cắm trại'},
                                  {'word': 'hiking', 'meaning': 'đi bộ đường dài'},
                                  {'word': 'fishing', 'meaning': 'câu cá'},
                                  {'word': 'free time', 'meaning': 'thời gian rảnh'},
                                  {'word': 'favorite', 'meaning': 'yêu thích nhất'},
                                  {'word': 'popular', 'meaning': 'phổ biến'},
                                  {'word': 'relaxing', 'meaning': 'thư giãn'}],
 '⚽ Thể thao và hoạt động': [{'word': 'soccer', 'meaning': 'bóng đá'},
                             {'word': 'baseball', 'meaning': 'bóng chày'},
                             {'word': 'basketball', 'meaning': 'bóng rổ'},
                             {'word': 'volleyball', 'meaning': 'bóng chuyền'},
                             {'word': 'tennis', 'meaning': 'quần vợt'},
                             {'word': 'badminton', 'meaning': 'cầu lông'},
                             {'word': 'swimming', 'meaning': 'bơi lội'},
                             {'word': 'cycling', 'meaning': 'đạp xe'},
                             {'word': 'skating', 'meaning': 'trượt băng'},
                             {'word': 'boxing', 'meaning': 'quyền anh'},
                             {'word': 'taekwondo', 'meaning': 'taekwondo'},
                             {'word': 'yoga', 'meaning': 'yoga'},
                             {'word': 'fitness', 'meaning': 'thể dục thể hình'},
                             {'word': 'field', 'meaning': 'sân, cánh đồng'},
                             {'word': 'court', 'meaning': 'sân thi đấu'},
                             {'word': 'stadium', 'meaning': 'sân vận động'},
                             {'word': 'coach', 'meaning': 'huấn luyện viên'},
                             {'word': 'match', 'meaning': 'nối, ghép'},
                             {'word': 'competition', 'meaning': 'cuộc thi, giải đấu'},
                             {'word': 'medal', 'meaning': 'huy chương'}],
 '🌦️ Thời tiết và mùa': [{'word': 'season', 'meaning': 'mùa'},
                         {'word': 'spring', 'meaning': 'mùa xuân'},
                         {'word': 'summer', 'meaning': 'mùa hè'},
                         {'word': 'fall', 'meaning': 'mùa thu'},
                         {'word': 'winter', 'meaning': 'mùa đông'},
                         {'word': 'cloudy', 'meaning': 'nhiều mây'},
                         {'word': 'rainy', 'meaning': 'có mưa'},
                         {'word': 'snowy', 'meaning': 'có tuyết'},
                         {'word': 'windy', 'meaning': 'có gió'},
                         {'word': 'stormy', 'meaning': 'có bão'},
                         {'word': 'foggy', 'meaning': 'có sương mù'},
                         {'word': 'dry', 'meaning': 'khô'},
                         {'word': 'wet', 'meaning': 'ướt'},
                         {'word': 'humid', 'meaning': 'ẩm'},
                         {'word': 'temperature', 'meaning': 'nhiệt độ'},
                         {'word': 'degree', 'meaning': 'độ'},
                         {'word': 'forecast', 'meaning': 'dự báo thời tiết'},
                         {'word': 'umbrella', 'meaning': 'ô, dù'},
                         {'word': 'raincoat', 'meaning': 'áo mưa'},
                         {'word': 'rainbow', 'meaning': 'cầu vồng'}],
 '🌳 Thiên nhiên và môi trường': [{'word': 'nature', 'meaning': 'thiên nhiên'},
                                 {'word': 'environment', 'meaning': 'môi trường'},
                                 {'word': 'plant', 'meaning': 'cây, thực vật'},
                                 {'word': 'forest', 'meaning': 'rừng'},
                                 {'word': 'lake', 'meaning': 'hồ'},
                                 {'word': 'ocean', 'meaning': 'đại dương'},
                                 {'word': 'island', 'meaning': 'hòn đảo'},
                                 {'word': 'desert', 'meaning': 'sa mạc'},
                                 {'word': 'field', 'meaning': 'sân, cánh đồng'},
                                 {'word': 'farm', 'meaning': 'nông trại'},
                                 {'word': 'village', 'meaning': 'ngôi làng'},
                                 {'word': 'leaf', 'meaning': 'lá'},
                                 {'word': 'root', 'meaning': 'rễ'},
                                 {'word': 'stone', 'meaning': 'đá'},
                                 {'word': 'sand', 'meaning': 'cát'},
                                 {'word': 'soil', 'meaning': 'đất'},
                                 {'word': 'plastic', 'meaning': 'nhựa'},
                                 {'word': 'recycle', 'meaning': 'tái chế'},
                                 {'word': 'protect', 'meaning': 'bảo vệ'},
                                 {'word': 'pollution', 'meaning': 'ô nhiễm'}],
 '🍽️ Nhà hàng và gọi món': [{'word': 'restaurant', 'meaning': 'nhà hàng'},
                            {'word': 'menu', 'meaning': 'thực đơn'},
                            {'word': 'seat', 'meaning': 'chỗ ngồi'},
                            {'word': 'waiter', 'meaning': 'nam phục vụ'},
                            {'word': 'waitress', 'meaning': 'nữ phục vụ'},
                            {'word': 'order', 'meaning': 'gọi món, đặt hàng'},
                            {'word': 'dish', 'meaning': 'món ăn, cái đĩa'},
                            {'word': 'meal', 'meaning': 'bữa ăn'},
                            {'word': 'soup', 'meaning': 'súp'},
                            {'word': 'salad', 'meaning': 'sa lát'},
                            {'word': 'steak', 'meaning': 'bít tết'},
                            {'word': 'pizza', 'meaning': 'pizza'},
                            {'word': 'pasta', 'meaning': 'mì Ý'},
                            {'word': 'burger', 'meaning': 'bánh burger'},
                            {'word': 'sandwich', 'meaning': 'bánh sandwich'},
                            {'word': 'dessert', 'meaning': 'món tráng miệng'},
                            {'word': 'spicy', 'meaning': 'cay'},
                            {'word': 'sweet', 'meaning': 'ngọt'},
                            {'word': 'bill', 'meaning': 'hóa đơn'},
                            {'word': 'receipt', 'meaning': 'biên lai'}],
 '🛍️ Mua sắm và giá cả': [{'word': 'shop', 'meaning': 'cửa hàng'},
                          {'word': 'market', 'meaning': 'chợ'},
                          {'word': 'mall', 'meaning': 'trung tâm mua sắm'},
                          {'word': 'supermarket', 'meaning': 'siêu thị'},
                          {'word': 'cashier', 'meaning': 'thu ngân'},
                          {'word': 'customer', 'meaning': 'khách hàng'},
                          {'word': 'price', 'meaning': 'giá'},
                          {'word': 'sale', 'meaning': 'giảm giá'},
                          {'word': 'discount', 'meaning': 'giảm giá'},
                          {'word': 'coupon', 'meaning': 'phiếu giảm giá'},
                          {'word': 'change', 'meaning': 'tiền thối lại'},
                          {'word': 'coin', 'meaning': 'đồng xu'},
                          {'word': 'bill', 'meaning': 'hóa đơn'},
                          {'word': 'expensive', 'meaning': 'đắt'},
                          {'word': 'cheap', 'meaning': 'rẻ'},
                          {'word': 'size', 'meaning': 'kích cỡ'},
                          {'word': 'color', 'meaning': 'màu sắc'},
                          {'word': 'brand', 'meaning': 'thương hiệu'},
                          {'word': 'exchange', 'meaning': 'đổi hàng'},
                          {'word': 'refund', 'meaning': 'hoàn tiền'}],
 '👕 Quần áo và ngoại hình': [{'word': 'T-shirt', 'meaning': 'áo thun'},
                             {'word': 'pants', 'meaning': 'quần dài'},
                             {'word': 'jeans', 'meaning': 'quần jean'},
                             {'word': 'shorts', 'meaning': 'quần ngắn'},
                             {'word': 'skirt', 'meaning': 'váy'},
                             {'word': 'dress', 'meaning': 'váy liền, đầm'},
                             {'word': 'jacket', 'meaning': 'áo khoác'},
                             {'word': 'coat', 'meaning': 'áo khoác dài'},
                             {'word': 'sweater', 'meaning': 'áo len'},
                             {'word': 'hoodie', 'meaning': 'áo hoodie'},
                             {'word': 'uniform', 'meaning': 'đồng phục'},
                             {'word': 'socks', 'meaning': 'tất, vớ'},
                             {'word': 'sneakers', 'meaning': 'giày thể thao'},
                             {'word': 'boots', 'meaning': 'ủng'},
                             {'word': 'sandals', 'meaning': 'dép xăng đan'},
                             {'word': 'scarf', 'meaning': 'khăn quàng cổ'},
                             {'word': 'gloves', 'meaning': 'găng tay'},
                             {'word': 'belt', 'meaning': 'thắt lưng'},
                             {'word': 'glasses', 'meaning': 'kính'},
                             {'word': 'comfortable', 'meaning': 'thoải mái'}],
 '🚇 Giao thông và chỉ đường': [{'word': 'bus stop', 'meaning': 'trạm xe buýt'},
                               {'word': 'subway', 'meaning': 'tàu điện ngầm'},
                               {'word': 'airport', 'meaning': 'sân bay'},
                               {'word': 'terminal', 'meaning': 'bến, nhà ga'},
                               {'word': 'platform', 'meaning': 'sân ga'},
                               {'word': 'route', 'meaning': 'tuyến đường'},
                               {'word': 'direction', 'meaning': 'hướng'},
                               {'word': 'straight', 'meaning': 'đi thẳng'},
                               {'word': 'corner', 'meaning': 'góc đường'},
                               {'word': 'block', 'meaning': 'khu, dãy nhà'},
                               {'word': 'traffic', 'meaning': 'giao thông'},
                               {'word': 'crosswalk', 'meaning': 'vạch qua đường'},
                               {'word': 'sidewalk', 'meaning': 'vỉa hè'},
                               {'word': 'bridge', 'meaning': 'cây cầu'},
                               {'word': 'tunnel', 'meaning': 'đường hầm'},
                               {'word': 'entrance', 'meaning': 'lối vào'},
                               {'word': 'exit', 'meaning': 'lối ra'},
                               {'word': 'transfer', 'meaning': 'chuyển tuyến'},
                               {'word': 'lost', 'meaning': 'bị lạc'},
                               {'word': 'guide', 'meaning': 'hướng dẫn, hướng dẫn viên'}],
 '🧳 Du lịch và lưu trú': [{'word': 'travel', 'meaning': 'du lịch'},
                          {'word': 'trip', 'meaning': 'chuyến đi'},
                          {'word': 'vacation', 'meaning': 'kỳ nghỉ'},
                          {'word': 'tourist', 'meaning': 'khách du lịch'},
                          {'word': 'guide', 'meaning': 'hướng dẫn, hướng dẫn viên'},
                          {'word': 'passport', 'meaning': 'hộ chiếu'},
                          {'word': 'flight', 'meaning': 'chuyến bay'},
                          {'word': 'hotel', 'meaning': 'khách sạn'},
                          {'word': 'motel', 'meaning': 'nhà nghỉ ven đường'},
                          {'word': 'hostel', 'meaning': 'nhà trọ'},
                          {'word': 'reservation', 'meaning': 'đặt chỗ'},
                          {'word': 'check in', 'meaning': 'nhận phòng'},
                          {'word': 'check out', 'meaning': 'trả phòng'},
                          {'word': 'luggage', 'meaning': 'hành lý'},
                          {'word': 'suitcase', 'meaning': 'vali'},
                          {'word': 'backpack', 'meaning': 'ba lô'},
                          {'word': 'souvenir', 'meaning': 'quà lưu niệm'},
                          {'word': 'museum', 'meaning': 'bảo tàng'},
                          {'word': 'famous', 'meaning': 'nổi tiếng'},
                          {'word': 'local', 'meaning': 'địa phương'}],
 '👥 Quan hệ bạn bè': [{'word': 'friendship', 'meaning': 'tình bạn'},
                      {'word': 'best friend', 'meaning': 'bạn thân nhất'},
                      {'word': 'teammate', 'meaning': 'đồng đội'},
                      {'word': 'partner', 'meaning': 'bạn cùng nhóm, đối tác'},
                      {'word': 'message', 'meaning': 'tin nhắn'},
                      {'word': 'call', 'meaning': 'gọi điện'},
                      {'word': 'chat', 'meaning': 'trò chuyện'},
                      {'word': 'invite', 'meaning': 'mời'},
                      {'word': 'visit', 'meaning': 'thăm'},
                      {'word': 'meet', 'meaning': 'gặp'},
                      {'word': 'hang out', 'meaning': 'đi chơi'},
                      {'word': 'laugh', 'meaning': 'cười'},
                      {'word': 'share', 'meaning': 'chia sẻ'},
                      {'word': 'trust', 'meaning': 'tin tưởng'},
                      {'word': 'promise', 'meaning': 'lời hứa, hứa'},
                      {'word': 'secret', 'meaning': 'bí mật'},
                      {'word': 'joke', 'meaning': 'trò đùa'},
                      {'word': 'together', 'meaning': 'cùng nhau'},
                      {'word': 'alone', 'meaning': 'một mình'},
                      {'word': 'forgive', 'meaning': 'tha thứ'}],
 '😊 Cảm xúc mở rộng': [{'word': 'excited', 'meaning': 'hào hứng'},
                       {'word': 'nervous', 'meaning': 'lo lắng, hồi hộp'},
                       {'word': 'bored', 'meaning': 'chán'},
                       {'word': 'surprised', 'meaning': 'ngạc nhiên'},
                       {'word': 'confused', 'meaning': 'bối rối'},
                       {'word': 'embarrassed', 'meaning': 'xấu hổ, ngượng'},
                       {'word': 'proud', 'meaning': 'tự hào'},
                       {'word': 'disappointed', 'meaning': 'thất vọng'},
                       {'word': 'lonely', 'meaning': 'cô đơn'},
                       {'word': 'relaxed', 'meaning': 'thư thái'},
                       {'word': 'calm', 'meaning': 'bình tĩnh'},
                       {'word': 'upset', 'meaning': 'buồn bực'},
                       {'word': 'interested', 'meaning': 'quan tâm, thích thú'},
                       {'word': 'satisfied', 'meaning': 'hài lòng'},
                       {'word': 'thankful', 'meaning': 'biết ơn'},
                       {'word': 'hopeful', 'meaning': 'đầy hy vọng'},
                       {'word': 'mood', 'meaning': 'tâm trạng'},
                       {'word': 'stress', 'meaning': 'căng thẳng'},
                       {'word': 'confidence', 'meaning': 'sự tự tin'},
                       {'word': 'courage', 'meaning': 'lòng can đảm'}],
 '💭 Suy nghĩ và ý kiến': [{'word': 'think', 'meaning': 'nghĩ'},
                          {'word': 'believe', 'meaning': 'tin'},
                          {'word': 'guess', 'meaning': 'đoán'},
                          {'word': 'remember', 'meaning': 'nhớ'},
                          {'word': 'forget', 'meaning': 'quên'},
                          {'word': 'mean', 'meaning': 'có nghĩa là'},
                          {'word': 'agree', 'meaning': 'đồng ý'},
                          {'word': 'disagree', 'meaning': 'không đồng ý'},
                          {'word': 'opinion', 'meaning': 'ý kiến'},
                          {'word': 'idea', 'meaning': 'ý tưởng'},
                          {'word': 'reason', 'meaning': 'lý do'},
                          {'word': 'example', 'meaning': 'ví dụ'},
                          {'word': 'fact', 'meaning': 'sự thật'},
                          {'word': 'choice', 'meaning': 'sự lựa chọn'},
                          {'word': 'decision', 'meaning': 'quyết định'},
                          {'word': 'advice', 'meaning': 'lời khuyên'},
                          {'word': 'suggestion', 'meaning': 'gợi ý, đề xuất'},
                          {'word': 'possible', 'meaning': 'có thể'},
                          {'word': 'impossible', 'meaning': 'không thể'},
                          {'word': 'confusing', 'meaning': 'khó hiểu'}],
 '📅 Kế hoạch và cuộc hẹn': [{'word': 'plan', 'meaning': 'kế hoạch'},
                            {'word': 'appointment', 'meaning': 'cuộc hẹn'},
                            {'word': 'promise', 'meaning': 'lời hứa, hứa'},
                            {'word': 'meeting', 'meaning': 'cuộc họp, buổi gặp'},
                            {'word': 'date', 'meaning': 'ngày, cuộc hẹn'},
                            {'word': 'event', 'meaning': 'sự kiện'},
                            {'word': 'party', 'meaning': 'bữa tiệc'},
                            {'word': 'festival', 'meaning': 'lễ hội'},
                            {'word': 'deadline', 'meaning': 'hạn chót'},
                            {'word': 'calendar', 'meaning': 'lịch'},
                            {'word': 'next week', 'meaning': 'tuần sau'},
                            {'word': 'message', 'meaning': 'tin nhắn'},
                            {'word': 'join', 'meaning': 'tham gia'},
                            {'word': 'prepare', 'meaning': 'chuẩn bị'},
                            {'word': 'decide', 'meaning': 'quyết định'},
                            {'word': 'change', 'meaning': 'tiền thối lại'},
                            {'word': 'cancel', 'meaning': 'hủy'},
                            {'word': 'on time', 'meaning': 'đúng giờ'},
                            {'word': 'available', 'meaning': 'có sẵn, rảnh'},
                            {'word': 'reminder', 'meaning': 'lời nhắc'}],
 '🩺 Cuộc sống lành mạnh': [{'word': 'health', 'meaning': 'sức khỏe'},
                           {'word': 'body', 'meaning': 'cơ thể'},
                           {'word': 'eye', 'meaning': 'mắt'},
                           {'word': 'ear', 'meaning': 'tai'},
                           {'word': 'nose', 'meaning': 'mũi'},
                           {'word': 'mouth', 'meaning': 'miệng'},
                           {'word': 'tooth', 'meaning': 'răng'},
                           {'word': 'hand', 'meaning': 'bàn tay'},
                           {'word': 'arm', 'meaning': 'cánh tay'},
                           {'word': 'leg', 'meaning': 'chân'},
                           {'word': 'foot', 'meaning': 'bàn chân'},
                           {'word': 'stomach', 'meaning': 'bụng, dạ dày'},
                           {'word': 'back', 'meaning': 'lưng'},
                           {'word': 'heart', 'meaning': 'tim'},
                           {'word': 'clinic', 'meaning': 'phòng khám'},
                           {'word': 'vitamin', 'meaning': 'vitamin'},
                           {'word': 'diet', 'meaning': 'chế độ ăn'},
                           {'word': 'cough', 'meaning': 'ho'},
                           {'word': 'flu', 'meaning': 'cúm'},
                           {'word': 'breathe', 'meaning': 'thở'}],
 '📱 Truyền thông và điện thoại': [{'word': 'smartphone', 'meaning': 'điện thoại thông minh'},
                                  {'word': 'screen', 'meaning': 'màn hình'},
                                  {'word': 'app', 'meaning': 'ứng dụng'},
                                  {'word': 'website', 'meaning': 'trang web'},
                                  {'word': 'internet', 'meaning': 'internet'},
                                  {'word': 'Wi-Fi', 'meaning': 'Wi-Fi'},
                                  {'word': 'password', 'meaning': 'mật khẩu'},
                                  {'word': 'text', 'meaning': 'tin nhắn văn bản'},
                                  {'word': 'video call', 'meaning': 'cuộc gọi video'},
                                  {'word': 'gallery', 'meaning': 'thư viện ảnh'},
                                  {'word': 'news', 'meaning': 'tin tức'},
                                  {'word': 'channel', 'meaning': 'kênh'},
                                  {'word': 'post', 'meaning': 'bài đăng'},
                                  {'word': 'comment', 'meaning': 'bình luận'},
                                  {'word': 'upload', 'meaning': 'tải lên'},
                                  {'word': 'download', 'meaning': 'tải xuống'},
                                  {'word': 'search', 'meaning': 'tìm kiếm'},
                                  {'word': 'click', 'meaning': 'nhấp chuột'},
                                  {'word': 'battery', 'meaning': 'pin'},
                                  {'word': 'notification', 'meaning': 'thông báo'}],
 '🌈 Nghề nghiệp và tương lai': [{'word': 'job', 'meaning': 'nghề nghiệp'},
                                {'word': 'work', 'meaning': 'làm việc'},
                                {'word': 'company', 'meaning': 'công ty'},
                                {'word': 'office', 'meaning': 'văn phòng'},
                                {'word': 'factory', 'meaning': 'nhà máy'},
                                {'word': 'engineer', 'meaning': 'kỹ sư'},
                                {'word': 'mechanic', 'meaning': 'thợ máy'},
                                {'word': 'chef', 'meaning': 'đầu bếp'},
                                {'word': 'firefighter', 'meaning': 'lính cứu hỏa'},
                                {'word': 'farmer', 'meaning': 'nông dân'},
                                {'word': 'designer', 'meaning': 'nhà thiết kế'},
                                {'word': 'singer', 'meaning': 'ca sĩ'},
                                {'word': 'actor', 'meaning': 'diễn viên'},
                                {'word': 'athlete', 'meaning': 'vận động viên'},
                                {'word': 'dream', 'meaning': 'ước mơ'},
                                {'word': 'future', 'meaning': 'tương lai'},
                                {'word': 'goal', 'meaning': 'mục tiêu'},
                                {'word': 'skill', 'meaning': 'kỹ năng'},
                                {'word': 'interview', 'meaning': 'phỏng vấn'},
                                {'word': 'experience', 'meaning': 'kinh nghiệm'}]}


# =========================================================
# Vietnamese meaning data
# =========================================================
# Speaking card game component
# =========================================================
def daily_word_card_speaking_game(word_themes):
    items = []
    for cat, words in word_themes.items():
        cat_emoji = cat.split()[0] if cat else "🌱"
        for item in words:
            new_item = dict(item)
            new_item["cat"] = cat
            new_item["emoji"] = cat_emoji
            items.append(new_item)

    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="daily-word-card-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 50%, #fff7ed 100%);
        border: 1.5px solid #bbf7d0;
        border-radius: 30px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        max-width: 100%;
        overflow-x: hidden;
        box-sizing: border-box;
    ">
        <style>
            #daily-word-card-app * {
                box-sizing: border-box;
            }

            #daily-word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }

            #daily-word-card-app select {
                max-width: 100%;
            }

            #cardBox {
                position: relative;
                overflow: hidden;
                transform-origin: center center;
                will-change: transform, opacity, filter;
            }

            /* transition effect when moving to the next word */
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
                0% {
                    opacity: 0;
                    transform: translateX(46px) scale(0.965);
                    filter: blur(3px) brightness(1.05);
                }
                55% {
                    opacity: 1;
                    transform: translateX(-7px) scale(1.012);
                    filter: blur(0) brightness(1.03);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                    filter: blur(0) brightness(1);
                }
            }

            @keyframes nextBadgePop {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-18px) scale(0.86);
                }
                20% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1.04);
                }
                62% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-8px) scale(0.96);
                }
            }

            @keyframes nextLightSweep {
                0% {
                    opacity: 0;
                    transform: translateX(-115%);
                }
                20% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    transform: translateX(115%);
                }
            }

            @media (max-width: 768px) {
                #daily-word-card-app {
                    padding: 14px !important;
                    border-radius: 22px !important;
                }

                #categorySelect {
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

                #emojiBox {
                    font-size: 72px !important;
                }

                #meaningBox {
                    font-size: 32px !important;
                    line-height: 1.25 !important;
                }

                #answerBox {
                    font-size: 27px !important;
                    padding: 14px 12px !important;
                    word-break: break-word;
                }

                #buttonBox button {
                    flex: 1 1 100%;
                    font-size: 16px !important;
                    padding: 13px 12px !important;
                }

                #transcriptBox {
                    font-size: 19px !important;
                }

                #resultBox {
                    font-size: 17px !important;
                }
            }
        </style>

        <div id="topControlBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">Chọn phạm vi từ vựng</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bbf7d0;
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
            ">🎲 Trộn phạm vi này</button>

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
                ">Đúng 0 / 0 · Cần luyện tập 0 từ</div>
            </div>

            <div id="cardBox" style="
                background:white;
                border-radius:32px;
                padding:30px 24px;
                border:1.5px solid #dcfce7;
                box-shadow:0 8px 24px rgba(0,0,0,0.07);
                text-align:center;
                margin-bottom:18px;
            ">
                <div id="emojiBox" style="
                    font-size: 96px;
                    line-height: 1.1;
                    margin-bottom: 14px;
                ">🌱</div>

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
                " id="meaningLangBadge">Nghĩa tiếng Việt</div>

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
                    word-break:break-word;
                ">hint</div>

                <div id="cardFeedbackBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:28px;
                    font-weight:900;
                    margin-top:14px;
                    word-break:break-word;
                ">✅ Đúng rồi!</div>
            </div>

            <div id="buttonBox" style="margin-bottom:16px;">
                <div style="display:grid; grid-template-columns:1fr; gap:8px; margin-bottom:8px;">
                    <button id="micBtn" style="
                        width:100%;
                        border:1.5px solid #fecaca;
                        background:#fff1f2;
                        color:#be123c;
                        border-radius:999px;
                        padding:15px 20px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:18px;
                    ">🎙️ Nói tiếng Anh</button>
                </div>

                <div style="
                    background:#f8fafc;
                    border:1.5px solid #e2e8f0;
                    border-radius:18px;
                    padding:12px 14px;
                    margin-bottom:8px;
                    min-height:54px;
                ">
                    <div style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px;">Từ được nhận dạng</div>
                    <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155; word-break:break-word;"></div>
                </div>

                <div id="smallButtonRow" style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px;">
                    <button id="hintBtn" style="
                        border:1.5px solid #fed7aa;
                        background:#fff7ed;
                        color:#9a3412;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">💡 Gợi ý</button>

                    <button id="answerBtn" style="
                        border:1.5px solid #bfdbfe;
                        background:#eff6ff;
                        color:#1d4ed8;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">Đáp án+🔊</button>

                    <button id="skipBtn" style="
                        border:1.5px solid #c7d2fe;
                        background:#eef2ff;
                        color:#3730a3;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">Tiếp ➡️</button>
                </div>
            </div>

            <div id="resultBox" style="
                display:none;
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:10px 12px;
                font-size:16px;
                font-weight:900;
                color:#334155;
            ">
                Nhấn nút micro và nói từ tiếng Anh. Đây là hoạt động kiểm tra xem bạn có biết từ hay không, không phải bài kiểm tra phát âm.
            </div>
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
            <div id="finishTitle" style="
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
            ">Đúng 0 / 0 · Cần luyện tập 0 từ</div>
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
    const meaningLangBadge = document.getElementById("meaningLangBadge");
    const answerBox = document.getElementById("answerBox");
    const hintBox = document.getElementById("hintBox");
    const cardFeedbackBox = document.getElementById("cardFeedbackBox");

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

    function uniqueCategories() {
        const ranges = [];
        const chunkSize = 50;

        for (let start = 0; start < ITEMS.length; start += chunkSize) {
            const end = Math.min(start + chunkSize, ITEMS.length);
            ranges.push((start + 1) + "~" + end);
        }

        return ranges;
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
        const selected = categorySelect.value;
        const chunkSize = 50;

        if (!selected || selected.indexOf("~") === -1) {
            return ITEMS.slice(0, chunkSize);
        }

        const parts = selected.split("~");
        const start = parseInt(parts[0], 10) - 1;
        const end = parseInt(parts[1], 10);

        return ITEMS.slice(start, end);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
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
            .replace(/\bp\.?e\.?\b/g, "pe")
            .replace(/\bphysical education\b/g, "pe")
            .replace(/\bt shirt\b/g, "tshirt")
            .replace(/\btee shirt\b/g, "tshirt")
            .replace(/\bwi fi\b/g, "wifi")
            .replace(/\bwi-fi\b/g, "wifi")
            .replace(/\bwifi\b/g, "wifi")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
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
            for (let j = 0; j <= b.length; j++) {
                dp[i][j] = 0;
            }
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
            "you": ["you", "u", "yew", "yo", "ya", "your"],
            "he": ["he", "hi", "hey"],
            "she": ["she", "see", "sea", "shi", "seat"],
            "we": ["we", "wee", "wi", "me", "be"],
            "they": ["they", "day", "dey", "the", "there", "their", "that"],
            "one": ["one", "won"],
            "two": ["two", "to", "too"],
            "three": ["three", "tree", "free"],
            "four": ["four", "for"],
            "five": ["five", "fife"],
            "six": ["six", "sex", "sick"],
            "eight": ["eight", "ate"],
            "here": ["here", "hear"],
            "there": ["there", "their"],
            "right": ["right", "write", "light"],
            "wait": ["wait", "weight"],
            "know": ["know", "no"],
            "okay": ["okay", "ok", "kay"],
            "pe": ["pe", "pee", "p", "physicaleducation"],
            "wifi": ["wifi", "wi", "wifei"],
            "tshirt": ["tshirt", "teeshirt", "t shirt", "tee shirt"],
            "math": ["math", "mat", "mass", "meth", "matt"],
            "art": ["art", "heart", "at"],
            "science": ["science", "sience", "signs"],
            "history": ["history", "his story", "hisstory"],
            "music": ["music", "musick"]
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

    function soundOverlap(a, b) {
        const ka = soundKey(a);
        const kb = soundKey(b);

        if (!ka || !kb) return 0;
        if (ka === kb) return 1;

        let overlap = 0;
        for (let i = 0; i < ka.length; i++) {
            if (kb.indexOf(ka.charAt(i)) !== -1) overlap += 1;
        }

        return overlap / Math.max(1, Math.min(ka.length, kb.length));
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
        if (typeof KNOWN_ANSWER_WORDS === "undefined") return false;
        if (!KNOWN_ANSWER_WORDS.includes(sw)) return false;
        if (sw === aw) return false;
        if (aliasMatch(sw, aw)) return false;

        const sim = wordSimilarity(sw, aw);
        const soundSim = wordSimilarity(soundKey(sw), soundKey(aw));
        const vowelSim = wordSimilarity(vowelLooseKey(sw), vowelLooseKey(aw));

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        // Do not block possible ASR misrecognitions too strictly.
        // Example: art→heart, math→mass, clothes→close, weather→whether
        // But clearly different words are marked incorrect.
        const hasClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            hasSharedBigram(sw, aw) ||
            sim >= 0.38 ||
            soundSim >= 0.28 ||
            vowelSim >= 0.30;

        return !hasClue;
    }

    function isSmallRecognitionMistake(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        // Pronouns with different meanings are not accepted unless listed as aliases.
        const pronouns = ["i", "you", "he", "she", "we", "they"];
        if (pronouns.includes(aw) && pronouns.includes(sw) && aw !== sw) {
            return false;
        }

        // A clearly different known word is incorrect.
        if (isClearlyDifferentKnownWord(sw, aw)) {
            return false;
        }

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

        const soundSameFirst =
            soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);

        const soundSameLast =
            soundSw && soundAw &&
            soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);

        const overlap = soundOverlap(sw, aw);

        // Minimum clue to prevent clearly different answers.
        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            hasSharedBigram(sw, aw) ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25 ||
            sim >= 0.28 ||
            overlap >= 0.28;

        if (!hasAnyClue) return false;

        // Allow partial or merged ASR results for one-word recognition.
        // Example: refrigerator → refriger, cafeteria → cafe, comfortable → comfort
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) {
            return true;
        }

        // Accept if the consonant skeleton is similar.
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.22) return true;

        // 1-2 letter words: be generous for short items like P.E.
        if (aw.length <= 2) {
            return (
                sim >= 0.50 ||
                soundSim >= 0.28 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast
            );
        }

        // 3-4 letter words: especially generous.
        // ASR can be unstable for short words like art, club, copy, etc.
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.30 ||
                soundSim >= 0.20 ||
                vowelSim >= 0.24 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast ||
                hasSharedBigram(sw, aw)
            );
        }

        // 5-6 letter words: allow several character differences.
        if (aw.length <= 6) {
            return (
                dist <= 4 ||
                sim >= 0.32 ||
                soundSim >= 0.22 ||
                vowelSim >= 0.25 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // Long words: accept partial syllable matches.
        return (
            dist <= 6 ||
            sim >= 0.28 ||
            soundSim >= 0.20 ||
            vowelSim >= 0.22 ||
            sameFirst ||
            sameFirstTwo ||
            sameFirstThree ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function hasEnglishText(text) {
        return /[a-zA-Z]/.test(String(text || ""));
    }

    function isCorrectSpeech(spoken, answer) {
        // If no English letters are detected, treat it as incorrect.
        if (!hasEnglishText(String(spoken || ""))) return false;

        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        // One-word answer:
        // This checks word knowledge, not pronunciation, so it is generous.
        if (answerWords.length === 1) {
            const target = answerWords[0];

            // If the recognized phrase is similar, it is correct.
            // Example: "a subject", "the subject", "subject please"
            if (isSmallRecognitionMistake(s, target)) return true;

            // If any candidate word is similar, it is correct.
            for (const sw of spokenWords) {
                if (isSmallRecognitionMistake(sw, target)) {
                    return true;
                }
            }

            // If the browser merges words.
            const joinedSpoken = spokenWords.join("");
            if (isSmallRecognitionMistake(joinedSpoken, target)) return true;

            // Check again after removing fillers.
            const fillerRemoved = spokenWords.filter(w =>
                !["a", "an", "the", "uh", "um", "please", "yes", "no", "is", "it"].includes(w)
            );

            if (fillerRemoved.length > 0) {
                const joinedClean = fillerRemoved.join("");
                if (isSmallRecognitionMistake(joinedClean, target)) return true;

                for (const w of fillerRemoved) {
                    if (isSmallRecognitionMistake(w, target)) return true;
                }
            }

            return false;
        }

        // Multi-word expression:
        if (s.includes(a)) return true;

        // Allow spacing differences like check in / take notes / living room.
        const joinedSpoken = spokenWords.join("");
        const joinedAnswer = answerWords.join("");
        if (isSmallRecognitionMistake(joinedSpoken, joinedAnswer)) return true;

        // Accept if core words appear in similar order.
        let pos = 0;

        for (const sw of spokenWords) {
            const target = answerWords[pos];
            if (!target) break;

            if (isSmallRecognitionMistake(sw, target)) {
                pos += 1;
            }

            if (pos >= answerWords.length) break;
        }

        return pos >= answerWords.length;
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
        scoreLabel.innerText = "Đúng " + correctCount + " / " + list.length + " · Cần luyện tập " + missedCount;
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

        finishScore.innerText = "Đúng " + correctCount + " / " + list.length + " · Cần luyện tập " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }

    function getCurrentMeaning(item) {
        return item.meaning || "";
    }

    function updateMeaningLanguageBadge() {
        if (!meaningLangBadge) return;
        meaningLangBadge.innerText = "Nghĩa tiếng Việt";
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();
        cleanupRecognition();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        emojiBox.innerText = currentItem.emoji || "🌱";
        updateMeaningLanguageBadge();
        meaningBox.innerText = getCurrentMeaning(currentItem);

        answerBox.style.display = "none";
        answerBox.innerText = "Đáp án: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        cardFeedbackBox.style.display = "none";
        cardFeedbackBox.innerText = "";

        transcriptBox.innerText = "";
        transcriptBox.style.color = "#334155";
        resultBox.innerText = "Nhấn nút micro và nói từ tiếng Anh. Đây là hoạt động kiểm tra xem bạn có biết từ hay không, không phải bài kiểm tra phát âm.";
        resultBox.style.background = "#f1f5f9";
        resultBox.style.borderColor = "#e2e8f0";
        resultBox.style.color = "#334155";

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

            // When correct, show the correct English word instead of raw ASR text.
            // Show the correct English word in the recognized-word box.
            // Example: subject ✅ correct
            cardFeedbackBox.style.display = "none";
            transcriptBox.innerHTML =
                "<span style='color:#334155;'>" + escapeHtml(currentItem.word) + "</span>" +
                " <span style='display:inline-block; margin-left:8px; padding:4px 9px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-size:0.82em; font-weight:900; vertical-align:middle;'>✅ Đúng rồi</span>";
            transcriptBox.style.color = "#334155";

            resultBox.innerText = "";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";

            speak(currentItem.word);

            // Do not move automatically after a correct answer.
            // Only the score increases; the student moves by pressing Next.
            cleanupRecognition();
            resultBox.style.display = "none";
            resultBox.innerText = "";
        } else {
            // When incorrect, keep the recognized word as it is.
            // Show only a short guide below.
            cardFeedbackBox.style.display = "none";
            transcriptBox.style.color = "#334155";
            resultBox.innerText = "Hãy nói lại.";
            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#9a3412";
        }
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "Trình duyệt này không hỗ trợ nhận dạng giọng nói. Hãy thử dùng Chrome.";
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

        // If already listening, clean up the previous recognition and restart.
        // Safety guard to prevent the button from getting stuck.
        cleanupRecognition();

        // Helps reduce mobile microphone-permission issues.
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(function(track) { track.stop(); });
            } catch (err) {
                resultBox.innerText = "Hãy cho phép micro rồi nhấn lại.";
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
        recognition.interimResults = false;
        recognition.continuous = false;
        recognition.maxAlternatives = 10;

        isListening = true;
        micBtn.disabled = true;
        micBtn.style.opacity = "0.72";
        micBtn.style.cursor = "wait";
        micBtn.innerText = "🎙️ Đang nghe...";

        resultBox.innerText = "Hãy nói.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";

        recognition.onresult = function(event) {
            if (thisRunId !== recognitionRunId) return;
            let bestTranscript = "";

            if (!event.results || !event.results[0]) {
                resetMicButton();
                return;
            }

            for (let i = 0; i < event.results[0].length; i++) {
                const transcript = event.results[0][i].transcript.trim();
                if (i === 0) bestTranscript = transcript;

                if (isCorrectSpeech(transcript, currentItem.word)) {
                    bestTranscript = transcript;
                    break;
                }
            }

            // Show recognized text at once.
            transcriptBox.style.color = "#334155";
            transcriptBox.innerText = bestTranscript;
            checkSpeech(bestTranscript);
        };

        recognition.onerror = function(event) {
            if (thisRunId !== recognitionRunId) return;
            if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                resultBox.innerText = "Hãy cho phép sử dụng micro.";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
            } else if (event.error === "no-speech") {
                resultBox.innerText = "Không nhận dạng được âm thanh. Hãy nhấn lại.";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            } else {
                resultBox.innerText = "Hãy nhấn lại.";
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

        // Restore the button even if onend is delayed or missing.
        setTimeout(function() {
            if (isListening) {
                resetMicButton();
            }
        }, 9000);

        micSafetyTimer = setTimeout(function() {
            if (thisRunId !== recognitionRunId) return;
            if (isListening) {
                try { recognition.abort(); } catch (e) {}
                try { recognition.stop(); } catch (e) {}
                recognition = null;
                resetMicButton();
            }
        }, 11000);

        try {
            recognition.start();
        } catch (err) {
            resultBox.innerText = "Hãy nhấn lại.";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";
            cleanupRecognition();
        }
    }

    function resetCurrentRange() {
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
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    randomBtn.addEventListener("click", function() {
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
        answerBox.innerText = "Đáp án: " + currentItem.word;
        speak(currentItem.word);
    });

    hintBtn.addEventListener("click", function() {
        if (!currentItem) return;

        const cleanWord = String(currentItem.word || "").trim();
        const words = cleanWord.split(/\s+/).filter(Boolean);

        const hintText = words.map(function(word) {
            const lettersOnly = word.replace(/[^a-zA-Z]/g, "");
            if (lettersOnly.length <= 2) return word;

            const firstTwo = lettersOnly.slice(0, 2);
            const blanks = "_".repeat(Math.max(1, lettersOnly.length - 2));

            return firstTwo + blanks;
        }).join(" ");

        hintBox.style.display = "block";
        hintBox.innerText = "Gợi ý: " + hintText;
    });

    skipBtn.addEventListener("click", function() {
        cleanupRecognition();
        if (currentItem && !correctMap[getItemKey(currentItem)]) {
            missedMap[getItemKey(currentItem)] = true;
            updateScore();
        }
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


daily_word_card_speaking_game(WORD_THEMES)
