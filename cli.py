"""
This file contains the pipeline for the ChatDoc project, accessible via the command line.

Example usage:
$ python pipe.py generate --dataset icd --output_path ./data
$ python pipe.py train --dataset pmc --base_model t5-base --output_path ./model
"""

import argparse

from chat_doc.app.app import App
from chat_doc.config import logger
from chat_doc.dataset_generation.dataset_factory import DatasetFactory
from chat_doc.training.train import Trainer

if __name__ == "__main__":
    logger.info("Pipe ready")

    parser = argparse.ArgumentParser(description="ChatDoc pipeline")

    # Subparsers for "generate" and "train" commands
    subparsers = parser.add_subparsers(dest="command")

    # "generate" subcommand
    generate_parser = subparsers.add_parser("generate", help="Generate data")
    generate_parser.add_argument(
        "--dataset",
        choices=["pmc", "icd", "diagnose", "med-dialogue", "dialogue-full", "full"],
        required=True,
        help="Dataset to generate",
    )
    # generate_parser.add_argument(
    #     "--output_path", default="./data", help="Output path (default: ./data)"
    # )

    # "train" subcommand
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument(
        "--dataset",
        choices=["pmc", "icd", "diagnose", "med-dialogue", "dialogue-full", "full"],
        required=True,
        help="Dataset to train on",
    )
    train_parser.add_argument(
        "--base_model",
        default="meta-llama/Llama-2-7b-hf",
        help="Base model (default: Llama-2-7b-hf)",
    )
    train_parser.add_argument(
        "--output_path", default="./model", help="Output path (default: ./model)"
    )
    # setting default to None here so that we can check if the user has set the hyperparameter + defaults are set in train.py
    train_parser.add_argument(
        "--epoch", type=int, help="Number of epochs (default: 3)", default=None
    )
    train_parser.add_argument(
        "--lr", type=float, help="Learning rate (default: 2e-4)", default=None
    )
    train_parser.add_argument(
        "--batch_size", type=int, help="Batch size (default: 2)", default=None
    )

    # "run-app" subcommand
    generate_parser = subparsers.add_parser("run-app", help="Run web-app")
    generate_parser.add_argument("--port", default=5000, help="Port for the flask app")
    generate_parser.add_argument(
        "--debug", default=True, type=bool, help="Log-level for the flask app"
    )

    args = parser.parse_args()

    if args.command == "generate":
        logger.info(f"Generating data for dataset: {args.dataset}")
        # logger.info(f"Output path: {args.output_path}")

        datasetFactory = DatasetFactory()
        datasetFactory.build_dataset(name=args.dataset)

        logger.info(f"{args.dataset} data generated.")

    elif args.command == "train":
        logger.info(f"Training model on dataset: {args.dataset}")
        logger.info(f"Base model: {args.base_model}")
        logger.info(f"Output path: {args.output_path}")

        hyperparams = {}
        if args.epoch is not None:
            hyperparams["epochs"] = args.epoch

        if args.lr is not None:
            hyperparams["lr"] = args.lr

        if args.batch_size is not None:
            hyperparams["per_device_train_batch_size"] = args.batch_size

        trainer = Trainer(args.dataset, args.base_model, args.output_path, hyperparams)
        trainer.train()

    elif args.command == "run-app":
        app = App()
        app.run(port=args.port, debug=args.debug)
    else:
        logger.error("Invalid command. Use 'generate' or 'train'.")

    args = parser.parse_args()
