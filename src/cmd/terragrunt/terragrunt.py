import os
import glob
import json
import logging
import subprocess
from pathlib import Path

class TerragruntUtils(object):
    def __init__(self):
        pass

    def gather_directories(self, terragrunt_root_addr="tests/haydar-terragrunt/"):
        pathname = terragrunt_root_addr + "/**/terragrunt.hcl"
        modules = glob.glob(pathname, recursive=True)

        return modules


class Terragrunt(object):
    def __init__(self):
        self.utils = TerragruntUtils()
        self.modules = []

    def fetch_list_of_state_files(self, terragrunt_root_addr="tests/haydar-terragrunt/"): ## function to fetch state files from remote address
        self.modules = self.utils.gather_directories(terragrunt_root_addr)

        for module in self.modules:
            directory = module.replace("terragrunt.hcl", "")
            try:
                os.makedirs("/tmp/states/{}".format(directory), exist_ok=True)
                subprocess.run("terragrunt state pull --terragrunt-working-dir {} > /tmp/states/{}tg.tfstate".format(directory, directory), shell=True, check=True)
            except Exception as exp:
                logging.warning(exp)

    def state_checker(self): ## that is responsible to fetch states from the remote address
        
        for module in self.modules:
            directory = module.replace("terragrunt.hcl", "")
            try:

                subprocess.run("terragrunt refresh --terragrunt-working-dir {}".format(directory, directory), shell=True, check=True)
                subprocess.run("terragrunt plan --terragrunt-working-dir {} > /tmp/states/{}plan_output ".format(directory, directory), shell=True, check=True)

            except Exception as exp:
                logging.warning(exp)

    def aggregator(self): ## aggregate plan output with issue templates
        for module in self.modules:
            directory = module.replace("terragrunt.hcl", "")
            plan_output = "/tmp/states/{}plan_output".format(directory)
            plan_map = {}
            try:
                contents = Path(plan_output).read_text()
                plan_map[module] = contents
            except Exception as exp:
                logging.warning(exp)




obj = Terragrunt()
obj.fetch_list_of_state_files()
#obj.state_checker()
obj.aggregator()