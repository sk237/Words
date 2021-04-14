
```
File Tree

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
│   │   └── dictionary.py
│   ├── service
│   │   ├── __init__.py
│   │   ├── delete_service.py
│   │   ├── post_service.py
│   │   └── search_service.py
│   └── utils.py
└── wordsapi_sample.json
```

--------------------------------------------------------------------------------------------


Setup

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
Multiple ways to improve the search engine

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

결과적으로 batch size를 500으로 설정하였을때 최적의 결과를 보여준다. 


Size 500: 1 round - 244.11668300628662 sec    |  2 round - 243.90434217453003  sec
                                               
                                               Post를 200번 요청하여 결과를 받기 까지의 시간.

index의 mappings을 사용하면 조금더 성능을 향상 시킬 수 있다. 
```


Search의 성능 향상

1. shard의 개수를 조절한다.

------------------------------------------------------------------------------------
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
    
2. Cache server.
```
    elasticsearch의 match query는 cache가 적용되지 않는다. (Filter는 cache를 사용할 수 있지만, 오타를 고려한 단어 검색을 위해 고려하지 않았다.)
    비슷한 오타를 반복적으로 발생하는 상황에서 cache server는 성능향상에 중요한 역할을 할 수 있다. (새로운 단어가 추가 되지 않을 경우)
    client와 elasticsearch 사이에 cache server를 추가 하여, 오타에 해당하는 결과값을 cache값을 client에가 빠르게 전달 할 수 있다.

1번과 2번의 많은양의 search request가 생성될 때 성능을 향상 시킬 수 있다. 

하지만 이번 과제의 경우, Nutella를 위한 단어 또는 예문 검색 시스템을 개발 하는것 이다. 
이 경우, 많은 양의 search request는 기대 되지 않으며, Cache hit을 기대 하기도 어렵다. 
그래서 이번 과제에서, cache server와 shard의 개수는 고려하지 않았다.  

```

3. ASCII folding token filter
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
                                            
    Nutella의 영어 공부를 위한 시스템을 만드는 것 이기 때문에, 단어와 예문은 영어로 한정된다. 이 경우 ASCII folding token filter를 사용하면 
    검색 성능을 향상시킬 수 있다. benchmark는 성능 ASCII folding을 적용한것과 하지 않은것의 성능 차이를 보여준다.
    