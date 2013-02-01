ChangedLines
======================

A Sublime Text 2 plugin that shows lines that have been added or modified since last git commit

![Screenshot](http://i.imgur.com/tjixeKA.png)

Example configuration:

`````javascript
 {
   // path to the icon that should be shown in the left gutter when lines
   // are added or modified, respectively
   "added_line_gutter_icon": "dot",
   "modified_line_gutter_icon": "dot",
 
   // Color theme 'scope' that should be applied to the gutter icons for
   // added and modified lines respectively
   // Color scopes are defined in .tmTheme color scheme files
   "added_color_scope": "vc.line.added",
   "modified_color_scope": "vc.line.modified"
 }
`````
