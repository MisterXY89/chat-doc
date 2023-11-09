"""
This file contains the pipeline for the ChatDoc project, accessible via the command line.

Example usage:
$ python pipe.py generate --dataset icd --output_path ./data
$ python pipe.py train --dataset pmc --base_model t5-base --output_path ./model
"""

import argparse

from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory

if __name__ == "__main__":
    logger.info("Pipe ready")

    parser = argparse.ArgumentParser(description="ChatDoc pipeline")

    # Subparsers for "generate" and "train" commands
    subparsers = parser.add_subparsers(dest="command")

    # "generate" subcommand
    generate_parser = subparsers.add_parser("generate", help="Generate data")
    generate_parser.add_argument(
        "--dataset", choices=["pmc", "icd", "full"], required=True, help="Dataset to generate"
    )
    generate_parser.add_argument(
        "--output_path", default="./data", help="Output path (default: ./data)"
    )

    # "train" subcommand
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument(
        "--dataset", choices=["pmc", "icd", "full"], required=True, help="Dataset to train on"
    )
    train_parser.add_argument(
        "--base_model", default="t5-base", help="Base model (default: t5-base)"
    )
    train_parser.add_argument(
        "--output_path", default="./model", help="Output path (default: ./model)"
    )

    args = parser.parse_args()

    if args.command == "generate":
        logger.info(f"Generating data for dataset: {args.dataset}")
        logger.info(f"Output path: {args.output_path}")

        datasetFactory = DatasetFactory()
        datasetFactory.build_dataset(name=args.dataset, output_path=args.output_path)

        logger.info(f"{args.dataset} data generated.")

    elif args.command == "train":
        logger.info(f"Training model on dataset: {args.dataset}")
        logger.info(f"Base model: {args.base_model}")
        logger.info(f"Output path: {args.output_path}")
        # Add your train code here
    else:
        logger.error("Invalid command. Use 'generate' or 'train'.")

    args = parser.parse_args()
