import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split


# 数据集构造
class My_Dataset(Dataset):
    def __init__(self,dataframe, tokenizer):
        df = dataframe.sample(frac=1.0).reset_index(drop=True)
        self.x = tokenizer(df['标题/微博内容'].tolist(), truncation=True, padding=True, max_length=256)
        self.y = df['label'].tolist()
 
    def __getitem__(self, index):
        item = {k: torch.tensor(v[index]) for k, v in self.x.items()}
        item['label'] = torch.tensor([self.y[index]])
        return item
 
    def __len__(self):
        return len(self.y)

def import_dataset(path='/home/ubuntu/Otree_Project/Co-Learning/co_learning/情感分析_20220915.xlsx'):
    df = pd.read_excel(path)
    df['label'] = df['情感预测'].apply(lambda x:1 if x=='积极' else 0)
    test_df = df.iloc[100:120]
    return test_df