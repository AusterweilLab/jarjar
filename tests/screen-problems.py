

# screen config
old='/usr/bin/screen'
new='/usr/local/bin/screen'
pid = 'jjtest'

template = ''' screen -x <screen.PID> -p 0 -X stuff 'echo $varname' '''

