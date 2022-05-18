from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline, set_seed
import torch
set_seed(88)
# from Paraphraser.paraphraser import torch_device
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# enhancer_tokenizer = GPT2Tokenizer.from_pretrained(enhancer_model_name)
# enhancer_model = GPT2LMHeadModel.from_pretrained(enhancer_model_name)
enhancer_model_name = "E:\\Project\\Passive-Adsenses-Blog\\Enhancer\\model\\gpt2-large"
enhancer_tokenizer = GPT2Tokenizer.from_pretrained(enhancer_model_name)
enhancer_model = GPT2LMHeadModel.from_pretrained(enhancer_model_name)

def enhance_sentence(text):
    input_ids = enhancer_tokenizer.encode(text, return_tensors='pt')
    sample_outputs = enhancer_model.generate(
        input_ids,
        do_sample=True, 
        max_length=50,
        no_repeat_ngram_size=2, 
        top_k=50, 
        top_p=0.95, 
        num_return_sequences=3
    )
    print("Output:\n" + 100 * '-')
    for i, sample_output in enumerate(sample_outputs):
        print("{}: {}".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))
