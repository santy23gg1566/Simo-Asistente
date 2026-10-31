"""Configura iconos adaptativos y edge-to-edge de SIMO (se ejecuta en GitHub Actions)."""
from pathlib import Path
import shutil
import re

root = Path(__file__).resolve().parents[1]
android = root / 'android'
java = android / 'app/src/main/java/com/simo/voice/MainActivity.java'
java.parent.mkdir(parents=True, exist_ok=True)
java.write_text('''package com.simo.voice;

import android.os.Bundle;
import android.os.Build;
import androidx.activity.EdgeToEdge;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
  @Override public void onCreate(Bundle savedInstanceState) {
    EdgeToEdge.enable(this);
    super.onCreate(savedInstanceState);
    if (Build.VERSION.SDK_INT >= 29) getWindow().setNavigationBarContrastEnforced(false);
  }
}
''', encoding='utf-8')

res = android / 'app/src/main/res'
for density in ('mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi'):
    dest = res / f'mipmap-{density}'
    dest.mkdir(parents=True, exist_ok=True)
    for suffix in ('', '_round', '_foreground'):
        shutil.copy2(root / 'assets' / f'ic_launcher{suffix}_{density}.png', dest / f'ic_launcher{suffix}.png')
# Set a fully opaque adaptive icon background
bg = res / 'values/ic_launcher_background.xml'
bg.write_text('<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">#0A1431</color></resources>\n', encoding='utf-8')
# Capacitor/Gradle generate manifest; plugin provides RECORD_AUDIO permission.
print('SIMO: iconos aplicados y ventana edge-to-edge activada')
