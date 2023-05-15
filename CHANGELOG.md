# Changelog

## [1.3.0] - 2023-05-15

### Added

- Get the track title for various music trackers files (.it, .mod, .s3m, .xm)
- Added the filename to the cover search
- This changelog

### Changed

- Update the GitHub Workflow for make the AppImage to Ubuntu 20.04 from 18.04
- New notification system. The new system uses Qt5's own libraries and works on the AppImage. Based on this https://gist.github.com/codito/dbd64bdc8cd51c58741a59537874e0be
- Add and remove some dependencies

### Fixed

- Fix two configuration options
- Fix window icon on Wayland session

## [1.2.1] - 2022-07-29

### Added

- Added shortcuts for menú options

### Changed

- Move saved playlist check to the AddFilesFromArgs function on init.py. The reason for this is so that it only loads it if the -f parameter has been used, in addition to deleting it if's exists

### [1.2.0] - 2022-07-27

### Added

- Added option for active/desactive cover download in casi if not in folder or song metadata
- Now the menu opens when you press the button and not only when you click on the arrow.
- Added button on the playlist to add files .
- Now you can set if at close the app remember the current volume.
- Now you can set if at close the app remember the current playlist and load on start.

# Changed

- Translations updated
- Other changes

## [1.1.1] - 2022-07-13

### Added

- Now check if a cover is available on the current song folder. If the song metadata does not contain a cover, look for an image file called AlbumArtSmall, cover or folder.
- Added some trackers files to open file dialog. .mod, .s3m, .it and .xm are supported by GStreamer

## [1.1.0] - 2022-06-29

### Added

- New option: Define the default folder where the selection dialogs will be opened
- New option: Show notifications on change track
- New option: Minimice the window to systray instead of closing the application
- New function for check is another instance is running

## [1.0.0] 2022-05-17

### Added

- You can now add files and directories by dragging them to the window.
- Now check if the playlist it's on M3U format
- Added new command line argument: -f --files, to add files and/or folders from command line
- Add files from the context menu of the file browser
- More than one instance is prevented

### Changed

- Some code clean and optimizations

## [0.3.3] - 2022-05-16

### Added

- Added more options in the systray icon menu

## [0.3.2] - 2022-05-14

### Added

- Now when adding a folder the files are added in order
- Show track info on window's title and systray icon
- Rename the button menu variable

## [0.3.1] - 2022-05-12

### Added

- Added command line argument: --custom-theme. If this argument is passed it will use the theme created for the app, otherwise it will use the system theme. This argument is passed by default in the AppImage

## [0.3.0] - 2022-05-07

### Added

- Now you can open and saving playlists in M3U format
- Added icon in the system tray, that when clicked the window is shown/hidden, and when clicked with the right mouse button a menu is shown to control the player
- Add AUR (Arch Linux User Repository) package

### Changed

- Enable shuffle button
- Enable button for loop playback and switch between modes (once, loop, disable)

## [0.2.0] - 2022-04-29

### Added

- Added option for add folder (and subfolders)
- Check if file is a valid audio file
- Show/Hide playlist when resizing the window
- Add translation files (Spanish)
- Add track from URL (for example a online radio)
- Add places icons (necessary for file and folder opening dialogs)

### Changed

- Many corrections and performance

## [0.1.0] - 2022-04-25

### Changed

- First release

[1.3.0]: https://github.com/son-link/PQMusic/compare/v.1.2.1...v.1.3.0
[1.2.1]: https://github.com/son-link/PQMusic/compare/v.1.2.0...v.1.2.1
[1.2.0]: https://github.com/son-link/PQMusic/compare/v.1.1.1...v.1.2.0
[1.1.1]: https://github.com/son-link/PQMusic/compare/v.1.1.0...v.1.1.1
[1.1.0]: https://github.com/son-link/PQMusic/compare/v.1.0.0...v.1.1.0
[1.0.0]: https://github.com/son-link/PQMusic/compare/v.0.3.3...v.1.0.0
[0.3.3]: https://github.com/son-link/PQMusic/compare/v.0.3.2...v.0.3.3
[0.3.2]: https://github.com/son-link/PQMusic/compare/v.0.3.1...v.0.3.2
[0.3.1]: https://github.com/son-link/PQMusic/compare/v.0.3.0...v.0.3.1
[0.3.0]: https://github.com/son-link/PQMusic/compare/v.0.2.0...v.0.3.0
[0.2.0]: https://github.com/son-link/PQMusic/compare/v.0.1.0...v.0.2.0