# treeflags

### 1. Overview

- Treeflags is an extremely simple wrapper over python argparse.

- Bare minimum of features, with minimal boilerplate -- cleaner and faster?

- Sweet spot of usage is probably for rapid prototyping.

### 2. Example

```py
from argparse import ArgumentParser
from treeflags import flags


def demo_treeflags():
    flags < {
        'data': {
            'dataset': str,
            'root': 'data/',
        },
        'train': {
            'device': 'cuda:0',
            'num_epochs': 1000,
            'batch_size': 64,
        },
        'optim': {
            'name': 'sgd',
            'lr': 1e-2,
        },
        'model': {
            'name': 'baseline',
            'dim': int,
        },
        'ux': {
            'tqdm': 1,
            'log': '',
        },
    }

    print('Parsed using treeflags:')
    print('- ', flags)
    print('- flags.train.num_epochs =', flags.train.num_epochs)
    print()


def demo_argparse():
    parser = ArgumentParser()
    parser.add_argument('--data.dataset', type=str, required=True)
    parser.add_argument('--data.root', type=str, default='data/')
    parser.add_argument('--train.device', type=str, default='cuda:0')
    parser.add_argument('--train.num_epochs', type=int, default=1000)
    parser.add_argument('--train.batch_size', type=int, default=64)
    parser.add_argument('--optim.name', type=str, default='sgd')
    parser.add_argument('--optim.lr', type=float, default=1e-2)
    parser.add_argument('--model.name', type=str, default='baseline')
    parser.add_argument('--model.dim', type=int, required=True)
    parser.add_argument('--ux.tqdm', type=int, default=1)
    parser.add_argument('--ux.log', type=str, default='')
    args = parser.parse_args()

    print('Parsed using argparse:')
    print('- args = %s' % args)
    print("- getattr(args, 'train.num_epochs') = %d" %
          getattr(args, 'train.num_epochs'))
    print()


def main():
    demo_treeflags()
    demo_argparse()


if __name__ == '__main__':
    main()
```

### 3. Highly opinionated

- It only creates two-dash arguments.  One-dash arguments are considered sin, considering the ease of using recursive namespaces in this scheme.

- Nargs not equal to 1?  Custom anything?  This library takes the position that such open-ended complexity does not belong in the flag definitions.

- Booleans flags are also eliminated (`--flag` or `--no-flag`); define them as int (`--flag 1` or `--flag 0`) instead.

### 4. Details

- It works by internally instantiating an ephemeral `argparse.ArgumentParser` when `<` is called, treating instance arguments as defaults and arguments given by types as required.  `flags` subclasses `argparse.Namespace`.
