from shell import App

def morf(kwargs, echo=False):
    if 'm' in kwargs:
        ret = kwargs['m']['description']
        del kwargs['m']
        return ret
    elif 'f' in kwargs:
        try:
            with open(kwargs['f']['file']) as f:
                del kwargs['f']
                return f.read().strip()
        except OSError:
            print(App.config['failed_to_read'])
            return None
    print('必须指定-m或-f选项中的一个')
    return None

def search(kwargs):
    return '&'.join((f'{k}={v[0] if v else "_"}' for k, v in kwargs.items()))