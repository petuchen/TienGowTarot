import streamlit as st
import random
import os
from helper import Preprocess, Evaluate

st.runtime.legacy_caching.clear_cache()

if 'final_score' not in st.session_state:
    st.session_state['final_score'] = []
if 'card_cache' not in st.session_state:
    st.session_state['card_cache'] = None
if 'slider' not in st.session_state:
    st.session_state['slider'] = 1

def update_value():
    st.session_state['final_score'] = []
    st.session_state['slider'] += 1


def slider(value = 1, key=st.session_state['slider'] ):
    slider_value = st.slider('請移動滑桿來切牌',
    min_value=1, max_value=32, value=value, step=1, key=key)

    return(slider_value)

st.title("牙牌神算")

txt_0 = '''

陳子善編的《私語張愛玲》裡，宋淇（筆名林以亮）說自己有一本從上海帶出來的牙牌籤書，在張愛玲寫《秧歌》英文版曾經為她卜了一卦，得到「中下中下中平。先否後泰，由難而易」的籤，或許是「巧合」但似乎切中張愛玲當時的心情，「愛玲居然很欣賞這本牙牌簽書，以後出書、出門、求吉凶都要借重它。可惜我們後來搬了幾次家，這本書已不知去向了。從這些小地方，可以看出愛玲是多麼的天真和單純」。

隨著《張愛玲往來書信集》的出版，在長達半世紀與宋淇夫婦的通信中，可以找到多次張愛玲利用牙牌卜卦（她稱之為「起課」）的記載。但最引人注目的大概是那支沒有加註評語的「下下中下中下」籤，「欲進反退，求名反辱。不如靜守，庶免災臨。一飲一啄，莫非前定。淘沙得金，其細已甚」。如同張愛玲筆下人物宿命感沈重那般，「回憶不管是愉快還是不愉快都有種悲哀。雖然淡，但她怕那滋味。她從來不自找傷感，現實生活裡有得是，無可避免。但是光就這麼想，像站在棟古建築物門口往裡張了張，在月光與黑影中，斷瓦頹垣千門萬戶，一瞥便知道全部都在那裡。」 （張愛玲《小團圓》私自潤飾），人生總還是無法「一瞥便知道全部都在那裡」，一支籤亦同。占卜的現代意義，撇除過度迷信的部分不談，除了心理暗示的成分，大概也是想在這充滿不確定的世界裡抓住點什麼、留住點什麼。

'''

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

txt_5 = '''

牙牌（也就是天九牌）由宋代宣和牌演進而來，本來是遊戲賭博的工具，清末發展成算命的一種，像是《牙牌神數》。張愛玲很喜歡用牙牌來問事，每張牌其實都可以看做是兩個骰子的結合，天九玩法有文牌武牌之分，用來算命則不需要。文牌就是兩兩相同成對的牌，武牌都是單張。文牌22張、武牌10張，總共32張牌。

1. 輸入相關資訊，並靜默十秒鐘，思考占卜的主題。
2. 一共占三輪，每輪由「洗牌」、「切牌」、「算開數得分」組成。得分為零必須重占，直到得分不為零。
3. 最後三輪開數加總取得籤詩。
4. 占卜結果僅供參考切勿過度迷信。

'''

txt_6 = '''

1. [《牙牌神數》岳慶山樵, 秦慎安校勘, 1925](https://taiwanebook.ncl.edu.tw/zh-tw/book/NTL-9900014378)
2. [〈張愛玲的牙牌籤〉馮睎乾, 2009](http://daimones.blogspot.com/2009/02/blog-post_05.html)
3. [〈也談張愛玲的牙牌籤〉2009](https://aloneinthefart.blogspot.com/2009/04/blog-post_14.html)

'''


st.markdown(txt_0)
st.divider()
st.subheader("牙牌神數")
with st.expander("原文"):
    st.subheader("序")
    st.markdown(txt_1)
    st.divider()
    st.subheader("占法")
    st.markdown(txt_2)
    st.divider()
    st.subheader("開數")
    st.markdown(txt_3)
    st.divider()
    st.subheader("跋")
    st.text(txt_4)

st.divider()
st.subheader("流程")
st.markdown(txt_5)

st.divider()

mbti_types = [ "不提供",
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

topic_types = [
    "事業", "感情", "健康", "財富", "本月運勢", "其他"
]

gender_input = st.selectbox('性別', ("不提供", "女", "男", "非二元"), index=0, help='不影響占卜結果。')
mbti_input = st.selectbox('MBTI 十六型人格', mbti_types, index=0, help='不影響占卜結果。')
topic_input = st.selectbox('占卜主題', topic_types, index=None, help='若選擇其他，請於心中默念想問的主題。')

if gender_input and mbti_input and topic_input:
    st.write('你的身分是：{}的{}人格，想問的是{}。'.format(gender_input, mbti_input, topic_input))
    st.write('個人資料只是為了將來拓展功能使用，不會被收集儲存。')

#----------
card_cache = None
card_list ={}



st.divider()
st.subheader("第{}輪，請切牌⋯⋯".format(len(st.session_state['final_score'])+1))


# int_val = st.slider('請移動滑桿來切牌',
#     min_value=1, max_value=32, value=st.session_state['slider'], step=1, key=)

int_val = slider()

if int_val > 1:

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
            st.write("零開，請移動滑桿重新切牌")
        else:
            st.session_state['final_score'].append(current_score)
            print(len(st.session_state['final_score']))
            if len(st.session_state['final_score']) <3:
                st.write("此輪結束，請移動滑桿重新切牌。")
            elif len(st.session_state['final_score'])==3:
                st.write("占卜結束。")

            with st.expander("數序細節"):
                st.write(Evaluate.result_translate(current_score))
                print(Evaluate.result_translate(current_score))

st.divider()
if len(st.session_state['final_score']) == 3:
    final_result = Preprocess.final_scoring(st.session_state['final_score'])
    st.write("最後數序：{}".format(final_result[1]))
    result_dict = Preprocess.lookup(final_result[0])
    if result_dict is not None:
        st.text("籤頭：{}".format(' '.join(result_dict['name'])))
        st.text("籤詩：{}".format(result_dict['poem']))
        st.text("解曰：{}".format(result_dict['description']))
        st.text("斷曰：{} \n     {}".format(result_dict['judgement'][0], result_dict['judgement'][1]))

    image_path = os.path.join(os.getcwd(), 'img', 'output', '{}.jpg'.format(final_result[0]))
    st.image(image_path)
    st.download_button(label='下載籤詩',
                        data= open(image_path, 'rb').read(),
                        file_name='{}.jpg'.format(final_result[1]),
                        mime='image/jpg')
    if st.button("占卜已結束，按下此鍵重新開始。", on_click=update_value):
        st.rerun()
        # st.rerun()
        # streamlit_js_eval(js_expressions="parent.window.location.reload()")


#---------- end result


st.divider()
st.subheader("參考資料")
st.markdown(txt_6)
