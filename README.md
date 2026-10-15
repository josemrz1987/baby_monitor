# 👶🐾 AI Camera Baby & Pet Activity Monitor

A lightweight and robust computer vision system developed in **Python** for monitoring rooms, **babies**, or **pets** using IP cameras (compatible with Tapo cameras via RTSP). Its design is specifically focused on filtering out false positives (such as people casually walking across the room) to detect only **continuous, repetitive movements** (such as a baby waking up or an agitated pet), sending automated notifications via **Telegram**.

---

## 🚀 Key Features

* **Direct RTSP Connection:** Low-latency real-time streaming using `cv2.VideoCapture`.
* **Intelligent Background Subtraction:** Optimized implementation of **OpenCV MOG2** with history and median filtering to isolate real silhouettes.
* **Range-Specific Size Filter (`MIN_AREA_MOVIMIENTO` / `MAX_AREA_MOVIMIENTO`):** 
  * Ignores small objects (insects, lighting changes).
  * Discards massive passing movements (people walking across the room).
  * Focuses exclusively on localized, steady movements typical of restless pets or babies.
* **"Water Bucket" Persistence Algorithm:** A progressive integration system that evaluates movement consistency over time before triggering an alarm, preventing false alerts from isolated spikes.
* **Telegram Notifications:** Instant asynchronous alert delivery via the Telegram Bot API with built-in anti-spam protection.
* **Environment Security:** Credential and token loading using `python-dotenv` (the `.env` file is excluded from version control).