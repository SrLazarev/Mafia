from fastapi import FastAPI, Query, HTTPException, status
from sqlmodel import Session, select, create_engine, SQLModel, Field
from typing import List, Optional
from enum import Enum


class Gender(str, Enum):
    MALE = "мужской"
    FEMALE = "женский"

# --- Настройка БД ---
sqlite_file_name = "mafia.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- Модели ---
class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uniq_name: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    gender: Gender
    comments: str | None
    birthday: str | None
    phone: str | None
    email: str | None
    city: str | None
    is_host: bool = Field(default=False, index=True)


class PlayerCreate(SQLModel):
    uniq_name: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    gender: Gender
    birthday: str | None
    phone: str | None
    email: str | None
    city: str | None
    comments: str | None
    is_host: bool = Field(default=False)

# --- Приложение ---
app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


players_list = []

@app.get("/")
async def index():
    return {"Mafia"}

@app.get("/Players/", response_model=List[Player])
async def players(
        uniq_name: str = Query(None, description="Уникальный ник игрока"),
        gender: Optional[Gender] = Query(None, description="Фильтр по полу"),
        comments: str = Query(None, description="Комментарии к игроку"),
        is_host: bool = Query(None, description="Является ли игрок ведущим?")
):
    """Получить список игроков."""
    result = players_list

    if uniq_name is not None:
        result = [player for player in result if player.uniq_name >= uniq_name]
    if gender is not None:
        result = [player for player in result if player.gender == gender]
    if comments is not None:
        result = [player for player in result if comments in player.comments]
    if is_host is not None:
        result = [player for player in result if player.is_host == is_host]

    return result


@app.get("/players/{player_id}", response_model=Player)
async def player_detail(player_id: int):
    """Получить детальную информацию об игроке."""
    player_id -= 1

    if player_id < 0 or player_id >= len(players_list):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Игрок не найден")

    return players_list[player_id]


@app.post("/players/", response_model=Player, status_code=status.HTTP_201_CREATED)
async def player_create(player: Player):
    """Добавить игрока."""

    for p in players_list:
        if p.uniq_name == player.uniq_name and p.floor == player.floor:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой игрок уже есть")

    players_list.append(player)
    return player


@app.put("/players/{player_id}", response_model=Player)
async def movie_update(player_id: int, movie: Player):
    """Изменить карточку Игрока."""
    player_id -= 1

    if player_id < 0 or player_id >= len(players_list):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фильм не найден")

    players_list[player_id].uniq_name = players.uniq_name
    players_list[player_id].floor = players.floor

    return players_list[player_id]


@app.delete("/player/{player_id}")
async def player_deletee(player_id: int):
    """Изменить игрока."""
    player_id -= 1

    if player_id < 0 or player_id >= len(players_list):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Игрок не найден")

    result = players_list.pop(player_id)

    return {"Message": f"Игрок {result.uniq_name} был удален"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)