# Database performance

|            | Find Entry | Upsert Entry | Remove Entry | Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: |
| PostgreSQL |   689.94   |    547.85    |    897.67    |  7,230.86   |
| MongoDB    |  1,373.88  |   2,516.66   |    572.77    |  14,199.87  |
| MySQL      |   649.42   |    373.24    |    885.60    |  14,636.07  |
| SQLite     |   487.21   |    372.24    |    469.26    |  44,137.56  |

## Lets add some colors!

|            | Find Entry | Upsert Entry | Remove Entry | Insert Dump | Good in Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: | :-----------------: |
| PostgreSQL |   689.94   |    547.85    |    897.67    |  7,230.86   |    :thumbsdown:     |
| MongoDB    |  1,373.88  |   2,516.66   |    572.77    |  14,199.87  |    :thumbsdown:     |
| MySQL      |   649.42   |    373.24    |    885.60    |  14,636.07  |    :thumbsdown:     |
| SQLite     |   487.21   |    372.24    |    469.26    |  44,137.56  |     :thumbsup:      |

## Or a ranking?

|            | Find Entry | Upsert Entry | Remove Entry | Insert Dump | Ranking by Insert Dump |
| :--------- | :--------: | :----------: | :----------: | :---------: | :--------------------: |
| PostgreSQL |   689.94   |    547.85    |    897.67    |  7,230.86   |          # 4           |
| MongoDB    |  1,373.88  |   2,516.66   |    572.77    |  14,199.87  |   :3rd_place_medal:    |
| MySQL      |   649.42   |    373.24    |    885.60    |  14,636.07  |   :2nd_place_medal:    |
| SQLite     |   487.21   |    372.24    |    469.26    |  44,137.56  |   :1st_place_medal:    |

## Define a baseline and see the gains!

|            | Find Entry | Gains in Find Entry |
| :--------- | :--------: | :-----------------: |
| SQLite     |   487.21   |         1x          |
| MySQL      |   649.42   |        1.33x        |
| PostgreSQL |   689.94   |        1.42x        |
| MongoDB    |  1,373.88  |        2.82x        |

