import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(
    page_title="Media Mega Комбайн v3.5", 
    page_icon="🚀", 
    layout="centered"
)

# Твой красивый баннер со звуковой волной вверху
banner_url = "https://squarespace-cdn.com"
st.image(banner_url, use_container_width=True)

st.title("🚀 Media Mega Комбайн v3.5")
st.write("Скачивайте, слушайте и смотрите медиа со всех соцсетей в один клик!")

# Поле ввода ссылки
link = st.text_input("🔗 Вставьте вашу ссылку сюда (Instagram, YouTube, TikTok, VK):", placeholder="https://...")

if link:
    st.markdown("---")
    
    # Умный определитель
    link_lower = link.lower()
    if "instagram.com" in link_lower:
        st.info("📸 **Обнаружена ссылка из Instagram!**")
    elif "youtube.com" in link_lower or "youtu.be" in link_lower:
        st.success("📺 **Обнаружена ссылка из YouTube!**")
    elif "tiktok.com" in link_lower:
        st.warning("🎵 **Обнаружена ссылка из TikTok!**")
    elif "vk.com" in link_lower:
        st.error("🔵 **Обнаружена ссылка из ВКонтакте!**")

    # Мощные настройки для обхода блокировок 403 Forbidden
    ydl_opts_base = {
        'noplaylist': True,
        'quiet': True,
        'no_check_certificate': True,
        'extracted_flat': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    with st.spinner("🔍 Умный анализ ссылки..."):
        try:
            with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                info = ydl.extract_info(link, download=False)
                video_title = info.get('title', 'Медиа файл')
                thumbnail_url = info.get('thumbnail', None)
                direct_video_url = info.get('url', None)

            st.subheader(f"📝 {video_title}")

            if thumbnail_url:
                st.image(thumbnail_url, caption="📸 Обложка вашего видео", use_container_width=True)
                st.link_button("🖼️ Открыть обложку в HD", thumbnail_url, use_container_width=True)

            st.subheader("📺 Посмотреть / Послушать прямо на сайте:")
            if direct_video_url:
                st.video(direct_video_url)
            else:
                st.warning("⚠️ Онлайн-плеер недоступен, но файл можно скачать кнопками ниже!")

        except Exception as e:
            st.error("Не удалось загрузить онлайн-превью. Но вы можете попробовать скачать файл кнопками ниже!")

    # Блок скачивания
    st.markdown("---")
    st.subheader("📥 Выберите формат для скачивания на устройство:")
    
    setting_col1, setting_col2 = st.columns(2)
    with setting_col1:
        video_quality = st.selectbox("🎬 Видео (MP4):", ["1080p (Full HD)", "720p (HD)", "480p (Эконом)"])
    with setting_col2:
        audio_quality = st.selectbox("🎛️ Звук (MP3):", ["320 kbps (Премиум)", "192 kbps (Хорошее)"])

    bitrate = "320" if "320" in audio_quality else "192"
    
    if "1080p" in video_quality:
        video_format = "best[height<=1080][ext=mp4]/best"
    elif "720p" in video_quality:
        video_format = "best[height<=720][ext=mp4]/best"
    else:
        video_format = "best[height<=480][ext=mp4]/best"

    col1, col2 = st.columns(2)

    # Кнопка MP4
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Скачивание видео..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = ydl_opts_base.copy()
                        ydl_opts.update({
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': video_format,
                        })
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        with open(filename, "rb") as f:
                            st.success("✨ Видео готово!")
                            st.download_button(
                                label="📥 Сохранить MP4 файл",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при скачивании. Попробуйте другую ссылку.")

    # Кнопка MP3
    with col2:
        if st.button("🎶 Скачать MP3 Звук", use_container_width=True):
            with st.spinner("🎵 Извлечение звука..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = ydl_opts_base.copy()
                        ydl_opts.update({
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': bitrate,
                            }],
                        })
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                            base, _ = os.path.splitext(filename)
                            mp3_filename = base + ".mp3"
                        
                        with open(mp3_filename, "rb") as f:
                            st.balloons()
                            st.success("✨ Звук извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3 файл",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при извлечении аудио. Попробуйте другую ссылку.")

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом")
