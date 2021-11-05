# Application configuration File
################################

# Directory To Watch, If not specified, the following value will be considered explicitly.
WATCH_DIRECTORY = "../UPLOAD"

# Delay Between Watch Cycles In Seconds
WATCH_DELAY = 10

# Check The WATCH_DIRECTORY and its children
WATCH_RECURSIVELY = True

# whether to watch for directory events
DO_WATCH_DIRECTORIES = True

# Patterns of the files to watch
WATCH_PATTERN = '.zip'

LOG_FILES_EXTENSIONS = ('.txt', '.log', '.trc')

# Patterns for observations
EXCEPTION_PATTERN = ['EXCEPTION', 'FATAL', 'ERROR']
