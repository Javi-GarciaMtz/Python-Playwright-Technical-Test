from app.core.config import settings
from app.models.amazon_login_request import AmazonLoginRequest
from app.core.logger import logger
from app.utils.decorators import catch_exceptions
from playwright.async_api import async_playwright, Page, Browser
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
import asyncio
import re
from app.utils.helpers import click_when_ready

DEFAULT_TIMEOUT = 15000
DEFAULT_TIME_SLEEP = 5

@catch_exceptions
async def login_amazon(page: Page, req: AmazonLoginRequest) -> bool:
    logger.info("Iniciando proceso de login en Amazon...")

    try :
        await page.goto(settings.AMAZON_URL)

        # await page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        button_continue_shopping = await page.query_selector('button:has-text("Continuar a Compras")')
        signin_button = await page.query_selector('a:has-text("Hola, identifícate")')

        if not button_continue_shopping and not signin_button:
            raise Exception("ERROR: No hay forma de llegar al login.")

        if button_continue_shopping:
            await button_continue_shopping.click()

            # await page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
            await asyncio.sleep(DEFAULT_TIME_SLEEP)

        signin_button = await page.query_selector('a:has-text("Hola, identifícate")')

        if not signin_button:
            raise Exception("ERROR: No se encontró el botón de login después de redirigir")

        await signin_button.click()

        await page.wait_for_selector('input[name="email"]')
        await page.fill('input[name="email"]', req.user_email)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.click('span#continue input[type="submit"]')

        await page.wait_for_selector('input[name="password"]')
        await page.fill('input[name="password"]', req.user_pwd)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.click('span#auth-signin-button input[type="submit"]')

        # await page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        logger.info("Login exitoso")
        return True

    except Exception as e:
        logger.error(f"Fallo al hacer login: {e}")
        raise

@catch_exceptions
async def go_to_tv_and_video(page: Page) -> bool:
    try:
        await page.wait_for_selector("#nav-hamburger-menu", state="visible", timeout=DEFAULT_TIMEOUT)
        await click_when_ready(page.locator("#nav-hamburger-menu"), log_label="Menú hamburguesa")

        await page.wait_for_selector(".hmenu-visible", state="visible", timeout=DEFAULT_TIMEOUT)

        # await page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        electronics = page.locator('a.hmenu-item[data-menu-id="11"]')
        await click_when_ready(electronics, log_label="Electrónicos")

        tv_video_link = page.get_by_role("link", name=re.compile(r"Televisión y Video", re.I))
        await click_when_ready(tv_video_link, log_label="Televisión y Video")

        await page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT)

        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        return True

    except Exception as e:
        logger.error(f"Fallo al ir a TV & Video: {e}")
        raise

@catch_exceptions
async def choose_tv(page: Page) -> bool:

    try:
        # await page.wait_for_load_state('networkidle', timeout=15000)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        img_locator = page.get_by_role("img", name=re.compile(r"Televisiones", re.I))
        await click_when_ready(img_locator, log_label="Imagen Televisiones")

        # await page.wait_for_load_state('networkidle', timeout=10000)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.wait_for_selector("img[alt='56\" y Más']", state='visible', timeout=DEFAULT_TIMEOUT)

        tvs_56 = page.locator("a[href*='p_n_size_browse-bin%3A9690389011'] img[alt='56\" y Más']")
        await click_when_ready(tvs_56, log_label='Imagen 56" y Más (selector específico)')

        # ? locator alternativo
        # tvs_56 = page.locator("img[alt='56\" y Más']")
        # await click_when_ready(tvs_56, log_label='Imagen 56" y Más (selector alternativo)')

        # await page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        # await page.wait_for_selector(".s-result-item", state='visible', timeout=DEFAULT_TIMEOUT)

        tv = page.locator('img[data-image-index="1"]')
        await click_when_ready(tv, log_label="Primera TV de la lista")

        # await page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        return True
    except Exception as e:
        logger.error(f"Fallo al elegir TV: {e}")
        raise

