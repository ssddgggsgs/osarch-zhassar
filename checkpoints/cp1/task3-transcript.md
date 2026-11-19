# task 3 - nightly report

## transcript

| # | evidence file (command) | what i expected | what i found | what i concluded |
|---|---|---|---|---|
| 1 | 00-README.txt | see what files we have | the pack has a list of commands and files | i will check the files one by one |
| 2 | 05-systemctl-failed.txt (`systemctl --failed`) | maybe the report failed | nightly-report and legacy-sync failed | i need to check both |
| 3 | 10-systemctl-status-legacy-sync.txt (`systemctl status legacy-sync.service`) | maybe this is the problem | it is an old sync service with `/bin/false` | i think it is not about the report |
| 4 | 06-systemctl-list-timers.txt (`systemctl list-timers`) | maybe the timer is off | the report ran at 09:42 and the next run is 09:44 | the timer looks okay |
| 5 | 07-systemctl-status-nightly-report.txt (`systemctl status nightly-report.service`) | see why the report failed | error `203/EXEC` and no such file | the script cannot start |
| 6 | 08-systemctl-cat-nightly-report.txt (`systemctl cat nightly-report.service nightly-report.timer`) | see the script path | it uses `/usr/local/bin/nightly-report.sh` and runs every 2 minutes | i will check this file |
| 7 | 13-ls-l-usr-local-bin.txt (`ls -l /usr/local/bin`) | maybe the script is missing | the file is there and has execute permission | it is not missing |
| 8 | 03-df-h.txt (`df -h`) | maybe the disk is full | there is 5.8 gb free | disk space is okay |
| 9 | 14-ls-l-var-log.txt (`ls -l /var/log`) | maybe the log is missing | the log exists but was last changed on nov 9 | the report stopped writing |
| 10 | 09-journalctl-nightly-report.txt (`journalctl -u nightly-report.service`) | see when the error started | it worked at 14:18 but failed at 14:20 | something changed at this time |
| 11 | 22-bash-history-aigerim.txt (`tail -n 15 ~/.bash_history`) | see if the script was changed | a script was copied and chmod was used | maybe the new script is the problem |
| 12 | 19-run-by-hand.txt (`/usr/local/bin/nightly-report.sh`) | maybe it works by hand | it says `cannot execute: required file not found` | it also fails without the timer |
| 13 | 16-cat-nightly-report-sh.txt (`cat /usr/local/bin/nightly-report.sh`) | see the script | it starts with `#!/bin/bash` | the text looks normal, but i will check more |
| 14 | 20-ls-l-bin-bash.txt (`which bash; ls -l /bin/bash`) | maybe bash is missing | `/bin/bash` exists | bash is not missing |
| 15 | 17-cat-A-nightly-report-sh.txt (`cat -A /usr/local/bin/nightly-report.sh`) | check for hidden symbols | there is `^M` at the end of lines | it has windows line endings |
| 16 | 18-head-1-od-c.txt (`head -1 /usr/local/bin/nightly-report.sh \| od -c`) | check the first line | it ends with `\r\n` | this explains why linux cannot start it |

## root cause

the script has windows line endings (`crlf`). file 17 shows `^M` and file 18 shows `\r\n` after `#!/bin/bash`. linux cannot find the correct interpreter because of this. the timer itself works, as file 06 shows.

## fix

i only have the evidence files, so these are the commands i would use on the server. i did not run them.

```bash
sudo cp /usr/local/bin/nightly-report.sh /usr/local/bin/nightly-report.sh.bak
sudo sed -i 's/\r$//' /usr/local/bin/nightly-report.sh
head -1 /usr/local/bin/nightly-report.sh | od -c
sudo systemctl reset-failed nightly-report.service
sudo systemctl start nightly-report.service
```

first i make a backup. then i change the line endings to linux format. after that i check the first line and try to start the service again.

## verification

```bash
systemctl status nightly-report.service
sudo journalctl -u nightly-report.service -n 15 --no-pager
tail -n 20 /var/log/nightly-report.log
systemctl list-timers --all
systemctl is-enabled nightly-report.timer
```

i expect no more `203/EXEC` error. the service should finish without an error and the log should have a new date, disk and memory information. the timer should still run every 2 minutes.

for checking after reboot i would use:

```bash
sudo reboot
```

then i would connect to the server again and run:

```bash
systemctl is-enabled nightly-report.timer
systemctl list-timers --all
sudo journalctl -u nightly-report.service -b --no-pager
tail -n 20 /var/log/nightly-report.log
```

i expect the timer to be enabled and the log to get a new report after the next run. if the timer is disabled, i would use `sudo systemctl enable --now nightly-report.timer` and check again.
