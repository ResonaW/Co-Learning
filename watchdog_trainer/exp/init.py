from transformers import AutoTokenizer, AutoModelForSequenceClassification
import datetime
import os

# 初始模型
model_name = "hfl/chinese-macbert-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
if not os.path.exists('./models/%s/' % (now_str)):
    os.mkdir('./models/%s/' % (now_str))

model.save_pretrained('./models/%s/' % now_str)
tokenizer.save_pretrained('./tokenizer')