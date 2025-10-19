import os
import csv
import subprocess
import xml.etree.ElementTree as ET
import json
import plistlib
import re
import glob

projs={
    "libsndfile": "repos_cpp/libsndfile",
    "libgit2": "repos_cpp/libgit2",
    "nghttp2": "repos_cpp/nghttp2"
}

results_dir= "results_cpp"
final= os.path.join(results_dir, "consolidated_cpp.csv")

CWE_TOP_25= {
    "CWE-787", "CWE-79", "CWE-89", "CWE-20", "CWE-125", "CWE-78",
    "CWE-416", "CWE-22", "CWE-352", "CWE-434", "CWE-476", "CWE-502",
    "CWE-269", "CWE-94", "CWE-863", "CWE-77", "CWE-306", "CWE-362",
    "CWE-798", "CWE-918", "CWE-400", "CWE-611", "CWE-502", "CWE-284", "CWE-295"
}

def run_cmd_capture(cmd):
    #runs a shell command and captures stdout/stderr
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def export_json(path, findings):
    #exports a list of dicts to JSON
    with open(path, "w") as f:
        json.dump(findings, f, indent=2)

def export_csv(path, findings):
    #exports a list of dicts to CSV
    if not findings:
        return
    keys = findings[0].keys()
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(findings)


#Flawfinder
def run_flawfinder(proj_path, proj_name, out_format="csv"):
    print(f"🔍 Running Flawfinder on {proj_name}")
    os.makedirs(results_dir, exist_ok=True)
    out_file = os.path.join(results_dir, f"{proj_name}_flawfinder.{out_format}")

    if out_format == "csv":
        cmd = ["flawfinder", "--csv", proj_path]
        stdout, stderr, rc = run_cmd_capture(cmd)
        if rc != 0:
            print(f"[!] Flawfinder failed: {stderr}")
            return []
        with open(out_file, "w") as f:
            f.write(stdout)
        return out_file  
    elif out_format == "json":
        cmd = ["flawfinder", "--columns", proj_path]
        stdout, stderr, rc = run_cmd_capture(cmd)
        findings = []
        for line in stdout.splitlines():
            if "CWE-" in line:
                idx = line.find("CWE-")
                cwe_id = line[idx:idx+7]
                findings.append({
                    "Project_name": proj_name,
                    "Tool_name": "Flawfinder",
                    "CWE_ID": cwe_id,
                    "Is_In_CWE_Top_25": "Yes" if cwe_id in CWE_TOP_25 else "No"
                })
        export_json(out_file, findings)
        return out_file


#Cppcheck
def run_cppcheck(proj_path, proj_name, out_format="xml"):
    print(f"🔎 Running Cppcheck on {proj_name}")
    os.makedirs(results_dir, exist_ok=True)
    out_file = os.path.join(results_dir, f"{proj_name}_cppcheck.{out_format}")

    cmd = ["cppcheck", "--xml", "--enable=all", "--inconclusive", "--quiet", proj_path]
    stdout, stderr, rc = run_cmd_capture(cmd)
    if rc != 0:
        print(f"[!] Cppcheck failed: {stderr}")
    with open(out_file, "w") as f:
        f.write(stderr)

    if out_format == "json":
        findings = []
        try:
            root = ET.fromstring(stderr)
            for error in root.iter("error"):
                cwe = error.attrib.get("cwe")
                if cwe:
                    cwe_id = f"CWE-{cwe}"
                    findings.append({
                        "Project_name": proj_name,
                        "Tool_name": "Cppcheck",
                        "CWE_ID": cwe_id,
                        "Is_In_CWE_Top_25": "Yes" if cwe_id in CWE_TOP_25 else "No"
                    })
            export_json(out_file, findings)
        except ET.ParseError:
            print(f"[!] Failed to parse Cppcheck XML for {proj_name}")

    return out_file

def run_scanbuild(proj_path, proj_name, out_format="json"):
    print(f"Running scan-build on {proj_name}")
    os.makedirs(results_dir, exist_ok=True)
    report_dir = os.path.join(results_dir, f"{proj_name}_scanbuild_report")
    out_file = os.path.join(results_dir, f"{proj_name}_scanbuild.{out_format}")

    #the -C flag tells make to change to the project directory before running so that the execution context remains clean
    cmd = ["scan-build", "-o", report_dir, "make", "-C", proj_path, "-j4"]
    stdout, stderr, rc = run_cmd_capture(cmd)

    if "scan-build: No bugs found." in stderr or "scan-build: No bugs found." in stdout:
        print(f"  [+] scan-build found no bugs in {proj_name}.")
        export_json(out_file, [])
        return out_file

    if rc != 0 and not glob.glob(os.path.join(report_dir, "**", "*.plist"), recursive=True):
         print(f"[!] scan-build failed for {proj_name}. Return code: {rc}")
         print(f"    STDOUT: {stdout.strip()}")
         print(f"    STDERR: {stderr.strip()}")
         return None

    print(f"  Parsing scan-build results for {proj_name}...")
    findings = []
    # scan-build creates a timestamped subdirectory, so we search recursively for plist files.
    plist_files = glob.glob(os.path.join(report_dir, "**", "*.plist"), recursive=True)

    for plist_file in plist_files:
        try:
            with open(plist_file, 'rb') as f:
                data = plistlib.load(f)
            for diag in data.get('diagnostics', []):
                description = diag.get('description', '')
                # Search for a CWE ID in the description text
                match = re.search(r'CWE-\d+', description)
                if match:
                    cwe_id = match.group(0)
                    findings.append({
                        "Project_name": proj_name,
                        "Tool_name": "scan-build",
                        "CWE_ID": cwe_id,
                        "Is_In_CWE_Top_25": "Yes" if cwe_id in CWE_TOP_25 else "No"
                    })
        except Exception as e:
            print(f"[!] Error parsing plist file {plist_file}: {e}")

    if out_format == "json":
        export_json(out_file, findings)

    return out_file

if __name__ == "__main__":
    if os.path.exists(final):
        os.remove(final)

    for proj in projs:
        proj_path = projs[proj]
        run_flawfinder(proj_path, proj, out_format="csv")   
        run_cppcheck(proj_path, proj, out_format="xml")    
        run_scanbuild(proj_path, proj, out_format="json")

    print(f"All analyses complete! Structured outputs saved in {results_dir}")
