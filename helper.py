import os
import random
from itertools import chain, product, combinations, permutations, filterfalse
from collections import Counter, deque, defaultdict
from matplotlib.pyplot import figure, imshow, axis
from matplotlib.image import imread
from PIL import Image
import streamlit as st
import time
from datetime import datetime
import logging
import logging.config
import json


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('Admin_Client')

class Preprocess:
    # Tils Preprocessing

    def __init__(self) -> list:
    # 文子（成雙）
        wen_list = [
            [6, 6], [1, 1], [4, 4], [1, 3], # 四大
            [5, 5], [3, 3], [2, 2], [5, 6], # 四素
            [4, 6], [1, 6], [1, 5]  # 三雜
            ]*2
        
        # 武子 （單支） 
        wu_list = [
            [3, 6], [4, 5], # 九
            [3, 5], [2, 6], # 八
            [3, 4], [2, 5], # 七
            [2, 3], [1, 4], # 五
            [4, 2], [1, 2]
            ]
        
        self.raw_tiles = wen_list + wu_list
    
    def shuffle(input_list:list) -> list:
        # Randomly shuffle list element
        # input_list: input_list
        # output_list: shuffled list
        
        output_list = input_list.copy()
        random.shuffle(output_list)
        return(output_list)
    
    def cut(input_list: list, input_index=0) -> list:
        # Cutting the series from the index positions
        # input_list: 1 <= input_list <= 32 
        # input_index: index -1 for the cutting point
        # output_list: new list after cutting

        if input_index >= 1 and input_index <= 32:
            new_index = input_index-1
        else:
            new_index = random.randint(1, 32)
        output_list = input_list[new_index:].copy() + input_list[0: new_index].copy()
        return(output_list)
    
    def show_images(input_list, folder_path='img/', show_image=False, title=''):
        # Plotting the selected tiles
        # Input folder_path: folder path of the tiles images
        # Input input_list: select tiles list

        name_list = [''.join(list(map(str, lst))) for lst in input_list]
        number_of_files = len(name_list)
        fig = figure(figsize=(1*number_of_files, 8), dpi=300)
        for i in range(number_of_files):
            a = fig.add_subplot(1, number_of_files, i+1)
            image = imread(os.path.join(folder_path, name_list[i]+'.svg.png'))
            imshow(image, cmap='Greys_r')
            axis('off')
        output_file = time.strftime("%Y%m%d_%H%M%S.png")
        fig.savefig(os.path.join('result_img', output_file))
        
        if show_image:
            # with Image.open(os.path.join('result_img', output_file)) as img:
            #     img.show(title=title)
            st.pyplot(fig.get_figure())

    def final_scoring(final_score:list):
        # classify total scores into categories
        # input: total_score (total scores)
        # return: catgories (d, m, u)

        score_result = {
            "dd": "下下",
            "md": "中下",
            "mm": "中平",
            "um": "上中",
            "uu": "上上"
            }
        final_result = ''
        final_result_zh = ''
        if final_score is not None:
            for i in final_score:
                if i[0][1] !=0:
                    final_result = final_result + i[0][0]
                    final_result_zh = final_result_zh + score_result[i[0][0]]
                    logger.info(score_result[i[0][0]])
                
        return(final_result, final_result_zh)
        
    def lookup(input_string:str):
        # lookup for the poem and desscriptio
        # input: 6-letter of u,m,d
        # output: dict of description

        des = dict(json.load(open('des.json')))
        if input_string in des.keys():
            return(des[input_string])
        else:
            return(None)

