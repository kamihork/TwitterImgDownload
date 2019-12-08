# IMPORT
import os
import tweepy
import time 
import urllib.request, urllib.error

# 画像の保存先
IMG_DIR = './images/'

# 環境変数
CONSUMER_KEY        = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET     = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY    = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# 検索キーワード
TARGET = '#高本彩花'

# 検索オプション
SEARCH_PAGES_NUMBER = 100 # 読み込むページ数
PER_PAGE_NUMBER = 100 # ページごとに返されるツイートの数（最大100）

class imageDownloader(object):
    def __init__(self):
        """初期設定
        """
        super(imageDownloader, self).__init__()
        self.set_api()

    def run(self):
        """実行
            1. キーワードの数だけtweetページを検索
            2. 読み込むページ数に対して、ページごとに返されるツイートの数で絞り込む
            3. キーワードを含む画像のURLがあればダウンロード
        """
        self.max_id = None # ページを跨ぐ検索対象IDの初期化
        for page in range(SEARCH_PAGES_NUMBER):
            ret_url_list = self.search(TARGET, PER_PAGE_NUMBER)
            for url in ret_url_list:
                print('OK ' + url)
                self.download(url)
            time.sleep(0.1) # TimeOut防止

    def set_api(self):
        """apiの設定
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def search(self, target, rpp):
        """twitterで検索実行
        """
        # 検索結果
        ret_url_list = []

        try:
            # 検索実行
            if self.max_id:
                # q: クエリ文字列, rpp: ツイート数, max_id: より小さい（古い）IDを持つステータスのみを返す
                res_search = self.api.search(q=target, lang='ja', rpp=rpp, max_id=self.max_id)
            else:
                res_search = self.api.search(q=target, lang='ja', rpp=rpp)
            # 結果を保存
            for result in res_search:
                if 'media' not in result.entities: continue
                for media in result.entities['media']:
                    url = media['media_url_https']
                    if url not in ret_url_list: ret_url_list.append(url)
            # 検索済みidの更新し、より古いツイートを検索させる
            self.max_id = result.id
            # 検索結果の返却
            return ret_url_list
        except Exception as e:
            self.error_catch(e)

    def download(self, url):
        """画像のダウンロード
        """
        url_orig = '%s:orig' % url
        path = IMG_DIR + url.split('/')[-1]
        try:
            response = urllib.request.urlopen(url=url_orig)
            with open(path, "wb") as f:
                f.write(response.read())
        except Exception as e:
            self.error_catch(e)

    def error_catch(self, error):
        """エラー処理
        """
        print("NG ", error)

def main():
    """メイン処理
    """
    try:
        downloader = imageDownloader()
        downloader.run()
    except KeyboardInterrupt:
        # Ctrl-Cで終了
        pass

if __name__ == '__main__':
    main()