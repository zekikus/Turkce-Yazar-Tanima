import codecs
import jpype
import glob
import nltk
from nltk.probability import ConditionalFreqDist
from nltk.tokenize import RegexpTokenizer,sent_tokenize

word_count_dict = {}


def startJVM():
    # JVM başlat
    # Aşağıdaki adresleri java sürümünüze ve jar dosyasının bulunduğu klasöre göre değiştirin
    jpype.startJVM(jpype.getDefaultJVMPath(),
             "-Djava.class.path=zemberek_jar\\zemberek-tum-2.0.jar", "-ea")
    # Türkiye Türkçesine göre çözümlemek için gerekli sınıfı hazırla
    Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
    # tr nesnesini oluştur
    tr = Tr()
    # Zemberek sınıfını yükle
    Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
    # zemberek nesnesini oluştur
    zemberek = Zemberek(tr)
    return zemberek

# Kelime Analizi yapılacak dosyaları oku.
def readFile(filename):
    corpus_raw = u""
    print("Reading '{0}'...".format(filename))
    with codecs.open(filename, "r", "utf-8") as book_file:
        corpus_raw += book_file.read()
    return corpus_raw


# Gelen kelimeleri köküne göre çözümle. Gelen kelimenin morfolojik analizi gerçekleştirilir.
# Gelen kelimenin sıfat,zamir,isim, fiil, özel kelime vb. gibi gruplardan hangisine dahil olduğu belirlenir.
def kelimeCozumle(words, zemberek, word_types):
    for word in words:
        if word.strip()>'':
            yanit = zemberek.kelimeCozumle(word)
            if yanit:
                tip = yanit[0].kok().tip()
                if str(tip) in word_types:
                    word_types[str(tip)] = word_types[str(tip)] + 1 

def explodeSentences(sentences, punkt_dict, zemberek, word_types):          
    # Cümleleri parçalayıp kelimeleri bir diziye doldurur ve kelimeleri çözümler
    words = []
    for sentence in sentences:
        words.extend(sentence.split())
        kelimeCozumle(sentence.split(), zemberek, word_types)
    
    # Cümle içerisinde geçen noktalama işaretleri sayısını bulur.
    for word in words:    
        for punkt in punkt_dict:
            if punkt in word:
                punkt_dict[punkt] = punkt_dict[punkt] + 1
    
    # Metin içerisinde kaç tane farklı kelime geçtiğinin sayısını verir.
    from collections import Counter
    word_count_dict = Counter(w.title() for w in words)
    return words,word_count_dict

# Metinlerin analiz edildikten sonra yapay sinir ağının işleyebileceği sayısal verilere
# dönüştürülmüş halini dosyaya yazar.
def writeFile(result):
    file = open("data.csv","w") 
    file.write(result)
    file.close()

def startApp():
    # Zemberek nesnesi oluşturuldu.
    zemberek = startJVM()
    book_filenames = sorted(glob.glob("metinler/*.txt"))
    result = ""
    
    for filename in book_filenames:
        
        punkt_dict= {"!":0, ".":0, ",":0, "?":0, ":":0}
        word_types = {"ISIM" : 0, "FIIL" : 0, "SIFAT" : 0, "ZAMIR" : 0, "ZARF" : 0, "BAGLAC" : 0, "EDAT" : 0, "ZAMAN" : 0, "SAYI" : 0, "OZEL" : 0, "KISALTMA" : 0, "SORU" : 0}
        
        # Dosyayı oku
        text = readFile(filename)
        # Dosyadaki cümleleri ayıkla
        sentences = sent_tokenize(text)
        words,word_count_dict = explodeSentences(sentences, punkt_dict, zemberek, word_types)
        
        # Okunan metin dosyaya yazılmak için csv formatına getirilir.
        result = result + str(len(sentences)) + ","
        result = result + str(len(words)) + ',' + str(len(word_count_dict)) + ','
        
        for key, value in punkt_dict.items():
            result = result + str(value) + ','
        for key, value in word_types.items():
            result = result + str(value) + ','
        result = result + (filename.split("_")[1])[:-4] +"\n"
    writeFile(result)
    
startApp()


#JVM kapat
jpype.shutdownJVM()