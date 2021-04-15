#File Tree
```
words
├── README.md
├── docker-compose.yaml
├── requirements.txt
├── setup.py
├── test
│   ├── __init__.py
│   ├── commands
│   │   └── __init__.py
│   └── service
│       ├── __init__.py
│       ├── test_delete_service.py
│       ├── test_post_service.py
│       └── test_search_service.py
├── word
│   ├── __init__.py
│   ├── cli.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── cmd_cli.py
│   │   └── utils.py
│   ├── config.py
│   ├── model
│   │   ├── __init__.py
│   │   ├── dictionary.py
│   ├── service
│   │   ├── __init__.py
│   │   ├── delete_service.py
│   │   ├── post_service.py
│   │   └── search_service.py
│   └── utils.py
└── wordsapi_sample.json
```

--------------------------------------------------------------------------------------------

#Setup

```
    docker compose up -d
    
    brew install virtualenv
    
    virtualenv venv
    
    source venv/bin/activate
    
    pip install .
```

Post wordsapi_sample.json
```
    word cli post {file path}
```

Delete indices
```
    word cli delete
```

Search word or example sentences
```
    word: word cli search {word}
    
    example sentence: word cli search {word} -e
    
    document: word cli search {word} -d
```

--------------------------------------------------------------------------------------------
#Multiple ways to improve the search engine

Post의 성능 향상
```
post의 성능을 향상 시키기 위해, bulk request를 사용했습니다. 
bulk의 chuck size가 500이기 때문에 500을 기준으로 benchmark를 진행하였습니다.   

Size 300: 1 round - 345.5526201725006   sec   |   2 round - 343.08479285240173 sec 
                                              |  
Size 500: 1 round - 251.180734872818    sec   |   2 round - 251.35249996185303 sec
                                              |
Size 1000: 1 round - 254.36213183403015 sec   |   2 round - 254.26697492599487 sec
                                              |
Size 2000: 1 round - 258.06533885002136 sec   |   2 round - 259.1686267852783  sec
                                               
                                               Post를 200번 요청하여 결과를 받기 까지의 시간.
```
결과적으로 batch size를 500으로 설정하였을때 최적의 결과를 보여준다. 

```
Size 500: 1 round - 244.11668300628662 sec    |  2 round - 243.90434217453003  sec
                                               
                                               Post를 200번 요청하여 결과를 받기 까지의 시간.
```
index의 mappings을 사용한 값을 보여준다. 이전의 값과 비교하였을때, 향상된 성능을 보여준다. 


------------------------------------------------------------------------------------
Search의 성능 향상

###1. shard

``` 
     한번에 많은 양의 request를 받았을때, shard의 개수가 검색 성능을 향상시키는데 영향을 줄 수 있다. 

                            Shard num: 1                        shard num: 3
                
     1 round            3.4565341472625732 sec              1.763411045074463  sec
     2 round            3.7890970706939697 sec              1.7218880653381348 sec
     3 round            3.8013930320739746 sec              1.8412392139434814 sec
     4 round            4.029897928237915  sec              2.785281181335449  sec
     5 round            4.308093786239624  sec              2.243682861328125  sec
     6 round            3.677070140838623  sec              2.0040361881256104 sec
     7 round            3.4081621170043945 sec              1.9161927700042725 sec
     8 round            2.8633573055267334 sec              2.3039710521698    sec
     9 round            3.09560489654541   sec              2.0648908615112305 sec
    10 round            4.734143972396851  sec              2.4587149620056152 sec
        
                   avg: 3.7163354396820067 sec         avg: 2.110330820083618  sec
                                        
                                                search를 1000번 요청하여 결과를 받기 까지의 시간.
``` 
------------------------------------------------------------------------------------

###2. ASCII folding token filter
```
                          (W/O ASCII folding)                (With ASCII folding)
     1 round            3.4565341472625732 sec              1.6874911785125732 sec
     2 round            3.7890970706939697 sec              1.5512290000915527 sec
     3 round            3.8013930320739746 sec              1.5330629348754883 sec
     4 round            4.029897928237915  sec              1.541114091873169  sec
     5 round            4.308093786239624  sec              1.5603041648864746 sec
     6 round            3.677070140838623  sec              1.445824146270752  sec
     7 round            3.4081621170043945 sec              1.8313138484954834 sec
     8 round            2.8633573055267334 sec              2.085002899169922  sec
     9 round            3.09560489654541   sec              2.0446016788482666 sec
    10 round            4.734143972396851  sec              2.644033908843994  sec
        
                   avg: 3.7163354396820067 sec          avg: 1.7923977851867676 sec
                   
                   
                                            search를 1000번 요청하여 결과를 받기 까지의 시간.
```

Nutella의 영어 공부를 위한 시스템을 만드는것이 과제의 목표 이기 때문에, 검색 대상의 단어와 예문은 영어로 한정된다. 
Benchmark를 확인하면, ASCII Folding을 적용하였을때, 검색 성능이 많이 향상되는것을 알 수 있다.  

elasticsearch에 document를 post할때 ASCII Folding analyzer를 검색 대상에 추가해 주면 된다.  

```
folding_analyzer = analyzer(
    'folding_analyzer',
    tokenizer="standard",
    filter=["lowercase", "asciifolding"]
)


class Dictionary(Document):
    word: Text(analyzer=folding_analyzer)
    definitions: Text()
    syllables: Text()
    pronunciation: Text()
    rhyme_patterns: Text()
    frequency: Text()
    letters: Integer()
    sounds: Integer()
    examples: list[Text(analyzer=folding_analyzer)]
```

