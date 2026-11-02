
# ============================================================
# A3 - FACADE MATERIAL AND COLOUR CHECKER
# DTU 41934 - Facade Design Review
# Blender / Bonsai / IfcOpenShell
# ============================================================

# NOTE:
# This tutorial demonstrates how Python and IfcOpenShell
# can support a facade design review using an IFC model.
#
# The client guidelines recommend natural and metallic
# materials, including brick, stone, concrete, wood,
# and other bio-based materials.
#
# White, green and blue exterior colours should be avoided.
# Natural material colours are preferred.
#
# IMPORTANT:
# This is a preliminary design review, not certification.
# Material and colour results must be interpreted carefully.


# ============================================================
# STEP 1 - IMPORT LIBRARIES
# ============================================================

import colorsys
from collections import Counter

import bonsai.tool as tool
import ifcopenshell.util.element


# NOTE:
# Bonsai provides access to the IFC model loaded in Blender.
# IfcOpenShell reads IFC properties and material associations.
# colorsys is used for approximate colour classification.


# ============================================================
# STEP 2 - LOAD THE IFC MODEL
# ============================================================

model = tool.Ifc.get()

if model is None:
    raise RuntimeError(
        "No IFC model loaded. Open the IFC file in Bonsai first."
    )

print("=== A3 FACADE MATERIAL CHECK ===")
print("IFC schema:", model.schema)


# ============================================================
# STEP 3 - DEFINE CLIENT REQUIREMENTS
# ============================================================

# NOTE:
# Known IFC material names are based on the A2 investigation.
# They are used for exact matching.
#
# NOTE:
# The status PREFERRED means the material belongs to a
# category recommended by the Client Report.
# It does not mean full facade compliance.

KNOWN_MATERIALS = {
    "DTU_Masonry_Brick_Natural_Yellow_Mat": "brick",
    "DTU_Concrete_Generic_Natural_Mat": "concrete",
    "DTU_Wood_Frame_Exterior_Painted_Black_Mat": "wood",
    "DTU_Wood_Frame_Exterior_Painted_Black_SemiGlossy": "wood",
    "DTU_Metal_Zinc_Natural_SemiMat": "metal",
    "DTU_Glass_Double_Clear_Glossy": "glass",
    "Glass 22mm (Double)": "glass"
}

PREFERRED_CATEGORIES = {
    "brick",
    "stone",
    "slate",
    "concrete",
    "wood",
    "timber",
    "metal",
    "steel",
    "zinc",
    "aluminium",
    "ceramic",
    "bio-based"
}

# NOTE:
# Glass is not automatically approved because the
# material recommendations primarily concern facade
# cladding and architectural appearance.


# ============================================================
# STEP 4 - DEFINE FACADE ELEMENT TYPES
# ============================================================

FACADE_TYPES = [
    "IfcWall",
    "IfcWindow",
    "IfcPlate",
    "IfcMember",
    "IfcBeam",
    "IfcCovering"
]

# NOTE:
# These IFC classes were identified in the A2 use case.
# They represent candidate facade elements.
# IFC class alone cannot prove external location.


# ============================================================
# STEP 5 - READ IFC PROPERTIES
# ============================================================

def get_predefined_type(element):

    # NOTE: Used to distinguish curtain panels,
    # mullions and roof-edge coverings.

    return str(
        getattr(element, "PredefinedType", None) or ""
    ).upper()


def get_external_status(element):

    # NOTE: External wall status is read from
    # Pset_WallCommon.IsExternal.

    psets = ifcopenshell.util.element.get_psets(element)

    return psets.get(
        "Pset_WallCommon", {}
    ).get("IsExternal")


# ============================================================
# STEP 6 - FILTER FACADE ELEMENTS
# ============================================================

def is_relevant(element):

    ifc_class = element.is_a()
    predefined = get_predefined_type(element)

    if ifc_class == "IfcWall":

        # NOTE:
        # We investigated all 149 walls:
        # 38 external, 111 internal, 0 missing.
        #
        # Only walls marked IsExternal = True are included.

        return get_external_status(element) is True

    if ifc_class == "IfcPlate":
        return predefined == "CURTAIN_PANEL"

    if ifc_class == "IfcMember":
        return predefined == "MULLION"

    if ifc_class == "IfcCovering":
        return predefined == "MOLDING"

    if ifc_class in ("IfcWindow", "IfcBeam"):

        # NOTE:
        # Windows and beams are included as candidates.
        # Their external location still needs verification.

        return True

    return False


