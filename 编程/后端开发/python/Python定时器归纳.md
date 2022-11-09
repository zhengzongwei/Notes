# Python 定时器归纳

> Python中定时任务的解决方案，总体来说有四种，分别是： crontab、 scheduler、 Celery、 APScheduler，其中 crontab不适合多台服务器的配置、 scheduler太过于简单、 Celery依赖的软件比较多，比较耗资源。最好的解决方案就是 APScheduler。

## crontab

## scheduler

## Celery

## APScheduler

```python
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def my_clock():
    print(f'Hello! The time is {datetime.now()}')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(my_clock, 'interval', seconds=3)
    scheduler.start()

```







```shell
{
    "message": null,
    "code": 0,
    "data": [
    
	]
}
```

