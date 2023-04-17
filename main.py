import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import QUrl


class AdBlocker:
    def __init__(self):
        self.rules = self.load_rules()

    def load_rules(self):
        rules = [
            "googlesyndication.com",
            "doubleclick.net",
            "adservice.google.com",
            "google-analytics.com",
            "adnxs.com",
            "taboola.com",
            "outbrain.com",
            "scorecardresearch.com",
        ]
        return rules

    def is_blocked(self, url):
        for rule in self.rules:
            if rule in url:
                return True
        return False


class AdBlockerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, ad_blocker):
        super().__init__()
        self.ad_blocker = ad_blocker

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if self.ad_blocker.is_blocked(url):
            info.block(True)


class Browser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        # Load ad blocker rules
        self.ad_blocker = AdBlocker()

        # Create user interface elements
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter a URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)

        # Set up web engine profile and interceptor
        self.web_engine_profile = QWebEngineProfile.defaultProfile()
        self.interceptor = AdBlockerInterceptor(self.ad_blocker)
        self.web_engine_profile.setUrlRequestInterceptor(self.interceptor)

        self.web_view = QWebEngineView(self)
        self.web_view.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.web_view.load(QUrl("https://duckduckgo.com/"))

        # Create layout and set central widget
        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.web_view)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle("boaz's Web Browser Ad Blocker")
        self.setGeometry(100, 100, 1280, 720)

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.web_view.load(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
