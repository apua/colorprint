def get_stages(namespace):
    import re
    from ..attributes import color_attr_mapping

    sep = re.compile(namespace.separator)
    field_form = re.compile(r'((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?:?((?:\+|-)?\d+)?')
    group_form = re.compile(r'(?:\+|-)?\d+')
    color_form = re.compile(r'(?!\d)\w*')

    def colors2attr(colors):
        if not colors:
            if namespace.default is None:
                raise ValueError('it should be given at least one color')
            colors = namespace.default

        attr = ()
        for c in colors:
            try:
                _attr = color_attr_mapping[c]
            except KeyError as e:
                raise KeyError('color "{}" is not defined'.format(e.args[0]))
            attr += _attr
        return attr


    def field2slice(match):
        if ':' in match.group():
            return slice(*tuple(i and int(i) for i in match.groups()))

        i = int(match.group(1))
        if   i > 0:
            return slice(i-1,  i,    None)
        elif i == 0:
            return slice(None, None, None)
        elif i == -1:
            return slice(-1,   None, None)
        else:
            return slice(i,    i+1,  None)


    def patt2stage(cond):
        patt, cond_ = re.compile(cond[0]), cond[1:]

        gidc = []
        for idx, arg in enumerate(cond_):
            m = group_form.fullmatch(arg)
            if m:
                group_idx = int(m.group())
                if group_idx <= 0:
                    raise ValueError('group index should be greater than zero')
                gidc.append(group_idx)
            else:
                colors = cond_[idx:]
                break
        else:
            colors = ()
        if not gidc:
            gidc = [0]

        if any(color_form.fullmatch(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (patt, gidc, attr)


    def field2stage(cond):
        fields = []
        for idx, arg in enumerate(cond):
            m = field_form.fullmatch(arg)
            if m:
                fields.append(field2slice(m))
            else:
                colors = cond[idx:]
                break
        else:
            colors = ()

        if not fields:
            raise ValueError('should give at lease one field')

        if any(color_form.fullmatch(c) is None for c in colors):
            raise ValueError('something wrong with condition "%s"' % ' '.join(cond))

        attr = colors2attr(colors)
        return (fields, attr)


    def trans2stage(cond):
        cls = cond[0].__class__.__name__
        if cls == 'patt_arg':
            r = patt2stage(cond)
        else:
            r = field2stage(cond)
        return r


    stages = tuple(map(trans2stage, namespace.conditions))
    return (stages, sep)


def gen_coloring_func(stages, sep):
    from collections import OrderedDict

    def coloring_func(orig_string):
        string = orig_string.rstrip('\r\n')
        line_feed = orig_string[len(string):]


        def gen_field_pos(string):
            head = 0
            for m in sep.finditer(string):
                yield (head, m.start())
                head = m.end()
            yield (head, len(string))


        def gen_pos_color(stages):
            if any(len(stage)==2 for stage in stages):
                L = tuple(gen_field_pos(string))
                I = tuple(range(len(L)))

            for stage in stages:
                if len(stage)==2:
                    if len(L)==1:
                        continue
                    fields, color = stage
                    for idx in set(sum((I[s] for s in fields),())):
                        start, end = L[idx]
                        yield (start, end, color)
                else:
                    patt, gnums, color = stage
                    for m in patt.finditer(string):
                        for gn in gnums:
                            if gn > len(m.groups()) or m.start(gn)==m.end(gn):
                                continue
                            yield (m.start(gn), m.end(gn), color)


        def gen_slices(states):
            keys = list(states.keys())
            for z in zip([0]+keys, keys+[None]):
                yield slice(*z)


        def gen_attr(states):
            state = []
            for move in states.values():
                if move['add']:
                    state.extend(move['add'])
                for color in move['del']:
                    state.remove(color)
                yield sum(state,())


        def attr2ctrl(attr):
            return '\x1b[{}m'.format(';'.join(map(str, attr)))

        states = {}
        for start, end, color in gen_pos_color(stages):
            states.setdefault(start, {'add':[], 'del':[]})['add'].append(color)
            states.setdefault(end,   {'add':[], 'del':[]})['del'].append(color)
        states = OrderedDict(sorted(states.items(), key=lambda t:t[0]))

        if len(states)==0:
            return orig_string
        else:
            colored_form = '{}'+'{}'.join(map(attr2ctrl, gen_attr(states)))+'{}'+line_feed
            return colored_form.format(*(string[s] for s in gen_slices(states)))


    return coloring_func


def colorprint(args, input_stream=None, output_stream=None):
    import sys

    if input_stream is None:
        input_stream = sys.stdin

    if output_stream is None:
        output_stream = sys.stdout

    try:
        stages, sep = get_stages(args)
    except (ValueError, KeyError) as e:
        raise Exception('e.args[0]') 

    coloring = gen_coloring_func(stages, sep)
    for line in input_stream:
        output_stream.write(coloring(line))
