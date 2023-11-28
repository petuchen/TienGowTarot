import streamlit as st
import random
import os
from helper import Preprocess, Evaluate

st.runtime.legacy_caching.clear_cache()


st.title("牙牌神算")


txt_1 = '''
物莫不具陰陽奇偶之理，不獨弈之爲數然也。理既具則數呈，數呈而理自見，卽造物之端。
倪測人事之吉凶，占玩之方，於是乎在，人顧習焉不察耳。如牙牌之有奇耦，此象數之尤著者也。

天之數十有二，蓋以十二月爲一周天，四分其數爲四時，而聚必以三則乾之本體存焉。
地數二，則坤之本體也。人受天地之中以生，有四體卽有四端，故以八爲數，而人名焉，三才備矣。
三才備而萬象呈，不動則不能變化以成象，故縱橫其奇耦之數，而錯綜之。
上下爲兩，犄角爲三，陽變陰合，有調劑之義焉，故謂之和，由是而生生不息矣。
自其奇耦之對待者言之，有長二長三長五么五六四六之屬，至五六爲天地之中合，而數止矣。
其象或耦與耦合，奇與奇合，奇與耦交相合，此動而未離乎靜者也，是故謂之文。
自其奇耦之參互者言之，有五點對七點對八點對之屬，數至九而老陽盡矣。
其象各自爲奇耦，於對待之中，化奇耦之迹，此變動而不居者也，是故謂之武。
至二四爲六，陰也。二爲三，陽也。統之得數之九，析之則一陽在衆陰之上，其象矣。
而三之而六之，不相對而爲對，蓋亦有說。蓋就二四而中之，則左右皆乾也。
又從而分截之，則上中坤也。左右之數偶，判而得乾，陰中陽也。
上中下之數奇，截而得坤，陽中陰也。
兩儀具陳，四象迭見，而人寓乎其間，此陰陽變易，三才溷淆，動之至也。
么二上奇下耦，尊卑奠定，乾清坤甯，其象秩然而不紊，此變之極而歸於不變，還其本體，靜之至也。
一動一靜，各臻其至，謂之至尊，不亦宜乎。

占者蓍龜之設，敎民卜筮，以辨吉凶，而定民志。謂神物得天地之靈，悉陰陽之變也。
牙牌之象數義蘊有如此，乃昵爲玩具，而謂不可以占乎。
山中習靜觀象繫辭，演爲此數，亦以見天地陰陽之理，隨物而寓，吉凶悔吝之機。
觸緒皆通，引而伸之，其受命也如響。

岳慶山樵 著

'''

txt_2 = "全副牙牌一字排，中間看有幾多開。連排三次分明記，上下中平內取裁。"

txt_3 = '''

+ 不同六開，五子五開，合巧四開，分相三開，馬軍三開，對子三開，么二三三開，二三靠三開，正快一開。
+ 十二開以上爲上上，十開十一開爲上中，八開及九開爲中平，五開至七開爲中下，一開至四開爲下下。
+ 如遇一開俱無須虔誠禱告再占。
'''

txt_4 = '''

按數分五類，每類二十五數。合成天數五，地數五，五五二十五之意。
共成一百二十五數，數詞四句，事變萬物，惟在占者誠心求之，則無不應驗。
如占得之數，與所問之事，語氣未協，當於字句間，玩味詳測之，所謂以意逆志，是爲得之也。

'''

st.subheader("牙牌神數序")
st.markdown(txt_1)
st.divider()
st.subheader("占法")
st.markdown(txt_2)
st.divider()
st.subheader("開數")
st.markdown(txt_3)
#----------
card_cache = None
card_list ={}

if 'final_score' not in st.session_state:
    st.session_state['final_score'] = []
if 'card_cache' not in st.session_state:
    st.session_state['card_cache'] = None

st.divider()
st.subheader("第{}輪，請切牌⋯⋯".format(len(st.session_state['final_score'])+1))


int_val = st.slider('切牌', min_value=1, max_value=32, value=1, step=1)

if int_val != 1:

    with st.spinner("占卜中⋯⋯"):
        # print("score: {}".format(score))
        if st.session_state['card_cache']:
            card_list = Preprocess.shuffle(st.session_state['card_cache'].copy())
        else:
            card_init = Preprocess()
            card_list = Preprocess.shuffle(card_init.raw_tiles)
        card_list = (Preprocess.cut(card_list, int_val))
        Preprocess.show_images(card_list, show_image=True)
        st.session_state['card_cache'] = card_list.copy()
        eva = Evaluate(card_list)
        current_score = eva.processing()
        score = current_score[0][1]
        # st.write(final_score, current_score)
        if score == 0:
            st.write("零開，請重新切牌。")
        else:
            st.session_state['final_score'].append(current_score)
            if len(st.session_state['final_score']) <3:
                st.write("此輪結束，請重新切牌。")
            elif len(st.session_state['final_score'])==3:
                st.write("占卜結束。")

            with st.expander("數序細節"):
                st.write(current_score)

st.divider()
if len(st.session_state['final_score']) == 3:
    final_result = Preprocess.final_scoring(st.session_state['final_score'])
    st.write("最後數序：{}".format(final_result[1]))
    result_dict = Preprocess.lookup(final_result[0])
    if result_dict is not None:
        st.text("籤頭：{}".format(' '.join(result_dict['name'])))
        st.text("籤詩：{}".format(' '.join(result_dict['poem'])))
        st.text("解曰：{}".format(' '.join(result_dict['description'])))
        st.text("斷曰：{} \n\t{}".format(result_dict['judgement'][0], result_dict['judgement'][1]))

    st.image(os.path.join(os.getcwd(), 'img', 'output', '{}.jpg'.format(final_result[0])))
    st.download_button(label='下載籤詩',
                            data= open(os.path.join(os.getcwd(), 'img', 'output', '{}.jpg'.format(final_result[0]), 'rb')).read(),
                            file_name='{}.jpg'.format(final_result[1]),
                            mime='image/jpg')


#---------- end result

st.divider()
st.subheader("跋")
st.text(txt_4)

