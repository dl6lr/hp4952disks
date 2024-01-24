import sys, struct

with open(sys.argv[1], 'rb') as f:
    a = bytearray(f.read())
with open(sys.argv[2], 'rb') as f:
    b = bytearray(f.read())

a_tracks, b_tracks = int(a[9]), int(b[9])
assert a_tracks < b_tracks
assert (len(a)&511) == 0
assert (len(b)&511) == 0

ex_tdh = b[0x200+a_tracks*4:0x200+b_tracks*4]
ents = list(struct.unpack('<%dH' % ((b_tracks-a_tracks)*2), ex_tdh))

a_off, b_off = len(a) // 512, ents[0]
for i in range(0,len(ents),2):
    ents[i] += a_off - b_off
a += b[b_off*0x200:]
a[0x200+a_tracks*4:0x200+b_tracks*4] = struct.pack('<%dH' % ((b_tracks-a_tracks)*2), *ents)
a[9] = b[9]

with open(sys.argv[3], 'wb') as f:
    f.write(a)
