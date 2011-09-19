


class MinusList(object):
    
    object_cls = None

    _client = None
    _url = None
    _initialized = False
    _items = {}
    _current = 0

    def __init__(self, client, url):
        self._client = client
        self._url = url

    def _initialize(self):
        response = self._client.get(self._url)
        
        self._pages = response['pages']
        self._per_page = response['per_page']
        self._total = response['total']
        self._pages_loaded = set(0) 
        self._initialized = True


    def _add_items(self, items, start_index=0):
        index = start_index
        for item in items:
            obj = self.object_cls(self._client, item['url'], **item)
            self._items[index] = obj
            index += 1


    def _get_page(self, page_index):
        if not self._initialized:
            self._initialize()

        if page_index in self._pages_loaded or page_index >= self._pages or \
                page_index < 0:
            return
       
        params = None
        if page_index > 0:
            params = {'page': page_index}

        response = self._client.get(self._url, params)

        self._add_items(response['results'], self._per_page * page_index)
        self._pages_loaded.add(page_index)


    def flush(self):
        self._items = {}
        self._initialize()

    def __iter__(self):
        return self

    def __len__(self):
        if not self._initialized:
            self._initialize()
        return self._total

    def next(self):
        if not self._initialized:
            self._initialize()

        if self.current >= self._total:
            raise StopIteration

        try:
            next_item = self._items[self.current]
        except IndexError:
            self._get_page(self.current * self._per_page)
            next_item = self._items[self.current]

        self.current += 1
        return next_item

