# Lab 0 — Inventory your own machine

Machine: Lenovo laptop, Windows
Date: 21.10.2026

## What I did

All values were read from PowerShell only, no graphical "About" screens.

```powershell
Get-CimInstance Win32_Processor
Get-CimInstance Win32_PhysicalMemory
Get-CimInstance Win32_ComputerSystem
Get-PhysicalDisk
Get-Volume
Get-CimInstance Win32_BIOS
(Get-ComputerInfo).BiosFirmwareType
```

## Result

| What | Value | Where I got it |
|---|---|---|
| CPU model | 12th Gen Intel Core i5-1235U | `Get-CimInstance Win32_Processor` |
| Cores / threads | 10 cores / 12 threads | `Get-CimInstance Win32_Processor` |
| RAM total | 16 GB (16 890 978 304 bytes) | `Get-CimInstance Win32_ComputerSystem` |
| RAM modules / speed | 2 modules x 8 GB (Samsung + Micron), 3200 MHz | `Get-CimInstance Win32_PhysicalMemory` |
| Disk model / type | Micron MTFDKCD512QFM-1BD1AABLA, 512 GB, NVMe SSD | `Get-PhysicalDisk` |
| Free space on C: (VM volume) | about 301 GiB free of 476 GiB (323 098 058 752 bytes) | `Get-Volume` |
| Firmware type | UEFI | `(Get-ComputerInfo).BiosFirmwareType` |
| Firmware version / date | LENOVO JKCN47WW, 21.08.2024 | `Get-CimInstance Win32_BIOS` |
| Hardware virtualization | Present and working: `HypervisorPresent = True` (see below) | `Win32_Processor`, `Win32_ComputerSystem` |

## What did not work the first time

1. `VirtualizationFirmwareEnabled` showed `False`, which looks like virtualization is off. I checked `(Get-CimInstance Win32_ComputerSystem).HypervisorPresent` and it returned `True`. That means Windows already runs its own hypervisor on top of the hardware virtualization, so the processor-level field reports `False` even though virtualization is on. I did not change anything in BIOS.
2. My GitHub repository was empty and existed only on the website, so I used `git clone` to create the local folder and then unpacked `repo_starter.zip` into it.
3. `firmware.txt` first had no firmware type line, and then the type was written twice because I ran the command twice. I regenerated the file from scratch.

## Evidence

- [evidence/cpu.txt](evidence/cpu.txt) — CPU model, cores, threads, virtualization fields
- [evidence/memory.txt](evidence/memory.txt) — two RAM modules, speed, total memory
- [evidence/disk.txt](evidence/disk.txt) — disk model and type, free space per volume
- [evidence/firmware.txt](evidence/firmware.txt) — BIOS vendor, version, date, UEFI type
