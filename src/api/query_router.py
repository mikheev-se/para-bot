from time import time
from fastapi import APIRouter
from src.service.params_recognition_service import ParamsService
from src.service.query_recognition_service import QueryService

query_router = APIRouter(
    prefix='/query',
    tags=['query']
)

query_service = QueryService()
params_service = ParamsService()


@query_router.get('', response_model=None)
def handle_query(query: str):
    start = time()
    params, new_query = params_service.get_params(query)
    base_query_params, score_params = query_service.evaluate(new_query)
    base_query_no_params, score_no_params = query_service.evaluate(query)
    base_query = base_query_params if score_params > score_no_params else base_query_no_params
    params = [] if score_params < score_no_params else params
    end = time()
    return {
        'base_query': base_query,
        'params': params,
        'wasted your precious time': end-start
    }
