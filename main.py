from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from components.buttons import TOGGLE_SWITCHES, BUTTONS
from components.displays import DISPLAYS
from riddles.lightsout import LightsOut
from riddles.word_riddle import WordRiddle
from riddles.pot_riddle import PotRiddle
from riddles.manager import RiddleManager

manager = RiddleManager()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- LightsOut ----------
class LightsOutRequest(BaseModel):
    correctGlyph: str
    incorrectGlyph: list[str]
    introduction: str
    onFail: list[str]
    onSolve: str


@app.post("/lights_out")
async def say_hello(body: LightsOutRequest):

    l = LightsOut(
        body.correctGlyph,
        body.incorrectGlyph,
        TOGGLE_SWITCHES,
        DISPLAYS[:4],
        body.introduction,
        body.onFail,
        body.onSolve
    )
    l.start()

    print(body)
    return {"message": f"Hello"}

# -------- WordRiddle ----------
class WordRiddleRequest(BaseModel):
    word: str
    introduction: str
    onFail: list[str]
    onSolve: str


@app.post("/word_riddle")
async def start_word_riddle(body: WordRiddleRequest):
    r = WordRiddle(
        body.word,
        BUTTONS,
	DISPLAYS[4:8],
        body.introduction,
        body.onFail,
        body.onSolve
    )
    r.start()
    return {"message": f"WordRiddle gestartet mit Wort: {body.word}"}

    # -------- PotRiddle ----------
class PotRiddleRequest(BaseModel):
    introduction: str
    onFail: list[str]
    onSolve: str

@app.post("/pot_riddle")
async def start_pot_riddle(body: PotRiddleRequest):
    r = PotRiddle(body.introduction, body.onFail, body.onSolve)
    r.start()
    return {"message": "PotRiddle gestartet"}

@app.post("/start_game")
async def start_game():
    manager.start()
    return {"message": "Game gestartet"}