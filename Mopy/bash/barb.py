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

"""Backup/restore Bash settings. Settings paths are defined in
_init_settings_files().

Re: bass.AppVersion, bass.settings['bash.version']

The latter is read from the settings - so on upgrading Bash it's the version of
the previous Bash install, whereupon is based the backup-on-upgrade routine.
Later on, in basher.BashApp#InitVersion, bass.settings['bash.version'] is
set to bass.AppVersion. We save both in the settings we backup:
- bass.settings['bash.version'] is saved first and corresponds to the version
the settings were created with
- bass.AppVersion, saved second, is the version of Bash currently executing
the backup
"""

import pickle
import os
from os.path import join as jo

from . import archives
from . import bass # for settings (duh!)
from . import bolt
from . import initialization
from .bass import dirs, AppVersion
from .bolt import GPath, deprint
from .exception import BoltError, StateError, raise_bolt_error

def _init_settings_files(fsName_):
    """Construct a dict mapping directory paths to setting files. Keys are
    tuples of absolute paths to directories, paired with the relative paths
    in the backup file. Values are sets of setting files in those paths,
    or empty, meaning we have to list those paths and backup everything."""
    if not initialization.bash_dirs_initialized:
        raise BoltError('_init_settings_files: Bash dirs are not initialized')
    settings_info = {
        (dirs['mopy'], jo(fsName_, 'Mopy')): {'bash.ini', },
        (dirs['mods'].join('Bash'), jo(fsName_, 'Data', 'Bash')): {
            'Table.dat', },
        (dirs['mods'].join('Docs'), jo(fsName_, 'Data', 'Docs')): {
            'Bash Readme Template.txt', 'Bash Readme Template.html',
            'My Readme Template.txt', 'My Readme Template.html',
            'wtxt_sand_small.css', 'wtxt_teal.css', },
        (dirs['modsBash'], jo(fsName_ + ' Mods', 'Bash Mod Data')): {
            'Table.dat', },
        (dirs['modsBash'].join('INI Data'),
         jo(fsName_ + ' Mods', 'Bash Mod Data', 'INI Data')): {
           'Table.dat', },
        (dirs['bainData'],
         jo(fsName_ + ' Mods', 'Bash Installers', 'Bash')): {
           'Converters.dat', 'Installers.dat', },
        (dirs['saveBase'], jo('My Games', fsName_)): {
            'BashProfiles.dat', 'BashSettings.dat', 'BashLoadOrders.dat',
            'People.dat', },
        # backup all files in Mopy\bash\l10n, Data\Bash Patches\,
        # Data\BashTags\ and Data\INI Tweaks\
        (dirs['l10n'], jo(fsName_, 'Mopy', 'bash', 'l10n')): {},
        (dirs['mods'].join('Bash Patches'),
         jo(fsName_, 'Data', 'Bash Patches')): {},
        (dirs['mods'].join('BashTags'),
         jo(fsName_, 'Data', 'BashTags')): {},
        (dirs['mods'].join('INI Tweaks'),
         jo(fsName_, 'Data', 'INI Tweaks')): {},
    }
    for setting_files in settings_info.values():
        for settings_file in set(setting_files):
            if settings_file.endswith('.dat'): # add corresponding bak file
                setting_files.add(settings_file + '.bak')
    return settings_info

