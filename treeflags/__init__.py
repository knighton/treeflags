from argparse import Namespace 


class TreeFlags(Namespace):
    @classmethod
    def _is_flag(cls, name):
        if not isinstance(name, str):
            return False
        if not name:
            return False
        if name.startswith('_'):
            return False
        if '.' in name:
            return False
        return True

    @classmethod
    def _tree_to_argparse(cls, parent_keys, tree, parser):
        for key in sorted(tree):
            if not cls._is_flag(key):
                raise Exception('Invalid flag name: ' + str(key))
            value = tree[key]
            keys = parent_keys + [key]
            if isinstance(value, dict):
                cls._tree_to_argparse(keys, value, parser)
                continue
            flag = '--' + '.'.join(keys)
            if isinstance(value, type):
                parser.add_argument(flag, type=value, required=True)
            elif isinstance(value, (int, float, str)):
                parser.add_argument(flag, type=type(value), default=value)
            else:
                raise Exception('Unhandled type of value: ' + str(type(value)))

    @classmethod
    def _parse_flags(cls, tree):
        assert isinstance(tree, dict)
        from argparse import ArgumentParser
        parser = ArgumentParser()
        cls._tree_to_argparse([], tree, parser)
        return parser.parse_args()

    @classmethod
    def _is_public(cls, name):
        return not name.startswith('_')

    @classmethod
    def _each(cls, obj):
        for key in sorted(filter(cls._is_public, dir(obj))):
            value = getattr(obj, key)
            yield key, value

    def __lt__(self, tree):
        args = self._parse_flags(tree)
        for key, value in self._each(args):
            value = getattr(args, key)
            keys = key.split('.')
            parent = self
            for key in keys[:-1]:
                if not hasattr(parent, key):
                    setattr(parent, key, self.__class__())
                parent = getattr(parent, key)
            setattr(parent, keys[-1], value)


flags = TreeFlags()
