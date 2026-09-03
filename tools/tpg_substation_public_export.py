import argparse, importlib, os, runpy, sys, traceback
from pathlib import Path

def args_after_dash():
    return sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []

def main():
    p=argparse.ArgumentParser(); p.add_argument('--variant',required=True); p.add_argument('--artifact-dir',required=True)
    a=p.parse_args(args_after_dash())
    workspace=Path(os.environ.get('GITHUB_WORKSPACE',os.getcwd())).resolve()
    out=Path(a.artifact_dir).resolve(); out.mkdir(parents=True,exist_ok=True)

    import addon_utils, bpy
    addon_root=Path(os.environ['BLENDER_USER_SCRIPTS']).resolve()/'addons'/'io_scene_edm'
    sys.path.insert(0,str(addon_root))
    addon_utils.enable('io_scene_edm',default_set=False,persistent=False)
    edm=importlib.import_module('io_scene_edm')
    if not bool(getattr(edm,'native_bindings',False)):
        raise RuntimeError('Official ED exporter loaded without native bindings')
    if tuple(bpy.app.version[:3]) != (4,1,1):
        raise RuntimeError(f'Expected Blender 4.1.1, got {bpy.app.version_string}')

    variants={
      'intact':('0','0','TPG_Electrical_Substation_V1.edm',True),
      'destroyed':('1','0','TPG_Electrical_Substation_V1_Destroyed.edm',True),
      'lod1':('0','1','TPG_Electrical_Substation_V1_LOD1.edm',False),
      'lod2':('0','2','TPG_Electrical_Substation_V1_LOD2.edm',False),
    }
    destroyed,lod,filename,save_blend=variants[a.variant]
    os.environ['TPG_SUB_DESTROYED']=destroyed; os.environ['TPG_SUB_LOD']=lod
    runpy.run_path(str(workspace/'edm-jobs'/'build_tpg_substation.py'),run_name='__main__')
    if len(bpy.context.scene.objects)==0: raise RuntimeError('Scene empty')
    if save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=str(out/(Path(filename).stem+'.blend')))
    from io_scene_edm import collection_walker
    from logger import log
    log.errors=[]; log.warnings=[]
    edm_path=out/filename
    collection_walker._write(bpy.context,str(edm_path))
    if log.errors: raise RuntimeError('EDM export errors: '+' | '.join(str(e) for e in log.errors))
    if not edm_path.exists() or edm_path.stat().st_size<=0: raise RuntimeError('No valid EDM output')
    print(f'DCS_EDM_EXPORT_SUCCESS {a.variant} {edm_path} {edm_path.stat().st_size}')

if __name__=='__main__':
    try: main()
    except Exception:
        traceback.print_exc(); raise SystemExit(1)
