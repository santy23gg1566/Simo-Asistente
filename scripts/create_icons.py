from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import math
root=Path(__file__).resolve().parents[1]
def bez(p0,p1,p2,p3,steps=180):
 out=[]
 for j in range(steps+1):
  t=j/steps;u=1-t
  out.append(((u**3)*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],(u**3)*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
 return out
S=512; ss=3; size=S*ss
back=Image.new('RGB',(size,size)); px=back.load()
for y in range(size):
 for x in range(size):
  dx=x/size;dy=y/size
  glow=max(0,1-math.hypot(dx-.18,dy-.14)/.7)**1.5
  glow2=max(0,1-math.hypot(dx-.85,dy-.9)/.8)**1.3
  px[x,y]=(int(7+14*glow+15*glow2),int(15+28*glow+5*glow2),int(32+49*glow+51*glow2))
# orb luminous glow
halo=Image.new('RGBA',(size,size));hd=ImageDraw.Draw(halo)
hd.ellipse((190*ss,182*ss,322*ss,330*ss),fill=(62,169,255,90))
halo=halo.filter(ImageFilter.GaussianBlur(58*ss));back=Image.alpha_composite(back.convert('RGBA'),halo)
# ring elements
ring=Image.new('RGBA',(size,size));rd=ImageDraw.Draw(ring)
for i in range(5):
 pad=(76+i*3)*ss
 rd.arc((pad,pad,size-pad,size-pad),-70,115,fill=(69,174,255,max(15,80-i*15)),width=2*ss)
 rd.arc((pad,pad,size-pad,size-pad),124,285,fill=(157,112,255,max(15,80-i*15)),width=2*ss)
back=Image.alpha_composite(back,ring)
# main stylized S from cubic segments
points=[]
points+=bez((342,169),(300,120),(195,117),(169,180),100)
points+=bez((169,180),(138,254),(359,230),(346,328),120)
points+=bez((346,328),(331,407),(214,410),(161,350),100)
pts=[(int(x*ss),int(y*ss)) for x,y in points]
glowlayer=Image.new('RGBA',(size,size));gd=ImageDraw.Draw(glowlayer)
gd.line(pts,fill=(46,163,254,150),width=35*ss,joint='curve');glowlayer=glowlayer.filter(ImageFilter.GaussianBlur(15*ss));back=Image.alpha_composite(back,glowlayer)
slayer=Image.new('RGBA',(size,size));d=ImageDraw.Draw(slayer)
d.line(pts,fill=(49,161,248,255),width=30*ss,joint='curve')
# draw segment gradient overlay
for i in range(len(pts)-1):
 t=i/(len(pts)-1)
 if t<.55: k=t/.55; col=(int(116-36*k),int(236-77*k),255,255)
 else: k=(t-.55)/.45;col=(int(80+102*k),int(159-38*k),255,255)
 d.line((pts[i],pts[i+1]),fill=col,width=24*ss,joint='curve')
# center sparkle diamond
cx=256*ss;cy=259*ss
pts2=[(cx,cy-15*ss),(cx+15*ss,cy),(cx,cy+15*ss),(cx-15*ss,cy)]
d.polygon(pts2,fill=(124,252,239,230))
back=Image.alpha_composite(back,slayer)
base=back.convert('RGB').resize((512,512),Image.Resampling.LANCZOS)
base.save(root/'www/icon-512.png')
base.resize((192,192),Image.Resampling.LANCZOS).save(root/'www/icon-192.png')
base.save(root/'assets/SIMO-LOGO.png')
# foreground inside adaptive safe circle; black-transparent outside
safe=Image.new('RGBA',(512,512),(0,0,0,0))
inside=base.resize((348,348),Image.Resampling.LANCZOS)
safe.paste(inside,(82,82))
for d,pxsize in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 image=base.resize((pxsize,pxsize),Image.Resampling.LANCZOS)
 image.save(root/f'assets/ic_launcher_{d}.png')
 image.save(root/f'assets/ic_launcher_round_{d}.png')
 safe.resize((pxsize,pxsize),Image.Resampling.LANCZOS).save(root/f'assets/ic_launcher_foreground_{d}.png')
print('Icons generated')
