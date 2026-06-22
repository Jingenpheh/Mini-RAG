# Entry point for `python -m tools.ingest`. The actual CLI lives in
# orchestrator.main(); this file exists so the package can be invoked directly.

from tools.ingest.orchestrator import main


if __name__ == "__main__":
    main()
