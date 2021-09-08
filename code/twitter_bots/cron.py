
#code modified from https://github.com/matiasandina/homecage_quantification/blob/master/setup_cron.py
from crontab import CronTab
# this is what we want to run
cmd_command = "bash ~/bots/openneuro/python-caller.sh"

job_comment = "run twitter bot"

# Get cron object
cron = CronTab(user="pi")
# don't create a new job if it is already there
# first check if it's already there

job_exists = any(list(map(lambda x: x.comment == job_comment, cron)))

if job_exists:
    for job in cron:
        if job.comment == job_comment:
            print("job named: " + job_comment + " already exists, scheduling 1 minute")
            job.minute.every(5)
            # write the program
            cron.write()
            #print("job: ")
            #print(job)
else:
    # only here, create it
    # create a new job
    print ("start new job")
    job = cron.new(command = cmd_command, comment=job_comment)
    # schedule it every 20 minutes
    job.minute.every(5)
    # write the program
    cron.write()
    #print(job)

print("Current cron tab (same as $ crontab -l)")
print("--------------------------------------")
print(cron)
