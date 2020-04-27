# Database performance

|  | Upsert Entry | Find Entry | Remove Entry | Insert Dump |
| :--- | :---: | :---: | :---: | :---: |
| SQLite | 372.24 | 487.21 | 469.26 | 44,137.56 |
| MongoDB | 2,516.66 | 1,373.88 | 572.77 | 14,199.87 |
| PostgreSQL | 547.85 | 689.94 | 897.67 | 7,230.86 |
| MySQL | 373.24 | 649.42 | 885.60 | 14,636.07 |

## Lets add some colors!

|  | Upsert Entry | Find Entry | Remove Entry | Insert Dump | Good in Insert Dump |
| :--- | :---: | :---: | :---: | :---: | :---: |
| SQLite | 372.24 | 487.21 | 469.26 | 44,137.56 | :thumbsup: |
| MongoDB | 2,516.66 | 1,373.88 | 572.77 | 14,199.87 | :thumbsdown: |
| PostgreSQL | 547.85 | 689.94 | 897.67 | 7,230.86 | :thumbsdown: |
| MySQL | 373.24 | 649.42 | 885.60 | 14,636.07 | :thumbsdown: |

## Or a ranking?

|  | Upsert Entry | Find Entry | Remove Entry | Insert Dump | Ranking by Insert Dump |
| :--- | :---: | :---: | :---: | :---: | :---: |
| SQLite | 372.24 | 487.21 | 469.26 | 44,137.56 | :1st_place_medal: |
| MongoDB | 2,516.66 | 1,373.88 | 572.77 | 14,199.87 | :3rd_place_medal: |
| PostgreSQL | 547.85 | 689.94 | 897.67 | 7,230.86 | # 4 |
| MySQL | 373.24 | 649.42 | 885.60 | 14,636.07 | :2nd_place_medal: |

## Define a baseline and see the gains!

|  | Find Entry | Gains in Find Entry |
| :--- | :---: | :---: |
| SQLite | 487.21 | 1x |
| MySQL | 649.42 | 1.33x |
| PostgreSQL | 689.94 | 1.42x |
| MongoDB | 1,373.88 | 2.82x |

