__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.processor.TokenProcessor import TokenProcessor
from dietpdf.item import optimize_content_stream

def create_content_stream_1():
    return b"""
        0.1 w
        /Artifact
        BMC
            q
            0 0.028 595.275 841.861 re
            W* n
        EMC

        /Link <<
            /MCID 0
        >>

        BDC
            q
                0 0 0.50196 rg
                BT
                    56.8 773.989 Td
                    /F1 12 Tf
                    [
                        <01> 2
                        <0203> -6
                        <04> 2
                        <0506> 2
                        <07> -6
                        <0809080A0B080C0D0507> 1
                        <0E06> 2
                        <0F> 2
                        <1011>
                    ] TJ
                ET
            Q

            q
                1 0 0 1 56.8 773.989 cm
                0.7 w 0 0 0.50196 RG
                0 -1.1 m 113.7 -1.1 l S
            Q
        EMC

        /Link <<
            /MCID 1
        >>
        
        BDC
            q
                0 0 0.50196 rg
                BT
                    56.8 746.389 Td
                    /F1 12 Tf
                    [
                        <01> 2
                        <0203> -6
                        <04> 2
                        <0506> 2
                        <07> -6
                        <0812080A0B080C0D0507> 1
                        <0E06> 2
                        <0F> 2
                        <1011>
                    ] TJ
                ET
            Q

            q
                1 0 0 1 56.8 746.389 cm
                0.7 w 0 0 0.50196 RG
                0 -1.1 m 113.7 -1.1 l S
            Q
        EMC

        Q
    """

def create_content_stream_2():
    return b"""0.1 w
/Artifact BMC
q 0 0.028 595.275 841.861 re
W* n
EMC
/Link<</MCID 0>>BDC
q 0 0 0.50196 rg
BT
56.8 773.989 Td /F1 12 Tf[<01>2<0203>-6<04>2<0506>2<07>-6<0809080A0B080C0D0507>1<0E06>2<0F>2<1011>]TJ
ET
Q
q 1 0 0 1 56.8 773.989 cm
0.7 w 0 0 0.50196 RG
0 -1.1 m 113.7 -1.1 l S
Q
EMC
/Link<</MCID 1>>BDC
q 0 0 0.50196 rg
BT
56.8 746.389 Td /F1 12 Tf[<01>2<0203>-6<04>2<0506>2<07>-6<0812080A0B080C0D0507>1<0E06>2<0F>2<1011>]TJ
ET
Q
q 1 0 0 1 56.8 746.389 cm
0.7 w 0 0 0.50196 RG
0 -1.1 m 113.7 -1.1 l S
Q
EMC
Q """

def hexdump(stream: bytes):
    for base in range(0, len(stream), 16):
        hexadecimal_part = " ".join([
            ("%02X" % stream[offset])
            if offset < len(stream) else "  "
            for offset in range(base, base + 16)
        ])

        ascii_part = "".join([
            "%c" % (
                stream[offset] if stream[offset] in range(32, 128) else "."
            )
            if offset < len(stream) else " "
            for offset in range(base, base + 16)
        ])

        print("%08X:  %s  %s" % (base, hexadecimal_part, ascii_part))


def test_optimize_content_stream():
    white_spaces = [b"\0", b"\t", b"\n", b"\f", b"\r", b" "]

    streams = [
        create_content_stream_2(),
        create_content_stream_1(),
    ]

    for stream in streams:
        minimum_possible_stream = stream
        for space in white_spaces:
            minimum_possible_stream = minimum_possible_stream.replace(space, b"")

        optimized_stream = optimize_content_stream(stream)

        hexdump(optimized_stream)

        assert len(optimized_stream) != 0
        assert len(optimized_stream) > len(minimum_possible_stream)
        assert b"/ArtifactBMC" not in optimized_stream
