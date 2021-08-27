import os
import sys
import csv
from natsort import natsorted

OPTIONS = {
  "BOOLEAN": {
    # "": "delete original files?",
    "prefex": "patch integer as prefex(y) or suffix(n)?",
    # "simple": "names use only subscript?"
    # "line_up": "include all the directory name up to the point?"
    # "extension": "reset subscript count by extension?"
  },
  "SELECTION": {
    # "sort": ("sort by?", ["name", "date"]),
    # "order": ("order is?",["asc", "desc"])
  },
  "STRING": {
    "joint": "what string to use for name connections?"
    # "iter": "what use for iterater? decimal(10)"
    # "ignore": "directory name or file name"
  }
}

class Directory:
  def __init__(self, path, mother=None):
    self.path = path
    self.mother = mother
    self.children = set()
    self.file_count = 0
    self.files = list()
    self.depth = self.calculate_depth()
    self.listup()
  
  def __str__(self):
    return os.path.basename(self.path)

  def calculate_depth(self):
    if self.mother is None:
      return 0
    else:
      tmp = self.mother.depth + 1
      return tmp

  def listup(self):
    for f in os.listdir(self.path):
      current_path = os.path.join(self.path, f)
      if os.path.isfile(current_path):
        self.file_count += 1
        # self.files.append[os.start(current_path)]
        continue
      if os.path.isdir(current_path):
        self.children.add(Directory(current_path, mother=self))
        continue
      raise ValueError("invarid path")

  def show(self):
    print("    " * self.depth, end="")
    print(self, end="")
    print("(" + str(self.file_count) + ")")

  def show_all(self):
    self.show()
    for child in self.children:
      child.show_all()

  def rename(self, prefex, joint):
    n = 0
    overlaps = set()
    for f in natsorted(os.listdir(self.path)):
      if f in overlaps:
        current_path = os.path.join(self.path, f+"_tmp")
      else:
        current_path = os.path.join(self.path, f)
      if os.path.isfile(current_path):
        # newname
        # self.give_name(zahl=n, flags=)
        new_name = str(n)
        if prefex:
          new_name = new_name + joint + str(self)
        else:
          new_name = str(self) + joint + new_name
        if f in overlaps:
          new_name = new_name.removesuffix("_tmp")
        new_path = os.path.join(self.path, new_name)
        if os.path.exists(new_path) and new_path != current_path:
          os.rename(new_path, new_path + "_tmp")
          overlaps.add(new_name)
        print("  ",end="")
        print(f, end=" ")
        print("->", end=" ")
        os.rename(current_path, new_path)
        print(new_name)
        if n > self.file_count:
          break
        n += 1
          
  def give_name(self, zahl, flags):
    name = str(zahl)
    if flags["prefex"]:
      name = name + flags["joint"] + str(self)
    else:
      name = str(self) + flags["joint"] + name
    return name
    
  def rename_all(self,prefex=False, joint=""):
    print(self.path)
    self.rename(prefex=prefex, joint=joint)
    for child in self.children:
      child.rename_all(prefex=prefex, joint=joint)
  
  


def main():
  if not len(sys.argv) in [1, 2, 3]:
    print("USAGE: python renamer.py [directory_path] [option.csv]")
    sys.exit(1)

  # identify directory name
  if len(sys.argv) == 1:
    while True:
      path = input("directory path: ")
      if os.path.isdir(path):
        break
      print("not exists")

  else:
    path = sys.argv[1]
  
  directory = Directory(path)
  directory.show_all()
  
  # read/ask option
  config_dir_path = os.path.join(os.path.dirname(__file__), "config")
  old_flags = dict()
  if len(sys.argv) >= 3:
    config_path = os.path.join(config_dir_path, sys.argv[2])
    if not os.path.exists(config_path):
      raise FileNotFoundError("invalid config file")
    with open(config_path, "r") as f:
      reader = csv.reader(f)
      for row in reader:
        if not row:
          continue
        old_flags[row[0]] = row[1]

  for q_type, q_dict in OPTIONS.items():
    for var, question in q_dict.items():
      if var in old_flags:
        flags[var] = satisfy_format(q_type, var, old_flags[var])
        if not flags[var] is None:
          continue
      if q_type == "BOOLEAN":
        flags[var] = ask_boolean(question)
        continue
      if q_type == "SELECTION":
        flags[var] = ask_selection(question)
        continue
      if q_type == "STRING":
        flags[var] = input(question + " (free): ")
        continue
      raise ValueError("This question type is not defined. \nPlease report this to developer.")

  directory.rename_all(flags["prefex"], flags["joint"])

  # save option
  if len(sys.argv) >= 3:
    new_flag_names = set(flags) - set(old_flags)
    if new_flag_names and ask_boolean("update(y) or make new file(n)?"):
      # update 
      with open(config_path, 'a') as f:
        w = csv.writer(f)
        for key in new_flag_names:
          w.writerow([key, flags[key]])
      print("success!!")

  else:
    if ask_boolean("save options?"):
    # fix config name
      while True:
        new_config_name = input("""filename? (ends with ".csv"): """)
        if not new_config_name.endswith(".csv"):
          print("""name must end with ".csv" """)
          continue
        new_config_path = os.path.join(config_dir_path, new_config_name)
        if os.path.exists(new_config_path):
          print("this name is already used")
          if ask_boolean("delete(and overwrite)?"):
            os.remove(new_config_path)
            break
          continue
        break
      # save
      with open(new_config_path, 'w') as f:
        w = csv.writer(f)
        print(flags)
        for key, value in flags.items():
          w.writerow([key, value])
      print("success!!")

def ask_boolean(question):
  while True:
    tmp = input(question + " (y/n): ").upper()
    if tmp in ["Y", "YES"]:
      return True
    if tmp in ["N", "NO"]:
      return False
    print("format: y/n")


def is_invalidname(self, str):
    for char in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
      if char in name:
        return False
    return True

def satisfy_format(q_type, var, ans):
# 一定の値を適切な形に変換して返す
# e.g.)"Yes" -> True
# 対応する形のない不正な値に対しては、Noneを返す
  if q_type == "STRING":
    return ans
  if q_type == "BOOLEAN":
    if ans.upper() in ["TRUE", "T", "YES", "Y"]:
      return True
    if ans.upper() in ["FALSE", "F", "NO", "N"]:
      return False
    return None
  if q_type == "SELECTION":
    if ans.upper() in OPTIONS[q_type][var][1]:
      return ans.upper
    return None
  raise ValueError("This question type is not defined. \nPlease report this to developer.")
  


if __name__ == "__main__":
  main()
