import os
import json
import random
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
        return moveTowardsPoint(body, 1, 1)
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



def smartWalk(body):
    x = body["you"]["x"]
    y = body["you"]["y"]
    if y < body["mapHeight"] - 10:
        return moveTowardsPoint(body, body["mapWidth"] - x/3, body["mapHeight"] -1)
    else:
        return moveTowardsPoint(body, body["mapWidth"] - x / 2, body["mapHeight"] - y / 4)


def middleBoardState(body)
    x = body["you"]["x"]
    y = body["you"]["y"]
    if (x < body["mapWidth"]-body["mapWidth"]/3) and (x > body["mapWidth"]/3) and not visibleEnemy(body)
        return "shoot"
    else:
        return moveTowardsCenterOfMap(body)









def visibleEnemy(body):
    if "x" in body["enemies"][0]:
        return True
    return False

def enemyInLine(body):
    if body["enemies"][0]["x"] == body["you"]["x"]:
        return "horisontal"
    elif body["enemies"][0]["y"] == body["you"]["y"]:
        return "vertical"
    return "none"

def lineVertical(body):
    if body["enemies"][0]["x"] < body["you"]["x"]:
        if body["enemies"][0]["direction"] == "right":
            if body["you"]["direction"] == "left":
                return "both see"
            return "he sees"
        if body["you"]["direction"] == "left":
            return "you see"
    else:
        if body["enemies"][0]["direction"] == "left":
            if body["you"]["direction"] == "right":
                return "both see"
            return "he sees"
        if body["you"]["direction"] == "right":
            return "you see"

def lineHorisontal(body):
    if body["enemies"][0]["y"] < body["you"]["y"]:
        if body["enemies"][0]["direction"] == "bottom":
            if body["you"]["direction"] == "top":
                return "both see"
            return "he sees"
        if body["you"]["direction"] == "top":
            return "you see"
    else:
        if body["enemies"][0]["direction"] == "top":
            if body["you"]["direction"] == "bottom":
                return "both see"
            return "he sees"
        if body["you"]["direction"] == "bottom":
            return "you see"
    return "noone sees"

def rotateToEnemy(body):
    if body["enemies"][0]["x"] == body["you"]["x"]:
        if body["enemies"][0]["y"] < body["you"]["y"]:
            if body["you"]["direction"] == "right":
                return ROTATE_LEFT
            return ROTATE_RIGHT
        else:
            if body["you"]["direction"] == "right":
                return ROTATE_RIGHT
            return ROTATE_LEFT
    if body["enemies"][0]["x"] < body["you"]["x"]:
        if body["you"]["direction"] == "top":
            return ROTATE_LEFT
        return ROTATE_RIGHT
    else:
        if body["you"]["direction"] == "top":
            return ROTATE_RIGHT
        return ROTATE_RIGHT


def chooseAction(body):
    action = middleBoardState(body)
    if visibleEnemy(body):
        line = enemyInLine(body)
        if line == "vertical":
            vert = lineVertical(body)
            if vert == "he sees":
                action = RETREAT
            elif vert == "both see":
                action = SHOOT
            elif vert == "you see":
                action = SHOOT
            else:
                action = rotateToEnemy(body)
        elif line == "horisontal":
            hori = lineHorisontal(body)
            if hori == "he sees":
                action = RETREAT
            elif hori == "both see":
                action = SHOOT
            elif hori == "you see":
                action = SHOOT
            else:
                action = rotateToEnemy(body)
    return action



env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Nils Olav"
    returnObject["team"] = "Det norske forsvaret"
elif req_params_query == "command":
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()