import streamlit as st
import yt_dlp
import os
import tempfile
import moviepy.editor as mp

# Настройка страницы
st.set_page_config(
    page_title="Media Mega Комбайн v5.0", 
    page_icon="🚀", 
    layout="centered"
)

st.title("🚀 Media Mega Комбайн v5.0")

# Создаем две удобные вкладки сверху сайта
tab_link, tab_file = st.tabs(["🔗 Скачать по ссылке", "📂 Загрузить из Галереи"])

# Ссылка на космический фон для красоты
space_image_url = "https://gstatic.com"

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ =================
with tab_link:
    st.write("Качайте видео, музыку и фото из Pinterest, YouTube, TikTok, VK и Instagram!")
    link = st.text_input("Вставьте вашу ссылку сюда:", placeholder="https://...", key="link_input")

    if not link:
        st.markdown("---")
        st.image(space_image_url, use_container_width=True, caption="Вставьте ссылку выше, чтобы начать")

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
                    if not direct_video_url:
                        direct_video_url = info.get('url', None)

                st.subheader(f"📝 {video_title}")
                if thumbnail_url:
                    st.image(thumbnail_url, use_container_width=True)
                    st.link_button("🖼️ Открыть картинку в HD", thumbnail_url, use_container_width=True)
                if direct_video_url and (direct_video_url != thumbnail_url):
                    st.video(direct_video_url)

            except Exception as e:
                st.error("Не удалось загрузить онлайн-превью. Используйте кнопки скачивания ниже!")

        # Кнопки скачивания для ссылок
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
                                st.success("✨ Видео готово!")
                                st.download_button("📥 Сохранить MP4 на устройство", f.read(), file_name=os.path.basename(filename), mime="video/mp4", use_container_width=True)
                    except Exception: st.error("Ошибка при скачивании.")
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
                                st.download_button("📥 Сохранить MP3 на устройство", f.read(), file_name=os.path.basename(mp3_filename), mime="audio/mp3", use_container_width=True)
                    except Exception: st.error("Ошибка при извлечении аудио.")

# ================= ВКЛАДКА 2: РАБОТА С ФАЙЛАМИ ИЗ ГАЛЕРЕИ =================
with tab_file:
    st.write("📁 Загрузите видео со своего устройства, чтобы извлечь звук или улучшить его!")
    
    # Кнопка загрузки файла из галереи
    uploaded_file = st.file_uploader("Выберите видеофайл из галереи", type=["mp4", "mov", "avi", "mkv"])

    if not uploaded_file:
        st.image(space_image_url, use_container_width=True, caption="Загрузите видео с ноутбука или телефона")

    if uploaded_file is not None:
        st.success(f"🎬 Файл '{uploaded_file.name}' успешно загружен!")
        
        # Дополнительная фича: Галочка для реставрации (Улучшайзер цвета!)
        enhance = st.checkbox("🪄 Включить 'Ретро-Улучшайзер' (Сделать старое видео 2012 года ярче и четче)")

        col_f1, col_f2 = st.columns(2)

        with col_f1:
            if st.button("🎵 Вырезать звук (В MP3)", use_container_width=True):
                with st.spinner("✂️ Извлекаю аудиодорожку из твоего файла..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                            t_video.write(uploaded_file.read())
                            video_path = t_video.name
                        
                        audio_path = video_path.replace(".mp4", ".mp3")
                        
                        # Конвертация через moviepy
                        video = mp.VideoFileClip(video_path)
                        video.audio.write_audiofile(audio_path, logger=None)
                        video.close()

                        with open(audio_path, "rb") as f:
                            st.balloons()
                            st.download_button("📥 Скачать готовый MP3", f.read(), file_name=os.path.splitext(uploaded_file.name)[0] + ".mp3", mime="audio/mp3", use_container_width=True)
                        
                        os.remove(video_path)
                        os.remove(audio_path)
                    except Exception as e: st.error(f"Ошибка конвертации: {e}")

        with col_f2:
            if st.button("✨ Обработать видео (MP4)", use_container_width=True):
                with st.spinner("🪄 Магия реставрации в процессе..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                            t_video.write(uploaded_file.read())
                            video_path = t_video.name
                        
                        output_video_path = video_path.replace(".mp4", "_enhanced.mp4")
                        
                        # Делаем реставрацию старого видео через MoviePy
                        clip = mp.VideoFileClip(video_path)
                        
                        if enhance:
                            # Увеличиваем контрастность и яркость для старых видео
                            clip = clip.fx(mp.vfx.colorx, 1.2) # Делаем цвета сочнее на 20%
                            clip = clip.fx(mp.vfx.lum_contrast, 10, 20, 128) # Подтягиваем контраст
                        
                        # Сохраняем обновленный файл
                        clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac", logger=None)
                        clip.close()

                        with open(output_video_path, "rb") as f:
                            st.success("🔮 Ретро-видео успешно обработано!")
                            st.download_button("📥 Скачать улучшенное видео", f.read(), file_name="enhanced_" + uploaded_file.name, mime="video/mp4", use_container_width=True)
                        
                        os.remove(video_path)
                        os.remove(output_video_path)
                    except Exception as e: st.error(f"Ошибка улучшения: {e}")

# Подвал
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом | Версия 5.0")
