import datetime
import shutil
import os

class Dashboard:

    def __init__(self):
        # self.date = self.time_get()
        # self.system_status = self.get_system_stats()
        pass

    def get_all_data(self) -> dict:
        # Kombiniert Zeit und Hardware in ein einziges JSON-Objekt
        return {
            "time": self.time_get(),
            **self.get_system_stats()
        }

    def time_get(self) -> str:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return time
    
    def get_system_stats(self) -> dict:
        stats = {
            "cpu_temp": "N/A",
            "cpu_load": "N/A",
            "disk_free": "N/A",
            "ram_info": "N/A"
        }

        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                stats["cpu_temp"] = f"{float(f.read()) / 1000.0:.1f} °C"
        except: pass

        try:
            with open("/proc/loadavg", "r") as f:
                stats["cpu_load"] = f.read().split()[0]
        except: pass

        try:
            _, _, free = shutil.disk_usage("/")
            stats["disk_free"] = f"{free / (1024**3):.1f} GB"
        except: pass

        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                free = int(lines[1].split()[1])
                used_pct = ((total - free) / total) * 100
                stats["ram_info"] = f"{used_pct:.1f} %"
        except: pass

        return stats

class Folder:
    def __init__(self, f_type):
        self.path = self.path_init(f_type)

    def path_init(self, f_type) -> str:
        base_path = "~/"
        match f_type:
            case "src":
                return os.path.expanduser(base_path + "src")
            
    def prew(self, max_range = 10) -> list:
        #format = {"name": "filename", "path": "full_path", "modified": "timestamp"}
        try:
            return_list = []
            #listcomprehension
            entries = [
                os.path.join(self.path, f)
                for f in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, f))
            ]
            entries.sort(key=os.path.getmtime, reverse=True)
            latest_entries = entries[:max_range]
            for f in latest_entries:
                mtime = os.path.getmtime(f)
                return_list.append({
                    "name": os.path.basename(f),
                    "path": f,
                    "modified": mtime
                    })
            
            return return_list
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def show_whole_dir(self) -> list:
        #format = {upper_dir : [{"name": "filename", "path": "full_path", "modified": "timestamp"}, ...]}
        try:
            result = {}
            for root, dirs, files in os.walk(self.path):
                file_list = []
                for f in files:
                    full_path = os.path.join(root, f)
                    file_list.append({
                        "name": f,
                        "path": full_path,
                        "modified": os.path.getmtime(full_path)
                    })
                if file_list:  # nur eintragen, wenn Ordner auch Dateien hat
                    result[root] = file_list
            return result
        except Exception as e:
            return [f"Error: {str(e)}"]