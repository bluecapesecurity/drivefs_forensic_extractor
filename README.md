# Google DriveFS Forensic Extractor & Metadata Exporter

[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)](https://github.com/bluecapesecurity/drivefs_forensic_extractor/releases/tag/v1.0.0)
[![Blue Cape Security, LLC](https://img.shields.io/badge/Blue%20Cape%20Security-LLC-blue)](https://bluecapesecurity.com)

## OVERVIEW

This tool assists digital forensic practitioners in recovering evidence from Google Drive File Stream (DriveFS) client artifacts on Windows systems. It recovers locally-cached user files from the 'content_cache' folder and optionally parses metadata from the related 'metadata_sqlite_db' database (items table) into CSV format. Timestamps in the CSV are automatically converted to ISO 8601 UTC for easy timeline analysis.

## KEY FEATURES

- Recovers tangible files from the 'content_cache' by identifying known file types through magic number (file signature) detection.
- Optionally exports the full 'items' table (with readable timestamps) from the Google DriveFS metadata database to CSV.
- Supported file types (as of release):
  * PDF (.pdf)
  * Office XML-format docs (.docx, .xlsx, .pptx as .zip)
  * JPEG Images (.jpg)
  * PNG Images (.png)
- User-friendly reporting: both a file carving report and an exported CSV (if metadata is extracted).

## REQUIREMENTS

- Python 3.x
- No special dependencies (uses only standard Python libraries)
- Windows system with Google DriveFS client artifacts

## USAGE

1. Open an administrative command prompt or terminal with access to Python 3.x.
2. Run the script as follows:

```bash
python drivefs_recover.py -s <path_to_content_cache> -d <output_dir> [ -m <path_to_metadata_sqlite_db> ]
```

For example:
```bash
python drivefs_recover.py \
  -s "C:\Users\<user>\AppData\Local\Google\DriveFS\<UserID>\content_cache" \
  -d C:\ForensicOutput \
  -m "C:\Users\<user>\AppData\Local\Google\DriveFS\<UserID>\metadata_sqlite_db"
```

- `-s` / `--source`: Path to the content_cache directory (REQUIRED)
- `-d` / `--dest`: Path to the destination/output directory (REQUIRED)
- `-m` / `--metadata_file`: Path to the metadata_sqlite_db SQLite file (OPTIONAL)

3. Deliverables written to the output directory are:
   - `drivefs_analysis_report.txt`: Summary of recovered files and status.
   - `drivefs_items_table.csv`: CSV export of metadata (if database specified), with all *_date fields in ISO 8601 UTC.

## DISCLAIMER

This tool is provided "AS IS" and WITHOUT WARRANTY of any kind. No liability is assumed by Blue Cape Security, LLC or its contributors for any direct, indirect, incidental, or consequential damages arising from its use. Use is at your own risk and intended for forensic investigation, incident response, and educational purposes only.

## ATTRIBUTION

Blue Cape Security, LLC  
https://bluecapesecurity.com

Questions or suggestions for improvement? Contact our team or submit a pull request/contribution via our official support portal.
