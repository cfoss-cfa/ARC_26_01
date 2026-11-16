"""A4 Facade Material and Colour Checker - Blender/Bonsai.

Provisional screening only; not formal DTU Campus compliance.
Run from Blender's Scripting workspace with an IFC project loaded in Bonsai.
"""
import bpy
import colorsys
import csv
import json
import os
import re
import time
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

import ifcopenshell.util.element as ifc_element

CLASSES = ("IfcWall", "IfcWindow", "IfcPlate", "IfcMember", "IfcBeam", "IfcCovering")
MATERIALS = {
    "BRICK": ("brick", "masonry", "tegl", "mursten"),
    "CONCRETE": ("concrete", "beton"),
    "WOOD": ("wood", "timber", "trae"),
    "STONE": ("stone", "slate", "skifer"),
    "ZINC": ("zinc", "zink"),
    "ALUMINIUM": ("aluminium", "aluminum"),
    "STEEL": ("steel", "staal"),
    "GLASS": ("glass", "glas", "glazing"),
}
PREFERRED = set(MATERIALS)
HEADERS = [
    "GlobalId", "IFC_Class", "Element_Name", "Exterior_Status", "Exterior_Evidence",
    "Material_Names", "Material_Categories", "Material_Status", "Colour_RGB",
    "Colour_Labels", "Colour_Source", "Colour_Status", "Colour_Data_Complete",
    "Overall_Status", "Manual_Review_Required", "Reason",
]


def get_model():
    try:
        import bonsai.tool as tool
        model = tool.Ifc.get()
        if model is not None:
            return model
    except ImportError:
        pass
    try:
        from blenderbim.bim.ifc import IfcStore
        model = IfcStore.get_file()
        if model is not None:
            return model
    except ImportError:
        pass
    raise RuntimeError("No active IFC model. Open the IFC project through Bonsai first.")


def blender_object(entity):
    try:
        import bonsai.tool as tool
        return tool.Ifc.get_object(entity)
    except (ImportError, AttributeError):
        return None


def exterior_direct(entity):
    try:
        psets = ifc_element.get_psets(entity)
        name = "Pset_" + entity.is_a()[3:] + "Common"
        value = psets.get(name, {}).get("IsExternal")
        if value is True:
            return "EXTERIOR", name + ".IsExternal=True"
        if value is False:
            return "NOT EXTERIOR", name + ".IsExternal=False"
    except Exception:
        pass
    return "UNCERTAIN", "No explicit IsExternal property"


def exterior(entity):
    status, evidence = exterior_direct(entity)
    if status != "UNCERTAIN" or not entity.is_a("IfcWindow"):
        return status, evidence
    try:
        for fill in entity.FillsVoids or []:
            for void in fill.RelatingOpeningElement.VoidsElements or []:
                host = void.RelatingBuildingElement
                host_status, _ = exterior_direct(host)
                if host_status != "UNCERTAIN":
                    return host_status, "Inferred from host " + host.GlobalId
    except Exception:
        pass
    return status, evidence


def material_entities(entity):
    try:
        m = ifc_element.get_material(entity, should_skip_usage=True)
        if m is None:
            return [], False
        if m.is_a("IfcMaterial"):
            return [m], False
        kinds = {
            "IfcMaterialList": ("Materials", None),
            "IfcMaterialLayerSet": ("MaterialLayers", "Material"),
            "IfcMaterialProfileSet": ("MaterialProfiles", "Material"),
            "IfcMaterialConstituentSet": ("MaterialConstituents", "Material"),
        }
        if m.is_a() not in kinds:
            return [], True
        attribute, inner = kinds[m.is_a()]
        items = getattr(m, attribute, ()) or ()
        return [getattr(item, inner, None) if inner else item for item in items
                if (getattr(item, inner, None) if inner else item) is not None], False
    except Exception:
        return [], True


