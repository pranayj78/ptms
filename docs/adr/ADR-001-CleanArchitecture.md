Why Clean Architecture?

Decision:

Use Clean Architecture.

Reason:

Tax rules change.

Excel changes.

Broker formats change.

Business logic should never change because the UI changed.        

           PTMS Core

         Tax Engine
         FIFO Engine
         Validation Engine
         FX Engine
         Schedule FA Engine

                ↑
                │

     Domain Models (Pydantic)

                ↑
                │

        Repository Interfaces

        ↑                   ↑

 SQLite Repository     Future Cloud Repository

                ↓

      Presentation Adapters

 Excel   CLI   PDF   REST API   Web UI

## Canonical Representation Principle

Every Value Object follows these rules:

- One canonical internal representation.
- One canonical string representation (`__str__`).
    __str__() returns the canonical, locale-independent representation of the value object. This representation is stable and intended for developers, logging, diagnostics, and system-to-system communication.

- Zero or more parsing formats.
- Presentation-specific formatting belongs outside the domain unless it represents a distinct business concept.

Presentation Representation

User-facing formatting (for example, "AY 2026-27") is outside the responsibility of the domain model and should be provided by the presentation layer or dedicated formatting components.


