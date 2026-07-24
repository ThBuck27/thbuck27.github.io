# Software Design and Engineering

## Weigh to Go

This Android application was originally created for CS 360. The project allows users to manage weight-related data and application settings.

For the software design and engineering enhancement, I refactored the application into a simplified MVVM-style architecture.

The enhanced structure separates responsibilities across:

- Activities for UI, navigation, permissions, and Android-specific behavior
- ViewModels for business logic
- A Repository layer for data access
- The existing DatabaseHelper for database operations

This enhancement improves separation of concerns, maintainability, and overall organization without replacing the existing database implementation.

## Files

- [Enhanced Artifact](TBuck_CS499_Enhancement_One.zip)
- [Enhancement Narrative](Enhancement_One_Narrative.pdf)

[Return to Home](../)
