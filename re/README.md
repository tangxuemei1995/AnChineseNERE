# Pytorch Implementation of BERT-based Relation Classification

###Realtion Data
./data/paper

### Requirements:
 
Python version >= 3.6 (recommended)

Pytorch version >= 1.1 (recommended)

pytorch-transformers: https://github.com/huggingface/pytorch-transformers  
!!! pytorch-transformers = 1.1 




### Tutorial of the code

1. Train the bert-based classification model

```
> python bert.py --config config.ini
```

```
...
09/11/2019 16:36:31 - INFO - pytorch_transformers.modeling_utils -   loading weights file /tmp/semeval/pytorch_model.bin
09/11/2019 16:36:33 - INFO - __main__ -   Loading features from cached file ./dataset/cached_dev_bert-large-uncased_128_semeval
09/11/2019 16:36:33 - INFO - __main__ -   Saving features into cached file ./dataset/cached_dev_bert-large-uncased_128_semeval
09/11/2019 16:36:34 - INFO - __main__ -   ***** Running evaluation  *****
09/11/2019 16:36:34 - INFO - __main__ -     Num examples = 2717
09/11/2019 16:36:34 - INFO - __main__ -     Batch size = 8
Evaluating: 100%|████████████████████████████████████████████████████| 340/340 [00:46<00:00,  7.24it/s]
09/11/2019 16:37:21 - INFO - __main__ -   ***** Eval results  *****  
10/07/2019 10:02:23 - INFO - __main__ -     acc = 0.8579315421420685
10/07/2019 10:02:23 - INFO - __main__ -     acc_and_f1 = 0.8579315421420685
10/07/2019 10:02:23 - INFO - __main__ -     f1 = 0.8579315421420685
```

2. Evaluate using the official script

```
> bash test.sh
```
