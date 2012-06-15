BOM
===

SF Labs Bill Of Materials Generator

-------------------
This repository proect is intended to act as a high-level Bill Of Materials Generator with real-time component pricing
for EDA projects.  

The first EDA to be integrated will be gEDA project (gschem Schematic Editor).  Custom attributes will need to be placed
at the schematic level for the BOM generator to properly parse all components.

Real-time pricing and supplier stock quantities are provided using the Octopart API.

Output formats will be delimited text file.  This will be customizable for various reports which are required.
Future output formats (i.e. reportlab PDF generation, ODS Libreoffice spreadsheet) are to be included at a later date