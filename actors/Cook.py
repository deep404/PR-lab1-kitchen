import requests
import time
import threading
import logging

logger = logging.getLogger(__name__)

DH_HOST = 'dinning_hall'


class Cook:
    def __init__(self, kitchen, id_, name, rank, proficiency, catch_phrase):
        self.kitchen = kitchen
        self.id_ = id_
        self.name = name
        self.rank = rank
        self.proficiency = proficiency
        self.catch_phrase = catch_phrase
        self.TIME_UNIT = 1

    def cook_work(self):
        for i in range(self.proficiency):
            threading.Thread(target=self.cook_hand_work, name=f'#K{self.kitchen.id_}-H{i}-{self.name}', daemon=True).start()

    def cook_hand_work(self):
        while True:
            try:
                q_item = self.kitchen.food_items_q.get_nowait()
                food_item = q_item[2]
                curr_counter = q_item[1]
                food_details = next((f for f in self.kitchen.food_list if f['id'] == food_item['food_id']), None)
                (order_idx, order_details) = next(((idx, order) for idx, order in enumerate(self.kitchen.order_list) if order['order_id'] == food_item['order_id']), (None, None))

                if self.can_prepare(food_details, order_details):
                    # prepare
                    time.sleep(food_details['preparation-time'] * self.TIME_UNIT)
                    self.kitchen.order_list[order_idx]['is_done_counter'] += 1
                    self.kitchen.order_list[order_idx]['cooking_details'].put_nowait({'food_id': food_details['id'], 'cook_id': self.id_})

                    if self.kitchen.order_list[order_idx]['is_done_counter'] == len(self.kitchen.order_list[order_idx]['items']):
                        # notify dinning hall
                        logger.debug(f'PREPARED orderId: "{order_details["order_id"]}" | priority: {order_details["priority"]}\n')
                        payload = {
                            **self.kitchen.order_list[order_idx],
                            'cooking_time': int(time.time() - self.kitchen.order_list[order_idx]['received_time']),
                            'cooking_details': list(self.kitchen.order_list[order_idx]['cooking_details'].queue)
                        }
                        res = requests.post(f'http://{DH_HOST}:{self.kitchen.dh_port}/distribution', json=payload)
                        logger.debug(f'Dinning hall response for prepared orderId: {order_details["order_id"]} response: {res.json()}\n')

                    # add new free cooking apparatus to queue
                    apparatus = food_details['cooking-apparatus']
                    if apparatus == 'oven':
                        n = self.kitchen.ovens_q.qsize()
                        self.kitchen.ovens_q.put_nowait(n)
                    elif apparatus == 'stove':
                        n = self.kitchen.stoves_q.qsize()
                        self.kitchen.stoves_q.put_nowait(n)

                else:
                    # cook hand could not prepare this order, put it back to queue
                    self.kitchen.food_items_q.put_nowait((food_item['priority'], curr_counter, food_item))

            except Exception as e:
                pass

    def can_prepare(self, food, order):
        if food['complexity'] == self.rank or food['complexity'] - 1 == self.rank:
            apparatus = food['cooking-apparatus']
            if apparatus == 'oven':
                try:
                    o = self.kitchen.ovens_q.get_nowait()
                    logger.warning(f'COOKING  foodId: {food["id"]} | orderId: "{order["order_id"][0:4]}" | priority: {order["priority"]} | oven: {o}\n')
                    return True
                except Exception as e:
                    return False
            elif apparatus == 'stove':
                try:
                    s = self.kitchen.stoves_q.get_nowait()
                    logger.warning(f'COOKING foodId: {food["id"]} | orderId: "{order["order_id"][0:4]}" | priority: {order["priority"]} | stove: {s}\n')
                    return True
                except Exception as e:
                    return False
            elif apparatus is None:
                logger.warning(f'COOKING foodId: {food["id"]} | orderId: "{order["order_id"][0:4]}" | priority: {order["priority"]} (hands)\n')
                return True
            return False
        return False