"""
This is the scrpt for process the data of AHD
"""
import sys
import codecs
import xml.etree.cElementTree as ET


class Term():
    def __init__(self, iid, text, pos, text_ex):
        self.iid = iid
        self.text = text
        self.pos = pos
        self.text_ex = text_ex


class AhdProcess():
    terms = []
    terms_chs = []
    iid = 0x5107df000000
    tag = 80  # tag of part of speech
    raw = 0  # term without part of speech
    ncm = 1  # common noun (ncm)
    npp = 2  # person proper noun (npp)
    ngp = 3  # geographic proper noun (ngp)
    nop = 4  # organizational proper noun (nop)
    adj = 5  # adjective (adj)
    adv = 6  # adverb (adv)
    vtr = 7  # transitive verb (vtr)
    vit = 8  # intransitive verb (vit)
    vdi = 9  # ditransitive verb (vdi)
    prep = 10  # ditransitive verb (vdi)
    conj = 11  # conjunctions
    phr = 14  # phrase (phr)
    dif = 15  # various words in limited numbers, see Note 2. (dif)
    year = 2015  # the first byte is 0 for a.d. ,and the second byte is 2015 for year
    seqs = [1 for x in range(16)]  # an vector with value 0 and 16 elements
    seqs_mx = 16777216
    indexOfPos = 0  # the index of current process of pos

    def parse_ahd(self, inputfile, output_en, output_chs, version):
        print(inputfile)
        print(output_en)
        print(output_chs)
        parser = ET.XMLParser(encoding="utf-8")
        doc = ET.parse(inputfile, parser=parser)
        root = doc.getroot()
        print(root.tag)
        print("----------------")
        for block in root:
            self.parse_block(block)
        #    print("----------------")
        self.write(output_en, output_chs, version)

    def parse_block(self, block):
        for child in block:
            if (child.tag == u"基本词义"):
                self.parse_basic_sense(child)

    def parse_basic_sense(self, basic_sense):
        for child in basic_sense:
            if (child.tag == u"单词项"):
                self.parse_term(child)

    def parse_term(self, term):
        pos = "n."
        text = ""
        text_ex = ""
        text_chs = ""
        text_ex_chs = ""
        for child in term:
            if (child.tag == u"单词原型"):
                text = child.text
            #    print(text.encode("utf8"))
            elif (child.tag == u"单词词性"):
                pos = self.parse_pos(child.text)
                #    print(pos)
            elif (child.tag == u"解释项"):
                text_ex = child.text
                if (text_ex is not None):
                    iid = [self.tag | self.indexOfPos, self.year, self.seqs[self.indexOfPos]]
                    self.iid = self.encoding_iid(iid)
                    term = Term(self.iid, text, pos, text_ex)
                    #        print(term.iid, term.text, term.pos, term.text_ex)
                    self.terms.append(term)
            elif (child.tag == u"子解释项"):
                text_ex = child.text
                if (text_ex is not None):
                    iid = [self.tag | self.indexOfPos, self.year, self.seqs[self.indexOfPos]]
                    self.iid = self.encoding_iid(iid)
                    term = Term(self.iid, text, pos, text_ex)
                    #        print(term.iid, term.text, term.pos, term.text_ex)
                    self.terms.append(term)
            elif (child.tag == u"跟随注释"):
                text_chs = child.text
                if (text_chs is not None):
                    self.parse_chs(text_chs, pos)
                self.seqs[self.indexOfPos] += 1
            #    print("-------term---------")

    def parse_pos(self, pos):
        # i need to map the parsed pos to the new pos, and assign the new pos to the iid encoding
        npos = pos.find(".")
        if (len(pos) == 0):
            pos = "NONE"
            self.indexOfPos = 0

        elif ("NONE" in pos):
            pos = "NONE"
            self.indexOfPos = 0

        elif (pos.find("v.tr.intr") != -1):
            pos = "vdi"
            self.indexOfPos = 9

        elif (pos.find("v.intr") != -1):
            pos = "vit"
            self.indexOfPos = 8

        elif (pos.find("adv.") != -1):
            pos = "adv"
            self.indexOfPos = 6

        elif (pos.find("v.") != -1):
            pos = "vtr"
            self.indexOfPos = 7
        elif (pos.find("v.tr") != -1):
            pos = "vtr"
            self.indexOfPos = 7

        elif (pos.find("n.") != -1):
            pos = "ncm"
            self.indexOfPos = 1

        elif (pos.find("pl.n.") != -1):
            pos = "ncm"
            self.indexOfPos = 1

        elif (pos.find("adj.") != -1):
            pos = "adj"
            self.indexOfPos = 5

        elif (pos.find("prep.") != -1):
            pos = "prep"
            self.indexOfPos = 10

        elif (pos.find("conj.") != -1):
            pos = "conj"
            self.indexOfPos = 11

        else:
            pos = "dif"
            self.indexOfPos = 15
        return pos

    def leading_zeros(self, value, num_bytes):
        # hex_value = hex(value)
        hex_value = format(value, 'x')
        value %= self.seqs_mx

        leading_length = num_bytes * 2
        # print num_bytes * 4, ' - ',  pre_fix_length, ' - ', len(hex_value), ' = ', leading_length
        if leading_length > 0:
            # print leading_length
            hex_value = hex_value.zfill(leading_length)

        return hex_value

    def encoding_iid(self, iid):
        digits = [1, 2, 3]
        hex_list = [self.leading_zeros(value, digit) for value, digit in zip(iid, digits)]
        return '0x' + ''.join(hex_list)

    def parse_chs(self, text_chs, pos):
        text_ex_chs = ""
        npos = text_chs.find(u"：")
        if (npos != -1):
            #    print("found the Chinese seperator!")
            text_ex_chs = text_chs[npos + 1:]
            text_chs = text_chs[:npos]
        spos = text_chs.find(u"{")
        epos = text_chs.find(u"}")
        if (spos != -1 and epos != -1):
            if (u"&I{【" in text_chs):
                text_chs = text_chs[epos + 1:]
            elif (npos != -1):
                text_chs = text_chs[epos + 1:]
            else:
                text_chs = text_chs[spos + 1: epos];
        if (len(text_ex_chs) == 0):
            text_ex_chs = text_chs
        term_chs = Term(self.iid, text_chs, pos, text_ex_chs)
        self.terms_chs.append(term_chs)
        # print(term_chs.iid, term_chs.text.encode("utf8"), term_chs.pos, term_chs.text_ex.encode("utf8"))

    def write(self, output_en, output_chs, version):
        if version == 0:
            print("you version is 1.0.1")
            self.write_en(output_en)
            print("-------vocabulary---------")
            self.write_chs(output_chs)
        elif version == 1:
            print("you version is 1.0.0")
            self.write_en_10(output_en)
            print("-------vocabulary---------")
            self.write_chs_10(output_chs)
        elif version == 2:
            print("you version is 0.6.5")
            self.write_en_65(output_en)
            print("-------vocabulary---------")
            self.write_chs_65(output_chs)

    def write_en(self, output_en):
        root = ET.Element("Vocabulary")
        root.set("Iid", "0x5107df000000")
        root.set("Lang", "en")
        root.set("Version", "1.0.1")
        for term in self.terms:
            _term = ET.SubElement(root, "Term")
            _term.set("Iid", str(term.iid))
            _term.set("Text", term.text)
            _term.set("Pos", term.pos)
            _term.set("TextExplanation", term.text_ex)
        # ET.dump(root)
        f = open(output_en, "wb")
        try:
            f.write(prettify(root))
        finally:
            f.close

    def write_chs(self, output_chs):
        root = ET.Element("Vocabulary")
        root.set("Iid", "0x5107df000000")
        root.set("Lang", "chs")
        root.set("Version", "1.0.1")
        for term in self.terms_chs:
            _term = ET.SubElement(root, "Term")
            _term.set("Iid", str(term.iid))
            _term.set("Text", term.text)
            _term.set("Pos", term.pos)
            _term.set("TextExplanation", term.text_ex)
        # ET.dump(root)
        ##        ET.ElementTree(root).write(output_chs)
        f = open(output_chs, "wb")
        try:
            f.write(prettify(root))
        finally:
            f.close

    def write_en_65(self, output_en):
        root = ET.Element("xpm:voc")
        root.set("xmlns:xpm", "xpm:std:voc:schema:2012:10:01")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "xpm:std:voc:schema:2012:10:01 xpm-schema-v65-2012-10-01.xsd")
        root.set("xpm:iid", "0x5107df000000")
        root.set("xpm:an", "Vocabulary")
        root.set("xpm:lang", "en")
        root.set("xpm:version", "0.6.5")
        for term in self.terms:
            _term = ET.SubElement(root, "xpm:term")
            _term.set("xpm:iid", str(term.iid))
            _term.set("xpm:fc", term.text)
            _term.set("xpm:pos", term.pos)
            _term.set("xpm:an", term.text_ex)
        # ET.dump(root)
        f = open(output_en, "wb")
        try:
            f.write(prettify(root))
        finally:
            f.close

    def write_chs_65(self, output_chs):
        root = ET.Element("xpm:voc")
        root.set("xmlns:xpm", "xpm:std:voc:schema:2012:10:01")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "xpm:std:voc:schema:2012:10:01 xpm-schema-v65-2012-10-01.xsd")
        root.set("xpm:iid", "0x5107df000000")
        root.set("xpm:an", "Vocabulary")
        root.set("xpm:lang", "chs")
        root.set("xpm:version", "0.6.5")
        for term in self.terms_chs:
            _term = ET.SubElement(root, "xpm:term")
            _term.set("xpm:iid", str(term.iid))
            _term.set("xpm:fc", term.text)
            _term.set("xpm:pos", term.pos)
            _term.set("xpm:an", term.text_ex)
        # ET.dump(root)
        ##        ET.ElementTree(root).write(output_chs)
        f = open(output_chs, "wb")
        try:
            f.write(prettify(root))
        finally:
            f.close

    def write_en_10(self, output_en):
        root = ET.Element("sdf:voc")
        root.set("xmlns:sdf", "sdf:std:voc:schema:2014:11:28")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "sdf:std:voc:schema:2014:11:28 xpm-schema-v10-2014-11-28.xsd")
        vid = ET.SubElement(root, "sdf:vid")
        vid.set("sdf:dt", "0x5107df000000")
        tag = ET.SubElement(root, "sdf:tag")
        tag.text = "0x8"
        vi = ET.SubElement(root, "sdf:vi")
        sui = ET.SubElement(vi, "sdf:sui")
        sui.text = "0x2000000000"
        author = ET.SubElement(vi, "sdf:author")
        author.text = "Research group"
        vx = ET.SubElement(root, "sdf:vx")
        lang = ET.SubElement(vx, "sdf:lang")
        lang.text = "en"
        time = ET.SubElement(vx, "sdf:time")
        time.text = "2015"
        for term in self.terms:
            _term = ET.SubElement(root, "sdf:term")
            _term.set("sdf:pos", term.pos)
            _id = ET.SubElement(_term, "sdf:id")
            _iid = ET.SubElement(_id, "sdf:iid")
            _iid.text = str(term.iid)
            _word = ET.SubElement(_id, "sdf:word")
            _word.text = str(term.text)
            _concept = ET.SubElement(_term, "sdf:concept")
            _text = ET.SubElement(_concept, "sdf:text")
            _text.text = str(term.text_ex)
        f = open(output_en, "wb")
        try:
            f.write(prettify(root))
        finally:
            f.close

    def write_chs_10(self, output_chs):
        root = ET.Element("sdf:voc")
        root.set("xmlns:sdf", "sdf:std:voc:schema:2014:11:28")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "sdf:std:voc:schema:2014:11:28 xpm-schema-v10-2014-11-28.xsd")
        vid = ET.SubElement(root, "sdf:vid")
        vid.set("sdf:dt", "0x5107df000000")
        tag = ET.SubElement(root, "sdf:tag")
        tag.text = "0x8"
        vi = ET.SubElement(root, "sdf:vi")
        sui = ET.SubElement(vi, "sdf:sui")
        sui.text = "0x2000000000"
        author = ET.SubElement(vi, "sdf:author")
        author.text = "Research group"
        vx = ET.SubElement(root, "sdf:vx")
        lang = ET.SubElement(vx, "sdf:lang")
        lang.text = "chs"
        time = ET.SubElement(vx, "sdf:time")
        time.text = "2015"
        for term in self.terms_chs:
            _term = ET.SubElement(root, "sdf:term")
            _term.set("sdf:pos", term.pos)
            _id = ET.SubElement(_term, "sdf:id")
            _iid = ET.SubElement(_id, "sdf:iid")
            _iid.text = str(term.iid)
            _word = ET.SubElement(_id, "sdf:word")
            _word.text = str(term.text)
            _concept = ET.SubElement(_term, "sdf:concept")
            _text = ET.SubElement(_concept, "sdf:text")
            _text.text = str(term.text_ex)
        f = open(output_chs, "wb")
        try:
            f.write(prettify(root))
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        finally:
            f.close


from xml.dom import minidom


def prettify(elem):
    rough_str = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_str)
    return reparsed.toprettyxml(indent="    ", encoding="utf-8")


def main():
    print("Begining the process")
    version = 0
    inputfile = "E:\dev\data\powerword2007_pwdecahd.dict"
    output_en = "E:\dev\data\Vocabulary_en_1.0.1.xml"
    output_chs = "E:\dev\data\Vocabulary_zh_1.0.1.xml"
    output_en_65 = "E:\dev\data\Vocabulary_en_0.6.5.xml"
    output_chs_65 = "E:\dev\data\Vocabulary_zh_0.6.5.xml"
    output_en_10 = "E:\dev\data\Vocabulary_en_1.0.0.xml"
    output_chs_10 = "E:\dev\data\Vocabulary_zh_1.0.0.xml"
    p = AhdProcess()
    p.parse_ahd(inputfile, output_en, output_chs, 0)
    p.parse_ahd(inputfile, output_en_10, output_chs_10, 1)
    p.parse_ahd(inputfile, output_en_65, output_chs_65, 2)
    print("End the process")


if __name__ == "__main__": main()