#------------------------------------------------------------------------------
class BackupSettings(object):
    """Create a 7z backup file with the settings files used by Bash. We need
    bass.dirs initialized and also bass.settings - to get the version of the
    settings we backup (bass.settings['bash.version']). Creates a backup.dat
    file that stores those versions."""

    def __init__(self, settings_file, fsName):
        self._backup_dest_file = settings_file # absolute path to dest 7z file
        self.files = {}
        for (bash_dir, tmpdir), setting_files in \
                _init_settings_files(fsName).items():
            if not setting_files: # we have to backup everything in there
                setting_files = bash_dir.list()
            tmp_dir = GPath(tmpdir)
            for name in setting_files:
                fpath = bash_dir.join(name)
                if fpath.exists():
                    self.files[tmp_dir.join(name)] = fpath
        # backup save profile settings
        savedir = GPath('My Games').join(fsName)
        profiles = [''] + initialization.getLocalSaveDirs()
        for profile in profiles:
            pluginsTxt = ('Saves', profile, 'plugins.txt')
            loadorderTxt = ('Saves', profile, 'loadorder.txt')
            for txt in (pluginsTxt, loadorderTxt):
                tpath = savedir.join(*txt)
                fpath = dirs['saveBase'].join(*txt)
                if fpath.exists(): self.files[tpath] = fpath
            table = ('Saves', profile, 'Bash', 'Table.dat')
            tpath = savedir.join(*table)
            fpath = dirs['saveBase'].join(*table)
            if fpath.exists(): self.files[tpath] = fpath
            if fpath.backup.exists(): self.files[tpath.backup] = fpath.backup

    @staticmethod
    def new_bash_version_prompt_backup(balt_, previous_bash_version):
        # return False if old version == 0 (as in not previously installed)
        if previous_bash_version == 0 or AppVersion == previous_bash_version:
            return False
        # return True if not same app version and user opts to backup settings
        return balt_.askYes(balt_.Link.Frame, '\n'.join([
            _('A different version of Wrye Bash was previously installed.'),
            _('Previous Version: ') + ('%s' % previous_bash_version),
            _('Current Version: ') + ('%s' % AppVersion),
            _('Do you want to create a backup of your Bash settings before '
              'they are overwritten?')]))

    @staticmethod
    def backup_filename(fsName_):
        return 'Backup Bash Settings %s (%s) v%s-%s.7z' % (
            fsName_, bolt.timestamp(), bass.settings['bash.version'],
            AppVersion)

    def backup_settings(self, balt_):
        deprint('')
        deprint(_('BACKUP BASH SETTINGS: ') + self._backup_dest_file.s)
        temp_settings_backup_dir = bolt.Path.tempDir()
        try:
            self._backup_settings(temp_settings_backup_dir)
            self._backup_success(balt_)
        finally:
            if temp_settings_backup_dir:
                temp_settings_backup_dir.rmtree(safety='WryeBash_')

    def _backup_settings(self, temp_dir):
        # copy all files to ~tmp backup dir
        for tpath, fpath in self.files.items():
            deprint(tpath.s + ' <-- ' + fpath.s)
            fpath.copyTo(temp_dir.join(tpath))
        # dump the version info and file listing
        with temp_dir.join('backup.dat').open('wb') as out:
            # Bash version the settings were saved with, if this is newer
            # than the installed settings version, do not allow restore
            pickle.dump(bass.settings['bash.version'], out, -1)
            # app version, if this doesn't match the installed settings
            # version, warn the user on restore
            pickle.dump(AppVersion, out, -1)
        # create the backup archive in 7z format WITH solid compression
        # may raise StateError
        backup_dir, dest7z = self._backup_dest_file.head, self._backup_dest_file.tail
        command = archives.compressCommand(dest7z, backup_dir, temp_dir)
        archives.compress7z(command, backup_dir, dest7z, temp_dir)
        bass.settings['bash.backupPath'] = backup_dir

    def _backup_success(self, balt_):
        if balt_ is None: return
        balt_.showInfo(balt_.Link.Frame, '\n'.join([
            _('Your Bash settings have been backed up successfully.'),
            _('Backup Path: ') + self._backup_dest_file.s]),
                       _('Backup File Created'))

    @staticmethod
    def warn_message(balt_):
        if balt_ is None: return
        balt_.showWarning(balt_.Link.Frame, '\n'.join([
            _('There was an error while trying to backup the Bash settings!'),
            _('No backup was created.')]), _('Unable to create backup!'))

