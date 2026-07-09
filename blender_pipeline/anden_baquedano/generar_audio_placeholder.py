"""
LINEA CERO - Anden Baquedano
Fase 3.5 - Audio (PLACEHOLDERS sintetizados)

IMPORTANTE: estos son tonos generados por sintesis simple (senoidales +
ruido), NO grabaciones reales. Sirven para dejar la infraestructura de
audio (AudioStreamPlayer3D, triggers, mezcla) funcionando y probable
mientras se consiguen las grabaciones/samples reales de Freesound.org
y ZapSplat (ver seccion 9 del documento de diseno), que requieren
descarga manual con cuenta/atribucion y no pueden bajarse via API
publica sin autenticacion.

Ejecutar: python generar_audio_placeholder.py
"""

import wave
import struct
import math
import random
import os

SR = 44100

def escribir_wav(path, samples, canales=1):
    with wave.open(path, "w") as f:
        f.setnchannels(canales)
        f.setsampwidth(2)
        f.setframerate(SR)
        frames = b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples)
        f.writeframes(frames)


def fade(samples, fade_in=0.05, fade_out=0.05):
    n = len(samples)
    n_in = int(n * fade_in)
    n_out = int(n * fade_out)
    out = list(samples)
    for i in range(n_in):
        out[i] *= i / max(1, n_in)
    for i in range(n_out):
        out[n - 1 - i] *= i / max(1, n_out)
    return out


def zumbido_electrico(duracion=4.0):
    n = int(SR * duracion)
    out = []
    for i in range(n):
        t = i / SR
        v = 0.15 * math.sin(2 * math.pi * 60 * t)
        v += 0.05 * math.sin(2 * math.pi * 120 * t)
        v += 0.01 * (random.random() * 2 - 1)
        out.append(v)
    return out


def chisporroteo(duracion=0.6):
    n = int(SR * duracion)
    out = []
    for i in range(n):
        t = i / SR
        envelope = math.exp(-t * 8)
        v = envelope * (random.random() * 2 - 1) * 0.8
        if random.random() < 0.02:
            v += (random.random() * 2 - 1) * 0.5
        out.append(v)
    return fade(out, 0.01, 0.3)


def tren_fantasma(duracion=7.0):
    n = int(SR * duracion)
    out = []
    for i in range(n):
        t = i / SR
        progreso = t / duracion
        envelope = math.sin(math.pi * progreso) ** 0.5
        freq = 40 + 15 * math.sin(2 * math.pi * 0.5 * t)
        v = envelope * 0.5 * math.sin(2 * math.pi * freq * t)
        v += envelope * 0.15 * (random.random() * 2 - 1)
        out.append(v)
    return fade(out, 0.15, 0.25)


def radio_estatica(duracion=2.0):
    n = int(SR * duracion)
    out = []
    prev = 0.0
    for i in range(n):
        white = random.random() * 2 - 1
        prev = prev * 0.95 + white * 0.05
        out.append(prev * 0.6 + white * 0.2)
    return fade(out, 0.05, 0.05)


def contacto_entidad(duracion=0.8):
    n = int(SR * duracion)
    out = []
    for i in range(n):
        t = i / SR
        envelope = math.exp(-t * 3) * math.sin(math.pi * min(1.0, t / 0.05))
        v = envelope * 0.4 * math.sin(2 * math.pi * 55 * t)
        v += envelope * 0.3 * (random.random() * 2 - 1)
        out.append(v)
    return fade(out, 0.02, 0.4)


def pasos_terrazo(duracion=0.25):
    n = int(SR * duracion)
    out = []
    for i in range(n):
        t = i / SR
        envelope = math.exp(-t * 25)
        v = envelope * (random.random() * 2 - 1) * 0.5
        out.append(v)
    return fade(out, 0.01, 0.5)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "audio", "anden_baquedano"))
    os.makedirs(out_dir, exist_ok=True)

    random.seed(42)

    archivos = {
        "zumbido_electrico.wav": zumbido_electrico(),
        "chisporroteo.wav": chisporroteo(),
        "tren_fantasma.wav": tren_fantasma(),
        "radio_estatica.wav": radio_estatica(),
        "contacto_entidad.wav": contacto_entidad(),
        "pasos_terrazo.wav": pasos_terrazo(),
    }

    for nombre, samples in archivos.items():
        path = os.path.join(out_dir, nombre)
        escribir_wav(path, samples)
        print(f"[LINEA CERO] Generado: {path} ({len(samples)/SR:.2f}s)")

    print("\n[LINEA CERO] AVISO: estos son placeholders sinteticos.")
    print("Reemplazar con grabaciones reales de Freesound.org / ZapSplat")
    print("segun la seccion 9 (Audio ambiental) de MAPA_AndenBaquedano.md")
