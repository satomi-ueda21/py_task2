from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas

def scraping():
  driver_path = ChromeDriverManager().install()
  options = ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
  driver = Chrome(driver_path, options=options)
  driver.get("https://gyoumu-kouritsuka-pro.site/")


  df = pandas.DataFrame()
  while True:
    article_elms = driver.find_elements_by_css_selector(".entry-card-wrap.a-wrap.border-element.cf")
    for article_elm in article_elms:
      #print(article_elm.text)
      title = article_elm.find_element_by_tag_name("h2").text
      post_date = article_elm.find_element_by_class_name("post-date").text
      article_link = article_elm.get_attribute("href")
      print(title, post_date, article_link)

      df = df.append({
        "タイトル": title,
        "登校日": post_date,
        "リンク": article_link
      }, ignore_index=True)

    try:
      driver.find_element_by_css_selector(".pagination-next-link.key-btn").click()
    except:
      print("最後のページです")
      break

  df.to_csv("記事一覧.csv", encoding="utf-8_sig")


scraping()