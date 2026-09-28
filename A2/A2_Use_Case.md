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

For the automated facade compliance tool, we need to extract information about the exterior facade elements, their materials, surface colours, and GlobalIds from the IFC model.

### Required information

| Information | Location in IFC | Available in model? | Use in the tool |
|---|---|---|---|
| Exterior status | `Pset_WallCommon.IsExternal` | Yes | Used to identify exterior wall elements. |
| Material | `IfcMaterial` / `IfcMaterialLayerSet` | Yes | Used to check the facade material against the requirements. |
| Surface colour | `IfcSurfaceStyle` | Yes | Used to check the facade colour against the requirements. |
| GlobalId | IFC element attribute `GlobalId` | Yes | Used to identify and report each checked element. |

### Findings in the IFC model

We inspected an exterior wall in the IFC model using Bonsai. The wall has `IsExternal = True` in `Pset_WallCommon`.

The wall uses an `IfcMaterialLayerSet`, which includes the exterior material:

`DTU_Masonry_Brick_Natural_Yellow_Mat`

The corresponding `IfcSurfaceStyle` contains surface colour information. For this material, the displayed colour is:

- RGB: `0.716, 0.697, 0.622`
- Hex: `#B6B29F`

The wall also contains a `GlobalId`, which can be used to identify the element in the results.

### IfcOpenShell

We will use IfcOpenShell in Python to open the IFC model and extract the required information. We need to learn how to:

- Find exterior facade elements using `IsExternal`.
- Access material associations and material layers.
- Access `IfcSurfaceStyle` and its colour information.
- Read the `GlobalId` of each element.
- Compare the extracted information with the predefined facade requirements.

This information will allow the tool to classify facade elements as compliant, non-compliant, or missing required information.
