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
- Zero or more parsing formats.
- Presentation-specific formatting belongs outside the domain unless it represents a distinct business concept.


