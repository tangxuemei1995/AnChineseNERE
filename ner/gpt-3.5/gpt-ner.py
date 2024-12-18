from easyinstruct import ICLPrompt
from easyinstruct.utils.api import set_openai_key
import json
import re
import random
import time
# Step1: Set your own API-KEY
set_openai_key("xxxxx")

# Step2: Declare a prompt class
prompt = ICLPrompt()

# Step3: Desgin a few task-specific examples


of = open('./dataset/train_ner_alpaca.json','r',encoding='utf-8')
train = []
r = of.read()
pattern = r'({.*?})'
r1 = re.findall(pattern,r)
for i in r1:
    dic = json.loads(i)
    train.append(dic)
of.close()
of = open('./dataset/test_ner_alpaca.json','r',encoding='utf-8')
test = []
r = of.read()
pattern = r'({.*?})'
r1 = re.findall(pattern,r)
for i in r1:
    dic = json.loads(i)
    test.append(dic)
of.close()


f = open('./test_ner_gpt.json','w',encoding='utf-8')
b = time.time()
count = 0
for d in test:
    count += 1
    if count > 859 or count==859:
        continue 
    # time.sleep(20)
    in_context_examples = []
    random.shuffle(train) #随机采样前面的数据，但是要保证每类实体都有出现
    have_all = []
    for train_example in train:
        if '书籍：无' not in train_example['output'] and "团体：无" not in train_example['output'] and "时间：无" not in train_example['output']:
            have_all.append(train_example)
        

    for i in range(0,4):
        in_context_examples.append({"input" :train[i]['input'],'output': '['+train[i]['output'].replace('。','') +']'})
    in_context_examples.append({"input":have_all[0]['input'],'output': '['+have_all[0]['output'].replace('。','')+']'})

    # print(in_context_examples)
#     exit()
    input = d['input']
      
# in_context_examples = [{"input": "后以风疾失音，致仕，加尚父，封赵王。薨，年八十，追封齐国王。", "output": "[人物：无；地点：无；职官：尚父，赵王，齐国王；书籍：无]"},
                         # {"input": "奂曰：「江有潘、陆之华，而无园、绮之实，辅弼储贰，窃谓非材。」后主深以为恨，乃自言于宣帝。", "output": "[人物：奂，江，潘，陆，园，绮，后主，宣帝；地点：无；职官：无；书籍：无]"}]
# input = '子宽，大将军、长乐郡公，先迥卒。宽兄谊，开府、资中郡公。宽弟顺，以迥平蜀功，授开府、安固郡公。'
# Step4: Build a prompt from the examples
    instruction = '你是一个实体是识别工具，你需要识别出输入句子中的人物、地点、职官和书籍，输出格式为列表：[人物：人物1，人物2；地点：地点1，地点2；职官：职官1，职官2；书籍：书籍1，书籍2；时间：时间1，时间2；团体：团体1，团体2]。除了这个列表以外请不要输出别的多余的话。input:' 
    x = prompt.build_prompt(instruction + input, in_context_examples, n_shots=5)
    # print(x)
    # exit()


# Step5: Get the result from LLM API service
    result = prompt.get_openai_result(engine="gpt-3.5-turbo")
    data = {'instruction':x.replace('\n','') , 'labels':d['output'],'GPT':result.replace(']','').replace('[','')}
    data = json.dumps(data, ensure_ascii=False)
    f.write(data + '\n')
    print(count)
# e = time.time()
# timeuse = e - b
# print(timeuse)
print('finished')
    
    
    # Examples:
 #    input: 晋荡公护。
 #    output: [人物：护；地点：无；职官：晋荡公；书籍：无]
 #
 #    input: 进爵广业郡公，转右司卫。时宣帝在东宫，亲狎谄佞，数有罪失。武帝于朝臣内选忠谅鲠正者以匡弼之，于是以运为右宫正。
 #    output: [人物：宣帝，武帝，运；地点：无；职官：广业郡公，右司卫，右宫正；书籍：无]
 #
 #    input: 子让能，字羣懿，擢进士第，从宣武王铎府为推官，以长安尉为集贤校理。丧母，以孝闻。又辟刘邺、牛蔚二府，稍进兵部员外郎。
 #    output: [人物：让能，羣懿，王铎，刘邺，牛蔚；地点：无；职官：进士，推官，长安尉，集贤校理，兵部员外郎；书籍：无]
 #
 #    input: 时年已老，日以时事为忧，虽食息顷不能忘。每闻一事可便民，一士可擢用，大则拜章，小则为当路者言，殷勤郑重，不能自已。三月，草开兴改元诏，闾巷閒皆能传诵，洛阳人拜诏毕，举城痛哭，其感人如此。
 #    output: [人物：无；地点：洛阳；职官：无；书籍：无]
 #
 #    input: 高祖南伐，以亮录尚书事，留镇洛阳。后高祖将自小平汎舟幸石济，亮谏曰：「臣闻垂堂之诲，振古成规，于安思危，著于周易。是以凭险弗防，没而不弔。
 #    output: [人物：高祖，亮，高祖，亮；地点：洛阳，小平，石济；职官：录尚书事；书籍：周易]
 #
 #    Questions
 #    你是一个实体是识别工具，你需要识别出输入句子中的人物、地点、职官和书籍，输出格式为列表：[人物：人物1，人物2；地点：地点1，地点2；职官：职官1，职官2；书籍：书籍1，书籍2]。除了这个列表以外请不要输出别的多余的话。input:或以问至德，荅曰：「夫庆赏刑罪，人主之权柄，凡为人臣，岂得与人主争权柄哉！」其慎密如此。后高宗知而深歎美之。仪凤四年薨，辍朝三日，使百官以次赴宅哭之，赠开府仪同三司、并州大都督，谥曰恭。
# print(result)



