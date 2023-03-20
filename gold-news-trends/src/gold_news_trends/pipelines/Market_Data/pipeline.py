from kedro.pipeline import Pipeline, node, pipeline
import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            name= 'get market data from twelvedata api',
            func= nodes.get_market_data,
            inputs=["params:url", "params:url_parameters"],
            outputs='market_data'
        ),
        node(
            name= 'process market data',
            func= nodes.process_market_data,
            inputs=["market_data"],
            outputs='market_data'
        )
    ])
