from exp.import_model import import_model, import_tokenizer
from exp.import_dataset import import_dataset, My_Dataset
from exp.trainer_builder import build_trainer

from watchdog.observers import Observer
from watchdog.events import *

import re
import pandas as pd
import time
import shutil
from datetime import datetime

def delete_folder_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

class FileEventHandler(FileSystemEventHandler):
    
    def __init__(self, test_dataset, model, tokenizer) -> None:
        super().__init__()
        # 正式使用时记得删除这一部分
        self.target_path = '/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/'
        delete_folder_content('/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/')
        # 在主程序里load初始模型，数据集，tokenizer，在这里使用
        self.test_dataset = test_dataset
        self.model = model
        self.tokenizer = tokenizer
        self.log_list = []

    def on_any_event(self, event):
        pass

    def on_moved(self, event):
        pass

    def on_created(self, event):
        if event.is_directory:
            # print("directory created:{0}".format(event.src_path))
            pass
        else:
            # 新出现的csv文件，进行模型训练和预测
            # print("file created:{0}".format(event.src_path))
            file_name = re.search('(\w+)\.csv',event.src_path).group(1)
            if (file_name not in self.log_list) and ('manual' not in file_name):
                print("%s提交100条训练" % file_name)
                self.log_list.append(file_name)
                # 模型训练阶段
                time.sleep(3)
                train_df = pd.read_csv(event.src_path)
                train_dataset = My_Dataset(train_df, self.tokenizer)
                trainer = build_trainer(model=self.model, train_dataset=train_dataset, test_dataset=self.test_dataset)
                trainer.train()
                # 模型预测
                labels = trainer.predict(self.test_dataset).label_ids.tolist()
                test_df_model = pd.DataFrame()
                test_df_model['label'] = labels
                csv_name = file_name + '_test_model'
                self.log_list.append(file_name)
                test_df_model.to_csv(self.target_path+csv_name+'.csv',index=False)
                time.sleep(3)
                print("%s模型输出20条完成"  % file_name)
            if 'manual' in file_name:
                self.log_list.append(file_name)
                print("%s提交20条测试" % file_name)


    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

if __name__ == "__main__":
    import time
    model = import_model()
    tokenizer = import_tokenizer()
    test_df = import_dataset()
    test_dataset = My_Dataset(test_df, tokenizer)
    observer = Observer()
    event_handler = FileEventHandler(model=model, tokenizer=tokenizer, test_dataset=test_dataset)
    observer.schedule(event_handler, "/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/", True)
    observer.start()
    print("-----Ready-----")
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        with open(r'/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/logging.txt','w',encoding='utf-8') as f:
            f.writelines(event_handler.log_list)
            f.close()
        observer.stop()