from elasticsearch import Elasticsearch
import datetime


class CHandleEs:
    def __init__(self):
        self.sCluster = ''

#    def __init__(self, sName):
#        self.sCluster = sName

    def _connection_to_es(self):
        if len(self.sCluster):
            es = Elasticsearch(cluster=self.sCluster)
        else:
            es = Elasticsearch()
        return es


class CData:
    def __init__(self, t_config, t_data):
        self.t_config = t_config
        self.t_data = t_data
        pass

    def get_tweets(self):
        pass

    def search_text(self, t_key_words):
        pass

    def search_retweet(self, s_tweet_id):
        pass

    def search_user(self, s_user_id):
        pass


class CCSV(CData):
    def __init__(self, t_config, t_data):
        self.t_config = t_config
        self.path = t_config['load__path_file']
        self.data = []
        self.t_data = t_data
        with open(self.t_config['load__path_file'], "r", encoding='utf16') as file:
            i = 0
            for row in file:
                if i == 0:
                    i += 1
                else:
                    h = row[1:].split('; ', maxsplit=3)
                    tmp = h[2][1:-3].encode('ascii', errors='ignore').decode()
                    x = (int(h[0]), str(tmp), str(h[1]))
                    self.data.append(x)

    def get_tweets(self):
        return self.data


