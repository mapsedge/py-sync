# py-sync

# Disclaimer
This software is provided "as-is," without any warranty of any kind. The authors are not responsible for any damages or issues that may arise from its use. Use at your own risk.

# Description
Automatically syncs a saved local file to an FTP server at the moment when it is saved

My process is to work directly against an FTP server: connect via Dolphin, open the file, edit, save, and the file is automatically updated on the server. (The same works with WinSCP on Windows.) 

My preferred editor is VSCode/ium, but I can't use it with this workflow because of a bug with .js files: on opening a .js file, it begins FTP bombing my server with CWD commands, trying to find "node_modules." (The VSCode/ium teams refuse to acknowledge it as an issue.)

Using this script, I can download my site's code to a local folder, run this script, and use the same workflow with local files, and no FTP bombing!

Drop the file into a convenient location. Change the settings to your site/uid/password/local folder. Run.  Edit locally.
