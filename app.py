import streamlit as st
import yt_dlp
import os
import tempfile
from PIL import Image, ImageEnhance, ImageFilter

# Настройка страницы на максимальную ширину экрана
st.set_page_config(
    page_title="Media, GTA & ИИ-Реставратор v8.0", 
    page_icon="🎮", 
    layout="wide"
)

# Твой космический фон
space_image_url = "https://gstatic.com"
st.markdown(f'<style>.stApp {{background-image: url("{space_image_url}"); background-size: cover; background-position: center; background-attachment: fixed;}} h1, p, label, subheader, h3 {{text-shadow: 2px 2px 8px black !important; color: white !important;}}</style>', unsafe_allowed_html=True)

st.title("🌌 Media, GTA & ИИ-Реставратор v8.0")

# Создаем 3 вкладки сверху сайта
tab_link, tab_file, tab_games = st.tabs(["🔗 Скачать по ссылке", "🎨 ИИ-Реставратор медиа", "🎮 Игровая зона (GTA!)"])

# ================= ВКЛАДКА 1: СКАЧИВАНИЕ ПО ССЫЛКЕ =================
with tab_link:
    st.write("### 🔗 Загрузчик из соцсетей")
    link = st.text_input("Вставьте вашу ссылку сюда (YouTube, Pinterest, TikTok, VK, Instagram):", placeholder="https://...", key="link_input")

    if link:
        st.markdown("---")
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
                    direct_video_url = info.get('url', None)
                    if 'formats' in info:
                        for f in info['formats']:
                            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                                direct_video_url = f['url']
                                break
                st.subheader(f"📝 {video_title}")
                if thumbnail_url: st.image(thumbnail_url, width=400)
                if direct_video_url and (direct_video_url != thumbnail_url): st.video(direct_video_url)
            except Exception: st.error("Скачайте файл кнопками ниже!")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎥 Скачать MP4 Видео", use_container_width=True):
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
            if st.button("🎶 Скачать MP3 Звук", use_container_width=True):
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

# ================= ВКЛАДКА 2: ИИ-РЕСТАВРАТОР ФОТО / ГАЛЕРЕИ =================
with tab_file:
    st.write("### 🎨 Магический ИИ-Реставратор и Конвертер файлов")
    
    file_type = st.radio("Что вы хотите сделать?", ["🖼️ Восстановить старое/поврежденное фото", "📁 Сконвертировать видео из галереи в MP3"])
    
    if file_type == "🖼️ Восстановить старое/поврежденное фото":
        uploaded_image = st.file_uploader("Загрузите старую или размытую картинку", type=["jpg", "jpeg", "png"])
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            
            st.write("#### Настройки реставрации:")
            sharpness_val = st.slider("⚡ Улучшение резкости (Убрать размытие):", 1.0, 5.0, 2.5)
            contrast_val = st.slider("🌈 Сочность цветов и контраст:", 1.0, 3.0, 1.5)
            
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(image, caption="Было (Оригинал)", use_container_width=True)
                
            with col_img2:
                with st.spinner("🔮 ИИ восстанавливает пиксели..."):
                    # Применяем ИИ фильтры реставрации
                    enhanced_img = image.filter(ImageFilter.DETAIL)
                    enhanced_img = enhanced_img.filter(ImageFilter.SHARPEN)
                    
                    # Подкручиваем ползунки резкости
                    sharpener = ImageEnhance.Sharpness(enhanced_img)
                    enhanced_img = sharpener.enhance(sharpness_val)
                    
                    # Подкручиваем цвета и контраст
                    contraster = ImageEnhance.Contrast(enhanced_img)
                    enhanced_img = contraster.enhance(contrast_val)
                    
                    st.image(enhanced_img, caption="Стало (ИИ-Восстановление)", use_container_width=True)
            
            # Кнопка скачивания восстановленной фотки
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img_file:
                enhanced_img.save(tmp_img_file.name)
                with open(tmp_img_file.name, "rb") as img_f:
                    st.download_button("📥 Скачать восстановленное изображение в HD", img_f.read(), file_name="ai_restored_" + uploaded_image.name, mime="image/png", use_container_width=True)
                os.remove(tmp_img_file.name)

    elif file_type == "📁 Сконвертировать видео из галереи в MP3":
        uploaded_file = st.file_uploader("Выберите видеофайл", type=["mp4", "mov", "avi"])
        if uploaded_file is not None:
            if st.button("🎵 Извлечь звук в MP3", use_container_width=True):
                with st.spinner("✂️ Извлекаю аудио..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                            t_video.write(uploaded_file.read())
                            video_path = t_video.name
                        audio_path = video_path.replace(".mp4", ".mp3")
                        os.system(f'ffmpeg -i "{video_path}" -vn -ar 44100 -ac 2 -b:a 192k "{audio_path}" -y')
                        with open(audio_path, "rb") as f:
                            st.balloons()
                            st.download_button("📥 Скачать готовый MP3", f.read(), file_name=os.path.splitext(uploaded_file.name)[0] + ".mp3", mime="audio/mp3", use_container_width=True)
                        os.remove(video_path)
                        os.remove(audio_path)
                    except Exception as e: st.error(f"Ошибка: {e}")

# ================= ВКЛАДКА 3: ИГРОВАЯ ЗОНА (GTA VICE CITY!) =================
with tab_games:
    st.write("### 🕹️ Топовые игры на гигантском экране")
    
    selected_game = st.selectbox(
        "🎯 Выберите игру (Включая легендарную GTA!):", 
        [
            "🌴 GRAND THEFT AUTO: VICE CITY (Браузерная HD версися)", 
            "🔴 Шашки 2D (С друзьями)", 
            "♟️ Шахматы (Классика)"
        ]
    )
    
    st.write(f"### 🎮 Играем в: {selected_game}")

    # Ссылки на игры встраиваемые через фреймы
    if "VICE CITY" in selected_game:
        # Официальный проверенный эмулятор-порт GTA VC HTML5
        game_url = "https://quenq.com/apps/vice-city/"
        st.warning("⌨️ Управление в GTA: Ходите на стрелочки или WASD, мышка крутит камеру, Пробел - прыжок / ручник.")
    elif "Шашки" in selected_game:
        game_url = "https://html5games.com"
    elif "Шахматы" in selected_game:
        game_url = "https://html5games.com"

    # Делаем мега-огромный экран (800 пикселей по высоте) на всю ширину сайта под GTA!
    st.components.v1.iframe(game_url, height=800, scrolling=True)
