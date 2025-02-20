import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.landingPage import LandingPage
from chunks.chromeCookiesNotification import ChromeCookiesNotification
from data.dataDownloadButton import TEST_DATA

import utils.global_functions as gf


@pytest.fixture
def driver(request):
    options = Options()
    gf.setup(options)

    if hasattr(request, 'param'):
        options.add_argument('--user-agent=' + request.param)
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()


@pytest.mark.parametrize('id,button_text,link,driver,download_url', TEST_DATA,
                         ids=[seq[0] for seq in TEST_DATA], indirect=['driver'])
def test_check_download_links(id, driver, button_text, link, download_url):
    landing_page = LandingPage(driver)
    landing_page.go_home()

    if 'android' in id:
        assert landing_page.get_download_button_text_android.strip() == button_text
        assert landing_page.get_download_button_link_android == link
        landing_page.click_download_button_android()
        assert landing_page.is_redirect_to_url(download_url)
    elif 'ios' in id:
        assert landing_page.get_download_button_text_ios.strip() == button_text
        assert landing_page.get_download_button_link_ios == link
    else:
        assert landing_page.get_download_button_text.strip() == button_text
        assert landing_page.get_download_button_link == link
        landing_page.click_download_button()
        if 'internet_explorer' in id or 'safari' in id:
            assert gf.wait_for_file_in_downloads(download_url)
        elif 'chrome' in id:
            chrome_cookie_notification = ChromeCookiesNotification(driver)
            chrome_cookie_notification.click_i_agree_button_chrome()
            assert landing_page.is_redirect_to_url(download_url)
        elif 'yandex' in id:
            chrome_cookie_notification = ChromeCookiesNotification(driver)
            chrome_cookie_notification.click_i_agree_button_yandex()
            assert landing_page.is_redirect_to_url(download_url)
        else:
            assert landing_page.is_redirect_to_url(download_url)

