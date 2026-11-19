# task 2 - plan and justify

## my computer

my laptop has 10 cpu cores, 12 logical processors, about 15.73 gib ram and 232.40 gb free on c:. i want the host to stay usable. the command says virtualization firmware enabled is false, so first i need to check and enable virtualization in bios if it is really off. without that, i cannot promise these vms will run.

## allocation

| part | ubuntu server | windows 11 |
|---|---|---|
| cpu | 2 vcpu | 2 vcpu |
| ram | 2 gib | 4 gib |
| virtual disk | 25 gb, dynamic | 64 gb, dynamic |
| network | nat plus host-only adapter | nat |

for ubuntu, nat is for internet and host-only is for ssh from the host. i chose two adapters because it is easy to check each connection. windows only needs nat for this task. i chose dynamic disks to avoid using all disk space immediately, but they can grow to their maximum size. windows 11 also needs compatible virtual tpm and secure boot settings.

## arithmetic

cpu: 12 logical processors - 2 - 2 = 8 not assigned to guests. this is only a simple planning number because vcpus share physical cpu time.

ram: 15.73 - 2 - 4 = 9.73 gib left for the host. i assume windows on the host needs about 8 gib, so this leaves about 1.73 gib extra. right now my host has only 6.42 gib available, so i should close programs before starting both guests and check memory again. this plan might still be slow.

disk: 232.40 - 25 - 64 = 143.40 gb left if both virtual disks grow to full size. i want to keep at least 50 gb free for the host, so this fits on paper.

i used 2 gib for ubuntu because it is a server without a big desktop. i used 4 gib for windows because it is the minimum i would try, not a comfortable amount. i did not choose bigger sizes because i need memory for the host too.

## verification plan

these are the commands i would use after building the guests. i have not run them yet.

| where | command | what i expect |
|---|---|---|
| ubuntu guest | `nproc` | `2` |
| ubuntu guest | `free -h` | about 2 gib total memory |
| ubuntu guest | `lsblk` | a virtual disk around 25 gb |
| ubuntu guest | `ip -br addr` | addresses on nat and host-only adapters |
| ubuntu guest | `systemctl status ssh` | ssh service active, after installing and enabling it |
| ubuntu guest | `ping -c 4 1.1.1.1` | replies, showing internet ip access |
| ubuntu guest | `getent hosts example.com` | an ip address, showing dns works |
| windows guest (powershell) | `Get-CimInstance Win32_Processor | Select NumberOfLogicalProcessors` | 2 logical processors |
| windows guest (powershell) | `Get-CimInstance Win32_ComputerSystem | Select TotalPhysicalMemory` | around 4 gb ram |
| windows guest (powershell) | `Get-Disk` | virtual disk around 64 gb |
| host (powershell) | `ssh username@HOST_ONLY_IP` | ubuntu login prompt, using the real ubuntu username and host-only ip |
| host (powershell) | `Get-CimInstance Win32_OperatingSystem | Select FreePhysicalMemory` | enough free ram to keep working |

if virtualization cannot be enabled, i would not build both guests on this laptop. i would use another machine that supports virtualization. i would not claim the plan worked without testing it.
