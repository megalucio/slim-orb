# Orb Source

This directory contains the source for the `slim-orb`, which slims Docker images and generates security profiles (such as AppArmor and seccomp) using [SlimToolkit](https://github.com/slimtoolkit/slim).

Orbs are shipped as individual `orb.yml` files, but for easier development, you can author an orb in _unpacked_ form and _pack_ it with the CircleCI CLI for publishing.

The default `.circleci/config.yml` is set up to automatically pack, test, and deploy changes made to the orb source in this directory.

## @orb.yml

This is the entry point for the orb "tree", which becomes the `orb.yml` file after packing.

**Main configuration keys:**

1. **version**  
    Use version 1.0.1 for orb-compatible configuration: `version: 1.0.1`
2. **description**  
    Describes the orb and its functionality. Displayed in the CLI and orb registry.
3. **display**  
    Set the `home_url` for documentation or product info, and `source_url` for the orb's source repository.
4. **orbs**  
    (Optional) Import dependencies here if your orb uses other orbs.

## Current Status

- The orb uses the containerized version of SlimToolkit (`dslim/slim`) to slim Docker images and generate security profiles.
- Example usage and commands are provided in the `src/examples` and `src/commands` directories.
- The orb is ready for packing and publishing with the CircleCI CLI.

## See:
 - [Orb Author Intro](https://circleci.com/docs/2.0/orb-author-intro/#section=configuration)
 - [Reusable Configuration](https://circleci.com/docs/2.0/reusing-config)
 - [SlimToolkit Documentation](https://github.com/slimtoolkit/slim)
