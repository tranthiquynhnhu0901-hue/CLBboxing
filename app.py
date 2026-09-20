import streamlit as st
from datetime import datetime
import random


# =========================================================
# 1. CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="PULSE SPORT",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CSS - GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FONT + TOÀN TRANG
    ===================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 0% 0%, rgba(0, 174, 255, 0.09), transparent 28%),
            radial-gradient(circle at 100% 0%, rgba(185, 255, 62, 0.08), transparent 25%),
            #f5f8fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07101e 0%,
                #0b1728 45%,
                #08111d 100%
            );
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.10);
    }


    /* =====================================================
       LOGO
    ===================================================== */

    .logo-wrap {
        padding: 12px 0 18px 0;
    }

    .logo-box {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .logo-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 900;
        color: #07101e;

        background:
            linear-gradient(
                135deg,
                #baff45,
                #67f6ff
            );

        box-shadow:
            0 8px 25px rgba(103,246,255,0.20);
    }

    .logo-name {
        font-size: 20px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: white;
    }

    .logo-sub {
        font-size: 10px;
        font-weight: 700;
        color: #7d91aa;
        letter-spacing: 1.8px;
        margin-top: -2px;
    }


    /* =====================================================
       HERO
    ===================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        min-height: 360px;

        border-radius: 32px;

        padding:
            58px
            60px;

        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(95, 241, 255, 0.40),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 100%,
                rgba(190, 255, 55, 0.25),
                transparent 30%
            ),
            linear-gradient(
                120deg,
                #06101d 0%,
                #0a2854 53%,
                #026c93 100%
            );

        box-shadow:
            0 25px 70px rgba(10, 34, 64, 0.20);

        margin-bottom: 28px;
    }

    .hero::after {
        content: "";
        position: absolute;

        width: 280px;
        height: 280px;

        right: -30px;
        top: -50px;

        border-radius: 50%;

        border:
            42px solid
            rgba(255,255,255,0.06);
    }

    .hero-badge {
        display: inline-block;

        padding:
            8px
            14px;

        border-radius: 999px;

        font-size: 11px;
        font-weight: 800;

        color: #baff45;

        background:
            rgba(186,255,69,0.08);

        border:
            1px solid rgba(186,255,69,0.18);

        letter-spacing: 1.2px;

        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 54px;
        line-height: 1.05;
        letter-spacing: -2px;

        max-width: 800px;

        color: white;

        font-weight: 900;

        margin:
            0 0 18px 0;
    }

    .hero p {
        max-width: 680px;

        font-size: 17px;
        line-height: 1.7;

        color: #c4d7e9;

        margin: 0;
    }


    /* =====================================================
       SECTION TITLE
    ===================================================== */

    .section-wrap {
        margin-top: 38px;
        margin-bottom: 16px;
    }

    .section-kicker {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;

        color: #1686ff;

        text-transform: uppercase;

        margin-bottom: 6px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 900;

        color: #0b1728;

        letter-spacing: -0.8px;

        margin: 0;
    }

    .section-desc {
        margin-top: 5px;

        font-size: 14px;
        line-height: 1.6;

        color: #708196;
    }


    /* =====================================================
       STAT CARDS
    ===================================================== */

    .stat-card {
        background: rgba(255,255,255,0.95);

        border:
            1px solid #e4eaf1;

        border-radius: 22px;

        padding:
            24px;

        min-height: 130px;

        box-shadow:
            0 12px 35px
            rgba(31, 51, 73, 0.06);

        transition:
            all 0.25s ease;
    }

    .stat-card:hover {
        transform:
            translateY(-4px);

        box-shadow:
            0 18px 45px
            rgba(31, 51, 73, 0.11);
    }

    .stat-icon {
        font-size: 24px;

        margin-bottom: 14px;
    }

    .stat-number {
        font-size: 26px;
        font-weight: 900;

        color: #07101e;
    }

    .stat-label {
        font-size: 12px;
        font-weight: 700;

        color: #8391a2;

        margin-top: 4px;
    }


    /* =====================================================
       CATEGORY CARDS
    ===================================================== */

    .category-card {
        min-height: 180px;

        border-radius: 24px;

        padding:
            25px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f5f8fd
            );

        border:
            1px solid #e4eaf1;

        box-shadow:
            0 12px 30px
            rgba(31,51,73,0.05);

        transition:
            all 0.25s ease;
    }

    .category-card:hover {
        transform:
            translateY(-5px);

        border-color:
            #afd5ff;

        box-shadow:
            0 20px 45px
            rgba(31,51,73,0.11);
    }

    .category-icon {
        width: 52px;
        height: 52px;

        border-radius: 16px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 25px;

        background:
            linear-gradient(
                145deg,
                #eaf5ff,
                #edfaff
            );

        margin-bottom: 17px;
    }

    .category-title {
        font-size: 17px;
        font-weight: 800;

        color: #0a1727;

        margin-bottom: 7px;
    }

    .category-desc {
        font-size: 12px;
        line-height: 1.6;

        color: #7b899b;
    }


    /* =====================================================
       PRODUCT CARD
    ===================================================== */

    .product-card {
        background: #ffffff;

        border:
            1px solid #e5eaf0;

        border-radius: 26px;

        padding:
            16px;

        box-shadow:
            0 12px 35px
            rgba(31,51,73,0.06);

        min-height: 505px;

        transition:
            all 0.25s ease;

        margin-bottom: 15px;
    }

    .product-card:hover {
        transform:
            translateY(-6px);

        box-shadow:
            0 24px 55px
            rgba(31,51,73,0.13);

        border-color:
            #b7d8fc;
    }

    .product-visual {
        height: 220px;

        border-radius: 20px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;

        background:
            radial-gradient(
                circle at 50% 40%,
                rgba(84,218,255,0.28),
                transparent 40%
            ),
            linear-gradient(
                140deg,
                #09182b,
                #123861
            );

        position:
            relative;

        overflow:
            hidden;

        margin-bottom: 16px;
    }

    .product-visual::before {
        content: "";

        width: 170px;
        height: 170px;

        border-radius: 50%;

        position: absolute;

        background:
            rgba(255,255,255,0.04);

        border:
            1px solid rgba(255,255,255,0.08);
    }

    .product-emoji {
        font-size: 74px;

        position: relative;

        z-index: 2;

        filter:
            drop-shadow(
                0 10px 12px
                rgba(0,0,0,0.25)
            );
    }

    .badge-hot {
        position: absolute;

        top: 13px;
        left: 13px;

        padding:
            7px 10px;

        border-radius: 999px;

        font-size: 9px;
        font-weight: 900;

        color: #07101e;

        background:
            #baff45;

        z-index: 3;
    }

    .badge-discount {
        position: absolute;

        top: 13px;
        right: 13px;

        padding:
            7px 10px;

        border-radius: 999px;

        font-size: 10px;
        font-weight: 900;

        color: #ffffff;

        background:
            #ff5247;

        z-index: 3;
    }

    .product-category {
        color: #1686ff;

        font-size: 10px;
        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 0.8px;

        margin-bottom: 7px;
    }

    .product-name {
        font-size: 16px;

        font-weight: 850;

        line-height: 1.35;

        color: #07101e;

        min-height: 44px;

        margin-bottom: 8px;
    }

    .rating {
        color: #ffad20;

        font-size: 12px;

        font-weight: 700;

        margin-bottom: 10px;
    }

    .product-desc {
        font-size: 12px;

        color: #7b899b;

        line-height: 1.6;

        min-height: 58px;
    }

    .price-row {
        display: flex;

        align-items: center;

        gap: 10px;

        margin-top: 14px;
    }

    .price {
        font-size: 21px;

        font-weight: 900;

        color: #081726;
    }

    .old-price {
        font-size: 12px;

        color: #9aa7b5;

        text-decoration:
            line-through;
    }


    /* =====================================================
       PRODUCT DETAIL MINI INFO
    ===================================================== */

    .mini-info {
        padding:
            10px 13px;

        border-radius:
            12px;

        background:
            #f5f8fc;

        font-size:
            11px;

        color:
            #6f7f90;

        margin-top:
            10px;
    }


    /* =====================================================
       BLOG
    ===================================================== */

    .blog-card {
        background:
            #ffffff;

        border:
            1px solid #e4eaf1;

        border-radius:
            22px;

        padding:
            22px;

        min-height:
            260px;

        box-shadow:
            0 12px 30px
            rgba(31,51,73,0.05);

        transition:
            all 0.25s ease;

        margin-bottom:
            15px;
    }

    .blog-card:hover {
        transform:
            translateY(-4px);

        box-shadow:
            0 18px 40px
            rgba(31,51,73,0.10);
    }

    .blog-icon {
        width:
            48px;

        height:
            48px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;

        border-radius:
            14px;

        font-size:
            23px;

        background:
            #edf7ff;

        margin-bottom:
            17px;
    }

    .blog-tag {
        font-size:
            10px;

        font-weight:
            800;

        color:
            #1686ff;

        text-transform:
            uppercase;

        letter-spacing:
            1px;
    }

    .blog-title {
        font-size:
            18px;

        font-weight:
            850;

        color:
            #07101e;

        line-height:
            1.4;

        margin-top:
            8px;

        min-height:
            52px;
    }

    .blog-desc {
        font-size:
            12px;

        line-height:
            1.7;

        color:
            #788799;

        margin-top:
            8px;
    }


    /* =====================================================
       CHECKOUT BOX
    ===================================================== */

    .checkout-summary {
        background:
            linear-gradient(
                145deg,
                #07101e,
                #0c2340
            );

        padding:
            26px;

        border-radius:
            24px;

        color:
            white;

        box-shadow:
            0 18px 40px
            rgba(7,16,30,0.18);
    }

    .checkout-summary h3 {
        color:
            white;

        margin-top:
            0;
    }

    .checkout-line {
        display:
            flex;

        justify-content:
            space-between;

        padding:
            9px 0;

        color:
            #b8c8db;

        font-size:
            13px;

        border-bottom:
            1px solid rgba(255,255,255,0.06);
    }

    .checkout-total {
        display:
            flex;

        justify-content:
            space-between;

        padding-top:
            16px;

        font-weight:
            900;

        font-size:
            20px;

        color:
            #baff45;
    }


    /* =====================================================
       CHATBOT
    ===================================================== */

    .bot-header {
        background:
            linear-gradient(
                135deg,
                #07101e,
                #10467c
            );

        color:
            white;

        padding:
            25px;

        border-radius:
            24px;

        margin-bottom:
            20px;
    }

    .bot-status {
        display:
            inline-block;

        width:
            8px;

        height:
            8px;

        border-radius:
            50%;

        background:
            #baff45;

        margin-right:
            5px;
    }


    /* =====================================================
       SUCCESS BOX
    ===================================================== */

    .success-box {
        padding:
            28px;

        border-radius:
            24px;

        background:
            linear-gradient(
                135deg,
                #eaffc9,
                #e7fbff
            );

        border:
            1px solid #c9f39e;

        text-align:
            center;
    }

    .success-box h2 {
        color:
            #1c5623;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .footer {
        margin-top:
            70px;

        padding:
            30px;

        background:
            #07101e;

        border-radius:
            24px;

        color:
            #8ea0b5;

        text-align:
            center;

        font-size:
            12px;
    }


    /* =====================================================
       STREAMLIT BUTTON
    ===================================================== */

    .stButton > button {
        border:
            none;

        border-radius:
            12px;

        font-weight:
            750;

        min-height:
            43px;

        transition:
            all 0.2s ease;

        background:
            linear-gradient(
                135deg,
                #1686ff,
                #00b7db
            );

        color:
            white;
    }

    .stButton > button:hover {
        transform:
            translateY(-2px);

        box-shadow:
            0 8px 18px
            rgba(22,134,255,0.24);

        color:
            white;

        border:
            none;
    }


    /* =====================================================
       INPUT
    ===================================================== */

    [data-baseweb="input"] {
        border-radius:
            12px;
    }

    [data-baseweb="select"] > div {
        border-radius:
            12px;
    }


    /* =====================================================
       RESPONSIVE
    ===================================================== */

    @media(max-width: 768px) {

        .hero {
            padding:
                35px
                25px;

            min-height:
                auto;
        }

        .hero h1 {
            font-size:
                36px;
        }

        .hero p {
            font-size:
                14px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. DỮ LIỆU SẢN PHẨM
# =========================================================

PRODUCTS = [

    {
        "id": 1,
        "name": "Áo Training Performance Pro",
        "category": "Quần áo",
        "price": 349000,
        "old_price": 449000,
        "rating": 4.9,
        "reviews": 218,
        "stock": 32,
        "emoji": "👕",
        "badge": "BEST SELLER",
        "desc": "Áo tập dry-fit co giãn, thoáng khí và phù hợp tập gym."
    },

    {
        "id": 2,
        "name": "Quần Short Training 2-in-1",
        "category": "Quần áo",
        "price": 429000,
        "old_price": 549000,
        "rating": 4.8,
        "reviews": 164,
        "stock": 27,
        "emoji": "🩳",
        "badge": "HOT",
        "desc": "Thiết kế 2 lớp hỗ trợ vận động mạnh và tập luyện cường độ cao."
    },

    {
        "id": 3,
        "name": "Pulse Runner X1",
        "category": "Giày",
        "price": 1390000,
        "old_price": 1690000,
        "rating": 4.9,
        "reviews": 351,
        "stock": 18,
        "emoji": "👟",
        "badge": "TOP RATED",
        "desc": "Giày chạy đệm êm, trọng lượng nhẹ và hỗ trợ chạy hàng ngày."
    },

    {
        "id": 4,
        "name": "Găng tay Gym Grip Pro",
        "category": "Phụ kiện",
        "price": 259000,
        "old_price": 329000,
        "rating": 4.7,
        "reviews": 120,
        "stock": 41,
        "emoji": "🧤",
        "badge": "POPULAR",
        "desc": "Tăng độ bám khi tập tạ và hạn chế chai tay trong quá trình luyện tập."
    },

    {
        "id": 5,
        "name": "Bộ dây kháng lực Power Band",
        "category": "Dụng cụ tập",
        "price": 399000,
        "old_price": 499000,
        "rating": 4.8,
        "reviews": 198,
        "stock": 35,
        "emoji": "⭕",
        "badge": "HOT",
        "desc": "Bộ nhiều mức lực phù hợp tập tại nhà, gym và phục hồi chức năng."
    },

    {
        "id": 6,
        "name": "Kettlebell Power 12KG",
        "category": "Dụng cụ tập",
        "price": 749000,
        "old_price": 899000,
        "rating": 4.8,
        "reviews": 94,
        "stock": 14,
        "emoji": "🏋️",
        "badge": "PRO",
        "desc": "Tạ kettlebell hỗ trợ squat, swing và các bài tập sức mạnh toàn thân."
    },

    {
        "id": 7,
        "name": "Thảm Yoga Flex Premium",
        "category": "Yoga",
        "price": 459000,
        "old_price": 599000,
        "rating": 4.9,
        "reviews": 147,
        "stock": 26,
        "emoji": "🧘",
        "badge": "NEW",
        "desc": "Bề mặt chống trượt, độ đàn hồi cao, phù hợp yoga và mobility."
    },

    {
        "id": 8,
        "name": "Dây nhảy Speed Rope X",
        "category": "Dụng cụ tập",
        "price": 229000,
        "old_price": 299000,
        "rating": 4.7,
        "reviews": 88,
        "stock": 42,
        "emoji": "⚡",
        "badge": "CARDIO",
        "desc": "Dây nhảy tốc độ cao dành cho cardio, boxing và HIIT."
    },

    {
        "id": 9,
        "name": "Bình nước Sport 1L",
        "category": "Phụ kiện",
        "price": 189000,
        "old_price": 239000,
        "rating": 4.6,
        "reviews": 64,
        "stock": 50,
        "emoji": "🥤",
        "badge": "DAILY",
        "desc": "Bình nước dung tích lớn phù hợp gym, chạy bộ và hoạt động ngoài trời."
    },

    {
        "id": 10,
        "name": "Foam Roller Recovery Pro",
        "category": "Phục hồi",
        "price": 329000,
        "old_price": 419000,
        "rating": 4.8,
        "reviews": 112,
        "stock": 31,
        "emoji": "🌀",
        "badge": "RECOVERY",
        "desc": "Hỗ trợ massage cơ, mobility và phục hồi sau tập luyện."
    },

    {
        "id": 11,
        "name": "Túi Gym Urban Sport",
        "category": "Phụ kiện",
        "price": 549000,
        "old_price": 699000,
        "rating": 4.7,
        "reviews": 91,
        "stock": 21,
        "emoji": "🎒",
        "badge": "URBAN",
        "desc": "Túi gym nhiều ngăn, thiết kế hiện đại và chống nước nhẹ."
    },

    {
        "id": 12,
        "name": "Đai Lưng Weightlifting Pro",
        "category": "Phụ kiện",
        "price": 629000,
        "old_price": 799000,
        "rating": 4.9,
        "reviews": 136,
        "stock": 19,
        "emoji": "💪",
        "badge": "STRENGTH",
        "desc": "Hỗ trợ vùng core khi squat, deadlift và các bài compound nặng."
    }

]


# =========================================================
# 4. BLOG
# =========================================================

BLOG_POSTS = [

    ("Gym", "🏋️", "Người mới tập Gym nên bắt đầu từ đâu?",
     "Hướng dẫn xây dựng lịch tập cơ bản và những nguyên tắc quan trọng cho người mới."),

    ("Dinh dưỡng", "🥗", "Protein có vai trò gì trong phát triển cơ bắp?",
     "Tìm hiểu protein, nhu cầu hằng ngày và cách lựa chọn nguồn protein phù hợp."),

    ("Running", "🏃", "5 lỗi phổ biến của người mới chạy bộ",
     "Những lỗi thường gặp khiến hiệu suất chạy giảm và nguy cơ chấn thương tăng."),

    ("Gym", "💪", "Cách xây dựng lịch tập Gym 4 buổi mỗi tuần",
     "Gợi ý cách phân chia nhóm cơ giúp cân bằng giữa tập luyện và phục hồi."),

    ("Dinh dưỡng", "🍳", "Nên ăn gì trước khi tập?",
     "Các nhóm thực phẩm giúp bổ sung năng lượng trước buổi tập."),

    ("Phục hồi", "😴", "Giấc ngủ ảnh hưởng thế nào tới cơ bắp?",
     "Ngủ đủ giúp cơ thể phục hồi, cân bằng hormone và nâng cao hiệu suất."),

    ("Running", "👟", "Cách chọn giày chạy bộ phù hợp",
     "Những yếu tố cần quan tâm khi lựa chọn giày chạy dành cho người mới."),

    ("Gym", "🏋️", "Squat đúng kỹ thuật cho người mới",
     "Hướng dẫn tư thế squat cơ bản và các lỗi thường gặp."),

    ("Gym", "⚡", "Deadlift có thực sự nguy hiểm?",
     "Hiểu đúng về deadlift và cách tập an toàn hơn."),

    ("Cardio", "❤️", "Cardio bao nhiêu phút là đủ?",
     "Cách lựa chọn thời lượng cardio theo từng mục tiêu tập luyện."),

    ("Giảm mỡ", "🔥", "HIIT có giúp giảm mỡ nhanh hơn?",
     "Phân tích ưu điểm và hạn chế của hình thức tập HIIT."),

    ("Mobility", "🧘", "Mobility khác Stretching như thế nào?",
     "Phân biệt hai phương pháp giúp cải thiện khả năng vận động."),

    ("Dinh dưỡng", "🥛", "Có cần uống Whey Protein không?",
     "Whey chỉ là thực phẩm bổ sung và không phải điều bắt buộc để tăng cơ."),

    ("Gym", "📈", "Progressive Overload là gì?",
     "Nguyên tắc quan trọng giúp cơ thể tiếp tục thích nghi và phát triển."),

    ("Phục hồi", "🌀", "Foam Roller có tác dụng gì?",
     "Cách sử dụng foam roller trong quá trình phục hồi sau tập."),

    ("Running", "🏃", "Zone 2 Running là gì?",
     "Phương pháp chạy ở cường độ thấp giúp phát triển nền tảng tim mạch."),

    ("Dinh dưỡng", "💧", "Uống bao nhiêu nước khi tập thể thao?",
     "Gợi ý cách bổ sung nước hợp lý trước, trong và sau buổi tập."),

    ("Gym", "🧠", "Mind-Muscle Connection là gì?",
     "Hiểu mối liên hệ giữa tập trung tinh thần và khả năng kiểm soát cơ bắp."),

    ("Trang bị", "🎒", "Những món đồ nên có khi đi Gym",
     "Danh sách những phụ kiện cơ bản giúp buổi tập thuận tiện hơn."),

    ("Lifestyle", "🎯", "Làm sao duy trì thói quen tập luyện?",
     "Các phương pháp giúp bạn duy trì động lực và xây dựng thói quen lâu dài.")

]


# =========================================================
# 5. SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào! Tôi là SportBot. Bạn đang tìm sản phẩm hay kiến thức tập luyện?"
        }
    ]

