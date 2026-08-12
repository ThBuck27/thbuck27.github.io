---
layout: default
title: Databases Enhancement
---

# Enhancement Three: Databases

## Grazioso Salvare Animal Shelter Dashboard

This artifact was originally developed in CS 340 and uses Python, MongoDB, and Dash to support animal-shelter data analysis and rescue filtering.

For the database enhancement, I improved the artifact by adding configurable MongoDB connection handling, removing hard-coded credentials, validating query fields, operators, and value types, protecting update and delete operations from empty filters, adding the `rescue_search_idx` compound index, and creating automated connection and query-validation tests.

A representative local MongoDB dataset was also created so the enhanced dashboard could be tested when the original course database was unavailable.

## Project Files

- [Original Artifact](Original/)
- [Enhanced Artifact](Enhanced/)
- [Enhancement Narrative](Enhancement_Three_Narrative.pdf)

## Enhancement Highlights

- Configurable MongoDB connection
- Removal of hard-coded credentials
- Query validation
- Empty update/delete protection
- Compound MongoDB indexing
- Automated connection and validation testing
- Updated Dash and Jupyter compatibility
- Representative local test database

## Course Outcome Alignment

This enhancement demonstrates practical database design, testing, performance optimization, and security-focused development. It particularly supports course outcomes related to professional-quality computing solutions, industry-relevant tools and techniques, and developing a security mindset.
