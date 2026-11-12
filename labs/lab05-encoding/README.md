# lab 5 - encoding forensics

machine: windows 11 
date: 12.11.2026

## what i did

first, i checked the broken csv file to find the problem. some kazakh and russian letters were not showing correctly.

i checked the file encoding, line endings and the first 16 bytes.

the original encoding was kz-1048. the file used crlf line endings and had no bom.

then i used a python script to convert the file to utf-8 with bom and lf line endings.

```powershell
py .\scripts\fix.py
```

## result

the script worked and created a new file called `staff-fixed.csv`.

i opened the new file in excel and the names looked normal. the kazakh and russian letters were correct.

the original file was not deleted.

## what did not work the first time

at first, python did not work when i typed `python` in powershell. windows said python was not found.

i tried using `py` instead and it worked. after that, the script converted the file.

## evidence

- `evidence/staff-broken.csv` - original file
- `evidence/staff-fixed.csv` - fixed file
- `evidence/file-before.txt` - information before fixing
- `evidence/file-after.txt` - information after fixing
- `evidence/hexdump-before.txt` - first 16 bytes
- `evidence/excel-check.png` - csv opened in excel
- `scripts/fix.py` - script used to fix the file