if "order_success" not in st.session_state:
    st.session_state.order_success = False


# =========================================================
# 6. HÀM HỖ TRỢ
# =========================================================

def money(number):

    return f"{number:,.0f}đ".replace(",", ".")


def add_to_cart(product_id):

    if product_id not in st.session_state.cart:
        st.session_state.cart[product_id] = 1

    else:
        st.session_state.cart[product_id] += 1


def cart_count():

    return sum(st.session_state.cart.values())


def cart_total():

    total = 0

    for product in PRODUCTS:

        if product["id"] in st.session_state.cart:

            total += (
                product["price"]
                *
                st.session_state.cart[product["id"]]
            )

    return total


def discount_percent(product):

    return round(
        (
            1
            -
            product["price"]
            /
            product["old_price"]
        )
        *
        100
    )


# =========================================================
# 7. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo-wrap">
            <div class="logo-box">

                <div class="logo-icon">
                    ⚡
                </div>

                <div>

                    <div class="logo-name">
                        PULSE SPORT
                    </div>

                    <div class="logo-sub">
                        PERFORMANCE STORE
                    </div>

                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "MENU",
        [
            "🏠 Trang chủ",
            "🛍️ Cửa hàng",
            f"🛒 Giỏ hàng ({cart_count()})",
            "❤️ Yêu thích",
            "📚 Blog",
            "🤖 SportBot"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption("HỖ TRỢ KHÁCH HÀNG")

    st.markdown(
        """
        **📞 Hotline**

        0900 123 456

        **✉️ Email**

        hello@pulsesport.vn

        **🕒 Thời gian hỗ trợ**

        08:00 - 22:00
        """
    )


# =========================================================
# 8. COMPONENT - TITLE
# =========================================================

def section_title(kicker, title, description=""):

    st.markdown(
        f"""
        <div class="section-wrap">

            <div class="section-kicker">
                {kicker}
            </div>

            <div class="section-title">
                {title}
            </div>

            <div class="section-desc">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 9. COMPONENT - PRODUCT
# =========================================================

def product_card(product, prefix):

    discount = discount_percent(product)

    st.markdown(
        f"""
        <div class="product-card">

            <div class="product-visual">

                <div class="badge-hot">
                    {product["badge"]}
                </div>

                <div class="badge-discount">
                    -{discount}%
                </div>

                <div class="product-emoji">
                    {product["emoji"]}
                </div>

            </div>

            <div class="product-category">
                {product["category"]}
            </div>

            <div class="product-name">
                {product["name"]}
            </div>

            <div class="rating">
                ⭐ {product["rating"]}
                &nbsp;
                <span style="color:#8b98a7">
                    ({product["reviews"]} đánh giá)
                </span>
            </div>

            <div class="product-desc">
                {product["desc"]}
            </div>

            <div class="price-row">

                <div class="price">
                    {money(product["price"])}
                </div>

                <div class="old-price">
                    {money(product["old_price"])}
                </div>

            </div>

            <div class="mini-info">
                Còn {product["stock"]} sản phẩm
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([4, 1])

    with c1:

        if st.button(
            "🛒 Thêm vào giỏ",
            key=f"cart_{prefix}_{product['id']}",
            use_container_width=True
        ):

            add_to_cart(product["id"])

            st.toast(
                f"Đã thêm {product['name']} vào giỏ hàng"
            )

    with c2:

        heart = (
            "❤️"
            if product["id"] in st.session_state.wishlist
            else "♡"
        )

        if st.button(
            heart,
            key=f"wish_{prefix}_{product['id']}",
            use_container_width=True
        ):

            if product["id"] in st.session_state.wishlist:

                st.session_state.wishlist.remove(
                    product["id"]
                )

            else:

                st.session_state.wishlist.append(
                    product["id"]
                )

            st.rerun()


# =========================================================
# 10. TRANG CHỦ
# =========================================================

def home_page():

    st.markdown(
        """
        <div class="hero">

            <div class="hero-badge">
                PERFORMANCE • TRAINING • LIFESTYLE
            </div>

            <h1>
                Train Strong.<br>
                Live Better.
            </h1>

            <p>
                PULSE SPORT mang đến trang phục,
                phụ kiện và dụng cụ tập luyện hiện đại
                dành cho người yêu thể thao.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    stats = [

        (
            stat1,
            "🛍️",
            "120+",
            "Sản phẩm thể thao"
        ),

        (
            stat2,
            "⭐",
            "4.8/5",
            "Đánh giá khách hàng"
        ),

        (
            stat3,
            "🚚",
            "700K",
            "Miễn phí vận chuyển"
        ),

        (
            stat4,
            "📚",
            "20",
            "Bài viết kiến thức"
        )

    ]

    for column, icon, number, label in stats:

        with column:

            st.markdown(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        {icon}
                    </div>

                    <div class="stat-number">
                        {number}
                    </div>

                    <div class="stat-label">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    section_title(
        "SHOP BY CATEGORY",
        "Khám phá theo nhu cầu",
        "Các nhóm sản phẩm dành cho nhiều hình thức tập luyện khác nhau."
    )

    categories = [

        (
            "👕",
            "Training Wear",
            "Trang phục tập luyện thoáng khí và linh hoạt."
        ),

        (
            "👟",
            "Running",
            "Giày và phụ kiện dành cho chạy bộ."
        ),

        (
            "🏋️",
            "Strength",
            "Dụng cụ hỗ trợ tập luyện sức mạnh."
        ),

        (
            "🧘",
            "Recovery",
            "Yoga, mobility và phục hồi cơ thể."
        )

    ]

    cols = st.columns(4)

    for col, item in zip(cols, categories):

        icon, title, desc = item

        with col:

            st.markdown(
                f"""
                <div class="category-card">

                    <div class="category-icon">
                        {icon}
                    </div>

                    <div class="category-title">
                        {title}
                    </div>

                    <div class="category-desc">
                        {desc}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    section_title(
        "TRENDING NOW",
        "Sản phẩm nổi bật",
        "Những sản phẩm được khách hàng quan tâm nhiều."
    )

    featured = PRODUCTS[:4]

    cols = st.columns(4)

    for col, product in zip(cols, featured):

        with col:

            product_card(
                product,
                "home"
            )

    section_title(
        "SPORT KNOWLEDGE",
        "Kiến thức dành cho bạn",
        "Không chỉ bán sản phẩm, PULSE SPORT còn giúp bạn tập luyện thông minh hơn."
    )

    cols = st.columns(3)

    for index, post in enumerate(BLOG_POSTS[:3]):

        tag, icon, title, desc = post

        with cols[index]:

            st.markdown(
                f"""
                <div class="blog-card">

                    <div class="blog-icon">
                        {icon}
                    </div>

                    <div class="blog-tag">
                        {tag}
                    </div>

                    <div class="blog-title">
                        {title}
                    </div>

                    <div class="blog-desc">
                        {desc}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 11. CỬA HÀNG
# =========================================================

def shop_page():

    section_title(
        "PULSE PERFORMANCE STORE",
        "Cửa hàng thể thao",
        "Tìm kiếm sản phẩm phù hợp với nhu cầu tập luyện của bạn."
    )

    filter1, filter2, filter3 = st.columns(
        [2.2, 1.3, 1.3]
    )

    with filter1:

        keyword = st.text_input(
            "Tìm kiếm",
            placeholder="Tìm áo, giày, phụ kiện..."
        )

    categories = [
        "Tất cả"
    ] + sorted(
        list(
            set(
                product["category"]
                for product in PRODUCTS
            )
        )
    )

    with filter2:

        selected_category = st.selectbox(
            "Danh mục",
            categories
        )

    with filter3:

        sort = st.selectbox(
            "Sắp xếp",
            [
                "Phổ biến",
                "Giá thấp → cao",
                "Giá cao → thấp",
                "Đánh giá cao"
            ]
        )

    max_price = st.slider(
        "Khoảng giá tối đa",
        200000,
        2000000,
        2000000,
        50000
    )

    filtered = PRODUCTS.copy()

    if keyword:

        filtered = [

            product

            for product in filtered

            if keyword.lower()
            in product["name"].lower()

        ]

    if selected_category != "Tất cả":

        filtered = [

            product

            for product in filtered

            if product["category"]
            ==
            selected_category

        ]

    filtered = [

        product

        for product in filtered

        if product["price"]
        <=
        max_price

    ]

    if sort == "Giá thấp → cao":

        filtered.sort(
            key=lambda x: x["price"]
        )

    elif sort == "Giá cao → thấp":

        filtered.sort(
            key=lambda x: x["price"],
            reverse=True
        )

    elif sort == "Đánh giá cao":

        filtered.sort(
            key=lambda x: x["rating"],
            reverse=True
        )

    st.caption(
        f"Tìm thấy {len(filtered)} sản phẩm"
    )

    for start in range(
        0,
        len(filtered),
        4
    ):

        rows = st.columns(4)

        chunk = filtered[
            start:
            start + 4
        ]

        for col, product in zip(
            rows,
            chunk
        ):

            with col:

                product_card(
                    product,
                    "shop"
                )


# =========================================================
# 12. GIỎ HÀNG
# =========================================================

def cart_page():

    section_title(
        "SHOPPING CART",
        "Giỏ hàng của bạn",
        "Kiểm tra sản phẩm trước khi tiến hành thanh toán."
    )

    if not st.session_state.cart:

        st.info(
            "Giỏ hàng hiện chưa có sản phẩm."
        )

        return

    left, right = st.columns(
        [1.7, 1]
    )

    with left:

        for product in PRODUCTS:

            if product["id"] not in st.session_state.cart:

                continue

            qty = st.session_state.cart[
                product["id"]
            ]

            with st.container(
                border=True
            ):

                c1, c2, c3 = st.columns(
                    [0.8, 2.5, 1.1]
                )

                with c1:

                    st.markdown(
                        f"""
                        <div style="
                            height:110px;
                            border-radius:18px;
                            display:flex;
                            justify-content:center;
                            align-items:center;
                            font-size:48px;
                            background:
                            linear-gradient(
                                145deg,
                                #09182b,
                                #174b7a
                            );
                        ">
                            {product["emoji"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with c2:

                    st.markdown(
                        f"### {product['name']}"
                    )

                    st.caption(
                        product["category"]
                    )

                    st.markdown(
                        f"**{money(product['price'])}**"
                    )

                with c3:

                    new_qty = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=10,
                        value=qty,
                        key=f"qty_{product['id']}"
                    )

                    st.session_state.cart[
                        product["id"]
                    ] = new_qty

                    if st.button(
                        "Xóa",
                        key=f"delete_{product['id']}",
                        use_container_width=True
                    ):

                        del st.session_state.cart[
                            product["id"]
                        ]

                        st.rerun()

    subtotal = cart_total()

    shipping = (
        0
        if subtotal >= 700000
        else 30000
    )

    total = (
        subtotal
        +
        shipping
    )

    with right:

        st.markdown(
            f"""
            <div class="checkout-summary">

                <h3>
                    Tóm tắt đơn hàng
                </h3>

                <div class="checkout-line">

                    <span>Tạm tính</span>

                    <span>
                        {money(subtotal)}
                    </span>

                </div>

                <div class="checkout-line">

                    <span>Vận chuyển</span>

                    <span>
                        {
                            "Miễn phí"
                            if shipping == 0
                            else money(shipping)
                        }
                    </span>

                </div>

                <div class="checkout-total">

                    <span>Tổng cộng</span>

                    <span>
                        {money(total)}
                    </span>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### Thông tin nhận hàng")

        customer_name = st.text_input(
            "Họ và tên"
        )

        phone = st.text_input(
            "Số điện thoại"
        )

        email = st.text_input(
            "Email"
        )

        city = st.selectbox(
            "Tỉnh / Thành phố",
            [
                "TP. Hồ Chí Minh",
                "Hà Nội",
                "Đà Nẵng",
                "Cần Thơ",
                "Bình Dương",
                "Đồng Nai",
                "Khác"
            ]
        )

        address = st.text_area(
            "Địa chỉ nhận hàng"
        )

        payment = st.radio(
            "Phương thức thanh toán",
            [
                "Thanh toán khi nhận hàng",
                "Chuyển khoản ngân hàng",
                "Thẻ ngân hàng"
            ]
        )

        if st.button(
            "ĐẶT HÀNG NGAY",
            use_container_width=True
        ):

            if (
                not customer_name
                or
                not phone
                or
                not address
            ):

                st.warning(
                    "Vui lòng nhập đầy đủ họ tên, số điện thoại và địa chỉ."
                )

            else:

                st.session_state.order_success = True

                order_code = (
                    "PS"
                    +
                    datetime.now().strftime(
                        "%d%m%H%M"
                    )
                    +
                    str(
                        random.randint(
                            10,
                            99
                        )
                    )
                )

                st.session_state.last_order = (
                    order_code
                )

                st.session_state.cart = {}

                st.rerun()

    if st.session_state.order_success:

        st.markdown(
            f"""
            <div class="success-box">

                <div style="
                    font-size:45px;
                    margin-bottom:8px;
                ">
                    ✅
                </div>

                <h2>
                    Bạn đã đặt hàng thành công!
                </h2>

                <p>
                    Mã đơn hàng:
                    <strong>
                        {st.session_state.get(
                            "last_order",
                            ""
                        )}
                    </strong>
                </p>

                <p>
                    PULSE SPORT sẽ liên hệ xác nhận
                    đơn hàng trong thời gian sớm nhất.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 13. WISHLIST
# =========================================================

def wishlist_page():

    section_title(
        "YOUR FAVORITES",
        "Sản phẩm yêu thích",
        "Danh sách sản phẩm bạn đã lưu."
    )

    products = [

        product

        for product in PRODUCTS

        if product["id"]
        in st.session_state.wishlist

    ]

    if not products:

        st.info(
            "Bạn chưa lưu sản phẩm nào."
        )

        return

    for start in range(
        0,
        len(products),
        4
    ):

        cols = st.columns(4)

        for col, product in zip(
            cols,
            products[start:start + 4]
        ):

            with col:

                product_card(
                    product,
                    "wishlist"
                )


# =========================================================
# 14. BLOG
# =========================================================

def blog_page():

    section_title(
        "PULSE KNOWLEDGE",
        "Kiến thức thể thao",
        "Tổng hợp kiến thức về tập luyện, dinh dưỡng, chạy bộ và phục hồi."
    )

    search = st.text_input(
        "Tìm bài viết",
        placeholder="Ví dụ: Gym, Protein, Running..."
    )

    tags = sorted(
        list(
            set(
                post[0]
                for post in BLOG_POSTS
            )
        )
    )

    selected_tag = st.selectbox(
        "Chủ đề",
        ["Tất cả"] + tags
    )

    filtered_posts = []

    for post in BLOG_POSTS:

        tag, icon, title, desc = post

        if (
            selected_tag != "Tất cả"
            and
            tag != selected_tag
        ):

            continue

        if search:

            text = (
                title
                +
                " "
                +
                desc
                +
                " "
                +
                tag
            ).lower()

            if search.lower() not in text:

                continue

        filtered_posts.append(post)

    for start in range(
        0,
        len(filtered_posts),
        3
    ):

        cols = st.columns(3)

        for col, post in zip(
            cols,
            filtered_posts[start:start + 3]
        ):

            tag, icon, title, desc = post

            with col:

                st.markdown(
                    f"""
                    <div class="blog-card">

                        <div class="blog-icon">
                            {icon}
                        </div>

                        <div class="blog-tag">
                            {tag}
                        </div>

                        <div class="blog-title">
                            {title}
                        </div>

                        <div class="blog-desc">
                            {desc}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Đọc bài viết →",
                    key=f"blog_{title}",
                    use_container_width=True
                ):

                    st.info(
                        "Phần nội dung chi tiết bài viết có thể phát triển ở bước tiếp theo."
                    )


# =========================================================
# 15. CHATBOT
# =========================================================

def bot_reply(text):

    text = text.lower()

    if (
        "giày"
        in text
    ):

        return (
            "Nếu bạn đang tìm giày chạy, "
            "Pulse Runner X1 là sản phẩm nổi bật "
            "với mức giá 1.390.000đ và đánh giá 4.9/5."
        )

    if (
        "găng"
        in text
    ):

        return (
            "Găng tay Gym Grip Pro phù hợp "
            "cho tập tạ và giúp tăng độ bám khi luyện tập."
        )

    if (
        "700"
        in text
        or
        "ship"
        in text
        or
        "vận chuyển"
        in text
    ):

        return (
            "PULSE SPORT miễn phí vận chuyển "
            "cho đơn hàng từ 700.000đ."
        )

    if (
        "protein"
        in text
        or
        "dinh dưỡng"
        in text
    ):

        return (
            "Trong khu Blog hiện có nhiều bài về "
            "Protein, Whey Protein, dinh dưỡng trước tập "
            "và bổ sung nước."
        )

    if (
        "gym"
        in text
    ):

        return (
            "Nếu bạn mới tập Gym, hãy ưu tiên kỹ thuật, "
            "lịch tập đơn giản và tăng mức độ tập luyện từ từ."
        )

    if (
        "thanh toán"
        in text
    ):

        return (
            "App hỗ trợ mô phỏng thanh toán khi nhận hàng, "
            "chuyển khoản và thẻ ngân hàng."
        )

    return (
        "Bạn có thể hỏi mình về sản phẩm, "
        "giày chạy, dụng cụ Gym, phí vận chuyển, "
        "thanh toán hoặc kiến thức thể thao."
    )


def chatbot_page():

    section_title(
        "PULSE AI ASSISTANT",
        "SportBot",
        "Trợ lý hỗ trợ khách hàng và tư vấn sản phẩm."
    )

    st.markdown(
        """
        <div class="bot-header">

            <h2 style="
                margin:0 0 5px 0;
                color:white;
            ">
                🤖 SportBot
            </h2>

            <div style="
                color:#bcd0e3;
                font-size:13px;
            ">

                <span class="bot-status"></span>

                Đang hoạt động

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    question = st.chat_input(
        "Hỏi SportBot..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = bot_reply(
            question
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()


# =========================================================
# 16. ROUTER
# =========================================================

if page == "🏠 Trang chủ":

    home_page()

elif page == "🛍️ Cửa hàng":

    shop_page()

elif page.startswith("🛒"):

    cart_page()

elif page == "❤️ Yêu thích":

    wishlist_page()

elif page == "📚 Blog":

    blog_page()

elif page == "🤖 SportBot":

    chatbot_page()


# =========================================================
# 17. FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <strong style="color:white">
            PULSE SPORT
        </strong>

        <br><br>

        Performance • Training • Running • Lifestyle

        <br>

        © 2026 PULSE SPORT.
        All rights reserved.

    </div>
    """,
    unsafe_allow_html=True
)
