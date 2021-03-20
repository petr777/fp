import pymongo
import datetime

class MongodbPipeline:

    def __init__(self, platform):
        self.collection_name = platform

    def open_spider(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['FOGSOFT']

    def close_spider(self):
        self.client.close()

    def clean_name_item(self, item):
        if item.get('Начальная цена, руб.'):
            item['Начальная цена'] = item.pop('Начальная цена, руб.')

        if item.get("Организатор торгов"):
            item['Организатор'] = item.pop('Организатор торгов')

        return item

    def data_normalization(self, item):

        if item.get('№'):
            item['procedure_url'] = item['№']['url']
            item['procedure_id']  = item['№']['name']
            del item['№']


        if item.get('Торги'):
            item['procedure_description'] = item['Торги']['name']
            del item['Торги']


        if item.get('№ лота'):
            item['lot_url'] = item['№ лота']['url']
            item['lot_id']  = item['№ лота']['name']
            del item['№ лота']


        if item.get('Лот'):
            item['lot_description'] = item['Лот']['name']
            del item['Лот']


        if item.get('Организатор'):
            item['organizer_url'] = item['Организатор']['url']
            item['organizer_name']  = item['Организатор']['name']
            del item['Организатор']


        if item.get('Победитель'):
            item['viner'] = item.pop('Победитель')


        if item.get('Дата проведения'):
            item['event_date'] = item.pop('Дата проведения')


        if item.get('Дата окончания представления заявок'):
            item['deadline_date'] = item.pop('Дата окончания представления заявок')


        if item.get('Статус'):
            item['status'] = item.pop('Статус')


        if item.get('Тип торга'):
            item['type_trade'] = item.pop('Тип торга')


        if item.get("Начальная цена"):
            item["initial_price"] = float(item['Начальная цена'].replace(' ', '').replace(',', '.'))
            del item['Начальная цена']

        return item


    def get_id_lot(self, item):
        return item['lot_url'].split('/')[-2]

    def comparison_item(self, item, item_db):
        # Для сравнения значений из набора item_db удааяем "_id", "date_created", "date_updated"

        if item_db.get('_id'):
            item_db.pop('_id')

        if item_db.get('date_created'):
            item_db.pop('date_created')

        if item_db.get('date_updated'):
            item_db.pop('date_updated')

        # TODO оповешать если изменения интересны
        # Ниже код показывает что именно изменилось возможно пригодится
        # diffkeys = [k for k in item_db if item_db[k] != item[k]]
        # for k in diffkeys:
        #     print(k, ':', item_db[k], '->', item[k])

        if item_db != item:
            return item
        else:
            return None


    def process_item(self, item):
        # Очищаем данные
        item = self.clean_name_item(item)
        item = self.data_normalization(item)
        # Получаем id
        id_lot = self.get_id_lot(item)
        item['id_lot'] = id_lot
        # Проверяем есть ли в базе данный
        # Проверку осушествляе по "id_lot"
        item_db = self.db[self.collection_name].find_one({'id_lot': id_lot})
        if item_db:
            # Если значение уже есть в базе сравниваем данные из базы и пришедшем item
            if self.comparison_item(item, item_db):
                item['date_updated'] = datetime.datetime.now()
                self.db[self.collection_name].find_one_and_update({'id_lot': id_lot}, {'$set': item})
        # Если значения в базе нет создаем
        else:
            item['date_created'] = datetime.datetime.now()
            self.db[self.collection_name].insert(item)



