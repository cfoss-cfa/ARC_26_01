# A2
## A2a - About group
how much do you agree with the following statement, the number gives your coding level, please provide your total score for your group.
I am confident coding in Python: Our total score is 6
Our focus area is aesthetics and facade. 

## A2b - Identify Claim
We have chosen to focus on Building 2601 – B308.

In Section 6.2 Exterior walls of the client report 26-01-A. The report states that facade materials should align with the aesthetics of the DTU campus.

The suggested façade materials include metallic materials and natural materials such as: stone, brick, concrete, wood, other bio-based materials. 

The report furthermore states that the colours of the exterior facade should correspond to the natural colours of the chosen materials, while white, green and blue shades should be avoided.

## A2b - Identify Claim
**Justification** 
We selected this claim because our focus area is Facade and Aesthetics for the Architectural dicicpline. 

Aesthetic quality is normally evaluated subjectively. However, the report translates part of the desired architectural expression into explicit requirements regarding facade materials and colours.

This makes it possible to investigate whether part of the architectural intent can be checked automatically using information contained in an IFC model.

Rather than attempting to determine whether a facade is generally “beautiful”, the use case therefore focuses on checking specific and measurable aspects of the intended facade expression.

## A2c - Use Case 
**Claim**
Will be checked through an Automated Facade Design Review.

The IFC model is analysed to identify exterior facade elements and retrieve their materials and surface colours. These are compared with the facade requirements defined in the client report.

The check should be performed during the design phase, after facade materials have been assigned but before the design is finalised.

* **BIM purpose:** Analyse
* **BIM use case:** Design Review

The process requires information about:
* Exterior façade elements
* Materials
* Surface colours
* Element GlobalIds

The result identifies facade elements as compliant, non-compliant, or missing information.

This is shown in the Flow 'A2c_USe_Case'


## A2d - Tool Idea
The scope of our tool is the automated analysis of the IFC model.

The tool will:
- Find exterior facade elements.
- Read their materials and surface colours.
- Check if the required information is available.
- Compare the information with the facade requirements.
- Identify missing information.

The scope is highlighted in the flow A2d_Scoped_Use_Case. 


## A2e: Tool Idea

Our idea is to develop an OpenBIM tool in Python using IfcOpenShell for automated facade design review.

The tool analyses an IFC model and identifies exterior facade elements. It retrieves their materials and surface colours and compares this information with predefined facade requirements. Each element is then classified as compliant, non-compliant, or missing required information. The GlobalId is used to identify the relevant elements in the IFC model.

### Business and societal value

The tool can reduce the time spent on manual facade reviews and help identify errors earlier in the design process. This can improve quality assurance and reduce the risk of costly changes later in the project.

The tool also provides a more consistent and transparent way of checking whether a facade design meets the specified requirements.

### BPMN diagram

The BPMN diagram A2e_Tool_Idea summarises the workflow of the proposed tool.


## A2f: Information Requirements


## A2f: Information Requirements

For our automated facade compliance tool, we need to extract information about the different elements that contribute to the external appearance of the facade.

The tool needs to identify the relevant facade elements and extract their IFC class, predefined type, material, surface colour and GlobalId. For walls, the `IsExternal` property can also be used to distinguish exterior walls from interior walls.

### Required information

| Information | Where in IFC? | Available in model? | Purpose |
|---|---|---|---|
| IFC element type | IFC class, e.g. `IfcWall`, `IfcWindow`, `IfcPlate`, `IfcMember`, `IfcBeam`, `IfcCovering` | Yes | Identifies what type of facade element is being checked |
| Predefined type | `PredefinedType` attribute | Yes | Helps distinguish specific element functions, e.g. `CURTAIN_PANEL`, `MULLION` and `MOLDING` |
| Exterior status | `Pset_WallCommon.IsExternal` where applicable | Yes | Helps distinguish exterior walls from interior walls |
| Material | `IfcMaterial`, `IfcMaterialLayerSet`, `IfcMaterialConstituentSet` or material profiles | Yes | Used to compare the element material with the facade requirements |
| Surface colour | `IfcSurfaceStyle` | Yes | Used to compare the visible colour with the facade requirements |
| GlobalId | `GlobalId` attribute | Yes | Used to identify the specific element in the results |

### Investigation of the IFC model

We inspected the IFC model in Bonsai and found that the facade consists of several different IFC element types. Therefore, the facade cannot be identified only by searching for `IfcWall`.

The following relevant facade elements were identified:

| Facade element | IFC type | Example material |
|---|---|---|
| Exterior wall | `IfcWall` | `DTU_Masonry_Brick_Natural_Yellow_Mat` |
| Window | `IfcWindow` | `DTU_Wood_Frame_Exterior_Painted_Black_SemiGlossy` and `DTU_Glass_Double_Clear_Glossy` |
| Curtain panel | `IfcPlate` with `PredefinedType = CURTAIN_PANEL` | `Glass 22mm (Double)` |
| Mullion/frame | `IfcMember` with `PredefinedType = MULLION` | `DTU_Wood_Frame_Exterior_Painted_Black_Mat` |
| Visible concrete beam | `IfcBeam` | Painted/coloured concrete |
| Roof edge/fascia | `IfcCovering` with `PredefinedType = MOLDING` | `DTU_Metal_Zinc_Natural_SemiMat` |

The roof itself is outside the scope of the tool. However, the visible roof edge/fascia is included because it contributes to the external appearance of the facade.

### Examples of information found in the model

For an exterior wall, we found:

- `Pset_WallCommon.IsExternal = True`
- Material: `DTU_Masonry_Brick_Natural_Yellow_Mat`
- Surface colour RGB: `0.716, 0.697, 0.622`
- Surface colour Hex: `#B6B29F`
- A GlobalId is available for the element.

For window and glazed facade elements, we found materials for both glass and frames. This shows that one facade element can contain multiple materials that may need to be checked separately.

Examples include:

- Glass: `DTU_Glass_Double_Clear_Glossy`
- Glass colour: RGB `0.857, 0.898, 1.000` / `#DBE5FF`
- Exterior wood frame: `DTU_Wood_Frame_Exterior_Painted_Black_Mat`
- Frame colour: RGB `0.522, 0.522, 0.522` / `#858585`

For the visible roof edge/fascia, we found:

- IFC type: `IfcCovering`
- PredefinedType: `MOLDING`
- Material: `DTU_Metal_Zinc_Natural_SemiMat`
- Surface colour RGB: `0.716, 0.716, 0.716`
- Surface colour Hex: `#B6B6B6`

The investigation also showed that not every `IfcWall` should automatically be considered part of the facade. For example, the model contains a strip foundation represented as an `IfcWall`. The tool therefore needs additional criteria to determine whether an element is relevant to the facade.

### IfcOpenShell

We plan to use IfcOpenShell in Python to extract and process this information from the IFC model.

We need to learn how to:

- Identify the relevant exterior facade elements across different IFC classes.
- Read `Pset_WallCommon.IsExternal` where applicable.
- Read `PredefinedType` and other element attributes.
- Extract materials from different IFC material structures.
- Handle elements containing more than one material.
- Find the `IfcSurfaceStyle` associated with a material or representation.
- Extract RGB surface colour values.
- Read the `GlobalId` of each checked element.
- Compare the extracted information with predefined facade requirements.
- Report elements as compliant, non-compliant or missing information.
