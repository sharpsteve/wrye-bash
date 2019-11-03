# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2019 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""Specific parser for Wrye Bash."""
from collections import OrderedDict
from functools import partial
import os

from . import ScriptParser         # generic parser class
from . import bass
from . import load_order
from .ScriptParser import error
import wx
import wx.wizard as wiz     # wxPython wizard class
from . import bosh, balt, bolt, bush
from .balt import vspace, hspace, set_event_hook, Events
from .env import get_file_version
import io
import traceback

#Translateable strings
from .bosh import OBSEIniFile

EXTRA_ARGS =   _("Extra arguments to '%s'.")
MISSING_ARGS = _("Missing arguments to '%s'.")
UNEXPECTED =   _("Unexpected '%s'.")

class WizardReturn(object):
    __slots__ = ('canceled', 'select_plugins', 'rename_plugins',
                 'select_sub_packages', 'ini_edits', 'should_install',
                 'wizard_size', 'wizard_pos',)
    # canceled: Set to true if the user canceled the wizard, or if an error
    # occurred
    # select_plugins: List of plugins to 'select' for install
    # rename_plugins: Dictionary of renames for plugins.  In the format of:
    #   'original name':'new name'
    # select_sub_packages: List of Subpackages to 'select' for install
    # ini_edits: Dictionary of INI edits to apply/create.  In the format of:
    #   'ini file': {
    #      'section': {
    #         'key': value
    #         }
    #      }
    #    For BatchScript type ini's, the 'section' will either be 'set',
    #    'setGS' or 'SetNumericGameSetting'
    # should_install: Set to True if after configuring this package, it should
    # also be installed.
    # wizard_size: Tuple/wxSize of the saved size of the Wizard
    # wizard_pos: Tuple/wxPoint of the saved position of the Wizard

    def __init__(self):
        self.canceled = False
        self.select_plugins = []
        self.rename_plugins = {}
        self.select_sub_packages = []
        self.ini_edits = {}
        self.should_install = False
        self.wizard_size = balt.defSize
        self.wizard_pos = balt.defPos

class InstallerWizard(wiz.Wizard):
    """Class used by Wrye Bash, creates a wx Wizard that dynamically creates
    pages based on a script."""

    def __init__(self, parentWindow, installer, bAuto, subs, pageSize, pos):
        wiz.Wizard.__init__(self, parentWindow, title=_('Installer Wizard'),
                            pos=pos, style=wx.DEFAULT_DIALOG_STYLE |
                                           wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        #'dummy' page tricks the wizard into always showing the "Next" button,
        #'next' will be set by the parser
        self.dummy = wiz.PyWizardPage(self)
        self.next = None
        #True prevents actually moving to the 'next' page.  We use this after the "Next"
        #button is pressed, while the parser is running to return the _actual_ next page
        #'finishing' is to allow the "Next" button to be used when it's name is changed to
        #'Finish' on the last page of the wizard
        self.blockChange = True
        self.finishing = False
        #parser that will spit out the pages
        self.wizard_file = installer.wizard_file()
        self.parser = WryeParser(self, installer, subs, bAuto)
        #Intercept the changing event so we can implement 'blockChange'
        set_event_hook(self, Events.WIZARD_PAGE_CHANGING, self.OnChange)
        self.ret = WizardReturn()
        self.ret.wizard_size = pageSize
        # So we can save window size
        set_event_hook(self, Events.RESIZE, self.OnSize)
        set_event_hook(self, Events.CLOSE, self.OnClose)
        set_event_hook(self, Events.WIZARD_CANCEL, self.OnClose)
        set_event_hook(self, Events.WIZARD_FINISHED, self.OnClose)
        #Set the minimum size for pages, and setup OnSize to resize the
        #First page to the saved size
        self.SetPageSize((600,500))
        self.firstPage = True

    def OnClose(self, event):
        if not self.IsMaximized():
            # Only save the current size if the page isn't maximized
            self.ret.wizard_size = self.GetSize()
            self.ret.wizard_pos = self.GetPosition()
        event.Skip()

    def OnSize(self, event):
        if self.firstPage:
            # On the first page, resize it to the saved size
            self.firstPage = False
            self.SetSize(self.ret.wizard_size)
        else:
            # Otherwise, regular resize, save the size if we're not
            # maximized
            if not self.IsMaximized():
                self.ret.wizard_size = self.GetSize()
                self.ret.wizard_pos = self.GetPosition()
            event.Skip()

    def OnChange(self, event):
        if event.GetDirection():
            if not self.finishing:
                # Next, continue script execution
                if self.blockChange:
                    #Tell the current page that next was pressed,
                    #So the parser can continue parsing,
                    #Then show the page that the parser returns,
                    #rather than the dummy page
                    event.GetPage().OnNext()
                    event.Veto()
                    self.next = self.parser.Continue()
                    self.blockChange = False
                    self.ShowPage(self.__next__)
                else:
                    self.blockChange = True
        else:
            # Previous, pop back to the last state,
            # and resume execution
            self.finishing = False
            event.Veto()
            self.next = self.parser.Back()
            self.blockChange = False
            self.ShowPage(self.__next__)

    def Run(self):
        page = self.parser.Begin(self.wizard_file)
        if page:
            self.ret.canceled = not self.RunWizard(page)
        # Clean up temp files
        if self.parser.bArchive:
            bass.rmTempDir()
        return self.ret

class PageInstaller(wiz.PyWizardPage):
    """Base class for all the parser wizard pages, just to handle a couple
    simple things here."""

    def __init__(self, parent):
        wiz.PyWizardPage.__init__(self, parent)
        self.parent = parent
        self._enableForward(True)

    def _enableForward(self, enable):
        self.parent.FindWindowById(wx.ID_FORWARD).Enable(enable)

    def GetNext(self): return self.parent.dummy

    def GetPrev(self):
        if self.parent.parser.choiceIdex > 0:
            return self.parent.dummy
        return None

    def OnNext(self):
        #This is what needs to be implemented by sub-classes,
        #this is where flow control objects etc should be
        #created
        pass

class PageError(PageInstaller):
    """Page that shows an error message, has only a "Cancel" button enabled,
    and cancels any changes made."""

    def __init__(self, parent, title, errorMsg):
        PageInstaller.__init__(self, parent)
        #Disable the "Finish"/"Next" button
        self._enableForward(False)
        #Layout stuff
        sizerMain = wx.FlexGridSizer(2, 1, 5, 5)
        textError = balt.RoTextCtrl(self, errorMsg, autotooltip=False)
        sizerMain.Add(balt.StaticText(parent, label=title))
        sizerMain.Add(textError, 0, wx.ALL|wx.CENTER|wx.EXPAND)
        sizerMain.AddGrowableCol(0)
        sizerMain.AddGrowableRow(1)
        self.SetSizer(sizerMain)
        self.Layout()

    def GetNext(self): return None

    def GetPrev(self): return None

class PageSelect(PageInstaller):
    """A page that shows a message up top, with a selection box on the left
    (multi- or single- selection), with an optional associated image and
    description for each option, shown when that item is selected."""
    def __init__(self, parent, bMany, title, desc, listItems, listDescs, listImages, defaultMap):
        PageInstaller.__init__(self, parent)
        self.listItems = listItems
        self.images = listImages
        self.descs = listDescs
        self.bMany = bMany
        self.bmp = wx.EmptyBitmap(1, 1)
        self.index = None
        sizerMain = wx.FlexGridSizer(5, 1, 5, 0)
        sizerTitle = balt.hsbSizer(self)
        self.TitleDesc = balt.StaticText(self, desc)
        self.TitleDesc.Wrap(parent.GetPageSize()[0]-10)
        sizerTitle.Add(self.TitleDesc, 1, wx.ALIGN_CENTER|wx.ALL)
        sizerMain.Add(sizerTitle, 0, wx.EXPAND)
        sizerMain.Add(balt.StaticText(self, _('Options:')))
        sizerBoxes = wx.GridSizer(1, 2, 5, 5)
        self.textItem = balt.RoTextCtrl(self, autotooltip=False)
        self.bmpItem = balt.Picture(self,0,0,background=None)
        if parent.parser.choiceIdex < len(parent.parser.choices):
            oldChoices = parent.parser.choices[parent.parser.choiceIdex]
            defaultMap = [choice in oldChoices for choice in listItems]
        list_box = partial(balt.listBox, self, choices=listItems,
                           isHScroll=True, onSelect=self.OnSelect)
        if bMany:
            self.listOptions = list_box(kind='checklist')
            for index, default in enumerate(defaultMap):
                self.listOptions.Check(index, default)
        else:
            self.listOptions = list_box()
            self._enableForward(False)
            for index, default in enumerate(defaultMap):
                if default:
                    self.listOptions.SetSelection(index)
                    self.Selection(index)
                    break
        sizerBoxes.Add(self.listOptions, 1, wx.ALL|wx.EXPAND)
        sizerBoxes.Add(self.bmpItem, 1, wx.ALL|wx.EXPAND)
        sizerMain.Add(sizerBoxes, wx.ID_ANY, wx.EXPAND)
        sizerMain.Add(balt.StaticText(self, _('Description:')))
        sizerMain.Add(self.textItem, wx.ID_ANY, wx.EXPAND|wx.ALL)
        self.SetSizer(sizerMain)
        sizerMain.AddGrowableRow(2)
        sizerMain.AddGrowableRow(4)
        sizerMain.AddGrowableCol(0)
        self.Layout()
        set_event_hook(self.bmpItem, Events.MOUSE_LEFT_DOUBLECLICK,
                       self.OnDoubleClick)
        set_event_hook(self.bmpItem, Events.MOUSE_MIDDLE_UP,
                       self.OnDoubleClick)

    def OnSelect(self, event):
        """:type event: wx._core.CommandEvent"""
        index = event.GetSelection()
        self.listOptions.SetSelection(index) # event.Skip() won't do
        self.Selection(index)

    def OnDoubleClick(self, _event):
        img = self.images[self.index]
        if img.isfile():
            try:
                img.start()
            except OSError:
                bolt.deprint('Failed to open %s.' % img, traceback=True)

    def Selection(self, index):
        self._enableForward(True)
        self.index = index
        self.textItem.SetValue(self.descs[index])
        # Don't want the bitmap to resize until we call self.Layout()
        self.bmpItem.Freeze()
        img = self.images[index]
        if img.isfile():
            image = wx.Bitmap(img.s)
            self.bmpItem.SetBitmap(image)
            self.bmpItem.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))
        else:
            self.bmpItem.SetBitmap(None)
            self.bmpItem.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.bmpItem.Thaw()
        # self.Layout() # the bitmap would change size and sho blurred

    def OnNext(self):
        temp = []
        if self.bMany:
            index = -1
            for item in self.listItems:
                index += 1
                if self.listOptions.IsChecked(index):
                    temp.append(item)
        else:
            for i in self.listOptions.GetSelections():
                temp.append(self.listItems[i])
        if self.parent.parser.choiceIdex < len(self.parent.parser.choices):
            oldChoices = self.parent.parser.choices[self.parent.parser.choiceIdex]
            if temp == oldChoices:
                pass
            else:
                self.parent.parser.choices = self.parent.parser.choices[0:self.parent.parser.choiceIdex]
                self.parent.parser.choices.append(temp)
        else:
            self.parent.parser.choices.append(temp)
        self.parent.parser.PushFlow('Select', False, ['SelectOne', 'SelectMany', 'Case', 'Default', 'EndSelect'], values=temp, hitCase=False)

