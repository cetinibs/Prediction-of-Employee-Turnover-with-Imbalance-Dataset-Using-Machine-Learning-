import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import NullFormatter
import json

import logging
from matplotlib.ticker import EngFormatter

######## DEĞİŞKEN YAPILARININ İNCELENMESİ ########
#Değişkenlerin Yakalanması ve İşlemlerin Genelleştirilmesi
def grap_col_names(dataframe, cat_th=10, car_th=20):
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardinal(Sınıf sayısı fazla olup anlam ifade etmeyen) değişkenlerin isimlerini verir
    Parameters
    ----------
    dataframe: dataframe
        değişken isimleri alınmak istemem dataframe' dir.
    cat_th: int, float
        numerik fakat kategorik olan değişkenler içim sınıf eşik değeri
    car_th: int, float
        kategorik fakat kardinal olan değişkenler içim sınıf eşik değeri
    Returns
    -------
    car_cols: list
        Kategorik değişken lsitesi
    num_cols: list
        Numerik değişken listesi
    cat_but_car: list
        Kategorik görünümlü kardinal değişken listesi
    Notes
    -------
    cat_cols + num_cols + cat_but_car = toplam değişken sayısı
    num_but_cat cat_cols' un içerisinde
    Return olan 3 liste toplamı toplam değişken sayısına eşittir:
    """
    #Kategorik kolonlar
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]

    ##Numerik olup kategorik veri içerebilen kolonlar.
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int", "float"]]

    #Açıklanamayacak kadar fazla sınıf varsa kardinal veridir. Ölçülebilir değişken değildir.
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and str(dataframe[col].dtypes) in  ["category", "object"]]

    #Tüm kategorik değişkenleri birleştir.
    #cat_cols = cat_cols + num_but_cat

    #Anlam ifade etmeyen kolonlar kategorik kolonlardan çıkartılır. Sınıf sayısı adreste fazla olacağından kardinal olarak değerlendirilemez.
    #Kategorik veriden Kardinal veriyi çıkarmıyoruz.
    #cat_cols = [col for col in cat_cols if col not in [cat_but_car]]
    num_cols = [col for col in dataframe.columns if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")

    return cat_cols, num_cols, cat_but_car

#ÖRNEK VERİ SETİNE İLİŞKİN BİLGİLER
def check_df(df, head = 10):
    print("\n##################### SHAPE #####################")
    print(df.shape)
    print("\n##################### TYPES #####################")
    print(df.dtypes)
    print("\n##################### HEAD #####################")
    print(df.head(head))
    print("\n##################### TAIL #####################")
    print(df.tail(head))
    print("\n##################### NA #####################")
    print(df.isnull().sum())
    print("\n##################### QUANTILES #####################")
    print(df.describe([0 , 0.05, 0.50, 0.95, 0.99, 1]).T)

#Değişkenlerin sayısı ve yüzdelik dilimini çizer.
def cat_summary(dframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dframe[col_name].value_counts(), "Ration": 100 * dframe[col_name].value_counts() / len(dframe)}))
    print("##########################################\n")
    if plot:
        sns.countplot(x=dframe[col_name], data=dframe)
        plt.show(block=True)

#Grafik Çizdir
#grafik üzerine sayı yazdırır.
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

#Bar grafiği çizer.
def show_bar_chart(df,title,color):
    fmt = EngFormatter(places=0)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title(title+' Kayıt Sayıları', loc ='center')
    #ax.set_xlabel('Değişkenler')
    ax.set_ylabel('Sayı')
    bar = ax.bar(df['variable'], df['value'], color=color)
    ax.yaxis.set_major_formatter(fmt)
    addlabels(df['variable'], df['value'])
    #ax.bar_label(bar)
    plt.show()

#Yatay bar grafiği çizer
def show_barh_chart(df,title,color):
    fmt = EngFormatter(places=0)
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    bars = ax.barh(y=df["variable"], width=df["value"], color=color)
    ax.xaxis.set_major_formatter(fmt)
    for b in bars:
        w = b.get_width()
        ax.text(w, b.get_y()+0.5*b.get_height(),
                fmt.format_eng(w),
                ha='left', va='center')