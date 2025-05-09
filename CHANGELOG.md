# Changelog

All notable changes to the Google DriveFS Forensic Extractor & Metadata Exporter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-05-09

### Added
- Initial release of the Google DriveFS Forensic Extractor & Metadata Exporter
- Support for recovering files from Google DriveFS content_cache
- File type detection using magic numbers for PDF, Office documents (as ZIP), JPEG, and PNG
- Metadata extraction from SQLite database with timestamp conversion to ISO 8601 UTC
- Comprehensive reporting of recovered files
