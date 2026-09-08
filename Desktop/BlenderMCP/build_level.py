"""Build the reference-inspired Drowned Titan environment in Blender 5.2.

Run with Blender's Python API (including through the Blender MCP bridge).
The bundled scan is CC BY 3.0; see assets/LeePerrySmith_License.txt.
"""
import bpy
import bmesh
import math
import random
from pathlib import Path
from mathutils import Vector, Matrix, Euler, noise

ROOT = Path(r'C:\Users\WIN10\Desktop\BlenderMCP')
random.seed(1047)

# Only replace this builder's scene when rebuilding. Other scenes are retained.
old = bpy.data.scenes.get('STONE TITAN • The Drowned Sanctuary')
scene = bpy.data.scenes.new('STONE TITAN • The Drowned Sanctuary' if old is None else 'Stone Titan rebuild')
bpy.context.window.scene = scene
if old is not None:
    old_collections=list(old.collection.children)
    for obj in list(old.objects):
        if obj.users_scene == (old,):
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.scenes.remove(old)
    for coll in old_collections:
        if coll.users==0:bpy.data.collections.remove(coll)
    scene.name = 'STONE TITAN • The Drowned Sanctuary'

def collection(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

titan_coll = collection('01 • TITAN / cut stone plates')
debris_coll = collection('02 • FALLEN STONE / traversable ruins')
water_coll = collection('03 • WATER / flooded basin')
figure_coll = collection('04 • EXPLORER / scale reference')
air_coll = collection('05 • ATMOSPHERE / mist & distant cliffs')
rig_coll = collection('06 • CINEMATOGRAPHY')
source_coll = collection('99 • SOURCE / preserved head scan')
source_coll.hide_render = True
source_coll.hide_viewport = True

def move_to(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return obj

def new_node(nt, typ, name, pos):
    n = nt.nodes.new(typ); n.label = name; n.location = pos
    return n

def stone_material(name, dark=False):
    m = bpy.data.materials.new(name); m.use_nodes=True
    m.diffuse_color = (0.27,0.31,0.255,1) if not dark else (0.13,0.16,0.13,1)
    nt=m.node_tree; nt.nodes.clear(); lk=nt.links.new
    out=new_node(nt,'ShaderNodeOutputMaterial','Surface',(880,80))
    bs=new_node(nt,'ShaderNodeBsdfPrincipled','Weathered limestone',(620,100))
    bs.inputs['Roughness'].default_value=.74
    tex=new_node(nt,'ShaderNodeNewGeometry','World-scale stone',(-1080,120))
    broad=new_node(nt,'ShaderNodeTexNoise','Mineral clouding',(-840,320))
    broad.inputs['Scale'].default_value=.29;broad.inputs['Detail'].default_value=5.0;broad.inputs['Roughness'].default_value=.78
    lk(tex.outputs['Position'],broad.inputs['Vector'])
    ramp=new_node(nt,'ShaderNodeValToRGB','Jade grey / chalk / lichen',(-560,330))
    r=ramp.color_ramp;r.elements.remove(r.elements[1])
    colors=[(.18,(.12,.145,.110,1)),(.40,(.24,.270,.218,1)),(.60,(.34,.376,.303,1)),(.83,(.48,.505,.407,1))]
    for i,(p,c) in enumerate(colors):
        e=r.elements[0] if i==0 else r.elements.new(p);e.position=p
        e.color=tuple(v*.67 if j<3 and dark else v for j,v in enumerate(c))
    lk(broad.outputs['Fac'],ramp.inputs['Fac']);lk(ramp.outputs['Color'],bs.inputs['Base Color'])
    mid=new_node(nt,'ShaderNodeTexNoise','Eroded rock grain',(-830,-80))
    mid.inputs['Scale'].default_value=2.2;mid.inputs['Detail'].default_value=6;mid.inputs['Roughness'].default_value=.8
    lk(tex.outputs['Position'],mid.inputs['Vector'])
    bm=new_node(nt,'ShaderNodeBump','Weathered relief',(-180,-80));bm.inputs['Strength'].default_value=.85;bm.inputs['Distance'].default_value=.32
    lk(mid.outputs['Fac'],bm.inputs['Height'])
    fine=new_node(nt,'ShaderNodeTexNoise','Micro pits',(-520,-330));fine.inputs['Scale'].default_value=28;fine.inputs['Detail'].default_value=3;fine.inputs['Roughness'].default_value=.75
    lk(tex.outputs['Position'],fine.inputs['Vector'])
    b2=new_node(nt,'ShaderNodeBump','Granular stone',(100,-60));b2.inputs['Strength'].default_value=.38;b2.inputs['Distance'].default_value=.065
    lk(fine.outputs['Fac'],b2.inputs['Height']);lk(bm.outputs['Normal'],b2.inputs['Normal']);lk(b2.outputs['Normal'],bs.inputs['Normal'])
    lk(bs.outputs['BSDF'],out.inputs['Surface'])
    return m

stone=stone_material('LIMESTONE • pale mineral weathering')
cutstone=stone_material('FRACTURES • rough dark interior',True)

def simple_mat(name,color,roughness=.7,metallic=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=roughness;p.inputs['Metallic'].default_value=metallic
    return m

black=simple_mat('EXPLORER • graphite waterproof fabric',(.017,.021,.021))
brass=simple_mat('EXPLORER • weathered ochre pack',(.22,.12,.037))

# Import a new source into the new scene, preserving the earlier inspection scene.
pre=set(bpy.data.objects)
pre_scenes=set(bpy.data.scenes)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets'/'LeePerrySmith.glb'))
imports=[o for o in bpy.data.objects if o not in pre]
head=next(o for o in imports if o.type=='MESH')
head.name='SOURCE • Lee Perry-Smith scan (CC BY 3.0)'
for o in imports:
    if o != head: bpy.data.objects.remove(o,do_unlink=True)
head.data.transform(head.matrix_world);head.matrix_world=Matrix.Identity(4)
head.data.materials.clear();head.data.materials.append(stone);head.data.materials.append(cutstone)
bpy.context.view_layer.objects.active=head;head.select_set(True)

# Remove shoulders at the neck and close the scan before making solid fractures.
bm=bmesh.new();bm.from_mesh(head.data)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0001,plane_co=(0,0,-1.06),plane_no=(0,0,1),clear_inner=True)
boundary=[e for e in bm.edges if e.is_boundary]
if boundary: bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.to_mesh(head.data);bm.free()
sub=head.modifiers.new('Sculpt resolution','SUBSURF');sub.levels=1;sub.render_levels=1
bpy.ops.object.modifier_apply(modifier=sub.name)
for p in head.data.polygons:p.use_smooth=True
# Carved almond-like recesses replace the scan's closed eyelids.
for x,angle in ((-.68,-8),(.50,8)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=1,location=(x,-1.925,1.79))
    cutter=bpy.context.object;cutter.name='Temporary eye socket cutter'
    for v in cutter.data.vertices:v.co.z*=max(.08,math.sqrt(max(0,1-v.co.x**2)))
    cutter.scale=(.405,.44,.152);cutter.rotation_euler[1]=math.radians(angle)
    cutter.data.materials.append(stone);cutter.data.materials.append(cutstone)
    for p in cutter.data.polygons:p.material_index=1;p.use_smooth=True
    bpy.context.view_layer.objects.active=cutter
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    boolean=head.modifiers.new('Carved stone eye socket','BOOLEAN');boolean.operation='DIFFERENCE';boolean.solver='EXACT';boolean.object=cutter
    bpy.context.view_layer.objects.active=head
    bpy.ops.object.modifier_apply(modifier=boolean.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
base=head.data.copy()
move_to(head,source_coll)
head.hide_render=True
for imported_scene in list(bpy.data.scenes):
    if imported_scene not in pre_scenes:bpy.data.scenes.remove(imported_scene)
for imported_collection in list(scene.collection.children):
    if imported_collection not in (titan_coll,debris_coll,water_coll,figure_coll,air_coll,rig_coll,source_coll) and not imported_collection.all_objects:
        bpy.data.collections.remove(imported_collection)

rot=Euler((math.radians(3),math.radians(-12),math.radians(10)),'XYZ').to_matrix().to_4x4()
world=Matrix.Translation(Vector((13,18,11.5))) @ rot @ Matrix.Scale(12.0,4)

# Voronoi prisms partition the actual head mesh. Each cut is capped with an
# interior material, so missing plates reveal solid angular rock, not a decal.
seed_values=[(-1.15,3.65),(-.15,3.92),(1.34,3.50),(-1.22,2.60),(-.30,2.80),(.91,2.74),(2.70,2.50),
             (-1.87,1.66),(-.67,1.67),(.40,1.16),(2.37,1.45),
             (-1.16,.73),(-.48,.25),(.86,-.25),(2.43,.31),
             (-1.23,-.17),(-.60,-.55),(1.72,-1.29),(-.80,-1.46),(.26,-1.67)]
seeds=[Vector((x,0,z)) for x,z in seed_values]
recessed={3,11,15}
fragments=[]
for i,seed in enumerate(seeds):
    bm=bmesh.new();bm.from_mesh(base)
    for j,other in sorted(enumerate(seeds),key=lambda it:(it[1]-seed).length):
        if i==j:continue
        n=(other-seed).normalized();mid=(other+seed)*.5
        gap=.011 if seed.x<-.6 else .0017
        plane=mid-n*gap
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00002,plane_co=plane,plane_no=n,clear_outer=True)
        edges=[e for e in bm.edges if e.is_boundary and all(abs((v.co-plane).dot(n))<.0003 for v in e.verts)]
        if edges:
            fill=bmesh.ops.holes_fill(bm,edges=edges,sides=0)
            for f in fill.get('faces',[]):f.material_index=1;f.smooth=False
        if not bm.verts:break
    if not bm.faces:bm.free();continue
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    me=bpy.data.meshes.new('Solid cut limestone %02d'%i);bm.to_mesh(me);bm.free()
    me.materials.append(stone);me.materials.append(cutstone)
    ob=bpy.data.objects.new('TITAN • fractured plate %02d'%i,me);titan_coll.objects.link(ob)
    ob.matrix_world=world
    # The left temple and cheek have collapsed into the broken structure.
    if i in recessed:
        ob.location+=rot.to_3x3()@Vector((-.22,3.3,-.35))
        ob.rotation_euler.rotate_axis('Z',math.radians((i%3-1)*5))
        ob.name='TITAN • recessed collapse %02d'%i
    elif i==7:
        ob.location+=Vector((-.55,.10,-.35))
    for v in me.vertices:
        # Tiny, deterministic erosion of the scanned surface silhouette.
        original=v.co.copy()
        v.co+=noise.noise_vector(original*3.1)*.015
        v.co+=v.normal*(noise.noise_vector(original*11.5)[0]*.008)
    bev=ob.modifiers.new('Chipped arrises','BEVEL');bev.width=.007;bev.segments=2;bev.limit_method='ANGLE';bev.angle_limit=.53
    detail=ob.modifiers.new('Erosion tessellation','SUBSURF');detail.subdivision_type='SIMPLE';detail.levels=1;detail.render_levels=1
    grit=bpy.data.textures.new('Granular limestone %02d'%i,type='CLOUDS');grit.noise_scale=.095;grit.noise_depth=2
    disp=ob.modifiers.new('Physical limestone erosion','DISPLACE');disp.texture=grit;disp.texture_coords='LOCAL';disp.strength=.009;disp.mid_level=.5
    fragments.append(ob)

# Fine branching cracks supplement the broad structural breaks.
def poly_curve(name,points,radius,mat,coll):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=1
    spl=c.splines.new('POLY');spl.points.add(len(points)-1)
    for p,co in zip(spl.points,points):p.co=(*co,1)
    ob=bpy.data.objects.new(name,c);coll.objects.link(ob);c.materials.append(mat)
    return ob

# Irregular stones, with fractured profiles instead of smooth sphere silhouettes.
def rock(name,loc,size,seed,coll=debris_coll,flat=False):
    rng=random.Random(seed)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=loc)
    ob=bpy.context.object;ob.name=name;move_to(ob,coll)
    for v in ob.data.vertices:
        co=v.co.copy();factor=1+rng.uniform(-.15,.13)+noise.noise_vector(co*2.6+Vector((seed%37,0,0)))[0]*.15
        co*=factor
        if flat:
            co.z=max(-.65,min(.53,co.z))
        v.co=(co.x*size[0],co.y*size[1],co.z*size[2])
    ob.rotation_euler=(rng.uniform(-.14,.14),rng.uniform(-.18,.18),rng.uniform(0,6.28))
    ob.data.materials.append(stone)
    bevel=ob.modifiers.new('Weather-softened chips','BEVEL');bevel.width=.08;bevel.segments=2
    bevel.affect='EDGES'
    if not flat:
        sub=ob.modifiers.new('Water-softened weathering','SUBSURF');sub.levels=1;sub.render_levels=1
        texture=bpy.data.textures.new(name+' erosion',type='CLOUDS');texture.noise_scale=.6;texture.noise_depth=2
        disp=ob.modifiers.new('Eroded surface','DISPLACE');disp.texture=texture;disp.strength=.16;disp.mid_level=.5
    for p in ob.data.polygons:p.use_smooth=not flat
    return ob

# Distant low coast / collapsed fragments at the foot of the monumental face.
for i in range(28):
    angle=random.uniform(-math.pi*.95,math.pi*.15)
    x=13+math.cos(angle)*random.uniform(21,36)
    y=18+math.sin(angle)*random.uniform(13,30)
    size=random.uniform(.8,3.0)
    rock('SCREE • titan foot %02d'%i,(x,y,random.uniform(-.1,.45)),(size,size*.85,size*random.uniform(.8,1.8)),300+i)

# Deliberate playable stepping route sweeping from lower-left to the statue.
route=[(-14,-59,0.3, (10,8,3.0)),(-11,-44,.1,(4.6,3.8,2.0)),(-7,-33,.1,(4.1,3.4,2.6)),
       (-12,-24,.1,(3.5,3,2.2)),(-4,-14,.1,(2.8,2.7,2.1)),(2,-5,.1,(3.5,3.0,3.0))]
for i,(x,y,z,sz) in enumerate(route):rock('PATH • stepping ledge %02d'%i,(x,y,z),sz,900+i,flat=True)

# Tall, framing boulders and secondary broken plates.
for i,(loc,size) in enumerate([
    ((26,-39,.1),(7.5,5.6,6.0)),((20,-32,.1),(4.0,4.5,3.2)),
    ((-24,-8,.3),(5.5,4.3,5.1)),((-18,2,.2),(3.4,3.0,4.5)),
    ((8,-22,.1),(2.0,2.5,3.0)),((12,-16,.1),(1.1,1.8,2.5)),
    ((-29,21,.0),(8,5,6)),((35,4,.0),(5,5,5)),
    ((-24,-83,-.3),(13,9,2.5))]):
    rock('RUIN • monumental debris %02d'%i,loc,size,1050+i)
for i in range(30):
    x=random.uniform(-29,33);y=random.uniform(-45,6)
    if -21<x<-9 and y<-36:continue
    sz=random.uniform(.35,1.35)
    rock('RUBBLE • water worn fragment %02d'%i,(x,y,-.12),(sz,sz*random.uniform(.6,1.4),sz*random.uniform(.7,1.6)),1200+i)

# Large open water grid. Geometry provides long wave silhouettes; multi-scale
# anisotropic bump produces the tiny overlapping specular ripples.
water=bpy.data.materials.new('WATER • dark jade / layered wind ripples');water.use_nodes=True
nt=water.node_tree;nt.nodes.clear();lk=nt.links.new
out=new_node(nt,'ShaderNodeOutputMaterial','Water surface',(820,40))
bs=new_node(nt,'ShaderNodeBsdfPrincipled','Reflective flooded basin',(580,80))
bs.inputs['Base Color'].default_value=(.027,.054,.043,1)
bs.inputs['Metallic'].default_value=.38;bs.inputs['Roughness'].default_value=.10
bs.inputs['IOR'].default_value=1.333;bs.inputs['Transmission Weight'].default_value=.08
tex=new_node(nt,'ShaderNodeTexCoord','Water coordinates',(-1050,80))
mapping=new_node(nt,'ShaderNodeVectorMath','Elongated wind ripples',(-850,80));mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(.85,4.2,1)
lk(tex.outputs['Object'],mapping.inputs[0])
n1=new_node(nt,'ShaderNodeTexNoise','Crossing capillary waves',(-630,100));n1.inputs['Scale'].default_value=1.15;n1.inputs['Detail'].default_value=3;n1.inputs['Roughness'].default_value=.65
lk(mapping.outputs['Vector'],n1.inputs['Vector'])
b1=new_node(nt,'ShaderNodeBump','Ripple normals',(-280,120));b1.inputs['Strength'].default_value=.76;b1.inputs['Distance'].default_value=.26
lk(n1.outputs['Fac'],b1.inputs['Height'])
n2=new_node(nt,'ShaderNodeTexNoise','Fine reflection breakup',(-600,-210));n2.inputs['Scale'].default_value=8.5;n2.inputs['Detail'].default_value=2
lk(mapping.outputs['Vector'],n2.inputs['Vector'])
b2=new_node(nt,'ShaderNodeBump','Fine waves',(30,60));b2.inputs['Strength'].default_value=.24;b2.inputs['Distance'].default_value=.035
lk(n2.outputs['Fac'],b2.inputs['Height']);lk(b1.outputs['Normal'],b2.inputs['Normal']);lk(b2.outputs['Normal'],bs.inputs['Normal']);lk(bs.outputs['BSDF'],out.inputs['Surface'])
N=220;verts=[];faces=[]
for j in range(N+1):
    y=-145+j*250/N
    for i in range(N+1):
        x=-120+i*240/N
        z=.022*math.sin(y*2.2+x*.22)+.018*math.sin(y*3.3-x*.51)+.011*math.sin(x*2+y*.5)
        verts.append((x,y,z))
for j in range(N):
    for i in range(N):
        a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
me=bpy.data.meshes.new('Continuous rippled water grid');me.from_pydata(verts,[],faces);me.materials.append(water)
ob=bpy.data.objects.new('BASIN • jade black water',me);water_coll.objects.link(ob)
for p in me.polygons:p.use_smooth=True

# A subtle wet line around the stones, using world Z in the stone shader.
for mat in (stone,cutstone):
    nt=mat.node_tree;lk=nt.links.new
    bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
    oldcolor=bs.inputs['Base Color'].links[0].from_socket
    geo=new_node(nt,'ShaderNodeNewGeometry','Wet shoreline',(-1000,630))
    sep=new_node(nt,'ShaderNodeSeparateXYZ','Height above water',(-800,630));lk(geo.outputs['Position'],sep.inputs[0])
    height=new_node(nt,'ShaderNodeMapRange','Wet at waterline',(-570,630));height.inputs['From Min'].default_value=.12;height.inputs['From Max'].default_value=1.35;height.inputs['To Min'].default_value=.30;height.inputs['To Max'].default_value=1
    lk(sep.outputs['Z'],height.inputs['Value'])
    mix=new_node(nt,'ShaderNodeMixRGB','Wet darkening',(230,300));mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    lk(oldcolor,mix.inputs[1]);lk(height.outputs[0],mix.inputs[2]);lk(mix.outputs[0],bs.inputs['Base Color'])

# Tiny explorer in a coat, with an ochre pack and a restrained warm lantern.
def uvball(name,loc,scale,mat,coll=figure_coll):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=loc)
    o=bpy.context.object;o.name=name;move_to(o,coll);o.scale=scale;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def limb(name,a,b,r,mat):
    a=Vector(a);b=Vector(b);delta=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=r*.83,radius2=r,depth=delta.length,location=(a+b)*.5)
    o=bpy.context.object;o.name=name;move_to(o,figure_coll);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat)
    return o

