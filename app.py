import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(
    page_title="Media Mega Комбайн v3.6", 
    page_icon="🚀", 
    layout="centered"
)

# Твой красивый баннер со звуковой волной вверху
banner_url = "https://squarespace-cdn.com"
st.image(banner_url, use_container_width=True)

st.title("🚀 Media Mega Комбайн v3.6")
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

    # СВЕРХМОЩНЫЕ НАСТРОЙКИ ДЛЯ ОБХОДА БЛОКИРОВОК СОЦСЕТЕЙ
    ydl_opts_base = {
        'noplaylist': True,
        'quiet': True,
        'no_check_certificate': True,
        'extractor_args': {
            'youtube': ['player_client=android,web;player_skip=webpage_download'] # Имитируем вход с андроид-смартфона
        },
        'http_colors': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    }

    with st.spinner("🔍 Умный анализ ссылки..."):
        try:
            with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                info = ydl.extract_info(link, download=False)
                video_title = info.get('title', 'Медиа файл')
                thumbnail_url = info.get('thumbnail', None)
                
                # Ищем прямую ссылку на медиапоток
                direct_video_url = None
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                            direct_video_url = f['url']
                            break
                if not direct_video_url:
                    direct_video_url = info.get('url', None)

            st.subheader(f"📝 {video_title}")

            if thumbnail_url:
                st.image(thumbnail_url, caption="📸 Обложка вашего видео", use_container_width=True)
                st.link_button("🖼️ Открыть обложку в HD", thumbnail_url, use_container_width=True)

            st.subheader("📺 Посмотреть / Послушать прямо на сайте:")
            if direct_video_url:
                st.video(direct_video_url)
            else:
                st.warning("⚠️ Онлайн-плеер недоступен из-за защиты сайта, но файл можно скачать кнопками ниже!")

        except Exception as e:
            st.error("Не удалось загрузить онлайн-превью из-за защиты соцсети. Но вы можете попробовать скачать файл кнопками ниже!")

    # Блок скачивания
    st.markdown("---")
    st.subheader("📥 Выберите формат для скачивания на устройство:")
    
    setting_col1, setting_col2 = st.columns(2)
    with setting_col1:
        video_quality = st.selectbox("🎬 Видео (MP4):", ["1080p (Full HD)", "720p (HD)", "480p (Эконом)"])
    with setting_col2:
        audio_quality = st.selectbox("🎛️ Звук (MP3):", ["320 kbps (Премиум)", "192 kbps (Хорошее)"])

    bitrate = "320" if "320" in audio_quality else "192"
    
    # Для облачных серверов лучше всего запрашивать готовые форматы MP4, чтобы не вызывать ошибку 403
    video_format = "best[ext=mp4]/best"

    col1, col2 = st.columns(2)

    # Кнопка MP4
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Скачивание видео..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = ydl_opts_base.copy()
                        ydl_opts.update({
                            'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s',
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
                    st.error(f"Ошибка блокировки соцсети. Попробуйте другую ссылку (например, из Shorts или VK).")

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
                            st.success("✨ Звук извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3 файл",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Не удалось вырезать звук. Соцсеть заблокировала облачный сервер. Попробуйте Shorts/TikTok ссылку.")

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом")
