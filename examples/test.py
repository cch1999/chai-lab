import argparse
from pathlib import Path
import random

import torch

from chai_lab.chai1 import run_inference

def parse_args():
    parser = argparse.ArgumentParser(description="Run inference on protein structures")
    parser.add_argument("--fasta_file", type=Path, default="/tmp/example.fasta", help="Path to input FASTA file")
    parser.add_argument("--output_dir", type=Path, default=Path("/home/cch57/projects/repos/chai-lab/examples/outputs"), help="Directory for output files")
    parser.add_argument("--num_trunk_recycles", type=int, default=3, help="Number of trunk recycles")
    parser.add_argument("--num_diffn_timesteps", type=int, default=200, help="Number of diffusion timesteps")
    parser.add_argument("--num_seeds", type=int, default=1, help="Number of random seeds to use")
    parser.add_argument("--device", type=str, default="cuda:0", help="Device to run on (e.g., 'cuda:0', 'cpu')")
    parser.add_argument("--use_esm_embeddings", action="store_true", help="Use ESM embeddings")
    return parser.parse_args()

def main():
    args = parse_args()

    # We use fasta-like format for inputs.
    # Every record may encode protein, ligand, RNA or DNA
    example_fasta = """
    >7M41_1|Chains A, B|Hepatitis A virus cellular receptor 2|Homo sapiens (9606)
    SEVEYRAEVGQNAYLPCFYTPAAPGNLVPVCWGKGACPVFECGNVVLRTDERDVNYWTSRYWLNGDFRKGDVSLTIENVTLADSGIYCCRIQIPGIMNDEKFNLKLVIK
    >ligand
    Cc1nn2C(=O)Nc3cc(Cl)c(cc3c2n1)c4ccc(N[S](=O)(=O)c5[nH]ccn5)cc4C
    >ligand|calcium-ion
    [Ca+2]
    """.strip()

    args.fasta_file.write_text(example_fasta)

    for i in range(args.num_seeds):
        seed = random.randint(0, 10000)

        args.output_dir = args.output_dir / f"seed_{seed}"
        args.output_dir.mkdir(parents=True, exist_ok=True)

        output_paths = run_inference(
            fasta_file=args.fasta_file,
            output_dir=args.output_dir,
            num_trunk_recycles=args.num_trunk_recycles,
            num_diffn_timesteps=args.num_diffn_timesteps,
            seed=seed,
            device=torch.device(args.device),
            use_esm_embeddings=args.use_esm_embeddings,
        )

        print(f"Run {i+1}/{args.num_seeds} - Seed: {seed}")
        print(f"Output files saved to: {output_paths}")

if __name__ == "__main__":
    main()
