from django.shortcuts import render
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)
from peft import PeftModel
import json
from django.http import JsonResponse

MODEL_ID = "./flan-phraser/paraphraser/llms/flan-V6-LargeBest"


def initModelAndTokenizer(modelID: str):
    baseModelImport = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    peftModelTest = PeftModel.from_pretrained(
        baseModelImport, modelID, is_trainable=False
    )
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return peftModelTest, tokenizer


baseModel, tokenizer = initModelAndTokenizer(MODEL_ID)
print("Log ---------------- Model and tokenizer Loaded")


def BartesianInput(request):
    if request.method == "GET":
        return render(request, "paraphrase.html")


def Paraphraser(request):
    if request.method == "POST":
        print("Helloo")
        payload = json.loads(request.body)
        queryText = payload["inputText"]
        # queryTextLegth = len(queryText.split(" "))
        prompt = [
            f'Paraphrase this sentence without changing its meaning: "{queryText}"'
        ]
        tokenizedPrompt = tokenizer(
            prompt,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
            max_length=216,
        )
        inputIds = tokenizedPrompt["input_ids"]
        attentionMask = tokenizedPrompt["attention_mask"]
        # print(inputIds)
        # print(attentionMask)
        outputs = baseModel.generate(
            input_ids=inputIds,
            max_new_tokens=216,
            temperature=0.7,
            attention_mask=attentionMask,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            top_k=50,
            top_p=0.9,
        )
        # print(outputs)
        textedOutput = tokenizer.decode(
            outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        # print("Prompt-------------")
        # print(prompt[0])
        # print("\nModel Output-------")
        # print(textedOutput)
        context = {"outputText": textedOutput}
        return JsonResponse(data=context)
