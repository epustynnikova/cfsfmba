import csv
import logging
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from pysam import Fastafile

logging.basicConfig(level=logging.DEBUG)


@dataclass(eq=True)
class InputSNP:
    chr: str
    position: int
    rsId: str
    allele1: str
    allele2: str

    def __str__(self) -> str:
        return self.rsId


@dataclass
class OutputSNP:
    chr: str
    position: int
    rsId: str
    ref: str
    alt: str

    def __str__(self) -> str:
        return "\t".join(
            [self.chr, str(self.position), self.rsId, self.ref, self.alt, "\n"]
        )


def parse_args(input_args):
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="input_file_path",
        default="data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv",
        help="input file path",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file_path",
        default="data/FP_SNPs_output.tsv",
        help="output file path",
    )
    parser.add_argument(
        "-r",
        "--reference",
        dest="reference_path",
        default="data/ref/",
        help="index reference directory path",
    )
    return parser.parse_args(input_args)


def read_input_file(input_file_path: str) -> List[InputSNP]:
    logging.info("Start read input data")
    with open(input_file_path) as tsv_file:
        input_data = [
            InputSNP(item[0], int(item[1]), item[2], item[3], item[4])
            for item in csv.reader(tsv_file, delimiter="\t")
        ]
    logging.info("End read input data")
    return input_data


def read_reference(
    input_data: List[InputSNP], reference_path: str
) -> Dict[str, Fastafile]:
    logging.info("Start work with reference")
    logging.info("Start check reference files")
    chr_names = [
        chr_name
        for chr_name in set([item.chr for item in input_data])
        if Path(reference_path + chr_name + ".fa").exists()
    ]
    logging.info("End check reference files")
    logging.info("Start read reference chromosome files")
    read_fasta_files = dict(
        [
            (chr_name, Fastafile(reference_path + chr_name + ".fa"))
            for chr_name in chr_names
        ]
    )
    logging.info("End read reference chromosome files")
    logging.info("End work with reference")
    return read_fasta_files


def find_ref(read_fasta_files: Dict[str, Fastafile], snp: InputSNP):
    logging.info(f"Find ref for {snp.chr}:{snp.position}")
    if snp.chr in read_fasta_files:
        try:
            return read_fasta_files[snp.chr].fetch(
                snp.chr, snp.position, snp.position + 1
            )
        except IndexError:
            logging.error(
                f"Ref ref for {snp.chr}:{snp.position} not found: out of range"
            )
            return "NOT_FOUND_OUT_OF_RANGE"
        except ValueError:
            logging.error(
                f"Ref ref for {snp.chr}:{snp.position} not found: region is invalid"
            )
            return "NOT_FOUND_REGION_IS_INVALID"
    else:
        logging.info(
            f"Ref ref for {snp.chr}:{snp.position} not fount (reference file isn't exist"
        )
        return "NOT_FOUND_REF"


def write_output(
    input_data: List[InputSNP],
    read_fasta_files: Dict[str, Fastafile],
    output_file_path: str,
):
    logging.info("Start generating output file")
    with open(output_file_path, "w") as tsv_file:
        for snp in input_data:
            ref = find_ref(read_fasta_files, snp)
            out_snp = OutputSNP(
                snp.chr, snp.position, snp.rsId, ref, snp.allele1 + "/" + snp.allele2
            )
            logging.info(f"Generate output for {str(snp)}")
            tsv_file.write(str(out_snp))
    logging.info("End generating output file")


def run(input_args):
    args = parse_args(input_args)
    input_data = read_input_file(args.input_file_path)
    read_fasta_files = read_reference(input_data, args.reference_path)
    write_output(input_data, read_fasta_files, args.output_file_path)


if __name__ == "__main__":
    run(sys.argv[1:])
