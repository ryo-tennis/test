from selenium import webdriver
import yaml
from function_list import fuctionClass
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# 非同期テスト
import multiprocessing
import time
import asyncio

# 各関数で共有するurlなどをインプット
temporaryData = {}

async def main(siteName,testDate,numString):
    # 設定されたブラウザ分この関数を呼び出す
    async def browserMain(webName):
        print('\n\n'+webName+' '+siteName+' '+' start')
        webBrowserManager = testDateOpthons['web_browser_manager'][webName]
        # ドライバーオプションをブラウザ別に設定
        options = getattr(getattr(getattr(webdriver, webBrowserManager['import_name']),'options'),'Options')()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:922"+numString)
        # オプションの設定を読み込む
        [options.add_argument('--'+op_key) for op_key,op_value in testDateOpthons['opthions'].items() if op_value]
        # オプションの設定で接続
        driver = getattr(webdriver,webName)(executable_path=eval(webBrowserManager['import_manager'])().install(),options=options)
        # driverのオプションの設定を読み込む
        [getattr(driver, op_key)() for op_key,op_value in testDateOpthons['driver_opthions'].items() if op_value]
        # yamlで指定した処理順で実行
        # [eval(func[0])(siteInfSet, driver) for func in sorted(siteInfSet['test_screen'].items(),key=lambda x:x[1]) if func[1] != -1]

        for func in sorted(siteInfSet['test_screen'].items(),key=lambda x:x[1]):
            if func[1] != -1:
                eval(func[0])(siteInfSet, driver)
                print('aaa')
                await asyncio.sleep(10)



        print('\n\n'+webName+' '+siteName+' '+' end\n')

    siteInfSet = testDate['site_inf_set']
    # webdriverのオプションの設定をyamlから取得
    testDateOpthons = testDate['webdrive_inf_set']
    # オプション(yamlでtrueにしてあるブラウザ分ループ)
    [await browserMain(op_key) for op_key,op_value in siteInfSet['web_browser_select'].items() if op_value]
    print('\nall end')

# ログイン処理
def login(siteInfSet,driver):

    loginUrl = siteInfSet['home_url'] + siteInfSet['move_slug']['login']
    # もし現在のurlと一緒ならurl遷移をとばす
    if(driver.current_url != loginUrl):driver.get(loginUrl)
    # デバック用
    # outputFile.write(driver.page_source)

    # ログインIDを入力
    loginId = driver.find_element_by_class_name(siteInfSet['get_element']['login_id'])
    loginId.send_keys(siteInfSet['post_date']['user_email'])
    # ログインパスワードを入力
    loginPass = driver.find_element_by_class_name(siteInfSet['get_element']['login_pass'])
    loginPass.send_keys(siteInfSet['post_date']['user_pass'])
    # ログインボタンクリック
    loginBotton = driver.find_element_by_xpath(siteInfSet['get_element']['login_botton'])
    loginBotton.click()


# 商品一覧商品選択制御(商品一覧でカート投入が行える商品詳細url取得処理)
def itemList(siteInfSet,driver):
    itemListUrl = siteInfSet['home_url'] + siteInfSet['move_slug']['item_list']
    # もし現在のurlと一緒ならurl遷移をとばす
    if(driver.current_url != itemListUrl):driver.get(itemListUrl)
    # デバック用
    # outputFile.write(driver.page_source)

    # 商品一覧の商品urlを全取得
    itemUrlList = driver.find_elements_by_xpath(siteInfSet['get_element']['item_url'])
    # print(list(map(lambda x:x.get_attribute("href"),itemUrlList)))

    # 取得したurlリスト内のurlにアクセスし、商品在庫を確認
    url = ''
    # 一回別のリストを作らないと値が保持されないため作成(deepcopyでも多分OK)
    itemUrlList = [i for i in map(lambda x:x.get_attribute("href"),itemUrlList)]
    for urlDetail in itemUrlList:
        print(urlDetail)
        url = itemDetail(siteInfSet,driver,urlDetail,True)
        if(url != ''):break
    temporaryData['itemUrl'] = url

