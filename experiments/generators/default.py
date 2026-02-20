import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .utils import INSTRUCTIONS

class DefaultGenerator():
    def __init__(self, model, structured_chat=False):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            dtype=torch.bfloat16,
            device_map="auto",
        )
        self.structured_chat = structured_chat


    def _format_messages(self, candidate, target):
        if self.structured_chat:
            return [
                {"role": "system", "content": [{"type": "text", "text": INSTRUCTIONS}]},
                {"role": "user", "content": [{"type": "text", "text": f"candidate: {candidate}\ntarget: {target}"}]}
            ]
        else:
            return [
                {"role": "system", "content": INSTRUCTIONS},
                {"role": "user", "content": f"candidate: {candidate}\ntarget: {target}"}
            ]

    def predict_revision(self, candidate, target):
        messages = self._format_messages(candidate, target)
        text = self.tokenizer.apply_chat_template(
            messages, 
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=200,
            do_sample=False
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

        content = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return content

