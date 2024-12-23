import sys

import gradio as gr

sys.path.append("../..")
from pycorrector import MacBertCorrector


def predict(text):
    return model.correct(text)


if __name__ == '__main__':
    model_path = 'E:\\pycorrector\\model\\macbert4csc-base-chinese'
    model = MacBertCorrector(model_path)

    examples = [
        ['真麻烦你了。希望你们好好的跳无'],
        ['少先队员因该为老人让坐'],
        ['机七学习是人工智能领遇最能体现智能的一个分知'],
        ['今天心情很好'],
        ['他法语说的很好，的语也不错'],
        ['他们的吵翻很不错，再说他们做的咖喱鸡也好吃'],
    ]

    gr.Interface(
        predict,
        inputs="text",
        outputs="text",
        title="Chinese Spelling Correction Model shibing624/macbert4csc-base-chinese",
        description="Copy or input error Chinese text. Submit and the machine will correct text.",
        examples=examples
    ).launch()
