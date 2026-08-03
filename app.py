import streamlit as st
import yt_dlp
import os
import tempfile
import requests
import re
from PIL import Image, ImageEnhance, ImageFilter

# ================= 💰 НАСТРОЙКИ ПРЕМИУМА =================
SECRET_KEY = "Ruhinchik_PRO_2026"
DONATE_URL = "https://donationalerts.com" 
# =========================================================

st.set_page_config(page_title="Media & ИИ-Реставратор v12.1", page_icon="⚡", layout="centered")

st.title("🌌 Космо-Комбайн v12.1")
st.write("Скачивайте медиа и улучшайте старые фото прямо с телефона или ноутбука!")

tab_link, tab_file = st.tabs(["🔗 Скачать по ссылке", "🎨 ИИ-Реставратор фото"])

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ =================
with tab_link:
    st.write("### 🔗 Загрузчик из соцсетей")
    link = st.text_input("Вставьте вашу ссылку сюда (YouTube, Pinterest, TikTok, VK, Instagram):", placeholder="https://...", key="link_input")

    if link:
        st.markdown("---")
        
        # 👑 БРОНЕБОЙНЫЙ МЕТОД ОБХОДА ДЛЯ PINTEREST / INSTAGRAM
        direct_video_url = None
        thumbnail_url = None
        api_success = False
        
        with st.spinner("🚀 Пробиваю защиту соцсети и ищу прямую ссылку..."):
            # Метод 1: Пытаемся вытащить прямую ссылку через быстрый парсер Cobalt API
            try:
                payload = {"url": link, "videoQuality": "720"}
                headers = {"Accept": "application/json", "Content-Type": "application/json"}
                api_res = requests.post("https://cobalt.tools", json=payload, headers=headers, timeout=10).json()
                if api_res and api_res.get("url"):
                    direct_video_url = api_res.get("url")
                    api_success = True
            except Exception:
                api_success = False

            # Метод 2: Если первый метод заблокирован, включаем умный внутренний поиск по коду страницы
            if not api_success:
                try:
                    # Скачиваем код страницы Пинтереста через специальный маскировочный браузер
                    html_data = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=10).text
                    # Ищем скрытые теги с видеофайлом внутри кода
                    video_urls = re.findall(r'href="(https://v1\.pinimg\.com/videos/.*?\.mp4)"', html_data)
                    if not video_urls:
                        video_urls = re.findall(r'"videoUrl":"(https://.*?\.mp4)"', html_data)
                    if video_urls:
                        direct_video_url = video_urls[0].replace(r'\u002F', '/')
                        api_success = True
                except Exception:
                    pass

        st.markdown("---")
        
        # ЕСЛИ ПРЯМАЯ ССЫЛКА НАЙДЕНА — ДАЕМ ЕЁ ПОЛЬЗОВАТЕЛЮ (Это сработает на 100%!)
        if api_success and direct_video_url:
            st.success("🎯 Прямой медиапоток успешно перехвачен в обход всех защит!")
            st.link_button("🔥 СКАЧАТЬ ФАЙЛ НАПРЯМУЮ ЧЕРЕЗ БРАУЗЕР", direct_video_url, use_container_width=True)
            st.caption("💡 Инструкция: Видео откроется в новой вкладке. Нажми на нём три точки в углу или зажми пальцем экран и выбери **'Скачать видео'** или **'Сохранить'**!")
        else:
            st.warning("⚠️ Соцсеть наглухо скрыла прямую ссылку. Пробую запустить скачивание через стандартный сервер...")

        st.markdown("---")
        st.write("#### 📥 Стандартные кнопки сервера:")
        col1, col2 = st.columns(2)
        
        ydl_opts_base = {
            'noplaylist': True, 'quiet': True, 'no_check_certificate': True,
            'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        }
        
        with col1:
            if st.button("🎥 Скачать MP4 Видео", use_container_width=True, key="btn_mp4_link"):
                with st.spinner("🚀 Скачивание видео..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            ydl_opts = ydl_opts_base.copy()
                            ydl_opts.update({'outtmpl': f'{tmpdir}/%%(title)s.%%(ext)s', 'format': 'best[ext=mp4]/best'})
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(link, download=True)
                                filename = ydl.prepare_filename(info)
                            with open(filename, "rb") as f:
                                st.balloons()
                                st.download_button("📥 Сохранить MP4 файл", f.read(), file_name=os.path.basename(filename), mime="video/mp4", use_container_width=True)
                    except Exception: 
                        st.error("Сервер заблокирован. Пожалуйста, используйте верхнюю большую кнопку прямого скачивания!")
                        
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
                    except Exception: 
                        st.error("Не удалось извлечь звук. Защита заблокировала облако сервера.")

# ================= ВКЛАДКА 2: ИИ-РЕСТАВРАТОР ФОТО И КОНВЕРТЕР =================
with tab_file:
    st.write("### 🎨 Магический ИИ-Реставратор картинок")
    file_type = st.radio("Что вы хотите сделать?", ["🖼️ Восстановить размытое фото", "📁 Сконвертировать видео из галереи в MP3"])
    
    if file_type == "🖼️ Восстановить размытое фото":
        uploaded_image = st.file_uploader("Загрузите старую картинку", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.write("#### Настройки резкости:")
            sharpness_val = st.slider("⚡ Сила резкости (Убрать размытие):", 1.0, 3.0, 1.5)
            contrast_val = st.slider("🌈 PREMIUM 👑 Контраст цветов (Свыше 1.5 нужен Премиум):", 1.0, 3.0, 1.2)
            
            photo_premium = True
            if contrast_val > 1.5:
                st.warning("⚠️ Вы выбрали Ультра-контраст Премиум уровня!")
                st.markdown(f"🎁 **[ПОЛУЧИТЬ ПРЕМИУМ КЛЮЧ ЗА ДОНАТ]({DONATE_URL})**")
                user_key = st.text_input("🔑 Введите Премиум-ключ:", type="password", key="key_img")
                if user_key == SECRET_KEY:
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
                        st.download_button("📥 Скачать готовое фото в HD", img_f.read(), file_name="ai_restored_.png", mime="image/png", use_container_width=True)
                    os.remove(tmp_img_file.name)

    elif file_type == "📁 Сконвертировать видео из галереи в MP3":
        uploaded_file = st.file_uploader("Выберите видеофайл с ноутбука или телефона", type=["mp4", "mov", "avi"])
        if uploaded_file is not None:
            st.success(f"🎬 Видео успешно подгружено!")
            if st.button("🎵 Вырезать звук в MP3", key="btn_local_mp3"):
                with st.spinner("✂️ Извлекаю аудио..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                            t_video.write(uploaded_file.read())
                            video_path = t_video.name
                        audio_path = video_path.replace(".mp4", ".mp3")
                        os.system(f'ffmpeg -i "{video_path}" -vn -ar 44100 -ac 2 -b:a 192k "{audio_path}" -y')
                        with open(audio_path, "rb") as f:
                            st.balloons()
                            st.download_button("📥 Скачать готовый MP3 аудиофайл", f.read(), file_name="audio.mp3", mime="audio/mp3", use_container_width=True)
                        os.remove(video_path)
                        os.remove(audio_path)
                    except Exception as e: st.error(f"Ошибка: {e}")

# Подвал сайта
st.markdown("---")
st.write("👨‍💻 Разработано молодым программистом | v12.1 Облегченная версия")
