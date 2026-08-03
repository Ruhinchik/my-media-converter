import streamlit as st
import yt_dlp
import os
import tempfile

# Настройка внешнего вида сайта
st.set_page_config(page_title="Media Downloader & Converter", page_icon="📥", layout="centered")

st.title("📥 Скачивание и конвертация медиа")
st.write("Вставьте ссылку из Instagram Reels, YouTube или VK, чтобы скачать файл!")

# Поле для ввода ссылки
link = st.text_input("Вставьте ссылку на видео сюда:", placeholder="https://instagram.com...")

# Создаем две кнопки в один ряд
col1, col2 = st.columns(2)

if link:
    # 🎥 КНОПКА СКАЧАТЬ ВИДЕО (MP4)
    with col1:
        if st.button("🎥 Скачать как MP4 (Видео)", use_container_width=True):
            with st.spinner("Загрузка видео... Пожалуйста, подождите"):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': 'best[ext=mp4]/best', # Ищем формат MP4
                            'noplaylist': True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        # Читаем файл для выдачи пользователю
                        with open(filename, "rb") as f:
                            st.success("Видео готово!")
                            st.download_button(
                                label="📥 Сохранить Видео на ноутбук/телефон",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при скачивании видео: {e}")

    # 🎶 КНОПКА СКАЧАТЬ ЗВУК (MP3)
    with col2:
        if st.button("🎶 Скачать как MP3 (Звук)", use_container_width=True):
            with st.spinner("Извлечение аудиодорожки... Подождите"):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                            'format': 'bestaudio/best',
                            'noplaylist': True,
                            # Инструкция для yt-dlp: вырезать звук встроенными силами
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                            
                            # После обработки расширение файла меняется на .mp3 автоматически
                            base, _ = os.path.splitext(filename)
                            mp3_filename = base + ".mp3"
                        
                        # Читаем музыку для выдачи
                        with open(mp3_filename, "rb") as f:
                            st.balloons() # Праздничные шары при успехе!
                            st.success("Звук успешно извлечен!")
                            st.download_button(
                                label="📥 Сохранить MP3 на устройство",
                                data=f.read(),
                                file_name=os.path.basename(mp3_filename),
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Ошибка при создании MP3: {e}")

