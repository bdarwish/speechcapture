
# Change Log
The changes of each release is documented here.

## [v0.4.1] - 2025-08-9
This release fixes a major bug that prevented any use.

### Fixed
[Commit 3088b86](https://github.com/bdarwish/speechcapture/commit/3088b86347cbe2f40c4ae10747603c5d8b55a786) Fixed bug caused by leftover debug lines of code

## [v0.4.0] - 2025-08-8
This release adds the `pause_on_end` attribute to the `Recorder` class, used to automatically pause the recording instead of stopping.

### Added
[Commit 76e820a](https://github.com/bdarwish/speechcapture/commit/76e820ad5b0e9ce4eb12a05edb2ba7fd8af56ab3) Added pause_on_end

## [v0.3.0] - 2025-08-7
This release adds the `max_duration` attribute to the `Recorder` class.

### Added
[Commit 1d21566](https://github.com/bdarwish/speechcapture/commit/1d2156659f97feae99891a3e6258ab7ba3444e8f) Added max_duration to the Recorder class

### Changed
[Commit e6642f8](https://github.com/bdarwish/speechcapture/commit/e6642f80e95f7048c284685f377492b212540f54) Updated CHANGELOG.md

## [v0.2.4] - 2025-08-6
This release fixes a critical bug and removes leftover debug lines of code. 

### Changed
- [Commit 4243790](https://github.com/bdarwish/speechcapture/commit/4243790d9b8d33609eb4f4304e022e08510e29e2) Removed leftover debug lines of code

### Fixed
- [Commit 4243790](https://github.com/bdarwish/speechcapture/commit/4243790d9b8d33609eb4f4304e022e08510e29e2) Fixed a bug with record() never breaking out of the loop, causing an OSError.

## [v0.2.2] - 2025-08-6
This release fixes the version of dependencies and Python required.

### Changed
- [Commit d58100b](https://github.com/bdarwish/speechcapture/commit/d58100b9c3526d75236c4b199ddb2c16ca4c4842) Lowers the required version of: Python to 3.8 or higher, NumPy to 1.20 or higher, and PyAudio to 0.2.11 or higher.

## [v0.2.1] - 2025-08-6
This release fixes a minor error in the README file of the project

### Changed
- [Commit 143e681](https://github.com/bdarwish/speechcapture/commit/143e681514be4e9a54ac8549fb40a72ddd9d3231) Updated README.md to state the correct requirement of Python 3.11 or higher
 
## [v0.2.0] - 2025-08-6
Initial release