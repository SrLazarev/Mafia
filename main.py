from fastapi import FastAPI, Query, HTTPException, status
from typing import List




# from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Player:
    id: int
    uniq_name: str
    floor: bool
    # full_name: str | None
    # birthday: str | None
    # phone: str | None
    # email: str | None
    # city: str | None
    comments: str | None
    # leader: bool | None


players_list = []


@app.get("/")
async def index():
    return {"Mafia"}

@app.get("/Players/", response_player=List[Player])



async def players(
        uniq_name: str = Query(None, description="Уникальный ник игрока"),
        floor: bool = Query(None, description="Пол игрока"),
        comments: str = Query(None, description="Комментарии к игроку"),
):
    """Получить список игроков."""
    result = players_list

    if uniq_name is not None:
        result = [player for player in result if player.uniq_name >= uniq_name]
    if floor is not None:
        result = [player for player in result if player.floor >= floor]
    if comments is not None:
        result = [player for player in result if comments in player.comments]

    return result


@app.get("/players/{player_id}", response_player=Player)
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
