import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(
    page_title="Media Mega Комбайн v4.0", 
    page_icon="🚀", 
    layout="centered"
)

# === ТВОЙ КОСМИЧЕСКИЙ ФОН ===
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvqWJmFSWGztUB0uIlYNxqyJ1PgSKoQi84AEu_KsMF_A&s=10"

# Безопасная установка фона
st.markdown(f'<style>.stApp {{background-image: url("{IMAGE_URL}"); background-size: cover; background-position: center; background-attachment: fixed;}} h1, p, label, subheader, h3 {{text-shadow: 2px 2px 8px black !important; color: white !important;}} .stInfo, .stSuccess, .stWarning, .stError {{text-shadow: none !important;}}</style>', unsafe_allowed_html=True)

# Твой баннер со звуковой волной вверху
banner_url = "https://squarespace-cdn.com"
st.image(banner_url, use_container_width=True)

st.title("🚀 Media Mega Комбайн v4.0")
st.write("Скачивайте видео, музыку и фото из Pinterest, YouTube, TikTok, VK и Instagram!")

# Поле ввода ссылки
link = st.text_input("🔗 Вставьте вашу ссылку сюда:", placeholder="https://...")

if link:
    st.markdown("---")
    
    # ================= 5. УМНЫЙ ОПРЕДЕЛИТЕЛЬ ССЫЛОК С ПИНТЕРЕСТОМ =================
    link_lower = link.lower()
    if "pinterest.com" in link_lower or "pin.it" in link_lower:
        st.info("📌 **Обнаружена ссылка из Pinterest!** Извлекаю фото или видео.")
    elif "instagram.com" in link_lower:
        st.info("📸 **Обнаружена ссылка из Instagram!**")
    elif "youtube.com" in link_lower or "youtu.be" in link_lower:
        st.success("📺 **Обнаружена ссылка из YouTube!**")
    elif "tiktok.com" in link_lower:
        st.warning("🎵 **Обнаружена ссылка из TikTok!**")
    elif "vk.com" in link_lower:
        st.error("🔵 **Обнаружена ссылка из ВКонтакте!**")

    # Общие настройки для обхода блокировок
    ydl_opts_base = {
        'noplaylist': True,
        'quiet': True,
        'no_check_certificate': True,
        'extractor_args': {'youtube': ['player_client=android,web;player_skip=webpage_download']},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }

    with st.spinner("🔍 Умный анализ медиа..."):
        try:
            with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                info = ydl.extract_info(link, download=False)
                video_title = info.get('title', 'Медиа файл')
                thumbnail_url = info.get('thumbnail', None)
                
                # Проверяем, видео это или просто картинка (для Пинтереста)
                direct_video_url = None
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                            direct_video_url = f['url']
                            break
                if not direct_video_url:
                    direct_video_url = info.get('url', None)

            st.subheader(f"📝 {video_title}")

            # Показываем обложку/картинку
            if thumbnail_url:
                st.image(thumbnail_url, caption="📸 Найденное изображение / Обложка", use_container_width=True)
                st.link_button("🖼️ Открыть и сохранить картинку в HD", thumbnail_url, use_container_width=True)

            # Плеер отображается только если найдено реальное видео
            if direct_video_url and (direct_video_url != thumbnail_url):
                st.subheader("📺 Посмотреть видео прямо на сайте:")
                st.video(direct_video_url)

        except Exception as e:
            st.error("Не удалось загрузить онлайн-превью из-за защиты сайта. Но вы можете попробовать скачать файл кнопками ниже!")

    # Блок скачивания
    st.markdown("---")
    st.subheader("📥 Выберите формат для сохранения:")
    
    setting_col1, setting_col2 = st.columns(2)
    with setting_col1:
        video_quality = st.selectbox("🎬 Видео (MP4):", ["1080p (Full HD)", "720p (HD)", "480p (Эконом)"])
    with setting_col2:
        audio_quality = st.selectbox("🎛️ Звук (MP3):", ["320 kbps (Премиум)", "192 kbps (Хорошее)"])

    bitrate = "320" if "320" in audio_quality else "192"
    video_format = "best[ext=mp4]/best"

    col1, col2 = st.columns(2)

    # Кнопка MP4 (или скачивание видео из Пинтерест)
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Скачивание..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = ydl_opts_base.copy()
                        ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': video_format})
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        with open(filename, "rb") as f:
                            st.success("✨ Файл готов к сохранению!")
                            st.download_button(
                                label="📥 Сохранить MP4 на устройство",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error("Не удалось скачать видео. Попробуйте обновить страницу или вставить другую ссылку.")

    # Кнопка MP3
    with col2:
        if st.button("🎶 Скачать MP3 Звук", use_container_width=True):
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
                            st.success("✨ Звук успешно извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3 на устройство",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error("Не удалось извлечь аудиодорожку из этой ссылки.")

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом")
