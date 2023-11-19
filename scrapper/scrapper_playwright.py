
import parsel


class Scrapper:
    def __init__(self, url, playwright):
        self._url = url
        self._playwright = playwright
        self._browser = playwright.chromium.launch(headless=True)
        self._page = self._get_page()
        self._html = ""
        if url != "":
            self._set_url(url)

    def _get_page(self):
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/69.0.3497.100 Safari/537.36"
        )
        # was new_page for sync
        page = self._browser.new_page(user_agent=ua)
        return page

    def _set_url(self, url):
        self._url = url
        self._page.goto(self._url)
        self._html = self._page.content()
    
    def _clean_at_sephora(self):
        selector = parsel.Selector(text=self._html)
        clean_selector = selector.xpath('//div[@class="css-h2sczi eanm77i0"]//div//span//text()').getall()
        clean_selector = [ele.lower() for ele in clean_selector]
        clean_selector = " ".join(clean_selector)
        return "clean" in clean_selector

    
    @property
    def __close_browser(self):
        self._browser.close()

    @property
    def __get_url(self):
        return self._url
        

    @property
    def __get_sephora_ingredients(self):
        selector = parsel.Selector(text=self._html)
        ingredients = selector.xpath(
            '//div[@class="css-1ue8dmw eanm77i0"]//div//text()'
        ).getall()
        if self._clean_at_sephora():
            clean_idx = 0
            for i in range(len(ingredients)):
                if "clean" in ingredients[i].lower():
                    clean_idx = i
                    break
            return ingredients[:clean_idx]
        
        return ingredients