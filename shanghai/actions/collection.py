class CollectionMixin(object):

    def get_collection_data(self):
        return self.get_queryset()

    def get_collection(self):
        data = self.get_collection_data()

        return self.response(data)
