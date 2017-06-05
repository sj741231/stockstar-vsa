# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

import wx

class MyApp(wx.app):

    def OnInit(self):
        wx.MessageBox("Hello wx", "wx.App")
        return trun


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()