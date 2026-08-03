import streamlit as st
import yt_dlp
import os
import tempfile
from PIL import Image, ImageEnhance, ImageFilter

# ================= 💰 НАСТРОЙКИ ПРЕМИУМА =================
# Твой секретный пароль для открытия Премиум-функций
SECRET_KEY = "Ruhinchik_PRO_2026"

# Ссылка на донаты (DonationAlerts или Boosty)
DONATE_URL = "https://donationalerts.com"
# =========================================================

# Настройка страницы (layout="centered" идеально подходит для мобилок)
st.set_page_config(
    page_title="Media, Games & Mobile Premium", 
    page_icon="👑", 
    layout="centered" 
)

# Адаптивный дизайн для телефонов (крупные кнопки и скрытие логов)
st.markdown("""
    <style>
    .stButton>button {
        width: 100% !important;
        height: 55px !important;
        font-size: 16px !important;
        border-radius: 12px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        height: 45px !important;
    }
    @media (max-width: 640px) {
        h1 { font-size: 24px !important; }
        .stTabs [data-baseweb="tab"] { font-size: 14px !important; padding: 10px 5px !important; }
    }
    </style>
""", unsafe_allowed_html=True)

st.title("🌌 Космо-Комбайн v10.0 Mobile")
st.write("Скачивайте медиа, улучшайте фото и играйте прямо с телефона!")

