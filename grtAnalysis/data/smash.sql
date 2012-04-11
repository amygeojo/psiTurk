type: mysql
user: lab
password: 2research
host: smash.psych.nyu.edu
dbname: mt_experiments
query: SELECT workerid, cond, counterbalance, codeversion, beginhit, status, datastring FROM tvexp WHERE (status = 4) OR (status = 5)
