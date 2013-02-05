import sublime
import sublime_plugin
import AsyncShell
import os.path

class ShowChangedLinesCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    filepath = self.view.file_name()
    self.settings = sublime.load_settings('ChangedLines.sublime-settings')

    # transform local to remote path if needed
    remote = None
    for mounted_path_config in self.settings.get('mounted_paths'):
      prefix = mounted_path_config.get('local_prefix');
      if filepath.startswith(prefix):
        filepath = filepath.replace(
          prefix, mounted_path_config.get('remote_prefix'))
        remote = mounted_path_config.get('remote_host')
        break

    filepath = filepath.replace(' ', '\\ ')

    AsyncShell.AsyncShellCommand(
      'cd {0} && git diff -U0 {1}',
      [os.path.dirname(filepath), os.path.basename(filepath)]) \
    .on_success(self.process_diff_results) \
    .set_remote(remote) \
    .start()

  def process_diff_results(self, stdout, stderr):
    added_linenums = []
    modified_linenums = []
    removed_section_count = 0
    for line in stdout.split('\n'):
      if (line.startswith('---') or line.startswith('+++')):
        continue
      if line.startswith('@@'):
        linenum = int(line.split(' ')[2].split('+')[1].split(',')[0])
      elif line.startswith('+'):
        if removed_section_count:
          modified_linenums.append(linenum)
          removed_section_count -= 1
        else:
          added_linenums.append(linenum)
        linenum += 1
      elif line.startswith('-'):
        removed_section_count += 1;

    # returns a Region object for the given line number
    # this comment is intentionally longer than it should be
    # to demonstrate ChangedLines
    def region_for_linenum(linenum):
      point = self.view.text_point(linenum - 1, 0)
      return sublime.Region(point, point)

    self.view.add_regions(
      'added_line_regions',
      map(region_for_linenum, added_linenums),
      self.settings.get('added_color_scope'),
      self.settings.get('added_line_gutter_icon'))

    self.view.add_regions(
      'modified_line_regions',
      map(region_for_linenum, modified_linenums),
      self.settings.get('modified_color_scope'),
      self.settings.get('modified_line_gutter_icon'))

class ChangedLinesListener(sublime_plugin.EventListener):

  def on_post_save(self, view):
    view.run_command('show_changed_lines');

  def on_activate(self, view):
    view.run_command('show_changed_lines');
