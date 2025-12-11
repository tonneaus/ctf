![](matroiska.png)

We're given the file [`matroiska1.png`](matroiska1.png),
and it is actually a png file:
```
$ file matroiska1.png 
matroiska1.png: PNG image data, 204 x 420, 8-bit/color RGB, non-interlaced
```

However, the end of the file doesn't look like png.
```
$ hexdump -C matroiska1.png | tail
00048900  3c 93 23 33 8c bc ec 46  63 27 9c 3a c0 64 a5 00  |<.#3...Fc'.:.d..|
00048910  15 9b ed 20 ff fc df d6  05 4a df f6 d7 95 13 5b  |... .....J.....[|
00048920  3c 65 13 45 05 79 11 1b  f6 63 71 4c 01 1e 72 42  |<e.E.y...cqL..rB|
00048930  fa c4 f0 57 10 2a f1 55  e6 e8 62 39 4b 4f 20 71  |...W.*.U..b9KO q|
00048940  e8 10 ed 55 40 e6 3b a1  55 2a 58 47 e4 bf 84 0a  |...U@.;.U*XG....|
00048950  10 81 43 0b 2b 5f 4a 63  fd 21 5f e6 e4 6d 13 d6  |..C.+_Jc.!_..m..|
00048960  19 0e 42 dd 5c bb 28 62  0e 26 06 1e a5 51 1b 32  |..B.\.(b.&...Q.2|
00048970  3c 05 5f 69 97 5f 11 0f  5d 4e 02 03 5f 4b f3 0c  |<._i._..]N.._K..|
00048980  2b c4                                             |+.|
00048982
```

[A PNG file consists of a PNG signature followed by a series of chunks.][png]

Here is a tiny 1&times;1 png we can look at: 
```
$ hexdump -C 1x1.png 
00000000  89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52  |.PNG........IHDR|
00000010  00 00 00 01 00 00 00 01  01 00 00 00 00 37 6e f9  |.............7n.|
00000020  24 00 00 00 0a 49 44 41  54 08 5b 63 60 00 00 00  |$....IDAT.[c`...|
00000030  02 00 01 62 40 4f 68 00  00 00 00 49 45 4e 44 ae  |...b@Oh....IEND.|
00000040  42 60 82                                          |B`.|
00000043
```
We can see chunk names `IHDR`, `IDAT`, and `IEND`.
A chunk has this format:
```
|     length (4 bytes)     |      type (4 bytes)      |
+--------------------------+--------------------------+
|  data (variable length)  |      crc (4 bytes)       |
```

