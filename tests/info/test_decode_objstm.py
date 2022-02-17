__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


from dietpdf.info.decode_objstm import decode_objstm

def create_stream():
    return b"""11 0 12 54 13 107
<</Type/Font/Subtype/TrueType/FontDescriptor 12 0 R>>
<</Type/FontDescriptor/Ascent 891/FontFile2 22 0 R>>
<</Type/Font/Subtype/Type0/ToUnicode 10 0 R>>"""


def test_decode_objstm():
    objects = decode_objstm(create_stream(), 18)

    assert len(objects) == 3
    assert objects[0].obj_num == 11
    assert objects[1].obj_num == 12
    assert objects[2].obj_num == 13
