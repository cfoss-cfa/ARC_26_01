
# A3 – Facade Material and Colour Checker

**Course:** DTU 41934  
**Project Group:** Facade – ARC_26_01  
**Focus Group:** Architecture  
**BIM Role:** Facade Designer / Consultant  
**Level:** Beginner  
**Tools:** Blender, Bonsai, Python, IfcOpenShell

## 1. Learning Need and Focus Group

**Proposed learning need:** How can architects use IFC data and Python to check facade materials and colours against architectural design guidelines?

- **Teaching group:** Facade (ARC_26_01)
- **Focus group:** Architecture
- **Learning need owner:** To be identified
- **Focus group agreement:** Pending

**TODO:** Discuss learning needs with the Architecture Focus Group, agree on the distribution of tutorial topics, identify the learning need owner and confirm the learning objectives.

## 2. Learning Objectives

After completing this tutorial, students should be able to:

1. Access an IFC model using Python and IfcOpenShell.
2. Identify potential facade elements and extract material information.
3. Compare materials and colours with architectural guidelines.
4. Interpret automated checks and their limitations.

## 3. Purpose

This tutorial builds on our [A2 facade use case](../A2/A2_Use_Case.md) and the DTU Strategic Campus Plan (2022).

The client recommends natural and metallic facade materials and prefers natural material colours. White, green and blue exterior shades should be avoided.

Our Python script demonstrates a preliminary automated check of these guidelines.

## 4. Requirements

- Blender with Bonsai installed
- An IFC model loaded in Bonsai
- Basic Blender knowledge; no Python experience required

**Script:** [facade_material_checker.py](facade_material_checker.py)

The script includes explanatory `# NOTE` comments and does not require external CSV files.

## 5. Step-by-Step Tutorial

1. Open Blender/Bonsai and load the IFC model.
2. Go to the **Scripting** workspace.
3. Open `facade_material_checker.py`.
4. Click **Run Script**.
5. Open Blender's system console and find `A3 SUMMARY`.

The script accesses the IFC model using:

    model = tool.Ifc.get()

It then:
- Selects potential facade elements.
- Filters external walls using `Pset_WallCommon.IsExternal`.
- Extracts IFC material information.
- Checks materials against preferred categories.
- Identifies possible white, green and blue colours.

## 6. Tested Results

The script was successfully executed on our IFC model.

| Result | Count |
|---|---:|
| Selected IFC elements | 1,442 |
| Material records | 1,615 |
| Preferred material records | 499 |
| Material records requiring review | 1,116 |
| Missing material records | 0 |
| Elements with colour warnings | 353 |

**Result interpretation:**

- `PREFERRED`: Recognised preferred material category.
- `REVIEW`: Manual assessment required.
- `UNKNOWN`: Material information unavailable.
- `WARNING`: Possible undesirable colour.

These results are preliminary and do not establish full facade compliance.

## 7. Limitations

- Not all selected elements are confirmed to be visible exterior facade elements.
- Exterior wall materials are partly identified using known layer patterns.
- Colour checks use approximate Blender display colours.
- Hidden foundation materials may be included.
- Material names and checking rules are model-specific.

## 8. Tutorial Formats and Peer Review

**Format 1:** This Markdown tutorial.  
**Format 2:** Annotated Python script with `# NOTE` explanations.

**Video:** Not planned.

**Peer-testing:** NOT COMPLETED.

**TODO:**
- Confirm whether these two written formats satisfy the A3 tutorial-format requirements.
- Ask another student or group to test the tutorial.
- Collect feedback and document any improvements.
- Complete the required tutorial presentation and peer-review activities.

## 9. Future Development – A4

Possible improvements include more reliable exterior-surface identification, better IFC colour analysis and structured result export.

## References

- DTU Strategic Campus Plan (2022)
- [A2 – Facade Use Case](../A2/A2_Use_Case.md)
- [IfcOpenShell Documentation](https://docs.ifcopenshell.org/)
- [Bonsai BIM](https://bonsaibim.org/)