fx,fy,fz=-11.6,-57.2,1.85
def P(x,y,z):return (fx+x*.65,fy+y*.65,fz+z*.65)
uvball('EXPLORER • hood',P(0,0,1.57),(.091,.094,.117),black)
uvball('EXPLORER • jacket',P(0,0,1.12),(.15,.098,.234),black)
uvball('EXPLORER • ochre pack',P(0,-.145,1.18),(.117,.065,.15),brass)
limb('EXPLORER • left leg',P(-.11,0,.95),P(-.19,.08,.10),.076,black)
limb('EXPLORER • right leg',P(.11,0,.95),P(.22,-.08,.10),.076,black)
limb('EXPLORER • left sleeve',P(-.20,0,1.36),P(-.30,0,.94),.066,black)
limb('EXPLORER • right sleeve',P(.20,0,1.36),P(.37,.02,1.02),.066,black)
uvball('EXPLORER • left boot',P(-.19,.10,.08),(.085,.15,.08),black)
uvball('EXPLORER • right boot',P(.22,-.05,.08),(.085,.15,.08),black)
em=bpy.data.materials.new('LANTERN • amber ember');em.use_nodes=True
pbs=em.node_tree.nodes.get('Principled BSDF');pbs.inputs['Base Color'].default_value=(1,.23,.035,1);pbs.inputs['Emission Color'].default_value=(1,.16,.025,1);pbs.inputs['Emission Strength'].default_value=5
uvball('EXPLORER • lantern',P(.38,.03,.83),(.065,.065,.105),em)