def normalize(value):
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(value))
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def check_materials(entity):
    mats, incomplete = material_entities(entity)
    names = list(dict.fromkeys((m.Name or "").strip() for m in mats if (m.Name or "").strip()))
    if len(names) < len(mats):
        incomplete = True
    categories = []
    for name in names:
        normalized = " " + normalize(name) + " "
        matches = [category for category, words in MATERIALS.items()
                   if any(" " + normalize(word) + " " in normalized for word in words)]
        categories.append(matches[0] if len(matches) == 1 else
                          "AMBIGUOUS" if matches else "UNRECOGNISED")
    status = ("UNKNOWN" if incomplete or not names else
              "PREFERRED" if all(c in PREFERRED for c in categories) else "REVIEW")
    return " | ".join(names), " | ".join(categories), status, mats


def unique_rgb(values):
    return list(dict.fromkeys(tuple(round(float(x), 4) for x in rgb) for rgb in values))


def ifc_colours(entity, mats):
    colours, issues, visited, styled_seen = [], set(), set(), set()

    def style(s):
        try:
            if s.id() in styled_seen:
                return
            styled_seen.add(s.id())
            if s.is_a("IfcPresentationStyleAssignment"):
                for nested in s.Styles or ():
                    style(nested)
            elif s.is_a("IfcSurfaceStyle"):
                found = False
                for child in s.Styles or ():
                    if child.is_a("IfcSurfaceStyleShading"):
                        c = child.SurfaceColour
                        colours.append((c.Red, c.Green, c.Blue))
                        found = True
                    if child.is_a("IfcSurfaceStyleWithTextures"):
                        issues.add("IFC texture not evaluated")
                if not found:
                    issues.add("Surface style without readable RGB")
        except Exception:
            issues.add("Unreadable IFC style")

    def walk(item, depth=0):
        if item is None:
            return
        if depth > 25:
            issues.add("Representation nesting limit")
            return
        try:
            if item.id() in visited:
                return
            visited.add(item.id())
            for assigned in getattr(item, "StyledByItem", ()) or ():
                for s in assigned.Styles or ():
                    style(s)
            if item.is_a("IfcMappedItem"):
                for child in item.MappingSource.MappedRepresentation.Items or ():
                    walk(child, depth + 1)
            if item.is_a("IfcBooleanResult"):
                walk(item.FirstOperand, depth + 1)
                walk(item.SecondOperand, depth + 1)
            for child in getattr(item, "Items", ()) or ():
                walk(child, depth + 1)
        except Exception:
            issues.add("Unreadable IFC representation")

    try:
        if entity.Representation:
            for representation in entity.Representation.Representations or ():
                for item in representation.Items or ():
                    walk(item)
    except Exception:
        issues.add("Representation read failed")
    for mat in mats:
        try:
            for definition in getattr(mat, "HasRepresentation", ()) or ():
                for rep in definition.Representations or ():
                    for item in rep.Items or ():
                        if item.is_a("IfcStyledItem"):
                            for s in item.Styles or ():
                                style(s)
        except Exception:
            issues.add("Material style unreadable")
    return unique_rgb(colours), issues


def blender_colours(entity):
    obj = blender_object(entity)
    if obj is None:
        return [], {"No Blender object linked"}
    colours, issues = [], set()
    for slot in obj.material_slots:
        mat = slot.material
        if mat is None:
            issues.add("Empty Blender material slot")
            continue
        rgb, linked = None, False
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    socket = node.inputs.get("Base Color")
                    if socket:
                        linked = socket.is_linked
                        if not linked:
                            rgb = tuple(socket.default_value[:3])
                    break
        if linked:
            issues.add("Blender texture/linked shader not evaluated")
            continue
        if rgb is None:
            rgb = tuple(mat.diffuse_color[:3])
            issues.add("Blender diffuse colour approximation")
        colours.append(rgb)
    return unique_rgb(colours), issues


