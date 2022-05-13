#!/usr/bin/env python3
# T5 Finetuning
# PEGASUS paraphraser
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from Levenshtein import distance
from newspaper import Article
import nltk
import people_also_ask
import yake
import spacy
import re
import cloudscraper
import newspaper
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

paraphraser_model_name = 'E:\\Project\\Passive-Adsenses-Blog\\Paraphraser\\model\\fine-tune-pegasus-paraphraser'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
paraphraser_tokenizer = PegasusTokenizer.from_pretrained(paraphraser_model_name,local_files_only=True)
paraphraser_model = PegasusForConditionalGeneration.from_pretrained(paraphraser_model_name,local_files_only=True).to(torch_device)
# paraphraser_tokenizer.save_pretrained("./model/fine-tune-pegaus-pharaphraser/tokenizer")
# paraphraser_model.save_pretrained("./model/fine-tune-pegaus-pharaphraser/model")

def paraphrase_question(question,num_return_sequences=10,num_beams=40):
   return sorted(filter(lambda x: True if x.endswith('?') else False , paraphrase_sentence(question,num_return_sequences,num_beams)),key=lambda x: distance(x,question), reverse=True)[0]

def paraphrase_article(corpus):
  paraphrased_corpus = ""
  num_beams = 40
  num_return_sequences = 10
  for index,sent in tqdm(enumerate(corpus.split("\n")),'Paraphrasing article'):
    if index % 2 == 0:
      print('Sub topic:',sent)
      try:
        new_sent = paraphrase_question(sent,num_return_sequences,num_beams)
      except:
        lst_paraphrase = paraphrase_sentence(sent,num_return_sequences,num_beams)
        new_sent = sorted(lst_paraphrase,key=lambda x: distance(sent,x),reverse=True)[0]
    else:
      doc = nlp(sent)
      new_sent = ""
      for sent in list(doc.sents):
        lst_paraphrase = paraphrase_sentence(sent.text,10,40)
        new_sent = new_sent + " " + sorted(lst_paraphrase,key=lambda x: distance(sent.text,x),reverse=True)[0]
      # lst_paraphrase = paraphrase_sentence(sent,num_return_sequences,num_beams)
      # new_sent = sorted(lst_paraphrase,key=lambda x: distance(sent,x),reverse=True)[0]
      new_sent = new_sent.strip()
    paraphrased_corpus = paraphrased_corpus + new_sent + "\n"
  return 

def paraphrase_sentence(input_text,num_return_sequences=10,num_beams=40):
  batch = paraphraser_tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = paraphraser_model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = paraphraser_tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text

def paraphrase_corpus(corpus):
  for paragraph in corpus.split("\n\n"):
    doc = nlp(paragraph)
    new_paragraph = ""
    for sentence in list(doc.sents):
      lst_paraphrase = paraphrase_sentence(sentence.text)
      result = sorted(lst_paraphrase,key=lambda x: distance(sentence.text,x),reverse=True)[0]
      new_paragraph += result

def paraphrased_list_article(corpus):
  # legalzoom.com
  paraphrased_article = ""
  template_point = r'\s*^[0-9].\s*'
  template_example = ''
  for paragraph in corpus.split("\n\n"):
    new_paragraph = ""
    for line in paragraph.split("\n"):
      new_line = ""
      for sentence in nltk.tokenize.sent_tokenize(line):
        # Detect point2
        if bool(re.match(template_point,sentence)) or sentence.find(":") !=-1:
          new_line += sentence 
        else:
          lst_paraphrase = paraphrase_sentence(sentence)
          result = sorted(lst_paraphrase,key=lambda x: distance(sentence,x),reverse=True)[0]
          new_line += result
      new_paragraph += new_line + "<br>"
    paraphrased_article = paraphrased_article + new_paragraph + "<br><br>"
  return paraphrased_article

if __name__ == '__main__':
  print('GPU Available:',torch.cuda.is_available())
  # Read input
  data = os.listdir('./input')[0]
  print("Read Input...")
  with open(f"./input/{data}",'r') as f:
    corpus = f.read()
  print("Paraphrasing Input...")
  result = paraphrased_list_article(corpus)
  print("Saving Input...")
  with open(f'./output/{data}',"w+") as f: 
    f.write(result)
  print("Done...")
  
  
  
  