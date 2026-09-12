from src.common import *


ENEMIES = {
    "zako": {
        "health": 1,
        "sprite": Sprite(48, 0),
        "shoot_cd": 0,
        "score": 10,
        "xspeed": 1,
        "yspeed": 0,
        "can_approach": True,
    },
    "shield": {
        "health": 2,
        "sprite": Sprite(32, 0),
        "shoot_cd": 0,
        "score": 20,
        "xspeed": 1,
        "yspeed": 0,
        "can_approach": True,
    },
    "shooter": {
        "health": 1,
        "sprite": Sprite(16, 0),
        "shoot_cd": 120,
        "score": 20,
        "xspeed": 1,
        "yspeed": 0,
        "can_approach": True,
    },
    "fast": {
        "health": 1,
        "sprite": Sprite(64, 0),
        "shoot_cd": 0,
        "score": 15,
        "xspeed": 2,
        "yspeed": 0,
        "can_approach": True,
    },
    "diver": {
        "health": 1,
        "sprite": Sprite(64, 16),
        "shoot_cd": 0,
        "score": 15,
        "xspeed": 1,
        "yspeed": 1,
        "can_approach": False,
    },
    "boss": {
        "health": 18,
        "sprite": Sprite(0, 16),
        "shoot_cd": 50,
        "score": 1000,
        "xspeed": 1,
        "yspeed": 0,
        "can_approach": False,
    },
}
