Class diagram
=============

The diagram shows the structure of the address book domain: the base field, specialized fields,
contact record, and address book container.

.. mermaid::
  
  classDiagram
  direction TB

  class Field {
    # value
    +\__init__(self, value)
    +validate(value) bool*
    +\__str__(self) str
  }

  class Name 
  class Phone {
    +validate(value) bool
  }
  class Record {
    # Name name
    # list~Phone~ phones
    
    +add_phone(str phone)
    +remove_phone(str phone) bool
    +edit_phone(str phone)
    +find_phone(str phone) Phone
    +\__init__(self, Name name, List~phone~ phones = [])
    +\__str__(self) str
  }
  class AddressBook {
    + Dictionary data
    +add_record(Record record)
    +find_record(str name) Record
    +remove_record(str name) bool
  }

  Field <|-- Name
  Field <|-- Phone

  Record *-- "1" Name : name
  Record *-- "*" Phone : phones

  AddressBook *-- "*" Record : records

  note for Field "Base class for entry fields."
  note for Name "Stores the contact name. <br/> Required field."
  note for Phone "Stores the phone number. <br/> Validates format (10 digits)."
  note for Record "Stores contact information, including name and a list of phone numbers. <br/> if name is missing raise an error. <br/> Can add, remove, edit, and find phone numbers. <br/> If the phone number fails validation error should be raised"
  note for AddressBook "Stores entries and manages them."

Relationships
-------------

* **Field** is the base class; **Name** and **Phone** are subclasses.
* **Record** has composition with **Name** (one required name) and **Phone** (a list of numbers).
* **AddressBook** has composition with **Record** (a collection of contact entries).
