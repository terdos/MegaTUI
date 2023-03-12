#!/usr/bin/python
#encoding=utf-8

import traceback, os, sys, getopt
root_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, os.path.join(root_path, 'mylib'))
from snack import * #Import graphical interface
#from snack_lib import Mask
from config import config_first
from config import config_secondary
import inspect
import three_page
__version__ = "1.2.1"

def usage():
  print "<Instructions>"
  print "-h This help"
def warwindows(screen, title, text, help = None):
    #Warning window
    btn = Button("Sure")
    war = GridForm(screen, title, 20, 16)
    war.add(Label(text),0,1)
    war.add(Label(""),0,2)
    war.add(btn, 0, 3)
    war.runOnce(43,8)
class Menu_tool:
    def __init__(self):

        self.screen = SnackScreen()
        self.screen.setColor("ROOT", "white", "blue")
        self.screen.setColor("ENTRY","white","blue")
        self.screen.setColor("LABEL","black","white")
        self.screen.setColor("HELPLINE","white","blue")
        self.screen.setColor("TEXTBOX","black","yellow")
        self.screen.pushHelpLine("<%s> Powered by meetbill...Please use TAB to switch between options"%__version__)
        self.main_location = 1
        self.sec_location = 1

    def main(self):
      try:
        self.first_menu()
      except Exception,e:
        self.screen.finish()
        print e
        print traceback.format_exc()
      finally:
        self.screen.finish()
        print "Thank you！"
        return ''

    def QUIT(self):
    #Call the exit to the command line, enter the EXIT back
        buttons = ("yes", "no")
        bb = ButtonBar(self.screen, buttons)
        g = GridForm(self.screen, "Back to the login interface？" , 20,16)
        g.add(bb,1,3,(10,0,10,0), growx = 1)
        rq = g.runOnce(32,8)
        self.screen.popWindow()
        if rq == "ESC" or bb.buttonPressed(rq) == "no":
            self.first_menu()
        else:
            self.screen.finish()
            return

    def first_menu(self):
    #Main interface
        # Main MEMU menu item location
        while True:
            self.screen = SnackScreen()
            self.screen.finish()
            self.screen = SnackScreen()
            self.screen.setColor("ROOT", "white", "blue")
            self.screen.setColor("ENTRY","white","blue")
            self.screen.setColor("LABEL","black","white")
            self.screen.setColor("HELPLINE","white","blue")
            self.screen.setColor("TEXTBOX","black","yellow")
            self.screen.pushHelpLine("<%s> Powered by meetbill...Please use TAB to switch between options"%__version__)
            li = Listbox(height = 15, width = 18, returnExit = 1, showCursor = 0)

            items_n = 1
            for items in config_first["items"]:
                li.append(items, items_n)
                items_n += 1
            li.setCurrent(self.main_location)

            bb = CompactButton('|->quit<-|')
            g = GridForm(self.screen, "manager", 1, 10)
            g.add(li, 0, 1)
            g.add(bb, 0, 2)
            g.add(Label(" "),0,3)
            g.add(Label("[Managed weapon]"),0,4)
            rc=g.run(1,3)
            self.main_location = li.current()
            if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
                return self.QUIT()
            if li.current() in range(1,len(config_first["items"])+1):
                self.secondary_menu()

    # The second layer menu
    def secondary_menu(self):
        li = Listbox(height = 15, width = 14, returnExit = 1, showCursor = 0)
        n = 0
        bb = CompactButton('return')
        secondary_window = config_secondary[self.main_location - 1]
        items_n = 1
        for items in secondary_window["items"]:
            li.append(items[0], items_n)
            items_n += 1
        while True:
            h = GridForm(self.screen, "please choose", 1, 16)
            if len(secondary_window["items"]) < self.sec_location:
                li.setCurrent(1)
            else:
                li.setCurrent(self.sec_location)
            h.add(li, 0, 1)
            h.add(bb, 0, 9)
            rc = h.run(24,3)
            if "snack.CompactButton" in str(rc) or rc == 'ESC':
                return 0
            else :
                self.sec_location = li.current()
                if self.sec_location in range(1,len(secondary_window["items"])+1):
                    if secondary_window["items"][self.sec_location-1][1] in dir(three_page):
                        for fun in inspect.getmembers(three_page,callable):
                        #for fun in inspect.getmembers(self, predicate=inspect.ismethod):
                            if secondary_window["items"][self.sec_location-1][1] == fun[0]:
                                fun[1](self.screen)
                    else:
                        warwindows(self.screen, "warn", "Can't find the corresponding function!")
                else:
                    warwindows(self.screen, "test", "xxx")

try:
    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()

    if len(config_first["items"]) != len(config_secondary):
        print "一The number of level directory is not corresponding to the number of secondary windows"
        sys.exit()
    if  os.getenv('STY'):
        print "not support screen"
        sys.exit()
    menu = Menu_tool()
    menu.main()
except Exception,e:
    print e
    print "The specified parameter is invalid"
    usage()
