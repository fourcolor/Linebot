from apscheduler.schedulers.blocking import BlockingScheduler
import requests
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    url = "https://line-bot-fourcolor.herokuapp.com/"
    conn = requests.get(url)
        

sched.start()