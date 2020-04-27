# Database performance

|            | Find Entry | Remove Entry | Upsert Entry | Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: |
| PostgreSQL |   689.94   |    897.67    |    547.85    |  7,230.86   |
| MongoDB    |  1,373.88  |    572.77    |   2,516.66   |  14,199.87  |
| MySQL      |   649.42   |    885.60    |    373.24    |  14,636.07  |
| SQLite     |   487.21   |    469.26    |    372.24    |  44,137.56  |

## Lets add some colors!

|            | Find Entry | Remove Entry | Upsert Entry | Insert Dump | Good in Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: | :-----------------: |
| PostgreSQL |   689.94   |    897.67    |    547.85    |  7,230.86   |    :thumbsdown:     |
| MongoDB    |  1,373.88  |    572.77    |   2,516.66   |  14,199.87  |    :thumbsdown:     |
| MySQL      |   649.42   |    885.60    |    373.24    |  14,636.07  |    :thumbsdown:     |
| SQLite     |   487.21   |    469.26    |    372.24    |  44,137.56  |     :thumbsup:      |

## Or a ranking?

|            | Find Entry | Remove Entry | Upsert Entry | Insert Dump | Ranking by Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: | :--------------------: |
| PostgreSQL |   689.94   |    897.67    |    547.85    |  7,230.86   |   :1st_place_medal:    |
| MongoDB    |  1,373.88  |    572.77    |   2,516.66   |  14,199.87  |   :2nd_place_medal:    |
| MySQL      |   649.42   |    885.60    |    373.24    |  14,636.07  |   :3rd_place_medal:    |
| SQLite     |   487.21   |    469.26    |    372.24    |  44,137.56  |          # 4           |

## Define a baseline and see the gains!

|            | Find Entry | Gains in Find Entry |
| :--------- | :--------: | :-----------------: |
| SQLite     |   487.21   |         1x          |
| MySQL      |   649.42   |        1.33x        |
| PostgreSQL |   689.94   |        1.42x        |
| MongoDB    |  1,373.88  |        2.82x        |

