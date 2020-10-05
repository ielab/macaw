"""
The Pyserini search engine.

Authors: Hang Li (hang.li4@uq.net.au)
"""

from pyserini.search import SimpleSearcher

from macaw.core.retrieval.doc import Document
from macaw.core.retrieval.search_engine import Retrieval


class Pyserini(Retrieval):
    def __init__(self, params):
        super().__init__(params)
        self.results_requested = self.params['results_requested'] if 'results_requested' in self.params else 1
        self.searcher = SimpleSearcher(self.params['pyserini_index'])
        self.searcher.set_bm25(0.9, 0.4)
        self.searcher.set_rm3(5, 3, 0.5)

    def retrieve(self, query):
        query_results = self.searcher.search(query, k=self.results_requested)
        results = []
        for item in query_results:
            doc = self.get_doc_from_index(item.docid)[0]
            doc.id = item.docid
            doc.score = item.score
            results.append(doc)
        return results

    def get_doc_from_index(self, doc_id):
        doc = self.searcher.doc(doc_id)
        title = doc.get('report_title')
        pdf_url = doc.get('pdf_url')
        web_url = doc.get('web_url')
        contents = doc.contents()
        d = Document(doc_id, title, contents, 0., web_url, pdf_url)
        return [d]
