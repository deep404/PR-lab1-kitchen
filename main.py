import addons
import logging
import threading
from flask import Flask
from flask import request
from actors.Kitchen import Kitchen
import coloredlogs

logging.basicConfig(filename='kitchen.log', level=logging.DEBUG, format='%(asctime)s: %(threadName)s: %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

APP_HOST = '0.0.0.0'

app1 = Flask('Kitchen - 1')
app2 = Flask('Kitchen - 2')
app3 = Flask('Kitchen - 3')
app4 = Flask('Kitchen - 4')

# each kitchen should be configured by the data returned from its corresponding dinning hall
data1 = utils.fetch_kitchen_data_from_dh(4001)
k1 = Kitchen(5001, 4001, 1, data1['cooks'], data1['ovens'], data1['stoves'], data1['menu'])

data2 = utils.fetch_kitchen_data_from_dh(4002)
k2 = Kitchen(5002, 4002, 2, data2['cooks'], data2['ovens'], data2['stoves'], data2['menu'])

data3 = utils.fetch_kitchen_data_from_dh(4003)
k3 = Kitchen(5003, 4003, 3, data3['cooks'], data3['ovens'], data3['stoves'], data3['menu'])

data4 = utils.fetch_kitchen_data_from_dh(4004)
k4 = Kitchen(5004, 4004, 4, data4['cooks'], data4['ovens'], data4['stoves'], data4['menu'])

kitchens_apps = [{
    'app': app1,
    'kitchen': k1
}, {
    'app': app2,
    'kitchen': k2
}, {
    'app': app3,
    'kitchen': k3
}, {
    'app': app4,
    'kitchen': k4
}]

for i, app_data in enumerate(kitchens_apps):
    app = app_data['app']
    kitchen = app_data['kitchen']


    @app.route('/order', methods=['POST'])
    def order(k=kitchen):
        data = request.get_json()
        logger.info(f'Kitchen-{k.id_} NEW ORDER "{data["order_id"]}" | priority: {data["priority"]} | items: {data["items"]}\n')
        return k.receive_new_order(data)


def main():
    open("kitchen.log", "w").close()

    threading.Thread(target=lambda: app1.run(host=APP_HOST, port=k1.port, debug=False, use_reloader=False, threaded=True), name=f'FLASK-K1', daemon=True).start()
    threading.Thread(target=lambda: app2.run(host=APP_HOST, port=k2.port, debug=False, use_reloader=False, threaded=True), name=f'FLASK-K2', daemon=True).start()
    threading.Thread(target=lambda: app3.run(host=APP_HOST, port=k3.port, debug=False, use_reloader=False, threaded=True), name=f'FLASK-K2', daemon=True).start()
    threading.Thread(target=lambda: app4.run(host=APP_HOST, port=k4.port, debug=False, use_reloader=False, threaded=True), name=f'FLASK-K2', daemon=True).start()

    threading.Thread(target=k1.start_kitchen, daemon=True).start()
    threading.Thread(target=k2.start_kitchen, daemon=True).start()
    threading.Thread(target=k3.start_kitchen, daemon=True).start()
    threading.Thread(target=k4.start_kitchen, daemon=True).start()

    while True:
        pass


if __name__ == '__main__':
    main()