def light(name,typ,loc,energy,color,size=1,target=None):
    data=bpy.data.lights.new(name,typ);data.energy=energy;data.color=color
    ob=bpy.data.objects.new(name,data);rig_coll.objects.link(ob);ob.location=loc
    if typ=='AREA':data.shape='DISK';data.size=size
    elif typ=='POINT':data.shadow_soft_size=size
    if target is not None:ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    return ob

light('LANTERN • local pool','POINT',P(.38,-.03,1.0),14,(1,.33,.10),.12)
light('KEY • pale jade shaft','AREA',(-40,-16,57),58000,(.77,.88,.70),18,(5,5,25))
light('WATER • long soft reflection','AREA',(-29,-38,20),5000,(.48,.68,.61),18,(0,-15,0))
rim=light('RIM • dying ember','AREA',(40,30,37),10000,(1,.055,.018),14,(14,10,31));rim.data.specular_factor=.14
light('FOG • far shore glow','AREA',(-39,17,12),9000,(.63,.78,.68),14,(-8,0,4))
light('WATER • silver path','AREA',(-18,44,9),11000,(.52,.71,.61),18,(-7,-40,0))

worldmat=bpy.data.worlds.new('WORLD • subterranean night');worldmat.use_nodes=True
worldmat.node_tree.nodes.get('Background').inputs['Color'].default_value=(.023,.038,.029,1)
worldmat.node_tree.nodes.get('Background').inputs['Strength'].default_value=.18
scene.world=worldmat

