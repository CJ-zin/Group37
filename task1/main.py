# main.py
import webview
from api import Api
import os

if __name__ == '__main__':
    # Guarantee the initialization directory exists for mapping files
    if not os.path.exists("./data"):
        os.makedirs("./data")

    api = Api()  # Instantiate backend bridge interface

    # Render the native web window powered by pywebview
    window = webview.create_window(
        'HK Smart Recycling Network',
        'gui/index.html',
        js_api=api,
        width=1500,
        height=850,
        resizable=False
    )
    webview.start(debug=False)