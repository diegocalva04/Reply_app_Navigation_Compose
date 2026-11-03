"""Verificación real del flujo oficial. Requiere APK instalado y adb en PATH.

Uso: python scripts/validar_emulador.py [serial]
No envía el pedido: abre la hoja de compartir y regresa a la aplicación.
"""
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidencias'
OUT.mkdir(exist_ok=True)
SERIAL = sys.argv[1] if len(sys.argv) > 1 else 'emulator-5554'
RESULTS = []

def adb(*args, binary=False):
    r = subprocess.run(['adb', '-s', SERIAL, *args], check=True, capture_output=True, timeout=60)
    return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')

def tree():
    adb('shell', 'uiautomator', 'dump', '/sdcard/cupcake-validation.xml')
    return ET.fromstring(adb('shell', 'cat', '/sdcard/cupcake-validation.xml'))

def nodes(text, attr='text'):
    return [n for n in tree().iter('node') if n.get(attr) == text]

def check(label, condition, detail=''):
    assert condition, label + ': ' + detail
    RESULTS.append({'prueba': label, 'resultado': 'CORRECTO', 'detalle': detail})
    print('CORRECTO:', label, detail, flush=True)

def has(text):
    return bool(nodes(text))

def tap(text, attr='text'):
    found = nodes(text, attr)
    assert found, 'No se encontró: ' + text
    x1,y1,x2,y2=map(int,re.findall(r'\d+',found[0].get('bounds')))
    adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2))
    time.sleep(.5)

def shot(name):
    (OUT / name).write_bytes(adb('exec-out','screencap','-p',binary=True))

def back():
    adb('shell','input','keyevent','4')
    time.sleep(.5)

def enabled(text):
    root = tree()
    parent = {child: node for node in root.iter() for child in node}
    n = next(n for n in root.iter('node') if n.get('text') == text)
    while n.get('clickable') != 'true' and n in parent:
        n = parent[n]
    return n.get('enabled') == 'true'

def start():
    adb('shell','am','force-stop','com.example.cupcake')
    adb('shell','am','start','-n','com.example.cupcake/.MainActivity')
    time.sleep(2)

def options():
    return [n.get('text') for n in tree().iter('node') if re.match(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ',n.get('text',''))]

try:
    start()
    check('Inicio sin botón Up',has('Reply App') and not nodes('Back','content-desc'))
    shot('02_inicio.png')
    for label,price in [('One Cupcake','Subtotal $2.00'),('Six Cupcakes','Subtotal $12.00'),('Twelve Cupcakes','Subtotal $24.00')]:
        tap(label)
        check('Cantidad: '+label,has(price),price)
        check('Next deshabilitado sin sabor: '+label,not enabled('Next'))
        tap('Cancel')
        check('Cancelar desde Flavor: '+label,has('Reply App') and not nodes('Back','content-desc'))

    tap('Six Cupcakes')
    tap('Chocolate')
    check('Next habilitado al elegir sabor',enabled('Next'))
    shot('03_sabor.png')
    shot('07_appbar.png')
    tap('Next')
    check('Next deshabilitado sin fecha',not enabled('Next'))
    dates=options()
    check('Cuatro fechas de retiro',len(dates)==4,str(dates))
    tap(dates[0])
    check('Recargo por retiro hoy',has('Subtotal $15.00'))
    tap(dates[1])
    check('Retiro posterior sin recargo',has('Subtotal $12.00'))
    shot('04_retiro.png')
    tap('Next')
    check('Resumen conserva cantidad sabor fecha y precio',all(has(t) for t in ['Order Summary','6 cupcakes','Chocolate',dates[1],'Subtotal $12.00']))
    shot('05_resumen.png')
    tap('Back','content-desc')
    check('Up vuelve a Pickup conservando selección',has('Choose Pickup Date') and enabled('Next') and has('Subtotal $12.00'))
    back()
    check('Atrás del sistema vuelve a Flavor',has('Choose Flavor') and enabled('Next'))
    tap('Next')
    tap('Cancel')
    check('Cancelar desde Pickup limpia pila',has('Reply App') and not nodes('Back','content-desc'))

    tap('One Cupcake')
    check('Nuevo pedido sin sabor anterior ni precio residual',has('Subtotal $2.00') and not enabled('Next'))
    tap('Vanilla')
    tap('Next')
    tap(options()[1])
    tap('Next')
    tap('Cancel')
    check('Cancelar desde Summary limpia pila',has('Reply App') and not nodes('Back','content-desc'))

    tap('Six Cupcakes')
    tap('Chocolate')
    tap('Next')
    tap(options()[1])
    tap('Next')
    tap('Send Order to Another App')
    hierarchy=tree()
    (OUT/'sharesheet.xml').write_text(ET.tostring(hierarchy,encoding='unicode'),encoding='utf-8')
    packages={n.get('package') for n in hierarchy.iter('node')}
    check('Android Sharesheet abierto',any(p and p!='com.example.cupcake' and ('intentresolver' in p or p=='android') for p in packages),str(packages))
    shot('06_compartir.png')
    adb('shell','input','keyevent','4')
    check('Regreso desde Sharesheet mantiene resumen',has('Order Summary') and has('Chocolate'))
finally:
    (OUT/'validacion.json').write_text(json.dumps({'dispositivo':SERIAL,'pruebas':RESULTS},ensure_ascii=False,indent=2),encoding='utf-8')
