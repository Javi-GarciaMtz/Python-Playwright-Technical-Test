# app/utils/playwright_helpers.py

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

DEFAULT_TIMEOUT = 15000  # 15 segundos

async def click_when_ready(locator, *, timeout=DEFAULT_TIMEOUT, log_label=""):
    """
    Espera a que un locator sea visible y lo scrollea si es necesario, posteriormente hace clic en el
    Lanza error si el elemento no aparece dentro del timeout
    """
    try:
        await locator.wait_for(state="visible", timeout=timeout)
        await locator.scroll_into_view_if_needed()
        await locator.click(timeout=timeout)
        if log_label:
            print(f"[OK] Click en {log_label}")
    except PlaywrightTimeoutError:
        raise RuntimeError(f"Timeout esperando '{log_label}' o elemento no visible")