def get_colours(entity, mats):
    colours, issues = ifc_colours(entity, mats)
    if colours:
        source = "IFC_SURFACE_STYLE"
    else:
        colours, fallback_issues = blender_colours(entity)
        issues |= fallback_issues
        source = "BLENDER_MATERIAL" if colours else "NOT_AVAILABLE"
    blockers = ("texture", "unreadable", "nesting", "empty", "failed", "without readable")
    completeness = ("NO" if not colours or any(
        word in issue.lower() for issue in issues for word in blockers
    ) else "UNCERTAIN")
    return colours, source, completeness, sorted(issues)


def classify_colour(rgb):
    r, g, b = (max(0.0, min(1.0, float(x))) for x in rgb)
    hue, saturation, value = colorsys.rgb_to_hsv(r, g, b)
    if value >= 0.90 and saturation <= 0.12:
        return "WHITE", "WARNING"
    if saturation < 0.25 or value < 0.20:
        return "NEUTRAL/DARK", "NO_FLAG"
    if 75 <= hue * 360 < 170:
        return "GREEN", "WARNING"
    if 185 <= hue * 360 < 260:
        return "BLUE", "WARNING"
    return "OTHER", "NO_FLAG"


def assess(entity):
    ext, evidence = exterior(entity)
    names, categories, material_status, mats = check_materials(entity)
    colours, source, completeness, issues = get_colours(entity, mats)
    colour_checks = [classify_colour(rgb) for rgb in colours]
    colour_status = ("UNKNOWN" if not colour_checks else
                     "WARNING" if any(s == "WARNING" for _, s in colour_checks) else "NO_FLAG")
    if ext == "NOT EXTERIOR":
        overall = "NOT APPLICABLE"
    elif colour_status == "WARNING":
        overall = "WARNING"
    elif material_status == "UNKNOWN" or colour_status == "UNKNOWN" or completeness == "NO":
        overall = "UNKNOWN"
    elif material_status == "REVIEW":
        overall = "REVIEW"
    else:
        overall = "PREFERRED"
    review = "NO" if overall in ("PREFERRED", "NOT APPLICABLE") else "YES"
    reasons = []
    if material_status != "PREFERRED":
        reasons.append("Material: " + material_status)
    if colour_status == "WARNING":
        reasons.append("Potentially discouraged colour")
    if colour_status == "UNKNOWN":
        reasons.append("No readable colour")
    if completeness == "NO":
        reasons.append("Known incomplete colour data")
    if completeness == "UNCERTAIN":
        reasons.append("Full surface coverage unverified")
    reasons.extend(issues)
    return {
        "GlobalId": entity.GlobalId,
        "IFC_Class": entity.is_a(),
        "Element_Name": entity.Name or "",
        "Exterior_Status": ext,
        "Exterior_Evidence": evidence,
        "Material_Names": names,
        "Material_Categories": categories,
        "Material_Status": material_status,
        "Colour_RGB": " | ".join("({:.3f}, {:.3f}, {:.3f})".format(*c) for c in colours),
        "Colour_Labels": " | ".join(label for label, _ in colour_checks),
        "Colour_Source": source,
        "Colour_Status": colour_status,
        "Colour_Data_Complete": completeness,
        "Overall_Status": overall,
        "Manual_Review_Required": review,
        "Reason": "; ".join(dict.fromkeys(reasons)),
    }


def downloads_folder():
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
                path, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
                return Path(os.path.expandvars(path))
        except (OSError, ImportError):
            pass
    return Path.home() / "Downloads"


