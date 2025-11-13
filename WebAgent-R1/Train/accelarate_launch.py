from accelerate import Accelerator

if __name__ == "__main__":
    accelerator = Accelerator()  # this reads your default or config YAML
    accelerator.print(f"Using devices: {accelerator.num_processes}")
    # import the rest of your training setup here
    from verifiers.script import main
    main()