class CElastic(CData):
    def __init__(self, t_config, t_data):
        self.sCluster = ''
        self.t_config = t_config
        self.xEs = self._connection_to_es()
        self.sLimit = t_config['load__es_limit']
        self.sIndexName = t_config['load__es_index']
        self.sDocTypeName = t_config['load__es_doctype']
        self.sTriName = t_config['load__es_tri_name']
        self.sDateBegin = t_config['load__es_date_begin'] + '000'
        self.sDateEnd = t_config['load__es_date_end'] + '000'
        self.tData = t_data
        self.nIndexSize = 0

    def _connection_to_es(self):
        if len(self.sCluster):
            es = Elasticsearch(cluster=self.sCluster)
        else:
            es = Elasticsearch()
        return es

    def get_tweets(self):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])

        l_fields = ['timestamp_ms', 'id_str', 'text', 'user.id_str', 'has_image']

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m',
                                     sort=['timestamp_ms:asc'], _source=l_fields, stored_fields=l_fields,
                                     size=self.sLimit, body={'query': {'match_all': {}}})

        self.nIndexSize = int(x_response['hits']['total'])

        data = self._return_from_scroll(x_response)
        return data

    def get_tri_exist(self):
        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={'query': {
            'exists': {"field": self.sTriName}}})

        return x_response['hits']['total']

    def get_ok(self):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])
        l_fields = ['timestamp_ms', 'id_str', 'text', 'user.id_str']

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {self.sTriName:
                              {"query": 1}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])

        data = self._return_from_scroll(x_response)
        return data

    def get_ok_id(self):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])
        l_fields = ['timestamp_ms', 'id_str', 'text', 'user.id_str']

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {self.sTriName:
                              {"query": 1}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])

        data = self._return_from_scroll(x_response)
        return data

    def get_nok(self):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])
        l_fields = ['timestamp_ms', 'id_str', 'text', 'user.id_str']

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {self.sTriName:
                              {"query": -1}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])

        data = self._return_from_scroll(x_response)
        return data

    def get_nok_id(self):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])
        l_fields = ['timestamp_ms', 'id_str', 'text', 'user.id_str']

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {self.sTriName:
                              {"query": -1}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])

        data = self._return_id_from_scroll(x_response)
        return data

    def search_text(self, t_key_words):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])

        s_key_words = '"'
        n_words = 0
        for word in t_key_words:
            s_key_words += word
            s_key_words += ' '
            n_words += 1
        s_key_words = s_key_words[:-1]
        s_key_words += '"'

        print('s_key_words')
        print(s_key_words)
        print('n_words')
        print(n_words)
        print('t_key_words')
        print(t_key_words)

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                        {"text":
                            {"query": s_key_words, "operator": "or", "minimum_should_match": n_words}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])
        print("%d documents found" % x_response['hits']['total'])

        data = self._retweet_from_scroll(x_response, n_words)

        return data

    def search_retweet(self, s_tweet_id):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])
        t_words = ''
        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {"id_str":
                              {"query": s_tweet_id}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        for hit in x_response['hits']['hits']:
            t_words = hit['_source']['text'].split(' ')
            print('HIT -> ' + hit['_source']['text'])

        if t_words[0] == 'RT':
            del t_words[0]

        if t_words[0][0] == '@':
            del t_words [0]

        data = self.search_text(t_words)

        return data



    def search_user(self, s_user_id):
        self.nIndexSize = int(self.xEs.count(index=self.sIndexName)['count'])

        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                        {"user.id_str":
                            {"query": s_user_id}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])
        # print("%d documents found" % x_response['hits']['total'])

        data = self._return_from_scroll(x_response)

        return data

    def _retweet_from_scroll(self, x_response, nb_words):
        data = []
        n_cmpt = 0

        s_scroll = x_response['_scroll_id']
        for hit in x_response['hits']['hits']:
            st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000).strftime('%Y-%m-%d %H:%M:%S')
            result_len = len(hit['_source']['text'].split(' ')) - 1
            if result_len <= nb_words:
                test = (hit['_source']['text'].encode('ascii', errors='ignore').decode(), st, hit['_source']['id_str'],
                        hit['_source']['user']['id_str'], hit['_source']['has_image'])
                if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in self.tData.ok_id:
                    data.append(test)
                n_cmpt += 1

        n_cmpt += 1

        while n_cmpt < self.nIndexSize and n_cmpt < int(self.sLimit):
            try:
                n_cmpt -= 1
                x_response = self.xEs.scroll(scroll_id=s_scroll, scroll='10s')
                s_scroll = x_response['_scroll_id']
                for hit in x_response['hits']['hits']:
                    st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000)\
                        .strftime('%Y-%m-%d %H:%M:%S')
                    result_len = len(hit['_source']['text'].split(' ')) - 1
                    if result_len <= nb_words:
                        test = (hit['_source']['text'].encode('ascii', errors='ignore').decode(), st,
                                hit['_source']['id_str'], hit['_source']['user']['id_str'], hit['_source']['has_image'])
                        if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in \
                                self.tData.ok_id:
                            data.append(test)
                    n_cmpt += 1
                n_cmpt += 1
            except:
                print('test')
                break

        return data

    def _return_from_scroll(self, x_response):
        data = []
        n_cmpt = 0

        s_scroll = x_response['_scroll_id']
        for hit in x_response['hits']['hits']:
            st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000).strftime('%Y-%m-%d %H:%M:%S')
            test = (hit['_source']['text'].encode('ascii', errors='ignore').decode(), st, hit['_source']['id_str'],
                    hit['_source']['user']['id_str'], hit['_source']['has_image'])
            if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in self.tData.ok_id:
                data.append(test)
            n_cmpt += 1

        n_cmpt += 1

        while n_cmpt < self.nIndexSize and n_cmpt < int(self.sLimit):
            try:
                n_cmpt -= 1
                x_response = self.xEs.scroll(scroll_id=s_scroll, scroll='10s')
                s_scroll = x_response['_scroll_id']
                for hit in x_response['hits']['hits']:
                    st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000)\
                        .strftime('%Y-%m-%d %H:%M:%S')
                    test = (hit['_source']['text'].encode('ascii', errors='ignore').decode(), st,
                            hit['_source']['id_str'], hit['_source']['user']['id_str'], hit['_source']['has_image'])
                    if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in \
                            self.tData.ok_id:
                        data.append(test)
                    n_cmpt += 1
                n_cmpt += 1
            except:
                print('test')
                break

        return data

    def _return_id_from_scroll(self, x_response):
        data = []
        n_cmpt = 0

        s_scroll = x_response['_scroll_id']
        for hit in x_response['hits']['hits']:
            st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000).strftime('%Y-%m-%d %H:%M:%S')
            test = (hit['_source']['id_str'])
            if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in self.tData.ok_id:
                data.append(test)
            n_cmpt += 1

        n_cmpt += 1

        while n_cmpt < self.nIndexSize and n_cmpt < int(self.sLimit):
            try:
                n_cmpt -= 1
                x_response = self.xEs.scroll(scroll_id=s_scroll, scroll='10s')
                s_scroll = x_response['_scroll_id']
                for hit in x_response['hits']['hits']:
                    st = datetime.datetime.fromtimestamp(int(hit['_source']['timestamp_ms'])/1000)\
                        .strftime('%Y-%m-%d %H:%M:%S')
                    test = (hit['_source']['id_str'])
                    if hit['_source']['id_str'] not in self.tData.nok_id and hit['_source']['id_str'] not in \
                            self.tData.ok_id:
                        data.append(test)
                    n_cmpt += 1
                n_cmpt += 1
            except:
                print('test')
                break

        return data

    def init_tri(self):
        x_response = self.xEs.update_by_query(index=self.sIndexName,
                                     body={"query": {"match_all": {}},
                                           "script": {"inline": "ctx._source."+ self.sTriName +" = 0"}})

    def save_data(self, id_str, value):
        x_response = self.xEs.search(index=self.sIndexName, doc_type=self.sDocTypeName, scroll='10m', body={"query": {
            "bool":
                {"must": [
                    {"match":
                         {"id_str":
                              {"query": id_str}}},
                    {'range': {'timestamp_ms': {'gte': self.sDateBegin, 'lte': self.sDateEnd}}}]}}})

        self.nIndexSize = int(x_response['hits']['total'])
        internal_id = x_response['hits']['hits'][0]['_id']

        x_response = self.xEs.update(index=self.sIndexName, doc_type=self.sDocTypeName, id=internal_id,
                                     body={"script": "ctx._source." + self.sTriName + "= " + str(value)})
        #
        # print(id_str)