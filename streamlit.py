import streamlit as st
import numpy as np
import pandas as pd
from janome.tokenizer import Tokenizer

count_word_1 = 0
count_symbol_1 = 0
count_word_2 = 0
count_symbol_2 = 0
t = Tokenizer()
s1="吾輩は猫である。名前はまだ無い。"
s2="吾輩は猫である。名前はもう有る。"
arr1 =[]
arr2 =[]

st.sidebar.title('コサイン類似度')
st.title("２つの文章の類似度を確認します。")
st.write("\n")

s1 = st.text_input("解析したい文章を入力してください①", value=s1, max_chars=None, type='default')
if s1!="":
    for token in t.tokenize(s1):
        if token.part_of_speech.split(',')[0] == "記号":
            count_symbol_1 += 1
        elif token.part_of_speech.split(',')[0] != "記号":
            arr1.append(token.surface)
            if count_word_1+count_symbol_1<5:
                st.write(token)
        elif count_word_1 == 5:
            st.write("...")
        count_word_1 += 1
st.write("この文章は{}個の品詞と{}個の記号で構成されています。".format(count_word_1,count_symbol_1))

s2 = st.text_input("解析したい文章を入力してください②", value=s2, max_chars=None, type='default')
if s2!="":
    for token in t.tokenize(s2):
        if token.part_of_speech.split(',')[0] == "記号":
            count_symbol_2 += 1
        elif token.part_of_speech.split(',')[0] != "記号":
            arr2.append(token.surface)
            if count_word_2+count_symbol_2<5:
                st.write(token)
        elif count_word_2 == 5:
            st.write("...")
        count_word_2 += 1
st.write("この文章は{}個の品詞と{}個の記号で構成されています。".format(count_word_2,count_symbol_2))
st.title("分解表と分散表現")
    
if (s1!="")&(s2!=""):
    df_1 = pd.DataFrame({'1st_sentence':arr1})
    df_2 = pd.DataFrame({'2nd_sentence':arr2}) 
    df_ =  pd.concat([df_1,df_2],axis=1)
    st.dataframe(df_)
    
    Wlist = [arr1,arr2]
    word_to_index = {}
    index_to_word = {}
    for s in Wlist:
        for w in s:
            if w not in word_to_index:
                new_index = len(word_to_index)
                word_to_index[w] = new_index
                index_to_word[new_index] = w

    corpus = np.zeros((len(Wlist), len(word_to_index)))
    
    for i, s in enumerate(Wlist):
        for w in s:
            corpus[i, word_to_index[w]] = 1
    
    if st.checkbox("show vector"):
        st.write(pd.DataFrame(corpus).T)

    
    def cos_sim(x, y):
        return np.dot(x, y) / (np.sqrt(np.sum(x**2)) * np.sqrt(np.sum(y**2)))
    for i, v in enumerate([""]):
        per = cos_sim(corpus[0], corpus[i + 1])
        st.sidebar.title(v + ":" + f"{per:.2}")
    st.sidebar.write('※出現回を考慮しないコサイン類似度として計算')
  
