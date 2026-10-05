"""Deterministically crop supplied art, register, assemble and inspect native atlas.

Does not draw, redesign or alter the character. Imagegen makes pose artwork;
this script handles only alpha fringe, crop, shared scaling and placement.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from extract_components import pose_boxes

ROOT = Path(__file__).resolve().parent
CELL = (192, 208)
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
NAMES = ['idle', 'running-right', 'running-left', 'waving', 'jumping', 'failed', 'waiting', 'running', 'review', 'look-0', 'look-8']
LABELS = ['常态', '向右跑', '向左跑', '挥手', '小跳', '炸毛', '等你回应', '思考工作', '完成开心', '视线上半圈', '视线下半圈']
FONT = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 18)
SMALLFONT = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 13)
SOURCES = {
    'running-right': ('run-right-v2.png', 4, 2),
    'running-left': ('run-left-v2.png', 4, 2),
    'waving': ('waving-v1.png', 2, 2),
    'jumping': ('jumping-v1.png', 3, 2),
    'waiting': ('waiting-v1.png', 3, 2),
    'running': ('working-v1.png', 3, 2),
    'look-0': ('look-first-eight-v1.png', 4, 2),
    'look-8': ('look-second-eight-v1.png', 4, 2),
}
TIMINGS = [[1680,660,660,840,840,1920], [120]*7+[220], [120]*7+[220], [140]*3+[280], [140]*4+[280], [140]*7+[240], [150]*5+[260], [120]*5+[220], [150]*5+[280], [280]*8, [280]*8]
frames, reviews = {}, {}

def hash_file(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def clean(im):
    data = np.array(im.convert('RGBA'))
    data[data[:,:,3] <= 8] = 0
    return Image.fromarray(data)

for row, state in enumerate(NAMES):
    folder = ROOT / 'frames' / state
    folder.mkdir(parents=True, exist_ok=True)
    if state in ['idle', 'failed', 'review']:
        previous = 'happy' if state == 'review' else state
        paths = sorted((ROOT.parent / 'samples' / 'v3' / 'native-frames' / previous).glob('*.png'))
        if len(paths) != COUNTS[row]:
            raise ValueError(f'Approved frame count wrong: {state}')
        frames[state] = [Image.open(path).convert('RGBA') for path in paths]
        reviews[state] = {'reused_approved_v3_state': previous, 'source_frame_hashes': [hash_file(p) for p in paths]}
    else:
        source_name, cols, rows = SOURCES[state]
        path = ROOT / 'sources' / source_name
        master = Image.open(path).convert('RGBA')
        poses, details = [], []
        boxes, component_review = pose_boxes(master, cols, rows, COUNTS[row])
        repair_scale = None
        if state in ['look-0','look-8']:
            repair_path = ROOT/'sources'/'look-edge-repair-v1.png'
            repair_master = Image.open(repair_path).convert('RGBA')
            repair_boxes,_ = pose_boxes(repair_master,2,1,2)
            repair_scale = float(np.median([b[3]-b[1] for b in boxes])) / float(np.median([b[3]-b[1] for b in repair_boxes]))
        for index in range(COUNTS[row]):
            if state in ['look-0','look-8'] and index==7:
                repair_box=repair_boxes[0 if state=='look-0' else 1]
                repair=clean(repair_master.crop(repair_box))
                repair=repair.resize((round(repair.width*repair_scale),round(repair.height*repair_scale)),Image.Resampling.LANCZOS)
                poses.append(repair)
                details.append({'repaired_source':repair_path.name,'source_sha256':hash_file(repair_path),'component_bounds':repair_box,'pair_fixed_scale':repair_scale})
                continue
            box = boxes[index]
            source_clipped = box[0]==0 or box[1]==0 or box[2]==master.width or box[3]==master.height
            if source_clipped:
                raise ValueError(f'Clipped at entire source image edge {state}:{index}, {box}')
            poses.append(clean(master.crop(box)))
            details.append({'component_bounds':box})
        scale = min(180 / float(np.median([p.height for p in poses])), 168/max(p.width for p in poses), 184/max(p.height for p in poses))
        # Only placement adds flight height; no character pixels are redrawn.
        # Keep the ahoge inside the cell even at the airborne apex.
        jump_offsets = [0, 8, 16, 8, 0] if state == 'jumping' else [0]*len(poses)
        if state == 'jumping':
            scale = min(scale, min((190-offset)/pose.height for offset, pose in zip(jump_offsets, poses)))
        result = []
        for index, pose in enumerate(poses):
            fitted = pose.resize((round(pose.width*scale),round(pose.height*scale)), Image.Resampling.LANCZOS)
            cell = Image.new('RGBA', CELL)
            cell.alpha_composite(fitted, ((192-fitted.width)//2, 196-fitted.height-jump_offsets[index]))
            result.append(cell)
        frames[state] = result
        reviews[state] = {'source':source_name,'source_sha256':hash_file(path),'source_dimensions':master.size,'alpha_extrema':master.getchannel('A').getextrema(),'fixed_scale':scale,'flight_y_offsets':jump_offsets,'source_height_ratio':max(p.height for p in poses)/min(p.height for p in poses),'poses':details}
    for index, cell in enumerate(frames[state]):
        alpha = np.array(cell.getchannel('A'))
        if np.any(alpha[0]) or np.any(alpha[-1]) or np.any(alpha[:,0]) or np.any(alpha[:,-1]):
            raise ValueError(f'Final cell clipped {state}:{index}')
        cell.save(folder / f'{index+1:03d}.png')

atlas = Image.new('RGBA', (1536,2288))
for row, state in enumerate(NAMES):
    for column, cell in enumerate(frames[state]):
        atlas.alpha_composite(cell,(192*column,208*row))
package = ROOT / 'weiweimei'
package.mkdir(exist_ok=True)
atlas.save(ROOT / 'spritesheet.png')
atlas.save(package / 'spritesheet.webp', lossless=True, method=6, exact=True)
config = {'id':'weiweimei','displayName':'维维美','description':'安静陪伴，完成开心，出错短暂炸毛。细描边二维 Q 版；支持 16 个视线方向。','spriteVersionNumber':2,'spritesheetPath':'spritesheet.webp'}
(package/'pet.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Inspect the final decoded WebP, never an unencoded stand-in.
decoded = Image.open(package / 'spritesheet.webp').convert('RGBA')
if decoded.size != (1536,2288):
    raise ValueError('Native v2 dimensions wrong')
if not np.array_equal(np.array(decoded),np.array(atlas)):
    raise ValueError('Lossless WebP pixels differ')
valid, unused, encoded_frames = [], [], {}
for row, state in enumerate(NAMES):
    encoded_frames[state] = []
    for col in range(8):
        cell=decoded.crop((col*192,row*208,(col+1)*192,(row+1)*208))
        a=np.array(cell.getchannel('A'))
        if col < COUNTS[row]:
            if not np.any(a): raise ValueError(f'Missing required cell {row},{col}')
            encoded_frames[state].append(cell)
            valid.append({'row':row,'col':col,'state':state,'bbox':cell.getbbox(),'alpha_nonzero_pixels':int(np.count_nonzero(a))})
        else:
            if np.any(a): raise ValueError(f'Unused cell not transparent {row},{col}')
            unused.append([row,col])
if len(valid)!=73 or len(unused)!=15:
    raise ValueError('Native v2 frame count wrong')

previews = ROOT/'previews'
previews.mkdir(exist_ok=True)
encoding = {}
for row, state in enumerate(NAMES):
    seq=encoded_frames[state]
    durations=TIMINGS[row]
    if state not in ['idle','look-0','look-8']:
        # Native default reactions run three cycles, then return to idle.
        seq=seq*3+encoded_frames['idle']
        durations=durations*3+TIMINGS[0]
    seq[0].save(previews/f'{state}.webp',save_all=True,append_images=seq[1:],duration=durations,loop=0,lossless=True,method=6,exact=True)
    with Image.open(previews/f'{state}.webp') as animation:
        animation.load()
        count=animation.n_frames
        hashes=[]
        decoded_duration=0
        for i in range(count):
            animation.seek(i); animation.load()
            decoded_duration+=animation.info.get('duration',0)
            visible=np.array(animation.convert('RGBA'))
            visible[visible[:,:,3]==0,:3]=0
            hashes.append(hashlib.sha256(visible.tobytes()).hexdigest())
    encoding[state]={'decoded_frames':count,'unique_visible_frames':len(set(hashes)),'requested_duration_ms':sum(durations),'decoded_duration_ms':decoded_duration,'source_state_frames':COUNTS[row]}
    if decoded_duration!=sum(durations):
        raise ValueError(f'Encoded preview duration differs: {state}')
    if encoding[state]['unique_visible_frames'] < COUNTS[row]:
        raise ValueError(f'No meaningful unique animation frames: {state}')
look=encoded_frames['look-0']+encoded_frames['look-8']
look[0].save(previews/'look-directions.webp',save_all=True,append_images=look[1:],duration=280,loop=0,lossless=True,method=6,exact=True)

# QA presentation labels only; this drawing never enters the character atlas.
contact=Image.new('RGB',(1536,11*240),'#f1f3f7')
for row,state in enumerate(NAMES):
    for col,cell in enumerate(encoded_frames[state]):
        contact.paste(cell,(col*192,row*240),cell)
        label=f'{LABELS[row]} {col+1}' if row <9 else f'{(row-9)*180+col*22.5:g}°'
        ImageDraw.Draw(contact).text((col*192+96,row*240+224),label,font=FONT,fill='#263040',anchor='mm')
contact.save(previews/'all-frames-contact.png')
contact.resize((768,1320),Image.Resampling.LANCZOS).save(previews/'all-frames-small.png')
overview=Image.new('RGB',(3*320,3*280),'#f1f3f7')
for row,state in enumerate(NAMES[:9]):
    ox=(row%3)*320; oy=(row//3)*280
    cell=encoded_frames[state][0]
    overview.paste(cell,(ox+64,oy+10),cell)
    ImageDraw.Draw(overview).text((ox+160,oy+244),LABELS[row],font=FONT,fill='#263040',anchor='mm')
overview.save(previews/'states-overview.png')
look_contact=Image.new('RGB',(8*192,2*240),'#f1f3f7')
for index,cell in enumerate(look):
    x=index%8*192; y=index//8*240
    look_contact.paste(cell,(x,y),cell)
    ImageDraw.Draw(look_contact).text((x+96,y+224),f'{index*22.5:g}°',font=FONT,fill='#263040',anchor='mm')
look_contact.save(previews/'look-directions.png')
edges=Image.new('RGB',(3*192,2*208))
for col,state in enumerate(['idle','review','failed']):
    for row,bg in enumerate(['#f1f3f7','#1c202a']):
        stage=Image.new('RGB',CELL,bg); cell=encoded_frames[state][0]; stage.paste(cell,(0,0),cell); edges.paste(stage,(col*192,row*208))
edges.save(previews/'edges-light-dark.png')

report={'dimensions':list(decoded.size),'cell':list(CELL),'rows':NAMES,'required_per_row':COUNTS,'required_frames':len(valid),'transparent_unused_cells':unused,'lossless_pixels_equal':True,'atlas_sha256':hash_file(package/'spritesheet.webp'),'required_cells':valid,'sources':reviews,'encoded_previews':encoding,'native_runtime_verified':False}
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['dimensions','required_frames','lossless_pixels_equal','atlas_sha256','encoded_previews']},ensure_ascii=False,indent=2))
