import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(
    page_title="Media & Game Космо-Комбайн v6.1", 
    page_icon="🎮", 
    layout="centered"
)

st.title("🌌 Media & Game Космо-Комбайн v6.1")

# Создаем 3 вкладки сверху сайта (Медиа + Игры!)
tab_link, tab_file, tab_games = st.tabs(["🔗 Скачать по ссылке", "📂 Конвертер файлов", "🎮 Игровая зона"])

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ =================
with tab_link:
    st.write("Качайте видео, музыку и фото из Pinterest, YouTube, TikTok, VK и Instagram!")
    link = st.text_input("Вставьте вашу ссылку сюда:", placeholder="https://...", key="link_input")

    if link:
        st.markdown("---")
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

        ydl_opts_base = {
            'noplaylist': True, 'quiet': True, 'no_check_certificate': True,
            'extractor_args': {'youtube': ['player_client=android,web;player_skip=webpage_download']},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }
        }

        with st.spinner("🔍 Умный анализ медиа..."):
            try:
                with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                    info = ydl.extract_info(link, download=False)
                    video_title = info.get('title', 'Медиа файл')
                    thumbnail_url = info.get('thumbnail', None)
                    direct_video_url = None
                    if 'formats' in info:
                        for f in info['formats']:
                            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                                direct_video_url = f['url']
                                break

                st.subheader(f"📝 {video_title}")
                if thumbnail_url:
                    st.image(thumbnail_url, use_container_width=True)
                if direct_video_url and (direct_video_url != thumbnail_url):
                    st.video(direct_video_url)

            except Exception:
                st.error("Предупреждение: Онлайн-превью защищено, но вы можете скачать файл кнопками ниже!")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎥 Скачать MP4 Видео", use_container_width=True, key="btn_mp4_link"):
                with st.spinner("🚀 Скачивание..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': 'best[ext=mp4]/best'})
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                            with open(filename, "rb") as f:
                                st.download_button("📥 Сохранить MP4 файл", f.read(), file_name=os.path.basename(filename), mime="video/mp4", use_container_width=True)
                    except Exception: st.error("Ошибка скачивания.")
        with col2:
            if st.button("🎶 Скачать MP3 Звук", use_container_width=True, key="btn_mp3_link"):
                with st.spinner("🎵 Извлечение звука..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]})
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                                base, _ = os.path.splitext(filename)
                                mp3_filename = base + ".mp3"
                            with open(mp3_filename, "rb") as f:
                                st.balloons()
                                st.download_button("📥 Сохранить MP3 файл", f.read(), file_name=os.path.basename(mp3_filename), mime="audio/mp3", use_container_width=True)
                    except Exception: st.error("Ошибка аудио.")

# ================= ВКЛАДКА 2: ЧИСТЫЙ КОНВЕРТЕР ФАЙЛОВ ИЗ ГАЛЕРЕИ =================
with tab_file:
    st.write("📁 Загрузите видео со своего устройства, чтобы мгновенно извлечь из него аудиодорожку!")
    uploaded_file = st.file_uploader("Выберите видеофайл из галереи ноутбука или телефона", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.success(f"🎬 Файл '{uploaded_file.name}' успешно загружен!")
        
        if st.button("🎵 Превратить в MP3", use_container_width=True):
            with st.spinner("✂️ Извлекаю аудио..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                        t_video.write(uploaded_file.read())
                        video_path = t_video.name
                    
                    audio_path = video_path.replace(".mp4", ".mp3")
                    
                    # Легкая и надежная конвертация через встроенный FFmpeg
                    os.system(f'ffmpeg -i "{video_path}" -vn -ar 44100 -ac 2 -b:a 192k "{audio_path}" -y')
                    
                    with open(audio_path, "rb") as f:
                        st.balloons()
                        st.download_button("📥 Скачать готовый MP3 аудиофайл", f.read(), file_name=os.path.splitext(uploaded_file.name) + ".mp3", mime="audio/mp3", use_container_width=True)
                    
                    os.remove(video_path)
                    os.remove(audio_path)
                except Exception as e:
                    st.error(f"Ошибка конвертации: {e}")

# ================= ВКЛАДКА 3: ИГРОВАЯ ЗОНА С ДРУЗЬЯМИ =================
with tab_games:
    st.subheader("🎮 Настольные мини-игры для двоих")
    game_choice = st.radio("Выберите игру, чтобы играть с другом прямо сейчас:", ["🔴 2D Шашки", "♟️ Шахматы"])

    if game_choice == "🔴 2D Шашки":
        st.write("### Игровое поле: Шашки (Ходите по очереди с другом)")
        st.components.v1.iframe("https://html5games.com", height=500, scrolling=False)
        
    elif game_choice == "♟️ Шахматы":
        st.write("### Игровое поле: Шахматы (Битва умов)")
        st.components.v1.iframe("https://html5games.com", height=500, scrolling=False)
