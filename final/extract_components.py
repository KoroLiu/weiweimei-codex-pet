"""Read-only alpha connected-component analysis for supplied sprite artwork."""
import numpy as np

def components(image):
    mask = np.asarray(image.getchannel('A')) > 8
    parent, bounds, areas = [], [], []
    previous = []
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def union(a,b):
        a,b = find(a),find(b)
        if a != b: parent[b] = a
    for y,line in enumerate(mask):
        changes = np.diff(np.pad(line.astype(np.int8),(1,1)))
        starts, ends = np.flatnonzero(changes==1),np.flatnonzero(changes==-1)
        current=[]
        j=0
        for x0,x1 in zip(starts,ends):
            i=len(parent); parent.append(i); bounds.append((int(x0),y,int(x1),y+1)); areas.append(int(x1-x0)); current.append((int(x0),int(x1),i))
            while j<len(previous) and previous[j][1]<x0: j+=1
            k=j
            while k<len(previous) and previous[k][0]<=x1:
                union(i,previous[k][2]); k+=1
        previous=current
    result={}
    for i,(box,area) in enumerate(zip(bounds,areas)):
        root=find(i)
        if root not in result: result[root]={'bbox':list(box),'area':area}
        else:
            r=result[root];r['area']+=area;r['bbox']=[min(r['bbox'][0],box[0]),min(r['bbox'][1],box[1]),max(r['bbox'][2],box[2]),max(r['bbox'][3],box[3])]
    return sorted(result.values(),key=lambda x:x['area'],reverse=True)

def pose_boxes(image,cols,rows,count):
    cs=components(image)
    significant=[c for c in cs if c['area']>400]
    # Large bodies must be separate. Smaller ahoges/accessories are retained
    # by assigning their component to the closest body's horizontal center.
    primary=[c for c in significant if c['area']>max(c['area'] for c in significant)*0.24]
    if len(primary)!=count:
        raise ValueError(f'Expected {count} separate bodies, got {len(primary)}: {primary}')
    primary=sorted(primary,key=lambda c:(round(((c['bbox'][1]+c['bbox'][3])/2)/(image.height/rows)-0.5),c['bbox'][0]))
    boxes=[p['bbox'][:] for p in primary]
    for component in significant:
        if component in primary: continue
        box=component['bbox']; cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
        distances=[]
        for p in primary:
            b=p['bbox']; px=(b[0]+b[2])/2; py=(b[1]+b[3])/2
            distances.append((cx-px)**2+(cy-py)**2)
        index=int(np.argmin(distances));b=boxes[index]
        boxes[index]=[min(b[0],box[0]),min(b[1],box[1]),max(b[2],box[2]),max(b[3],box[3])]
    return boxes,significant

if __name__=='__main__':
    from pathlib import Path
    from PIL import Image
    import json
    root=Path(__file__).parent/'sources'
    for p in root.glob('*-v1.png'):
        print(p.name,json.dumps(components(Image.open(p).convert('RGBA'))[:12]))
