from kedro.pipeline import Pipeline, node, pipeline
from .nodes import get_news_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([])
