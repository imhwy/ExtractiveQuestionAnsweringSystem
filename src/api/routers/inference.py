"""
This module defines FastAPI endpoints for inference operations.
"""
import time
from fastapi import (status,
                     Depends,
                     APIRouter,
                     Request,
                     HTTPException)
from fastapi.responses import JSONResponse

from src.services.service import Service
from src.api.dependencies.inference_dependencies import get_inference_service
from src.api.schemas.inference import RequestQuestionContext
from src.services.inference_state import InferenceState
from src.api.schemas.result import Result
from src.utils.utility import create_new_id

inference_state = InferenceState()

inference_router = APIRouter(
    tags=["Inference"],
    prefix="/inference",
)


@inference_router.post("/selectModel", status_code=status.HTTP_200_OK)
async def select_model(
    option: Request,
    service: Service = Depends(get_inference_service)
) -> str:
    """
    Selects a question answering model for inference.

    Args:
        option (str): The option specifying the model to load.
        service (Service): Dependency injection to get the inference service.

    Returns:
        str: Confirmation message upon successful model selection.

    Raises:
        HTTPException: If there is an error loading the model.
    """
    try:
        payload = await option.json()
        option = payload.get("category")
        print(f"the option is: {option}")
        tokenizer, model = await service.model.loading_question_answering_model(path=option)
        inference_state.tokenizer = tokenizer
        inference_state.model = model
        inference_state.option = option
        return f"Successfully selected model: {option}!!!"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)) from e


@inference_router.post("/requestQA", status_code=status.HTTP_200_OK)
async def inference_request(
    request_info: RequestQuestionContext,
    service: Service = Depends(get_inference_service)
) -> JSONResponse:
    """
    Performs question answering inference using the selected model.

    Args:
        request_info (RequestQuestionContext): Request payload containing question and context.
        service (Service): Dependency injection to get the inference service.

    Returns:
        dict: The result of the inference operation.

    Raises:
        HTTPException: If there is an error during inference.
    """
    if inference_state.tokenizer is None or inference_state.model is None:
        return JSONResponse(
            {
                "answer": "Please select a model first and wait a little bit for loading model!!!"
            }
        )
    try:
        start_time = time.time()
        result = await service.inference.inference_pipeline(
            tokenizer=inference_state.tokenizer,
            model=inference_state.model,
            context=request_info.context,
            question=request_info.question
        )
        result_id = create_new_id(prefix="result")
        end_time = time.time()
        inference_time = str(end_time - start_time) + "s"
        saved_result = Result(
            Id=result_id,
            model=inference_state.option,
            question=request_info.question,
            context=request_info.context,
            answer=result,
            time=inference_time
        )
        await service.result_collection.add_new_result(result=saved_result)
        print(f"Time: {inference_time}")
        print(f"The result is: {result}")
        return JSONResponse({"answer": result})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)) from e