# Вкладки, адаптированные под мобильный экран
tab_link, tab_file, tab_games = st.tabs(["🔗 Ссылка", "🎨 ИИ-Реставратор", "🎮 Игры 2D"])

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ =================
with tab_link:
    st.write("### 🔗 Загрузчик из соцсетей")
    link = st.text_input("Вставьте вашу ссылку сюда:", placeholder="https://...", key="link_input")

    if link:
        st.markdown("---")
        ydl_opts_base = {
            'noplaylist': True, 'quiet': True, 'no_check_certificate': True,
            'extractor_args': {'youtube': ['player_client=android,web;player_skip=webpage_download']},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            }
        }
        with St.spinner("🔍 Анализирую медиа..."):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                    info = ydl.extract_info(link, download=False)
                    video_title = info.get('title', 'Медиа файл')
                    thumbnail_url = info.get('thumbnail', None)
                    direct_video_url = info.get('url', None)
                    if 'formats' in info:
                        for f in info['formats']:
                            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                                direct_video_url = f['url']
                                break
                st.write(f"**📝 {video_title}**")
                if thumbnail_url: st.image(thumbnail_url, use_container_width=True)
                if direct_video_url and (direct_video_url != thumbnail_url): st.video(direct_video_url)
            except Exception: st.error("Скачайте файл кнопками ниже!")

        st.markdown("---")
        st.write("#### 📥 Выберите качество:")
        
        # Полный список всех качеств видео
        video_quality = st.selectbox(
            "🎬 Качество видео (MP4):", 
            [
                "144p (Низкое - Бесплатно)", 
                "360p (Обычное - Бесплатно)", 
                "480p (Эконом - Бесплатно)", 
                "720p (HD - Бесплатно)", 
                "1080p (Full HD - PREMIUM 👑)", 
                "1440p (2K Ultra - PREMIUM 👑)", 
                "2160p (4K Max - PREMIUM 👑)"
            ]
        )
        
        # Полный список всех качеств звука
        audio_quality = st.selectbox(
            "🎛️ Качество звука (MP3):", 
            [
                "64 kbps (Низкое - Бесплатно)", 
                "128 kbps (Среднее - Бесплатно)", 
                "192 kbps (Хорошее - Бесплатно)", 
                "320 kbps (Премиум - PREMIUM 👑)"
            ]
        )

        # Проверяем на Премиум
        is_link_premium = "PREMIUM" in video_quality or "PREMIUM" in audio_quality
        
        premium_access = True
        if is_link_premium:
            st.warning("⚠️ Вы выбрали PREMIUM качество. Нужен секретный ключ!")
            st.markdown(f"🎁 **[ПОЛУЧИТЬ ПРЕМИУМ КЛЮЧ ЗА ДОНАТ]({DONATE_URL})**")
            user_key = st.text_input("🔑 Введите Премиум-ключ:", type="password", key="key_link")
            if user_key == SECRET_KEY:
                st.success("✅ Доступ открыт!")
                premium_access = True
            elif user_key == "":
                premium_access = False
            else:
                st.error("❌ Ключ неверный!")
                premium_access = False

        # Настройка битрейта под выбор
        bitrate = "192"
        for b in ["64", "128", "192", "320"]:
            if b in audio_quality: bitrate = b

        # Настройка разрешения видео под выбор
        v_limit = "720"
        for res in ["144", "360", "480", "720", "1080", "1440", "2160"]:
            if res in video_quality: v_limit = res
        video_format = f"best[height<={v_limit}][ext=mp4]/best"

        # Кнопки
        if link and premium_access:
            if st.button("🎥 Скачать MP4 Видео", key="btn_mp4_link"):
                with st.spinner("🚀 Скачивание..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': video_format})
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                            with open(filename, "rb") as f:
                                st.download_button("📥 Сохранить MP4 в Галерею", f.read(), file_name=os.path.basename(filename), mime="video/mp4", use_container_width=True)
                    except Exception: st.error("Ошибка скачивания.")
            
            if st.button("🎶 Скачать MP3 Звук", key="btn_mp3_link"):
                with st.spinner("🎵 Извлечение звука..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}]})
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                                base, _ = os.path.splitext(filename)
                                mp3_filename = base + ".mp3"
                            with open(mp3_filename, "rb") as f:
                                st.balloons()
                                st.download_button("📥 Сохранить MP3 в музыку", f.read(), file_name=os.path.basename(mp3_filename), mime="audio/mp3", use_container_width=True)
                    except Exception: st.error("Ошибка аудио.")

# ================= ВКЛАДКА 2: ИИ-РЕСТАВРАТОР ФОТО / ГАЛЕРЕИ =================
with tab_file:
    st.write("### 🎨 Магический ИИ-Реставратор")
    file_type = st.radio("Что делаем?", ["🖼️ Восстановить фото", "📁 Видео из галереи в MP3"])
    
    if file_type == "🖼️ Восстановить фото":
        uploaded_image = st.file_uploader("Загрузите картинку с телефона", type=["jpg", "jpeg", "png"])
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.write("#### Настройки резкости:")
            sharpness_val = st.slider("⚡ Сила резкости:", 1.0, 3.0, 1.5)
            contrast_val = st.slider("🌈 PREMIUM 👑 Контраст (Выше 1.5 нужен Премиум):", 1.0, 3.0, 1.2)
            
            photo_premium = True
            if contrast_val > 1.5:
                st.warning("⚠️ Выбран Ультра-контраст Премиум уровня!")
                st.markdown(f"🎁 **[ПОЛУЧИТЬ ПРЕМИУМ КЛЮЧ ЗА ДОНАТ]({DONATE_URL})**")
                user_key_img = st.text_input("🔑 Введите Премиум-ключ:", type="password", key="key_img")
                if user_key_img == SECRET_KEY:
                    st.success("✅ Доступ открыт!")
                    photo_premium = True
                else:
                    photo_premium = False
            
            if photo_premium:
                st.image(image, caption="Было", use_container_width=True)
                with st.spinner("🔮 ИИ восстанавливает пиксели..."):
                    enhanced_img = image.filter(ImageFilter.DETAIL).filter(ImageFilter.SHARPEN)
                    enhanced_img = ImageEnhance.Sharpness(enhanced_img).enhance(sharpness_val)
                    enhanced_img = ImageEnhance.Contrast(enhanced_img).enhance(contrast_val)
                    st.image(enhanced_img, caption="Стало", use_container_width=True)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img_file:
                    enhanced_img.save(tmp_img_file.name)
                    with open(tmp_img_file.name, "rb") as img_f:
                        st.download_button("📥 Скачать готовое фото", img_f.read(), file_name="ai_restored_.png", mime="image/png", use_container_width=True)
                    os.remove(tmp_img_file.name)

    elif file_type == "📁 Видео из галереи в MP3":
        uploaded_file = st.file_uploader("Выберите видео с телефона", type=["mp4", "mov", "avi"])
        if uploaded_file is not None:
            st.success(f"🎬 Видео загружено!")
            if st.button("🎵 Извлечь звук в MP3", key="btn_local_mp3"):
