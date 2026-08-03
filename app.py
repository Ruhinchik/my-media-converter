import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(page_title="Media Mega Downloader", page_icon="⚡", layout="centered")

# ================= НАСТРОЙКА ДИЗАЙНА И ФОНА С ТВОИМ CSS =================
# Здесь мы меняем фон всего сайта. Сейчас стоит красивый темный градиент.
# Если хочешь вместо него картинку, замени строку с background на:
# background-image: url('ССЫЛКА_НА_ТВОЮ_КАРТИНКУ_ИЗ_ИНТЕРНЕТА'); background-size: cover;
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 50%, #06040a 100%);
    }
    h1 { 
        color: #a04ef6; 
        font-family: 'Helvetica Neue', sans-serif; 
        text-align: center;
        text-shadow: 0 0 10px rgba(160, 78, 246, 0.5);
    }
    p { text-align: center; color: #d1c4e9; }
    
    /* Красивый стиль для кнопок */
    .stButton>button {
        background: linear-gradient(45deg, #a04ef6, #673ab7);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #a04ef6;
        color: white;
    }
    </style>
""", unsafe_allowed_html=True)

st.title("⚡ Media Premium Downloader")
st.write("Качайте видео и музыку в любом качестве в один клик!")

# Поле ввода ссылки
link = st.text_input("🔗 Вставьте вашу ссылку сюда:", placeholder="https://...")

# Создаем настройки качества в два столбца (Новые фичи!)
setting_col1, setting_col2 = st.columns(2)

with setting_col1:
    video_quality = st.selectbox(
        "🎬 Качество видео (MP4):", 
        ["1080p (Full HD)", "720p (HD)", "480p (Эконом)"]
    )

with setting_col2:
    audio_quality = st.selectbox(
        "🎛️ Качество звука (MP3):", 
        ["320 kbps (Премиум)", "192 kbps (Хорошее)"]
    )

# Настройка битрейта для аудио
bitrate = "320" if "320" in audio_quality else "192"

# Настройка формата для видео на основе выбора пользователя
if "1080p" in video_quality:
    video_format = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best"
elif "720p" in video_quality:
    video_format = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best"
else:
    video_format = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best"

# Кнопки действия
col1, col2 = st.columns(2)

if link:
    # 🎥 КНОПКА СКАЧАТЬ ВИДЕО
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Загрузка видео..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': video_format, # Используем выбранное качество!
                            'noplaylist': True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        with open(filename, "rb") as f:
                            st.success(f"✨ Видео ({video_quality}) готово!")
                            st.download_button(
                                label="📥 Сохранить на устройство",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при скачивании видео: {e}")

    # 🎶 КНОПКА СКАЧАТЬ ЗВУК
    with col2:
        if st.button("🎶 Скачать MP3 Звук", use_container_width=True):
            with st.spinner("🎵 Извлечение аудио..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': 'bestaudio/best',
                            'noplaylist': True,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': bitrate,
                            }],
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                            base, _ = os.path.splitext(filename)
                            mp3_filename = base + ".mp3"
                        
                        with open(mp3_filename, "rb") as f:
                            st.balloons()
                            st.success(f"✨ Звук ({audio_quality}) извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при извлечении аудио: {e}")

# Подвал сайта
st.markdown("---")
st.markdown("<p style='text-align: center;'>👨‍💻 Разработано молодым программистом</p>", unsafe_allowed_html=True)

st.markdown("""
    <div style='text-align: center;'>
        <a href='#' target='_blank'>
            <button style='background: linear-gradient(45deg, #ff4b4b, #ff7676); color: white; border: none; border-radius: 10px; padding: 12px 20px; cursor: pointer; font-weight: bold;'>
                ❤️ Поддержать автора (Донат)
            </button>
        </a>
    </div>
""", unsafe_allowed_html=True)