_obse_mod_formats = bolt.LowerDict(
    {']set[': ' %(setting)s to %(value)s%(comment)s',
     ']setGS[': ' %(setting)s %(value)s%(comment)s',
     ']SetNumericGameSetting[': ' %(setting)s %(value)s%(comment)s'})
_obse_del_formats = bolt.LowerDict(
    {']set[': ' %(setting)s to DELETED', ']setGS[': ' %(setting)s DELETED',
     ']SetNumericGameSetting[': ' %(setting)s DELETED'})

def generateTweakLines(wizardEdits, target):
    lines = [_('; Generated by Wrye Bash %s for \'%s\' via wizard') % (
        bass.AppVersion, target.s)]
    for realSection, values in list(wizardEdits.items()):
        if not realSection:
            continue
        realSection = OBSEIniFile.ci_pseudosections.get(realSection,
                                                        realSection)
        try: # OBSE pseudo section
            modFormat = values[0] + _obse_mod_formats[realSection]
            delFormat = ';-' + values[0] + _obse_del_formats[realSection]
        except KeyError: # normal ini, assume pseudosections don't appear there
            lines.append('')
            lines.append('[%s]' % values[0])
            modFormat = '%(setting)s=%(value)s%(comment)s'
            delFormat = ';-%(setting)s'
        for realSetting in values[1]:
            setting,value,comment,deleted = values[1][realSetting]
            fmt = delFormat if deleted else modFormat
            lines.append(fmt % (dict(setting=setting, value=value,
                                     comment=comment)))
    return lines

class PageFinish(PageInstaller):
    """Page displayed at the end of a wizard, showing which sub-packages and
    which plugins will be selected. Also displays some notes for the user."""

    def __init__(self, parent, subsList, plugin_list, plugin_renames, bAuto,
                 notes, iniedits):
        PageInstaller.__init__(self, parent)
        subs = list(subsList.keys())
        subs.sort(lambda l,r: cmp(l, r))
        subs = [x.replace('&','&&') for x in subs]
        plugins = list(plugin_list.keys())
        plugins.sort(lambda l,r: cmp(l, r))
        #--make the list that will be displayed
        displayed_plugins = []
        for x in plugins:
            if x in plugin_renames:
                displayed_plugins.append(x + ' -> ' + plugin_renames[x])
            else:
                displayed_plugins.append(x)
        displayed_plugins = [x.replace('&','&&') for x in displayed_plugins]
        sizerMain = balt.vSizer()
        parent.parser.choiceIdex += 1
        #--Heading
        sizerTitle = balt.hsbSizer(self)
        textTitle = balt.StaticText(self, _("The installer script has finished, and will apply the following settings:"))
        textTitle.Wrap(parent.GetPageSize()[0]-10)
        sizerTitle.Add(textTitle,0,wx.ALIGN_CENTER)
        sizerMain.Add(sizerTitle,0,wx.EXPAND)
        #--Subpackages and Plugins
        subPackageSizer = balt.vSizer(
            balt.StaticText(self, _('Sub-Packages')), vspace(2))
        self.listSubs = balt.listBox(self, choices=subs, kind='checklist',
                                     onCheck=self.OnSelectSubs)
        for index,key in enumerate(subs):
            key = key.replace('&&','&')
            if subsList[key]:
                self.listSubs.Check(index, True)
                self.parent.ret.select_sub_packages.append(key)
        subPackageSizer.Add(self.listSubs,1,wx.EXPAND)
        plugin_sizer = balt.vSizer(balt.StaticText(self, _('Plugins')),
                                   vspace(2))
        self.plugin_selection = balt.listBox(self, choices=displayed_plugins,
                                             kind='checklist',
                                             onCheck=self._on_select_plugin)
        for index,key in enumerate(plugins):
            if plugin_list[key]:
                self.plugin_selection.Check(index, True)
                self.parent.ret.select_plugins.append(key)
        plugin_sizer.Add(self.plugin_selection, 1, wx.EXPAND)
        self.parent.ret.rename_plugins = plugin_renames
        sizer_subs_plugins = balt.hSizer(
            (subPackageSizer, 1, wx.EXPAND), hspace(5),
            (plugin_sizer, 1, wx.EXPAND))
        sizerMain.Add(*vspace(5))
        sizerMain.Add(sizer_subs_plugins, 2, wx.EXPAND)
        sizerMain.Add(*vspace(5))
        #--Ini tweaks
        sizerTweaks = balt.vSizer(balt.StaticText(self, _('Ini Tweaks:')),
                                  vspace(2))
        self.listInis = balt.listBox(self, onSelect=self.OnSelectIni,
                                     choices=[x.s for x in list(iniedits.keys())])
        sizerTweaks.Add(self.listInis,1,wx.EXPAND)
        sizerContents = balt.vSizer(balt.StaticText(self, ''), vspace(2))
        self.listTweaks = balt.listBox(self)
        sizerContents.Add(self.listTweaks,1,wx.EXPAND)
        sizerIniTweaks = balt.hSizer((sizerTweaks, 1, wx.EXPAND),
            hspace(5), (sizerContents, 1, wx.EXPAND))
        sizerMain.Add(sizerIniTweaks, 2, wx.EXPAND)
        sizerMain.Add(*vspace(5))
        self.parent.ret.ini_edits = iniedits
        #--Notes
        sizerMain.Add(balt.StaticText(self, _('Notes:')))
        sizerMain.Add(*vspace(2))
        sizerMain.Add(
            balt.RoTextCtrl(self, ''.join(notes), autotooltip=False), 1,
            wx.EXPAND)
        checkSizer = balt.hSizer()
        checkSizer.AddStretchSpacer()
        # Apply the selections
        self.checkApply = balt.checkBox(self, _('Apply these selections'),
                                        onCheck=self.OnCheckApply,
                                        checked=bAuto)
        checkSubSizer = balt.vSizer(self.checkApply, vspace(2))
        # Also install/anneal the package
        auto = bass.settings['bash.installers.autoWizard']
        self.checkInstall = balt.checkBox(self, _('Install this package'),
                                          onCheck=self.OnCheckInstall,
                                          checked=auto)
        self.parent.ret.should_install = auto
        checkSubSizer.Add(self.checkInstall)
        checkSizer.Add(checkSubSizer,0,wx.EXPAND)
        sizerMain.Add(checkSizer,0,wx.TOP|wx.RIGHT|wx.EXPAND,5)
        self._enableForward(bAuto)
        self.parent.finishing = True
        sizerMain.SetSizeHints(self)
        self.SetSizer(sizerMain)
        self.Layout()

    def OnCheckApply(self):
        self._enableForward(self.checkApply.IsChecked())

    def OnCheckInstall(self):
        self.parent.ret.should_install = self.checkInstall.IsChecked()

    def GetNext(self): return None

    # Undo selecting/deselection of items for UI consistency
    def OnSelectSubs(self, event):
        index = event.GetSelection()
        self.listSubs.Check(index, not self.listSubs.IsChecked(index))

    def _on_select_plugin(self, event):
        index = event.GetSelection()
        self.plugin_selection.Check(index, not self.plugin_selection.IsChecked(index))

    def OnSelectIni(self, event):
        index = event.GetSelection()
        ini_path = bolt.GPath(self.listInis.GetString(index))
        lines = generateTweakLines(self.parent.ret.ini_edits[ini_path],
                                   ini_path)
        self.listTweaks.Set(lines)
        self.listInis.SetSelection(index)

