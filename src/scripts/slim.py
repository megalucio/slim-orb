import os
import re
import subprocess
import sys

def sanitize_and_validate(images, tag, repo, output_tag, build_options, global_options):
    # Split and trim images
    images_list = [img.strip() for img in images.split(',') if img.strip()]
    # Validate images: allow only alphanum, -, _, /, and .
    for image in images_list:
        if not re.match(r'^[a-zA-Z0-9._/-]+$', image):
            print(f"Invalid image name: {image}")
            sys.exit(1)
    # Validate tag and output_tag: allow only alphanum, -, _, and .
    if not re.match(r'^[a-zA-Z0-9._-]+$', tag):
        print(f"Invalid tag: {tag}")
        sys.exit(1)
    if output_tag and not re.match(r'^[a-zA-Z0-9._-]+$', output_tag):
        print(f"Invalid output tag: {output_tag}")
        sys.exit(1)
    # Validate build_options and global_options: reject dangerous shell metacharacters
    for opt, name in [(build_options, "build_options"), (global_options, "global_options")]:
        if re.search(r'[;&|`$()]', opt):
            print(f"Invalid {name}: contains potentially dangerous characters.")
            sys.exit(1)
    return images_list

def main():
    # These would be replaced by your parameter injection logic
    images = os.environ.get("IMAGES", "")
    tag = os.environ.get("TAG", "")
    repo = os.environ.get("REPO", "")
    output_tag = os.environ.get("OUTPUT_TAG", "")
    build_options = os.environ.get("BUILD_OPTIONS", "")
    global_options = os.environ.get("GLOBAL_OPTIONS", "")
    push_images = os.environ.get("PUSH_IMAGES", "false").lower() == "true"

    images_list = sanitize_and_validate(images, tag, repo, output_tag, build_options, global_options)

    os.makedirs("workspace", exist_ok=True)
    
    for image in images_list:
        full_image = f"{repo}{image}"
        input_image = f"{full_image}:{tag}"
        if not output_tag:
            output_image = f"{full_image}:slim.{tag}"
        else:
            output_image = f"{full_image}:{output_tag}"
        cmd = ["slim"]
        if global_options:
            cmd.extend(global_options.split())
        cmd.extend([
            "build", 
            "--target", input_image, "--tag", output_image, 
            "--copy-meta-artifacts", "."
        ])
        if build_options:
            cmd.extend(build_options.split())
        subprocess.run(cmd, check=True)
        img_name = image.split('/', 1)[-1].split(':', 1)[0]
        for profile in [f"{img_name}-apparmor-profile", f"{img_name}-seccomp.json"]:
            if os.path.isfile(profile):
                os.rename(profile, os.path.join("workspace", profile))
        # Optionally push image
        if push_images:
            subprocess.run(["docker", "push", output_image], check=True)

if __name__ == "__main__":
    main()
