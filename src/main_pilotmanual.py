import os
import src
from src.logging_handler import logger

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
import torch


PATH = os.path.join(os.path.dirname(os.path.abspath(src.__file__)), "..")
DATA_PATH = os.path.join(PATH, "data")

gpu = torch.cuda.is_available()
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
retriever = DensePassageRetriever(document_store=document_store, use_gpu=gpu)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=gpu, num_processes=1)
pipe = ExtractiveQAPipeline(reader, retriever)


def main(json_data):
    question = json_data['question']

    prediction = pipe.run(
        query=question
    )
    answers = []
    for answer in prediction['answers'][:10]:
        answers.append({
            'answer': answer.answer,
            'document': answer.meta['name'],
            'chapter': f"{answer.meta['chapter_number']} {answer.meta['chapter']}",
            'section': f"{answer.meta['section_number']} {answer.meta['section']}",
            'subsection': f"{answer.meta['subsection']}"
        })

    return {'result': answers}