# 商品詳細制御(カート投入可能な物を判別→ボタンクリック)
def itemDetail(siteInfSet,driver,urlDetail='',callerJudgement=False):
    try:
        if(urlDetail == ''):urlDetail = temporaryData['itemUrl']
    except:
        print('itemDetailエラー:選択できるurlがありません')
        return
    # もし現在のurlと一緒ならurl遷移をとばす
    if(driver.current_url != urlDetail):driver.get(urlDetail)
    if(callerJudgement):
        try:
            textElements=driver.find_elements_by_class_name(siteInfSet['get_element']['item_check'])
            for text in map(lambda x:x.get_attribute("textContent").replace(' ','').replace('\n',''),textElements):
                print(text)
                if(text == siteInfSet['get_text']['cart_in']):return urlDetail
            return ''
        except:
            print('NO')
            return ''
    # カート投入ボタンクリック
    outputFile.write(driver.page_source)
    cartInBotton = driver.find_element_by_class_name(siteInfSet['get_element']['cart_in_botton'])
    cartInBotton.click()

# カートトップ商品購入(カートトップ→購入最終確認画面)
def cartTop(siteInfSet,driver):
    cartUrl = siteInfSet['home_url'] + siteInfSet['move_slug']['cart_top']
    # もし現在のurlと一緒ならurl遷移をとばす
    if(driver.current_url != cartUrl):driver.get(cartUrl)
    try:
        # カート投入ボタンクリック
        moveToFinalScreen = driver.find_element_by_class_name(siteInfSet['get_element']['move_to_final_screen'])
        moveToFinalScreen.click()
    # 最終確認画面に遷移できないとき(未ログイン時)にこっち
    except:
        # ログインIDを入力
        loginId = driver.find_element_by_xpath(siteInfSet['get_element']['cart_login_email'])
        loginId.send_keys(siteInfSet['post_date']['user_email'])
        # ログインパスワードを入力
        loginPass = driver.find_element_by_xpath(siteInfSet['get_element']['cart_login_pass'])
        loginPass.send_keys(siteInfSet['post_date']['user_pass'])
        # カート投入ボタンクリック
        moveToFinalScreen = driver.find_element_by_xpath(siteInfSet['get_element']['login_after_move'])
        moveToFinalScreen.click()
async def a():
    while True:
        print('hoge')
        await asyncio.sleep(10)


# def main2()

if __name__ == "__main__":
    # テスト情報をinput_date.jsonファイルから取得
    with open('config.yaml',encoding='utf-8') as inputYamlFile:testInfo = yaml.safe_load(inputYamlFile)
    # デフォルトの情報を抽出
    defaultList = testInfo['default']
    # スクレイピングを行うサイトを取得
    testSiteControl = testInfo['test_site']
    # デバック用出力先ファイルの指定
    outputFile = open('debug.txt', encoding='utf-8', mode='w')
    # テストを行うサイトの情報を抽出
    testSiteList = {key:testInfo[key] for key in [key for key,value in testSiteControl.items() if value]}
    # サイトごとにメイン関数を呼びだし(同時にデフォルトとテストデータのjsonデータを結合)
    # [main(siteName, fuctionClass().update_dict(defaultList,testDate)) for siteName,testDate in testSiteList.items() if siteName != 'default']

    async def main2():
        task1 = asyncio.create_task(main('a', defaultList,'1'))
        task2 = asyncio.create_task(main('b', defaultList,'2'))
        await task1
        await task2

    asyncio.run(main2())
    

    # executor = ThreadPoolExecutor(10)
    # loop = asyncio.get_event_loop()
    # print(loop)
    # # for url in ["https://google.de"] * 2:
    # #     loop.run_in_executor(executor, main('a', defaultList), url)

    # loop.run_until_complete(asyncio.gather(main('a', defaultList),main('b', defaultList)))
    



