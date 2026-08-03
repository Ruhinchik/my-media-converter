import streamlit as st
import yt_dlp
import os
import tempfile
from PIL import Image, ImageEnhance, ImageFilter

# ================= 💰 НАСТРОЙКИ ПРЕМИУМА =================
SECRET_KEY = "Ruhinchik_PRO_2026"
DONATE_URL = "https://donationalerts.com" 
# =========================================================

st.set_page_config(page_title="Media, Games & Mobile Premium", page_icon="👑", layout="centered")

st.title("🌌 Космо-Комбайн v11.0 Финал")
st.write("Скачивайте медиа, улучшайте фото и играйте прямо с телефона!")

tab_link, tab_file, tab_games = st.tabs(["🔗 Ссылка", "🎨 ИИ-Реставратор", "🎮 Яндекс Игры"])

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ (КАК В ПЕРВОМ КОДЕ) =================
with tab_link:
    st.write("### 🔗 Загрузчик из соцсетей")
    link = st.text_input("Вставьте вашу ссылку сюда:", placeholder="https://...", key="link_input")

    if link:
        st.markdown("---")
        # Базовые и самые надежные настройки из первой версии кода
        ydl_opts_base = {
            'noplaylist': True, 
            'quiet': True, 
            'no_check_certificate': True,
            'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        }
        
        with st.spinner("🔍 Умный анализ медиа..."):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                    info = ydl.extract_info(link, download=False)
                    video_title = info.get('title', 'Медиа файл')
                    thumbnail_url = info.get('thumbnail', None)
                st.write(f"**📝 {video_title}**")
                if thumbnail_url: st.image(thumbnail_url, use_container_width=True)
            except Exception:
                st.write("🔗 Ссылка распознана. Готова к скачиванию!")

        st.markdown("---")
        col1, col2 = st.columns(2)
        
        # Кнопка MP4 (Чистая логика из первой версии)
        with col1:
            if st.button("🎥 Скачать MP4 Видео", use_container_width=True, key="btn_mp4_link"):
                with st.spinner("🚀 Скачивание файла..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            # Качаем лучшее готовое mp4 видео, без разделения на видео/аудио потоки
                            ydl_opts.update({
                                'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 
                                'format': 'best[ext=mp4]/best'
                            })
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                            with open(filename, "rb") as f:
                                st.balloons()
                                st.download_button("📥 Сохранить MP4 на устройство", f.read(), file_name=os.path.basename(filename), mime="video/mp4", use_container_width=True)
                    except Exception as e: 
                        st.error("Не удалось скачать через сервер. Попробуйте другую ссылку.")
                        
        # Кнопка MP3 (Чистая логика из первой версии)
        with col2:
            if st.button("🎶 Скачать MP3 Звук", use_container_width=True, key="btn_mp3_link"):
                with st.spinner("🎵 Извлечение звука..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({
                                'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 
                                'format': 'bestaudio/best', 
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio', 
                                    'preferredcodec': 'mp3', 
                                    'preferredquality': '192'
                                }]
                            })
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                                base, _ = os.path.splitext(filename)
                                mp3_filename = base + ".mp3"
                            with open(mp3_filename, "rb") as f:
                                st.balloons()
                                st.download_button("📥 Сохранить MP3 в музыку", f.read(), file_name=os.path.basename(mp3_filename), mime="audio/mp3", use_container_width=True)
                    except Exception: 
                        st.error("Ошибка извлечения аудиодорожки.")

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
                with st.spinner("✂️ Извлекаю аудио..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                            t_video.write(uploaded_file.read())
                            video_path = t_video.name
                        audio_path = video_path.replace(".mp4", ".mp3")
                        os.system(f'ffmpeg -i "{video_path}" -vn -ar 44100 -ac 2 -b:a 192k "{audio_path}" -y')
                        with open(audio_path, "rb") as f:
                            st.balloons()
                            st.download_button("📥 Скачать готовый MP3", f.read(), file_name="audio.mp3", mime="audio/mp3", use_container_width=True)
                        os.remove(video_path)
                        os.remove(audio_path)
                    except Exception as e: st.error(f"Ошибка: {e}")

# ================= ВКЛАДКА 3: ИГРОВАЯ ЗОНА =================
with tab_games:
    st.write("### 🕹️ Стабильные игры от Яндекс Платформы")
    selected_game = st.selectbox("🎯 Выберите игру:", ["🔴 Шашки (На двоих)", "♟️ Шахматы (Интеллект)", "🏎️ Неоновые Гонки (Драйв)"])
    
    if "Шашки" in selected_game: game_url = "https://html5games.com"
    elif "Шахматы" in selected_game: game_url = "https://html5games.com"
    elif "Гонки" in selected_game: game_url = "https://html5games.com"

    st.components.v1.iframe(game_url, height=550, scrolling=False)

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом | 📱 Полная поддержка iOS и Android")
