Install packages and then on 4 different terminals, run:
```
$ INDEX_PATH="inverted_index_0.txt" flask --app index run --host 0.0.0.0 --port 9000
$ INDEX_PATH="inverted_index_1.txt" flask --app index run --host 0.0.0.0 --port 9001
$ INDEX_PATH="inverted_index_2.txt" flask --app index run --host 0.0.0.0 --port 9002
$ flask --app search run --host 0.0.0.0 --port 8000
```
Navigate to localhost:8000.