fog=bpy.data.materials.new('ATMOSPHERE • low drifting mist');fog.use_nodes=True
nt=fog.node_tree;nt.nodes.clear();lk=nt.links.new
out=new_node(nt,'ShaderNodeOutputMaterial','Mist',(600,0))
vol=new_node(nt,'ShaderNodeVolumePrincipled','Scattering',(370,0));vol.inputs['Color'].default_value=(.58,.68,.61,1);vol.inputs['Anisotropy'].default_value=.25
tc=new_node(nt,'ShaderNodeTexCoord','Local mist',(-600,0))
sep=new_node(nt,'ShaderNodeSeparateXYZ','Height falloff',(-400,180));lk(tc.outputs['Generated'],sep.inputs[0])
r=new_node(nt,'ShaderNodeValToRGB','Fade above the water',(-170,180));r.color_ramp.elements[0].position=.05;r.color_ramp.elements[0].color=(1,1,1,1);r.color_ramp.elements[1].position=.93;r.color_ramp.elements[1].color=(0,0,0,1);lk(sep.outputs['Z'],r.inputs[0])
ns=new_node(nt,'ShaderNodeTexNoise','Patchy drift',(-400,-120));ns.inputs['Scale'].default_value=5;ns.inputs['Detail'].default_value=3;lk(tc.outputs['Generated'],ns.inputs['Vector'])
mul=new_node(nt,'ShaderNodeMath','Fog wisps',(-30,0));mul.operation='MULTIPLY';lk(r.outputs[0],mul.inputs[0]);lk(ns.outputs['Fac'],mul.inputs[1])
den=new_node(nt,'ShaderNodeMath','Density',(170,0));den.operation='MULTIPLY';den.inputs[1].default_value=.010;lk(mul.outputs[0],den.inputs[0]);lk(den.outputs[0],vol.inputs['Density']);lk(vol.outputs['Volume'],out.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,10,5));fogob=bpy.context.object;fogob.name='MIST • drifting low layer';move_to(fogob,air_coll);fogob.scale=(175,155,14);fogob.data.materials.append(fog);fogob.display_type='WIRE'