@catch_exceptions
async def go_to_cart(page: Page) -> bool:
    try:
        # await page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.wait_for_selector('#add-to-cart-button', state='visible', timeout=DEFAULT_TIMEOUT)
        await click_when_ready(page.locator("#add-to-cart-button"), log_label="Cart button")

        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.wait_for_selector('a[href*="/cart"][data-csa-c-type="button"]', state='visible', timeout=DEFAULT_TIMEOUT)
        await click_when_ready(page.locator('a[href*="/cart"][data-csa-c-type="button"]'), log_label="Go 2 Cart button")

        # await page.wait_for_load_state('networkidle', timeout=DEFAULT_TIMEOUT)
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        return True
    except Exception as e:
        logger.error(f"Fallo al ir al carrito: {e}")
        raise

@catch_exceptions
async def checkout(page: Page) -> bool:
    try:
        await asyncio.sleep(DEFAULT_TIME_SLEEP)

        await page.wait_for_selector('input[name="proceedToRetailCheckout"]', state='visible', timeout=15000)

        await click_when_ready(page.locator('input[name="proceedToRetailCheckout"]'), log_label="Go 2 checkout")

        await asyncio.sleep(DEFAULT_TIME_SLEEP)
        return True

    except Exception as e:
        logger.error(f"Fallo al ir al checkout: {e}")
        raise

@catch_exceptions
async def main_shopping_flow(req: AmazonLoginRequest):
    logger.info("=== INICIANDO FLUJO DE COMPRA EN AMAZON ===")

    async with async_playwright() as playwright:

        # ? Iniciamos el navegador
        browser = await playwright.chromium.launch(
            headless=req.headless,
            args=[
                '--disable-web-security',
                '--no-sandbox',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )

        logger.debug(f"Navegador iniciado. Headless = {req.headless}")

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1440, 'height': 900},
            locale='es-MX',
            timezone_id='America/Mexico_City',
            has_touch=True
        )

        # ? Clave importante: modificar webdriver para evitar detección
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Ocultar otras propiedades que revelan automatización
            window.navigator.chrome = {
                runtime: {}
            };

            // Ocultar entorno automatizado
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );

            // Cambiar artifacts de automatización
            const newProto = navigator.__proto__;
            delete newProto.webdriver;
        """)

        # ? Crear una página nueva
        # page = await browser.new_page()
        page = await context.new_page()

        try:
            # Paso 1: Login
            login_ok = await login_amazon(page, req)
            if not login_ok:
                raise Exception("Login falloo")
            logger.info("Paso 1 completado: Login exitoso")

            # Paso 2: Ir a TV y Video
            tv_video_ok = await go_to_tv_and_video(page)
            if not tv_video_ok:
                raise Exception("Fallo al ir a TV y Video")
            logger.info("Paso 2 completado: Ir a tv y video exitoso")

            # Paso 3: Seleccionar TV
            choose_tv_ok = await choose_tv(page)
            if not choose_tv_ok:
                raise Exception("Fallo al seleccionar TV")
            logger.info("Paso 3 completado: Seleccionar TV exitoso")

            # Paso 4: Ir al carrito
            cart_ok = await go_to_cart(page)
            if not cart_ok:
                raise Exception("Fallo al ir al carrito")
            logger.info("Paso 4 completado: Ir al carrito exitoso")

            # Paso 5: Checkout TV
            checkout_ok = await checkout(page)
            if not checkout_ok:
                raise Exception("Fallo en checkout")
            logger.info("Paso 5 completado: Checkout TV exitoso")

            logger.info("=== FLUJO COMPLETO FINALIZADO ===")
            return {
                "code": 200,
                "message": "Proceso completado con éxito"
            }

        except Exception as e:
            logger.error(f"Error en el flujo de compras: {e}")
            return {
                "code": 500,
                "message": f"Error: {str(e)}"
            }

        finally:
            await browser.close()
