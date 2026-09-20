import json
import os
import re
import sqlite3
import unicodedata
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# =========================================================
# CẤU HÌNH ỨNG DỤNG
# =========================================================
st.set_page_config(
    page_title="PULSE SPORT | Sport Shop & Knowledge Hub",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
ASSET_DIR = APP_DIR / "assets" / "generated"
ASSET_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = APP_DIR / "sport_shop.db"

BRAND = "PULSE SPORT"
FREE_SHIP_THRESHOLD = 700_000
DEFAULT_SHIPPING = 30_000

# =========================================================
# CSS - GIAO DIỆN THỂ THAO HIỆN ĐẠI
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ink: #111318;
        --muted: #68707f;
        --surface: #ffffff;
        --soft: #f4f6f8;
        --line: #e7e9ee;
        --lime: #d9ff43;
        --lime-dark: #b8df16;
        --charcoal: #171a20;
    }

    .stApp { background: #f7f8fa; color: var(--ink); }
    [data-testid="stSidebar"] { background: #111318; }
    [data-testid="stSidebar"] * { color: #f7f8fa; }
    [data-testid="stSidebar"] .stRadio label { padding: .18rem 0; }

    .hero {
        border-radius: 28px;
        padding: 42px 42px;
        background:
            radial-gradient(circle at 85% 20%, rgba(217,255,67,.26), transparent 34%),
            linear-gradient(135deg, #111318 0%, #252a34 100%);
        color: white;
        overflow: hidden;
        position: relative;
        box-shadow: 0 16px 45px rgba(17,19,24,.18);
        margin-bottom: 18px;
    }
    .hero h1 { font-size: 3rem; line-height: 1.02; margin: 0 0 14px 0; }
    .hero p { color: #d7dbe3; font-size: 1.05rem; max-width: 720px; }
    .hero-badge {
        display: inline-block; padding: 8px 12px; border-radius: 999px;
        background: var(--lime); color: #111318; font-weight: 800; margin-bottom: 16px;
    }

    .section-title { margin-top: 16px; margin-bottom: 8px; }
    .muted { color: var(--muted); }
    .price { font-size: 1.2rem; font-weight: 850; color: #111318; }
    .old-price { text-decoration: line-through; color: #8a909b; font-size: .9rem; }
    .rating { color: #555f6f; font-size: .92rem; }
    .pill {
        display:inline-block; padding:5px 9px; border-radius:999px;
        background:#eef1f4; margin-right:5px; margin-bottom:5px; font-size:.78rem;
    }
    .sale-pill {
        display:inline-block; padding:5px 9px; border-radius:999px;
        background:#111318; color:#d9ff43; font-size:.76rem; font-weight:800;
    }
    .notice {
        background:#f0ffd0; border:1px solid #d9ff43; border-radius:14px;
        padding:13px 15px; color:#252a34;
    }
    .blog-card {
        background:white; border:1px solid #e7e9ee; border-radius:18px;
        padding:20px; min-height:170px; box-shadow:0 7px 20px rgba(20,25,35,.05);
        margin-bottom: 12px;
    }
    .blog-meta { color:#7b8391; font-size:.82rem; }
    .feature {
        background:white; border:1px solid #e7e9ee; border-radius:18px;
        padding:20px; min-height:135px;
    }
    .footer {
        margin-top: 38px; padding: 26px 8px; border-top:1px solid #e2e5ea;
        color:#7c8490; font-size:.88rem;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius:12px; font-weight:750; min-height:42px;
    }
    div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] {
        background:#171a20; border-color:#171a20;
    }
    [data-testid="stMetric"] {
        background:white; border:1px solid #e7e9ee; border-radius:16px; padding:12px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DỮ LIỆU SẢN PHẨM
# =========================================================
PRODUCTS: List[Dict] = [
    {
        "id": "SP001", "name": "Áo Training Dry-Fit Pro", "category": "Quần áo",
        "price": 329_000, "old_price": 399_000, "rating": 4.8, "reviews": 186, "stock": 34,
        "badge": "Bán chạy", "color": (35, 41, 53), "accent": (217, 255, 67),
        "desc": "Áo tập co giãn 4 chiều, thoát ẩm nhanh, phù hợp gym, chạy bộ và vận động cường độ cao.",
        "specs": ["Polyester pha Spandex", "Co giãn 4 chiều", "Nhanh khô", "Size S–XXL"],
    },
    {
        "id": "SP002", "name": "Quần Short Flex 2-in-1", "category": "Quần áo",
        "price": 389_000, "old_price": 459_000, "rating": 4.7, "reviews": 122, "stock": 28,
        "badge": "Mới", "color": (31, 67, 86), "accent": (79, 217, 255),
        "desc": "Quần short thể thao 2 lớp hỗ trợ vận động linh hoạt, có túi khóa kéo và lớp lót ôm nhẹ.",
        "specs": ["Thiết kế 2 lớp", "Túi khóa kéo", "Cạp co giãn", "Size M–XXL"],
    },
    {
        "id": "SP003", "name": "Giày Running Velocity X", "category": "Giày thể thao",
        "price": 1_290_000, "old_price": 1_490_000, "rating": 4.9, "reviews": 244, "stock": 16,
        "badge": "Top Rated", "color": (44, 44, 56), "accent": (255, 121, 63),
        "desc": "Giày chạy hằng ngày với đệm êm, upper thoáng khí và đế bám tốt cho đường nhựa.",
        "specs": ["Trọng lượng ~275 g", "Đệm EVA đàn hồi", "Mesh thoáng khí", "Size 38–44"],
    },
    {
        "id": "SP004", "name": "Găng Tay Gym GripMax", "category": "Găng & phụ kiện",
        "price": 219_000, "old_price": 259_000, "rating": 4.6, "reviews": 98, "stock": 52,
        "badge": "Phổ biến", "color": (43, 43, 43), "accent": (240, 222, 92),
        "desc": "Găng tập có đệm lòng bàn tay, tăng độ bám và hạn chế chai tay khi tập tạ, kéo xà.",
        "specs": ["Đệm lòng bàn tay", "Vải thoáng khí", "Dây cổ tay Velcro", "Size M/L/XL"],
    },
    {
        "id": "SP005", "name": "Dây Kháng Lực PowerBand Set", "category": "Dụng cụ tập",
        "price": 349_000, "old_price": 420_000, "rating": 4.8, "reviews": 151, "stock": 41,
        "badge": "Combo", "color": (53, 62, 73), "accent": (141, 255, 112),
        "desc": "Bộ 5 dây kháng lực nhiều mức tải, đi kèm tay cầm, neo cửa và túi đựng tiện lợi.",
        "specs": ["5 mức kháng lực", "Tay cầm chống trượt", "Neo cửa", "Túi đựng"],
    },
    {
        "id": "SP006", "name": "Thảm Yoga Balance 6mm", "category": "Yoga & Mobility",
        "price": 459_000, "old_price": 520_000, "rating": 4.8, "reviews": 117, "stock": 25,
        "badge": "Êm & bám", "color": (82, 56, 98), "accent": (236, 160, 255),
        "desc": "Thảm yoga 6mm chống trượt hai mặt, độ đàn hồi tốt và dễ vệ sinh sau khi tập.",
        "specs": ["Dày 6mm", "Hai mặt chống trượt", "Dễ vệ sinh", "Kèm dây mang"],
    },
    {
        "id": "SP007", "name": "Bình Nước SportFlow 1L", "category": "Găng & phụ kiện",
        "price": 189_000, "old_price": 219_000, "rating": 4.5, "reviews": 73, "stock": 68,
        "badge": "Tiện dụng", "color": (29, 74, 89), "accent": (82, 234, 255),
        "desc": "Bình nước dung tích 1 lít có vạch thời gian nhắc uống, nắp khóa chống rò rỉ.",
        "specs": ["Dung tích 1L", "BPA-free", "Nắp khóa", "Vạch nhắc uống"],
    },
    {
        "id": "SP008", "name": "Con Lăn Foam Roller Core", "category": "Yoga & Mobility",
        "price": 299_000, "old_price": 350_000, "rating": 4.7, "reviews": 91, "stock": 37,
        "badge": "Recovery", "color": (49, 55, 70), "accent": (255, 132, 159),
        "desc": "Foam roller mật độ cao hỗ trợ thả lỏng cơ, mobility và phục hồi sau buổi tập.",
        "specs": ["Dài 33cm", "EVA mật độ cao", "Bề mặt massage", "Dễ vệ sinh"],
    },
    {
        "id": "SP009", "name": "Dây Nhảy Speed Rope Pro", "category": "Dụng cụ tập",
        "price": 259_000, "old_price": 299_000, "rating": 4.7, "reviews": 109, "stock": 44,
        "badge": "Cardio", "color": (57, 45, 45), "accent": (255, 181, 71),
        "desc": "Dây nhảy tốc độ dùng vòng bi mượt, chiều dài tùy chỉnh, phù hợp cardio và boxing.",
        "specs": ["Vòng bi tốc độ", "Dây thép bọc PVC", "Tùy chỉnh chiều dài", "Tay cầm nhẹ"],
    },
    {
        "id": "SP010", "name": "Đai Lưng Tập Tạ StrongLift", "category": "Găng & phụ kiện",
        "price": 499_000, "old_price": 590_000, "rating": 4.8, "reviews": 135, "stock": 22,
        "badge": "Strength", "color": (48, 39, 34), "accent": (230, 191, 121),
        "desc": "Đai hỗ trợ thân người khi squat/deadlift nặng, bản lưng chắc và khóa kim loại bền.",
        "specs": ["Bản lưng 10cm", "Khóa kim loại", "Lót êm", "Size S–XL"],
    },
    {
        "id": "SP011", "name": "Kettlebell 12kg IronCore", "category": "Dụng cụ tập",
        "price": 749_000, "old_price": 820_000, "rating": 4.9, "reviews": 68, "stock": 14,
        "badge": "Home Gym", "color": (38, 42, 48), "accent": (217, 255, 67),
        "desc": "Kettlebell 12kg phủ sơn tĩnh điện, tay cầm rộng cho swing, goblet squat và conditioning.",
        "specs": ["Khối lượng 12kg", "Gang đúc nguyên khối", "Sơn tĩnh điện", "Đế phẳng"],
    },
    {
        "id": "SP012", "name": "Túi Gym Urban Athlete 28L", "category": "Găng & phụ kiện",
        "price": 579_000, "old_price": 650_000, "rating": 4.7, "reviews": 84, "stock": 19,
        "badge": "Lifestyle", "color": (34, 49, 57), "accent": (111, 219, 255),
        "desc": "Túi gym 28L có ngăn giày riêng, ngăn đồ ướt và nhiều khoang nhỏ cho phụ kiện cá nhân.",
        "specs": ["Dung tích 28L", "Ngăn giày riêng", "Ngăn chống ẩm", "Dây đeo tháo rời"],
    },
]

PRODUCT_INDEX = {p["id"]: p for p in PRODUCTS}
st.image("123456.jpg")

# =========================================================
# BLOG - 20 BÀI KIẾN THỨC CÓ SẴN
# =========================================================
BLOG_POSTS = [
    {
        "id": 1, "title": "Khởi động đúng cách trước khi tập: 8–10 phút có thể làm gì?",
        "category": "Nền tảng tập luyện", "read": "6 phút", "date": "12/09/2026",
        "excerpt": "Một quy trình khởi động ngắn nhưng có cấu trúc giúp cơ thể sẵn sàng hơn cho buổi tập.",
        "content": """
### Vì sao cần khởi động?
Khởi động không chỉ là làm nóng người. Mục tiêu là tăng dần nhịp tim, đưa khớp qua biên độ vận động phù hợp và tập thử chính chuyển động sắp thực hiện ở cường độ thấp.

### Quy trình 8–10 phút
1. **2–3 phút vận động nhẹ:** đi bộ nhanh, đạp xe hoặc nhảy dây nhẹ.
2. **3 phút mobility động:** xoay vai, hip opener, leg swing, ankle rock.
3. **3–4 phút bài đặc hiệu:** nếu chuẩn bị squat, hãy squat không tạ rồi tăng tải qua vài set nhẹ.

### Cần tránh
Không nên biến khởi động thành một buổi cardio dài khiến cơ thể mệt trước phần chính. Với phần lớn buổi tập sức mạnh, hãy ưu tiên chuyển động động và set làm nóng thay vì kéo giãn tĩnh quá lâu ngay trước khi nâng nặng.

> Mẹo thực hành: khởi động nên liên quan trực tiếp đến bài tập chính trong ngày.
""",
    },
    {
        "id": 2, "title": "Lịch tập sức mạnh 3 buổi/tuần cho người mới bắt đầu",
        "category": "Gym & Strength", "read": "7 phút", "date": "10/09/2026",
        "excerpt": "Mẫu lịch toàn thân đơn giản, tập trung vào kỹ thuật và khả năng duy trì lâu dài.",
        "content": """
### Mục tiêu của người mới
Trong giai đoạn đầu, ưu tiên lớn nhất là học kỹ thuật, hình thành thói quen và tăng dần khối lượng tập một cách có kiểm soát.

### Mẫu lịch
**Buổi A:** Squat 3×8, Push-up/Bench Press 3×8–10, Row 3×10, Plank 3 hiệp.  
**Buổi B:** Romanian Deadlift 3×8, Overhead Press 3×8, Lat Pulldown 3×10, Split Squat 3×8 mỗi bên.  
**Buổi C:** Leg Press 3×10, Incline Press 3×10, Seated Row 3×10, Hip Thrust 3×10.

### Tăng tiến
Khi bạn hoàn thành đủ số reps với kỹ thuật ổn trong 2–3 buổi liên tiếp, có thể tăng nhẹ mức tạ hoặc tăng 1–2 reps. Không cần tăng tải mỗi buổi nếu form bắt đầu xấu.

### Nghỉ ngơi
Chừa ít nhất một ngày nghỉ giữa các buổi toàn thân nếu cơ thể chưa quen. Giấc ngủ và dinh dưỡng có ảnh hưởng lớn đến khả năng phục hồi.
""",
    },
    {
        "id": 3, "title": "Chạy bộ cho người mới: bắt đầu thế nào để không quá sức?",
        "category": "Chạy bộ", "read": "6 phút", "date": "08/09/2026",
        "excerpt": "Bắt đầu bằng run-walk và tăng khối lượng chậm thường dễ duy trì hơn chạy liên tục ngay từ đầu.",
        "content": """
### Đừng bắt đầu bằng tốc độ
Người mới nên ưu tiên thời lượng và sự đều đặn. Một buổi 25–30 phút có thể xen kẽ 2 phút chạy nhẹ với 1 phút đi bộ.

### Nhịp độ phù hợp
Phần lớn thời gian nên ở mức bạn vẫn có thể nói được câu ngắn. Nếu thở gấp liên tục, hãy giảm tốc hoặc đi bộ.

### Tăng tải từ từ
Chỉ tăng một yếu tố chính mỗi giai đoạn: tổng thời gian, số buổi hoặc tốc độ. Việc tăng tất cả cùng lúc dễ khiến cơ thể không kịp thích nghi.

### Trang bị
Giày vừa chân, tất phù hợp và quần áo thoát ẩm thường quan trọng hơn việc mua quá nhiều phụ kiện ngay từ đầu.
""",
    },
    {
        "id": 4, "title": "Bài tập toàn thân tại nhà chỉ với dây kháng lực",
        "category": "Tập tại nhà", "read": "7 phút", "date": "05/09/2026",
        "excerpt": "Một buổi full-body gọn nhẹ dành cho ngày bận rộn hoặc khi không đến phòng gym.",
        "content": """
### Cấu trúc buổi tập
Thực hiện 3 vòng, nghỉ 45–75 giây giữa các bài tùy thể lực.

- Band Squat: 12–15 reps
- Band Row: 12–15 reps
- Chest Press: 10–15 reps
- Romanian Deadlift: 12 reps
- Shoulder Press: 10–12 reps
- Pallof Press: 10 reps mỗi bên

### Chọn mức kháng lực
Mức dây phù hợp là khi 2–3 reps cuối có thử thách nhưng bạn vẫn kiểm soát được tốc độ và biên độ.

### Cách tăng độ khó
Tăng số reps, dùng dây nặng hơn, giảm thời gian nghỉ hoặc thực hiện chuyển động chậm hơn. Không cần thay toàn bộ bài tập mỗi tuần.
""",
    },
    {
        "id": 5, "title": "Protein trong tập luyện: hiểu đơn giản để áp dụng hằng ngày",
        "category": "Dinh dưỡng", "read": "7 phút", "date": "02/09/2026",
        "excerpt": "Protein hỗ trợ xây dựng và sửa chữa mô; cách phân bổ trong ngày thường quan trọng hơn chạy theo một bữa duy nhất.",
        "content": """
### Protein làm gì?
Protein cung cấp amino acid cho nhiều quá trình của cơ thể, trong đó có việc duy trì và xây dựng mô cơ khi kết hợp với tập luyện sức mạnh.

### Nguồn thực phẩm phổ biến
Thịt nạc, cá, trứng, sữa, sữa chua, đậu hũ, đậu và các sản phẩm từ đậu đều có thể đóng góp protein.

### Cách phân bổ
Thay vì dồn phần lớn protein vào một bữa, hãy chia tương đối đều qua các bữa chính để dễ đạt nhu cầu tổng ngày và hỗ trợ cảm giác no.

### Thực tế quan trọng nhất
Tổng chế độ ăn, năng lượng, chất lượng thực phẩm, giấc ngủ và chương trình tập đều quan trọng. Không có một thực phẩm đơn lẻ nào thay thế được toàn bộ nền tảng đó.
""",
    },
    {
        "id": 6, "title": "Uống nước khi tập: cách nhận biết bạn đang uống quá ít",
        "category": "Dinh dưỡng", "read": "5 phút", "date": "30/08/2026",
        "excerpt": "Khát nhiều, nước tiểu sẫm màu và giảm hiệu suất có thể là tín hiệu cần chú ý đến thói quen bù nước.",
        "content": """
### Trước buổi tập
Bắt đầu buổi tập trong trạng thái đủ nước sẽ dễ hơn cố bù toàn bộ trong lúc tập. Hãy duy trì uống nước đều trong ngày.

### Trong buổi tập
Với buổi tập thông thường trong điều kiện mát, nước lọc thường là lựa chọn đơn giản. Buổi kéo dài, ra mồ hôi nhiều hoặc tập ngoài trời nóng có thể cần chú ý thêm điện giải.

### Sau buổi tập
Tiếp tục uống nước theo cảm giác khát và bữa ăn bình thường. Tránh ép uống lượng quá lớn trong thời gian rất ngắn.

### Một dấu hiệu thực tế
Màu nước tiểu quá sẫm kéo dài có thể gợi ý lượng nước chưa đủ, dù đây không phải công cụ chẩn đoán y khoa.
""",
    },
    {
        "id": 7, "title": "Giấc ngủ và phục hồi: vì sao tập chăm vẫn cần ngủ đủ?",
        "category": "Phục hồi", "read": "6 phút", "date": "27/08/2026",
        "excerpt": "Phục hồi tốt giúp bạn duy trì chất lượng buổi tập và khả năng tiến bộ lâu dài.",
        "content": """
### Tập luyện chỉ là một nửa quá trình
Buổi tập tạo ra kích thích; cơ thể cần thời gian và nguồn lực để thích nghi. Thiếu ngủ kéo dài thường khiến cảm giác mệt, động lực và hiệu suất tập bị ảnh hưởng.

### Xây thói quen ngủ
Giữ giờ ngủ tương đối ổn định, giảm caffeine quá muộn, hạn chế màn hình sát giờ ngủ và tạo phòng ngủ tối, mát là những bước cơ bản.

### Khi nào nên giảm tải?
Nếu nhiều buổi liên tiếp bạn thấy mức tạ quen thuộc trở nên rất nặng, nhịp tim nghỉ tăng bất thường hoặc cảm giác mệt tích lũy, một vài ngày giảm khối lượng tập có thể hợp lý.
""",
    },
    {
        "id": 8, "title": "Cách chọn giày chạy bộ theo nhu cầu thay vì theo quảng cáo",
        "category": "Chạy bộ", "read": "7 phút", "date": "24/08/2026",
        "excerpt": "Độ vừa chân, mục đích sử dụng và cảm giác khi chạy nên được ưu tiên hơn một thông số đơn lẻ.",
        "content": """
### Bắt đầu từ mục đích
Bạn chạy hằng ngày, chạy tempo, chạy trail hay dùng giày cho cả đi bộ? Mỗi nhu cầu có thể ưu tiên khác nhau về đệm, trọng lượng và độ bám.

### Độ vừa chân
Ngón chân cần khoảng trống hợp lý, gót không trượt quá nhiều và upper không ép gây tê. Nên thử giày vào thời điểm chân đã vận động trong ngày.

### Đừng quá phụ thuộc một con số
Drop, stack height hay trọng lượng đều có giá trị tham khảo nhưng không thể thay thế cảm giác vừa chân và sự phù hợp với cách bạn sử dụng.
""",
    },
    {
        "id": 9, "title": "Găng tay gym có cần thiết không? Khi nào nên dùng?",
        "category": "Trang bị", "read": "5 phút", "date": "21/08/2026",
        "excerpt": "Găng tay không bắt buộc, nhưng có thể hữu ích khi bạn muốn tăng độ bám hoặc giảm ma sát lòng bàn tay.",
        "content": """
### Lợi ích chính
Găng tập có thể giảm cảm giác cọ xát, hỗ trợ độ bám khi tay nhiều mồ hôi và tạo cảm giác thoải mái hơn với một số người.

### Điểm cần lưu ý
Găng quá dày có thể làm cảm giác cầm thanh tạ kém tự nhiên. Hãy chọn đúng size, vật liệu thoáng và phần đệm vừa đủ.

### Không thay thế kỹ thuật
Nếu bạn liên tục mất grip vì mức tạ vượt khả năng kiểm soát, phụ kiện không nên là cách duy nhất để khắc phục. Hãy xem lại kỹ thuật và mức tải.
""",
    },
    {
        "id": 10, "title": "Dây kháng lực: 5 cách dùng hiệu quả ngoài việc khởi động",
        "category": "Tập tại nhà", "read": "6 phút", "date": "18/08/2026",
        "excerpt": "Dây kháng lực có thể dùng cho tập sức mạnh, hỗ trợ kỹ thuật và thêm kháng lực vào nhiều bài quen thuộc.",
        "content": """
### 5 ứng dụng dễ dùng
1. Row cho lưng và tay trước.  
2. Pallof Press để tập chống xoay thân người.  
3. Lateral Walk cho nhóm cơ quanh hông.  
4. Assisted Pull-up để giảm tải khi kéo xà.  
5. Band-resisted Squat/Press để thay đổi đường kháng lực.

### Ưu điểm
Nhẹ, gọn, dễ mang theo và phù hợp cho home gym. Nhược điểm là khó định lượng lực chính xác như tạ máy hoặc tạ tự do.
""",
    },
    {
        "id": 11, "title": "HIIT và cardio cường độ thấp: chọn kiểu nào cho mục tiêu của bạn?",
        "category": "Cardio", "read": "7 phút", "date": "15/08/2026",
        "excerpt": "Không cần chọn một bỏ một; hai hình thức có thể phục vụ những mục tiêu và thời điểm khác nhau.",
        "content": """
### HIIT
Các quãng cường độ cao xen kẽ nghỉ thường tiết kiệm thời gian nhưng gây mệt nhiều hơn và đòi hỏi nền tảng kỹ thuật tốt ở bài vận động được chọn.

### Cardio cường độ thấp
Đi bộ nhanh, đạp xe nhẹ hoặc chạy rất nhẹ dễ phục hồi hơn và có thể tích lũy thời lượng lớn.

### Cách kết hợp
Nếu bạn ưu tiên sức mạnh, có thể dùng cardio nhẹ thường xuyên và chỉ thêm 1–2 buổi interval ngắn tùy khả năng phục hồi. Tổng tải của cả tuần quan trọng hơn việc chạy theo một phương pháp duy nhất.
""",
    },
    {
        "id": 12, "title": "Squat cơ bản: 6 lỗi thường gặp và cách tự kiểm tra",
        "category": "Gym & Strength", "read": "8 phút", "date": "12/08/2026",
        "excerpt": "Tự quay video ở góc phù hợp là cách đơn giản để nhận biết một số lỗi kỹ thuật phổ biến.",
        "content": """
### Những điểm thường gặp
- Gót chân nhấc khỏi sàn.
- Gối mất kiểm soát hướng.
- Thân người đổ quá mức so với kiểu squat đang thực hiện.
- Mất căng thân người ở đáy động tác.
- Xuống sâu hơn khả năng mobility đang có.
- Tăng tạ quá sớm.

### Cách kiểm tra
Quay video từ góc chéo trước hoặc ngang, dùng mức tạ nhẹ và so sánh qua nhiều reps. Kỹ thuật có thể khác đôi chút giữa từng người do tỷ lệ cơ thể và mục tiêu tập.
""",
    },
    {
        "id": 13, "title": "Push-up từ số 0: lộ trình để tăng số lần chống đẩy",
        "category": "Gym & Strength", "read": "6 phút", "date": "09/08/2026",
        "excerpt": "Điều chỉnh độ cao tay chống giúp bạn luyện đúng chuyển động trước khi tiến tới chống đẩy sàn.",
        "content": """
### Bắt đầu ở biến thể vừa sức
Nếu chống đẩy sàn quá khó, hãy đặt tay lên bàn hoặc ghế chắc chắn. Chọn độ cao cho phép thực hiện 6–12 reps kiểm soát.

### Kỹ thuật cơ bản
Giữ thân người tương đối thẳng, tay đặt ổn định, vai không nhô sát tai và hạ ngực có kiểm soát.

### Tăng tiến
Khi đạt 3 hiệp x 12–15 reps dễ dàng, hạ dần độ cao tay chống. Tập 2–3 lần/tuần thường đủ để luyện kỹ năng mà không cần tập tới thất bại mỗi ngày.
""",
    },
    {
        "id": 14, "title": "Deadlift an toàn hơn: cách setup trước khi kéo",
        "category": "Gym & Strength", "read": "7 phút", "date": "06/08/2026",
        "excerpt": "Một setup lặp lại ổn định giúp bạn kiểm soát chuyển động tốt hơn khi mức tạ tăng.",
        "content": """
### Trình tự setup gợi ý
1. Đặt bàn chân ổn định và thanh tạ gần giữa bàn chân.
2. Gập hông để nắm thanh.
3. Tạo căng phần lưng trên và thân người.
4. Đưa cẳng chân tiến gần thanh mà không đẩy thanh đi xa.
5. Đạp sàn và giữ thanh đi gần cơ thể.

### Không cần vội tăng tải
Deadlift là bài có thể dùng mức tạ lớn nên sai số nhỏ khi tải cao cũng trở nên đáng kể. Hãy tăng từ từ và dừng set nếu kỹ thuật xuống rõ rệt.
""",
    },
    {
        "id": 15, "title": "Mobility và stretching khác nhau thế nào?",
        "category": "Phục hồi", "read": "5 phút", "date": "03/08/2026",
        "excerpt": "Mobility thường nhấn mạnh khả năng chủ động kiểm soát biên độ, trong khi stretching chỉ là một phần của câu chuyện.",
        "content": """
### Stretching
Kéo giãn có thể là động hoặc tĩnh, thường tập trung vào cảm giác kéo căng của mô trong một tư thế hoặc chuyển động.

### Mobility
Mobility liên quan đến việc tạo và kiểm soát chuyển động tại khớp trong biên độ cần thiết cho hoạt động cụ thể.

### Áp dụng
Nếu squat bị hạn chế, chỉ kéo giãn chưa chắc giải quyết toàn bộ vấn đề. Bạn có thể cần bài ankle mobility, kiểm soát hông và thực hành squat ở mức tải phù hợp.
""",
    },
    {
        "id": 16, "title": "Túi tập gym nên có gì? Checklist tối giản cho người bận rộn",
        "category": "Trang bị", "read": "4 phút", "date": "31/07/2026",
        "excerpt": "Mang đủ đồ cần thiết nhưng không biến túi tập thành kho chứa đồ là mục tiêu thực tế nhất.",
        "content": """
### Bộ cơ bản
Quần áo tập, giày, bình nước, khăn nhỏ, khóa tủ nếu phòng gym yêu cầu và đồ vệ sinh cá nhân là đủ cho đa số buổi tập.

### Phụ kiện tùy mục tiêu
Găng tay, straps, belt, dây kháng lực hoặc tai nghe chỉ nên mang khi bạn thực sự dùng chúng trong chương trình.

### Tổ chức túi
Ngăn giày và ngăn đồ ướt giúp hạn chế mùi. Sau buổi tập, lấy quần áo ẩm ra càng sớm càng tốt thay vì để qua đêm trong túi.
""",
    },
    {
        "id": 17, "title": "Cách lập kế hoạch tập một tuần để dễ duy trì hơn",
        "category": "Nền tảng tập luyện", "read": "7 phút", "date": "28/07/2026",
        "excerpt": "Một lịch tập tốt cần khớp với thời gian và mức phục hồi thật của bạn, không chỉ đẹp trên giấy.",
        "content": """
### Bước 1: chốt số buổi thực tế
Nếu lịch làm việc chỉ cho phép 3 buổi, hãy xây lịch 3 buổi tốt thay vì cố theo lịch 6 buổi rồi bỏ dở.

### Bước 2: xác định ưu tiên
Sức mạnh, tăng cơ, chạy bộ hay sức khỏe tổng thể sẽ ảnh hưởng cách phân phối bài tập.

### Bước 3: đặt ngày nghỉ chiến lược
Tránh dồn quá nhiều buổi nặng liên tiếp nếu bạn phục hồi kém. Có thể xen kẽ ngày sức mạnh với cardio nhẹ hoặc mobility.

### Bước 4: theo dõi 4–6 tuần
Chỉ thay chương trình khi có lý do rõ ràng. Quá nhiều thay đổi làm khó đánh giá thứ gì thật sự hiệu quả.
""",
    },
    {
        "id": 18, "title": "Tập mãi không tiến bộ: 7 câu hỏi nên kiểm tra trước khi đổi giáo án",
        "category": "Nền tảng tập luyện", "read": "7 phút", "date": "25/07/2026",
        "excerpt": "Plateau đôi khi đến từ phục hồi, kỹ thuật hoặc việc theo dõi kém chứ không phải thiếu bài tập mới.",
        "content": """
### 7 câu hỏi nhanh
1. Bạn có ghi lại mức tạ và reps không?  
2. Kỹ thuật có ổn định khi tăng tải không?  
3. Bạn có ngủ đủ trong phần lớn tuần không?  
4. Tổng năng lượng và protein có phù hợp mục tiêu không?  
5. Có tập quá nhiều set đến thất bại không?  
6. Bạn đã duy trì chương trình đủ lâu chưa?  
7. Có dấu hiệu đau hoặc mệt kéo dài cần giảm tải không?

Trả lời các câu hỏi này trước khi thay toàn bộ giáo án giúp bạn tránh đổi chương trình chỉ vì vài buổi tập không tốt.
""",
    },
    {
        "id": 19, "title": "Cân bằng năng lượng: nền tảng để hiểu tăng cân và giảm cân",
        "category": "Dinh dưỡng", "read": "7 phút", "date": "22/07/2026",
        "excerpt": "Thay đổi cân nặng dài hạn liên quan đến cân bằng giữa năng lượng nạp vào và năng lượng tiêu hao.",
        "content": """
### Khái niệm đơn giản
Khi năng lượng nạp vào thường xuyên thấp hơn năng lượng tiêu hao, cân nặng có xu hướng giảm theo thời gian; chiều ngược lại thường dẫn tới tăng cân.

### Nhưng cơ thể không phải máy tính đơn giản
Mức vận động, cảm giác đói, khối lượng cơ thể và nhiều yếu tố hành vi có thể thay đổi khi bạn ăn ít hoặc nhiều hơn.

### Cách tiếp cận thực tế
Theo dõi xu hướng cân nặng nhiều tuần thay vì phản ứng với từng ngày. Ưu tiên thực phẩm giàu dinh dưỡng, đủ protein, rau quả, giấc ngủ và vận động phù hợp.
""",
    },
    {
        "id": 20, "title": "Đau khi tập: khi nào nên dừng lại và tìm hỗ trợ chuyên môn?",
        "category": "Phục hồi", "read": "6 phút", "date": "19/07/2026",
        "excerpt": "Phân biệt cảm giác gắng sức bình thường với cơn đau bất thường là kỹ năng quan trọng để tập bền vững.",
        "content": """
### Đau không phải lúc nào cũng là dấu hiệu “tập hiệu quả”
Cảm giác căng cơ hoặc mỏi sau tập có thể xảy ra, nhưng đau sắc, đau tăng dần, sưng rõ hoặc mất chức năng không nên bị xem nhẹ.

### Nên dừng bài tập khi
Cơn đau đột ngột xuất hiện, bạn mất khả năng chịu lực bình thường, có cảm giác tê/yếu bất thường hoặc chấn thương do va chạm mạnh.

### Khi cần hỗ trợ
Nếu triệu chứng kéo dài, tái phát hoặc ảnh hưởng sinh hoạt, hãy tìm chuyên gia y tế có chuyên môn phù hợp để được đánh giá trực tiếp. Nội dung trên blog chỉ mang tính giáo dục, không thay thế chẩn đoán cá nhân.
""",
    },
]

# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def money(value: int) -> str:
    return f"{int(value):,}".replace(",", ".") + " ₫"


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text)


def hex_color(rgb):
    return "#" + "".join(f"{c:02x}" for c in rgb)


def load_font(size=30):
    candidates = [
        APP_DIR / "DejaVuSans-Bold.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_product_image(product: Dict) -> Path:
    path = ASSET_DIR / f"{product['id']}.png"
    if path.exists():
        return path

    w, h = 1100, 760
    bg = product["color"]
    accent = product["accent"]
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)

    # Gradient dọc đơn giản
    for y in range(h):
        ratio = y / h
        col = tuple(int(bg[i] * (1 - 0.24 * ratio) + 16 * (0.24 * ratio)) for i in range(3))
        d.line([(0, y), (w, y)], fill=col)

    # Hình khối trang trí
    d.ellipse((720, -140, 1240, 380), fill=accent)
    d.ellipse((-120, 540, 360, 1020), outline=accent, width=28)
    d.rounded_rectangle((55, 55, 235, 105), radius=25, fill=(245, 247, 250))
    d.text((86, 71), product["id"], fill=(20, 22, 27), font=load_font(25))

    # Minh họa theo danh mục
    cx, cy = 550, 360
    icon = (245, 247, 250)
    cat = product["category"]
    if cat == "Quần áo":
        # Áo thể thao cách điệu
        pts = [(420, 230), (495, 190), (605, 190), (680, 230), (640, 315), (610, 290), (610, 535), (490, 535), (490, 290), (460, 315)]
        d.polygon(pts, fill=icon)
        d.ellipse((515, 185, 585, 245), fill=bg)
        d.line((545, 260, 545, 505), fill=accent, width=16)
    elif cat == "Giày thể thao":
        pts = [(330, 435), (475, 430), (560, 365), (625, 395), (670, 445), (815, 470), (830, 520), (400, 520), (340, 495)]
        d.polygon(pts, fill=icon)
        d.line((415, 470, 735, 470), fill=accent, width=14)
        for x in [535, 575, 615]:
            d.line((x, 405, x+45, 435), fill=bg, width=9)
    elif cat == "Dụng cụ tập":
        # Dumbbell
        d.rounded_rectangle((365, 325, 735, 390), radius=28, fill=icon)
        d.rounded_rectangle((305, 265, 390, 455), radius=20, fill=icon)
        d.rounded_rectangle((710, 265, 795, 455), radius=20, fill=icon)
        d.rounded_rectangle((260, 295, 325, 425), radius=18, fill=accent)
        d.rounded_rectangle((775, 295, 840, 425), radius=18, fill=accent)
    elif cat == "Yoga & Mobility":
        d.rounded_rectangle((330, 435, 780, 515), radius=38, fill=icon)
        d.ellipse((680, 405, 805, 540), fill=accent)
        d.arc((390, 220, 710, 500), 195, 345, fill=icon, width=35)
    else:
        # Găng / phụ kiện: shield + grip
        shield = [(550, 190), (735, 255), (705, 455), (550, 560), (395, 455), (365, 255)]
        d.polygon(shield, fill=icon)
        d.ellipse((475, 300, 625, 450), outline=accent, width=30)
        d.line((505, 375, 590, 375), fill=accent, width=22)

    # Nhãn danh mục
    d.rounded_rectangle((55, 625, 470, 695), radius=22, fill=(245, 247, 250))
    label = normalize_text(cat).upper()[:25]
    d.text((82, 644), label, fill=(20, 22, 27), font=load_font(25))

    img.save(path, quality=92)
    return path


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                subtotal INTEGER NOT NULL,
                discount INTEGER NOT NULL,
                shipping INTEGER NOT NULL,
                total INTEGER NOT NULL,
                items_json TEXT NOT NULL,
                note TEXT
            )
            """
        )
        conn.commit()


def save_order(order: Dict):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO orders (
                order_id, created_at, customer_name, phone, email, address, city,
                payment_method, subtotal, discount, shipping, total, items_json, note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order["order_id"], order["created_at"], order["customer_name"], order["phone"],
                order["email"], order["address"], order["city"], order["payment_method"],
                order["subtotal"], order["discount"], order["shipping"], order["total"],
                json.dumps(order["items"], ensure_ascii=False), order["note"],
            ),
        )
        conn.commit()


def load_orders(order_ids: List[str]) -> List[Dict]:
    if not order_ids:
        return []
    placeholders = ",".join("?" for _ in order_ids)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"SELECT * FROM orders WHERE order_id IN ({placeholders}) ORDER BY created_at DESC",
            tuple(order_ids),
        ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["items"] = json.loads(item.pop("items_json"))
        result.append(item)
    return result


def init_state():
    defaults = {
        "cart": {},
        "wishlist": [],
        "coupon": "",
        "chat_history": [
            {
                "role": "assistant",
                "content": "Xin chào! Mình là **SportBot**. Bạn có thể hỏi mình về sản phẩm, ngân sách, giao hàng, thanh toán, đổi trả hoặc kiến thức tập luyện.",
            }
        ],
        "order_ids": [],
        "last_order": None,
        "shop_search": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_to_cart(product_id: str, qty: int = 1):
    current = st.session_state.cart.get(product_id, 0)
    stock = PRODUCT_INDEX[product_id]["stock"]
    st.session_state.cart[product_id] = min(current + qty, stock)
    st.toast("Đã thêm sản phẩm vào giỏ hàng", icon="🛒")


def cart_count() -> int:
    return sum(st.session_state.cart.values())


def cart_totals():
    subtotal = sum(PRODUCT_INDEX[pid]["price"] * qty for pid, qty in st.session_state.cart.items())
    coupon = st.session_state.coupon.strip().upper()
    discount = min(int(subtotal * 0.10), 100_000) if coupon == "SPORT10" else 0
    shipping = 0 if subtotal >= FREE_SHIP_THRESHOLD else DEFAULT_SHIPPING
    if coupon == "FREESHIP":
        shipping = 0
    total = max(0, subtotal - discount + shipping)
    return subtotal, discount, shipping, total


def parse_budget(query: str):
    q = normalize_text(query)
    patterns = [
        r"(\d+(?:[\.,]\d+)?)\s*(trieu|tr)",
        r"(\d+(?:[\.,]\d+)?)\s*k",
        r"(\d{5,9})\s*(?:d|dong)?",
    ]
    for i, pat in enumerate(patterns):
        m = re.search(pat, q)
        if m:
            num = float(m.group(1).replace(",", "."))
            if i == 0:
                return int(num * 1_000_000)
            if i == 1:
                return int(num * 1_000)
            return int(num)
    return None


def product_recommendations(query: str) -> List[Dict]:
    q = normalize_text(query)
    budget = parse_budget(query)
    mapping = {
        "giay": "Giày thể thao",
        "chay": "Giày thể thao",
        "ao": "Quần áo",
        "quan": "Quần áo",
        "gang": "Găng & phụ kiện",
        "phu kien": "Găng & phụ kiện",
        "day": "Dụng cụ tập",
        "ta": "Dụng cụ tập",
        "home gym": "Dụng cụ tập",
        "yoga": "Yoga & Mobility",
        "mobility": "Yoga & Mobility",
    }
    category = None
    for key, cat in mapping.items():
        if key in q:
            category = cat
            break

    items = PRODUCTS
    if category:
        items = [p for p in items if p["category"] == category]
    if budget:
        items = [p for p in items if p["price"] <= budget]
    items = sorted(items, key=lambda p: (-p["rating"], p["price"]))
    return items[:3]


def answer_chat(query: str) -> str:
    q = normalize_text(query)
    if not q:
        return "Bạn cứ nhập câu hỏi, mình sẽ hỗ trợ nhé."

    if any(x in q for x in ["xin chao", "hello", "hi ", "chao ban", "alo"]):
        return "Chào bạn 👋 Mình có thể gợi ý sản phẩm theo **mục tiêu + ngân sách**, giải đáp chính sách mua hàng hoặc tìm bài Blog phù hợp."

    if any(x in q for x in ["giao hang", "ship", "van chuyen", "phi ship"]):
        return (
            f"Phí giao hàng mặc định trong bản demo là **{money(DEFAULT_SHIPPING)}**. "
            f"Đơn từ **{money(FREE_SHIP_THRESHOLD)}** được miễn phí giao hàng. Bạn cũng có thể thử mã **FREESHIP** ở giỏ hàng."
        )

    if any(x in q for x in ["thanh toan", "cod", "chuyen khoan", "the"]):
        return (
            "App hiện hỗ trợ 3 lựa chọn ở bước checkout: **COD**, **chuyển khoản (demo)** và **thẻ (demo)**. "
            "Để đưa lên production, bạn nên kết nối cổng thanh toán thật như VNPay/MoMo/ZaloPay hoặc Stripe tùy thị trường."
        )

    if any(x in q for x in ["doi tra", "hoan hang", "bao hanh", "doi size"]):
        return (
            "Chính sách mẫu của PULSE SPORT: hỗ trợ yêu cầu đổi size/đổi sản phẩm trong **7 ngày** nếu sản phẩm còn nguyên tình trạng phù hợp. "
            "Khi triển khai thật, bạn nên thay nội dung này bằng chính sách pháp lý và vận hành chính thức của cửa hàng."
        )

    if any(x in q for x in ["ma giam", "coupon", "khuyen mai", "giam gia"]):
        return "Bạn có thể thử **SPORT10** (giảm 10%, tối đa 100.000 ₫) hoặc **FREESHIP** trong trang Giỏ hàng."

    # Tìm trực tiếp theo tên sản phẩm
    for p in PRODUCTS:
        tokens = [t for t in normalize_text(p["name"]).split() if len(t) >= 4]
        if len(tokens) >= 2 and sum(t in q for t in tokens) >= 2:
            return (
                f"**{p['name']}** hiện có giá **{money(p['price'])}**, đánh giá **{p['rating']}/5** từ {p['reviews']} lượt. "
                f"{p['desc']} Kho còn **{p['stock']}** sản phẩm trong dữ liệu demo."
            )

    if any(x in q for x in ["goi y", "nen mua", "tu van", "ngan sach", "tim san pham", "mua gi"]):
        recs = product_recommendations(query)
        if recs:
            lines = ["Mình gợi ý các lựa chọn sau:"]
            for p in recs:
                lines.append(f"- **{p['name']}** — {money(p['price'])} — ⭐ {p['rating']}/5")
            lines.append("Bạn có thể nói rõ môn tập, mức ngân sách và ưu tiên của bạn để mình lọc sát hơn.")
            return "\n".join(lines)
        return "Mình chưa thấy sản phẩm phù hợp đúng ngân sách đó. Bạn thử tăng ngân sách hoặc nói rõ nhóm sản phẩm nhé."

    if any(x in q for x in ["blog", "bai viet", "kien thuc", "huong dan"]):
        scored = []
        q_words = set(q.split())
        for post in BLOG_POSTS:
            hay = normalize_text(post["title"] + " " + post["category"] + " " + post["excerpt"])
            score = sum(1 for w in q_words if len(w) > 3 and w in hay)
            scored.append((score, post))
        best = [p for s, p in sorted(scored, key=lambda x: -x[0]) if s > 0][:3]
        if not best:
            best = BLOG_POSTS[:3]
        return "Bạn có thể xem các bài: \n" + "\n".join(f"- **{p['title']}**" for p in best)

    # Các intent thể thao phổ biến
    if "khoi dong" in q:
        return "Bạn vào Blog và tìm bài **“Khởi động đúng cách trước khi tập: 8–10 phút có thể làm gì?”**. Bài có quy trình cardio nhẹ → mobility động → set đặc hiệu."
    if "protein" in q:
        return "Blog có bài **“Protein trong tập luyện: hiểu đơn giản để áp dụng hằng ngày”**. Nội dung tập trung vào vai trò, nguồn thực phẩm và cách phân bổ protein trong ngày."
    if "squat" in q:
        return "Bạn xem bài **“Squat cơ bản: 6 lỗi thường gặp và cách tự kiểm tra”** trong Blog. Nếu bạn đang đau khi squat, nên giảm tải và cân nhắc được đánh giá trực tiếp bởi người có chuyên môn."

    return (
        "Mình chưa chắc bạn đang hỏi theo hướng nào. Bạn có thể thử: **“gợi ý giày chạy dưới 1,5 triệu”**, "
        "**“phí ship bao nhiêu?”**, **“mã giảm giá”**, **“tìm bài blog về squat”** hoặc nhập đúng tên sản phẩm."
    )

# =========================================================
# COMPONENTS
# =========================================================
def sidebar():
    with st.sidebar:
        st.markdown("## 🏃 PULSE SPORT")
        st.caption("SHOP • TRAIN • RECOVER")
        st.divider()
        page = st.radio(
            "Điều hướng",
            ["Trang chủ", "Cửa hàng", "Blog thể thao", f"Giỏ hàng ({cart_count()})", "SportBot", "Đơn hàng của tôi"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**Ưu đãi demo**")
        st.code("SPORT10", language=None)
        st.caption("Giảm 10% • tối đa 100.000 ₫")
        st.code("FREESHIP", language=None)
        st.caption("Miễn phí giao hàng")
        st.divider()
        st.caption("📞 CSKH: 1900 0000 (demo)")
        st.caption("✉️ hello@pulsesport.local")
    return page


def render_product_card(product: Dict, key_prefix="shop"):
    image_path = generate_product_image(product)
    st.image(str(image_path), use_container_width=True)
    left, right = st.columns([4, 1])
    with left:
        st.markdown(f"**{product['name']}**")
    with right:
        if st.button("♡", key=f"wish_{key_prefix}_{product['id']}", help="Thêm/bỏ yêu thích", use_container_width=True):
            if product["id"] in st.session_state.wishlist:
                st.session_state.wishlist.remove(product["id"])
            else:
                st.session_state.wishlist.append(product["id"])
            st.rerun()

    st.markdown(
        f"<span class='sale-pill'>{product['badge']}</span> "
        f"<span class='rating'>⭐ {product['rating']} ({product['reviews']})</span>",
        unsafe_allow_html=True,
    )
    discount_pct = round((1 - product["price"] / product["old_price"]) * 100)
    st.markdown(
        f"<span class='price'>{money(product['price'])}</span> &nbsp; "
        f"<span class='old-price'>{money(product['old_price'])}</span> &nbsp; "
        f"<span class='muted'>-{discount_pct}%</span>",
        unsafe_allow_html=True,
    )
    st.caption(product["desc"])
    with st.expander("Thông tin sản phẩm"):
        for item in product["specs"]:
            st.markdown(f"- {item}")
        st.caption(f"Tồn kho demo: {product['stock']} sản phẩm")
    if st.button("Thêm vào giỏ", key=f"add_{key_prefix}_{product['id']}", type="primary", use_container_width=True):
        add_to_cart(product["id"], 1)


def render_footer():
    st.markdown(
        """
        <div class="footer">
        <b>PULSE SPORT</b> — Demo e-commerce & sports knowledge app built with Streamlit.<br>
        Dữ liệu giá, tồn kho, đánh giá, chính sách và thanh toán hiện là dữ liệu minh họa để phát triển sản phẩm.
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PAGES
# =========================================================
def page_home():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">MOVE BETTER • TRAIN SMARTER</div>
            <h1>Trang bị tốt hơn.<br>Tập luyện thông minh hơn.</h1>
            <p>PULSE SPORT kết hợp cửa hàng đồ thể thao, kiến thức tập luyện và trợ lý tư vấn tự động trong cùng một ứng dụng.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sản phẩm", len(PRODUCTS), "6 nhóm")
    c2.metric("Bài kiến thức", len(BLOG_POSTS), "Có sẵn")
    c3.metric("Miễn phí ship từ", "700K")
    c4.metric("Đánh giá TB", f"{sum(p['rating'] for p in PRODUCTS)/len(PRODUCTS):.1f}/5")

    st.markdown("### Danh mục nổi bật", help="Các nhóm sản phẩm chính trong dữ liệu demo")
    cats = [
        ("👕", "Quần áo", "Dry-fit, short 2-in-1 và trang phục vận động"),
        ("👟", "Giày thể thao", "Giày chạy hằng ngày và tập luyện"),
        ("🏋️", "Dụng cụ tập", "Dây kháng lực, kettlebell, dây nhảy"),
        ("🧘", "Yoga & Mobility", "Thảm tập và dụng cụ phục hồi"),
    ]
    cols = st.columns(4)
    for col, (icon, title, text) in zip(cols, cats):
        with col:
            st.markdown(f"<div class='feature'><h3>{icon} {title}</h3><p class='muted'>{text}</p></div>", unsafe_allow_html=True)

    st.markdown("### Sản phẩm được quan tâm")
    featured = sorted(PRODUCTS, key=lambda p: (-p["rating"], -p["reviews"]))[:3]
    cols = st.columns(3)
    for col, p in zip(cols, featured):
        with col:
            with st.container(border=True):
                render_product_card(p, key_prefix="home")

    st.markdown("### Vì sao app này thực tế hơn một landing page bán hàng?")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("<div class='feature'><h3>🛒 Luồng mua hàng</h3><p class='muted'>Tìm kiếm → chọn sản phẩm → giỏ hàng → mã giảm giá → checkout → lưu đơn SQLite.</p></div>", unsafe_allow_html=True)
    with f2:
        st.markdown("<div class='feature'><h3>📚 Content Hub</h3><p class='muted'>20 bài viết nền tảng về gym, chạy bộ, dinh dưỡng, phục hồi và trang bị.</p></div>", unsafe_allow_html=True)
    with f3:
        st.markdown("<div class='feature'><h3>🤖 SportBot</h3><p class='muted'>Chat tự động offline, tư vấn theo từ khóa, sản phẩm và ngân sách mà không cần API.</p></div>", unsafe_allow_html=True)


def page_shop():
    st.title("Cửa hàng thể thao")
    st.caption("Tìm sản phẩm theo nhu cầu, ngân sách, mức đánh giá và danh mục.")

    search = st.text_input("Tìm kiếm", value=st.session_state.shop_search, placeholder="Ví dụ: giày chạy, găng tay, dây kháng lực...")
    st.session_state.shop_search = search

    categories = sorted(set(p["category"] for p in PRODUCTS))
    f1, f2, f3 = st.columns([1.5, 1.2, 1])
    with f1:
        selected_categories = st.multiselect("Danh mục", categories, default=[])
    with f2:
        max_price = max(p["price"] for p in PRODUCTS)
        price_range = st.slider("Khoảng giá", 0, max_price, (0, max_price), step=50_000, format="%d ₫")
    with f3:
        min_rating = st.selectbox("Đánh giá từ", [0, 4.5, 4.7, 4.8, 4.9], index=0)

    sort = st.selectbox("Sắp xếp", ["Nổi bật", "Giá tăng dần", "Giá giảm dần", "Đánh giá cao"])

    q = normalize_text(search)
    filtered = []
    for p in PRODUCTS:
        searchable = normalize_text(p["name"] + " " + p["category"] + " " + p["desc"] + " " + " ".join(p["specs"]))
        if q and q not in searchable:
            continue
        if selected_categories and p["category"] not in selected_categories:
            continue
        if not (price_range[0] <= p["price"] <= price_range[1]):
            continue
        if p["rating"] < min_rating:
            continue
        filtered.append(p)

    if sort == "Giá tăng dần":
        filtered.sort(key=lambda p: p["price"])
    elif sort == "Giá giảm dần":
        filtered.sort(key=lambda p: -p["price"])
    elif sort == "Đánh giá cao":
        filtered.sort(key=lambda p: (-p["rating"], -p["reviews"]))
    else:
        filtered.sort(key=lambda p: (-p["reviews"], -p["rating"]))

    st.markdown(f"**{len(filtered)} sản phẩm phù hợp**")
    if not filtered:
        st.info("Không tìm thấy sản phẩm phù hợp bộ lọc hiện tại.")
        return

    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, p in zip(cols, filtered[i:i+3]):
            with col:
                with st.container(border=True):
                    render_product_card(p, key_prefix=f"shop{i}")


def page_cart():
    st.title("Giỏ hàng & Thanh toán")

    if st.session_state.last_order:
        order = st.session_state.last_order
        st.success(f"🎉 Bạn đã đặt hàng thành công! Mã đơn: {order['order_id']}")
        st.markdown(
            f"<div class='notice'>Tổng thanh toán: <b>{money(order['total'])}</b> • Phương thức: <b>{order['payment_method']}</b></div>",
            unsafe_allow_html=True,
        )
        if st.button("Ẩn thông báo đơn vừa đặt"):
            st.session_state.last_order = None
            st.rerun()

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Hãy vào **Cửa hàng** để thêm sản phẩm.")
        return

    left, right = st.columns([1.55, 1])
    with left:
        st.subheader("Sản phẩm trong giỏ")
        remove_ids = []
        for pid, qty in list(st.session_state.cart.items()):
            p = PRODUCT_INDEX[pid]
            with st.container(border=True):
                c1, c2, c3 = st.columns([1.1, 2.2, 1])
                with c1:
                    st.image(str(generate_product_image(p)), use_container_width=True)
                with c2:
                    st.markdown(f"**{p['name']}**")
                    st.caption(p["category"])
                    st.markdown(f"**{money(p['price'])}** / sản phẩm")
                with c3:
                    new_qty = st.number_input(
                        "Số lượng", min_value=1, max_value=p["stock"], value=qty, step=1,
                        key=f"qty_{pid}",
                    )
                    if new_qty != qty:
                        st.session_state.cart[pid] = int(new_qty)
                    if st.button("Xóa", key=f"remove_{pid}", use_container_width=True):
                        remove_ids.append(pid)
        for pid in remove_ids:
            st.session_state.cart.pop(pid, None)
            st.rerun()

        st.subheader("Mã ưu đãi")
        coupon = st.text_input("Coupon", value=st.session_state.coupon, placeholder="SPORT10 hoặc FREESHIP")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Áp dụng mã", use_container_width=True):
                code = coupon.strip().upper()
                if code in ["SPORT10", "FREESHIP"]:
                    st.session_state.coupon = code
                    st.success(f"Đã áp dụng mã {code}")
                    st.rerun()
                else:
                    st.warning("Mã không hợp lệ trong bản demo.")
        with c2:
            if st.button("Bỏ mã", use_container_width=True):
                st.session_state.coupon = ""
                st.rerun()

        if st.session_state.coupon:
            st.caption(f"Mã đang dùng: {st.session_state.coupon}")

    with right:
        subtotal, discount, shipping, total = cart_totals()
        with st.container(border=True):
            st.subheader("Tóm tắt đơn hàng")
            st.write(f"Tạm tính: **{money(subtotal)}**")
            st.write(f"Giảm giá: **-{money(discount)}**")
            st.write(f"Phí giao hàng: **{money(shipping)}**")
            st.divider()
            st.markdown(f"### Tổng cộng: {money(total)}")
            if subtotal < FREE_SHIP_THRESHOLD and shipping > 0:
                st.caption(f"Mua thêm {money(FREE_SHIP_THRESHOLD - subtotal)} để đạt ngưỡng freeship.")

        st.subheader("Thông tin nhận hàng")
        with st.form("checkout_form", clear_on_submit=False):
            name = st.text_input("Họ và tên *", placeholder="Nguyễn Văn A")
            phone = st.text_input("Số điện thoại *", placeholder="09xxxxxxxx")
            email = st.text_input("Email", placeholder="ban@example.com")
            city = st.selectbox(
                "Tỉnh/Thành phố *",
                ["TP. Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Cần Thơ", "Hải Phòng", "Bình Dương", "Đồng Nai", "Khác"],
            )
            address = st.text_area("Địa chỉ nhận hàng *", placeholder="Số nhà, đường, phường/xã, quận/huyện")
            payment = st.radio("Phương thức thanh toán", ["COD", "Chuyển khoản (demo)", "Thẻ (demo)"])
            note = st.text_area("Ghi chú cho đơn hàng", placeholder="Ví dụ: giao giờ hành chính")
            agree = st.checkbox("Tôi xác nhận thông tin đặt hàng là chính xác.")
            submitted = st.form_submit_button("Đặt hàng", type="primary", use_container_width=True)

        if submitted:
            clean_phone = re.sub(r"\D", "", phone)
            errors = []
            if len(name.strip()) < 2:
                errors.append("Vui lòng nhập họ tên hợp lệ.")
            if not (9 <= len(clean_phone) <= 11):
                errors.append("Số điện thoại cần có khoảng 9–11 chữ số.")
            if email.strip() and ("@" not in email or "." not in email.split("@")[-1]):
                errors.append("Email chưa đúng định dạng.")
            if len(address.strip()) < 8:
                errors.append("Vui lòng nhập địa chỉ nhận hàng đầy đủ hơn.")
            if not agree:
                errors.append("Bạn cần xác nhận thông tin đặt hàng.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                items = []
                for pid, qty in st.session_state.cart.items():
                    p = PRODUCT_INDEX[pid]
                    items.append({
                        "product_id": pid, "name": p["name"], "qty": qty,
                        "unit_price": p["price"], "line_total": p["price"] * qty,
                    })
                order = {
                    "order_id": "PS-" + datetime.now().strftime("%y%m%d") + "-" + uuid.uuid4().hex[:6].upper(),
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "customer_name": name.strip(), "phone": clean_phone, "email": email.strip(),
                    "address": address.strip(), "city": city, "payment_method": payment,
                    "subtotal": subtotal, "discount": discount, "shipping": shipping, "total": total,
                    "items": items, "note": note.strip(),
                }
                save_order(order)
                st.session_state.order_ids.append(order["order_id"])
                st.session_state.last_order = order
                st.session_state.cart = {}
                st.session_state.coupon = ""
                st.rerun()

        if payment if 'payment' in locals() else False:
            pass
        st.caption("🔒 Thanh toán trong bản demo chỉ mô phỏng luồng checkout, chưa trừ tiền thật.")


def page_blog():
    st.title("Blog kiến thức thể thao")
    st.caption("20 bài viết có sẵn để xây dựng content hub và hỗ trợ SEO/nurturing cho shop.")

    search = st.text_input("Tìm bài viết", placeholder="Ví dụ: squat, chạy bộ, protein, phục hồi...")
    categories = ["Tất cả"] + sorted(set(p["category"] for p in BLOG_POSTS))
    category = st.selectbox("Chủ đề", categories)

    q = normalize_text(search)
    posts = []
    for p in BLOG_POSTS:
        hay = normalize_text(p["title"] + " " + p["excerpt"] + " " + p["content"])
        if q and q not in hay:
            continue
        if category != "Tất cả" and p["category"] != category:
            continue
        posts.append(p)

    st.markdown(f"**{len(posts)} bài viết**")
    for p in posts:
        with st.container(border=True):
            st.markdown(f"### {p['title']}")
            st.markdown(
                f"<div class='blog-meta'>{p['category']} • {p['read']} • {p['date']}</div>",
                unsafe_allow_html=True,
            )
            st.write(p["excerpt"])
            with st.expander("Đọc bài đầy đủ"):
                st.markdown(p["content"])
                st.info("Nội dung mang tính giáo dục chung; các vấn đề sức khỏe/chấn thương cần được đánh giá cá nhân bởi chuyên gia phù hợp.")


def page_chat():
    st.title("🤖 SportBot — Trợ lý mua sắm & kiến thức")
    st.caption("Chạy offline bằng rule-based retrieval nên không cần API key. Có thể nâng cấp sang LLM sau.")

    quick_cols = st.columns(4)
    quick_prompts = [
        "Gợi ý giày chạy dưới 1,5 triệu",
        "Phí ship bao nhiêu?",
        "Mã giảm giá nào đang có?",
        "Tìm bài blog về squat",
    ]
    selected_quick = None
    for col, prompt in zip(quick_cols, quick_prompts):
        with col:
            if st.button(prompt, use_container_width=True, key=f"quick_{normalize_text(prompt)}"):
                selected_quick = prompt

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Hỏi SportBot...")
    prompt = selected_quick or user_input
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        response = answer_chat(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("Xóa hội thoại"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Xin chào! Mình là **SportBot**. Bạn cần mình tư vấn sản phẩm hay kiến thức tập luyện?"}
            ]
            st.rerun()


def page_orders():
    st.title("Đơn hàng của tôi")
    st.caption("Chỉ hiển thị các đơn được tạo trong phiên sử dụng hiện tại để tránh lộ dữ liệu của người khác.")
    orders = load_orders(st.session_state.order_ids)
    if not orders:
        st.info("Bạn chưa tạo đơn hàng nào trong phiên này.")
        return

    for order in orders:
        with st.expander(f"{order['order_id']} • {money(order['total'])} • {order['created_at'].replace('T', ' ')}", expanded=True):
            st.write(f"**Người nhận:** {order['customer_name']} — {order['phone']}")
            st.write(f"**Địa chỉ:** {order['address']}, {order['city']}")
            st.write(f"**Thanh toán:** {order['payment_method']}")
            for item in order["items"]:
                st.write(f"- {item['name']} × {item['qty']} — {money(item['line_total'])}")
            st.divider()
            st.write(f"Tạm tính: {money(order['subtotal'])}")
            st.write(f"Giảm giá: -{money(order['discount'])}")
            st.write(f"Phí giao hàng: {money(order['shipping'])}")
            st.markdown(f"**Tổng: {money(order['total'])}**")

# =========================================================
# MAIN
# =========================================================
init_db()
init_state()

# Tạo sẵn toàn bộ ảnh minh họa ở lần chạy đầu
for _product in PRODUCTS:
    generate_product_image(_product)

page = sidebar()

if page == "Trang chủ":
    page_home()
elif page == "Cửa hàng":
    page_shop()
elif page == "Blog thể thao":
    page_blog()
elif page.startswith("Giỏ hàng"):
    page_cart()
elif page == "SportBot":
    page_chat()
elif page == "Đơn hàng của tôi":
    page_orders()

render_footer()