class PageVersions(PageInstaller):
    """Page for displaying what versions an installer requires/recommends and
    what you have installed for Game, *SE, *GE, and Wrye Bash."""
    def __init__(self, parent, bGameOk, gameHave, gameNeed, bSEOk, seHave,
                 seNeed, bGEOk, geHave, geNeed, bWBOk, wbHave, wbNeed):
        PageInstaller.__init__(self, parent)
        bmp = [wx.Bitmap(bass.dirs['images'].join('error_cross_24.png').s),
               wx.Bitmap(bass.dirs['images'].join('checkmark_24.png').s)]
        sizerMain = wx.FlexGridSizer(5, 1, 0, 0)
        self.textWarning = balt.StaticText(self, _('WARNING: The following version requirements are not met for using this installer.'))
        self.textWarning.Wrap(parent.GetPageSize()[0]-20)
        sizerMain.Add(self.textWarning, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        sizerVersionsTop = balt.hsbSizer(self, _('Version Requirements'))
        sizerVersions = wx.FlexGridSizer(5, 4, 5, 5)
        sizerVersionsTop.Add(sizerVersions, 1, wx.EXPAND, 0)
        sizerVersions.AddStretchSpacer()
        sizerVersions.Add(balt.StaticText(self, _('Need')))
        sizerVersions.Add(balt.StaticText(self, _('Have')))
        sizerVersions.AddStretchSpacer()

        def _hyperlink(label, url): return wx.HyperlinkCtrl(self, balt.defId,
                                                       label=label, url=url)
        # Game
        if bush.game.patchURL != '':
            linkGame = _hyperlink(bush.game.displayName, bush.game.patchURL)
            linkGame.SetVisitedColour(linkGame.GetNormalColour())
        else:
            linkGame = balt.StaticText(self, bush.game.displayName)
        linkGame.SetToolTip(balt.tooltip(bush.game.patchTip))
        sizerVersions.Add(linkGame)
        sizerVersions.Add(balt.StaticText(self, gameNeed))
        sizerVersions.Add(balt.StaticText(self, gameHave))
        sizerVersions.Add(balt.staticBitmap(self, bmp[bGameOk]))
        # Script Extender
        if bush.game.se.se_abbrev != '':
            linkSE = _hyperlink(bush.game.se.long_name, bush.game.se.url)
            linkSE.SetVisitedColour(linkSE.GetNormalColour())
            linkSE.SetToolTip(balt.tooltip(bush.game.se.url_tip))
            sizerVersions.Add(linkSE)
            sizerVersions.Add(balt.StaticText(self, seNeed))
            sizerVersions.Add(balt.StaticText(self, seHave))
            sizerVersions.Add(balt.staticBitmap(self, bmp[bSEOk]))
        # Graphics extender
        if bush.game.ge.ge_abbrev != '':
            linkGE = _hyperlink(bush.game.ge.long_name, bush.game.ge.url)
            linkGE.SetVisitedColour(linkGE.GetNormalColour())
            linkGE.SetToolTip(balt.tooltip(bush.game.ge.url_tip))
            sizerVersions.Add(linkGE)
            sizerVersions.Add(balt.StaticText(self, geNeed))
            sizerVersions.Add(balt.StaticText(self, geHave))
            sizerVersions.Add(balt.staticBitmap(self, bmp[bGEOk]))
        linkWB = _hyperlink('Wrye Bash',
                            'https://www.nexusmods.com/oblivion/mods/22368')
        linkWB.SetVisitedColour(linkWB.GetNormalColour())
        linkWB.SetToolTip(balt.tooltip('https://www.nexusmods.com/oblivion'))
        sizerVersions.Add(linkWB)
        sizerVersions.Add(balt.StaticText(self, wbNeed))
        sizerVersions.Add(balt.StaticText(self, wbHave))
        sizerVersions.Add(balt.staticBitmap(self, bmp[bWBOk]))
        sizerVersions.AddGrowableCol(0)
        sizerVersions.AddGrowableCol(1)
        sizerVersions.AddGrowableCol(2)
        sizerVersions.AddGrowableCol(3)
        sizerMain.Add(sizerVersionsTop, 2, wx.ALL|wx.EXPAND, 5)
        sizerMain.AddStretchSpacer()
        sizerCheck = wx.FlexGridSizer(1, 2, 5, 5)
        self.checkOk = balt.checkBox(self, _('Install anyway.'),
                                     onCheck=self.OnCheck)
        self._enableForward(False)
        sizerCheck.AddStretchSpacer()
        sizerCheck.Add(self.checkOk)
        sizerCheck.AddGrowableRow(0)
        sizerCheck.AddGrowableCol(0)
        sizerMain.Add(sizerCheck, 3, wx.EXPAND)
        self.SetSizer(sizerMain)
        sizerMain.AddGrowableRow(0)
        sizerMain.AddGrowableRow(2)
        sizerMain.AddGrowableCol(0)
        self.Layout()

    def OnCheck(self):
        self._enableForward(self.checkOk.IsChecked())

class WryeParser(ScriptParser.Parser):
    """A derived class of Parser, for handling BAIN install wizards."""
    codeboxRemaps = {
        'Link': {
            # These are links that have different names than their text
            'SelectOne':'SelectOne1',
            'SelectMany':'SelectMany1',
            '=':'Assignment',
            '+=':'CompountAssignmentetc',
            '-=':'CompountAssignmentetc',
            '*=':'CompountAssignmentetc',
            '/=':'CompountAssignmentetc',
            '^=':'CompountAssignmentetc',
            '+':'Addition',
            '-':'Subtraction',
            '*':'Multiplication',
            '/':'Division',
            '^':'Exponentiation',
            'and':'Andampand',
            '&':'Andampand',
            'or':'Oror',
            '|':'Oror',
            'not':'Notnot',
            '!':'Notnot',
            'in':'Inin',
            'in:':'CaseInsensitiveInin',
            '==':'Equal',
            '==:':'CaseinsensitiveEqual',
            '!=':'NotEqual',
            '!=:':'CaseinsensitiveNotEqual',
            '>=':'GreaterThanorEqualgt',
            '>=:':'CaseInsensitiveGreaterThanorEqualgt',
            '>':'GreaterThangt',
            '>:':'CaseInsensitiveGreaterThangt',
            '<=':'LessThanorEquallt',
            '<=:':'CaseInsensitiveLessThanorEquallt',
            '<':'LessThanlt',
            '<:':'CaseInsensitiveLessThanlt',
            '.':'DotOperator',
            'SubPackages':'ForContinueBreakEndFor',
            },
        'Text': {
            # These are symbols that need to be replaced to be xhtml compliant
            '&':'&amp;',
            '<':'&lt;',
            '<:':'&lt;:',
            '<=':'&lt;=',
            '<=:':'&lt;=:',
            '>':'&gt;',
            '>:':'&gt;:',
            '>=':'&gt;=',
            '>=:':'&gt;=:',
            },
        'Color': {
            # These are items that we want colored differently
            'in':'blue',
            'in:':'blue',
            'and':'blue',
            'or':'blue',
            'not':'blue',
            },
        }

    @staticmethod
    def codebox(lines,pre=True,br=True):
        self = WryeParser(None, None, None, None, codebox=True) ##: drop this !
        def colorize(text_, color='black', link=True):
            href = text_
            text_ = WryeParser.codeboxRemaps['Text'].get(text_, text_)
            if color != 'black' or link:
                color = WryeParser.codeboxRemaps['Color'].get(text_, color)
                text_ = '<span style="color:%s;">%s</span>' % (color, text_)
            if link:
                href = WryeParser.codeboxRemaps['Link'].get(href,href)
                text_ = '<a href="#%s">%s</a>' % (href, text_)
            return text_
        self.cLine = 0
        outLines = []
        lastBlank = 0
        while self.cLine < len(lines):
            line = lines[self.cLine]
            self.cLine += 1
            self.tokens = []
            self.TokenizeLine(line)
            tokens = self.tokens
            line = line.strip('\r\n')
            lastEnd = 0
            dotCount = 0
            outLine = ''
            for i in tokens:
                start,stop = i.pos
                if start is not None and stop is not None:
                    # Not an inserted token from the parser
                    if i.type == ScriptParser.STRING:
                        start -= 1
                        stop  += 1
                    # Padding
                    padding = line[lastEnd:start]
                    outLine += padding
                    lastEnd = stop
                    # The token
                    token_txt = line[start:stop]
                    # Check for ellipses
                    if i.text == '.':
                        dotCount += 1
                        if dotCount == 3:
                            dotCount = 0
                            outLine += '...'
                        continue
                    else:
                        while dotCount > 0:
                            outLine += colorize('.')
                            dotCount -= 1
                    if i.type == ScriptParser.KEYWORD:
                        outLine += colorize(token_txt,'blue')
                    elif i.type == ScriptParser.FUNCTION:
                        outLine += colorize(token_txt,'purple')
                    elif i.type in (ScriptParser.INTEGER, ScriptParser.DECIMAL):
                        outLine += colorize(token_txt,'cyan',False)
                    elif i.type == ScriptParser.STRING:
                        outLine += colorize(token_txt,'brown',False)
                    elif i.type == ScriptParser.OPERATOR:
                        outLine += colorize(i.text)
                    elif i.type == ScriptParser.CONSTANT:
                        outLine += colorize(token_txt,'cyan')
                    elif i.type == ScriptParser.NAME:
                        outLine += '<i>%s</i>' % token_txt
                    else:
                        outLine += token_txt
            if self.runon:
                outLine += ' \\'
            if lastEnd < len(line):
                comments = line[lastEnd:]
                if ';' in comments:
                    outLine += colorize(comments,'green',False)
            if outLine == '':
                if len(outLines) != 0:
                    lastBlank = len(outLines)
                else:
                    continue
            else:
                lastBlank = 0
            if pre:
                outLine = '<span class="code-n" style="display: inline;">%s</span>\n' % outLine
            else:
                if br:
                    outLine = '<span class="code-n">%s</span><br />\n' % outLine
                else:
                    outLine = '<span class="code-n">%s</span>' % outLine
            outLines.append(outLine)
        if lastBlank:
            outLines = outLines[:lastBlank]
        return outLines

    def __init__(self, parent, installer, subs, bAuto, codebox=False):
        ScriptParser.Parser.__init__(self)
        if not codebox:
            self.parent = parent
            self.installer = installer
            self.bArchive = isinstance(installer, bosh.InstallerArchive)
            self._path = bolt.GPath(installer.archive) if installer else None
            if installer and installer.fileRootIdex:
                root_path = installer.extras_dict.get('root_path', '')
                self._path = self._path.join(root_path)
            self.bAuto = bAuto
            self.page = None
            self.choices = []
            self.choiceIdex = -1
            self.sublist = bolt.LowerDict()
            self.plugin_list = bolt.LowerDict()
            for k, v in installer.espmMap.items():
                for j in v:
                    if j not in self.plugin_list:
                        self.plugin_list[j] = False
                if k == '': continue
                self.sublist[k] = False
        #--Constants
        self.SetConstant('SubPackages','SubPackages')
        #--Operators
        #Assignment
        self.SetOperator('=' , self.Ass, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('+=', self.AssAdd, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('-=', self.AssMin, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('*=', self.AssMul, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('/=', self.AssDiv, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('%=', self.AssMod, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        self.SetOperator('^=', self.AssExp, ScriptParser.OP.ASS, ScriptParser.RIGHT)
        #Comparison
        self.SetOperator('==', self.opE, ScriptParser.OP.CO2)
        self.SetOperator('!=', self.opNE, ScriptParser.OP.CO2)
        self.SetOperator('>=', self.opGE, ScriptParser.OP.CO1)
        self.SetOperator('>' , self.opG, ScriptParser.OP.CO1)
        self.SetOperator('<=', self.opLE, ScriptParser.OP.CO1)
        self.SetOperator('<' , self.opL, ScriptParser.OP.CO1)
        self.SetOperator('==:', self.opEc, ScriptParser.OP.CO2, passTokens=False)  # Case insensitive ==
        self.SetOperator('!=:', self.opNEc, ScriptParser.OP.CO2, passTokens=False) # Case insensitive !=
        self.SetOperator('>=:', self.opGEc, ScriptParser.OP.CO1, passTokens=False) # Case insensitive >=
        self.SetOperator('>:', self.opGc, ScriptParser.OP.CO1, passTokens=False)   # Case insensitive >
        self.SetOperator('<=:', self.opLEc, ScriptParser.OP.CO1, passTokens=False) # Case insensitive <=
        self.SetOperator('<:', self.opLc, ScriptParser.OP.CO1, passTokens=False)   # Case insensitive <
        #Membership operators
        self.SetOperator('in', self.opIn, ScriptParser.OP.MEM, passTokens=False)
        self.SetOperator('in:', self.opInCase, ScriptParser.OP.MEM, passTokens=False) # Case insensitive in
        #Boolean
        self.SetOperator('&' , self.opAnd, ScriptParser.OP.AND)
        self.SetOperator('and', self.opAnd, ScriptParser.OP.AND)
        self.SetOperator('|', self.opOr, ScriptParser.OP.OR)
        self.SetOperator('or', self.opOr, ScriptParser.OP.OR)
        self.SetOperator('!', self.opNot, ScriptParser.OP.NOT, ScriptParser.RIGHT)
        self.SetOperator('not', self.opNot, ScriptParser.OP.NOT, ScriptParser.RIGHT)
        #Pre-increment/decrement
        self.SetOperator('++', self.opInc, ScriptParser.OP.UNA)
        self.SetOperator('--', self.opDec, ScriptParser.OP.UNA)
        #Math
        self.SetOperator('+', self.opAdd, ScriptParser.OP.ADD)
        self.SetOperator('-', self.opMin, ScriptParser.OP.ADD)
        self.SetOperator('*', self.opMul, ScriptParser.OP.MUL)
        self.SetOperator('/', self.opDiv, ScriptParser.OP.MUL)
        self.SetOperator('%', self.opMod, ScriptParser.OP.MUL)
        self.SetOperator('^', self.opExp, ScriptParser.OP.EXP, ScriptParser.RIGHT)
        #--Functions
        self.SetFunction('CompareObVersion', self.fnCompareGameVersion, 1)      # Retained for compatibility
        self.SetFunction('CompareGameVersion', self.fnCompareGameVersion, 1)
        self.SetFunction('CompareOBSEVersion', self.fnCompareSEVersion, 1)      # Retained for compatibility
        self.SetFunction('CompareSEVersion', self.fnCompareSEVersion, 1)
        self.SetFunction('CompareOBGEVersion', self.fnCompareGEVersion, 1)      # Retained for compatibility
        self.SetFunction('CompareGEVersion', self.fnCompareGEVersion, 1)
        self.SetFunction('CompareWBVersion', self.fnCompareWBVersion, 1)
        self.SetFunction('DataFileExists', self.fnDataFileExists, 1, ScriptParser.KEY.NO_MAX)
        self.SetFunction('GetEspmStatus', self.fn_get_plugin_status, 1)
        self.SetFunction('GetPluginStatus', self.fn_get_plugin_status, 1)       # Retained for compatibility
        self.SetFunction('EditINI', self.fnEditINI, 4, 5)
        self.SetFunction('DisableINILine',self.fnDisableINILine, 3)
        self.SetFunction('Exec', self.fnExec, 1)
        self.SetFunction('EndExec', self.fnEndExec, 1)
        self.SetFunction('str', self.fnStr, 1)
        self.SetFunction('int', self.fnInt, 1)
        self.SetFunction('float', self.fnFloat, 1)
        #--String functions
        self.SetFunction('len', self.fnLen, 1, dotFunction=True)
        self.SetFunction('endswith', self.fnEndsWith, 2, ScriptParser.KEY.NO_MAX, dotFunction=True)
        self.SetFunction('startswith', self.fnStartsWith, 2, ScriptParser.KEY.NO_MAX, dotFunction=True)
        self.SetFunction('lower', self.fnLower, 1, dotFunction=True)
        self.SetFunction('find', self.fnFind, 2, 4, dotFunction=True)
        self.SetFunction('rfind', self.fnRFind, 2, 4, dotFunction=True)
        #--String pathname functions
        self.SetFunction('GetFilename', self.fnGetFilename, 1)
        self.SetFunction('GetFolder', self.fnGetFolder, 1)
        #--Keywords
        self.SetKeyword('SelectSubPackage', self.kwdSelectSubPackage, 1)
        self.SetKeyword('DeSelectSubPackage', self.kwdDeSelectSubPackage, 1)
        # The keyowrds with 'espm' in their name are retained for backwards
        # compatibility only - use their 'plugin' equivalents instead
        self.SetKeyword('SelectEspm', self.kwd_select_plugin, 1)
        self.SetKeyword('SelectPlugin', self.kwd_select_plugin, 1)
        self.SetKeyword('DeSelectEspm', self.kwd_de_select_plugin, 1)
        self.SetKeyword('DeSelectPlugin', self.kwd_de_select_plugin, 1)
        self.SetKeyword('SelectAll', self.kwdSelectAll)
        self.SetKeyword('DeSelectAll', self.kwdDeSelectAll)
        self.SetKeyword('SelectAllEspms', self.kwd_select_all_plugins)
        self.SetKeyword('SelectAllPlugins', self.kwd_select_all_plugins)
        self.SetKeyword('DeSelectAllEspms', self.kwd_de_select_all_plugins)
        self.SetKeyword('DeSelectAllPlugins', self.kwd_de_select_all_plugins)
        self.SetKeyword('RenameEspm', self.kwd_rename_plugin, 2)
        self.SetKeyword('RenamePlugin', self.kwd_rename_plugin, 2)
        self.SetKeyword('ResetEspmName', self.kwd_reset_plugin_name, 1)
        self.SetKeyword('ResetPluginName', self.kwd_reset_plugin_name, 1)
        self.SetKeyword('ResetAllEspmNames', self.kwd_reset_all_plugin_names)
        self.SetKeyword('ResetAllPluginNames',self.kwd_reset_all_plugin_names)
        self.SetKeyword('Note', self.kwdNote, 1)
        self.SetKeyword('If', self.kwdIf, 1 )
        self.SetKeyword('Elif', self.kwdElif, 1)
        self.SetKeyword('Else', self.kwdElse)
        self.SetKeyword('EndIf', self.kwdEndIf)
        self.SetKeyword('While', self.kwdWhile, 1)
        self.SetKeyword('Continue', self.kwdContinue)
        self.SetKeyword('EndWhile', self.kwdEndWhile)
        self.SetKeyword('For', self.kwdFor, 3, ScriptParser.KEY.NO_MAX, passTokens=True, splitCommas=False)
        self.SetKeyword('from', self.kwdDummy)
        self.SetKeyword('to', self.kwdDummy)
        self.SetKeyword('by', self.kwdDummy)
        self.SetKeyword('EndFor', self.kwdEndFor)
        self.SetKeyword('SelectOne', self.kwdSelectOne, 7, ScriptParser.KEY.NO_MAX)
        self.SetKeyword('SelectMany', self.kwdSelectMany, 4, ScriptParser.KEY.NO_MAX)
        self.SetKeyword('Case', self.kwdCase, 1)
        self.SetKeyword('Default', self.kwdDefault)
        self.SetKeyword('Break', self.kwdBreak)
        self.SetKeyword('EndSelect', self.kwdEndSelect)
        self.SetKeyword('Return', self.kwdReturn)
        self.SetKeyword('Cancel', self.kwdCancel, 0, 1)
        self.SetKeyword('RequireVersions', self.kwdRequireVersions, 1, 4)

    @property
    def path(self): return self._path

    def Begin(self, file):
        self.variables.clear()
        self.Flow = []
        self.notes = []
        self.plugin_renames = {}
        self.iniedits = {}
        self.cLine = 0
        self.reversing = 0
        self.ExecCount = 0
        if file.exists() and file.isfile():
            try:
                with file.open(encoding='utf-8-sig') as script:
                    # Ensure \n line endings for the script parser
                    self.lines = [x.replace('\r\n','\n') for x in script.readlines()]
                return self.Continue()
            except UnicodeError:
                balt.showWarning(self.parent,_('Could not read the wizard file.  Please ensure it is encoded in UTF-8 format.'))
                return
        balt.showWarning(self.parent, _('Could not open wizard file'))
        return None

    def Continue(self):
        self.page = None
        while self.cLine < len(self.lines):
            newline = self.lines[self.cLine]
            try:
                self.RunLine(newline)
            except ScriptParser.ParserError as e:
                return PageError(self.parent, _('Installer Wizard'),
                                 _('An error occurred in the wizard script:') + '\n'
                                 + _('Line %s:\t%s') % (self.cLine, newline.strip('\n')) + '\n'
                                 + _('Error:\t%s') % e)
            except Exception:
                o = io.StringIO()
                o.write(_('An unhandled error occurred while parsing the wizard:') + '\n'
                        + _('Line %s:\t%s') % (self.cLine, newline.strip('\n')) + '\n\n')
                traceback.print_exc(file=o)
                msg = o.getvalue()
                o.close()
                return PageError(self.parent, _('Installer Wizard'), msg)
            if self.page:
                return self.page
        self.cLine += 1
        self.cLineStart = self.cLine
        return PageFinish(self.parent, self.sublist, self.plugin_list,
                          self.plugin_renames, self.bAuto, self.notes,
                          self.iniedits)

    def Back(self):
        if self.choiceIdex == 0:
            return
        # Rebegin
        self.variables.clear()
        self.Flow = []
        self.notes = []
        self.plugin_renames = {}
        self.iniedits = {}
        i = 0
        while self.ExecCount > 0 and i < len(self.lines):
            line = self.lines[i]
            i += 1
            if line.startswith('EndExec('):
                numLines = int(line[8:-1])
                del self.lines[i-numLines:i]
                i -= numLines
                self.ExecCount -= 1
        for i in self.sublist:
            self.sublist[i] = False
        for i in self.plugin_list:
            self.plugin_list[i] = False
        self.cLine = 0
        self.reversing = self.choiceIdex-1
        self.choiceIdex = -1
        return self.Continue()

    def _is_plugin_in_package(self, plugin_name, package):
        if package not in self.installer.espmMap: return False
        plugin_name = plugin_name.lower()
        v = self.installer.espmMap[package]
        for j in v:
            if plugin_name == j.lower():
                return True
        return False

    def _plugin_in_active_package(self, plugin_name):
        for i in self.sublist:
            if self._is_plugin_in_package(plugin_name, i):
                if self.sublist[i]:
                    return True
        return False

    def _resolve_plugin_rename(self, plugin_name):
        plugin_name = plugin_name.lower()
        for i in self.plugin_list:
            if plugin_name == i.lower():
                return i
        return None

    # Assignment operators
    def Ass(self, l, r):
        if l.type not in [ScriptParser.VARIABLE,ScriptParser.NAME]:
            error(_('Cannot assign a value to %s, type is %s.') % (l.text, ScriptParser.Types[l.type]))
        self.variables[l.text] = r.tkn
        return r.tkn

    def AssAdd(self, l, r): return self.Ass(l, l+r)
    def AssMin(self, l, r): return self.Ass(l, l-r)
    def AssMul(self, l, r): return self.Ass(l, l*r)
    def AssDiv(self, l, r): return self.Ass(l, l/r)
    def AssMod(self, l, r): return self.Ass(l, l%r)
    def AssExp(self, l, r): return self.Ass(l, l**r)

    # Comparison operators
    def opE(self, l, r): return l == r

    def opEc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() == r.lower()
        else:
            return l == r

    def opNE(self, l, r): return l != r

    def opNEc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() != r.lower()
        else:
            return l != r

    def opGE(self, l, r): return l >= r

    def opGEc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() >= r.lower()
        else:
            return l >= r

    def opG(self, l, r): return l > r

    def opGc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() > r.lower()
        else:
            return l > r

    def opLE(self, l, r): return l <= r

    def opLEc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() <= r.lower()
        else:
            return l <= r

    def opL(self, l, r): return l < r

    def opLc(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() < r.lower()
        else:
            return l < r

    # Membership tests
    def opIn(self, l, r): return l in r

    def opInCase(self, l, r):
        if isinstance(l, str) and isinstance(r, str):
            return l.lower() in r.lower()
        else:
            return l in r

    # Boolean operators
    def opAnd(self, l, r): return l and r
    def opOr(self, l, r): return l or r
    def opNot(self, l): return not l

    # Pre-increment/decrement
    def opInc(self, l):
        if l.type not in [ScriptParser.VARIABLE,ScriptParser.NAME]:
            error(_('Cannot increment %s, type is %s.') % (l.text, ScriptParser.Types[l.type]))
        new_val = l.tkn + 1
        self.variables[l.text] = new_val
        return new_val

    def opDec(self, l):
        if l.type not in [ScriptParser.VARIABLE,ScriptParser.NAME]:
            error(_('Cannot decrement %s, type is %s.') % (l.text, ScriptParser.Types[l.type]))
        new_val = l.tkn - 1
        self.variables[l.text] = new_val
        return new_val

    # Math operators
    def opAdd(self, l, r): return l + r
    def opMin(self, l, r): return l - r
    def opMul(self, l, r): return l * r
    def opDiv(self, l, r): return l / r
    def opMod(self, l, r): return l % r
    def opExp(self, l, r): return l ** r

    # Functions...
    def fnCompareGameVersion(self, obWant):
        ret = self._TestVersion(
            self._TestVersion_Want(obWant),
            bass.dirs['app'].join(*bush.game.version_detect_file))
        return ret[0]

    def fnCompareSEVersion(self, seWant):
        if bush.game.se.se_abbrev != '':
            if bass.inisettings['SteamInstall']:
                se = bush.game.se.steam_exe   # User may not have obse_loader.exe, since it's only required for the CS
            else:
                se = bush.game.se.exe
            ret = self._TestVersion(self._TestVersion_Want(seWant), bass.dirs['app'].join(se))
            return ret[0]
        else:
            # No script extender available for this game
            return 1

    def fnCompareGEVersion(self, geWant):
        if bush.game.ge.ge_abbrev != '':
            ret = self._TestVersion_GE(self._TestVersion_Want(geWant))
            return ret[0]
        else:
            # No graphics extender available for this game
            return 1

    def fnCompareWBVersion(self, wbWant):
        wbHave = bass.AppVersion
        return cmp(float(wbHave), float(wbWant))

    def fnDataFileExists(self, *filenames):
        for filename in filenames:
            if not bass.dirs['mods'].join(filename).exists():
                # Check for ghosted mods
                if bolt.GPath(filename) in bosh.modInfos:
                    return True # It's a ghosted mod
                return False
        return True

    def fn_get_plugin_status(self, filename):
        file = bolt.GPath(filename)
        if file in bosh.modInfos.merged: return 3   # Merged
        if load_order.cached_is_active(file): return 2  # Active
        if file in bosh.modInfos.imported: return 1 # Imported (not active/merged)
        if file in bosh.modInfos: return 0          # Inactive
        return -1                                   # Not found

    def fnEditINI(self, ini_name, section, setting, value, comment=''):
        self._handleINIEdit(ini_name, section, setting, value, comment, False)

    def fnDisableINILine(self, ini_name, section, setting):
        self._handleINIEdit(ini_name, section, setting, '', '', True)

    def _handleINIEdit(self, ini_name, section, setting, value, comment,
                       disable):
        """
        Common implementation for the EditINI and DisableINILine wizard
        functions.

        :param ini_name: The name of the INI file to edit. If it's not one of
            the game's default INIs (e.g. Skyrim.ini), it's treated as relative
            to the Data folder.
        :param section: The section of the INI file to edit.
        :param setting: The name of the setting to edit.
        :param value: The value to assign. If disabling a line, this is
            ignored.
        :param comment: The comment to place with the edit. Pass an empty
            string if no comment should be placed.
        :param disable: Whether or not this edit should disable the setting in
            question.
        """
        ini_path = bolt.GPath(ini_name)
        section = section.strip()
        setting = setting.strip()
        comment = comment.strip()
        real_section = OBSEIniFile.ci_pseudosections.get(section, section)
        if comment and not comment.startswith(';'):
            comment = ';' + comment
        self.iniedits.setdefault(ini_path, bolt.LowerDict()).setdefault(
            real_section, [section, bolt.LowerDict()])
        self.iniedits[ini_path][real_section][0] = section
        self.iniedits[ini_path][real_section][1][setting] = (setting, value,
                                                             comment, disable)

    def fnExec(self, strLines):
        lines = strLines.split('\n')
        # Manual EndExec calls are illegal - if we don't check here, a wizard
        # could exploit this by doing something like this:
        #   Exec("EndExec(1)\nAnythingHere\nReturn")
        # ... which doesn't really cause harm, but is pretty strange and
        # inconsistent
        if any([l.strip().startswith('EndExec(') for l in lines]):
            error(UNEXPECTED % 'EndExec')
        lines.append('EndExec(%i)' % (len(lines)+1))
        self.lines[self.cLine:self.cLine] = lines
        self.ExecCount += 1

    def fnEndExec(self, numLines):
        if self.ExecCount == 0:
            error(UNEXPECTED % 'EndExec')
        del self.lines[self.cLine-numLines:self.cLine]
        self.cLine -= numLines
        self.ExecCount -= 1

    def fnStr(self, data): return str(data)

    def fnInt(self, data):
        try:
            return int(data)
        except ValueError:
            return 0

    def fnFloat(self, data):
        try:
            return float(data)
        except ValueError:
            return 0.0

    def fnLen(self, data):
        try:
            return len(data)
        except TypeError:
            return 0

    def fnEndsWith(self, String, *args):
        if not isinstance(String, str):
            error(_("Function 'endswith' only operates on string types."))
        return String.endswith(args)

    def fnStartsWith(self, String, *args):
        if not isinstance(String, str):
            error(_("Function 'startswith' only operates on string types."))
        return String.startswith(args)

    def fnLower(self, String):
        if not isinstance(String, str):
            error(_("Function 'lower' only operates on string types."))
        return String.lower()

    def fnFind(self, String, sub, start=0, end=-1):
        if not isinstance(String, str):
            error(_("Function 'find' only operates on string types."))
        if end < 0: end += len(String) + 1
        return String.find(sub, start, end)

    def fnRFind(self, String, sub, start=0, end=-1):
        if not isinstance(String, str):
            error(_("Function 'rfind' only operates on string types."))
        if end < 0: end += len(String) + 1
        return String.rfind(sub, start, end)

    def fnGetFilename(self, String): return os.path.basename(String)
    def fnGetFolder(self, String): return os.path.dirname(String)

    # Dummy keyword, for reserving a keyword, but handled by other keywords
    # (like from, to, and by)
    def kwdDummy(self): pass

    # Keywords, mostly for flow control (If, Select, etc)
    def kwdIf(self, bActive):
        if self.LenFlow() > 0 and self.PeekFlow().type == 'If' and not self.PeekFlow().active:
            #Inactive portion of an If-Elif-Else-EndIf statement, but we hit an If, so we need
            #To not count the next 'EndIf' towards THIS one
            self.PushFlow('If', False, ['If', 'EndIf'])
            return
        self.PushFlow('If', bActive, ['If', 'Else', 'Elif', 'EndIf'], ifTrue=bActive, hitElse=False)

    def kwdElif(self, bActive):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'If' or self.PeekFlow().hitElse:
            error(UNEXPECTED % 'Elif')
        if self.PeekFlow().ifTrue:
            self.PeekFlow().active = False
        else:
            self.PeekFlow().active = bActive
            self.PeekFlow().ifTrue = self.PeekFlow().active or self.PeekFlow().ifTrue

    def kwdElse(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'If' or self.PeekFlow().hitElse:
            error(UNEXPECTED % 'Else')
        if self.PeekFlow().ifTrue:
            self.PeekFlow().active = False
            self.PeekFlow().hitElse = True
        else:
            self.PeekFlow().active = True
            self.PeekFlow().hitElse = True

    def kwdEndIf(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'If':
            error(UNEXPECTED % 'EndIf')
        self.PopFlow()

    def kwdWhile(self, bActive):
        if self.LenFlow() > 0 and self.PeekFlow().type == 'While' and not self.PeekFlow().active:
            # Within an un-true while statement, but we hit a new While, so we
            # need to ignore the next 'EndWhile' towards THIS one
            self.PushFlow('While', False, ['While', 'EndWhile'])
            return
        self.PushFlow('While', bActive, ['While', 'EndWhile'],
                      cLine=self.cLine - 1)

    def kwdContinue(self):
        #Find the next up While or For statement to continue from
        index = self.LenFlow()-1
        iType = None
        while index >= 0:
            iType = self.PeekFlow(index).type
            if iType in ['While','For']:
                break
            index -= 1
        if index < 0:
            # No while statement was found
            error(UNEXPECTED % 'Continue')
        #Discard any flow control statments that happened after
        #the While/For, since we're resetting either back to the
        #the While/For', or the EndWhile/EndFor
        while self.LenFlow() > index+1:
            self.PopFlow()
        flow = self.PeekFlow()
        if iType == 'While':
            # Continue a While loop
            self.cLine = flow.cLine
            self.PopFlow()
        else:
            # Continue a For loop
            if flow.ForType == 0:
                # Numeric loop
                if self.variables[flow.varname] == flow.end:
                    # For loop is done
                    self.PeekFlow().active = False
                else:
                    # keep going
                    self.cLine = flow.cLine
                self.variables[flow.varname] += flow.by
            elif flow.ForType == 1:
                # Iterator type
                flow.index += 1
                if flow.index == len(flow.List):
                    # Loop is done
                    self.PeekFlow().active = False
                else:
                    # Re-loop
                    self.cLine = flow.cLine
                    self.variables[flow.varname] = flow.List[flow.index]

    def kwdEndWhile(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'While':
            error(UNEXPECTED % 'EndWhile')
        #Re-evaluate the while loop's expression, if needed
        flow = self.PopFlow()
        if flow.active:
            self.cLine = flow.cLine

    def kwdFor(self, *args):
        if self.LenFlow() > 0 and self.PeekFlow().type == 'For' and not self.PeekFlow().active:
            #Within an ending For statement, but we hit a new For, so we need to ignore the
            #next 'EndFor' towards THIS one
            self.PushFlow('For', False, ['For', 'EndFor'])
            return
        varname = args[0]
        if varname.type not in [ScriptParser.VARIABLE,ScriptParser.NAME]:
            error(_("Invalid syntax for 'For' statement.  Expected format:")
                    +'\n For var_name from value_start to value_end [by value_increment]\n For var_name in SubPackages\n For var_name in subpackage_name'
                  )
        if args[1].text == 'from':
            #For varname from value_start to value_end [by value_increment]
            if (len(args) not in [5,7]) or (args[3].text != 'to') or (len(args)==7 and args[5].text != 'by'):
                error(_("Invalid syntax for 'For' statement.  Expected format:")
                      +'\n For var_name from value_start to value_end\n For var_name from value_start to value_end by value_increment'
                      )
            start = self.ExecuteTokens([args[2]])
            end = self.ExecuteTokens([args[4]])
            if len(args) == 7:
                by = self.ExecuteTokens([args[6]])
            elif start > end:
                by = -1
            else:
                by = 1
            self.variables[varname.text] = start
            self.PushFlow('For', True, ['For', 'EndFor'], ForType=0, cLine=self.cLine, varname=varname.text, end=end, by=by)
        elif args[1].text == 'in':
            # For name in SubPackages / For name in SubPackage
            if args[2].text == 'SubPackages':
                if len(args) > 4:
                    error(_("Invalid syntax for 'For' statement.  Expected format:")
                          +'\n For var_name in Subpackages\n For var_name in subpackage_name'
                          )
                List = sorted(self.sublist.keys())
            else:
                name = self.ExecuteTokens(args[2:])
                subpackage = name if name in self.sublist else None
                if subpackage is None:
                    error(_("SubPackage '%s' does not exist.") % name)
                List = []
                if isinstance(self.installer,bosh.InstallerProject):
                    sub = bass.dirs['installers'].join(self.path, subpackage)
                    for root_dir, dirs, files in sub.walk():
                        for file_ in files:
                            rel = root_dir.join(file_).relpath(sub)
                            List.append(rel.s)
                else:
                    # Archive
                    for file_, _size, _crc in self.installer.fileSizeCrcs:
                        rel = bolt.GPath(file_).relpath(subpackage)
                        if not rel.s.startswith('..'):
                            List.append(rel.s)
                List.sort()
            if len(List) == 0:
                self.variables[varname.text] = ''
                self.PushFlow('For', False, ['For','EndFor'])
            else:
                self.variables[varname.text] = List[0]
                self.PushFlow('For', True, ['For','EndFor'], ForType=1, cLine=self.cLine, varname=varname.text, List=List, index=0)
        else:
            error(_("Invalid syntax for 'For' statement.  Expected format:")
                  +'\n For var_name from value_start to value_end [by value_increment]\n For var_name in SubPackages\n For var_name in subpackage_name'
                  )

    def kwdEndFor(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'For':
            error(UNEXPECTED % 'EndFor')
        #Increment the variable, then test to see if we should end or keep going
        flow = self.PeekFlow()
        if flow.active:
            if flow.ForType == 0:
                # Numerical loop
                if self.variables[flow.varname] == flow.end:
                    #For loop is done
                    self.PopFlow()
                else:
                    #Need to keep going
                    self.cLine = flow.cLine
                    self.variables[flow.varname] += flow.by
            elif flow.ForType == 1:
                # Iterator type
                flow.index += 1
                if flow.index == len(flow.List):
                    self.PopFlow()
                else:
                    self.cLine = flow.cLine
                    self.variables[flow.varname] = flow.List[flow.index]
        else:
            self.PopFlow()

    def kwdSelectOne(self, *args):
        self._KeywordSelect(False, 'SelectOne', *args)

    def kwdSelectMany(self, *args):
        self._KeywordSelect(True, 'SelectMany', *args)

    def _KeywordSelect(self, bMany, name, *args):
        args = list(args)
        if self.LenFlow() > 0 and self.PeekFlow().type == 'Select' and not self.PeekFlow().active:
            #We're inside an invalid Case for a Select already, so just add a blank FlowControl for
            #this select
            self.PushFlow('Select', False, ['SelectOne', 'SelectMany', 'EndSelect'])
            return
        # Escape ampersands, since they're treated as escape characters by wx
        main_desc = args.pop(0).replace('&', '&&')
        if len(args) % 3:
            error(MISSING_ARGS % name)
        images = []
        titles = OrderedDict()
        descs = []
        image_paths = []
        while len(args):
            title = args.pop(0)
            is_default = title[0] == '|'
            if is_default:
                title = title[1:]
            titles[title] = is_default
            descs.append(args.pop(0))
            images.append(args.pop(0))
        if self.bAuto:
            # auto wizard will resolve SelectOne/SelectMany only if default(s)
            # were specified.
            defaults = [t for t, default in list(titles.items()) if default]
            if not bMany: defaults = defaults[:1]
            if defaults:
                self.PushFlow('Select', False,
                              ['SelectOne', 'SelectMany', 'Case',
                               'Default', 'EndSelect'], values=defaults,
                              hitCase=False)
                return
        self.choiceIdex += 1
        if self.reversing:
            # We're using the 'Back' button
            self.reversing -= 1
            self.PushFlow('Select', False, ['SelectOne', 'SelectMany', 'Case', 'Default', 'EndSelect'], values = self.choices[self.choiceIdex], hitCase=False)
            return
        # If not an auto-wizard, or an auto-wizard with no default option
        if self.bArchive:
            imageJoin = bass.getTempDir().join
        else:
            imageJoin = bass.dirs['installers'].join(self.path).join
        for i in images:
            path = imageJoin(i)
            if not path.exists() and bass.dirs['mopy'].join(i).exists():
                path = bass.dirs['mopy'].join(i)
            image_paths.append(path)
        self.page = PageSelect(self.parent, bMany, _('Installer Wizard'),
                               main_desc, list(titles.keys()), descs, image_paths,
                               list(titles.values()))

    def kwdCase(self, value):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'Select':
            error(UNEXPECTED % 'Case')
        if value in self.PeekFlow().values or str(value) in self.PeekFlow().values:
            self.PeekFlow().hitCase = True
            self.PeekFlow().active = True

    def kwdDefault(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'Select':
            error(UNEXPECTED % 'Default')
        if self.PeekFlow().hitCase:
            return
        self.PeekFlow().active = True
        self.PeekFlow().hitCase = True

    def kwdBreak(self):
        if self.LenFlow() > 0 and self.PeekFlow().type == 'Select':
            # Break for SelectOne/SelectMany
            self.PeekFlow().active = False
        else:
            # Test for a While/For statement earlier
            index = self.LenFlow() - 1
            while index >= 0:
                if self.PeekFlow(index).type in ('While', 'For'):
                    break
                index -= 1
            if index < 0:
                # No while or for statements found
                error(UNEXPECTED % 'Break')
            self.PeekFlow(index).active = False

            # We're going to jump to the EndWhile/EndFor, so discard
            # any flow control structs on top of the While/For one
            while self.LenFlow() > index + 1:
                self.PopFlow()
            self.PeekFlow().active = False

    def kwdEndSelect(self):
        if self.LenFlow() == 0 or self.PeekFlow().type != 'Select':
            error(UNEXPECTED % 'EndSelect')
        self.PopFlow()

    # Package selection functions
    def kwdSelectSubPackage(self, subpackage):
        self._SelectSubPackage(True, subpackage)

    def kwdDeSelectSubPackage(self, subpackage):
        self._SelectSubPackage(False, subpackage)

    def _SelectSubPackage(self, bSelect, subpackage):
        package = subpackage if subpackage in self.sublist else None
        if package:
            self.sublist[package] = bSelect
            for i in self.installer.espmMap[package]:
                if bSelect:
                    self._select_plugin(True, i)
                else:
                    if not self._plugin_in_active_package(i):
                        self._select_plugin(False, i)
        else:
            error(_("Sub-package '%s' is not a part of the installer.") % subpackage)

    def kwdSelectAll(self): self._SelectAll(True)
    def kwdDeSelectAll(self): self._SelectAll(False)

    def _SelectAll(self, bSelect):
        for i in list(self.sublist.keys()):
            self.sublist[i] = bSelect
        for i in list(self.plugin_list.keys()):
            self.plugin_list[i] = bSelect

    def kwd_select_plugin(self, plugin_name):
        self._select_plugin(True, plugin_name)

    def kwd_de_select_plugin(self, plugin_name):
        self._select_plugin(False, plugin_name)

    def _select_plugin(self, should_activate, plugin_name):
        resolved_name = self._resolve_plugin_rename(plugin_name)
        if resolved_name:
            self.plugin_list[resolved_name] = should_activate
        else:
            error(_("Plugin '%s' is not a part of the installer.") %
                  plugin_name)

    def kwd_select_all_plugins(self): self._select_all_plugins(True)
    def kwd_de_select_all_plugins(self): self._select_all_plugins(False)

    def _select_all_plugins(self, should_activate):
        for i in list(self.plugin_list.keys()):
            self.plugin_list[i] = should_activate

    def kwd_rename_plugin(self, plugin_name, new_name):
        plugin_name = self._resolve_plugin_rename(plugin_name)
        if plugin_name:
            # Keep same extension
            if plugin_name.lower()[-4:] != new_name.lower()[-4:]:
                raise ScriptParser.ParserError(_('Cannot rename %s to %s: '
                                                 'the extensions must '
                                                 'match.') %
                                               (plugin_name, new_name))
            self.plugin_renames[plugin_name] = new_name

    def kwd_reset_plugin_name(self, plugin_name):
        plugin_name = self._resolve_plugin_rename(plugin_name)
        if plugin_name and plugin_name in self.plugin_renames:
            del self.plugin_renames[plugin_name]

    def kwd_reset_all_plugin_names(self):
        self.plugin_renames = dict()

    def kwdNote(self, note):
        self.notes.append('- %s\n' % note)

    def kwdRequireVersions(self, game, se='None', ge='None', wbWant='0.0'):
        if self.bAuto: return
        gameWant = self._TestVersion_Want(game)
        if gameWant == 'None': game = 'None'
        seWant = self._TestVersion_Want(se)
        if seWant == 'None': se = 'None'
        geWant = self._TestVersion_Want(ge)
        if geWant == 'None': ge = 'None'
        if not wbWant: wbWant = '0.0'
        wbHave = bass.AppVersion
        ret = self._TestVersion(
            gameWant, bass.dirs['app'].join(*bush.game.version_detect_file))
        bGameOk = ret[0] >= 0
        gameHave = ret[1]
        if bush.game.se.se_abbrev != '':
            if bass.inisettings['SteamInstall']:
                seName = bush.game.se.steam_exe
            else:
                seName = bush.game.se.exe
            ret = self._TestVersion(seWant, bass.dirs['app'].join(seName))
            bSEOk = ret[0] >= 0
            seHave = ret[1]
        else:
            bSEOk = True
            seHave = 'None'
        if bush.game.ge.ge_abbrev != '':
            ret = self._TestVersion_GE(geWant)
            bGEOk = ret[0] >= 0
            geHave = ret[1]
        else:
            bGEOk = True
            geHave = 'None'
        try:
            bWBOk = float(wbHave) >= float(wbWant)
        except ValueError:
            # Error converting to float, just assume it's OK
            bWBOk = True
        if not bGameOk or not bSEOk or not bGEOk or not bWBOk:
            self.page = PageVersions(self.parent, bGameOk, gameHave, game,
                                     bSEOk, seHave, se, bGEOk, geHave, ge,
                                     bWBOk, wbHave, wbWant)

    def _TestVersion_GE(self, want):
        if isinstance(bush.game.ge.exe,str):
            files = [bass.dirs['mods'].join(bush.game.ge.exe)]
        else:
            files = [bass.dirs['mods'].join(*x) for x in bush.game.ge.exe]
        ret = [-1, 'None']
        for file in reversed(files):
            ret = self._TestVersion(want, file)
            if ret[1] != 'None':
                return ret
        return ret

    def _TestVersion_Want(self, want):
        try:
            need = [int(i) for i in want.split('.')]
        except ValueError:
            need = 'None'
        return need

    def _TestVersion(self, need, file_):
        if file_.exists():
            have = get_file_version(file_.s)
            ver = '.'.join([str(i) for i in have])
            if need == 'None':
                return [1, ver]
            for have_part, need_part in zip(have, need):
                if have_part > need_part:
                    return [1, ver]
                elif have_part < need_part:
                    return [-1, ver]
            return [0, ver]
        elif need == 'None':
            return [0, 'None']
        return [-1, 'None']

    def kwdReturn(self):
        self.page = PageFinish(self.parent, self.sublist, self.plugin_list,
                               self.plugin_renames, self.bAuto, self.notes,
                               self.iniedits)

    def kwdCancel(self, msg=_("No reason given")):
        self.page = PageError(self.parent, _('The installer wizard was canceled:'), msg)

bolt.codebox = WryeParser.codebox