# ============================================================
# STEP 7 - EXTRACT MATERIALS
# ============================================================

def get_material_names(element):

    # NOTE:
    # IFC elements can have different material structures:
    #
    # IfcMaterial
    # IfcMaterialLayerSet
    # IfcMaterialConstituentSet
    # IfcMaterialProfileSet
    # IfcMaterialList
    #
    # should_skip_usage=True unwraps material usage objects
    # such as IfcMaterialProfileSetUsage.

    material = ifcopenshell.util.element.get_material(
        element,
        should_skip_usage=True
    )

    if material is None:
        return []

    names = []

    if material.is_a("IfcMaterial"):
        names.append(material.Name)

    elif material.is_a("IfcMaterialLayerSet"):
        for layer in material.MaterialLayers:
            if layer.Material:
                names.append(layer.Material.Name)

    elif material.is_a("IfcMaterialConstituentSet"):
        for constituent in material.MaterialConstituents or []:
            if constituent.Material:
                names.append(constituent.Material.Name)

    elif material.is_a("IfcMaterialProfileSet"):
        for profile in material.MaterialProfiles or []:
            if profile.Material:
                names.append(profile.Material.Name)

    elif material.is_a("IfcMaterialList"):
        for item in material.Materials:
            names.append(item.Name)

    return list(dict.fromkeys(
        name for name in names if name
    ))


# ============================================================
# STEP 8 - IDENTIFY EXTERIOR WALL MATERIALS
# ============================================================

def get_exterior_wall_materials(element):

    # NOTE:
    # Two wall constructions were visually investigated:
    #
    # Brick facade:
    # 110 - DTU_Masonry_Brick_Natural_Yellow_Mat
    # 100 - DTU_Default_Wall_Interior_Mat
    #
    # Concrete base:
    # 110 - DTU_Concrete_Generic_Natural_Mat
    # 90  - DTU_Default_Wall_Interior_Mat
    #
    # NOTE:
    # Brick and concrete were visually confirmed as
    # exterior materials on the inspected examples.
    #
    # NOTE:
    # We recognise these exact two-layer combinations.
    # Other combinations are marked for manual review.
    #
    # IMPORTANT:
    # Matching layer names does not independently prove
    # the exterior orientation of every wall.

    material = ifcopenshell.util.element.get_material(
        element,
        should_skip_usage=True
    )

    if material is None:
        return [], "UNKNOWN"

    if not material.is_a("IfcMaterialLayerSet"):
        return get_material_names(element), "REVIEW"

    layers = list(material.MaterialLayers)

    names = [
        layer.Material.Name if layer.Material else ""
        for layer in layers
    ]

    known_exterior = {
        "DTU_Masonry_Brick_Natural_Yellow_Mat",
        "DTU_Concrete_Generic_Natural_Mat"
    }

    interior_name = "DTU_Default_Wall_Interior_Mat"

    if (
        len(names) == 2
        and names[0] in known_exterior
        and names[1] == interior_name
    ):
        return [names[0]], "ASSUMED_EXTERIOR"

    # NOTE:
    # Unknown wall constructions are not automatically
    # assigned an exterior layer.

    return get_material_names(element), "REVIEW"


# ============================================================
# STEP 9 - CHECK MATERIAL REQUIREMENTS
# ============================================================

def check_material(material_name):

    known_lookup = {
        name.casefold(): category
        for name, category in KNOWN_MATERIALS.items()
    }

    category = known_lookup.get(material_name.casefold())

    if category:

        if category in PREFERRED_CATEGORIES:
            return "PREFERRED", category

        return "REVIEW", category

    # NOTE:
    # Unknown materials may be new facade materials.
    # Keyword matching suggests a category, but does
    # not automatically approve the material.

    name = material_name.casefold()

    for keyword in sorted(
        PREFERRED_CATEGORIES,
        key=len,
        reverse=True
    ):
        if keyword in name:
            return "REVIEW", keyword

    return "REVIEW", "unknown"


# ============================================================
# STEP 10 - EXTRACT BLENDER DISPLAY COLOURS
# ============================================================

def get_surface_colours(element):

    # NOTE:
    # The code reads Blender material display colours.
    # These may differ from the original IFC surface styles.
    #
    # NOTE:
    # Material slots may contain colours from surfaces
    # that are not visible on the exterior facade.

    obj = tool.Ifc.get_object(element)

    if obj is None or obj.data is None:
        return []

    if not hasattr(obj.data, "materials"):
        return []

    colours = []

    for material in obj.data.materials:

        if material is None:
            continue

        colours.append(
            tuple(material.diffuse_color[:3])
        )

    return list(dict.fromkeys(colours))


