# Draws the app icon (a word with a red focus letter) as PNGs, no dependencies.
import struct, zlib, sys

BG, FG, RED = (15, 16, 19), (236, 236, 239), (229, 72, 77)

def color(x, y):
    if 0.445 <= y <= 0.555:
        if 0.17 <= x <= 0.44: return FG
        if 0.465 <= x <= 0.535: return RED
        if 0.56 <= x <= 0.83: return FG
    if 0.488 <= x <= 0.512 and (0.33 <= y <= 0.39 or 0.61 <= y <= 0.67): return RED
    return BG

def png(path, n):
    raw = b''.join(b'\0' + b''.join(bytes(color((x + .5) / n, (y + .5) / n)) for x in range(n)) for y in range(n))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', n, n, 8, 2, 0, 0, 0))
                + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

for name, n in [('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)]:
    png(name, n)
