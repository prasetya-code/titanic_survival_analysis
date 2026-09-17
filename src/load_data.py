from pathlib import Path
import zipfile
import subprocess

# root dir project ~
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# raw data dir
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def download_titanic_data():

    print("=" * 60)
    print("START: Download Titanic Dataset")
    print("=" * 60)

    try:
        # --------------------------------------------------
        # 1. Debug project location
        # --------------------------------------------------
        print(f"[DEBUG] PROJECT_ROOT : {PROJECT_ROOT}")
        print(f"[DEBUG] RAW_DATA_DIR : {RAW_DATA_DIR}")

        # --------------------------------------------------
        # 2. Create raw data directory
        # --------------------------------------------------
        print("[INFO] Creating raw data directory...")

        RAW_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"[DEBUG] Directory exists: {RAW_DATA_DIR.exists()}")

        # --------------------------------------------------
        # 3. Define ZIP path
        # --------------------------------------------------
        zip_path = RAW_DATA_DIR / "titanic.zip"

        print(f"[DEBUG] Expected ZIP path: {zip_path}")

        # --------------------------------------------------
        # 4. Kaggle authentication
        # --------------------------------------------------
        """
        Kaggle authentication:

        Login:
            kaggle auth login

        Check access token:
            kaggle auth print-access-token

        Logout / revoke:
            kaggle auth revoke
        """

        # --------------------------------------------------
        # 5. Build Kaggle command
        # --------------------------------------------------
        command = [
            "kaggle",
            "competitions",
            "download",
            "-c",
            "titanic",
            "-p",
            str(RAW_DATA_DIR)
        ]

        print("[DEBUG] Kaggle command:")
        print(" ".join(command),)

        # --------------------------------------------------
        # 6. Download dataset
        # --------------------------------------------------
        print("[INFO] Downloading Titanic dataset from Kaggle...")

        subprocess.run(
            command,
            check=True
        )

        print("[SUCCESS] Kaggle download completed.")

        # --------------------------------------------------
        # 7. Check ZIP file
        # --------------------------------------------------
        if not zip_path.exists():

            raise FileNotFoundError(
                f"Titanic ZIP file not found: {zip_path}"
            )

        print(f"[SUCCESS] ZIP file found: {zip_path}")
        print(f"[DEBUG] ZIP size: {zip_path.stat().st_size} bytes")

        # --------------------------------------------------
        # 8. Extract ZIP
        # --------------------------------------------------
        print("[INFO] Extracting Titanic dataset...")

        with zipfile.ZipFile(file = zip_path, mode = "r") as zip_ref:

            print("[DEBUG] Files inside ZIP:")

            for file_name in zip_ref.namelist():
                print(f"\t - {file_name}")

            zip_ref.extractall(RAW_DATA_DIR)

        print("[SUCCESS] Dataset extraction completed.")

        # --------------------------------------------------
        # 9. Keep ZIP file
        # --------------------------------------------------
        print("[INFO] ZIP file is kept.")
        print(f"[DEBUG] ZIP location: {zip_path}")

        # --------------------------------------------------
        # 10. Show resulting files
        # --------------------------------------------------
        print("[INFO] Files in raw data directory:")

        for file_path in RAW_DATA_DIR.iterdir():
            print(f"    - {file_path.name}")

        print("=" * 60)
        print("SUCCESS: Titanic dataset is ready.")
        print("=" * 60)

    except subprocess.CalledProcessError as error:

        print("=" * 60)
        print("[ERROR] Kaggle command failed.")
        print("=" * 60)

        print(f"[ERROR] Return code : {error.returncode}")
        print(f"[ERROR] Command     : {error.cmd}")

        print()
        print("[INFO] Make sure you have authenticated with:")
        print("       kaggle auth login")

        raise

    except FileNotFoundError as error:

        print("=" * 60)
        print("[ERROR] File or directory not found.")
        print("=" * 60)

        print(f"[ERROR] {error}")

        raise

    except zipfile.BadZipFile as error:

        print("=" * 60)
        print("[ERROR] Invalid or corrupted ZIP file.")
        print("=" * 60)

        print(f"[ERROR] {error}")

        raise

    except Exception as error:

        print("=" * 60)
        print("[ERROR] Unexpected error.")
        print("=" * 60)

        print(f"[ERROR TYPE] {type(error).__name__}")
        print(f"[ERROR] {error}")

        raise

    finally:

        print("=" * 60)
        print("END: Download Titanic Dataset")
        print("=" * 60)


if __name__ == "__main__":
    download_titanic_data()