# Dark rear cliffs remain barely legible beyond the water.
for i in range(7):
    distant=rock('DISTANCE • cavern buttress %02d'%i,(-90+i*30,92+random.uniform(-5,12),4),(random.uniform(11,18),12,random.uniform(8,14)),1600+i,air_coll)
    distant.data.materials.clear();distant.data.materials.append(cutstone)

camd=bpy.data.cameras.new('CAMERA • reference composition');cam=bpy.data.objects.new('CAMERA • reference composition',camd);rig_coll.objects.link(cam)
cam.location=(-7,-112,7.3);target=Vector((0,10,21.0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camd.lens=56;camd.sensor_width=36;camd.clip_end=600;camd.dof.use_dof=False
scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=True
scene.cycles.max_bounces=8;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=4;scene.cycles.transmission_bounces=4;scene.cycles.volume_bounces=1
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='OPTIX'
    scene.cycles.device='GPU'
except Exception:scene.cycles.device='CPU'
scene.render.resolution_x=1000;scene.render.resolution_y=1250;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(ROOT/'Stone_Titan_Preview.png')
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.3
scene.render.image_settings.color_mode='RGB'
scene['Design']='Drowned Sanctuary — monumental shattered limestone head, flooded traversal route, explorer for scale. Reference-inspired 3D environment.'
scene['Head scan credit']='Infinite, 3D Head Scan by Lee Perry-Smith / Infinite Realities. CC BY 3.0. Source: three.js examples; modified into fractured stone.'
scene['Navigation']='Use the numbered Outliner collections. Numpad 0: composed camera. Material Preview or Rendered: finished stone and water.'
scene.unit_settings.system='METRIC'
# Place the sanctuary at colossal architectural scale: about 180 m tall,
# with a roughly 1.8 m explorer. Framing is preserved by scaling the camera.
anchor=Vector((fx,fy,fz));world_scale=3.0;explorer_scale=1.55
for ob in list(scene.objects):
    if ob in source_coll.objects.values():continue
    if ob in figure_coll.objects.values() or ob.name.startswith('LANTERN • local'):
        ob.location=anchor*world_scale+(ob.location-anchor)*explorer_scale
        ob.scale*=explorer_scale
    else:
        ob.location*=world_scale
        ob.scale*=world_scale
    if ob.type=='LIGHT':
        ob.data.energy*=world_scale**2
    if ob.type=='CAMERA':ob.data.clip_end*=world_scale
for mat in (stone,cutstone,water):
    for node in mat.node_tree.nodes:
        if node.type=='BUMP':node.inputs['Distance'].default_value*=world_scale
den.inputs[1].default_value/=world_scale
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.shading.type='MATERIAL'
        area.spaces.active.shading.use_scene_world=True
        area.spaces.active.shading.use_scene_lights=True
scene.render.fps=24
text=bpy.data.texts.new('ABOUT • Drowned Sanctuary')
text.write('DROWNED SANCTUARY\n\nReference-inspired environment built for this Blender project.\nEditable stone fragments, flooded basin, traversal ledges and explorer.\n\nHEAD SCAN ATTRIBUTION\nInfinite, 3D Head Scan by Lee Perry-Smith / Infinite Realities\nCreative Commons Attribution 3.0 Unported\nhttps://creativecommons.org/licenses/by/3.0/\nhttps://github.com/mrdoob/three.js/tree/dev/examples/models/gltf/LeePerrySmith\nModified: neck trimmed, stone materials, volumetric fracture plates, scale and pose.\n\nRebuild: run build_level.py from the Blender text editor or the MCP execute tool.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Stone_Titan_Level.blend'),compress=True)
result={'file':bpy.data.filepath,'scene':scene.name,'objects':len(scene.objects),'head_fragments':len(fragments),'render_device':scene.cycles.device}
