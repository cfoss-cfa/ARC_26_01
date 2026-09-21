# A2
## A2a - About group
how much do you agree with the following statement, the number gives your coding level, please provide your total score for your group.
I am confident coding in Python: Our total score is 6
Our focus area is aesthetics and facade. 

##A2b - Identify Claim
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

**BIM purpose:** Analyse
**BIM use case:** Design Review

The process requires information about:
* Exterior façade elements
* Materials
* Surface colours
* Element GlobalIds

The result identifies facade elements as compliant, non-compliant, or missing information.
