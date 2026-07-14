#!/usr/bin/env python3
"""
Muz Animasyonu Oluşturucu
10 saniyelik MP4 video: "Ben çok faydalı bir yiyeceğim" metni ile dönen muz
"""

from moviepy.editor import *
from PIL import Image, ImageDraw
import numpy as np
import os

def create_banana_frame(frame_num, total_frames, width=1280, height=720):
    """
    Muz şekli çizen ve döndüren frame oluştur
    """
    # Beyaz arkaplan
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Merkez koordinatları
    center_x = width // 2
    center_y = height // 2
    
    # Dönüş açısı (frame'e göre)
    rotation_angle = (frame_num / total_frames) * 360
    
    # Geçici resim - muz çiz
    temp_img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Muz şekli (sarı eğri daire)
    banana_box = [center_x - 200, center_y - 150, center_x + 200, center_y + 150]
    temp_draw.ellipse(banana_box, fill=(255, 215, 0, 255), outline=(255, 180, 0, 255), width=3)
    
    # Muz ucunu koyu yap
    temp_draw.ellipse([center_x + 150, center_y - 40, center_x + 220, center_y + 40], 
                      fill=(139, 90, 0, 255))
    
    # Döndür
    temp_img = temp_img.rotate(-rotation_angle, center=(center_x, center_y), expand=False)
    
    # Ana resime yapıştır
    img.paste(temp_img, (0, 0), temp_img)
    
    return np.array(img)

def create_banana_animation(output_file='banana_animation.mp4', duration=10, fps=30):
    """
    10 saniyelik muz animasyonu MP4 videosu oluştur
    """
    print(f"🍌 Muz animasyonu oluşturuluyor... ({duration} saniye)")
    
    total_frames = duration * fps
    
    # Frame'leri oluştur
    print("📸 Frame'ler oluşturuluyor...")
    frames = []
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"   Progress: {i}/{total_frames}")
        frame = create_banana_frame(i, total_frames)
        frames.append(frame)
    
    # Video klibine dönüştür
    print("🎬 Video klibine dönüştürülüyor...")
    clip = ImageSequenceClip(frames, fps=fps)
    
    # Metin ekle
    print("📝 Metin ekleniyor...")
    txt_clip = TextClip(
        "Ben çok faydalı bir yiyeceğim",
        fontsize=60,
        color='darkgreen',
        font='Arial-Bold',
        method='caption',
        size=(width, None)
    )
    txt_clip = txt_clip.set_duration(duration)
    txt_clip = txt_clip.set_position(('center', 'bottom'))
    
    # Video + metin birleştir
    print("🎨 Video ve metin birleştiriliyor...")
    final_clip = CompositeVideoClip([clip, txt_clip])
    
    # MP4 olarak kaydet
    print(f"💾 MP4 olarak kaydediliyor: {output_file}")
    final_clip.write_videofile(
        output_file,
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    print(f"✅ Tamamlandı! Video: {output_file}")
    return output_file

if __name__ == '__main__':
    width, height = 1280, 720
    create_banana_animation(output_file='banana_animation.mp4', duration=10, fps=30)
