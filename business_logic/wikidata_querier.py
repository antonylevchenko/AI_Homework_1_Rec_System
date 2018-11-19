from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get

# This class can obtain id's for wikidata entities using real name of the movie.
# Than it uses it to get required information about actors and characters from the movie.

class Wikidata_Querier:
    __sparql_wrapper: SPARQLWrapper

    def __init__(self):
        self.__sparql_wrapper = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.__sparql_wrapper.setReturnFormat(JSON)

    @staticmethod
    def get_q_id(real_movie_name: str):
        json = get('https://www.wikidata.org/w/api.php', {
            'action': 'wbgetentities',
            'titles': real_movie_name,
            'sites': 'enwiki',
            'props': '',
            'format': 'json'
        }).json()
        result = list(json['entities'])[0]
        return result

    #simplify_result may be used to create shorter version of the query result with the most important information.
    def get_information_for_movie(self, real_movie_name: str, simplify_result: bool):
        q_id = Wikidata_Querier.get_q_id(real_movie_name)

        self.__sparql_wrapper.setQuery("""
        SELECT ?actor ?actorLabel ?character ?characterLabel
        WHERE {  
          wd:Q47703
          p:P161 [
                    ps:P161 ?actor;
                    pq:P453 ?character
                  ];
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """)

        result = self.__sparql_wrapper.query().convert()
        if(simplify_result):
            result = Wikidata_Querier.__simplify_result(result)
        return result;

    @staticmethod
    def __simplify_result(result_data):
        simplified_result = {}
        for id, result in enumerate(result_data['results']['bindings']):
            simplified_result[id] = {'actorLabel': result['actorLabel']['value'],
                                     'actorLink': result['actor']['value'],
                                     'characterLabel':result['characterLabel']['value'],
                                     'characterLink':result['character']['value']}
        return simplified_result

