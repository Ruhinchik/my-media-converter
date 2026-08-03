import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка страницы
st.set_page_config(page_title="Media Mega Комбайн v3.0", page_icon="🚀", layout="centered")

st.title("🚀 Media Mega Комбайн v3.0")
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

    # Получаем информацию о видео без его скачивания (для обложки и плеера)
    with st.spinner("🔍 Анализирую ссылку и ищу обложку..."):
        try:
            ydl_opts_info = {'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(link, download=False)
                
                video_title = info.get('title', 'Медиа файл')
                thumbnail_url = info.get('thumbnail', None)
                direct_video_url = info.get('url', None) # Прямая ссылка для плеера

            st.subheader(f"📝 {video_title}")

            # ================= 3. СКАЧИВАНИЕ ОБЛОЖЕК И ФОТО (ПРЕВЬЮ) =================
            if thumbnail_url:
                st.image(thumbnail_url, caption="📸 Обложка (Превью) вашего видео", use_container_width=True)
                # Даем ссылку, чтобы пользователь мог просто сохранить картинку
                st.markdown(f"""
                    <div style='text-align: center; margin-bottom: 20px;'>
                        <a href='{thumbnail_url}' target='_blank'>
                            <button style='background-color: #2b2b2b; color: white; border: 1px solid #444; border-radius: 8px; padding: 8px 12px; cursor: pointer; font-weight: bold;'>
                                🖼️ Открыть и скачать обложку в HD
                            </button>
                        </a>
                    </div>
                """, unsafe_allowed_html=True)

            # ================= 1. ВСТРОЕННЫЙ МЕДИАПЛЕЕР =================
            st.subheader("📺 Посмотреть / Послушать прямо на сайте:")
            if direct_video_url:
                # Встраиваем видеоплеер. Если это аудио, Streamlit автоматически сделает удобный плеер без картинки
                st.video(direct_video_url)
            else:
                st.warning("⚠️ Не удалось запустить онлайн-плеер для этого сайта, но вы все еще можете скачать файл ниже!")

        except Exception as e:
            st.error(f"Не удалось получить превью. Возможно, аккаунт приватный. Ошибка: {e}")

    # ================= БЛОК ДЛЯ СКАЧИВАНИЯ ФАЙЛОВ =================
    st.markdown("---")
    st.subheader("📥 Выберите формат для скачивания на устройство:")
    
    # Настройки качества
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

    # Кнопка MP4
    with col1:
        if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
            with st.spinner("🚀 Загрузка видео на сервер..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': video_format,
                            'noplaylist': True,
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

    # Кнопка MP3
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
