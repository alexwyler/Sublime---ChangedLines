import sublime
import sublime_plugin
import subprocess

class ShowChangedLinesCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    arg_filename = self.view.file_name().replace(' ', '\\ ')
    script = 'git diff -U0 %s' % (arg_filename)
    proc = subprocess.Popen(
      script,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      shell=True)
    stdout, stderr = proc.communicate()

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

    settings = sublime.load_settings('ChangedLines.sublime-settings')
    self.view.add_regions(
      'added_line_regions',
      map(region_for_linenum, added_linenums),
      settings.get('added_color_scope'),
      settings.get('added_line_gutter_icon'))

    self.view.add_regions(
      'modified_line_regions',
      map(region_for_linenum, modified_linenums),
      settings.get('modified_color_scope'),
      settings.get('modified_line_gutter_icon'))

class ChangedLinesListener(sublime_plugin.EventListener):

  def on_post_save(self, view):
    view.run_command('show_changed_lines');

  def on_activate(self, view):
    view.run_command('show_changed_lines');
