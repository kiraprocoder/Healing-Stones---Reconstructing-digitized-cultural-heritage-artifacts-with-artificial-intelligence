import subprocess

# List of scripts in order
scripts = [
    "1_align.py",
    "2_arrange.py",
    "2.2_visualize.py",
    "3_descriptors.py",
    "4_match.py",
    "5_extract.py",
    "6_weighted_graphh.py",
    "7_v_graph.py",
    "8_align_matches.py",
    "9_train.py",
    "10_evaluation.py",
    "11_reconstruct.py"
]

def run_script(script_name):
    print(f"\n🛠️ Running {script_name} ...")
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Finished {script_name}")
        print(result.stdout)
    else:
        print(f"❌ Error in {script_name}")
        print(result.stderr)
        exit(1)

def main():
    print("🚀 Starting full pipeline for Mayan Stele reconstruction...\n")
    for script in scripts:
        run_script(script)
    print("\n🎉 All steps completed successfully!")

if __name__ == "__main__":
    main()
