from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import PegasusConfig, PegasusModel
import torch
from datasets import load_dataset

def evaluate():
    dataset = load_dataset('billsum', split="test")
    '''txt_path = "/kaggle/input/feedback-prize-2021/train/0000D23A521A.txt"

    with open(txt_path, "rt") as f:
        txt = f.read()'''
    tests = dataset["text"]
    #print(tests[0])
    model_name = "google/pegasus-xsum"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    batch = tokenizer(tests, truncation=True, max_length=150, padding="longest", return_tensors="pt").to(device)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    #print(" ".join(tgt_text))
    text_file = open("summaries.csv", "w")
    text_file.write("************ \n".join(tgt_text))
    text_file.close()

if __name__ == "__main__":
    evaluate()


# Initializing a PEGASUS google/pegasus-large style configuration
#configuration = PegasusConfig()

# Initializing a model (with random weights) from the google/pegasus-large style configuration
#model = PegasusModel(configuration)

# Accessing the model configuration
#configuration = model.config