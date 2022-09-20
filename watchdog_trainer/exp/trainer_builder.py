from transformers import Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, cohen_kappa_score

# 评价指标构造
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    # calculate accuracy using sklearn's function
    acc = accuracy_score(labels, preds)
    kap = cohen_kappa_score(labels, preds)
    return {
      'accuracy': acc, 'kappa':kap
    }

# training_args = TrainingArguments(
#     output_dir='./results',          # output directory
#     num_train_epochs=5,              # total number of training epochs
#     per_device_train_batch_size=16,  # batch size per device during training
#     per_device_eval_batch_size=16,   # batch size for evaluation
#     learning_rate=1e-5,
#     weight_decay=0.01,               # strength of weight decay
#     logging_dir='./logs',            # directory for storing logs
#     load_best_model_at_end=True,     # load the best model when finished training (default metric is loss)
#     logging_steps=1000,               # log & save weights each logging_steps
#     save_steps=1000,
#     evaluation_strategy="steps",     # evaluate each `logging_steps`
# )

# only save model training args

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=1,              # total number of training epochs
    per_device_train_batch_size=8,  # batch size per device during training
    per_device_eval_batch_size=8,   # batch size for evaluation
    warmup_steps=500,
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
)

def build_trainer(model,train_dataset,test_dataset):
    trainer = Trainer(
        model=model,                         # the instantiated Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=test_dataset,          # evaluation dataset
        compute_metrics=compute_metrics,     # the callback that computes metrics of interest
    )
    return trainer