#------------------------------------------------------------------------------
class RestoreSettings(object):
    """Class responsible for restoring settings from a 7z backup file
    created by BackupSettings. We need bass.dirs initialized to restore the
    settings, which depends on the bash.ini - so this exports also functions
    to restore the backed up ini, if it exists. Restoring the settings must
    be done on boot as soon as we are able to initialize bass#dirs."""
    __tmpdir_prefix = 'RestoreSettingsWryeBash_'
    __unset = object()

    def __init__(self, settings_file):
        self._settings_file = GPath(settings_file)
        self._saved_settings_version = self._settings_saved_with = None
        # bash.ini handling
        self._timestamped_old = self.__unset
        self._bash_ini_path = self.__unset
        # extract folder
        self._extract_dir = self.__unset

    # Restore API -------------------------------------------------------------
    def extract_backup(self):
        """Extract the backup file and return the tmp directory used. If
        the backup file is a dir we assume it was created by us before
        restarting."""
        if self._settings_file.isfile():
            temp_dir = bolt.Path.tempDir(prefix=RestoreSettings.__tmpdir_prefix)
            archives.extract7z(self._settings_file, temp_dir)
            self._extract_dir = temp_dir
        elif self._settings_file.isdir():
            self._extract_dir = self._settings_file
        else:
            raise BoltError(
                '%s is not a valid backup location' % self._settings_file)
        return self._extract_dir

    def backup_ini_path(self):
        """Get the path to the backup bash.ini if it exists - must be run
        before restore_settings is called, as we need the Bash ini to
        initialize bass.dirs."""
        if self._extract_dir is self.__unset: raise BoltError(
            'backup_ini_path: you must extract the settings file first')
        for r, d, fs in bolt.walkdir('%s' % self._extract_dir):
            for f in fs:
                if f == 'bash.ini':
                    self._bash_ini_path = jo(r, f)
                    break
        else: self.bash_ini_path = None
        return self._bash_ini_path

    def restore_settings(self, fsName):
        if self._bash_ini_path is self.__unset: raise BoltError(
            'restore_settings: you must handle bash ini first')
        if self._extract_dir is self.__unset: raise BoltError(
            'restore_settings: you must extract the settings file first')
        try:
            self._restore_settings(fsName)
        finally:
            self.remove_extract_dir(self._extract_dir)

    def _restore_settings(self, fsName):
        deprint('')
        deprint(_('RESTORE BASH SETTINGS: ') + self._settings_file.s)
        # backup previous Bash ini if it exists
        old_bash_ini = dirs['mopy'].join('bash.ini')
        self._timestamped_old = ''.join(
            [old_bash_ini.root.s, '(', bolt.timestamp(), ').ini'])
        try:
            old_bash_ini.moveTo(self._timestamped_old)
            deprint('Existing bash.ini moved to %s' % self._timestamped_old)
        except StateError: # does not exist
            self._timestamped_old = None
        # restore all the settings files
        restore_paths = list(_init_settings_files(fsName).keys())
        for dest_dir, back_path in restore_paths:
            full_back_path = self._extract_dir.join(back_path)
            for name in full_back_path.list():
                if full_back_path.join(name).isfile():
                    deprint(GPath(back_path).join(
                        name).s + ' --> ' + dest_dir.join(name).s)
                    full_back_path.join(name).copyTo(dest_dir.join(name))
        # restore savegame profile settings
        back_path = GPath('My Games').join(fsName, 'Saves')
        saves_dir = dirs['saveBase'].join('Saves')
        full_back_path = self._extract_dir.join(back_path)
        if full_back_path.exists():
            for root_dir, folders, files_ in full_back_path.walk(True,None,True):
                root_dir = GPath('.'+root_dir.s)
                for name in files_:
                    deprint(back_path.join(root_dir,name).s + ' --> '
                            + saves_dir.join(root_dir, name).s)
                    full_back_path.join(root_dir, name).copyTo(
                        saves_dir.join(root_dir, name))

    # Validation --------------------------------------------------------------
    def incompatible_backup_error(self, current_game):
        saved_settings_version, settings_saved_with = \
            self._get_settings_versions()
        if saved_settings_version > bass.settings['bash.version']:
            # Disallow restoring settings saved on a newer version of bash # TODO(ut) drop?
            return '\n'.join([
                _('The data format of the selected backup file is newer than '
                  'the current Bash version!'),
                _('Backup v%s is not compatible with v%s') % (
                    saved_settings_version, bass.settings['bash.version']),
                '', _('You cannot use this backup with this version of '
                       'Bash.')]), _(
                'Error: Settings are from newer Bash version')
        else:
            game_name = self._get_backup_game()
            if game_name != current_game:
                return '\n'.join(
                    [_('The selected backup file is for %(game_name)s while '
                       'your current game is %(current_game)s') % locals(),
                     _('You cannot use this backup with this game.')]), _(
                    'Error: Settings are from a different game')
        return '', ''

    def incompatible_backup_warn(self):
        saved_settings_version, settings_saved_with = \
            self._get_settings_versions()
        if settings_saved_with != bass.settings['bash.version']:
            return '\n'.join(
                [_('The version of Bash used to create the selected backup '
                   'file does not match the current Bash version!'),
                 _('Backup v%s does not match v%s') % (
                     settings_saved_with, bass.settings['bash.version']), '',
                 _('Do you want to restore this backup anyway?')]), _(
                'Warning: Version Mismatch!')
        return '', ''

    def _get_settings_versions(self):
        if self._extract_dir is self.__unset: raise BoltError(
            '_get_settings_versions: you must extract the settings file '
            'first')
        if self._saved_settings_version is None:
            backup_dat = self._extract_dir.join('backup.dat')
            try:
                with backup_dat.open('rb') as ins:
                    # version of Bash that created the backed up settings
                    self._saved_settings_version = pickle.load(ins)
                    # version of Bash that created the backup
                    self._settings_saved_with = pickle.load(ins)
            except (OSError, IOError, pickle.UnpicklingError, EOFError):
                raise_bolt_error('Failed to read %s' % backup_dat)
        return self._saved_settings_version, self._settings_saved_with

    def _get_backup_game(self):
        """Get the game this backup was for - hack, this info belongs to backup.dat."""
        for node in os.listdir('%s' % self._extract_dir):
            if node != 'My Games' and not node.endswith(
                    'Mods') and os.path.isdir(self._extract_dir.join(node).s):
                return node
        raise BoltError('%s does not contain a game dir' % self._extract_dir)

    # Dialogs and cleanup/error handling --------------------------------------
    @staticmethod
    def remove_extract_dir(backup_dir):
        backup_dir.rmtree(safety=RestoreSettings.__tmpdir_prefix)

    def restore_ini(self):
        if self._timestamped_old is self.__unset:
            return # we did not move bash.ini
        if self._timestamped_old is not None:
            bolt.deprint('Restoring bash.ini')
            GPath(self._timestamped_old).copyTo('bash.ini')
        elif self._bash_ini_path:
            # remove bash.ini as it is the one from the backup
            bolt.GPath('bash.ini').remove()

    @staticmethod
    def warn_message(balt_, msg=''):
        if balt_ is None: return
        balt_.showWarning(balt_.Link.Frame, '\n'.join([
            _('There was an error while trying to restore your settings from '
              'the backup file!'), msg, _('No settings were restored.')]),
                          _('Unable to restore backup!'))
