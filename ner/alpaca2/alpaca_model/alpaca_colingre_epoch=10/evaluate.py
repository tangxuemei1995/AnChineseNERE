

'''
coling ner评测
'''
import json



def each_class_f1(labels,y_pre,y_true,true_labels): 
        # labels = list(set([line.strip().split('(')[0] for line in open('/ceph/home/jun01/tangxuemei/re/data/coling/relation2id.tsv')] ))   
        count_predict, count_total,count_right = {'other':0}, {'other':0}, {'other':0}
        for x in labels:
            count_predict[x] = 0
            count_total[x] = 0
            count_right[x] = 0
        for y1,y2 in zip(y_pre,y_true):
               print(y1,y2)
               if y1 not in labels:
                    count_predict['other']+=1
               else:
                    count_predict[y1]+=1
               count_total[y2]+=1
               if y1==y2:
                   count_right[y1]+=1
        test_precision, test_recall= {}, {}

        for x in labels:
            test_precision[x] = 0
            test_recall[x] = 0
        correct, pre, true =0,0,0

        for i in labels:
               correct += count_right[i]
               pre += count_predict[i]
               true += count_total[i]
               
               if count_predict[i]!=0 :
                   test_precision[i] = float(count_right[i])/count_predict[i]
            
               if count_total[i]!=0:
                   test_recall[i] = float(count_right[i])/count_total[i]
            
        test_f1s, test_p, test_r = {}, {}, {}
        for x in labels:
            test_f1s[x] = 0
            test_p[x] = 0
            test_r[x] = 0

        for i in labels:
            if test_precision[i] == 0 and test_recall[i] == 0:
                test_f1s[i] = 0
                test_p[i] = 0
                test_r[i] = 0
            else:
                test_f1s[i] = (2*test_precision[i]*test_recall[i])/(test_precision[i]+test_recall[i])
        microp,micror,microf1 = 0,0,0
        f2 = open('/ceph/home/jun01/tangxuemei/re/tmp/zztj/siku_roberta/coling/f1.txt','w',encoding='utf-8')
        for x in test_f1s:
            if x in labels:
               microf1 += test_f1s[x]
               microp += test_precision[x]
               micror += test_recall[x]

               f2.write(x + '\t' + str(test_precision[x]*100) + '\t' + str(test_recall[x]*100)+ '\t' + str(test_f1s[x]*100) + '\n')
               print(x,test_precision[x], test_recall[x], str(test_f1s[x]))
        print('平均值microf1', microp/len(labels),micror/len(labels),microf1/len(labels))
        print('平均值macrof1', correct/pre*100,correct/true*100,(2*(correct/pre*100)*(correct/true*100))/((correct/pre*100)+(correct/true*100)))
        f2.write(str((microf1/len(labels))*100))
#仅分类
import json
true, pre = [], []
no_pre_relation = 0
corr, act = 0, 0

# for line in open('/ceph/home/jun01/tangxuemei/glm2/ptuning/output/re-128-2e-2/generated_predictions.txt'):

#     line = line.strip().split(' [/INST] ')[1]
#     line = line.split('</s>		true label:	')
#     if len(line) != 2:
        
#         continue
#     pre_sen, true_sen = line[0].split('；'), line[1].split('；')
#     pre_sen = [x.replace('。','') for x in pre_sen]
#     print(pre_sen)
#     exit()
#     for x in true_sen:
#         if x == '':
#               continue
#         x = x.replace('。','')
#         act += 1
#         if x in pre_sen:
#             corr += 1
# print(corr/act)
def eval_ner_alpaca(path):

    trues, pres, labels = [], [], []
    f = open(path,'r',encoding='utf-8')
    text = f.read().split('\n')
    for line in text:
        print(line)
        line = line.split('[/INST] ')[1]
        pre,true = line.split('</s>		true label:')
        print(line)

        # true,pre = line[0].replace('{"labels": "',''),line[1].replace('"}','')
        pre = pre.split('，')[1]
        
        true = true.split('，')[1]
        # print(true,pre)
        # exit()
        trues.append(true)
        pres.append(pre)
    # print(trues)
    # print(pres)
    labels = pres + trues
    labels = list(set(labels))

    true_labels = list(set(trues))
    # true_labels.append('other')
    # print(true_labels)
    # exit()
    each_class_f1(true_labels, pres, trues, true_labels)

        

if __name__=="__main__":
    eval_ner_alpaca('test_result.txt')


# 驻守 0.6290322580645161 0.7222222222222222 0.6724137931034483
# 管理 0.4230769230769231 0.39285714285714285 0.4074074074074074
# 兄弟 0.5384615384615384 0.7 0.608695652173913
# 到达 0.7037037037037037 0.6333333333333333 0.6666666666666667
# 出生于某地 1.0 0.8076923076923077 0.8936170212765957
# 政治奥援 0.6049382716049383 0.494949494949495 0.5444444444444444
# 父母 0.8679245283018868 0.8070175438596491 0.8363636363636363
# 上下级 0.672 0.7850467289719626 0.7241379310344829
# 敌对攻伐 0.7846153846153846 0.8138297872340425 0.7989556135770236
# 任职 0.9765625 0.9920634920634921 0.9842519685039369
# 同僚 0.6065573770491803 0.5522388059701493 0.578125
# 别名 0.6875 0.5789473684210527 0.6285714285714286
# 平均值microf1 0.7078643737398392 0.6900165189645707 0.695304213593582
# 平均值macrof1 77.67094017094017 77.5880469583778 77.62947143619861