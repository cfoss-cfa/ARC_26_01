# A3 – Facade Material and Colour Checker

**Course:** DTU 41934  
**BIM Role:** Facade Designer / Consultant  
**Level:** Beginner  
**Format:** Written tutorial with annotated Python code  
**Tools:** Blender, Bonsai, Python, IfcOpenShell

## 1. Purpose

This tutorial demonstrates how to check facade materials and colours in an IFC model using Python and IfcOpenShell.

The checker is based on our [A2 facade use case](../A2/A2_Use_Case.md) and the DTU Strategic Campus Plan (2022).

The client prefers natural and metallic facade materials such as brick, concrete, wood, stone and metal. White, green and blue exterior colours should be avoided.

## 2. Learning Objectives

After this tutorial, you should be able to:

1. Access an IFC model using Python.
2. Identify potential facade elements.
3. Extract IFC material information.
4. Compare materials and colours with design guidelines.
5. Interpret automated checks and their limitations.

## 3. Requirements

- Blender with Bonsai installed.
- An IFC model loaded in Bonsai.
- Basic knowledge of Blender. No previous Python experience required.

**Tutorial script:** [facade_material_checker.py](facade_material_checker.py)

The script contains explanatory `# NOTE` comments and does not require external CSV files.

## 4. Step-by-Step Tutorial

### Step 1 – Open the IFC Model

Open Blender/Bonsai and load the IFC model.

### Step 2 – Open the Script

Go to **Scripting** in Blender and open `facade_material_checker.py`.

### Step 3 – Run the Checker

Click **Run Script**.

The script accesses the active IFC model:

```python
model = tool.Ifc.get()
```

### Step 4 – Understand the Checks

The script:

1. Selects potential facade elements (`IfcWall`, `IfcWindow`, `IfcPlate`, `IfcMember`, `IfcBeam`, `IfcCovering`).
2. Filters external walls using `Pset_WallCommon.IsExternal`.
3. Extracts IFC material associations.
4. Compares materials with preferred categories.
5. Checks Blender display colours for possible white, green and blue shades.

### Step 5 – Read the Results

Open Blender's system console and find `A3 SUMMARY`.

Example output from our tested IFC model:

| Result | Count |
|---|---:|
| Selected IFC elements | 1,442 |
| Material records | 1,615 |
| Preferred material records | 499 |
| Material records for review | 1,116 |
| Missing material records | 0 |
| Elements with colour warnings | 353 |

**Result interpretation:**

- `PREFERRED`: Recognised preferred material category.
- `REVIEW`: Requires manual assessment.
- `UNKNOWN`: Material information not found.
- `WARNING`: Possible undesirable colour.

These statuses are not final compliance decisions.

## 5. Limitations

- Not every selected element is confirmed to be part of the visible exterior facade.
- Exterior wall materials are identified using investigated material-layer patterns.
- Colour checks use approximate Blender display colours, not verified exterior IFC surface styles.
- Hidden foundation materials may be included.
- The script is model-specific and provides preliminary design guidance only.

## 6. Tutorial Testing and Feedback

**Status: NOT COMPLETED**

The tutorial has not yet been tested by other students.

**Planned:** Ask another student or group to follow the instructions, run the script and provide feedback on clarity and reproducibility.

Feedback and any resulting improvements will be documented here after testing.

## 7. Tutorial Formats

- **Format 1:** This Markdown tutorial.
- **Format 2:** Annotated Python script with step-by-step `# NOTE` explanations.

**Video:** Not planned.

## 8. Future Development (A4)

Possible improvements include more reliable exterior-surface identification, IFC surface-style analysis and structured result export.

## References

- DTU Strategic Campus Plan (2022).
- [IfcOpenShell Documentation](https://docs.ifcopenshell.org/)
- [Bonsai BIM](https://bonsaibim.org/)
- [Project Repository](https://github.com/cfoss-cfa/ARC_26_01)