elasticsearch_dsl을 사용하여 작성한 document에 검색 대상이 되는 examples과 word에 analyzer를 추가한 모습이다.

###3. Prefix length

```
                  <prefix_length: None>               <prefix_length: 1>                  <prefix_length: 2>
   1 round      28.594666957855225  sec             34.19754695892334   sec             43.60235285758972   sec
   2 round      47.86689209938049   sec             46.341793060302734  sec             43.065855979919434  sec
   3 round      46.53716516494751   sec             44.98031401634216   sec             43.949942111968994  sec
   4 round      50.50426983833313   sec             45.391807079315186  sec             44.561277866363525  sec
   5 round      47.29262185096741   sec             45.3971471786499    sec             43.950685024261475  sec
   6 round      48.702868938446045  sec             45.21590614318848   sec             44.106505155563354  sec
   7 round      49.00595021247864   sec             45.836780071258545  sec             45.144521951675415  sec
   8 round      50.969626665115356  sec             44.66949677467346   sec             44.29913592338562   sec
   9 round      49.00327396392822   sec             44.80926203727722   sec             44.28098392486572   sec
  10 round      49.5166962146759    sec             45.23629808425903   sec             44.36857509613037   sec
        total: 467.99403190612793   sec      total: 442.07635140419006  sec      total: 441.32983589172363  sec

                                                       각각의 round는 search를 10,000번 요청하여 결과를 받기 까지의 시간.
```

검색 선능을 향상시킬 수 있는 또다른 방법은, prefix 옵션을 사용하는것이다. 대부분의 오타는 단어의 중간 또는 마지막 부분에서 발생한다. 첫 단어부터 오타가 발생하는
경우는 거이 없다. Benchmark는 prefix의 값을 다르게 설정하였을때 나오는 차이를 보여준다.

###4. Multi Queries
```
                        <Multi Queries>                   <Match - Fuzzyness>
   1 round          25.279136896133423  sec             43.60235285758972   sec
   2 round          48.654414892196655  sec             43.065855979919434  sec
   3 round          50.0985381603241    sec             43.949942111968994  sec
   4 round          51.193500995635986  sec             44.561277866363525  sec
   5 round          49.93040609359741   sec             43.950685024261475  sec
   6 round          50.95412802696228   sec             44.106505155563354  sec
   7 round          49.68225812911987   sec             45.144521951675415  sec
   8 round          50.037113904953     sec             44.29913592338562   sec
   9 round          49.23568892478943   sec             44.28098392486572   sec
  10 round          50.3095269203186    sec             44.36857509613037   sec
            total: 475.37471294403076   sec      total: 441.32983589172363  sec
                            각각의 round는 search를 10,000번 요청하여 결과를 받기 까지의 시간.
```

```
              <Multi Queries>                              <Match - Fuzzyness>
            max_score: 36.26639,                          max_score: 9.066598
            hits:                                         hits:
                -score: 36.26639,                             -score: 9.066598
                -source:                                      -source:
                    -word: apple,                                 -word: apple
                -score: 27.506413,                            -score: 6.876603
                -source:                                      -source:
                    -word: apple-polisher                         -word: apple-polisher   
```
왼쪽은 Multi Queries를 사용하여 apple을 검색한 결과이고, 오른쪽은 match를 이용하여 apple을 검색한 결과 이다. 검색의 속도에서는 오른쪽의 match가 좋은 성능을 보여 준다.
또한 두 검색 모두 apple을 가장 연관된 단어로 검색 할 수 있었다. 하지만 score에서 큰 차이를 보인다.

```
  "match":                                  |     "match":                                  |   "match_phrase":
      key:                                  |         key:                                  |       key:
          "query": value,                   |             "query": value,                   |           "query": value,
          "fuzziness": "auto",              |             "fuzziness": "auto",              |           "boost": 2
          'fuzzy_transpositions': True,     |             'fuzzy_transpositions': True,     |
          "prefix_length": 1,               |             "prefix_length": 1,               |
                                            |             "operator": "and"                 |
                                            |                                               |      
                                 조건 1                                            조건 2                           조건 3
```
Multi Queries에서 사용된 조건이다. match를 위해 사용된 조건은 1번이었지만, multi queries에서는 2번과 3번 조건을 추가 하였다.
추가된 조건을 통하여, 일치하는 단어의 score에 가중치를 부여 할 수 있게 되었으며, 검색의 정확도 향상을 기대 할 수 있다.

이번 과제에서, post의 성능을 향상 시키기 위해 mappings을 사용하였으며, search 성능을 향상 시키기 위해서, ascii folding, prefix lengh, and multi queries를 사용하였다.

###How to measure the scoring of the search engine?
elasticsearch에서 score를 계산하기위해 tf/idf를 사용한다. 

Term frequency(tf)는 해당 다큐먼트에 검색한 단어의 빈도 수를 의미한다.

Inverse Document frequency(idf)는 전체 다큐먼트중 단어가 등장하는 빈도의 역을 의미한다. (전체의 다큐먼트에서 빈번하게 등장하는 단어의 가중치를 낮추기 위한 용도)

term frequency가 클수록, document frequency가 작을수록 score는 커지게 된다. 

Field length 또한 score에 영향을 준다. 전체 다큐먼트에서 검색한 단어가 차지하는 비율이 클 수록 score에 가중치가 부여된다. 

------------------------------------------------------------------------------------
# Link between best search engine score and performance

Search 성능의 향상 4번의 benchmark를 보면, best search engin score와 performance의 관계를 알 수 있다. 검색을 정확하게 하기 위해 다양한 조건을 추가 할 수록
performance는 감소하게 된다. 결국, 정확성과 속도는 trade-off 관계이다.   
