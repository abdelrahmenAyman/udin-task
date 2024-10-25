from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app import actions
from app.dependencies import get_session
from app.errors import RecordDoesNotExist
from app.schemas.base_stats import BaseStatsUpdate
from app.schemas.champion import ChampionCreate, ChampionRead, ChampionUpdate

router = APIRouter()


@router.post("/champions/", status_code=201, response_model=ChampionRead)
async def create_champion(data: ChampionCreate, session: Session = Depends(get_session)):
    return await actions.Champion.create_with_base_stats(data=data, session=session)


@router.get("/champions/", status_code=200, response_model=list[ChampionRead])
async def list_champions(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, lt=100),
    session: Session = Depends(get_session),
):
    return await actions.Champion.list(offset=offset, limit=limit, session=session)


@router.get(
    "/champions/{champion_id}/",
    status_code=200,
    response_model=ChampionRead,
    responses={"404": {"detail": "Champion with ID 0 not found"}},
)
async def read_champion(champion_id: int, session: Session = Depends(get_session)):
    try:
        return await actions.Champion.get_by_id(id=champion_id, session=session)
    except RecordDoesNotExist:
        raise HTTPException(status_code=404, detail=f"Champion with ID {champion_id} not found")


@router.delete(
    "/champions/{champion_id}/",
    status_code=204,
    responses={"404": {"detail": "Champion with ID 0 not found"}},
)
async def delete_champion(champion_id: int, session: Session = Depends(get_session)):
    try:
        await actions.Champion.delete(id=champion_id, session=session)
    except RecordDoesNotExist:
        raise HTTPException(status_code=404, detail=f"Champion with ID {champion_id} not found")


@router.patch(
    "/champions/{champion_id}/",
    status_code=200,
    response_model=ChampionRead,
    responses={404: {"detail": "Champion with ID not found"}},
)
async def update_champion(champion_id: int, data: ChampionUpdate, session: Session = Depends(get_session)):
    try:
        champion = await actions.Champion.update(id=champion_id, data=data, session=session)
        session.commit()
        session.refresh(champion)
        return champion
    except RecordDoesNotExist:
        raise HTTPException(status_code=404, detail=f"Champion with ID {champion_id} not found")


@router.patch(
    "/champions/{champion_id}/base-stats",
    status_code=200,
    response_model=ChampionRead,
    responses={404: {"detail": "Champions with ID not found"}},
)
async def update_champion_base_stats(champion_id: int, data: BaseStatsUpdate, session=Depends(get_session)):
    try:
        stats = await actions.BaseStats.update(champion_id=champion_id, data=data, session=session)
        session.commit()
        session.refresh(stats)
        return stats.champion
    except RecordDoesNotExist:
        raise HTTPException(status_code=404, detail=f"Champion with ID {champion_id} not found")
