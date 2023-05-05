"""
This is a boilerplate pipeline 'news_data'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func= get_news_data,
                inputs="params:proxies",
                outputs="news_data",
                name="get_news_data",
            )
    ])
