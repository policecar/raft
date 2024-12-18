"""
This module contains the main CLI functionality for the RAFT project.
"""

import argparse
import sys


def action_doc() -> str:
    """
    Return a string describing available actions for the CLI.

    Returns:
        str: Description of available actions.
    """
    return """
The following actions are available:

- fetch: Fetch the blog from Substack and store it in the data directory.
- chunk: Chunk the blog into 4096 token pieces and store them in /data.
- embed: Create embeddings for the chunks and store them.
- ft:gen: Generate finetune files for the blog.
- ft:run: Run the finetune job for the blog.
- bench:setup: Setup the benchmark for the blog.
- ask: Ask a question about the blog content.
"""


cmds = ["fetch", "chunk", "embed", "ft:gen", "ft:run", "bench:setup", "ask"]


def main() -> None:
    """
    Main function to handle CLI arguments and execute corresponding actions.
    """
    parser = argparse.ArgumentParser(
        description="Run the raft command.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=action_doc(),
    )
    parser.add_argument(
        "action",
        help="The action to perform; see below for details.",
        choices=cmds,
    )

    parser.add_argument("name", help="The name of the blog to process.")
    parser.add_argument(
        "--oai",
        help="Only generate finetune or benchmark for openai \
            (from existing generic file).",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--generic",
        help="Only generate generic finetune or benchmark file.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--question",
        help="The question to ask about the blog content.",
        default=None,
    )
    parser.add_argument(
        "--no-useful-check",
        action="store_true",
        help="Skip usefulness check when summarizing memories",
    )

    args = parser.parse_args()

    try:
        if args.action == "fetch":
            from raft import substack_embeddings

            substack_embeddings.main(args.name)
        elif args.action == "chunk":
            from raft import files_helper

            files_helper.chunker(args.name)
        elif args.action == "embed":
            from raft import embeddings_helpers

            embeddings_helpers.store_grounding_embeddings(args.name)
        elif args.action == "ft:gen":
            if args.oai:
                from raft import oai_finetune

                oai_finetune.create_openai_finetune_file(args.name)
            elif args.generic:
                from raft import generate_finetune

                generate_finetune.generate_finetune(args.name)
            else:
                from raft import generate_finetune

                generate_finetune.generate_finetune(args.name)
                oai_finetune.create_openai_finetune_file(args.name)
        elif args.action == "ft:run":
            from raft import oai_finetune

            oai_finetune.run_oai_finetune(args.name)
        elif args.action == "bench:setup":
            if args.oai:
                from raft import oai_finetune

                oai_finetune.create_openai_finetune_file(args.name, "benchmark")
            elif args.generic:
                from raft import generate_finetune

                generate_finetune.generate_finetune(args.name)
            else:
                from raft import generate_finetune

                generate_finetune.generate_benchmark(args.name)
                oai_finetune.create_openai_finetune_file(args.name, "benchmark")
        elif args.action == "ask":
            if args.question is None:
                print("Please provide a question using the --question argument.")
            else:
                from raft import memories

                memory_manager = memories.MemoryManager(
                    args.name, {}
                )  # Empty metadata for now
                answer = memory_manager.ask_question(args.question)
                print(f"Answer: {answer}")
        else:
            print(f"Unknown action: {args.action}")
    except ImportError as e:
        print(f"Error: Could not load required module for '{args.action}' action: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
