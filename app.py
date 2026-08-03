import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(page_title="Media Mega Комбайн v3.1", page_icon="🚀", layout="centered")

st.title("🚀 Media Mega Комбайн v3.1")
st.write("Скачивайте, слушайте и смотрите медиа со всех соцсетей в один клик!")

# Поле ввода ссылки
link = st.text_input("🔗 Вставьте вашу ссылку сюда (Instagram, YouTube, TikTok, VK):", placeholder="https://...")

if link:
    st.markdown("---")
    
    # ================= 5. УМНЫЙ ОПРЕДЕЛИТЕЛЬ ССЫЛОК + ИКОНКИ =================
    link_lower = link.lower()
    if "instagram.com" in link_lower:
        st.info("📸 **Обнаружена ссылка из Instagram!** Готовлюсь извлечь Reels/Видео.")
    elif "youtube.com" in link_lower or "youtu.be" in link_lower:
        st.success("📺 **Обнаружена ссылка из YouTube!** Готовлюсь извлечь ролик/клип.")
    elif "tiktok.com" in link_lower:
        st.warning("🎵 **Обнаружена ссылка из TikTok!** Готовлюсь извлечь тренд.")
    elif "vk.com" in link_lower:
        st.error("🔵 **Обнаружена ссылка из ВКонтакте!** Готовлюсь извлечь видео/клип.")
    else:
        st.subheader("🔗 **Обнаружена ссылка!** Пытаюсь распознать сайт...")

    # Получаем информацию о видео с защитой от блокировок (User-Agent)
    # Это решает проблему с ошибкой HTTP Error 403: Forbidden
    ydl_opts_info = {
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    with st.spinner("🔍 Анализирую ссылку и ищу обложку..."):
        try:
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(link, download=False)
                
                video_title = info.get('title', 'Медиа файл')
                thumbnail_url = info.get('thumbnail', None)
                direct_video_url = info.get('url', None)

            st.subheader(f"📝 {video_title}")

            # ================= 3. СКАЧИВАНИЕ ОБЛОЖЕК И ФОТО (ПРЕВЬЮ) =================
            if thumbnail_url:
                st.image(thumbnail_url, caption="📸 Обложка (Превью) вашего видео", use_container_width=True)
                # Безопасная кнопка-ссылка без использования опасного HTML кода
                st.link_button("🖼️ Открыть и скачать обложку в HD", thumbnail_url, use_container_width=True)

            # ================= 1. ВСТРОЕННЫЙ МЕДИАПЛЕЕР =================
            st.subheader("📺 Посмотреть / Послушать прямо на сайте:")
            if direct_video_url:
                st.video(direct_video_url)
            else:
                st.warning("⚠️ Не удалось запустить онлайн-плеер для этого сайта, но вы все еще можете скачать файл ниже!")

        except Exception as e:
            st.error(f"Не удалось загрузить превью. Попробуйте скачать файл кнопками ниже. Ошибка: {e}")

    # ================= БЛОК ДЛЯ СКАЧИВАНИЯ ФАЙЛОВ =================
    st.markdown("---")
    st.subheader("📥 Выберите формат для скачивания на устройство:")
    
    setting_col1, setting_col2 = st.columns(2)
    with setting_col1:
        video_quality = st.selectbox("🎬 Видео (MP4):", ["1080p (Full HD)", "720p (HD)", "480p (Эконом)"])
    with setting_col2:
        audio_quality = st.selectbox("🎛️ Звук (MP3):", ["320 kbps (Премиум)", "192 kbps (Хорошее)"])

    bitrate = "320" if "320" in audio_quality else "192"
    if "1080p" in video_quality:
        video_format = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best"
    elif "720p" in video_quality:
        video_format = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best"
    else:
        video_format = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best"

    col1, col2 = st.columns(2)

    # Кнопка MP4 с защитой User-Agent
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Загрузка видео на сервер..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': video_format,
                            'noplaylist': True,
                            'http_headers': ydl_opts_info['http_headers']
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        with open(filename, "rb") as f:
                            st.success("✨ Видео готово!")
                            st.download_button(
                                label="📥 Сохранить MP4 на устройство",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при скачивании видео: {e}")

    # Кнопка MP3 с защитой User-Agent
    with col2:
        if st.button("🎶 Скачать MP3 Звук", use_container_width=True):
            with st.spinner("🎵 Извлечение аудио..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': 'bestaudio/best',
                            'noplaylist': True,
                            'http_headers': ydl_opts_info['http_headers'],
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
                            st.success("✨ Звук извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3 на устройство",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при извлечении аудио: {e}")

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом")
