"""Original product illustrations made with Pillow; no downloaded product photos.

The drawings are deliberately stylized demo assets, not representations of real
brands. Included under this project's MIT license and reproducible by seed_demo.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = (800, 700)


def product_art(kind, path, transparent=False):
    colors = {
        "headphones": ((227, 233, 217), (208, 219, 196)),
        "hoodie": ((232, 220, 203), (220, 201, 179)),
        "lamp": ((236, 230, 209), (220, 214, 184)),
        "backpack": ((220, 225, 216), (197, 209, 199)),
        "smartwatch": ((228, 227, 219), (209, 212, 198)),
        "sneakers": ((237, 229, 220), (224, 216, 202)),
        "speaker": ((224, 229, 218), (205, 217, 201)),
        "mug": ((234, 221, 208), (226, 207, 190)),
        "keyboard": ((224, 229, 225), (202, 212, 207)),
        "mouse": ((232, 231, 224), (214, 214, 201)),
        "powerbank": ((226, 228, 218), (207, 214, 198)),
        "jacket": ((219, 230, 231), (195, 212, 218)),
        "tshirt": ((237, 229, 218), (223, 213, 198)),
        "wallet": ((235, 223, 208), (218, 206, 188)),
        "glasses": ((235, 232, 216), (224, 216, 192)),
        "watch": ((236, 227, 216), (220, 209, 192)),
        "plant": ((230, 233, 216), (209, 218, 195)),
        "organizer": ((233, 226, 214), (217, 207, 190)),
        "yoga": ((224, 231, 226), (196, 216, 203)),
        "bottle": ((226, 229, 218), (207, 217, 197)),
        "pythonbook": ((231, 227, 215), (220, 213, 195)),
        "mlbook": ((226, 229, 223), (209, 218, 208)),
    }
    top, bottom = colors[kind]
    canvas = Image.new("RGB", SIZE)
    background = ImageDraw.Draw(canvas)
    for y in range(SIZE[1]):
        t = y / SIZE[1]
        color = tuple(int(a * (1-t) + b*t) for a, b in zip(top, bottom))
        background.line((0, y, SIZE[0], y), fill=color)
    shadow = Image.new("RGBA", SIZE)
    ImageDraw.Draw(shadow).ellipse((210, 539, 635, 609), fill=(41, 51, 35, 36))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow)
    obj = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(obj)

    if kind == "headphones":
        d.arc((205, 103, 595, 635), 180, 360, fill="#718265", width=51)
        d.arc((211, 109, 590, 629), 183, 354, fill="#a1b18c", width=36)
        d.arc((219, 117, 582, 619), 188, 348, fill="#c0cbaa", width=8)
        d.arc((236, 134, 566, 605), 190, 351, fill="#62745a", width=5)
        d.rounded_rectangle((205, 340, 244, 469), 15, fill="#829470")
        d.rounded_rectangle((561, 340, 598, 469), 15, fill="#768666")
        d.rounded_rectangle((169, 350, 242, 565), 35, fill="#485642")
        d.rounded_rectangle((575, 350, 629, 565), 27, fill="#4c5b42")
        d.rounded_rectangle((183, 347, 283, 566), 44, fill="#7d926e")
        d.rounded_rectangle((502, 345, 602, 566), 44, fill="#889d76")
        d.rounded_rectangle((189, 355, 270, 557), 38, fill="#adbd99")
        d.rounded_rectangle((508, 352, 591, 557), 38, fill="#9fb58c")
        d.rounded_rectangle((198, 363, 263, 548), 30, fill="#b7c5a2")
        d.rounded_rectangle((516, 361, 585, 548), 31, fill="#adc098")
        d.line((226, 376, 226, 521), fill="#c4ceae", width=3)
        d.line((548, 373, 548, 524), fill="#bdccaa", width=3)
        d.ellipse((218, 513, 233, 528), outline="#83966d", width=2)
        d.rounded_rectangle((589, 466, 595, 489), 3, fill="#53684b")
        obj = obj.rotate(-19, resample=Image.Resampling.BICUBIC)
    elif kind in {"smartwatch", "watch"}:
        smart = kind == "smartwatch"
        band = "#7c9271" if smart else "#8c634c"
        d.rounded_rectangle((343, 85, 457, 610), 26, fill=band)
        d.rounded_rectangle((349, 87, 450, 610), 22, outline="#9ead88" if smart else "#b58668", width=3)
        for y in range(457, 580, 22):
            d.rounded_rectangle((394, y, 406, y+9), 4, fill="#52604b" if smart else "#50392c")
        if smart:
            d.rounded_rectangle((288, 240, 509, 457), 50, fill="#6f7966")
            d.rounded_rectangle((297, 247, 499, 447), 44, fill="#2d3a33")
            d.rounded_rectangle((304, 256, 490, 437), 38, fill="#192e27")
            d.arc((328, 275, 468, 414), 20, 340, fill="#acc388", width=10)
            d.arc((342, 289, 454, 400), -30, 257, fill="#dfbaa1", width=9)
            d.arc((356, 302, 440, 387), 30, 309, fill="#7a9b85", width=8)
            d.line((400, 318, 400, 348, 425, 361), fill="#eef0d8", width=5)
            d.rounded_rectangle((508, 300, 520, 334), 5, fill="#7f8e70")
        else:
            d.ellipse((278, 230, 521, 473), fill="#a48c60")
            d.ellipse((288, 240, 510, 462), fill="#d7c7a0")
            d.ellipse((298, 250, 500, 452), fill="#f5f0e4")
            for x1,y1,x2,y2 in [(400,260,400,278),(400,425,400,441),(310,351,329,351),(470,351,486,351)]:
                d.line((x1,y1,x2,y2), fill="#8e8167", width=3)
            d.line((400,294,400,351,449,370), fill="#466051", width=5)
            d.ellipse((394,345,406,357),fill="#ad9561")
            d.rectangle((522,337,536,365),fill="#b59b6c")
        obj=obj.rotate(-13, resample=Image.Resampling.BICUBIC)
    elif kind == "speaker":
        d.rounded_rectangle((210, 195, 610, 533), 95, fill="#697f5d")
        d.rounded_rectangle((213, 195, 600, 518), 91, fill="#9cab89")
        d.rounded_rectangle((227, 205, 587, 499), 80, fill="#829775")
        for y in range(231, 480, 8):
            for x in range(250, 570, 8):
                if not ((x < 280 or x > 550) and (y < 260 or y > 450)):
                    d.ellipse((x,y,x+2,y+2), fill="#586c50")
        d.rounded_rectangle((345, 203, 471, 225), 10, fill="#aaba96")
        d.line((370, 212, 382, 212), fill="#647657", width=2)
        d.line((440, 207, 440, 219), fill="#647657", width=2)
        d.line((434, 213, 446, 213), fill="#647657", width=2)
        d.rounded_rectangle((388, 416, 449, 439), 4, fill="#9bab8a")
        d.text((402, 421), "NOVA", fill="#5d7357", font=ImageFont.load_default(size=10))
    elif kind == "keyboard":
        d.rounded_rectangle((95, 230, 709, 505), 25, fill="#69786a")
        d.rounded_rectangle((99, 216, 709, 485), 22, fill="#a8b4a0")
        d.rounded_rectangle((112, 229, 695, 471), 15, fill="#5d705f")
        for row in range(5):
            for col in range(13):
                x=124+col*42;y=241+row*43
                if row == 4 and 3 <= col <= 8:
                    continue
                fill="#d8ddce" if col < 10 else "#9dae94"
                if row==0 and col==0:fill="#c6a386"
                d.rounded_rectangle((x,y,x+35,y+35),5,fill="#798977")
                d.rounded_rectangle((x,y,x+35,y+31),5,fill=fill)
                if row<4:d.text((x+12,y+8), str((col+row)%10) if row==0 else "QWERTYUIOPASD"[(col+row)%13], fill="#758069", font=ImageFont.load_default(size=12))
        d.rounded_rectangle((250,414,495,449),5,fill="#d3dace")
        obj=obj.rotate(-9,resample=Image.Resampling.BICUBIC)
    elif kind == "mouse":
        d.rounded_rectangle((280, 150, 528, 556), 118, fill="#899b7a")
        d.rounded_rectangle((290, 145, 517, 537), 107, fill="#b7c3a1")
        d.arc((294,148,513,530),187,353,fill="#cad2b7",width=8)
        d.line((404, 149, 404, 305),fill="#8b9d78",width=3)
        d.arc((296,198,512,335),2,178,fill="#9dad8b",width=2)
        d.rounded_rectangle((391,198,417,260),12,fill="#7c8e68")
        d.rounded_rectangle((396,203,412,252),7,fill="#d0d7bb")
        d.text((385,459),"nova",fill="#93a27e",font=ImageFont.load_default(size=14))
        obj=obj.rotate(-22,resample=Image.Resampling.BICUBIC)
    elif kind == "powerbank":
        d.rounded_rectangle((260, 170, 552, 547), 32, fill="#73856e")
        d.rounded_rectangle((260, 151, 541, 527), 30, fill="#b0bda3")
        d.line((280,165,520,165),fill="#d0d7c4",width=4)
        d.rounded_rectangle((361,199,445,239),10,fill="#344d3d")
        d.text((385,209),"100",fill="#d7e5bf",font=ImageFont.load_default(size=18))
        d.rounded_rectangle((356,499,393,509),3,fill="#485e42")
        d.rounded_rectangle((416,499,441,509),3,fill="#485e42")
        obj=obj.rotate(-12,resample=Image.Resampling.BICUBIC)
    elif kind in {"hoodie", "jacket", "tshirt"}:
        fill = {"hoodie":"#bda88b","jacket":"#668996","tshirt":"#ece7d7"}[kind]
        edge = {"hoodie":"#a38e72","jacket":"#527683","tshirt":"#c8c4b1"}[kind]
        d.polygon([(294,200),(206,226),(137,417),(203,446),(274,321),(265,565),(535,565),(526,321),(597,446),(662,417),(593,226),(506,200)],fill=edge)
        d.polygon([(299,192),(217,225),(155,407),(204,422),(284,296),(277,550),(523,550),(516,296),(596,422),(644,407),(583,225),(501,192)],fill=fill)
        d.line((281,310,290,521),fill=edge,width=3)
        d.line((516,310,510,520),fill=edge,width=3)
        if kind=="hoodie":
            d.ellipse((291,112,506,310),fill=edge)
            d.ellipse((305,112,492,285),fill=fill)
            d.ellipse((336,141,461,270),fill="#75644e")
            d.polygon([(328,243),(346,204),(400,270),(453,204),(473,243),(437,311),(358,311)],fill=fill)
            d.line((359,266,353,374),fill="#ddd0b7",width=4)
            d.line((439,266,446,374),fill="#ddd0b7",width=4)
            d.polygon([(337,431),(463,431),(481,508),(319,508)],fill=edge)
            d.polygon([(342,429),(458,429),(474,499),(326,499)],fill="#b6a082")
        elif kind=="jacket":
            d.polygon([(318,178),(351,161),(400,215),(449,161),(483,178),(448,262),(400,226),(353,262)],fill="#97adb2")
            d.line((400,228,400,544),fill="#446573",width=6)
            for y in range(274,545,51):d.ellipse((407,y,414,y+7),fill="#cdb793")
            for x in [303,442]:
                d.rectangle((x,285,x+56,351),outline="#a6b8b9",width=2)
                d.polygon([(x,285),(x+56,285),(x+56,304),(x+28,318),(x,304)],fill="#587d8b")
            d.line((283,528,519,528),fill="#a6b8b9",width=2)
        else:
            d.ellipse((333,157,467,256),fill=edge)
            d.ellipse((349,159,452,238),fill="#c7c0ae")
            d.polygon([(244,332),(268,285),(277,550),(523,550),(531,285),(555,332),(510,570),(291,570)],fill=fill)
            d.rectangle((436,305,477,350),outline="#d3cebd",width=2)
        d.line((283,541,518,541),fill=edge,width=3)
    elif kind=="sneakers":
        for offset in [(20,-90),(-35,40)]:
            shoe=Image.new("RGBA",SIZE);s=ImageDraw.Draw(shoe)
            s.polygon([(168,412),(217,276),(282,321),(378,320),(471,394),(606,425),(651,465),(629,509),(171,504),(141,470)],fill="#b4b4a0")
            s.polygon([(174,396),(220,283),(279,330),(371,329),(459,402),(591,436),(633,464),(617,486),(170,482),(154,462)],fill="#eae6d5")
            s.polygon([(180,397),(219,296),(236,319),(197,433)],fill="#a6b398")
            s.rounded_rectangle((158,466,641,515),16,fill="#f6f2e5")
            s.line((170,496,628,496),fill="#c7c5b0",width=3)
            s.polygon([(296,348),(331,333),(412,397),(381,418)],fill="#91a084")
            for i in range(5):s.line((286+i*23,349+i*12,268+i*23,380+i*12),fill="#fffdf0",width=7)
            s.arc((510,407,634,480),195,290,fill="#d5d0ba",width=3)
            shoe=shoe.rotate(-10,resample=Image.Resampling.BICUBIC)
            obj.alpha_composite(shoe,offset)
    elif kind=="wallet":
        d.rounded_rectangle((187,244,624,487),22,fill="#674f3a")
        d.rounded_rectangle((183,226,615,471),20,fill="#98724e")
        d.rounded_rectangle((198,239,600,455),16,outline="#ba976c",width=2)
        d.line((216,252,581,252),fill="#ae885f",width=2)
        d.rounded_rectangle((526,295,642,398),12,fill="#805d3e")
        d.rounded_rectangle((531,295,635,390),10,fill="#9c7952")
        d.ellipse((577,330,596,349),fill="#bf9c66")
        d.text((222,402),"NOVA",fill="#c0a277",font=ImageFont.load_default(size=16))
        obj=obj.rotate(-12,resample=Image.Resampling.BICUBIC)
    elif kind=="glasses":
        d.line((186,300,239,186,333,177),fill="#76614c",width=16)
        d.line((609,300,554,191,474,181),fill="#76614c",width=16)
        d.rounded_rectangle((151,284,357,457),55,fill="#7f674f")
        d.rounded_rectangle((431,284,640,457),55,fill="#7f674f")
        d.rounded_rectangle((165,296,343,442),47,fill="#354d42")
        d.rounded_rectangle((445,296,626,442),47,fill="#354d42")
        d.arc((165,296,343,443),188,353,fill="#668578",width=12)
        d.arc((445,296,626,443),188,353,fill="#668578",width=12)
        d.arc((344,299,446,368),190,349,fill="#7f674f",width=14)
        d.line((140,304,168,304),fill="#b4a07c",width=5)
        d.line((624,304,652,304),fill="#b4a07c",width=5)
        obj=obj.rotate(-12,resample=Image.Resampling.BICUBIC)
    elif kind=="backpack":
        d.arc((275,119,527,469),180,359,fill="#354c3d",width=37)
        d.arc((282,126,520,461),180,359,fill="#617858",width=17)
        d.rounded_rectangle((245,185,565,578),85,fill="#49604c")
        d.rounded_rectangle((252,182,551,561),74,fill="#778a69")
        d.arc((270,201,535,463),190,349,fill="#a1b093",width=3)
        d.rounded_rectangle((281,381,524,531),25,fill="#586f51")
        d.rounded_rectangle((286,381,517,523),20,fill="#6a805f")
        d.line((300,411,503,411),fill="#3c5542",width=4)
        d.rounded_rectangle((325,250,474,333),12,fill="#7f9370")
        d.rounded_rectangle((362,277,438,307),3,fill="#c3b295")
        d.text((379,285),"NOVA",fill="#5c6950",font=ImageFont.load_default(size=12))
        d.line((500,406,500,436),fill="#c2b092",width=6)
    elif kind=="lamp":
        d.ellipse((218,512,579,600),fill="#9b997a")
        d.ellipse((221,502,577,583),fill="#c5c2a1")
        d.ellipse((235,505,565,564),fill="#ded8b4")
        d.rounded_rectangle((382,216,409,546),13,fill="#a4a985")
        d.rounded_rectangle((389,218,400,540),5,fill="#c1c9a2")
        d.pieslice((229,109,568,410),180,360,fill="#b7bea0")
        d.ellipse((230,254,567,319),fill="#849776")
        d.ellipse((247,260,552,305),fill="#eae5c7")
        d.ellipse((371,272,426,303),fill="#fff4d0")
        d.ellipse((487,526,505,540),fill="#8b9778")
    elif kind=="mug":
        d.ellipse((465,245,674,469),fill="#b99278")
        d.ellipse((498,278,641,438),fill=top)
        d.rounded_rectangle((221,215,529,532),45,fill="#b4876d")
        d.rounded_rectangle((227,211,516,517),43,fill="#cfa58b")
        d.ellipse((221,180,529,265),fill="#e3c1a7")
        d.ellipse((238,191,512,250),fill="#785744")
        d.ellipse((254,210,497,248),fill="#a48366")
        d.arc((239,243,502,493),94,162,fill="#dfbca0",width=7)
        d.arc((235,187,520,263),176,356,fill="#f0d2b7",width=3)
    elif kind=="plant":
        d.line((402,181,409,467),fill="#6f8557",width=9)
        for box, angle, color in [((256,187,417,289),-27,"#638753"),((390,136,549,248),29,"#7d985e"),((245,293,410,393),-20,"#819e62"),((396,273,554,375),27,"#567a4b"),((348,111,421,262),-10,"#7b9258")]:
            leaf=Image.new("RGBA",SIZE);ld=ImageDraw.Draw(leaf);ld.ellipse(box,fill=color)
            ld.line((box[0]+15,(box[1]+box[3])//2,box[2]-15,(box[1]+box[3])//2),fill="#a1b584",width=2)
            leaf=leaf.rotate(angle,resample=Image.Resampling.BICUBIC,center=((box[0]+box[2])//2,(box[1]+box[3])//2))
            obj=Image.alpha_composite(obj,leaf)
        d=ImageDraw.Draw(obj)
        d.polygon([(288,405),(519,405),(492,567),(316,567)],fill="#bf9d7f")
        d.ellipse((288,380,519,430),fill="#e2c6aa")
        d.ellipse((304,389,503,419),fill="#5e5c40")
        d.ellipse((316,549,492,584),fill="#bf9d7f")
        d.line((333,438,345,552),fill="#d6b59b",width=3)
    elif kind=="organizer":
        d.polygon([(172,268),(580,207),(650,324),(235,390)],fill="#ad9271")
        d.polygon([(172,268),(235,390),(235,552),(172,432)],fill="#9b8062")
        d.polygon([(235,390),(650,324),(650,490),(235,552)],fill="#c7ad89")
        d.polygon([(204,280),(570,225),(619,313),(249,370)],fill="#e2d0af")
        d.polygon([(252,338),(407,316),(416,354),(267,376)],fill="#8b977a")
        d.polygon([(269,316),(402,295),(410,327),(274,346)],fill="#e9ddc2")
        d.polygon([(469,230),(531,219),(555,311),(492,321)],fill="#758a70")
        d.line((420,248,436,350),fill="#b29770",width=7)
        d.line((549,243,565,328),fill="#ba9d74",width=7)
        d.rounded_rectangle((370,420,491,441),8,fill="#9c8261")
        for y in range(458,529,19):d.line((251,y,634,y-65),fill="#b69a75",width=2)
    elif kind=="yoga":
        d.rounded_rectangle((152,359,641,542),18,fill="#7f9c85")
        d.line((175,519,620,519),fill="#a2bca7",width=3)
        d.rounded_rectangle((223,168,588,418),95,fill="#63876f")
        d.ellipse((155,171,345,420),fill="#abc0a6")
        d.ellipse((173,189,325,404),fill="#719379")
        d.ellipse((190,207,309,387),fill="#b2c8af")
        d.ellipse((208,226,291,369),fill="#75977e")
        d.ellipse((225,247,274,347),fill="#afc4aa")
        d.line((350,182,542,182),fill="#94b39c",width=3)
    elif kind=="bottle":
        d.rounded_rectangle((305,225,502,577),57,fill="#80967c")
        d.rounded_rectangle((311,216,491,565),49,fill="#9baf8c")
        d.rounded_rectangle((333,264,344,505),6,fill="#b9c6a7")
        d.rectangle((344,177,463,255),fill="#a1b393")
        d.rounded_rectangle((336,155,468,218),14,fill="#3e5846")
        d.arc((378,91,467,217),178,360,fill="#425e4a",width=14)
        d.line((349,165,449,165),fill="#6f8568",width=3)
        d.text((367,447),"NOVA",fill="#d1dbba",font=ImageFont.load_default(size=18))
    elif kind in {"pythonbook","mlbook"}:
        python=kind=="pythonbook"
        cover="#315948" if python else "#b78f6b"
        d.polygon([(234,163),(553,183),(571,564),(246,546)],fill="#b3b29a")
        d.polygon([(241,153),(560,170),(560,543),(241,525)],fill="#ece7d2")
        for y in range(518,539,4):d.line((255,y,554,y+17),fill="#c8c5b0",width=1)
        d.polygon([(228,141),(545,157),(546,524),(228,508)],fill=cover)
        d.line((246,148,246,507),fill="#57745b" if python else "#d0ac84",width=5)
        d.text((278,205),"THE EVERYDAY LIBRARY",fill="#b6c3a6" if python else "#ead6b8",font=ImageFont.load_default(size=13))
        d.text((277,258),"PYTHON" if python else "MACHINE",fill="#f0ebd3",font=ImageFont.load_default(size=38))
        d.text((279,306),"PROGRAMMING" if python else "LEARNING",fill="#e4d8bd",font=ImageFont.load_default(size=23 if python else 36))
        d.text((279,352),"A practical guide" if python else "The fundamentals",fill="#c2c9ad" if python else "#f0dbbb",font=ImageFont.load_default(size=18))
        for i in range(4):d.arc((320+i*17,405+i*5,450-i*8,503-i*8),180,359,fill="#c7bc96",width=3)
        obj=obj.rotate(-10,resample=Image.Resampling.BICUBIC)
    if transparent:
        canvas = Image.alpha_composite(shadow, obj)
    else:
        canvas = Image.alpha_composite(canvas, obj).convert("RGB")
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    canvas.save(path,"PNG",optimize=True)


def hero_art(path):
    product_art("headphones",path, transparent=True)
