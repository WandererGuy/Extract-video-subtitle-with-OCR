import subprocess

while True:
    try:
        result = subprocess.run(
            ['python', '7_create_vietocr_dataset_p4.py'],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Success:", result.stdout)
        break   # exit the loop on success
    except subprocess.CalledProcessError as e:
        print("❌ Failed with exit code", e.returncode)
        print("stdout:\n", e.stdout)
        print("stderr:\n", e.stderr)
        # decide what to do next: retry, sleep, or abort
