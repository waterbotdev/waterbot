class TimeHelper:
    '''Useful module for converting times and shit.
    '''

    @staticmethod
    def sec_to_str(sec):
        m = 0
        h = 0
        d = 0
        s = sec
        while s >= 86400:
            d += 1
            s -= 86400
            print(f'Add D \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60*60:
            h += 1
            s -= 60*60
            print(f'Add S \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60:
            m += 1
            s -= 60
            print(f'Add M \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        return f'{d}d {h}h {m}m {s}s'
