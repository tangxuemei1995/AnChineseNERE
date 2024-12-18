

def pre_for_llm(path):
    '''将NER的conll格式转化为LLM训练的格式'''
    f = open(path, 'r', encoding='utf-8')
    text = f.read()
    f2 = open(path.replace('.txt','_ner_alpaca.json'),'w',encoding='utf-8')
    f3 = open(path.replace('.txt','_ner_glm.json'),'w',encoding='utf-8')
    
    instruction = '你是一个实体是识别工具，你需要识别出输入句子中的人物、地点、职官、书籍、时间和团体，输出格式为：人物：人物1，人物2；地点：地点1，地点2；职官：职官1，职官2；书籍：书籍1，书籍2；时间：时间1，时间2；团体：团体1，团体2。'
    text = text.split('\n\n')
    for line in text:
        line = line.strip().split('\n')
        sen = ''
        d = {'PER':[],'BOOK':[],'OFI':[],'LOC':[],'TIME':[],'GPE':[]}
        entity = ''
        type = ''
        for char_tag in line:
            char_tag = char_tag.split('\t')
            if len(char_tag) != 2:
                 continue
            char,tag = char_tag[0], char_tag[1]
            sen += char
            if tag.startswith('B'):
                type = tag.replace('B-','')
                entity += char
            elif tag.startswith('I'):
                entity += char
            elif tag.startswith('E'):
                entity += char
                if type != '':
                    d[type].append(entity)
                    entity, type = '', ''
                else:
                    print('没有实体类型')

            elif tag.startswith('S'):
                entity = char
                type = tag.replace('S-','')
                d[type].append(entity)
                entity, type = '', ''
        output = ''
        if d['PER'] != []:
            output += '人物：' + '，'.join(d['PER']) + '；'
        else:
            output += '人物：无；'
        if d['LOC'] != []:
            output += '地点：' + '，'.join(d['LOC']) + '；'
        else:
            output += '地点：无；'
        if d['OFI'] != []:
            output += '职官：' + '，'.join(d['OFI']) + '；'
        else:
            output += '职官：无；'

        if d['BOOK'] != []:
            output += '书籍：' + '，'.join(d['BOOK']) + '；'
        else:
            output += '书籍：无；'
        if d['TIME'] != []:
            output += '时间：' + '，'.join(d['TIME']) + '；'
        else:
            output += '时间：无；'

        if d['GPE'] != []:
            output += '团体：' + '，'.join(d['GPE']) + '。'
        else:
            output += '团体：无。'

        data =  {'instruction':instruction,'input':sen,'output':output}
        import json
        # data = {"instruction":instruction,"input":input,'output':output}
      
        data = json.dumps(data, ensure_ascii=False)

        f2.write(data + '\n')
        instruction1 = instruction + '输入的句子是：' + sen
        data = {'content':instruction1 , 'answer':output}
        data = json.dumps(data, ensure_ascii=False)

        f3.write(data + '\n')

if __name__ == "__main__":

    pre_for_llm('./dataset/train.txt')