# task 1 - inventory and interpret

## 1a. my laptop

i used powershell to check my laptop. the command output is in `evidence/task1.txt`.

| figure | this computer | command |
|---|---|---|
| cpu model | intel core i5-1235u | `Get-CimInstance Win32_Processor` |
| cores / logical processors | 10 / 12 | `Get-CimInstance Win32_Processor` |
| hardware virtualization | the cpu is an intel i5, but my command did not confirm support. firmware enabled says false, so i need to check bios and task manager | `Get-CimInstance Win32_Processor` |
| memory total / available now | 15.73 gib / 6.42 gib | `Get-CimInstance Win32_OperatingSystem` |
| system disk | 512.11 gb ssd (nvme), 232.40 gb free on c: | `Get-Disk`; `Get-Volume -DriveLetter C` |
| partition style | gpt | `Get-Disk` |
| os and version | windows 11 pro, 10.0.26200 | `Get-CimInstance Win32_OperatingSystem` |

my older lab 0 disk evidence says the micron drive is an nvme ssd. the new command did not show media type.

## 1b. another laptop

### can it run both guests?

in lab 1 i made an ubuntu vm with 2 cpus, 2 gb ram and 25 gb disk. i did not finish lab 2, so i do not have a real windows vm size from my build log. i cannot say i tested both guests.

for a rough check, i assume a windows 11 vm would need 2 cpus, 4 gb ram and at least 64 gb disk. i also assume the host needs about 2 cpu threads, 3 gb ram and some free disk space.

cpu: 4 threads total - 2 ubuntu - 2 windows = 0 threads left if all vcpus need to run at once. vcpus can share cpu time, but this would be slow for the host.

ram: 8 - 2 - 4 - 3 = -1 gb. there is not enough memory with my host assumption.

disk: 31 - 25 - 64 = -58 gb, even before leaving space for the host. there is not enough storage.

so i do not think it can run both guests at the same time at these assumed sizes. the windows size is only an assumption because i did not do lab 2. also, windows 11 home in s mode may limit installing normal vm software unless s mode is switched off.

### what would i change first?

i would change the storage first because 31 gb free is not enough even for the two virtual disks. but the 128 gb emmc is soldered, so i cannot just replace it. the ram is also soldered. i would use another computer with more ram and an ssd instead. i would also check the vm software situation with s mode.
