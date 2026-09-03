from pathlib import Path
import shutil, zipfile

ws=Path.cwd()
merged=ws/'merged'
root=ws/'package'/'TPG_Electrical_Substation_V1'
for d in (root/'Shapes',root/'Textures',root/'Database'): d.mkdir(parents=True,exist_ok=True)
names=['TPG_Electrical_Substation_V1.edm','TPG_Electrical_Substation_V1_Destroyed.edm','TPG_Electrical_Substation_V1_LOD1.edm','TPG_Electrical_Substation_V1_LOD2.edm']
for n in names:
    found=list(merged.rglob(n))
    if not found: raise FileNotFoundError(n)
    shutil.copy2(found[0],root/'Shapes'/n)
for p in merged.rglob('*'):
    if p.is_file() and 'Textures' in p.parts:
        shutil.copy2(p,root/'Textures'/p.name)
(root/'Shapes'/'TPG_Electrical_Substation_V1.lods').write_text('''model={\n lods={\n  {"TPG_Electrical_Substation_V1.edm",1500.0};\n  {"TPG_Electrical_Substation_V1_LOD1.edm",4500.0};\n  {"TPG_Electrical_Substation_V1_LOD2.edm",22000.0};\n };\n collision_shell="TPG_Electrical_Substation_V1.edm";\n}\n''',encoding='ascii')
(root/'entry.lua').write_text('''declare_plugin("TPG Electrical Substation V1.0",{installed=true,dirName=current_mod_path,displayName=_("TPG Electrical Substation V1.0"),version="1.0.0",state="installed",info=_("High-detail electrical substation static structure")})\nmount_vfs_model_path(current_mod_path.."/Shapes")\nmount_vfs_texture_path(current_mod_path.."/Textures")\ndofile(current_mod_path.."/Database/db_tpg_electrical_substation.lua")\nplugin_done()\n''',encoding='utf-8')
(root/'Database'/'db_tpg_electrical_substation.lua').write_text('''local function add_structure(f)\n f.shape_table_data={{file=f.ShapeName,life=f.Life,username=f.Name,desrt=f.ShapeNameDestr or "self",classname="lLandVehicle",positioning="BYNORMAL"}}\n if f.ShapeNameDestr then f.shape_table_data[#f.shape_table_data+1]={name=f.ShapeNameDestr,file=f.ShapeNameDestr} end\n f.mapclasskey="P0091000076"\n f.attribute={wsType_Static,wsType_Standing,"Structures"}\n add_surface_unit(f)\nend\nadd_structure({Name="TPG_Electrical_Substation_V1",DisplayName=_("TPG Electrical Substation V1.0"),ShapeName="TPG_Electrical_Substation_V1",ShapeNameDestr="TPG_Electrical_Substation_V1_Destroyed",Life=1200,Rate=100,category="Structures",SeaObject=false,isPutToWater=false,numParking=0})\n''',encoding='utf-8')
(root/'README.txt').write_text('TPG Electrical Substation V1.0\nInstall TPG_Electrical_Substation_V1 directly into Saved Games\\DCS\\Mods\\tech\\\nFinal pass: true terrain-contact berm, reference-driven substation insulators, flat placard signage.\n',encoding='utf-8')
out=ws/'TPG_Electrical_Substation_V1.0_DCS_DropIn.zip'
if out.exists(): out.unlink()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in root.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(root.parent))
print(out, out.stat().st_size)
