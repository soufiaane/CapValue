

class ExternalConfig(object):
    """
    Wrapper for ConfigParser
    Reads a section from a config file and provides an object with the
    properties and the values defined in the config.
    """

    def __init__(self, conf_file, section):
        """
        Reads the section "section" from the config "conf_file"
        """
        self._conf_file = conf_file
        self._section = section

        self._config = ConfigParser()
        self._config.read(self._conf_file)

        self._index = len(self._config.options(self._section))

    def __getattr__(self, name):
        """
        Read the property from the config
        """
        if name.startswith('_'):
            return self.__dict__[name]
        try:
            value = self._config.get(self._section, name)
            if value.isdigit():
                return int(value)
            elif value in ('True', 'False'):
                return value == 'True'
            else:
                return value
        except NoOptionError:
            raise AttributeError

    def __getitem__(self, name):
        """
        Read the property from the config
        """
        return self.__getattr__(name)

    def __iter__(self):
        """
        __iter__ method
        """
        return self

    def next(self):
        """
        next method
        """
        if self._index == 0:
            raise StopIteration
        self._index -= 1
        return self._config.options(self._section)[self._index]
