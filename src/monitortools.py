import platform
import subprocess
import re
import os


class MonitorTools:
    def __init__(self):
        self.system = platform.system()

    def get_settings(self):
        if self.system == "Windows":
            return self._get_windows_settings()
        elif self.system == "Linux":
            return self._get_linux_settings()
        else:
            raise NotImplementedError("Unsupported OS")

    def set_settings(self, resolution=None, refresh_rate=None):
        if resolution and refresh_rate:
            if self.system == "Windows":
                return self._set_windows_settings(resolution, refresh_rate)
            elif self.system == "Linux":
                return self._set_linux_settings(resolution, refresh_rate)
            else:
                raise NotImplementedError("Unsupported OS")

    # Windows methods
    def _get_windows_settings(self):
        try:
            # Use dxdiag to get display info
            dxinfo_file = "dxinfo.txt"
            subprocess.run(f"dxdiag /t {dxinfo_file}", shell=True, check=True)
            with open(
                dxinfo_file, "r", encoding="Windows-1252" if os.name == "nt" else "utf-8"
            ) as f:
                content = f.read()
            
            os.remove(dxinfo_file)
            match = re.search(r"Current Mode:\s*(\d+\s*x\s*\d+) \(.*?\) \((\d+)Hz\)", content)
            if match:
                resolution = match.group(1)
                refresh_rate = match.group(2)
                return {"resolution": resolution, "refresh_rate": refresh_rate}
            else:
                raise ValueError(
                    "dxdiag output does not contain resolution and refresh rate"
                )
        except Exception as dxdiag_error:
            try:
                output = subprocess.check_output(
                    "wmic path Win32_VideoController get VideoModeDescription",
                    shell=True,
                )
                output = output.decode(errors="ignore").splitlines()
                for line in output:
                    if "x" in line:
                        resolution = line.strip()
                        break
                return {
                    "resolution": resolution,
                    "refresh_rate": "Unknown (dxdiag failed: "
                    + str(dxdiag_error)
                    + ")",
                }
            except Exception as wmic_error:
                return {
                    "error": f"dxdiag failed: {dxdiag_error}, wmic fallback failed: {wmic_error}"
                }

    def _set_windows_settings(self, resolution=None, refresh_rate=None):
        # Requiores NirCmd: https://www.nirsoft.net/utils/nircmd.html
        try:
            if resolution:
                res = resolution.lower().split("x")
                color_depth = 32
                # cmd = f"nircmd.exe setdisplay monitor:0 {res[0]} {res[1]} {color_depth} {refresh_rate}" # syntax for multiple monitors
                cmd = f"nircmd.exe setdisplay {res[0]} {res[1]} {color_depth} {refresh_rate}"
                subprocess.run(cmd, shell=True, check=True)
            return {"status": "Applied using NirCmd"}
        except subprocess.CalledProcessError as e:
            return {"error": f"NirCmd failed: {e}"}

    # Linux methods
    def _get_linux_settings(self):
        try:
            output = subprocess.check_output("xrandr", shell=True).decode()
            match = re.search(r"(\d+x\d+)\s+(\d+\.\d+)\*", output)
            if match:
                resolution = match.group(1)
                refresh_rate = match.group(2)
                return {"resolution": resolution, "refresh_rate": refresh_rate}
            else:
                return {"error": "Could not parse xrandr output"}
        except Exception as e:
            return {"error": str(e)}

    def _get_linux_modes(self):
        try:
            output = subprocess.check_output("xrandr", shell=True).decode()
            modes = re.findall(r"(\d+x\d+)\s+(\d+\.\d+)", output)
            return [(res, rate.split(".")[0]) for res, rate in modes]
        except Exception as e:
            return []

    def _set_linux_settings(self, resolution=None, refresh_rate=None):
        try:
            cmd = "xrandr"
            output = subprocess.check_output(cmd, shell=True).decode()
            screen = re.search(
                r"^([a-zA-Z0-9-]+) connected", output, re.MULTILINE
            ).group(1)

            cmd = f"xrandr --output {screen}"
            if resolution:
                cmd += f" --mode {resolution}"
            if refresh_rate:
                cmd += f" --rate {refresh_rate}"

            subprocess.run(cmd, shell=True)
            return {"status": "Settings changed"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    mt = MonitorTools()
    print(mt.get_settings())
    mt.set_settings("2560x1440", "60")
    print(mt.get_settings())