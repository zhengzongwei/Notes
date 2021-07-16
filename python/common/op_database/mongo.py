import pymongo

class Mongo(object):
    def __init__(self,collection="log",ip="127.0.0.1",port=27017):
        self.client = pymongo.MongoClient(ip,port)
        self.db = self.client[collection]

class BaseHandle(object):
    
    @staticmethod
    def insert_one(collection,data):
        result = collection.insert_one(data)
        return result.inserted
    
    @staticmethod
    def insert_many(collection,data_list):
        result = collection.insert_many(data_list)
        return result.inserted_ids

    @staticmethod
    def find_one(collection,data,data_field={}):
        if len(data_field):
            result = collection.find_one(data,data_field)
        result = collection.find_one(data)
        return result
    
    @staticmethod
    def find_many(collection,data,data_field={}): 
        if len(data_field):
            result = collection.find(data,data_field)
        result = collection.find(data)
        return result
    
    @staticmethod
    def update_one(collection,data_codition,data_set):
        result = collection.update_one(data_codition,data_set)
        return result

    @staticmethod
    def update_many(collection,data_codition,data_set):
        result = collection.update_many(data_codition,data_set)
        return result
    
    @staticmethod
    def replace_one(collection, data_condition, data_set):
        """ 完全替换掉 这一条数据， 只是 _id 不变"""
        result = collection.replace_one(data_condition, data_set)
        return result
    
    @staticmethod
    def delete_many(collection, data):
        result = collection.delete_many(data)
        return result

    @staticmethod
    def delete_one(collection, data):
        result = collection.delete_one(data)
        return result


class DBbase(object):
    def __init__(self,collection):
        self.mongo = Mongo()
        self.collection = self.mongo.db[collection]

    def insert_one(self,data):
        result = BaseHandle.insert_one(self.collection,data)
        return result
    
    def insert_many(self,data_list):
        result = BaseHandle.insert_many(self.collection,data_list)
        return result
    
    def find_one(self,data,data_field={}):
        result = BaseHandle.find_one(self.collection,data,data_field)
        return result
    
    def find_many(self,data,data_field={}):
        result = BaseHandle.find_many(self.collection,data,data_field)
        return result

    def find_all(self, data={}, data_field={}):
        """select * from table"""
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_in(self, field, item_list, data_field={}):
        """SELECT * FROM inventory WHERE status in ("A", "D")"""
        data = dict()
        data[field] = {"$in": item_list}
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_or(self, data_list, data_field={}):
        """db.inventory.find(
            {"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})

        SELECT * FROM inventory WHERE status = "A" OR qty < 30
        """
        data = dict()
        data["$or"] = data_list
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_between(self, field, value1, value2, data_field={}):
        """获取俩个值中间的数据"""
        data = dict()
        data[field] = {"$gt": value1, "$lt": value2}
        # data[field] = {"$gte": value1, "$lte": value2} # <>   <= >=
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_more(self, field, value, data_field={}):
        data = dict()
        data[field] = {"$gt": value}
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_less(self, field, value, data_field={}):
        data = dict()
        data[field] = {"$lt": value}
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def find_like(self, field, value, data_field={}):
        """ where key like "%audio% """
        data = dict()
        data[field] = {'$regex': '.*' + value + '.*'}
        # print(data)
        result = BaseHandle.find_many(self.collection, data, data_field)
        return result

    def query_limit(self, query, num):
        """db.collection.find(<query>).limit(<number>) 获取指定数据"""
        result = query.limit(num)
        return result

    def query_count(self, query):
        result = query.count()
        return result

    def query_skip(self, query, num):
        result = query.skip(num)
        return result

    def query_sort(self, query, data):
        """db.orders.find().sort( { amount: -1 } ) 根据amount 降序排列"""
        result = query.sort(data)
        return result

    def delete_one(self, data):
        """ 删除单行数据 如果有多个 则删除第一个"""
        result = BaseHandle.delete_one(self.collection, data)
        return result

    def delete_many(self, data):
        """ 删除查到的多个数据 data 是一个字典 """
        result = BaseHandle.delete_many(self.collection, data)
        return result


class DBNeiHan(DBBase):
    def __init__(self):
        super(DBNeiHan, self).__init__("neihan_content")

#表名字
class DBPerson(DBBase):
    def __init__(self):
        super(DBPerson, self).__init__("person")


  
if __name__ == '__main__':
    person = DBPerson()
    data={
            "weixin": [
                {
                    "name": "开源优测",
                    "uid": "DeepTest",
                    "desc": "分享开源测试技术"
                },
                {
                    "name": "开源优测_demo",
                    "uid": "DeepTest_demo",
                    "desc": "分享开源测试技术_demo"
                }
            ],
            "web": [
                {
                    "url": "www.testingunion.com",
                    "name": "开源优测社区",
                    "desc": "分享各类开源测试技巧"
                },
                {
                    "url": "www.testingunion.com_demo",
                    "name": "开源优测社区_demo",
                    "desc": "分享各类开源测试技巧_demo"
                }
            ]
        }
    for key ,value in data.items():
        for item in value:
              person.insert_one(item)
    f = person.find_like("name", "开源")
    print(list(f))