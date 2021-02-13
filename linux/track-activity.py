from crontab import CronTab
import click
import os

def set_crontab_task():
    cron = CronTab(user=True)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'script.py')
    print(path)
    if path in cron.crons:
        print("job already present")
    else:
        cmd = f'env DISPLAY=:0 python3 {path}'
        job = cron.new(command= cmd)
        job.minute.every(1)
        cron.write()
        print("job is setup finished!")

@click.command()
@click.option('--time', default=1, help='Number of days')
@click.option('--sendmail',is_flag=True,help='Mail will be sent if the user!')
def trackx(time,sendmail):
    """Trackx is the program which tracks your"""
    if sendmail:
        click.echo("Mail will be sent!")
    if time > 1:
        click.echo(f'You have set time as {time}')
    set_crontab_task()

if __name__ == '__main__':
    trackx()