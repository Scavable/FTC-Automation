import os
import shutil
from os.path import exists

import nbtlib
import tkinter as tk


class DragonReset:
    def __init__(self, instance):
        if exists(instance + "/Minecraft/world/level.dat_old"):
            print("level.dat_old File Exists")
            os.remove(instance + "/Minecraft/world/level.dat_old")
            print("level.dat_old deleted")
        else:
            print("level.dat_old does not exist")

        if exists(instance + "/Minecraft/world/level.dat"):
            print("level.dat File Exists")
            shutil.copy(instance + "/Minecraft/world/level.dat", instance + "/Minecraft/world/level.dat.bak")
            nbt_file = nbtlib.load(instance + "/Minecraft/world/level.dat")

            if nbt_file['Data'].keys().__contains__("DragonFight"):
                print("Dragon fight folder exists")
                nbt_file['Data'].pop("DragonFight")
                nbt_file.save()
                print("Dragon fight folder deleted")
            else:
                print("Dragon fight folder does not exist")
        else:
            print("level.dat does not exist")

    @staticmethod
    def create_new_window(root):
        new_window = tk.Toplevel(root)
        root.update()
        new_window.geometry('%dx%d+%d+%d' % (gui.w/2, gui.h/2, gui.x, gui.y))
        return new_window