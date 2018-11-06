import os
import json
from random import randint
import math

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)

def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction =  MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
    return plannedAction



def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)


def fuckThatPinguin(body):
    if body["enemies"]["weaponDamage"] > body["you"]["weaponDamage"]:
        return runTheFuckAway(body)
    else:
        if (body["enemies"]["x"] - body["you"]["x"] < 6) or (body["enemies"]["y"] - body["you"]["y"] < 6)
            return "shoot"
        else:
            return "pass"





def facingYou(body):
    xWay = "right" if body["enemies"]["x"] > body["you"]["x"] else xWay="left"
    yWay = "bottom" if body["enemies"]["y"] > body["you"]["y"] else yWay="top"

    hisDi = body["enemies"]["direction"]
    youDi = body["you"]["direction"]


    if ((hisDi == xWay) or (hisDi == yWay)) and (((youDi == "left" and hisDi == "right") or (youDi == "right" and hisDi == "left")) or ((youDi == "top" and hisDi == "bottom") or (youDi == "bottom" and hisDi == "top"))):
        return True
    else:
        return False






def ifVisiblePinguin(body):
    #he is gay
    if facingYou(body):
        return runTheFuckAway(body)
    else:
        return moveTowardsPoint(body, 10, 10)





def runTheFuckAway(body):
    return moveTowardsPoint(body, 7, 7)




def chooseAction(body):
    action = PASS
    action = "shoot"
    return action





env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Nils Olav"
    returnObject["team"] = "Garden"
elif req_params_query == "command":    
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()