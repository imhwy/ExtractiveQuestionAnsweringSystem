"""
This module is used for inference.
"""
import torch


class InferenceEngine:
    """
    This module is used for inference.
    """

    def __init__(self):
        print("using InferenceEngine!!!")


    async def load_input(self, tokenizer, context, question):
        """_summary_

        Returns:
            _type_: _description_
        """
        inputs = tokenizer(
            question,
            context,
            return_tensors="pt"
        )
        return inputs

    async def load_output(self, model, inputs):
        """_summary_

        Returns:
        """

        with torch.no_grad():
            outputs = model(**inputs)
        return outputs

    async def get_answer_index(self, outputs):
        """_summary_

        Returns:
        """

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()
        return answer_start_index, answer_end_index

    async def get_predict_answer_tokens(self, inputs, answer_start_index, answer_end_index):
        """_summary_

        Args:
            inputs (_type_): _description_
            answer_start_index (_type_): _description_
            answer_end_index (_type_): _description_

        Returns:
            _type_: _description_
        """
        predict_answer_tokens = inputs.input_ids[0,answer_start_index: answer_end_index + 1]
        return predict_answer_tokens

    async def decode_answer(self, tokenizer, predict_answer_tokens):
        """_summary_

        Args:
            tokenizer (_type_): _description_
            predict_answer_tokens (_type_): _description_

        Returns:
            _type_: _description_
        """

        predict_answer = tokenizer.decode(
            predict_answer_tokens,
            skip_special_tokens=True
        )

        return predict_answer

    async def inference_pipeline(self, tokenizer, model, context, question):
        """
        Execute the inference pipeline for a question-answering task.

        Args:
            tokenizer: The tokenizer to preprocess the context and question.
            model: The model to generate predictions.
            context (str): The context in which the question needs to be answered.
            question (str): The question for which the answer is sought.

        Returns:
            str: The predicted answer to the question based on the provided context.
        """
        inputs = await self.load_input(
            tokenizer=tokenizer,
            context=context,
            question=question
        )
        outputs = await self.load_output(
            model=model,
            inputs=inputs
        )
        start_answer_digits, end_answer_digits = await self.get_answer_index(outputs=outputs)
        predict_answer_tokens = await self.get_predict_answer_tokens(
            inputs=inputs,
            answer_start_index=start_answer_digits,
            answer_end_index=end_answer_digits
        )
        modified_result = await self.decode_answer(
            tokenizer=tokenizer,
            predict_answer_tokens=predict_answer_tokens
        )
        return modified_result
