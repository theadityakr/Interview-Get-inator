from browser_use import Browser, BrowserConfig
from .env import get_env

class BrowserFactory:

    @staticmethod
    def create():
        args = get_env("BROWSER_ARGS", "")
        args_list = args.split(",") if args else []

        return Browser(
            config=BrowserConfig(
                headless=get_env("HEADLESS", "false") == "true",
                disable_security=get_env("BROWSER_SECURITY", "false") == "true",
                extra_args=args_list
            )
        )