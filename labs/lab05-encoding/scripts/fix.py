from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "evidence" / "staff-broken.csv"
target = root / "evidence" / "staff-fixed.csv"
raw = source.read_bytes()
text = raw.decode("kz1048")
text = text.replace("\r\n", "\n")
target.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
print("Converted KZ-1048 to UTF-8 with BOM and LF line endings")
print("Output:", target)
