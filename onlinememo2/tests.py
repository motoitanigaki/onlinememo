from selenium import webdriver
import unittest

class LogoutStatusTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_logout_status(self):

        # サイト訪問
        self.browser.get('http://127.0.0.1:8000/')

        # タイトルタグ確認
        self.assertIn('オンラインメモ｜会員登録無くブラウザで使えるwebメモ帳サービス',self.browser.title)

        # 新しくノートを記入
        NOTE_TITLE = 'メモテスト'
        self.browser.find_element_by_id('input-title').send_keys(NOTE_TITLE)

        # メモリストに反映されているか確認
        note_title_value = self.browser.find_element_by_xpath('/html/body/main/div[1]/nav/div[2]/li[1]').text
        self.assertIn(NOTE_TITLE, note_title_value)

        # メモ削除
        self.browser.find_element_by_xpath('/html/body/main/div[1]/section/div[1]/button[4]').click()

        # メモに反映されているか確認
        self.assertIn('',self.browser.find_element_by_id('input-title').text)

        self.fail('Finish the Test.')

if __name__ == '__main__':
    unittest.main(warnings='ignore')