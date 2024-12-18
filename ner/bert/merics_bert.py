
from __future__ import print_function
import sys


def reverse_style(input_string):
    target_position = input_string.index('[')
    input_len = len(input_string)
    output_string = input_string[target_position:input_len] + input_string[0:target_position]
    return output_string

def get_ner_BM(label_list):
    '''

    :param label_list:[['B_M','M_M','M_M','B_Dou','B_J','M_J','M_J'],['B_M','M_M','B_J','B_J','B_J']]
    :return: ['[0,1,2]M', '[3,3]DOU', '[4,5,6]J'] ,      ['[0,1,2]', '[3,3]', '[4,5,6]']
    '''
    list_len = len(label_list)
    begin_label = 'B_'
    end_label = 'M_'
    whole_tag = ''
    index_tag = ''
    tag_list ,dj_list = [],[]
    stand_matrix = []
    for i in range(0, list_len):

        current_label = label_list[i].upper()
        if begin_label in current_label:
            if index_tag != '':
                tag_list.append(whole_tag + ',' + str(i-1))
            whole_tag = current_label.replace(begin_label,"",1) +'[' +str(i)
            index_tag = current_label.replace(begin_label,"",1)
        elif end_label in current_label:
            if index_tag != '':
                if i<list_len-1 and label_list[i+1].startswith('B'):
                    tag_list.append(whole_tag +',' + str(i))
                    whole_tag = ''
                    index_tag = ''
                else:
                    whole_tag += ',' + str(i)
        else:
            continue
    if (whole_tag != '')&(index_tag != ''):
        tag_list.append(whole_tag)
    tag_list_len = len(tag_list)

    for i in range(0, tag_list_len):
        if len(tag_list[i]) > 0:
            tag_list[i] = tag_list[i] + ']'
            dj_list.append(tag_list[i][tag_list[i].index('[')::])
            insert_list = reverse_style(tag_list[i])
            stand_matrix.append(insert_list)

    # print(stand_matrix,dj_list)
    # exit()
    return stand_matrix,dj_list

def pre_re_f1(A,B,C):

    precision = 1.0 * A / B if B > 0 else 0
    recall = 1.0 * A / C if C > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    return precision, recall, f1

def evaluation(predictions, answers):
    co, pre, an= 0,0,0
    co_dj,pre_dj, an_dj = 0,0,0
    for p, a in zip(predictions, answers):  # 将预测的tag和答案一起做成元组([O,O,O,O,SEG-S],[O,O,O,O,SEG-S])

        bd_p, dj_p = get_ner_BM(p[: len(a)])
        bd_a, dj_a = get_ner_BM(a)
        #标点
        co += len(set(bd_p) & set(bd_a))
        pre += len(bd_p)
        an += len(bd_a)

        #断句
        co_dj+= len(set(dj_p) & set(dj_a))
        pre_dj += len(dj_p)
        an_dj += len(dj_a)


    bd = pre_re_f1(co,pre,an)
    dj = pre_re_f1(co_dj,pre_dj,an_dj)
    return bd, dj




if __name__ == "__main__":
    p = [['B_M','M_M','M_M','B_Dou','B_M','M_M','M_M'],['B_M','M_M','B_J','B_J','B_J']]
    a = [['B_M','M_M','M_M','B_Dou','B_J','M_J','M_J'],['B_M','M_M','B_M','B_J','M_J']]

    r = evaluation(p, a)
    print(r)
