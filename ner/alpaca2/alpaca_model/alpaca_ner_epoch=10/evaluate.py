


def eval_ner_alpaca(path):

    pre_number, true_number, correct_number = 0, 0, 0
    pre_number_per, true_number_per, correct_number_per = 0, 0, 0
    pre_number_loc, true_number_loc, correct_number_loc = 0, 0, 0
    pre_number_ofi, true_number_ofi, correct_number_ofi = 0, 0, 0
    pre_number_book, true_number_book, correct_number_book = 0, 0, 0
    for line in open(path):
        line = line.split(' [/INST] ')
        pre, true = line[1].split('</s>		true label:	')
        pre = pre.replace('。','').split('；')
        
        true = true.replace('。','').replace('\n','').split('；')
        for i in range(len(pre)):
            if i == 0:
                pre_per = pre[i].split('：')[1].split('，')
                true_per = true[i].split('：')[1].split('，')
                if true_per != ['无']:
                    pre_number_per += len(pre_per)
                    true_number_per += len(true_per)

                    for x in true_per:
                        if x in pre_per:
                            index = pre_per.index(x)
                            pre_per.pop(index)
                            correct_number_per += 1
            elif i == 1:
                pre_loc = pre[i].split('：')[1].split('，')
                true_loc = true[i].split('：')[1].split('，')

                if true_loc != ['无']:
                    pre_number_loc += len(pre_loc)
                    true_number_loc += len(true_loc)
                    for x in true_loc:
                        if x in pre_loc:
                            index = pre_loc.index(x)
                            pre_loc.pop(index)
                            correct_number_loc += 1
            elif i == 2:
                pre_ofi = pre[i].split('：')[1].split('，')
                true_ofi = true[i].split('：')[1].split('，')
                
                if true_ofi != ['无']:
                    pre_number_ofi += len(pre_ofi)
                    true_number_ofi += len(true_ofi)
                    for x in true_ofi:
                        if x in pre_ofi:
                            index = pre_ofi.index(x)
                            pre_ofi.pop(index)
                            correct_number_ofi += 1
            elif i == 3:
                pre_book = pre[i].split('：')[1].split('，')
                true_book = true[i].split('：')[1].split('，')
                
                if true_book != ['无']:
                    print(true_book)
                    pre_number_book += len(pre_book)
                    true_number_book += len(true_book)
                    # print(true_number)
                    # print(pre_book)
                    for x in true_book:
                        if x in pre_book:
                            index = pre_book.index(x)
                            pre_book.pop(index)
                            correct_number_book += 1
    # print(pre_number_book,correct_number_book)
    # exit()
    p_per = (correct_number_per/pre_number_per)*100
    r_per = (correct_number_per/true_number_per)*100
    f_per = (2*p_per*r_per)/(p_per + r_per)

    p_loc = (correct_number_loc/pre_number_loc)*100
    r_loc = (correct_number_loc/true_number_loc)*100
    f_loc = (2*p_loc*r_loc)/(p_loc + r_loc)

    p_ofi = (correct_number_ofi/pre_number_ofi)*100
    r_ofi = (correct_number_ofi/true_number_ofi)*100
    f_ofi = (2*p_ofi*r_ofi)/(p_ofi + r_ofi)

    p_book = (correct_number_book/pre_number_book)*100
    r_book = (correct_number_book/true_number_book)*100
    f_book = (2*p_book*r_book)/(p_book + r_book)

    print('PER',p_per, r_per, f_per)

    print('LOC',p_loc, r_loc, f_loc)

    print('OFI',p_ofi, r_ofi, f_ofi)

    print('BOOK',p_book, r_book, f_book)

    microf1 = (f_per + f_loc + f_ofi + f_book)/4
    print('macrof1',microf1)
    correct_number = correct_number_per + correct_number_loc + correct_number_ofi + correct_number_book
    pre_number = pre_number_per + pre_number_loc + pre_number_ofi + pre_number_book
    true_number = true_number_per + true_number_loc + true_number_ofi + true_number_book
    macroP = (correct_number/pre_number)*100
    macroR = (correct_number/true_number)*100
    macroF = (2*macroP*macroR)/(macroP+macroR) 

    print('microF',macroF)


if __name__=="__main__":
    eval_ner_alpaca('test_result.txt')



# PER 90.28985507246377 87.62306610407876 88.93647394718059
# LOC 89.10411622276028 86.58823529411764 87.82816229116945
# OFI 78.36990595611285 76.68711656441718 77.51937984496122
# BOOK 63.63636363636363 53.84615384615385 58.33333333333333
# macrof1 78.15433735416114
# microF 85.8321870701513
