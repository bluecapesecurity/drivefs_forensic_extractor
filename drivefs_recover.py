import os
import shutil
import argparse
import sqlite3
import csv
from datetime import datetime, timezone

# ==== Version Information ====
VERSION = "1.0.0"

# ==== Attribution & Disclaimer Banner ====
BANNER = f"""
==========================================================
  Google DriveFS Forensic Extractor & Metadata Exporter
  Version {VERSION}
  (c) 2024 Blue Cape Security, LLC
  NO WARRANTY OR LIABILITY. Use at your own risk.
==========================================================
Supported file types for recovery:
  - PDF (.pdf)
  - Office XML-format docs (.docx, .xlsx, .pptx as .zip)
  - JPEG Images (.jpg)
  - PNG Images (.png)
----------------------------------------------------------
"""

# ==== File type detection based on magic numbers ====
known_types = {
    "application/pdf": "pdf",
    "application/zip": "zip",  # Often Office docs
    "image/jpeg": "jpg",
    "image/png": "png",
}

def detect_file_type(file_path):
    with open(file_path, 'rb') as f:
        sig = f.read(8)
    if sig.startswith(b'%PDF'):
        return 'application/pdf'
    elif sig.startswith(b'PK\x03\x04'):
        return 'application/zip'  # Office files (docx, xlsx, pptx) too
    elif sig.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif sig.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    else:
        return 'unknown'

def convert_ts(val):
    """Convert Google DriveFS ms-since-epoch to ISO8601. Return empty string if not a valid int."""
    if not isinstance(val, int) or val == 0:
        return ""
    try:
        dt = datetime.fromtimestamp(val / 1000.0, tz=timezone.utc)
        return dt.isoformat()
    except Exception:
        return str(val)

def dump_items_table_to_csv(sqlite_path, output_dir):
    csv_path = os.path.join(output_dir, 'drivefs_items_table.csv')
    try:
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()
        if not rows:
            print("No rows found in items table.")
            return None

        fieldnames = rows[0].keys()
        date_fields = [k for k in fieldnames if k.endswith('_date')]

        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for row in rows:
                out_row = []
                for k in fieldnames:
                    v = row[k]
                    if k in date_fields:
                        try:
                            v = int(v)
                        except:
                            pass
                        v = convert_ts(v)
                    out_row.append(v)
                writer.writerow(out_row)
        print(f"Metadata CSV exported: {csv_path}")
        return csv_path
    except Exception as e:
        print(f"Failed to export metadata: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Blue Cape Security, LLC: Google DriveFS Forensic Artifact Recovery\n"
            "Recovers locally cached user files from Google DriveFS 'content_cache' and, optionally, "
            "exports file/folder metadata from metadata_sqlite_db to CSV (with timestamps as ISO8601 UTC).\n"
            "Supported recoverable file types: PDF, Office (as .zip), JPEG, PNG.\n"
            "NO WARRANTY OR LIABILITY. Use for forensic/educational purposes only."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-s', '--source', required=True, help='Path to the content_cache directory')
    parser.add_argument('-d', '--dest', required=True, help='Path to the output directory')
    parser.add_argument('-m', '--metadata_file', required=False, help='Path to metadata_sqlite_db file (optional)')

    args = parser.parse_args()

    print(BANNER)

    CACHE_DIR = args.source
    OUTPUT_DIR = args.dest
    METADATA_DB = args.metadata_file

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report = []

    # File recovery
    for root, dirs, files in os.walk(CACHE_DIR):
        for file in files:
            try:
                full_path = os.path.join(root, file)
                file_type = detect_file_type(full_path)
                if file_type in known_types:
                    ext = known_types[file_type]
                    new_name = f"{file}.{ext}"
                    dest_path = os.path.join(OUTPUT_DIR, new_name)
                    shutil.copy2(full_path, dest_path)
                    report.append(f"{file} --> {new_name} [{file_type}]")
            except Exception as e:
                report.append(f"{file} --> ERROR: {e}")

    # Write analysis file report
    with open(os.path.join(OUTPUT_DIR, "drivefs_analysis_report.txt"), "w") as f:
        f.write("\n".join(report))
    print(f"Analysis complete. {len(report)} files processed.")

    # Metadata (SQLite) export including ISO timestamps
    if METADATA_DB:
        print(f"Parsing metadata database at: {METADATA_DB}")
        dump_items_table_to_csv(METADATA_DB, OUTPUT_DIR)
        print(f"Timestamps for all fields ending in _date are exported as ISO8601 UTC.")

if __name__ == '__main__':
    main()