def export_excel(results, path):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.worksheet.table import Table, TableStyleInfo
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("Excel skipped: openpyxl not installed in Blender Python.", flush=True)
        return

    wb = Workbook()
    wb.remove(wb.active)
    priority = {"WARNING": 0, "UNKNOWN": 1, "REVIEW": 2}
    review = sorted((r for r in results if r["Manual_Review_Required"] == "YES"),
                    key=lambda r: (priority.get(r["Overall_Status"], 9), r["GlobalId"]))
    fills = {"WARNING": "F4CCCC", "REVIEW": "FFF2CC", "UNKNOWN": "E7E6E6",
             "PREFERRED": "D9EAD3", "YES": "F4CCCC", "NO": "D9EAD3",
             "UNCERTAIN": "FFF2CC", "EXTERIOR": "D9EAD3", "NOT APPLICABLE": "E7E6E6"}
    status_cols = {"Exterior_Status", "Material_Status", "Colour_Status",
                   "Colour_Data_Complete", "Overall_Status", "Manual_Review_Required"}
    for title, rows in (("Review Required", review), ("All Elements", results)):
        ws = wb.create_sheet(title)
        ws.append(HEADERS)
        for r in rows:
            ws.append([r.get(h, "") for h in HEADERS])
        ws.freeze_panes = "D2"
        ws.sheet_view.showGridLines = False
        ws.row_dimensions[1].height = 34
        for index, header in enumerate(HEADERS, 1):
            ws.column_dimensions[get_column_letter(index)].width = (
                65 if header == "Reason" else 44 if header in
                ("Material_Names", "Exterior_Evidence") else 30 if header in
                ("Element_Name", "Colour_RGB") else 23)
        for cell in ws[1]:
            cell.fill = PatternFill("solid", fgColor="17365D")
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for header in status_cols:
            col = HEADERS.index(header) + 1
            for row_index in range(2, ws.max_row + 1):
                cell = ws.cell(row_index, col)
                if cell.value in fills:
                    cell.fill = PatternFill("solid", fgColor=fills[cell.value])
        last_col = get_column_letter(len(HEADERS))
        if rows:
            table = Table(displayName="ReviewTable" if title == "Review Required"
                          else "AllElementsTable", ref=f"A1:{last_col}{ws.max_row}")
            table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
            ws.add_table(table)
        else:
            ws.auto_filter.ref = f"A1:{last_col}1"
    wb.active = 0
    wb.save(path)
    print("Excel saved:", path, flush=True)


def save_reports(results):
    """Write three independent, timestamped reports to Downloads."""
    folder = downloads_folder()
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    base = folder / f"A4_Facade_Check_Results_{stamp}"

    csv_path = Path(str(base) + ".csv")
    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS, delimiter=";")
        writer.writeheader()
        writer.writerows(results)
    print("CSV saved:", csv_path, flush=True)

    json_path = Path(str(base) + ".json")
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)
    print("JSON saved:", json_path, flush=True)

    try:
        export_excel(results, Path(str(base) + ".xlsx"))
    except Exception as exc:
        print("Excel export failed:", repr(exc), flush=True)


def main():
    started = time.perf_counter()
    print("\nStarting A4 Facade Checker...", flush=True)
    model = get_model()
    elements = {e.id(): e for cls in CLASSES for e in model.by_type(cls)}
    print("Candidate elements:", len(elements), flush=True)
    results = []
    for index, entity in enumerate(elements.values(), 1):
        try:
            results.append(assess(entity))
        except Exception as exc:
            print("Element error:", entity.GlobalId, repr(exc), flush=True)
            row = {h: "" for h in HEADERS}
            row.update(GlobalId=entity.GlobalId, IFC_Class=entity.is_a(),
                       Element_Name=entity.Name or "", Overall_Status="UNKNOWN",
                       Manual_Review_Required="YES", Reason="Processing error: " + str(exc))
            results.append(row)
        if index % 100 == 0:
            print(f"Processed {index}/{len(elements)}", flush=True)
    print("Analysis finished. Exporting...", flush=True)
    save_reports(results)
    counts = Counter(r["Overall_Status"] for r in results)
    for status in ("PREFERRED", "REVIEW", "WARNING", "UNKNOWN", "NOT APPLICABLE"):
        print(f"{status}: {counts[status]}", flush=True)
    print("Manual review:", sum(r["Manual_Review_Required"] == "YES" for r in results))
    print(f"Completed in {time.perf_counter() - started:.1f} seconds", flush=True)
    return results


if __name__ == "__main__":
    A4_RESULTS = main()
