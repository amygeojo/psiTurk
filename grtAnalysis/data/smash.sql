type: mysql
user: lab
password: 2research
host: smash.psych.nyu.edu
dbname: mt_experiments
query: SELECT workerid, cond, counterbalance, codeversion, beginhit, status, datastring FROM tvexp WHERE ((status = 3) OR (status = 4) OR (status = 5)) AND (codeversion = 1.2 OR codeversion = 1.3 OR codeversion = 1.4)
