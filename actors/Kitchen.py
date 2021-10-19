import queue
import threading
import itertools
import time
import logging
from domain.Cook import Cook

logger = logging.getLogger(__name__)


class Kitchen:
    def __init__(self, port, dh_port, id_, cooks, ovens, stoves, food_list):
        self.port = port
        self.dh_port = dh_port
        self.id_ = id_
        self.cooks = [Cook(self, data['id'], data['name'], data['rank'], data['proficiency'], data['catch-phrase']) for i, data in enumerate(cooks)]
        self.ovens_q = queue.Queue(ovens)
        self.stoves_q = queue.Queue(stoves)
        self.food_items_q = queue.PriorityQueue()
        self.food_list = food_list
        self.order_list = []
        for i in range(ovens): self.ovens_q.put_nowait(i)
        for i in range(stoves): self.stoves_q.put_nowait(i)
        self.WAITING_COEFFICIENT = 2
        # https://stackoverflow.com/questions/40205223/priority-queue-with-tuples-and-dicts
        self.counter = itertools.count()
        logger.info(f'kitchen configured, cooks: {len(self.cooks)}, ovens: {self.ovens_q.qsize()}, stoves: {self.stoves_q.qsize()}')

    def start_kitchen(self):
        for cook in self.cooks:
            threading.Thread(target=cook.cook_work, name=f'K{self.id_}', daemon=True).start()

    def receive_new_order(self, data):
        priority = -int(data['priority'])
        kitchen_order = {
            'order_id': data['order_id'],
            'table_id': data['table_id'] if 'table_id' in data else None,
            'waiter_id': data['waiter_id'] if 'waiter_id' in data else None,
            'items': data['items'],
            'priority': priority,
            'max_wait': data['max_wait'],
            'received_time': time.time(),
            'cooking_details': queue.Queue(),
            'is_done_counter': 0,
            'time_start': data['time_start'],
        }
        self.order_list.append(kitchen_order)
        waiting_estimation = 0
        for item_id in data['items']:
            food = next((f for i, f in enumerate(self.food_list) if f['id'] == item_id), None)
            if food is not None:
                waiting_estimation += food['preparation-time']
                self.food_items_q.put_nowait((priority, next(self.counter), {
                    'food_id': food['id'],
                    'order_id': data['order_id'],
                    'priority': priority
                }))
        return {'estimated_waiting_time': int(data['max_wait']) - self.WAITING_COEFFICIENT}