# debug_phone_scraper.py
# ---------------------------------------------------------
# Antes de ejecutar este script, asegúrate de haber instalado
# Playwright y los navegadores:
#   pip install playwright
#   playwright install
# ---------------------------------------------------------

import asyncio
import subprocess
import sys
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# URL que queremos depurar
TARGET_URL = 'https://www.idealista.com/inmueble/108574626/'

async def ensure_browsers_installed():
    # Intentamos lanzar Chromium en modo headless para validar la instalación
    try:
        async with async_playwright() as p:
            await p.chromium.launch(headless=True)
    except Exception:
        print("Navegadores no encontrados. Ejecutando 'playwright install'...")
        try:
            subprocess.run([sys.executable, '-m', 'playwright', 'install'], check=True)
            print("Instalación de navegadores completada.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar navegadores: {e}")
            sys.exit(1)

async def debug_page():
    # Comprobamos y, si hace falta, instalamos navegadores
    await ensure_browsers_installed()

    print('Iniciando navegador en modo de depuración (NO headless)...')
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,   # Para ver el navegador en tiempo real
            slow_mo=100       # Ralentiza las acciones para depuración
        )
        page = await browser.new_page()
        print(f'Navegando a: {TARGET_URL}')
        await page.goto(TARGET_URL, wait_until='domcontentloaded')

        # 1. Aceptar banner de cookies si aparece
        cookie_selector = '#didomi-notice-agree-button'
        try:
            print('Buscando banner de cookies...')
            await page.wait_for_selector(cookie_selector, timeout=5000)
            print('Banner encontrado. Aceptando...')
            await page.click(cookie_selector)
        except PlaywrightTimeoutError:
            print('No apareció banner de cookies o ya estaba aceptado.')

        # 2. Localizar y hacer clic en "Ver teléfono"
        print('Buscando botón "Ver teléfono"...')
        phone_button = page.get_by_role('button', name=r'(?i)ver teléfono')

        if await phone_button.count() > 0:
            print('Botón encontrado. Pausando para inspección...')
            await page.pause()
            print('Haciendo clic en el botón...')
            await phone_button.click()

            # 3. Extraer el número de teléfono
            print('Esperando número de teléfono...')
            phone_locator = page.locator('span.hidden-contact-phones_text')
            await phone_locator.wait_for(state='visible', timeout=5000)
            phone_text = (await phone_locator.text_content() or '').strip()

            print('---------------------------------')
            print(f'Teléfono extraído: {phone_text}')
            print('---------------------------------')
        else:
            print('ERROR: No se encontró el botón "Ver teléfono". Abriendo inspector...')
            await page.pause()

        print('Cerrando navegador en 10 segundos...')
        await asyncio.sleep(10)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_page())