# ============================================================
# STEP 11 - CHECK COLOURS
# ============================================================

def rgb_to_hex(rgb):

    return "#" + "".join(
        f"{max(0, min(255, round(c * 255))):02X}"
        for c in rgb
    )


def check_colour(rgb):

    # NOTE:
    # HSV is used for approximate colour classification.
    # The thresholds are illustrative and should be
    # validated against the actual facade materials.

    h, s, v = colorsys.rgb_to_hsv(*rgb)

    if v >= 0.90 and s <= 0.12:
        return "WARNING", "white"

    if 0.22 <= h <= 0.48 and s >= 0.25:
        return "WARNING", "green"

    if 0.52 <= h <= 0.75 and s >= 0.25:
        return "WARNING", "blue"

    # NOTE:
    # A colour that is not white, green or blue
    # is not automatically a natural material colour.

    return "REVIEW", "other"


# ============================================================
# STEP 12 - RUN MATERIAL AND COLOUR CHECK
# ============================================================

results = []
element_counts = Counter()

print("\n=== CHECKING FACADE ELEMENTS ===")

for ifc_class in FACADE_TYPES:

    for element in model.by_type(ifc_class):

        if not is_relevant(element):
            continue

        element_counts[ifc_class] += 1

        if ifc_class == "IfcWall":

            materials, exterior_status = (
                get_exterior_wall_materials(element)
            )

        else:
            materials = get_material_names(element)
            exterior_status = "NOT_VERIFIED"

        if not materials:
            materials = ["UNKNOWN"]

        colours = get_surface_colours(element)

        if not colours:
            colour_results = ["UNKNOWN"]
        else:
            colour_results = []

            for rgb in colours:
                status, family = check_colour(rgb)

                colour_results.append(
                    f"{rgb_to_hex(rgb)}: {status} ({family})"
                )

        for material_name in materials:

            if material_name == "UNKNOWN":
                material_status = "UNKNOWN"
                category = "unknown"
            else:
                material_status, category = (
                    check_material(material_name)
                )

            results.append({
                "GlobalId": element.GlobalId,
                "IFC_Class": ifc_class,
                "Material": material_name,
                "Category": category,
                "Material_Status": material_status,
                "Exterior_Status": exterior_status,
                "Colour_Result": " | ".join(colour_results)
            })


# ============================================================
# STEP 13 - DISPLAY RESULTS
# ============================================================

print("\n=== SELECTED ELEMENTS ===")

for ifc_class in FACADE_TYPES:
    print(f"{ifc_class}: {element_counts[ifc_class]}")

print("\n=== FIRST 30 MATERIAL RECORDS ===")

for result in results[:30]:

    print(
        f"{result['IFC_Class']} | "
        f"{result['Material']} | "
        f"{result['Material_Status']} | "
        f"{result['Exterior_Status']} | "
        f"{result['Colour_Result']}"
    )


# ============================================================
# STEP 14 - DISPLAY SUMMARY
# ============================================================

material_counts = Counter(
    row["Material_Status"]
    for row in results
)

colour_warning_elements = {
    row["GlobalId"]
    for row in results
    if "WARNING" in row["Colour_Result"]
}

print("\n=== A3 SUMMARY ===")

print("Selected IFC elements:", sum(element_counts.values()))
print("Material records:", len(results))
print("Preferred category:", material_counts["PREFERRED"])
print("Material review:", material_counts["REVIEW"])
print("Missing materials:", material_counts["UNKNOWN"])

print(
    "Elements with colour warnings:",
    len(colour_warning_elements)
)

print("\nA3 FACADE CHECK COMPLETE")


# ============================================================
# STEP 15 - INTERPRETATION AND LIMITATIONS
# ============================================================

# NOTE:
# PREFERRED means the material belongs to a category
# recommended by the Client Report.
#
# REVIEW means the material requires manual assessment.
#
# UNKNOWN means no IFC material association was found.
#
# ASSUMED_EXTERIOR means the wall matches one of the
# two material-layer patterns investigated in A2/A3.
# It is not proof of exterior orientation for every wall.
#
# NOT_VERIFIED means the external location or visible
# material has not been independently confirmed.
#
# Colour warnings are preliminary because the script
# uses Blender display colours rather than verified
# exterior IfcSurfaceStyle data.
#
# The script supports architectural design review,
# but it cannot replace professional judgement.
