from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.file_utils import is_torch_available

import os
import torch

def import_model(path=None):
    if torch.cuda.is_available() == is_torch_available() == True:
        print("cuda ready.")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        raise ValueError
    if path is not None:
        model = AutoModelForSequenceClassification.from_pretrained(path, num_labels=2).to("cuda")
    else:
        # dirs_list = []
        # for root, dirs, _ in os.walk('./models/', topdown=False):
        #     dirs_list.append(dirs)
        # latest_dir = root + '/' + max(dirs_list)
        model = AutoModelForSequenceClassification.from_pretrained("/home/ubuntu/Otree_Project/models/online_shopping_dataset_60model", num_labels=2).to("cuda")
    return model

def import_tokenizer(path=None):
    if path is not None:
        tokenizer = AutoTokenizer.from_pretrained(path)
    else:
        tokenizer = AutoTokenizer.from_pretrained('/home/ubuntu/Otree_Project/models/online_shopping_dataset_60model')
    return tokenizer