class Evaluate:
    # Evaluate and Score the tiles

    def __init__(self, input_list):
        self.input_list = input_list
        
    def window(self, seq=range(32), excluding_list=[], n=3):
        # create window sequence for all tiles
        # input seq: squence of tiles
        # input excluding_list: excluding unwanted tiles if any
        # yield: window list
        
        it = iter(seq)
        win = deque((next(it, None) for _ in range(n)), maxlen=n)
        # print(list(win))
        yield list(win)
        append = win.append
        for e in filterfalse(lambda x: x in excluding_list, it):
            append(e)
            # if e not in excluding_list:
                # print(e)
            if list(win)[1]-list(win)[0]==1:
                yield list(win)

    def set_list_analysis(self, input_list:list):
        # Generate list set features for cateogrise
        # input: input_list
        # return: element_list, list_len, set_len

        element_list = sorted(list(chain(*input_list)))
        eval_counter = Counter(element_list)
        list_len = len(element_list)
        set_len = len(set(element_list))

        return(element_list, eval_counter, list_len, set_len)
    

    def three_tils_eval_first(self, win_list):
        # print(win_list)
        eval_list, eval_counter, list_len, set_len = self.set_list_analysis(win_list)

        if list_len != 6:
            score = 0
            des = 'false combination'
            skip = False

        elif set_len == 6:
            score = 6
            des = '六不同(all six different)'
            skip = True

        elif eval_counter.most_common(1)[0][1] == 5:
            score = 5
            des = '五子(five the same)'
            skip = True

        elif eval_counter.most_common(2)[0][1] == 4 and \
            eval_counter.most_common(2)[0][1] == \
            eval_counter.most_common(2)[1][0] * eval_counter.most_common(2)[1][1] :
            score = 4
            des = '合巧(four the same and sum the same)'
            skip = True

        elif eval_counter.most_common(2)[0][1] == 3 and eval_counter.most_common(2)[1][1] == 3:
            score = 3
            des = '分相(two times three the same)'
            skip = True

        elif eval_list in [[1, 1, 2, 2, 3, 3]]:
            score = 3
            des = '么二三(123)'
            skip = True

        elif eval_list in [[4, 4, 5, 5, 6, 6]]:
            score = 3
            des = '馬軍(456)'
            skip = True

        elif eval_list in [[1, 1, 2, 2, 3, 3], [4, 4, 5, 5, 6, 6], [2, 2, 3, 3, 6, 6]]:
            score = 3
            des = '二三六(236)'
            skip = True

        elif eval_counter.most_common(1)[0][1] == 3 and \
            sum([i*j for i, j in eval_counter.most_common()[1:]]) >=14 :
            score = 1
            des = '正快(3xn, sum(rest)>=14)'
            skip = True    

        else:
            score = 0
            des = 'not found'
            skip = False
        
        return(skip, score, des)


    def three_tils_eval_second(self, win_list):
        # print(win_list)
        eval_list, eval_counter, list_len, set_len = self.set_list_analysis(win_list)

        if list_len != 6:
            score = 0
            des = 'false combination'
            skip = False

        elif eval_counter.most_common(1)[0][1] == 3 and \
            sum([i*j for i, j in eval_counter.most_common()[1:]]) >=14 :
            score = 1
            des = '正快 （3xn, sum(rest)>=14）'
            skip = True    

        else:
            score = 0
            des = 'not found'
            skip = False
        
        return(skip, score, des)


    def three_tils_eval_second(self, win_list):
        # print(win_list)
        eval_list, eval_counter, list_len, set_len = self.set_list_analysis(win_list)

        if list_len != 6:
            score = 0
            des = 'false combination'
            skip = False

        elif eval_counter.most_common(1)[0][1] == 3 and \
            sum([i*j for i, j in eval_counter.most_common()[1:]]) >=14 :
            score = 1
            des = '正快(3xn, sum(rest)>=14)'
            skip = True    

        else:
            score = 0
            des = 'not found'
            skip = False
        
        return(skip, score, des)

    def two_tils_eval(self, win_list):
        # print(win_list)
        eval_list, eval_counter, list_len, set_len = self.set_list_analysis(win_list)

        if list_len != 4:
            score = 0
            des = 'false combination'
            skip = False

        elif set_len == 1:
            score = 3
            des = '對子(pair)'
            skip = True

        else:
            score = 0
            des = 'not found'
            skip = False
        
        return(skip, score, des)

    def scoring(self, total_score:int):
        # classify total scores into categories
        # input: total_score (total scores)
        # return: catgories (d, m, u)

        mid_result = {
            "dd": [1, 4],
            "md": [5, 7],
            "mm": [8, 9],
            "um": [10, 11],
            "uu": [12, 50]
            }
        for k, v in mid_result.items():
            # print(k, v)
            if total_score >= v[0] and total_score <= v[1]:
                output = k, total_score
            elif total_score == 0:
                output = None, 0

        return(output)
    
    def processing(self):
        # Process the cards and evalute them accordingly
        # input: input_list
        # return: scores

        des_dict = defaultdict(lambda: 0)
        score = 0
        skip_list = []

        seq_3 = self.window(seq=range(32), excluding_list=[], n=3)
        for idx in seq_3:
            win_list = [self.input_list[i] for i in idx]
            logger.info('test')
            # logger.info('%s', (idx, win_list))

            if self.three_tils_eval_first(win_list)[0]:
                # logger.info(idx, win_list, '-----')
                # logger.info('%s', (idx, win_list))
                # logger.info('{}'.format(self.three_tils_eval_first(win_list)[1], self.three_tils_eval_first(win_list)[2]))
                des_dict[self.three_tils_eval_first(win_list)[2]] += 1
                score += self.three_tils_eval_first(win_list)[1]
                skip_list.append(idx)
                # count += 1
                try:
                    next(seq_3)
                    next(seq_3)
                except StopIteration as e:
                    logger.error(e)
                    break
                
            else:
                print(idx, win_list)
                # count += 1
        # print(len(skip_list), score)
        # skip_list = list(chain(*skip_list))

        seq_2 = self.window(seq=range(32), excluding_list=list(chain(*skip_list)), n=2)
        for idx in seq_2:
            win_list = [self.input_list[i] for i in idx]
            # print(idx, win_list)

            if self.two_tils_eval(win_list)[0]:
                # logger.info(idx, win_list, '-----')
                # logger.info('{} {}'.format(idx, win_list))
                # logger.info('{}'.format(self.two_tils_eval(win_list)[1], self.two_tils_eval(win_list)[2]))
                des_dict[self.two_tils_eval(win_list)[2]] += 1
                score += self.two_tils_eval(win_list)[1]
                skip_list.append(idx)
                # count += 1
                try:
                    next(seq_2)
                except StopIteration as e:
                    logger.error(e)
                    break
                
            else:
                logger.info(idx, win_list)
                # count += 1
        # skip_list = list(chain(*skip_list))

        seq_32 = self.window(seq=range(32), excluding_list=list(chain(*skip_list)), n=3)
        for idx in seq_32:
            win_list = [self.input_list[i] for i in idx]
            # print(idx, win_list)

            if self.three_tils_eval_second(win_list)[0]:
                # logger.info(idx, win_list, '-----')
                # logger.info('{} {}'.format(idx, win_list))
                # logger.info('{}'.format(self.three_tils_eval_second(win_list)[1], self.three_tils_eval_second(win_list)[2]))
                des_dict[self.three_tils_eval_second(win_list)[2]] += 1
                score += self.three_tils_eval_second(win_list)[1]
                skip_list.append(idx)
                # count += 1
                try:
                    next(seq_3)
                    next(seq_3)
                except StopIteration as e:
                    logger.error(e)
                    break
                
            else:
                print(idx, win_list)
                # count += 1

        # logger.info('{} {}'.format(len(list(chain(*skip_list))), score))

        return(self.scoring(score), len(list(chain(*skip_list))), dict(des_dict))
