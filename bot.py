from bs4 import BeautifulSoup
import urllib.request
import codecs
 
# Veri toplama işlemi bu script aracılığıyla gerçekleştirilir.

site = "http://www.hurriyet.com.tr"
# Verilen sayfa numaraları arasındaki sayfalarda geçen makale linklerini toplar.
urls = []
for i in range(0,5):
    url = "http://www.hurriyet.com.tr/yazarlar/mehmet-yasin/?p=" + str(i+1)
    url_oku = urllib.request.urlopen(url)
    soup = BeautifulSoup(url_oku, 'html.parser')
     
    icerik = soup.find_all('a',attrs={'class':'title'})
    for tag in icerik:
        if '/seyahat/' not in tag['href']:
            urls.append(site + tag['href'])

# Toplanan urllerdeki makalelerin ilgili kısımlarını getirip istenilen formatta dosyaya yazar.
index = 0
for url in urls:
    yazar_Adi = "mehmetyasin"
    url_oku = urllib.request.urlopen(url)
    soup = BeautifulSoup(url_oku, 'html.parser')
     
    # HTML sayfasındaki ilgili taglere odaklanır.
    icerik = soup.find_all('div',attrs={'class':'article-content news-text'})
    file = codecs.open("mak" + str(index) + "_" + yazar_Adi + ".txt","w","utf-8") 
    if len(icerik[0]) > 0:
        file.write(icerik[0].text)
        file.close()
        index = index + 1
    