import cv2
import numpy as np
import requests
import os
from dotenv import load_dotenv

# Cargar las contraseñas ocultas del archivo .env
load_dotenv()

# --- CONFIGURACIÓN ---
USUARIO  = os.getenv("USUARIO")
PASSWORD = os.getenv("PASSWORD")
IP       = os.getenv("IP")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"Intentando conectar a: rtsp://{USUARIO}:***@{IP}:554/stream2")

# --- CALIBRACIÓN DEL "CUBO DE AGUA" ---
FPS = 15
SEGUNDOS_PARA_ALERTA = 10
CAPACIDAD_MAXIMA = SEGUNDOS_PARA_ALERTA * FPS
nivel_inquietud  = 0

MIN_AREA_MOVIMIENTO = 1500  
MAX_AREA_MOVIMIENTO = 12000  

# Variable ANTI-SPAM
alerta_enviada = False 

# --- CONEXIÓN A LA CÁMARA ---
rtsp_url = f"rtsp://{USUARIO}:{PASSWORD}@{IP}:554/stream2"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("❌ No se pudo conectar a la cámara.")
    exit()

print("✅ Cámara conectada. Iniciando monitor con Telegram...")

fgbg = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=50, detectShadows=False)

# --- 1. CONFIGURACIÓN DEL GRABADOR DE VÍDEO ---
# Obtenemos el ancho y alto real del streaming de la cámara
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Si por algún motivo la cámara no devuelve las dimensiones, ponemos un valor por defecto (ej. 640x360 o 1280x720)
if ancho == 0 or alto == 0:
    ancho, alto = 640, 360

# Definimos el códec (mp4v) y creamos el objeto VideoWriter (guardará un archivo llamado "prueba_monitor.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('prueba_monitor.mp4', fourcc, FPS, (ancho, alto))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mascara = fgbg.apply(frame)
    mascara = cv2.medianBlur(mascara, 5)
    pixeles_moviendo = cv2.countNonZero(mascara)

    # --- LÓGICA DEL CUBO DE AGUA ---
    if MIN_AREA_MOVIMIENTO < pixeles_moviendo < MAX_AREA_MOVIMIENTO:
        nivel_inquietud += 1   
    else:
        nivel_inquietud -= 2   

    nivel_inquietud = max(0, min(nivel_inquietud, CAPACIDAD_MAXIMA + (FPS * 5)))

    # --- SISTEMA DE ALERTA ---
    if nivel_inquietud >= CAPACIDAD_MAXIMA:
        estado = "ANOMALIA: Inquietud Constante ⚠️"
        color = (0, 0, 255) # Rojo
        
        if not alerta_enviada:
            print("Enviando alerta a Telegram...")
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            datos = {"chat_id": TELEGRAM_CHAT_ID, "text": "⚠️ ALERTA: ¡Movimiento constante y repetitivo detectado en la cámara!"}
            requests.post(url, data=datos)
            alerta_enviada = True 
            
    else:
        estado = "Tranquilo / Mov. Ocasional ✓"
        color = (0, 255, 0) # Verde
        
        if nivel_inquietud < (CAPACIDAD_MAXIMA / 2):
            alerta_enviada = False

    # --- DIBUJAR EN PANTALLA ---
    cv2.putText(frame, estado, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    porcentaje = int((nivel_inquietud / CAPACIDAD_MAXIMA) * 100)
    ancho_barra = int((nivel_inquietud / CAPACIDAD_MAXIMA) * 300)
    
    cv2.rectangle(frame, (10, 60), (310, 80), (255, 255, 255), 2)
    if ancho_barra > 0:
        cv2.rectangle(frame, (10, 60), (10 + min(300, ancho_barra), 80), color, -1)
        
    cv2.putText(frame, f"Carga: {porcentaje}%", (320, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # --- 2. GUARDAR EL FOTOGRAMA EN EL VÍDEO ---
    out.write(frame) # Esto grabará exactamente lo que ves en la ventana "Baby Monitor"

    # Mostrar vídeos
    cv2.imshow("Baby Monitor", frame)
    cv2.imshow("Silueta (MOG2)", mascara)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 3. CERRAR Y LIBERAR RECURSOS ---
cap.release()
out.write # (por seguridad)
out.release()
cv2.destroyAllWindows()
print("📁 Vídeo de prueba guardado correctamente como 'prueba_monitor.mp4'.")