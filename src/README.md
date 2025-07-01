# slim-orb

A CircleCI orb to slim one or more Docker images using [SlimToolkit](https://github.com/slimtoolkit/slim) and generate security profiles.

---

## Usage

Add this orb to your `.circleci/config.yml`:

```yaml
orbs:
  slim-orb: your-namespace/slim-orb@x.y.z
```

### Example Workflow

```yaml
workflows:
  version: 2
  use-slim-orb:
    jobs:
      - slim-orb/slim:
          images: "nginx,alpine"
          tag: latest
          repo: ""                              # Optional: e.g. "myrepo/"
          output_tag: slim.latest               # Optional: e.g. "slim" or "slim.latest"
          setup_docker: true                    # Optional: set to true to use remote Docker
          build_options: "--http-probe=false"   # Optional: additional SlimToolkit build options
          global_options: ""                    # Optional: additional global SlimToolkit options
          push_images: false                    # Optional: set to true to push images after build
```

---

## Parameters

| Name           | Type     | Default | Description                                                                                  |
|----------------|----------|---------|----------------------------------------------------------------------------------------------|
| images         | string   |         | **Required.** Comma-separated list of image names (e.g. "nginx,alpine")                      |
| tag            | string   |         | **Required.** Tag to use for all input images                                                |
| repo           | string   | ""      | Optional repo to prepend to each image name (e.g. "myrepo/")                                 |
| output_tag     | string   | ""      | Tag to use for all output images (e.g. "slim" will produce nginx:slim). If not set, uses "slim.<tag>" |
| setup_docker   | boolean  | false   | Whether to set up remote Docker for image processing                                         |
| build_options  | string   | ""      | Additional SlimToolkit build command options ([docs](https://github.com/slimtoolkit/slim?tab=readme-ov-file#build-command-options)) |
| global_options | string   | ""      | Additional global options for the SlimToolkit command ([docs](https://github.com/slimtoolkit/slim?tab=readme-ov-file#usage-details)) |
| push_images    | boolean  | false   | Whether to push the resulting images to the remote registry after building                   |

---

## Advanced: Using Environment Variables

You can also pass parameters using environment variables. The orb will use the parameter value if set, otherwise it will fall back to the environment variable.

Example:

```yaml
jobs:
  build:
    docker:
      - image: cimg/base:stable
    environment:
      SLIM_ORB_IMAGES: "nginx,alpine"
      SLIM_ORB_TAG: "latest"
    steps:
      - slim-orb/slim:
          images: "" # Will use SLIM_ORB_IMAGES if this is empty
          tag: ""    # Will use SLIM_ORB_TAG if this is empty
```

---

## Outputs

- Slimmed Docker images are tagged and optionally pushed to your registry.
- Security profiles (AppArmor, Seccomp) are saved in the `workspace` directory.

---

## References

- [SlimToolkit Documentation](https://github.com/slimtoolkit/slim)
- [CircleCI Orbs Documentation](https://circleci.com/docs/orb-intro/)
- [Orb in the CircleCI Registry](https://circleci.com/developer/orbs/orb/megalucio/slim-orb)

---

## License

MIT