Therefore at the end of `matroiska1.png` we should expect an IEND chunk.
But it's not there.  If we search for the IEND chunk, we find it here:
```
00014ec0  57 3e fe bf b6 96 0e e6  df bc 46 01 00 00 00 00  |W>........F.....|
00014ed0  49 45 4e 44 ae 42 60 82  e5 31 37 22 7f 38 76 6b  |IEND.B`..17".8vk|
00014ee0  79 65 72 3f 25 29 3d 37  72 32 6c d3 79 65 73 58  |yer?%)=7r2l.yesX|
```

Let's isolate the data after the IEND chunk.
```
$ dd if=matroiska1.png of=matroiska2.bin bs=`printf %d 0x00014ed8` skip=1
```

The resulting file `matroiska2.bin` is not a png:
```
$ hexdump -C matroiska2.bin | head
00000000  e5 31 37 22 7f 38 76 6b  79 65 72 3f 25 29 3d 37  |.17".8vkyer?%)=7|
00000010  72 32 6c d3 79 65 73 58  64 67 79 65 72 8c fc 61  |r2l.yesXdgyer..a|
00000020  e7 65 72 3e 21 08 3a 26  22 7b 2f 22 59 35 00 5d  |.er>!.:&"{/"Y5.]|
00000030  0a 08 15 00 72 32 24 e8  ec 32 75 6a 3f a8 6f fb  |....r2$..2uj?.o.|
00000040  29 60 4d 65 71 21 32 78  84 2c 69 f4 60 72 26 69  |)`Meq!2x.,i.`r&i|
00000050  54 91 fc 12 46 40 70 75  38 be 65 20 bc eb 5e 9c  |T...F@pu8.e ..^.|
00000060  8c bb 3c 61 b9 b8 c2 33  6d be 78 fa 0e 22 24 10  |..<a...3m.x.."$.|
00000070  17 63 80 1c c8 c5 d0 9e  e7 8a 1b 32 ac b6 6c db  |.c.........2..l.|
00000080  95 4e ad a9 83 fa 42 9a  8f d5 a0 5e 9e f9 49 41  |.N....B....^..IA|
00000090  83 7c 79 8d 2f 4e c5 55  6e b0 76 12 23 f3 56 ee  |.|y./N.Un.v.#.V.|
```

But it does have some structure, e.g., at offset 0x00032880 there is
an unusual long stretch of printable characters:
<details>
<summary>long hex dump, click to view</summary>
`xxd` prints printable and non-printable characters in different colours.
```
$ xxd -s 0x000326f0 matroiska2.bin 
000326f0: 61e7 36ac edbb e869 e3a1 f3bc 7481 f1d9  a.6....i....t...
00032700: 5a90 22a6 66bf 4ce4 aa03 642a 4ff3 a5c9  Z.".f.L...d*O...
00032710: 9459 fc72 ceb5 f119 db51 53b2 f2ba 84f1  .Y.r.....QS.....
00032720: f613 34ff edda 8b51 9639 fe7a 83a5 4429  ..4....Q.9.z..D)
00032730: 5bd0 b7f1 e63f d671 2aa8 3694 ea28 4228  [....?.q*.6..(B(
00032740: 3662 6ca3 a52a b0ef f47c 85a9 7045 680c  6bl..*...|..pEh.
00032750: 5e1c f5ca 2ef7 76ce 4aa3 c029 5ece 7431  ^.....v.J..)^.t1
00032760: 104f 1648 cb47 de82 8967 e1b5 f06f 1c1a  .O.H.G...g...o..
00032770: 2c9c 500b a35d 1ddb 3008 d655 4b4b e190  ,.P..]..0..UKK..
00032780: 63e8 5cb8 cc53 5a2e 9448 11a3 fd70 7653  c.\..SZ..H...pvS
00032790: 9167 474e ba58 1192 653f ef48 8eea 5b81  .gGN.X..e?.H..[.
000327a0: d68c 538b 3acd a4a5 2faa baeb c839 425b  ..S.:.../....9B[
000327b0: 3a9c e4ba 0fd2 5feb e14d 09d2 a345 5a8d  :....._..M...EZ.
000327c0: 9210 4992 a7d8 110f 5dd8 2e1e 5869 1003  ..I.....]...Xi..
000327d0: 4b6c 110f 5d46 4b43 101d 5d4d 4b46 110e  Kl..]FKC..]MKF..
000327e0: 5d4f 4b46 1015 5d4b 4b46 110e 5d4e 4b0c  ]OKF..]KKF..]NK.
000327f0: 1014 5d4b 4b46 110e 5d4e 4b14 1027 5d4d  ..]KKF..]NK..']M
00032800: 4b46 110e 5d4c 4b46 9666 5d4a 4b46 110e  KF..]LKF.f]JKF..
00032810: 5d4e 4b1c 110f 5d4e 4b46 119f 5d4e 4b47  ]NK...]NKF..]NKG
00032820: 110f 5dde 4b46 110e 5d4d d9c0 1108 5d4e  ..].KF..]M....]N
00032830: 4b54 110f 5dca eb44 110b 5d4e 4b47 110f  KT..]..D..]NKG..
00032840: 5da2 eb45 110b 5d4e 4b47 110f 5d16 4b46  ]..E..]NKG..].KF
00032850: 110f 1c1d 080f 580f 5d4e 1825 636a 3820  ......X.]N.%cj8 
00032860: 382e 7e7b 19e4 d229 110f 5d47 3b0e 487c  8.~{...)..]G;.H|
00032870: 5d4e 5d63 110f 4b6b 4a0f 432b ad4e 4b44  ]N]c..KkJ.C+.NKD
00032880: cb66 0916 3f1e 5c43 672d 242b 3f6e 3921  .f..?.\Cg-$+?n9!
00032890: 2923 3f77 303e 4b46 110f 5d72 337c 6962  )#?w0>KF..]r3|ib
000328a0: 2d23 2e32 702f 2523 2728 6235 2573 6927  -#.2p/%#'(b5%si'
000328b0: 7560 3f2b 7128 6235 302b 3f27 3e2d 7d36  u`?+q(b50+?'>-}6
000328c0: 713e 7c7f 2925 7664 4942 0d6e 0829 636a  q>|.)%vdIB.n.)cj
000328d0: 7d78 6576 3f3f 7f70 4166 312f 613c 2f20  }xev??.pAf1/a</ 
000328e0: 2b5d 1908 6b3e 7c63 333d 7134 7569 606c  +]..k>|c3=q4ui`l
000328f0: 2332 657f 6761 6431 6678 7339 7868 7e7d  #2e.gad1fxs9xh~}
00032900: 3a61 7a7f 2836 727e 7969 233d 703c 2f20  :az.(6r~yi#=p</ 
00032910: 3c7c 2420 3f27 6922 333d 6864 2f05 7d6e  <|$ ?'i"3=hd/.}n
00032920: 6b66 312f 613c 2f20 2b4b 383d 2834 787f  kf1/a</ +K8=(4x.
00032930: 2927 2428 317d 3928 7127 7360 283a 7664  )'$(1}9(q's`(:vd
00032940: 3305 7d6e 6b66 312f 7d6e 6b66 312f 2523  3.}nkf1/}nkf1/%#
00032950: 2728 6235 3836 2220 2c2d 353a 3f36 2b20  '(b586" ,-5:?6+ 
00032960: 7220 3868 706b 322c 2e68 7260 3061 2e3e  r 8hpk2,.hr`0a.>
00032970: 7869 727f 6576 3e2d 576e 6b66 312f 7d6e  xir.ev>-Wnkf1/}n
00032980: 6b66 312f 7d36 262a 7f7c 673a 2220 7732  kf1/}6&*.|g:" w2
00032990: 7f26 3f32 6135 7261 2535 3f6e 3921 2923  .&?2a5ra%5?n9!)#
000329a0: 3f6c 3223 6432 7869 3b61 7a68 2120 7f70  ?l2#d2xi;azh! .p
000329b0: 4166 312f 7d6e 6b66 312f 612b 332f 7735  Af1/}nkf1/a+3/w5
000329c0: 083d 2e34 5260 3023 2e28 6531 0e2d 3923  .=.4R`0#.(e1.-9#
000329d0: 7461 2e26 2432 2d20 3836 2220 2b5a 2e2b  ta.&$2- 86" +Z.+
000329e0: 3905 7e62 302b 2532 2f05 7d6e 6b66 312f  9.~b0+%2/.}nkf1/
000329f0: 7d6e 6b7a 7477 3428 7116 7877 3822 1302  }nkztw4(q.xw8"..
00032a00: 7862 3820 382f 7e61 637c 7870 2d20 3836  xb8 8/~ac|xp- 86
00032a10: 2220 2b5f 3436 2e2a 494b 3423 2e28 6266  " +_46.*IK4#.(bf
00032a20: 3220 754c 312f 7d6e 6b66 312f 7d72 2e3e  2 uL1/}nkf1/}r.>
00032a30: 7869 671e 223e 7463 040a 222b 7461 2e27  xig.">tc.."+ta.'
00032a40: 2428 2f37 6572 6423 6966 3b74 1b2f 696a  $(/7erd#if;t./ij
00032a50: 3117 0f2f 7c6a 333d 2229 7f31 576e 6b66  1../|j3=").1Wnkf
00032a60: 312f 7d6e 6b66 2d7b 3428 2d7c 436a 2e21  1/}nkf-{4(-|Cj.!
00032a70: 2733 6566 3220 1e28 787b 637c 7769 6566  '3ef2 .(x{c|wief
00032a80: 3b28 7114 747c 3222 3e32 7860 331b 252f  ;(q.t|2">2x`3.%/
00032a90: 6531 576e 6b66 312f 7d6e 6b66 2d7b 3428  e1Wnkf1/}nkf-{4(
00032aa0: 2d7c 495d 383d 242a 647b 3421 2578 203b  -|I]8=$*d{4!%x ;
00032ab0: 6961 7a7a 3e7b 3428 2d7c 495d 383d 242a  iazz>{4(-|I]8=$*
00032ac0: 647b 3421 2578 1b2f 7d6e 6b66 312f 7d6e  d{4!%x./}nkf1/}n
00032ad0: 7732 7869 3b74 1214 747c 3222 3e32 7860  w2xi;t..t|2">2x`
00032ae0: 3370 7a72 2520 6c72 6432 7869 3b74 1214  3pzr% lrd2xi;t..
00032af0: 747c 3222 3e32 7860 3370 4166 312f 7d6e  t|2">2x`3pAf1/}n
00032b00: 6b66 312f 613a 2220 7735 123c 2223 7f7b  kf1/a:" w5.<"#.{
00032b10: 3c3a 2229 7f31 6c72 6432 7869 3b74 0434  <:").1lrd2xi;t.4
00032b20: 786a 333a 2a32 7860 3370 4166 312f 7d6e  xj3:*2x`3pAf1/}n
00032b30: 6b7a 3e7d 3928 7102 747c 3e3c 2236 6566  kz>}9(q.t|><"6ef
00032b40: 3220 754c 312f 7d72 6434 7569 671c 0f00  2 uL1/}rd4uig...
00032b50: 2f05 6161 337c 6962 2d23 2e32 7031 5737  /.aa3|ib-#.2p1W7
00032b60: 5234 eb0f 5d41 640f 554e 0936 4aab 4c06  R4..]Ad.UN.6J.L.
00032b70: c91a 8e53 6cd2 a0f5 ec3d 6717 4b1f c764  ...Sl....=g.K..d
00032b80: 9307 e5af 5945 40ac 35c2 f0c4 f319 0cec  ....YE@.5.......
00032b90: 4f8b 508c 960f 5a54 460b c85e 1a64 3f87  O.P...ZTF..^.d?.
00032ba0: dd84 69c4 132d 33c6 00ce 7953 4d4a 5e12  ..i..-3...ySMJ^.
00032bb0: 5539 4cdf 92fd 6a75 96f5 e4a1 6e75 655d  U9L...ju....nue]
00032bc0: 2dc2 a0aa a5a1 d605 e6e0 a7b1 1cfb aba0  -...............
00032bd0: 33f3 ee80 b228 980c 61cc 912d 3d4a 4918  3....(..a..-=JI.
00032be0: 32bb 096b 5e47 544f 4d1e 89ac 535f 5942  2..k^GTOM...S_YB
00032bf0: 0906 1864 cdff 1f13 544f 54e5 2006 003f  ...d....TOT. ..?
```
</details>

We can also see the word "layer" at various places:
```
00000c80  30 03 3f 7f 6c 4b 79 65  72 3a 6c 65 78 7f 72 37  |0.?.lKyer:lex.r7|
00000c90  6c 61 79 64 72 32 6c 5f  78 7e 72 37 6c 61 79 64  |laydr2l_x~r7layd|
00000ca0  72 32 6c 27 78 4d 72 31  6c 61 79 64 72 30 6c 61  |r2l'xMr1laydr0la|
00000cb0  fe 0c 72 36 6c 61 79 64  72 32 6c 2f 79 65 72 32  |..r6laydr2l/yer2|
00000cc0  6c 61 79 f5 72 32 6c 60  79 65 72 a2 6c 61 79 64  |lay.r2l`yer.layd|
00000cd0  72 31 fe e7 79 62 72 32  6c 73 79 65 72 4a cc 63  |r1..ybr2lsyerJ.c|
00000ce0  79 61 72 32 6c 60 79 65  72 80 cc 62 79 61 72 32  |yar2l`yer..byar2|
00000cf0  6c 60 79 65 73 58 6c 61  79 65 33 61 2f 28 30 65  |l`yesXlaye3a/(0e|
```
```
00000e90  0a 0c 1d 5c 52 6b 59 45  52 12 4c 41 59 45 52 0e  |...\RkYER.LAYER.|
00000ea0  09 19 10 03 48 67 1f 04  0b 26 1d 5f 01 04 17 11  |....Hg...&._....|
00000eb0  4c 61 0f 13 1c 00 1c 41  04 0e 0d 59 5d 57 14 08  |La.....A...Y]W..|
00000ec0  1f 5f 27 41 09 13 3a 0a  1f 5f 09 0f 0d 5b 78 12  |._'A..:.._...[x.|
00000ed0  4c 41 59 45 52 0e 43 13  1d 03 48 76 09 12 1a 17  |LAYER.C...Hv....|
00000ee0  1b 42 18 08 16 0b 4c 38  4c 41 59 59 5d 40 08 07  |.B....L8LAYY]@..|
00000ef0  43 37 36 74 52 6b 45 4a  0a 08 14 0c 09 08 17 46  |C76tRkEJ.......F|
00000f00  0d 5f 73 ab 22 97 f1 61  79 65 6e 5b 28 2e 2d 65  |._s."..ayen[(.-e|
00000f10  72 32 6e 61 79 65 72 32  6c 61 cc 65 72 32 44 61  |r2nayer2la.er2Da|
00000f20  79 65 c7 32 6c 61 cc 65  72 a6 94 51 3b 69 02 32  |ye.2la.er..Q;i.2|
```

If we xor this file with our tiny `1x1.png`, a pattern emerges:
```py
def xor(a, b):
    return bytes(i ^ j for i, j in zip(a, b))


tiny = open('1x1.png', 'rb').read()
matroiska2 = open('matroiska2.bin', 'rb').read()

print(xor(tiny, matroiska2))
```
```
b'layer2layer2layer2l\xd2yesYegyer\xbb\x92\x98\xc3er>+A~gvstA95\x00]\x08\x08\x14b2}L\xe8\xec2u#z\xe6+Uk\x00\xcf'
```
So maybe `matroiska2.bin` is obfuscated with a many-time pad
(a [one-time pad][otp] with key reuse), where the repeating key is `layer2`.
```py
def repeat(key):
    while True:
        for byte in key:
            yield byte


def many_time_pad(key, data):
    return xor(repeat(key), data)


matroiska3 = many_time_pad(b'layer2', matroiska2)
with open('matroiska2.png', 'wb') as fp:
    fp.write(matroiska3)
```

This results in [`matroiska2.png`](matroiska2.png).  Like the original png,
this file also has trailing data after its IEND chunk.  Maybe more pngs are
nested in this same way.  Testing this idea:
```py
PNG = b'\x89PNG\r\n'  # png magic bytes


def extract(img_bytes, xor_coterm=PNG, keysize=6):
    trailer_pos = img_bytes.find(b'\0\0\0\0IEND') + 12
    trailer = img_bytes[trailer_pos:]
    def gen_segments():
        for i in range(0, len(trailer), keysize):
            for byte in trailer[i:i + keysize]:
                yield byte
    key = xor(trailer[:keysize], xor_coterm)
    plaintext = xor(gen_segments(), repeat(key))
    return key, plaintext


with open('../matroiska1.png', 'rb') as fp:
    data = fp.read()

for i in range(2, 100):
    key, data = extract(data)
    if len(data) == 0:
        break
    with open(f'matroiska{i}.png', 'wb') as fp:
        fp.write(data)
    print(key)
    print(data[:20])
    print()
```

At the end we get `matroiska5.png` which contains the flag:

![](matroiska5.png)

<!--
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠶⠝⠛⠛⠛⠛⠋⠉⠛⠛⠻⠷⣦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡾⠟⠋⠀⢰⡿⠟⠀⠀⠀⠀⢀⣀⣀⣀⡀⠘⠿⠾⢗⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⢮⣻⣛⣭⠶⡿⠋⠀⠀⠀⠀⠀⠀⣀⡤⠖⠚⠉⠉⠉⠁⠈⠉⠙⠲⢤⡀⠙⢯⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⣼⠛⠉⠉⣩⠇⠀⠀⠀⠀⠀⠀⣴⠞⠁⠀⠀⠀⠀⠀⠸⣿⣿⣿⣷⠄⠀⠙⢦⡀⠻⣌⡿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡿⡇⢘⡇⠀⠀⣰⠇⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠋⠀⠀⠀⠀⠻⡄⠙⣟⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢹⣷⣼⣿⣦⣠⣿⣶⣿⣿⣿⣤⣠⡏⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠹⡄⠹⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⢷⣴⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⢻⣿⣿⣿⢸⠃⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠸⣿⠈⣿⡿⢿⢸⡆⠀⢸⡇⡿⠿⣿⡇⣿⠿⢿⣿⣿⣿⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠧⠖⠛⠛⠛⠛⡛⢟⠇⠀⢸⠀⠁⠀⢼⣗⢻⠶⠶⢿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⣿⣿⣿⣿⣿⣿⣿⣿⣯⠀⠀⣠⣶⣟⣿⣳⠾⠀⠀⠀⠈⠀⠀⠀⣼⢶⢶⣶⢤⡀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣇⠘⠉⠻⠀⠀⠉⢮⣻⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠐⢜⣿⣟⣨⠀⣾⣿⠟⢿⢸⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠉⢠⠀⣞⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠈⣇⣿⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⢻⡟⢿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⠀⠀⠀⠘⣿⣾⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⡿⠁⠈⠁⠀⠙⠇⠈⠳⠈⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠾⣿⣿⣿⠀⠀⠀⠀⠘⣿⣳⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢦⣀⡀⠀⠀⢀⣠⠴⡚⠁⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠘⢿⢇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠫⣝⢋⡽⠣⠊⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⡿⢻⣿⣷⣤⡀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⢈⣾⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣾⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣶⣜⣿⣿⡇⠀⠀⠀⠀⠀⢠⣾⠏⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⣀⣴⣿⣳⡀⠀⠀⠀⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⠀⠀⠀⠀
⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⠀⠀
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⢸⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀
⢸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⠀
⢸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡇
-->

[png]: https://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
[otp]: https://en.wikipedia.org/wiki/One-time_pad
