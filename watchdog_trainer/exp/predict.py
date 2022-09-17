def get_prediction(inputs, model, tokenizer, is_text):
    if is_text is True:
        # prepare our text into tokenized sequence
        inputs = tokenizer(inputs, padding=True, truncation=True, max_length=256, return_tensors="pt").to("cuda")
    # perform inference to our model
    outputs = model(**inputs)
    # get output probabilities by doing softmax
    probs = outputs[0].softmax(1)
    # executing argmax function to get the candidate label
    return probs.tolist()[0],int(probs.argmax())