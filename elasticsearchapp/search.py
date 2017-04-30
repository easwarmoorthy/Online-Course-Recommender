from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search

connections.create_connection()

class CourseModelIndex(DocType):
    title = Text()
    short_summary = Text()
    summary = Text()

def bulk_indexing():
    CourseModelIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.CourseModel.objects.all().iterator()))

def search(title):
    s = Search().filter('term', title=title)
    response = s.execute()
    return response
