# README A4

**DTU - Advanced BIM (41934)**  
**Group: ARC_26_01 - Architecture - s234281 & s234297**

## Purpose
This Python tool identifies potential material and colour issues in facades using IFC parameters data. It supports the design review process by reducing manual checking and flagging elements that may need further attention.

## Design Stage and Application

**Advanced Building Design Level:** C - Design Development (proposed).

**When to use:** After facade materials and colours have been assigned in the IFC model, and before the design is approved.

**Disciplines involved:** Architecture

The tool supports early identification of potential facade design issues, allowing the design team to review flagged elements before finalising the facade. It can also be used as a final design-stage check, to quickly get an overview of the status. 

## How It Works
- The tool runs in Blender with Bonsai and analyses IFC elements, including walls, windows, plates, members, beams and coverings.
- It checks available material and colour information, identifies potential issues and flags elements that require manual review.
- The checks use preliminary material and colour criteria and do not replace a full assessment against DTU Campus design guidelines.

## How to Run
1. Open the IFC model in Blender using Bonsai.
2. Open `main.py` in Blender's Scripting workspace.
3. Click Run Script.
4. Find the generated reports in your computer's Downloads folder.

## Output
The tool automatically generates three files:
- Excel (.xlsx): Results organised into *Review Required* and *All Elements*.
- CSV (.csv): Results for all checked elements.
- JSON (.json): Structured results for further use.

The tool also displays progress and a summary of the results in Blender's system console, including: 

- Number of checked elements
- Classifications of elements
- Number requiring manual review
- The saved report locations
- Execution time of the tool

## IFC Requirements
The tool uses IFC material assignments, available surface colours and exterior classification information.

The IDS file describes the expected IFC information requirements and can be validated independently.

## Limitations
The results depend on the quality and completeness of the IFC model. Some surface colours or materials may not be available, and uncertain exterior classifications will result in the need for manuel cheking. 

The tool is intended as a screening aid, not a final compliance assessment.
