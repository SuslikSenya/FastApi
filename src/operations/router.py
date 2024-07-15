import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache
from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    # query = select(operation).where(operation.c.type == operation_type)
    # result = await session.execute(query)
    print("Hi, its done")
    # return {
    #     "status": "success",
    #     "data": result.all(),
    #     "details": None
    # }
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        print(result)
        operations = result.fetchall()  # Fetch all results
        print(operations)

        # Convert each SQLAlchemy Row object to a dictionary
        operations_list = [{column.name: getattr(op, column.name) for column in operation.columns} for op in operations]
        print(operations_list)
        return {
            "status": "success",
            "data": operations_list,
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/add_specific_operations")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    """
    docstring
    """
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# @router.get("/main")
# async def main(session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(1))
#     return result.all()
