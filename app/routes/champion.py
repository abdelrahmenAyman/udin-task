from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import actions
from app.dependencies import get_session
from app.schemas.champion import ChampionCreate, ChampionRead

router = APIRouter()


@router.post("/champions/", status_code=201, response_model=ChampionRead)
async def create_champion(data: ChampionCreate, session: Session = Depends(get_session)):
    return await actions.Champion.create_with_base_stats(data=data, session=session)


@router.get("/champions/", response_model=list[ChampionRead])
async def list_champions(session: Session = Depends(get_session)):
    return await actions.Champion.list(session=session)
