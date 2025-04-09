
# 🎬 YouTube Video Downloader

A simple web app built with Django and Bootstrap that lets users download YouTube videos directly to their device using `yt-dlp`.

## 🚀 Features

- Paste any YouTube video URL and download instantly
- Uses `yt-dlp` for faster and reliable downloading
- Clean and responsive UI with Bootstrap 5
- Downloads video directly to user's system (not stored on server)

---

## 🛠️ Tech Stack

- 🐍 Django (Backend)
- 🎞 yt-dlp (Video download engine)
- 🎨 Bootstrap 5 (Frontend UI)

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Create and activate virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## ✅ Dependencies

Add this to your `requirements.txt`:

```
Django>=4.0
yt-dlp
```

Install `yt-dlp` CLI (if needed):
```bash
pip install yt-dlp
```

---

## 📁 Project Structure

```
YT-Download/
│
├── App/
│   ├── views.py                  # yt-dlp integration
│   ├── forms.py                  # URL input form
│   └── ...
│
├── yt_downloader/
│   └── settings.py
├── templates/
│   └── index.html
│   └── base.html
│   └── download.html
├── manage.py
└── requirements.txt
```


