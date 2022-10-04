import sys

from scripts.transform import (
    InputSNP,
    OutputSNP,
    find_ref,
    read_input_file,
    read_reference,
)


def test_read_input_data():
    # given: input file path
    path = f"{sys.path[0]}/resources/test.tsv"

    # when: read
    result = read_input_file(path)

    # then: list of 2 SNP
    assert len(result) == 2
    assert result[0] == InputSNP("chrONE", 3765267, "rs1181875", "C", "T")
    assert result[1] == InputSNP("chr1", 65, "rs1483198", "G", "A")


def test_read_reference():
    # given: reference path & some collections of InputSNP
    path = f"{sys.path[0]}/resources/ref/"
    snps = [
        InputSNP("chr1", 65, "rs1483198", "G", "A"),
        InputSNP("chr1", 4304166, "rs693734", "C", "AT"),
        InputSNP("chrONE", 3765267, "rs1181875", "C", "T"),
    ]

    # when:
    result = read_reference(snps, path)

    # then:
    assert len(result) == 1
    assert "chr1" in result


def test_find_ref():
    # given: input data
    snps = read_input_file(f"{sys.path[0]}/resources/test.tsv")
    read_references = read_reference(snps, f"{sys.path[0]}/resources/ref/")

    # when: find ref for first SNP
    first_snp_ref = find_ref(read_references, snps[0])

    # then:
    assert first_snp_ref == "NOT_FOUND_REF"

    # when: find ref for second SNP
    second_snp_ref = find_ref(read_references, snps[1])

    # then:
    assert second_snp_ref == "C"


def test_output_snp_to_str():
    # given: some OutputSNP
    snp = OutputSNP("chr1", 65, "rs1483198", "G", "A/T")

    # when:
    result = str(snp)

    # then:
    assert result == "chr1\t65\trs1483198\tG\tA/T\t\n"
