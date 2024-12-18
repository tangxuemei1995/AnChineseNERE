


def eval_ner_alpaca(path):
    of = open(path,'r',encoding='utf-8')
    pre = []
    r = of.read()[0:]
    pattern = r'({.*?})'
    r1 = re.findall(pattern,r)
    for i in r1:
        dic = json.loads(i)
        pre.append(dic)
    of.close()
    pre_number, true_number, correct_number = 0, 0, 0
    pre_number_per, true_number_per, correct_number_per = 0, 0, 0
    pre_number_loc, true_number_loc, correct_number_loc = 0, 0, 0
    pre_number_ofi, true_number_ofi, correct_number_ofi = 0, 0, 0
    pre_number_book, true_number_book, correct_number_book = 0, 0, 0
    true_count, pre_count,correct_count = {'人物': 0, '地点': 0, '职官': 0, '书籍': 0, '时间': 0, '团体': 0}, {'人物': 0, '地点': 0, '职官': 0, '书籍': 0, '时间': 0, '团体': 0}, {'人物': 0, '地点': 0, '职官': 0, '书籍': 0, '时间': 0, '团体': 0}

    for line in pre:
        
        pre, true = line['GPT'], line['labels']
        pre = pre.split('；')
        
        true = true.split('；')
        print(pre,true)
        pre_d, true_d = {}, {}
        
        for i in range(len(pre)):   
            pre_d[pre[i].split('：')[0]] = pre[i].split('：')[1].replace('。','').split('，')

        for i in range(len(true)):
            true_d[true[i].split('：')[0]] = true[i].split('：')[1].replace('。','').split('，')
        
        
        for key in true_d.keys():
            if true_d[key] != ['无']:
                true_count[key] += len(true_d[key])
            if key in pre_d.keys():
                if pre_d[key] != ['无']: 
                    pre_count[key]+= len(pre_d[key])
                if pre_d[key] != ['无'] and true_d[key] != ['无']:
                    for x in true_d[key]:
                        if x in pre_d[key]:
                            index = pre_d[key].index(x)
                            pre_d[key].pop(index)
                            correct_count[key] += 1
    microf1 = 0
    correct_number = 0
    pre_number = 0
    true_number = 0
    # print(pre_count,true_count, correct_count)
    # exit()
    for key in pre_count.keys():

        print(key)
        p_per = (correct_count[key]/pre_count[key])*100
        r_per = (correct_count[key]/true_count[key])*100
        f_per = (2*p_per*r_per)/(p_per + r_per)
        print('p', p_per)
        print('r', r_per)
        print('f', f_per)


        microf1 += f_per
        correct_number += correct_count[key]
        true_number += true_count[key]
        pre_number += pre_count[key]


    print('microf1',microf1/6)

    macroP = (correct_number/pre_number)*100
    macroR = (correct_number/true_number)*100
    macroF = (2*macroP*macroR)/(macroP+macroR) 
    print('macroP',macroP)
    print('macroR',macroR)
    print('macroF',macroF)


if __name__=="__main__":
    
    
    
#     from easyinstruct.utils.api import set_openai_key
    import json
    import re


    # of = open('/Users/tangtang/Desktop/投稿/coling/ner_alpaca/test_ner_alpaca.json','r',encoding='utf-8')
    # test = []
    # r = of.read()[0:]
    # pattern = r'({.*?})'
    # r1 = re.findall(pattern,r)
    # for i in r1:
    #     dic = json.loads(i)
    #     test.append(dic)
    # of.close()
    # of = open('/Users/tangtang/Desktop/投稿/coling/ner_alpaca/test_gpt.json','r',encoding='utf-8')
    # pre = []
    # r = of.read()[0:]
    # pattern = r'({.*?})'
    # r1 = re.findall(pattern,r)
    # for i in r1:
    #     dic = json.loads(i)
    #     pre.append(dic)
    # of.close()
    # print(len(test),len(pre))
    # for i in range(len(test)):
    #     if test[i]['input'].strip() != pre[i]['instruction'].split('话。input:')[1].strip():
    #         print(test[i]['input'])
    #         print(pre[i]['instruction'].split('话。input:')[1]).strip()
    #         # exit()
    #         print(i)
    
    eval_ner_alpaca('./test_ner_gpt_all.json')

#GPT 5-shot
# 人物
# p 77.17478052673583
# r 58.96341463414634
# f 66.85101970273072
# 地点
# p 72.20259128386337
# r 63.58921161825726
# f 67.62272476558192
# 职官
# p 41.50197628458498
# r 45.258620689655174
# f 43.29896907216495
# 书籍
# p 45.13888888888889
# r 40.625
# f 42.76315789473685
# 时间
# p 62.96296296296296
# r 48.29545454545455
# f 54.662379421221864
# 团体
# p 5.982905982905983
# r 35.0
# f 10.218978102189782
# microf1 47.569538159771014
# macroF 61.98889449772842