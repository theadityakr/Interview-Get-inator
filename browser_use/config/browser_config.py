from browser_use import Browser, BrowserProfile  
from config.env import get_env

class BrowserFactory:

    @staticmethod
    def create():
        args = get_env("BROWSER_ARGS", "")
        args_list = args.split(",") if args else []
        return Browser(
            browser_profile=BrowserProfile(
                headless=get_env("HEADLESS", "false") == "true",
                disable_security=get_env("BROWSER_SECURITY", "false") == "true",
                # extra_chromium_args=args_list
            )
        )