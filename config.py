import queue

global TIME_UNIT
TIME_UNIT = 1

global FOOD_ITEMS_Q
FOOD_ITEMS_Q = queue.PriorityQueue()

global ORDER_LIST
ORDER_LIST = []

global COOKS_LIST
COOKS_LIST = [{
    "id": 1,
    "rank": 3,
    "proficiency": 3,
    "name": "Jamie Oliver",
    "catch-phrase": "pukka"
}, {
    "id": 2,
    "rank": 1,
    "proficiency": 3,
    "name": "Anthony Bourdain",
    "catch-phrase": "Skills can be taught. Character you either have or you don’t have."
}, {
    "id": 3,
    "rank": 2,
    "proficiency": 3,
    "name": "Emeril Lagasse",
    "catch-phrase": "It's okay to play with your food."
}]

global STOVES_Q
STOVES_Q = queue.Queue()
STOVES_Q.put(0)
STOVES_Q.put(1)
STOVES_Q.put(2)
STOVES_Q.put(3)

global OVENS_Q
OVENS_Q = queue.Queue()
OVENS_Q.put_nowait(0)
OVENS_Q.put_nowait(1)
OVENS_Q.put_nowait(2)
OVENS_Q.put_nowait(3)

global FOOD_LIST
FOOD_LIST = [{
    "id": 1,
    "name": "pizza",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 2,
    "name": "salad",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": None
}, {
    "id": 4,
    "name": "Scallop Sashimi with Meyer Lemon Confit",
    "preparation-time": 32,
    "complexity": 3,
    "cooking-apparatus": None
}, {
    "id": 5,
    "name": "Island Duck with Mulberry Mustard",
    "preparation-time": 35,
    "complexity": 3,
    "cooking-apparatus": "oven"
}, {
    "id": 6,
    "name": "Waffles",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 7,
    "name": "Aubergine",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": None
}, {
    "id": 8,
    "name": "Lasagna",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 9,
    "name": "Burger",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": "oven"
}, {
    "id": 10,
    "name": "Gyros",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}]