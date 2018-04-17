__RESET = "\033[0m"
__BOLD = "\033[1m"
__UNDERLINE = "\033[4m"
__REVERSE = "\033[7m"
__BLACK = "\033[30m"
__RED = "\033[31m"
__GREEN = "\033[32m"
__YELLOW = "\033[33m"
__BLUE = "\033[34m"
__MAGENTA = "\033[35m"
__CYAN = "\033[36m"
__WHITE = "\033[37m"
__ON_BLACK = "\033[40m"
__ON_RED = "\033[41m"
__ON_GREEN = "\033[42m"
__ON_YELLOW = "\033[43m"
__ON_BLUE = "\033[44m"
__ON_MAGENTA = "\033[45m"
__ON_CYAN = "\033[46m"
__ON_WHITE = "\033[47m"

__ON_DIY = "\033[0;34;40m"


def red(message):
    print __RED + message + __RESET


def yellow(message):
    print __YELLOW + message + __RESET


def blue(message):
    print __BLUE + message + __RESET


def green(message):
    print __GREEN + message + __RESET


def wrap_yellow(message):
    return __YELLOW + message + __RESET


def magenta(message):
    print __MAGENTA + message + __RESET


def green(message):
    print __GREEN + message + __RESET


def offset():
    return len(__YELLOW + __RESET)
