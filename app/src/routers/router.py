from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Annotated

from src.schemas.bills import ListPosition, BillPosition
from src.validators.validator import IMGValidator

router = APIRouter(prefix="/bill", tags=["bill"])

@router.post("get_bill_parsing")
async def perfect_ping(file: UploadFile):
    validator = IMGValidator()
    validation = await validator.validate_file(file=file)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "File validation failed",
                "errors": validation["errors"]
            }
        )
    a1 = BillPosition(name = 'Дранник',
                      quantity = 1,
                      price = 17,
                      total = 17
                      )
    
    a2 = BillPosition(name = 'Дранник жирный',
                      quantity = 2,
                      price = 23,
                      total = 46
                      )
    total = ListPosition(pos_list=[a1,a2])
    print(file.filename)
    return total
