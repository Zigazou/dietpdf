__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.processor.TokenProcessor import TokenProcessor
from dietpdf.item.content_stream import optimize_content_stream

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
    return b"""/CIDInit/ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo<<
/Registry (Adobe)
/Ordering (UCS)
/Supplement 0
>> def
/CMapName/Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<00> <FF>
endcodespacerange
86 beginbfchar
<01> <0046>
<02> <0050>
<03> <0047>
<04> <0041>
<05> <0049>
<06> <006C>
<07> <0020>
<08> <00E9>
<09> <0074>
<0A> <0061>
<0B> <0069>
<0C> <0075>
<0D> <006E>
<0E> <0065>
<0F> <0066>
<10> <006F>
<11> <0073>
<12> <003A>
<13> <0043>
<14> <0055>
<15> <0048>
<16> <0072>
<17> <0076>
<18> <0064>
<19> <004D>
<1A> <006B>
<1B> <002C>
<1C> <0031>
<1D> <0039>
<1E> <0034>
<1F> <0063>
<20> <0068>
<21> <006D>
<22> <00F4>
<23> <0045>
<24> <002D>
<25> <0044>
<26> <0056>
<27> <004E>
<28> <00C9>
<29> <0070>
<2A> <0021>
<2B> <0067>
<2C> <0053>
<2D> <0062>
<2E> <0032>
<2F> <2019>
<30> <004C>
<31> <0071>
<32> <0030>
<33> <0035>
<34> <006A>
<35> <0037>
<36> <0036>
<37> <0024>
<38> <003F>
<39> <007A>
<3A> <00E8>
<3B> <004F>
<3C> <0051>
<3D> <0052>
<3E> <0054>
<3F> <0042>
<40> <0153>
<41> <0079>
<42> <0078>
<43> <00EA>
<44> <00E0>
<45> <00EE>
<46> <0033>
<47> <00E7>
<48> <00C8>
<49> <00AB>
<4A> <00BB>
<4B> <00C0>
<4C> <004B>
<4D> <0057>
<4E> <0028>
<4F> <0029>
<50> <0038>
<51> <0058>
<52> <0077>
<53> <00F9>
<54> <20AC>
<55> <002F>
<56> <002E>
endbfchar
endcmap
CMapName currentdict /CMap defineresource pop
end
end
"""

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
        optimized_stream = optimize_content_stream(stream)

        hexdump(optimized_stream)

        assert len(optimized_stream) != 0
        assert len(optimized_stream) < len(stream)
        assert b"/ArtifactBMC" not in optimized_stream
